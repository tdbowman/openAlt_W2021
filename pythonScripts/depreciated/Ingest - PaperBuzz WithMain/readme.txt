1) Create a new database
	- CREATE DATABASE paperbuzzeventdata;
	- SQL -> eventData-json_dump10k -> CreateSyntax-event_data_json.sql
		- Open CreateSyntax-event_data_json.sql

2) Import json_dump_10k.csv to the event_data_json table in workbench
	- SQL -> eventData-json_dump10k

3) Ignore steps 1 & 2 if you already have a database containing the paperbuzz data dump

4) DROP DATABASE crossrefeventdatawithmain

5) Run crossrefeventdataWithMain.sql and load up all 13 tables.

6) Run paperBuzzMain.py (preferably in terminal)
