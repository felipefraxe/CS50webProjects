from cs50 import SQL
from sys import argv
from csv import DictReader

if len(argv) != 2:
    print("An error has occured! Please provide the right number of arguments")

db = SQL("sqlite:///students.db")

for row in db.execute("SELECT * FROM students WHERE house = ? ORDER BY last, first", argv[1]):
    if row['middle'] != None:
        print (f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")
    else:
        print(f"{row['first']} {row['last']}, born {row['birth']}")