#!/bin/bash

set -m

if [ -z "$1" ]
then
    exit
fi
xvfb-run /usr/bin/ODAFileConverter_21.3.0.0/ODAFileConverter /input /output ACAD2007 $1 0 1
