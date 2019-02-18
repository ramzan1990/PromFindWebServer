#!/bin/bash -i
set -e
find PromID/files -mtime +5 -type f -delete
b=$(basename $1)
python PromID/pipeline/predictor_padding.py PromID/model_1 $1 600 1 PromID/files/${b}_output.txt $3 $4 > $2
touch "${2}_cf"
#python PromID/pipeline/choose_prom.py PromID/files/${b}_output.txt 