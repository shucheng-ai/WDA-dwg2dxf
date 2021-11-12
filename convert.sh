#!/bin/bash

TEMP=$1
INPUT=$2
OUTPUT=$3
FORMAT=$4

if [ -z "$OUTPUT" ]
then
    echo "Usage: $0 <temp_dir> <input> <output> <DXF|DWG>"
    exit
fi

if [ -z "$FORMAT" ]
then
    FORMAT=DXF
fi

mkdir -p "$TEMP"
TEMP=`readlink -e $TEMP`

if [ ! -d "$TEMP" ]
then
    echo $TEMP is not a directory
    exit
fi

#input_bname=`basename $INPUT`
#output_bname=`basename $OUTPUT`

rm -rf "$TEMP/*"
mkdir -p $TEMP/input $TEMP/output
chmod a+rwx $TEMP/output
cp "$INPUT" $TEMP/input/

echo RUNNING ODAFileConverter IN DOCKER

#docker run -u`id -u`:`id -g` -v $TEMP/input:/input -v $TEMP/output:/output wda/oda
if [ -f /convert_helper.sh ]
then
xvfb-run /usr/bin/ODAFileConverter_21.3.0.0/ODAFileConverter $TEMP/input $TEMP/output ACAD2007 $FORMAT 0 1
else
docker run --rm -v $TEMP/input:/input -v $TEMP/output:/output wda/oda /convert_helper.sh $FORMAT
fi
cp $TEMP/output/* $OUTPUT

