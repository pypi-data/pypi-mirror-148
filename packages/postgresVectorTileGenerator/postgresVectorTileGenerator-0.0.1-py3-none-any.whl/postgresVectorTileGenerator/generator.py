# -*- coding: utf-8 -*-
"""
Module for generating zxy tiles
.. module:: tileGenerator.generator
   :platform: Unix, Windows
   :synopsis: Module for generating zxy tiles
"""

import os
import time
import logging
import sys
import psycopg2
from psycopg2 import pool
from VectorTileGenerator import generator


root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

class GenerateTiles():
    """
    This class provides you the ability to generate zxy tiles from postgres
    """

    def __init__(self, cache_folder:str ,db_host:str, db_port:int, db_user:str, db_password:str, db_database:str, db_table:str, min_zoom:int, max_zoom:int, bounds:list=[-180, -90, 180, 90]):
        """
        Init method

        :param cache_folder: The minimum zoom level to start generating tiles.
        :param db_host: The maximum zoom level to stop generating tiles.
        :param db_port: The bounding box to generate tiles from.
        :param db_user: The bounding box to generate tiles from.
        :param db_password: The bounding box to generate tiles from.
        :param db_database: The bounding box to generate tiles from.
        :param db_table: The bounding box to generate tiles from.
        :param min_zoom: The bounding box to generate tiles from.
        :param max_zoom: The bounding box to generate tiles from.
        :param bounds: The bounding box to generate tiles from.
        :type minZoom: int
        :type maxZoom: int
        :type bounds: list

        """

        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_password = db_password
        self.db_database = db_database
        self.db_table = db_table
        self.cache_folder = cache_folder

        tileGeneration = generator.GenerateTiles(min_zoom, max_zoom, bounds)

        self.tiles = tileGeneration.generate()
    
    def generate(self):
        """
        Generate a list of tiles at to tile_cache folder for each given zoom level with the given bounds.

        :return:
            A request response string
        """
        db_pool = psycopg2.pool.SimpleConnectionPool(
            1,
            20,
            dbname=self.db_database,
            user=self.db_user,
            host=self.db_host,
            password=self.db_password,
            port=self.db_port,
        )
        
        for tiles in self.tiles:
            start_time = time.time()
            logging.info(f"Generating tiles for zoom level: {tiles}")
            for tile in self.tiles[tiles]:
                ps_connection = db_pool.getconn()     
                cur = ps_connection.cursor()           

                sql_field_query = f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{self.db_table}'
                and column_name != 'geom';
                """

                cur.execute(sql_field_query)
                fields = cur.fetchall()

                field_list = ""

                for field in fields:
                    field_list += f", {field[0]}"
                
                sql_vector_query = f"""
                SELECT ST_AsMVT(tile, '{self.db_table}', 4096)
                FROM (
                    WITH
                    bounds AS (
                        SELECT ST_TileEnvelope({tile[0]}, {tile[1]}, {tile[2]}) as geom
                    )
                    SELECT
                        st_asmvtgeom(
                            ST_Transform(t.geom, 3857)
                            ,bounds.geom
                        ) AS mvtgeom {field_list}
                    FROM {self.db_table} as t, bounds
                    WHERE ST_Intersects(
                        ST_Transform(t.geom, 4326),
                        ST_Transform(bounds.geom, 4326)
                    ) 	
                ) as tile
                """
                    
                cur.execute(sql_vector_query)
                tile_data = cur.fetchall()[-1][-1]

                db_pool.putconn(ps_connection)

                if not os.path.exists(f"{self.cache_folder}/{self.db_table}/{tile[0]}/{tile[1]}"):
                    os.makedirs(f"{self.cache_folder}/{self.db_table}/{tile[0]}/{tile[1]}")

                f = open(f"{self.cache_folder}/{self.db_table}/{tile[0]}/{tile[1]}/{tile[2]}", "wb")
                f.write(tile_data)
                f.close()

            end_time = round((time.time() - start_time), 2)

            logging.info(f"Generated tiles for zoom level: {tiles}")
            logging.info(f"It took {end_time} seconds to generate tiles.")
                        
        return "Tiles generated."


