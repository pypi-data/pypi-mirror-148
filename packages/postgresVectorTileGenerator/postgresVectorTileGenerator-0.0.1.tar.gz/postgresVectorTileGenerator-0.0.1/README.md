# postgresVectorTileGenerator

A python package to automatically generate a cache of vector tiles between two zoom levels and a bounding box for a table in postgreSQL.

## Install
`pip install postgresVectorTileGenerator`

## How to use
```
import os
from postgresVectorTileGenerator import generator

cache_location = f"{os.getcwd()}/cache"

tileGeneration = generator.GenerateTiles(cache_location, "localhost", 5432, "postgres", "postgres", "data", "states", 1, 5, [-118, 34, -84, 50])

tileGeneration.generate()
```