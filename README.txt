	          USER MANUAL

1. Install elasticsearch, deactivate all the security features in 
/etc/elasticsearch/elasticsearch.conf, run the service with 
`systemctl start elasticsearch`

2. Install the datasets by running the install_data.sh script.

3. Install the virtual environment by running the install_virtualenv.sh
script.

4. Enter the python virtual environment by running 
`source env/bin/activate`

5. Load the ISDX dataset in elasticsearch by running 
data_to_elastic_db.py

6. You can see data has been successfully loaded by running api_demo.py

7. Download the challenge 1 data in moodle

8. Run challenge1.py to generate the result file.

9. Run challenge2.py to generate the challenge 2 result file
(it can take a while).

10. You can always run cross_validation.py to cross validate models on
the ISDX dataset for a specific protocol or application.

