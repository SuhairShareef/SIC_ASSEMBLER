#     THIS IS PASS 1     #

# import defined objects and arrays from a file
import DEFININGS

# Read source file --> IT HAS TO BE .asm
INPUT = open("source_file.asm", "r")

# Output file --> intermediate file
OUTPUT = open("intmdte_file.mdt", "w+")

# Log file for errors --> errors file
ERRORS = open("errors_file.txt", "w+")

# Definings
OPTAB = DEFININGS.OPTAB
DIRECTIVES = DEFININGS.DIRECTIVES
SYMTAB = {}
LITTAB = {}
LOCCTR = 0
PRGLTH = 0
PRGNAME = ""
ERRCTR = 0
ADDSTA = 0

# Reading from file
for line in INPUT:
    OPTAB[line[0:9].split(' ')[0]] = line[10:15].strip()

# Reading first line
fileLine = INPUT.readline()
if fileLine[9:15].strip() == "START":
    ADDSTA = int(fileLine[16:35].strip(),16)
    LOCCTR = ADDSTA
    PRGNAME = fileLine[0:8].strip()
    space = 10 - len(str((LOCCTR)))
    OUTPUT.write(hex(LOCCTR)[2:] + " " * space + fileLine)
    OUTPUT.flush()

else:
    LOCCTR = 0

