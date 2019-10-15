import sys,re

def addLabel(label,LC):
  if isDuplicateLabel(label):
    #throw label has been define before error
    print()
  else:
    labelTable[label] = LC

def addOpcode(opcode, opcodeBin, size, instructionClass):
  if list(opcodeTable.keys()).count(opcode) == 0:
    opcodeTable[opcode] = [opcodeBin, size, instructionClass]

def addSymbol(variable,value,size):
  if isDuplicateSymbol(variable):
    #throw symbol has been defined more than once error
    pass
  else:
    symbolTable[variable] = [value,None,size]

def addLiteral(literal):
  if list(literalTable.keys()).count(literal) == 0:
    value = literal[2:-1]
    if not value.isdigit():
      #throw invalid literal error
      literalTable[literal] = [0,None,12]
      return 0
    literalTable[literal] = [int(value),None,12]
  return 1

def extractOpcode(lineNum,line):
  # print(line)
  tokens = line.upper().split()
  if tokens.count('CLA') == 1:
    addOpcode('CLA','0000',12,0)
  elif tokens.count('LAC') == 1:
    addOpcode('LAC','0001',12,1)
  elif tokens.count('SAC') == 1:
    addOpcode('SAC','0010',12,1)
  elif tokens.count('ADD') == 1:
    addOpcode('ADD','0011',12,1)
  elif tokens.count('SUB') == 1:
    addOpcode('SUB','0100',12,1)
  elif tokens.count('BRZ') == 1:
    addOpcode('BRZ','0101',12,1)
  elif tokens.count('BRN') == 1:
    addOpcode('BRN','0110',12,1)
  elif tokens.count('BRP') == 1:
    addOpcode('BRP','0111',12,1)
  elif tokens.count('INP') == 1:
    addOpcode('INP','1000',12,1)
  elif tokens.count('DSP') == 1:
    addOpcode('DSP','1001',12,1)
  elif tokens.count('MUL') == 1:
    addOpcode('MUL','1010',12,1)
  elif tokens.count('DIV') == 1:
    addOpcode('DIV','1011',12,1)
  elif tokens.count('STP') == 1:
    addOpcode('STP','1100',12,0)
  else:
    variable, value, size = checkPseudoinstruction(lineNum,line)
    if variable == None:
      #throw unknown opcode error; handled in pass 2
      return
    addSymbol(variable,value,size)

def extractLiteral(lineNum,line):
  tokens = line.split()
  for s in tokens:
    if s[:2] == "'=" and s[-1] == "'":
      i = addLiteral(s)
      if i == 0:
        errorTable.append([lineNum,"Invalid Literal used"])

def checkLabel(line):
  label = ''
  i = line.find(':')
  if i != -1:
    label = line[:i].strip()
    line = line[i+1:].strip()
  return label, line

def checkPseudoinstruction(lineNum,line):
  tokens = line.upper().split()
  i = tokens.count('DW')
  if i == 0:
    return None, None, None
  if i > 1 or len(tokens) > 3:
    #throw too many opcodes or operands error;
    errorTable.append([lineNum,"Too many operands"])
  variable = tokens[0].strip()
  if variable.isdigit():
    errorTable.append([lineNum,"Variable cannot be a numeric value or start with a digit"])
  value = 0
  if len(tokens) == 3:
    value = tokens[2].strip()
    if not value.isdigit():
      errorTable.append([lineNum,"Wrong operand type; Only numeric values permitted"])
      #throw wrong operand error
      value = 0
  # elif len(tokens) == 2:
  #   value = 0
  return variable, int(value), 12

def isComment(line):
  if line.find("//") == 0:
    return True
  return False

def removeComment(line):
  i = line.find("//")
  if i == -1:
    return line
  return line[:i].strip()

def isDuplicateSymbol(variable):
  if list(symbolTable.keys()).count(variable) > 0:
    return True
  return False

def isDuplicateLabel(label):
  if list(labelTable.keys()).count(label) > 0:
    return True
  return False

def assignAddressToVariablesAndLiterals(LC):
  for i in symbolTable:
    symbolTable[i][1] = LC
    LC += symbolTable[i][2]
  for i in literalTable:
    literalTable[i][1] = LC
    LC += literalTable[i][2]

def passOne():
  # lineCtr = 0
  locationCounter = 0
  cleanedCode = []

  for lineNum,line in code:
    # lineCtr += 1
    if isComment(line):
      continue
    line = removeComment(line)
    # print(line)
    label, line = checkLabel(line)
    if label != '':
      addLabel(label,locationCounter)
    cleanedCode.append([lineNum,line])
    extractOpcode(lineNum,line)
    extractLiteral(lineNum,line)
    locationCounter += 12
  assignAddressToVariablesAndLiterals(locationCounter)
  return cleanedCode


def passTwo():
  for lineNum,line in code:
    separate=line.split()
    if separate[0] in opcodeTable.keys():
      temp=opcodeTable[separate[0]]
      mcode.append(temp[0])
      # mcode[-1]+=' '
      if(temp[2]==1):
        if( len(separate)==2):
          if(separate[1] in symbolTable.keys()):
            addr=bin(symbolTable[separate[1]][1])[2:]
            while(len(addr)<8):
              addr='0'+addr
            mcode[-1]+=addr
          elif(separate[1] in labelTable.keys()):
            addr=bin(labelTable[separate[1]])[2:]
            while(len(addr)<8):
              addr='0'+addr
            mcode[-1]+=addr
          elif (separate[1] in literalTable.keys()):
            # print("lit")
            addr=bin(literalTable[separate[1]][1])[2:]
            while(len(addr)<8):
              addr='0'+addr
            mcode[-1]+=addr
          elif(separate[1].isnumeric()):
            addr=bin(int(separate[1]))[2:]
            while(len(addr)<8):
              addr='0'+addr
            mcode[-1]+=addr
          else:
            # print(separate[1])
            errorTable.append([lineNum,separate[1]+" Symbol used but not defined"])
            # throw symbol not found exception
        elif(len(separate)<2):
          errorTable.append([lineNum,"Operands Needed:1; Given:"+str(len(separate)-1)])
          pass
          # throw too less operands exception
        else:
          pass
          errorTable.append([lineNum,"Too less Operands; Needed:1; Given:"+str(len(separate)-1)])
          #throw too many operands exception
      if(temp[2]==0):
        mcode[-1]+='00000000'
        if(len(separate)>1):
          errorTable.append([lineNum,"Too many Operands; Needed:0; Given:"+str(len(separate)-1)])
          # throw too many operands exception
          pass
    elif separate[0] in symbolTable.keys():
      pass
    else:
      errorTable.append([lineNum,separate[0]+" is an invalid Opcode"])
      pass
  file=open("bin.txt","w+")

  if len(errorTable)>0:
    for e in errorTable:
      print("Error at Line "+str(e[0])+": "+e[1]+"\n")
      file.write("Error at Line "+str(e[0])+": "+e[1]+"\n")
  else:
    for x in mcode:
      file.write(x+"\n")
      print(x[:4]+" "+x[4:])
  file.close()

##CODE BEGINS HERE##

code = [] #Stores code in the format [lineNumber, line]
mcode = [] #Machine code

# hasError = [] #List that stores value True against a line number having an error to prevent those lines marked True in Pass one from being evaluated for errors again
errorTable=[] #Table that stores Errors [[lineNo,Error Description]]
labelTable = {} #Table that stores Label addresses { label : locationAddress }
symbolTable = {} #Table that stores variables in format { variable : [value,locationAddress,size] }
opcodeTable = {} #Table that stores opcodes occuring in the program in format { opcode : [binaryCodeForOpcode, size, inctructionClass] }
# Instruction class = 0 for 0 operand Instructions and 1 for Instructions with one operand
literalTable = {}

# hasError.append(False)
i = 0
for line in sys.stdin:
  i+=1
  code.append([i,line.strip()])
  # hasError.append(False)


# lineCtr = 0
code = passOne()

passTwo()
# print(code)

# print(labelTable)
# print(symbolTable)
# print(opcodeTable)
# print(literalTable)
