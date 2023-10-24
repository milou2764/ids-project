apt install install virtualenv
virtualenv env
source env/bin/activate

pip3 install -r requirements.txt

python3 scripts/ids_on_elastic_data.py
python scripts/api_demo.py
