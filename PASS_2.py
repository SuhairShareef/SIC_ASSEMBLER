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

print(LITPOOl)

if ERRCTR == 0:
    while True:
        line = INTMDT.readline()  # Read line from the intermediate file
        if not line:  # Check if there's no lines to read
            break

        currentLine = line

        ADDRESS = currentLine[0:8].strip()     # Getting the address
        LABEL = currentLine[9:17].strip()      # Getting label
        MNEMONIC = currentLine[18:25].strip()  # Getting the mnemonic
        OPERAND = currentLine[25:34].strip()   # Getting operand

        if MNEMONIC != "START":  # If we add START address twice there will duplication
            ADDARR.append(ADDRESS)

        # Write Header record to object program
        if MNEMONIC == "START":
            OBJFILE.write("H^" + LABEL + "^00" + currentLine[0:5].strip().upper() + "^00" + PRGLTH.upper())

            ADDARR.append(currentLine[0:6].strip())
            LISTARR.append("")      # Add listing for START

        elif MNEMONIC == "END":
            LISTARR.append("")      # Add listing for END

        else:  # Search OPTAB for MNEMONIC
            if MNEMONIC in DIRECTIVES or MNEMONIC in OPTAB.keys():
                if MNEMONIC == "RSUB":
                    objCode = OPTAB[MNEMONIC] + "0000"  # RSUB code + 0000 // has no operand

                    LISTARR.append(objCode)
                    LISTFILE.write(objCode + "\n")  # Write to listing file

                elif MNEMONIC not in DIRECTIVES and ",X" not in OPERAND:  # Mnemonic in OPTAB && not indexed
                    if OPERAND in SYMTAB.keys():
                        LISTFILE.write(OPTAB[MNEMONIC] + SYMTAB[OPERAND] + "\n")  # ObjCode = opcode + operand address
                        LISTARR.append(OPTAB[MNEMONIC] + SYMTAB[OPERAND])

                    elif "=" in OPERAND:  # If it's a literal
                        LISTFILE.write(OPTAB[MNEMONIC] + LITPOOl[str(OPERAND)[1:]][2] + "\n")
                        LISTARR.append(OPTAB[MNEMONIC] + LITPOOl[str(OPERAND)[1:]][2])

                elif OPERAND[-2:] == ",X":  # If it's hex
                    if OPERAND[:-2] in SYMTAB.keys():  # If it's in the SYMTAB then convert string to hex after adding
                        hexCode = hex(int(bin(1)[-1:] + "00" + bin(int(SYMTAB[OPERAND[:-2]][0:1]))[2:]))[-1:]
                        objCode = OPTAB[MNEMONIC[0:]] + hexCode + (SYMTAB[OPERAND[:-2]][1] +
                                  SYMTAB[OPERAND[:-2]][2] + SYMTAB[OPERAND[:-2]][3])

                        LISTFILE.write(objCode + "\n")
                        LISTARR.append(objCode)

                elif MNEMONIC == "RESW" or MNEMONIC == "RESB" or MNEMONIC == "LTORG":  # No opcode for those dir
                    LISTARR.append("")

                elif MNEMONIC == "WORD":  # If word convert operand to hex
                    objCode = str(hex(int(OPERAND)))[2:]

                    if len(objCode) < 6:  # Making sure it's six digits to fit object format
                        for i in range(6 - len(objCode)):
                            objCode = "0" + objCode

                    LISTFILE.write(objCode + "\n")
                    LISTARR.append(objCode)

                elif MNEMONIC == "BYTE" and MNEMONIC != "LTORG":  # the opcode =BYTE and it's not literal then we print the operand
                    temp = OPERAND[2:len(OPERAND) - 1]  # store the operand that comes after X' or C'

                    if "X'" in OPERAND:  # If hex such as X'05' we start from 0 to the end 5
                        LISTFILE.write(temp + "\n")  # Write into listing file
                        LISTARR.append(temp)

                    elif "C'" in OPERAND:  # means that the operand is in ascii
                        for i in temp:     # iterate through all characters
                            hexCode = hex(ord(i))[2:]  # Convert to hex
                            LISTFILE.write(str(hexCode))  # store hexcode
                            objCode += hexCode

                        LISTARR.append(objCode + "\n")

            elif LABEL == "*":  # lable = current location counter
                literal = LITPOOl[str(MNEMONIC)[1:]]  # Get the literal

                LISTFILE.write(literal[0] + "\n")
                LISTARR.append(literal[0])

            else:
                LISTARR.append("")

else:
    ERRORS.write("Cannot execute pass 2. The input file has errors!")
    print("Cannot execute pass 2. The input file has errors!")

# Writing to object program
currentListing = 1

while currentListing < len(LISTARR):  # Iterate through all listings

    currentAddress = ADDARR[currentListing]
    lngth = 0  # To calc length of record

    if LISTARR[currentListing] != "":
        # Write text record into OBJFILE
        OBJFILE.write("\nT^00" + currentAddress.upper() + "^")
        pointer = OBJFILE.tell()   # save current position of the file object
        OBJFILE.write("  ")
        j = currentListing

        # Length of LISTARR and LISTARR[j] is not equal space and the number of words less than 10
        # (the max length of text record )
        while j < len(LISTARR) and LISTARR[j] != "" and lngth < 10:
            OBJFILE.write("^" + LISTARR[j].upper())
            lngth += 1
            j += 1

        currentListing = j - 1

        OBJFILE.seek(pointer)  # Set the current position of file at the last position in OBJFILE
        # the current address in this text record - first address in ADDARR then add 3 (each word 3 byte)
        tempAdd = hex(int(str(int(ADDARR[currentListing], 16) - int(currentAddress, 16) + int(3))))[2:4]

        if len(tempAdd) == 1:
            tempAdd = "0" + tempAdd # add 0 before text address (fixed format)

        if tempAdd == "03":
            tempAdd = "01"

        OBJFILE.write(tempAdd.upper())
        OBJFILE.seek(0, 2)  # set the file's current position at the offset

    currentListing += 1

OBJFILE.write("\n" + "E" + "^00" + str(hex(ADDSTA))[2:])
OBJFILE.close()
INTMDT.close()
LISTFILE.close()