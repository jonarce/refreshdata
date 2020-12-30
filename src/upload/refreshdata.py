#!/usr/bin/env python
# pip3 install csv
"""refreshdata.py: Refresh Data in a system from any given source (database, csv, xml file)."""
from gi.types import nothing

__author__      = "Jon Arce"
__copyright_    = "Copyright 2020"
__credits__     = ["Jon Arce"]
__license__     = "Apache"
__version__     = "1.0.1"
__maintainer__  = "Jon Arce"
__email__       = "jon.arce@gmail.com"
__status__      = "Production"

# DEPENDENCIES:
#   pip3 installl xmltodict
#

import sys
import os
import datetime
from posix import getcwd
import xmltodict
import xml.etree.ElementTree as xml
import csv
from string import Template
# Database: Postgres
import psycopg2

# Function to substitute placeholders for actual values commming from the source
def replace_vals(str_template, vals):
    t= Template(str_template)
    return t.substitute(vals)


if __name__ == '__main__':
    now = datetime.datetime.now()
    lines = 0
    print("Starting job ..." + str(now))
    # Print arguments one by one
    job_file = str(sys.argv[1])
    #check if job file exists
    try:
        f = open(job_file)
    # Do something with the file
    except FileNotFoundError:
        print("ERROR: XML file not accessible")
        sys.exit()
    finally:
        f.close()
    print ('Job file:',  job_file)

    # read all XML parameters in a Dict.
    with open(job_file) as fd:
        job_doc = xmltodict.parse(fd.read())
    
    print('JOB NAME: ',job_doc['job']['common']['job-name'])
    print('JOB TYPE: ',job_doc['job']['common']['@type'])
    print(job_doc)

    # Open source
    if (job_doc['job']['source']['@type'] == 'file'):
        # open database connection
        check_exists_sql = job_doc['job']['target']['check-exists-sql']
        conn = psycopg2.connect(
        host=job_doc['job']['target']['server'],
        database=job_doc['job']['target']['database'],
        user=job_doc['job']['target']['user'],
        password=job_doc['job']['target']['password'])
        file_name = job_doc['job']['source']['file-name']
        file_encoding = job_doc['job']['source']['encoding']
        file_dialect = job_doc['job']['source']['dialect']
        file_delimiter = job_doc['job']['source']['delimiter']
        file_quotechar = job_doc['job']['source']['quote-char']
        source_reader = csv.DictReader(open(file_name, "rt", encoding = file_encoding),
                                            dialect = file_dialect,
                                            # fieldnames=job_doc['job']['source']['headers'],
                                            #delimiter=',', quotechar='"')
                                        delimiter = file_delimiter,
                                        quotechar = file_quotechar
                                        )
        for data_row in source_reader:
            # check if record exists
            print(data_row)
            print(replace_vals(job_doc['job']['target']['check-exists-sql'], data_row))
            lines += 1
            # print(', '.join(data_row))
            # replace_with_values(check_exists_sql, data_row);

            # open target
    
    # print end of job
    now = datetime.datetime.now()
    print("   ending job..."+str(now)+'lines:'+str(lines))    
    # close database
    conn.close()
    