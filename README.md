## PYTHON3 ##

Install the following python modules

* sqlalchemy
* psycopg2
* pandas
* numpy
* importlib.util
* sys
* os
* seaborn
* matplotlib.pyplot
* segno
* python-barcode
* Flask

## DATABASE ##

Note: Postgres on Linux only!

Step 1: Create Database and User

create database cmdb3;
create user cmdb with encrypted password 'cmdb';
grant all privileges on database cmdb3 to cmdb;

Step 2: Install and test uuid-ossp extension

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SELECT uuid_generate_v4();

Step 3: If the above select returns a value, implement the get_uuid function

CREATE OR REPLACE FUNCTION public.get_uuid()
 RETURNS text
 LANGUAGE plpgsql
AS $function$
DECLARE
    uuid varchar(32);
BEGIN
    SELECT REPLACE(CAST(uuid_generate_v4() AS varchar(36)), '-', '') INTO uuid;
    RETURN uuid;
END;
$function$

Step 4: Test the get_uuid function

select * from get_uuid();
             get_uuid
----------------------------------
 47c7e155c8a2428d8b62a90a60a7a45d

Step 5: Import sample data

psql -U cmdb cmdb3 -h 192.168.2.11 < cmdb.sql

Step 6: Start flask

./flask.sh

Step 7: Open pycmdb

http://localhost:5003/

## USING pycmdb ##

Admin -> Table

Table: the name of the table inside the database
Display Value: the display value of the table as it should appear
Order: defines the display order

Admin -> Column

Table: select a table (mandatory)
Column: the name of column inside the database
Display Value: the display value of the column as it should appear
Order: defines the display order

Admin -> Column -> Data Type

Reference: references another table, the column name must be the table name!
Length: keep empty
Default keep empty

Dictionary: will create a new dictionary with a default value
Length: keep empty
Default keep empty

Function: will load an additional function, the column name must be the function name
Length: keep empty
Default keep empty

Boolean: true/false
Length: keep empty
Default true/false

Integer: just an integer
Length: keep empty
Default any integer number you enter

Float: floating point number
Length: defines precision and scale, e.g. 6,3 will allow to enter numbers like 999.999
Default: any floating point number you enter

Character Varying: a string
Length: the number of characters for the string, default 256
Default: any string you enter

Date: date only, not date & Time, format: YYYY-MM-DD
Length: keep empty
Default: any date you enter

Admin -> Dictionary

Table: the table name (mandatory to select)
Column: the column name (mandatory to select)
Dict Value: the value of the dictionary (mandatory)
Color: the background color it should appear, e.g. ff0000 will set a red background (optional)
Order: the order the value will apear

Important note about dictionaries: each dictionary must have a different name!
Creating a dictionary called lifecycle on a table called hardware, and creating the same dictionary name on a table called software will lead to an error
Instead, create a dedicated dictionary hw_lifecycle for e.g. hardware and sw_lifecycle for e.g. software

Admin -> Function

Just lists available functions

Admin -> Report

Just some very basic reporting functionalities

Barplot & Countplot: for grouping of value, e.g. the lifecycle of an object
Heatmap: for date fields
Histplot: for integer and floating point numbers
