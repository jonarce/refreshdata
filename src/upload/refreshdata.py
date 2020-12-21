#!/usr/bin/env python

"""refreshdata.py: Refresh Data in a system from any given source (database, csv, xml file)."""

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

if __name__ == '__main__':
    now = datetime.datetime.now()
    print("Starting job ..." + str(now))
    print(getcwd())
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
 
    with open(job_file) as fd:
        job_doc = xmltodict.parse(fd.read())

    print(job_doc)
    ###### ['mydocument']['@has'] # == u'an attribute')
    # print end of job
    now = datetime.datetime.now()
    print("   ending job..."+str(now))
    