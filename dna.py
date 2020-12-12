from csv import DictReader
from sys import argv

if len(argv) != 3:
    print("An error has occured, please provide a valid number of arguments")

def main():
    with open(argv[2], "r") as f:
        sq = (f.read())
        
    agatc = find_str(sq, "AGATC")
    aatg = find_str(sq, "AATG")
    tatc = find_str(sq, "TATC")
    ttttttct = find_str(sq, "TTTTTTCT")
    tctag = find_str(sq, "TCTAG")
    gata = find_str(sq, "GATA")
    gaaa = find_str(sq, "GAAA")
    tctg = find_str(sq, "TCTG")
     
    check = 0
    with open (argv[1]) as g:
        dna = DictReader(g)
        for row in dna:
            if ttttttct == 0:
                if int(row["AGATC"]) == agatc and int(row["AATG"]) == aatg and int(row["TATC"]) == tatc:
                    print(row["name"])
                    check += 1
            else:
                if int(row["TTTTTTCT"]) == ttttttct and int(row["TCTAG"]) == tctag and int(row["GATA"]) == gata and int(row["GAAA"]) == gaaa and int(row["TCTG"]) == tctg and int(row["AGATC"]) == agatc and int(row["AATG"]) == aatg and int(row["TATC"]) == tatc:
                    print(row["name"])
                    check += 1
        
        if check == 0:
            print("No match")

def find_str(txt, term):
    g = 0
    for i in range(len(txt) - len(term) - 1):
        st = 0
        if txt[i:(i + len(term))] == term:
            j = i
            while txt[j:(j + len(term))] == term:
                st += 1
                j += len(term)
                if g <= st:
                    g = st
    return g

main()