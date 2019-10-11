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
    print()
  else:
    symbolTable[variable] = [value,None,size]

def addLiteral(literal):
  if list(literalTable.keys()).count(literal) == 0:
    value = literal[2:-1]
    if not value.isdigit():
      #throw invalid literal error
      return
    literalTable[literal] = [int(value),None,12]


def extractOpcode(line):
  # print(line)
  if line.upper().find('CLA') >= 0:
    addOpcode('CLA','0000',12,0)
  elif line.upper().find('LAC') >= 0:
    addOpcode('LAC','0001',12,1)
  elif line.upper().find('SAC') >= 0:
    addOpcode('SAC','0010',12,1)
  elif line.upper().find('ADD') >= 0:
    addOpcode('ADD','0011',12,1)
  elif line.upper().find('SUB') >= 0:
    addOpcode('SUB','0100',12,1)
  elif line.upper().find('BRZ') >= 0:
    addOpcode('BRZ','0101',12,1)
  elif line.upper().find('BRN') >= 0:
    addOpcode('BRN','0110',12,1)
  elif line.upper().find('BRP') >= 0:
    addOpcode('BRP','0111',12,1)
  elif line.upper().find('INP') >= 0:
    addOpcode('INP','1000',12,1)
  elif line.upper().find('DSP') >= 0:
    addOpcode('DSP','1001',12,1)
  elif line.upper().find('MUL') >= 0:
    addOpcode('MUL','1010',12,1)
  elif line.upper().find('DIV') >= 0:
    addOpcode('DIV','1011',12,1)
  elif line.upper().find('STP') >= 0:
    addOpcode('STP','1100',12,0)
  else:
    variable, value, size = checkPseudoinstruction(line)
    if variable == None:
      #throw error
      print("error line: "+line)
      return
    addSymbol(variable,value,size)

def extractLiteral(line):
  tokens = line.split()
  for s in tokens:
    if s[:2] == "'=" and s[-1] == "'":
      addLiteral(s)

def checkLabel(line):
  label = ''
  i = line.find(':')
  if i != -1:
    label = line[:i].strip()
    line = line[i+1:].strip()
  return label, line

def checkPseudoinstruction(line):
  i = line.upper().find('DW')
  if i == -1:
    return None, None, None
  variable = line[:i].strip()
  value = line[i+2:].strip()
  if not value.isdigit():
    #throw error
    return None,None,None
  return variable, value, 12

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
  lineCtr = 0
  locationCounter = 0
  cleanedCode = []

  for line in code:
    lineCtr += 1
    if isComment(line):
      continue
    line = removeComment(line)
    # print(line)
    label, line = checkLabel(line)
    if label != '':
      addLabel(label,locationCounter)
    cleanedCode.append(line)
    extractOpcode(line)
    extractLiteral(line)
    locationCounter += 12
  assignAddressToVariablesAndLiterals(locationCounter)
  return cleanedCode



##CODE BEGINS HERE##

code = []
mcode=[]

labelTable = {} #Table that stores Label addresses { label : locationAddress }
symbolTable = {} #Table that stores variables in format { variable : [value,locationAddress,size] }
opcodeTable = {} #Table that stores opcodes occuring in the program in format { opcode : [binaryCodeForOpcode, size, inctructionClass] }
# Instruction class = 0 for 0 operand Instructions and 1 for Instructions with one operand
literalTable = {}

for line in sys.stdin:
  # print(line)
  code.append(line.strip())

lineCtr = 0
code = passOne()
# print(code)

for line in code:
  separate=line.split()
  if separate[0] in opcodeTable.keys():
    temp=opcodeTable[separate[0]]
    mcode.append(temp[0])
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
        else:
          print(separate[1])
          pass
          # throw symbol not found exception
      elif(len(separate==1)):
        pass
        # throw too less operands exception
      else:
        pass
        #throw too many operands exception
    if(temp[2]==0):
      mcode[-1]+='00000000'
      if(len(separate)>1):
        # throw too many operands exception
        pass
  else:
    pass 

for x in mcode:
  print(x)
print(labelTable)
print(symbolTable)
# print(opcodeTable)
# print(literalTable)
