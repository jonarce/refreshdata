#!/usr/bin/env python
# pip3 install csv
"""refreshdata.py: Refresh Data in a system from any given source (database, csv, xml file)."""
from gi.types import nothing
from orca import input_event
from zim import datetimetz

__author__      = "Jon Arce"
__copyright_    = "Copyright 2020"
__credits__     = ["Jon Arce"]
__license__     = "Apache"
__version__     = "1.0.2"
__maintainer__  = "Jon Arce"
__email__       = "jon.arce@gmail.com"
__status__      = "Production"

# DEPENDENCIES:
#   pip3 install xmltodict
#

import sys
import yaml
import base64
import datetime
#from posix import getcwd
import xmltodict
#import xml.etree.ElementTree as xml
import csv
from string import Template
# Database: Postgres
import psycopg2

# Function to substitute placeholders for actual values commming from the source
def replace_vals(str_template, vals):
    # escape any required SQL character
    for key, value in vals.items():
        # set empty values to NONE
        if empty(value):
            vals[key] = 'NULL'
        # escape required SQL characters in strings
        elif isinstance(value, str):
            vals[key] = value.replace('\'', '\"')
    t=Template(str_template)
    return t.substitute(vals)

# Check if variable is empty
def empty(value):
    if isinstance(value, datetime.datetime):
        return False
    else:
        if not value:
            return True
        else:
            return False


if __name__ == '__main__':
    now = datetime.datetime.now()
    lines = 0
    print("Starting job..." + str(now))
    # Print arguments one by one
    job_file = str(sys.argv[1])
    #check if job file exists
    try:
        f = open(job_file)
    # Do something with the file
    except FileNotFoundError:
        print("ERROR: YAML file not accessible")
        sys.exit()
    finally:
        f.close()
    print ('Job file:',  job_file)

    # read all YAML parameters in a Dict.
    with open(job_file) as f:   
        job_doc = yaml.load(f, Loader=yaml.FullLoader)
    
    print('JOB NAME: ',job_doc['job']['common']['job-name'])
    print('JOB TYPE: ',job_doc['job']['common']['mode'])
    print(job_doc)

    # Open source
    if (job_doc['job']['source']['mode'] == 'file'):
        # open database connection
        check_exists_sql = job_doc['job']['target']['check-exists-sql']
        conn = psycopg2.connect(
                host=job_doc['job']['target']['server'],
                database=job_doc['job']['target']['database'],
                user=str(base64.urlsafe_b64decode(job_doc['job']['target']['user']), "utf-8"),
                password=str(base64.urlsafe_b64decode(job_doc['job']['target']['password']), "utf-8"))
        cur = conn.cursor()
        
        # file reader settings
        file_name = job_doc['job']['source']['file-name']
        file_encoding = job_doc['job']['source']['encoding']
        file_dialect = job_doc['job']['source']['dialect']
        file_delimiter = job_doc['job']['source']['delimiter']
        file_quotechar = job_doc['job']['source']['quote-char']
        # open as a dictionary
        source_reader = csv.DictReader(open(file_name, "rt", encoding = file_encoding),
                                            dialect = file_dialect,
                                            # fieldnames=job_doc['job']['source']['headers'],
                                            #delimiter=',', quotechar='"')
                                        delimiter = file_delimiter,
                                        quotechar = file_quotechar
                                        )
        check_exists_sql = job_doc['job']['target']['check-exists-sql']
        insert_sql = job_doc['job']['target']['insert-sql']
        update_sql = job_doc['job']['target']['update-sql']
        
        timestamp = datetime.datetime.now()
        timestamp_field = job_doc['job']['target']['timestamp']
        
        # delete old records / not touched by this batch 
        before_import_sql = job_doc['job']['target']['before-import-sql']
        if not empty(before_import_sql):
            print(' BEFORE IMPORT...', end="")
            job_params = {}
            # add timestamp to row of data
            job_params[timestamp_field] = timestamp
            sql_query = replace_vals(before_import_sql, job_params)
            print(sql_query)
            cur.execute(sql_query)
            conn.commit()
        
        
        for data_row in source_reader:
            # add timestamp to row of data
            data_row[timestamp_field] = timestamp
            print(lines+1, ":", end="")
            
            # check if record exists
            check_sql_query = replace_vals(check_exists_sql, data_row)
            cur.execute(check_sql_query)
            check_records = cur.fetchall()
            
            # if record exists then UPDATE
            if (cur.rowcount):
                print(' UPDATE...', end="")
                sql_query = replace_vals(update_sql, data_row)
            # if new record then INSERT
            else:
                print(' INSERT...', end="")
                sql_query = replace_vals(insert_sql, data_row)
            
            # print('SQL Query: ',sql_query)
            cur.execute(sql_query)
            conn.commit()

            lines += 1
            print([(k, data_row[k]) for k in data_row])
            # input("Press Enter to continue...")
    
    # delete old records / not touched by this batch 
    delete_old_sql = job_doc['job']['target']['delete-old-sql']
    if not empty(delete_old_sql):
        print(' DELETE...', end="")
        job_params = {}
        # add timestamp to row of data
        job_params[timestamp_field] = timestamp
        sql_query = replace_vals(delete_old_sql, job_params)
        print(sql_query)
        cur.execute(sql_query)
        conn.commit()
    
    # execute the after-import-sql 
    after_import_sql = job_doc['job']['target']['after-import-sql']
    if not empty(after_import_sql):
        print(' AFTER IMPORT...', end="")
        job_params = {}
        # add timestamp to row of data
        job_params[timestamp_field] = timestamp
        sql_query = replace_vals(after_import_sql, job_params)
        print(sql_query)
        cur.execute(sql_query)
        conn.commit()

    # print end of job
    now = datetime.datetime.now()
    print('   ending job...',str(now),' lines:',str(lines))    
    # close database
    cur.close()
    conn.close()
    f.close()
    
# EOF