## RefreshData
Utility created in the Python language, currently running in Python3. You may import text files (common CSV like) to a database. It solves the problem known as "data refresh" that consists of the following flow:

1. Update all records that already exists.
2. Add records that are new.
3. Erase records no longer present.

For it to works you create an .XML "job" definition file and pass it as a parameter to the utility.
Inside the "job", it will allow you to define a "source" and a "target" location.

# Common use cases are:

text CSV file -> Database - table
Database table -> database - table (could even be different database engines)

# Job Configuration (parameters):

Jobs are just XML files that describe the from -> to relationship and what data will be moved. They consist of 3x main sections:

1. common - parameters that are global or define the job itself. Notice the 'type' attribute is 'upload' as it is the ONLY mode supported (at least by now).
	job-name - Name of the job
	
2. source - the 'FROM' configuration of the sending end of the data, notice the 'type' attribute ('file' or 'database').
	IF FILE:
	file-name - file name of your source file
	read-from-line - the line # to start reading, normally 2.
			<read-from-line>2</read-from-line>
	new-line - how a line ends in the text file, normally this is \n (linefeed) for UNIX and \n\r (linefeed + carriage return) for Windows
	encoding - file encoding format: like 'utf-8-sig' (BOM), utf-8
	delimiter - how the fields are divided, normally just a ",".
	quote-char - how to identify character strings (if present), normally just a '"'.
	fiel-names - leave blank or do not provide, then the headers will be read from inside the file (first line), this are the column names. If provided it should be a comma delimited list of field names.
	IF DATABASE:
	 
3. target - the 'TO' configuration of the receiving end of the data, notice the 'type' attribute ('file' or 'database').
	IF DATABASE:
	engine - the name of the database engine like: POSTGRES, MS-SQL, ORACLE, MYSQL, SQLITE
	server - hostname of the server, could be 'localhost' if database server is installed locally.
	port - normally the TCP port of the service, if leaved blank no port will be passed and it will end up using the default port.
	database - name of the database used to store the information.
	check-exists-sql - SQL query used to verify if a record exists, notice the name of the place holder, at runtime that placeholder will be substituted by data readed from source.
	insert-sql - SQL statement used to insert new records. This may include database functions as well.
	update-sql - SQL statement used tp update records. Could include database functions.
	delete-old-sql - SQL statement used to delete ALL records that where not processed (inserted or updated) by this current run of the job. You may leave it blank if not required. You could ONLY use the timestamp parameter in it.
	after-import-sql - SQL commands to excecute after the import is completed. There could be multiples, just separate by ';'. For example I use this for converting PostGIS data into a Geography column, but anytype of SQL could be executed, it will use the same connection.

Primary Key & TIMESTAMP - there should be a PRIMARY KEY field in the target table, as that is the mechanics to check if a record exists, the system will then use the 'check-exists-sql' (from the job config file) query for that. The TIMESTAMP field is used to determinate the date/time of when the record was last changed.

How import works, there are 2x pass:
1. ADD or UPDATE - It will use the table primary key to check if the row exists, before determining if it should be added (INSERT INTO) or updated (UPDATE), it will allways place update the TIMESTAMP field.
2. DELETE - To determinate records to be erased (DELETE) the system will use the specified TIMESTAMP field, erasing anything that has not been updated or added since the process start (have NOT been touched so it is NOT in the list).

XML ENTITY REFERENCE:
As the format of the file is in XML there are characters that must be substituted if you need them.
There are 5 pre-defined entity references in XML:
&lt; 	< 	less than
&gt; 	> 	greater than
&amp; 	& 	ampersand 
&apos; 	' 	apostrophe
&quot; 	" 	quotation mark
Only < and & are strictly illegal in XML, but it is a good habit to replace > with &gt; as well.


I am sharing this utility (as Apache License) so anyone with the same problem have a solution or at least a starting point. You may contact me with any questions or concerns. 

													Jon.Arce@gmail.com
