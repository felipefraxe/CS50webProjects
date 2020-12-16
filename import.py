from cs50 import SQL
from sys import argv
from csv import DictReader

if len(argv) != 2:
    print("An error has occured! Please provide the right number of arguments")

db = SQL("sqlite:///students.db")

with open (argv[1]) as file:
    reader = DictReader(file)
    for row in reader:
        name = row["name"].split()
        first = name[0]
        if len(name) < 3:
            middle = None
            last = name[1]
        else:
            middle = name[1]
            last = name[2]
        house = row["house"]
        birth = int(row["birth"])
        
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", first, middle, last, house, birth)