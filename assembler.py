import sys

def addLabel(label,LC):
  labelTable[label] = LC

def addOpcode(opcode, opcodeBin, size, instructionClass):
  opcodeTable[opcode] = [opcodeBin, size, instructionClass]

def addSymbol(variable,value,size):
  symbolTable[variable] = [value,None,size]

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

def assignAddressToVariables(LC):
  for i in symbolTable:
    symbolTable[i][1] = LC
    LC += symbolTable[i][2]

def passOne():
  lineCtr = 0
  locationCounter = 0

  for line in code:
    lineCtr += 1
    if isComment(line):
      continue
    line = removeComment(line)
    print(line)
    label, line = checkLabel(line)
    if label != '':
      addLabel(label,locationCounter)
    extractOpcode(line)
    locationCounter += 12

  assignAddressToVariables(locationCounter)


code = []

labelTable = {} #Table that stores Label addresses { label : locationAddress }
symbolTable = {} #Table that stores variables in format { variable : [value,locationAddress,size] }
opcodeTable = {} #Table that stores opcodes occuring in the program in format { opcode : [binaryCodeForOpcode, size, inctructionClass] }
# Instruction class = 0 for 0 operand Instructions and 1 for Instructions with one operand
literalTable = {}

for line in sys.stdin:
  # print(line)
  code.append(line.strip())

lineCtr = 0
passOne()


# print(labelTable)
# print(symbolTable)
# print(opcodeTable)

