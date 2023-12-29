#!/bin/sh

data_dir=$(dirname $(readlink -f "$0"))/../data
mkdir -p $data_dir

download_data(){
  id=$1
  file=$data_dir/dataset.zip
  cookies=/tmp/cookies.txt
  wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id='$id -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=$id" -O $file && rm -rf $cookies
  unzip $file -d $data_dir
  rm $file
}
download_data 1YX7qBa4xZt_Y_Dnc3OSWEa1DK5bdXYV7
download_data 1qu2XLryTVs_x-5tWRwdooySv3t4RTQUA
download_data 1-REguw4C1IhqFkRPXXc_NUjNLE56-wBw
