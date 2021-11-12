#!/bin/bash

if [ "$1" == "shell" ]
then
    echo "open shell:"
    path=$(cd "$(dirname "$0")";pwd)
    echo "$path"
    cd ..
    basepath=$(cd "$(dirname "$0")";pwd)
    echo "$basepath"
    cd "$path"
    pwd
    echo "/www/dwg2dxf"
    docker run -it --rm -p 8001:8001 -v $basepath:/www cyborg/dwg2dxf /bin/bash
else
    echo "run server:"
    cd docker
    docker-compose -f docker-compose.yml up -d
fi
