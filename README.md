# EdaxCluster

## Description
This is a Python library to create an [Edax](https://github.com/abulmo/edax-reversi) cluster.
It requires at least Python 3.10, and the libraries listed in pyproject.toml.

## Installation
Run `pip install .` to install the package and all its dependencies.

## Run
`python3 run_server.py` starts a grpc server that listens on port 50051.
`python3 run_client.py <file> (<ip> <lower_empty_count> <upper_empty_count>)` starts a client that connects to a server at the given ip. It reads a scored game file and sends the positions between lower_empty_count and upper_empty_conut to the server. Once all positions are solved, the scores are written back to the file.
`python run_worker.py (<ip>)` starts a worker, that connects to the server at the given ip. It receives positions and solves them with Edax. One instance per CPU thread. The results are sent back to the server.
Omitted IPs default to `localhost`.
