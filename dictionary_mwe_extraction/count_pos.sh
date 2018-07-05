#!/bin/bash

COL=$1 # 2
FILE=$2 # mwes.ga

awk -v col="$COL" -F $'\t' '   {c[$col]++}
                 END{
                     for (i in c) printf("%s,%s\n",i,c[i])
                 }' $FILE
