## Overview

API implemented in python, FastAPI framework. 
SQLite database was chosen for easiest run and testing as standalone DB like Postgres requires docker-compose.yml with separate Postgres container.

## Run
```
docker build -t trucks-load .
docker run -p 8000:8000 trucks-load
```
Go to `localhost:8000/docs` to see available endpoints

## Code and data structure improvements (if I had more time)

- 'Loading' table to keep relation between trucks and packages. Each loading contains id, track_id, date. Each package instead of track_id has loading_id

## Enhanced approach
fdf