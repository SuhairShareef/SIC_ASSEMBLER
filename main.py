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
ERRORLIST = DEFININGS.ERRORLIST
SYMTAB = {}
LITTAB = {}
LOCCTR = 0
PRGLTH = 0
PRGNAME = ""
ERRCTR = 0
ADDSTA = 0

# Reading from file
# Reading first line
line = INPUT.readline()
if line:
    if line[9:15].strip() == "START":
        PRGNAME = line[0:8].strip()  # get program name
        ADDSTA = int(line[16:35].strip(), 16)  # get the starting address and convert to int
        LOCCTR = ADDSTA
        OUTPUT.write(hex(LOCCTR)[2:] + " " * (6 - len(str(LOCCTR))) + line)  # write first line in outputFile

        # Continue reading
        while True:
            line = INPUT.readline()
            if not line:  # Check if there's no lines to read
                break
            operation = line[9:15].strip()
            if operation != "END" and ("." not in line):  # if not endOfFile and the line is not a comment
                label = line[0:8].strip()  # get the label

                if label != "":  # Check if there's a label]
                    if label in SYMTAB:  # if the label already exist then log an error
                        ERRORS.write(ERRORLIST[2])
                        print(ERRORLIST[2])
                        ERRCTR += 1

                    else:  # if there's no errors add to the SYMTAB
                        SYMTAB[label] = hex(LOCCTR)[2:]
                        OUTPUT.write(SYMTAB[label] + "          " + line[0:8].strip() + '\n')  # Write to the outputFile

                operand = ""
                if operation == "LTORG":
                    OUTPUT.write(" " * 10 + line)

                else:
                    OUTPUT.write(hex(LOCCTR)[2:] + " " * (6 - len(str(LOCCTR))) + line)  # write line to outputFile

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
                       LOCCTR += int((len(operand) - 3)/2)

                    elif operand[0] == 'C':
                        LOCCTR += (len(operand)-3)

                elif operation == "RESW":
                    operand = line[16:35].strip()
                    LOCCTR += 3 * int(operand)

                elif operation == "LTORG":
                    for i in LITTAB:
                        LITTAB[i][2] = hex(LOCCTR)[2:]
                        OUTPUT.write(hex(LOCCTR)[2:]+" " * (6 - len(str(LOCCTR))) + "*" + " " * 7 + "=" + i + "\n")
                        LOCCTR += int(LITTAB[i][1])
                    LITTAB = {}

                else:
                    ERRORS.write(ERRORLIST[3])
                    print(ERRORLIST[3])
                    ERRCTR += 1

                literals = []
                if line[16:17] == '=':
                    exist = 1
                    literal = line[17:35].strip()
                    if literal[0] == 'X':
                        hexco = literal[2:-1]
                    elif literal[0] == 'C':
                        hexco = literal[2:-1].encode("utf-8").hex()

                    else:
                        print("NOT Valid Literal : " + " " + line[17:35].strip())
                        ErrorFile.write("NOT Valid Literal : " + " " + line[17:35].strip())
                        ErrorFile.write("\n")
                        break

                    if literal in litpool:
                        exist = 0

                    else:
                        literalList = [hexco, len(hexco) / 2, 0]
                        littab[literal] = literalList
                        litpool[literal] = literalList
                        Littab.write(str(litpool[literal]))
                        Littab.write("\n")

    else:
        ERRORS.write(ERRORLIST[1])
        print(ERRORLIST[1])

else:
    ERRORS.write(ERRORLIST[0])
    print(ERRORLIST[0])

