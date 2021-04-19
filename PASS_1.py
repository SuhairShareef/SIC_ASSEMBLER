# Palestine Polytechnic University
# College of IT & Computer Engineering
# System Programming Project: SIC Assembler PASS #1
#-------------------------------------------------------------------------#
# Done by:
#   Name: Suhair Shareef
#   ID  : 171055
#       &&
#   Name: Beesan Atawna
#   ID  : 171006
#-------------------------------------------------------------------------#

# Import defined objects and arrays from a file
from INPUT.DEFININGS import *

# Read source files --> IT HAS TO BE .asm
# There's multiple source files to test if the program is working correctly
# Uncomment the source file you want to try
INPUT = open("INPUT/Test_File_1.asm", "r")
# INPUT = open("INPUT/Test_File_2.asm", "r")
# INPUT = open("INPUT/Test_File_3.asm", "r")

# Output file --> intermediate file
OUTPUT = open("OUTPUT/intmdte_file.mdt", "w+")

# Log file for errors --> errors file
ERRORS = open("OUTPUT/errors_file.txt", "w+")

# Saving literal table
LITTABLE = open("OUTPUT/LITTABLE.txt", "w+")

# Definings
SYMTAB = {}
LITTAB = {}
LOCCTR = 0
PRGLTH = 0
PRGNAME = ""
ERRCTR = 0
ADDSTA = 0
LITPOOl = {}

print("\n**************SIC ASSEMBLER*****************\n")
# Reading from file
# Reading first line
line = INPUT.readline()
if line:
    if line[9:15].strip() == "START":
        PRGNAME = line[0:8].strip()  # get program name
        ADDSTA = int(line[16:35].strip(), 16)  # get the starting address and convert to int
        LOCCTR = ADDSTA
        OUTPUT.write(hex(LOCCTR)[2:] + " " * (10 - len(str(LOCCTR))) + line)  # write first line in outputFile

        # Continue reading
        while True:
            line = INPUT.readline()
            if not line:  # Check if there's no lines to read
                break
            operation = line[9:15].strip()

            if operation != "END" and ("." not in line):  # if not endOfFile and the line is not a comment
                if operation == "LTORG":
                    OUTPUT.write(" " * 10 + line)

                else:
                    OUTPUT.write(hex(LOCCTR)[2:] + " " * (10 - len(str(LOCCTR))) + line)  # write line to outputFile

                label = line[0:8].strip()  # get the label

                if label != "":  # Check if there's a label]
                    if label in SYMTAB:  # if the label already exist then log an error
                        ERRORS.write(ERRORLIST[2])
                        print(ERRORLIST[2])
                        ERRCTR += 1

                    else:  # if there's no errors add to the SYMTAB
                        SYMTAB[label] = hex(LOCCTR)[2:]

                if operation not in OPTAB:
                    operand = 0

                # check if operation exist in OPTAB
                if operation in OPTAB:
                    LOCCTR += 3

                elif operation == "WORD":
                    LOCCTR += 3

                elif operation == "RESB":
                    operand = line[16:35].strip()
                    LOCCTR += int(operand)

                elif operation == "BYTE":
                    operand = line[16:35].strip()

                    if operand[0] == 'X':
                        LOCCTR += int((len(operand) - 3) / 2)

                    elif operand[0] == 'C':
                        LOCCTR += (len(operand) - 3)

                elif operation == "RESW":
                    operand = line[16:35].strip()
                    LOCCTR += 3 * int(operand)

                elif operation == "LTORG":
                    for i in LITTAB:
                        LITTAB[i][2] = hex(LOCCTR)[2:]
                        OUTPUT.write(hex(LOCCTR)[2:] + " " * (10 - len(str(LOCCTR))) + "*" + " " * 7 + "=" + i + "\n")
                        LOCCTR += int(LITTAB[i][1])
                    LITTAB = {}

                else:
                    ERRORS.write(ERRORLIST[3])
                    print(ERRORLIST[3])
                    ERRCTR += 1

                literals = [] #literals array
                if line[16:17] == '=':  #meaning its letiral
                    exist = 1
                    literal = line[17:35].strip()

                    if literal[0] == 'X': # x in hexadecimal
                        hexcode = literal[2:-1]

                    elif literal[0] == 'C':
                        hexcode = literal[2:-1].encode("utf-8").hex() #c in hex

                    else:
                        ERRORS.write(ERRORLIST[4]) #not valid literal
                        print(ERRORLIST[4])
                        ERRCTR += 1
                        break

                    if literal not in LITPOOl:
                        literals = [hexcode, len(hexcode) / 2, 0]
                        LITTAB[literal] = literals #add literals into literal table
                        LITPOOl[literal] = literals
                        LITTABLE.write(str(LITPOOl[literal]) + "\n")

            if operation == "END":#end of program
                OUTPUT.write(" " * 10 + line)

    else:
        ERRORS.write(ERRORLIST[1]) 
        print(ERRORLIST[1])

else:
    ERRORS.write(ERRORLIST[0])
    print(ERRORLIST[0])

if LITTAB:
    for literal in LITTAB:
        LITTAB[literal][2] = hex(LOCCTR)[2:] #literals in hexadecimal
        OUTPUT.write(hex(LOCCTR)[2:] + " " * (10 - len(str(LOCCTR))) + "*" + " " * 7 + "=" + literal + "\n")
        LOCCTR += int(LITTAB[literal][1])

length = int(LOCCTR) - int(ADDSTA) #program length ( current location counter - start address)
PRGLTH = hex(int(length))[2:].format(int(length)) #program length in hexadecimal
loc = hex(int(LOCCTR))[2:].format(int(LOCCTR)) #location counter in hexadecimal
INPUT.close()
OUTPUT.close()
LITTABLE.close()
ERRORS.close()

print("PROGRAM NAME: " + PRGNAME)
print("PROGRAM LENGTH: " + str(PRGLTH).upper())
print("LOCATION COUNTER: " + str(loc).upper())
print("NUMBER OF ERRORS: " + str(ERRCTR) + "\n")

print(" SYMBOL TABLE\n--------------")
for label in SYMTAB:
    print(label + " " * (10 - len(str(label))) + SYMTAB[label].upper())
