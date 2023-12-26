#!/bin/sh

dir=~/ids-martinmilou
mkdir $dir
file=$dir/dataset.zip
cookies=/tmp/cookies.txt
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1YX7qBa4xZt_Y_Dnc3OSWEa1DK5bdXYV7' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1YX7qBa4xZt_Y_Dnc3OSWEa1DK5bdXYV7" -O $file && rm -rf $cookies
unzip $file -d $dir
