__author__ = "Santhosh Baswa"
__copyright__ = "Copyright 2016, Independent Security Research"

import sqlite3
import sqlite3
a = raw_input("Enter the db:")
conn = sqlite3.connect(a)
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE openphishdb
             (phishpage text, domain text ,ipaddr text)''')

c.execute("INSERT INTO openphishdb VALUES ('www.google.com/search','www.google.com','8.8.8.8')")

conn.commit()
conn.close()
