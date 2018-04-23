A simple relay for visualization links.

Initial use case is to link render with neuroglancer.

Usage:
    docker build . -t vizrelay
    docker run --init --rm -p 5000:5000 vizrelay