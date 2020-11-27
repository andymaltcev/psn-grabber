#psn-grabber
The application is a scheduled (cron) job that grabs the PSN website pages,
searches for products and their prices and stores them into the database.
As a result, a historical data about product prices is available in the database
for further analysis and visualization.

Clone this repo by command:

$ git clone <url>

At first you should install Python packages from requirements.txt.
To do this, run the following command in the command line:

$ pip install -r requirements.txt

All files run on local machine by command like:

$ python <file name>

1. create_tables_in_database.py - creates a database and the necessary
tables for subsequent filling. This file runs once.

2. add_data_in_tables.py - runs a parser from a file ps_store_parser.py
and fills both database tables with primary data. This file runs once.
After doing it you should use base_update.py to add new data.

3. base_update.py - runs a parser from a file "ps_store_parser.py" and
compares the received data with those already available in the database.
If they do not match, it adds new information to the database.

4. ps_store_parser.py - this file is not required to run. It is imported
as a module into the files described in points 2 and 3.

5. data_output.py - this file gives a simple output of the price
change graph from the database for the specified product.

Unfortunately, the parser described in the file "ps_store_parser.py"
no longer works. Cuz Sony changed the HTML markup on their website.

In this regard, the development of a different version of the parser
with a modified functional was started.

More details in the repository: /psn-grabber-v2