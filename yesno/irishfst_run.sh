#!/bin/bash
# loop through all files in directory and process all 
# 1. tokenize input text
# 2. flookup morphological analysis
# 3. convert to required CG i/p format
# 4. vislcg3  disambiguation
# elaine oct 2012,  Noah (iandioch11@gmail.com) June 2018

IRISHFST=~/work/irishfst
cat /dev/stdin | sed -E 's/(\S)([.,!?])/\1 \2/g' | tr -sc "[0-9a-zA-ZáéíóúÁÉÍÓÚ.?!,]" "[\n*]" | flookup -a $IRISHFST/bin/lexguess.fst | perl $IRISHFST/dis/lookup2cg3.prl | vislcg3 -g $IRISHFST/dis/gael-dis.rle
