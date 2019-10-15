# Assembler
A 2-pass Assembler written in Python for a 12-bit accumulator architecture as part of my Computer Organisation course

## To run
```
$ git clone https://github.com/arundhati-b/Assembler.git
$ python Assembler/assembler.py < [input-file-name].txt
```
Output code will appear in file `bin.txt`

## Files and output
  * `input.txt` Sample input file
  * `bin.txt` Output file/Error file (Stores errors, if any. Otherwise, stores translated machine code)
  Output/Errors are also displayed on terminal.

## Supported instructions

#### Opcodes
`CLA` Clear Accumulator  
`LAC` Load into Accumulator from Memory  
`SAC` Store Accumulator contents in Address  
`ADD` Add address contents to accumulator contents  
`SUB` Subtract address contents from accumulator contents  
`BRZ` Branch to address if accumulator contains zero  
`BRN` Branch to address if accumulator contains negative value  
`BRP` Branch to address if accumulator contains positive value  
`INP` Read from terminal and put in address  
`DSP` Display value in address on terminal  
`MUL` Multiply accumulator and address contents  
`DIV` Divide accumulator contents by address content. Quotient in R1 and remainder in R2  
`STP` Stop execution  

  `STP` should be the last instruction in the program (followed only by variable declarations, if any). Variables can be declared anywhere in the program.

#### Comments
Precede the comment by `//`
```
//This is a comment
CLA // CLears Accumulator
```
**Only single line comments supported. For multiline commenting precede each line by `//`**

#### Labels
Follow label name by a `:`
```
lbl1: STP
```

#### Symbols/Variables
Variables ***must*** be defined using `DW` followed by atmost one operand
```
I DW 22 //Symbol 'I' stored
J DW //Symbol 'J' symply declared
```

#### Literals
Literals are constants that occupy some memory location. Format: `'=*'` (* is a numerical constant value)
```
ADD '=1'
```
#### Error
The code can handle the following errors:  

  * Symbol has been defined more than once  
  * Label cannot be used as a variable  
  * #GivenLabel is a Reserved keyword; Cannot be declared as Variable  
  * Invalid Literal used  
  * Too many opcodes or operands  
  * Variable cannot be a numeric value or start with a digit  
  * Wrong operand type; Only numeric values permitted  
  * 1 byte datatype overflow  
  * 1 byte literal overflow  
  * Address overflow  
  * Label has been defined more than once  
  * Variable cannot be used as a Label  
  * #GivenLabel is a Reserved keyword; Cannot be used as Label  
  * #GivenSymbol is a reserved keyword; cannot be used as symbol  
  * #GivenSymbol Symbol used but not defined  
  * #GivenVariable is a Reserved keyword; Cannot be used as Variable  
  * Too less Operands; Needed:#Needed; Given: #Given  
  * Too many Operands; Needed:#Needed; Given: #Given  
  * #WrongOpcode Opcode used is not a legal Opcode  
  * STP should be the last instruction in the code

## Working

##### passOne()
  In the first pass of the Assembler the Literal Table, Opcode Table, Symbol/Variable Table and Label Table are created.
  Location counter is incremented by fixed number of bits (12) after every instruction.
  Variables are allotted (virtual) memory addresses after the first pass.

##### passTwo()
  Labels and variables are replaced by their memory addresses and opcodes are replaced by their corresponding 4-bit binary codes.

##### Errors
  Errors are added to a list as they are encountered so that the program does not termiate after encountering just one error. Instead, all errors are displayed together.
