#!/bin/bash -i
find PromID/files -mtime +5 -type f -delete
python PromID/pipeline/predictor_padding.py PromID/model_1 $1 251 1 PromID/files/output.txt
python PromID/pipeline/choose_prom.py PromID/files/output.txt 