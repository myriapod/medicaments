from classes import BDD, Table
import re
import mariadb
import sys

create_database = ""
# create_database = input("Do you want to create (or erase and create if it already exists) the database? ")
if re.match('(?i)yes|y|oui|o', create_database):
    import importBDD

medicaments = BDD()
medicaments.connect_BDD()

cur = medicaments.cur
conn = medicaments.conn

cur.execute("SHOW TABLES;")
# chercher nom -> SELECT nom FROM CIS_bdpm
# chercher pathologie
# substance active

# entrer la commande
cur.execute("SELECT nom FROM CIS_bdpm WHERE nom LIKE 'A%'")
if results := cur.fetchall():
    for r in results:
      print(r)

conn.close()