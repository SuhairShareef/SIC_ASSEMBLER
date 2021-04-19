# Palestine Polytechnic University
# College of IT & Computer Engineering
# System Programming Project: SIC Assembler PASS #2
#-------------------------------------------------------------------------#
# Done by:
#   Name: Suhair Shareef
#   ID  : 171055
#       &&
#   Name: Beesan Atawna
#   ID  : 171006
#-------------------------------------------------------------------------#

# Import definings from Pass1
from PASS_1 import DIRECTIVES, SYMTAB, OPTAB, ERRCTR, PRGLTH, ADDSTA, LITPOOl

# Read intermediate file --> IT HAS TO BE .mdt
INTMDT = open("OUTPUT/intmdte_file.mdt", "r")

# Write to Object File && Listing File
OBJFILE = open("OUTPUT/ObjectFile.obj", "w+")
LISTFILE = open("OUTPUT/ListingFile.lst", "w+")

# Log file for errors --> errors file
ERRORS = open("OUTPUT/errors_file.txt", "w+")

# Defined variables comes here
LISTARR = []  # An array that is used to hold all listings among the execution of the program
ADDARR = []   # An array that is used to hold the list of addresses in the program
f = ""
f1 = ""
currentLine = INTMDT.readline()  # Read first line from the intermediate file

if ERRCTR == 0:
    while True:
        line = INTMDT.readline()
        if not line:  # Check if there's no lines to read
            break

        currentLine = line

        ADDRESS = currentLine[0:5].strip()   # Getting the address
        OPCODE = currentLine[18:26].strip()  # Getting the opcode

        if OPCODE != "START":
            ADDARR.append(ADDRESS)

        label = currentLine[9:17].strip()
        operand = currentLine[26:34].strip()
        if OPCODE == "START":
            ADDARR.append(currentLine[0:6].strip())
            OBJFILE.write("H^" + label + "^00" + currentLine[0:5].strip().upper() + "^00" + PRGLTH.upper())
            LISTARR.append("")
        elif OPCODE == "END":
            LISTARR.append("")
        else:
            if OPCODE in OPTAB.keys() or OPCODE in DIRECTIVES:

                op = OPCODE
                if op == "RSUB":
                    code = OPTAB[OPCODE[0:]]
                    op = code + "0000"
                    LISTARR.append(op)
                    LISTFILE.write(op)
                    LISTFILE.write("\n")

                elif OPCODE not in DIRECTIVES and ",X" not in operand:
                    code = OPTAB[OPCODE[0:]]
                    if operand in SYMTAB.keys():
                        sym = SYMTAB[operand[0:]]
                        LISTFILE.write(code + sym)
                        LISTFILE.write("\n")
                        LISTARR.append(code + sym)

                    elif "=" in operand:
                        temp2 = LITPOOl[str(operand)[1:]]
                        LISTFILE.write(code + temp2[2])
                        LISTFILE.write("\n")
                        LISTARR.append(code + temp2[2])

                elif operand[-2:] == ",X":
                    opend = operand[:-2]
                    if opend in SYMTAB.keys():
                        first = SYMTAB[opend][0:1]
                        sec = SYMTAB[opend[0:]]

                        value4 = hex(int(bin(1)[-1:] + "00" + bin(int(first))[2:]))[-1:]
                        op = OPTAB[OPCODE[0:]] + value4 + (sec[1] + sec[2] + sec[3])
                        LISTFILE.write(op)
                        LISTFILE.write("\n")
                        LISTARR.append(op)

                elif OPCODE == "RESW" or OPCODE == "RESB" or OPCODE == "LTORG":
                    LISTARR.append("")

                elif OPCODE == "WORD":
                    code = hex(int(operand))
                    code1 = str(code)[2:]
                    if len(code1) < 6:
                        for i in range(6 - len(code1)):
                            code1 = "0" + code1
                    LISTFILE.write(code1)
                    LISTFILE.write("\n")
                    LISTARR.append(code1)



                elif OPCODE == "BYTE" and OPCODE != "LTORG":
                    print(operand)
                    temp = operand[2:len(operand) - 1]
                    if "X'" in operand:
                        LISTFILE.write(temp)
                        LISTFILE.write("\n")
                        LISTARR.append(temp)

                    elif "C'" in operand:
                        for i in temp:
                            hexcode = hex(ord(i))[2:]
                            LISTFILE.write(str(hexcode))
                            f += hexcode
                        LISTARR.append(f)
                        LISTFILE.write("\n")

            elif label == "*":
                temp = LITPOOl[str(OPCODE)[1:]]
                LISTFILE.write(temp[0])
                LISTFILE.write("\n")
                LISTARR.append(temp[0])

            else:
                LISTARR.append("")

else:
    ERRORS.write("Cannot execute pass 2. The input file has errors!")
    print("Cannot execute pass 2. The input file has errors!")

i = 1
print(LISTARR)

while i < len(LISTARR):
    if i == 1:
        addr = ADDARR[1]
        print(addr)
    else:
        addr = ADDARR[i]
    cont = 0
    if LISTARR[i] != "":
        OBJFILE.write("\nT^00" + addr.upper() + "^")
        poINTMDT = OBJFILE.tell()
        OBJFILE.write("  ")
        j = i
        while j < len(LISTARR) and LISTARR[j] != "" and cont < 10:
            print(LISTARR[j].upper())
            OBJFILE.write("^" + LISTARR[j].upper())
            cont += 1
            j += 1
        i = j - 1
        OBJFILE.seek(poINTMDT)
        print(int(ADDARR[i], 16))
        print(int(addr, 16))
        tempaddr = str(int(ADDARR[i], 16) - int(addr, 16) + int(3))
        tempaddr1 = hex(int(tempaddr))
        taddr = tempaddr1[2:4]
        print(taddr)
        if len(taddr) == 1:
            taddr = "0" + taddr
        if taddr == "03":
            taddr = "01"
        OBJFILE.write(taddr.upper())
        OBJFILE.seek(0, 2)

    i += 1
OBJFILE.write("\n" + "E" + "^00" + str(hex(ADDSTA))[2:])
OBJFILE.close()
INTMDT.close()
LISTFILE.close()