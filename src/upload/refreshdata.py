#!/usr/bin/env python

"""refreshdata.py: Refresh Data in a system from any given source (database, csv, xml file)."""

__author__ = "Jon Arce"
__copyright__ = "Copyright 2020"
__credits__ = ["Jon Arce"]
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = "Jon Arce"
__email__ = "jon.arce@gmail.com"
__status__ = "Production"

import sys
import datetime
import xml.etree.ElementTree as xml

if __name__ == '__main__':
    now = datetime.datetime.now()
    print("Starting job ..." + str(now))
    # Print arguments one by one
    print ('Job file:',  str(sys.argv[1]))
    now = datetime.datetime.now()    
    print("   ending job..."+str(now))
    