## RefreshData
Utility created in the Python language, currently running in Python3. It solves the problem known as "data refresh" that consists of the following flow:

1. Update all records that already exists.
2. Add records that are new.
3. Erase records no longer present.

For it to works you create an .XML "job" definition file and pass it as a parameter to the utility.
Inside the "job", it will allow you to define a "source" and a "target" location.

# Common use cases are:

text CSV file -> Database - table
Database table -> database - table (could even be different database engines)

I am sharing this utility (as Apache License) so anyone with the same problem have at least a starting point. You may contact me with any questions or concerns. 
													Jon.Arce@gmail.com
