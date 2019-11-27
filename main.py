EOF = 0
UNK = 1
VAR = 2
NUM = 3
OPR = 4
KW = 5
VAL = 6
ARR = -1
PTR = -2
var_types = ["float",  "int","short", "long","char", "unsigned", "double", "void"] # TODO check for float
keywords = ["auto", "break", "case", "char", "const", "continue",
          "default",    "do",       "double",   "else",     "enum",     "extern", 
          "float",      "for",      "goto",     "if",       "int",      "long",  # TODO check for float
          "register",   "return",   "short",    "signed",   "static",   "struct",   
          "switch"      "typedef",  "union",    "unsigned", "void",     "volatile", "while"]

class Lab6():
    def __init__(self, *args, **kwargs):
        self.string = kwargs["string"]
        self.lexems = []
        self.variables = dict()
        self.length = len(self.string)

    def get_lexems(self):
        self.lexems = []
        i = 0
        self.length = len(self.string)
        k = 0
        while i<self.length:
            if self.string[i].isspace():   # skip spaces
                i+=1
                while self.string[i].isspace():
                    i+=1
            elif self.string[i].isalpha() or self.string[i]== "_":         # start parsing id
                j = i+1
                while self.string[j].isalnum() or self.string[j]== "_":
                    j += 1
                if self.operator_check(self.string[j]) or self.string[j].isspace():   # found valid id
                    iden = self.string[i:j]
                    if (iden in keywords):                    # id is keyword
                        self.lexems.append([KW, iden, i, j, k])
                    else:                                   # id is variable
                        self.lexems.append([VAR, iden, i, j, k])
                else:                                       # found unk
                    while not (self.operator_check(self.string[j]) or self.string[j].isspace()):
                        j += 1
                    self.lexems.append([UNK, self.string[i:j], i, j, k])
                k += 1
                i = j
            elif self.string[i].isnumeric():                      # start parsing num
                j = i+1
                while self.string[j].isnumeric():
                    j += 1
                if self.operator_check(self.string[j]) or self.string[j].isspace():     # found num
                    self.lexems.append([NUM, self.string[i:j], i, j, k])
                else:                                   # found unk
                    while not (self.operator_check(self.string[j]) or self.string[j].isspace()):
                        j += 1
                    self.lexems.append([UNK, self.string[i:j], i, j, k])
                k += 1
                i = j
            elif self.unique_operator_check(self.string[i]):
                self.lexems.append([self.string[i], self.string[i], i, i + 1, k])
                k += 1
                i += 1
            elif self.operator_check(self.string[i]):
                j = i+1
                if self.string[i] == "=":
                    if self.string[j] == "=":
                        self.lexems.append([OPR, self.string[i:j + 1], i, j + 1, k])
                        i=j+1
                    else:
                        self.lexems.append([OPR, self.string[i], i, i + 1, k])
                        i=j
                elif self.string[j] == "=":
                    if self.string[i] in ["+", "-", "*", "/", "%", "<", ">", "&", "^", "|", "!"]:
                        self.lexems.append([OPR, self.string[i:j + 1], i, j + 1, k])
                    else:
                        self.lexems.append([UNK, self.string[i:j + 1], i, j + 1, k])
                    i=j+1
                elif (self.string[j] == "|" or self.string[j] == "&" or self.string[j] == "+" or self.string[j] == "-"):
                    if (self.string[i] == self.string[j]):
                        self.lexems.append([OPR, self.string[i:j + 1], i, j + 1, k])
                    else:
                        self.lexems.append([UNK, self.string[i:j + 1], i, j + 1, k])
                    i=j+1
                elif (self.string[j] == ">" or self.string[j] == "<"):
                    if self.string[j + 1] == "=":
                        self.lexems.append([OPR, self.string[i:j + 2], i, j + 2, k])
                        i=j+2
                    elif self.string[i] == self.string[j]:
                        self.lexems.append([OPR, self.string[i:j + 1], i, j + 1, k])
                        i=j+1
                    else:
                        self.lexems.append([UNK, self.string[i:j + 1], i, j + 2, k])
                        i=j+1
                    continue
                else:
                    self.lexems.append([OPR, self.string[i], i, j, k])
                    i=j
                k += 1
            else:
                j = i+1
                while not (self.operator_check(self.string[j]) or self.string[j].isspace()):
                    j += 1
                self.lexems.append([UNK, self.string[i:j], i, j, k])
                k += 1
                i = j
        else:
            self.lexems.append([EOF, EOF, self.length, self.length, k])
            k+=1
        self.lexems_length = len(self.lexems)

    def make_error_pointer_string(self, link, expl):
        return self.string + "\n" + "".join(["^" if i == link else " " for i in range(self.length)]) + "\n" + expl

    def definition(self, b, e):
        i = b
        while i<e:
            if self.lexems[i][0]==KW or self.lexems[i][0]==",":
                i+=1
            elif self.lexems[i][1]=="=":
                return (f"Assignment in definition statement not implemented", self.lexems[i][2]) # May need to be implemented
            else:
                return (f"',' or ';' or '=' expected, '{self.lexems[i][1]}' found", self.lexems[i][2])
            while i<=e and self.lexems[i][0]!=VAR:
                if self.lexems[i][0]==";":
                    return ("VAR expected in definition statement", self.lexems[i][2])
                elif self.lexems[i][0]==NUM:
                    return ("unexpected NUM in definition statement", self.lexems[i][2])
                elif self.lexems[i][0] == OPR or self.lexems[i][0]==self.lexems[i][1]:
                    if self.lexems[i][1] not in "*(,)":
                        return ("unexpected operator in definition statement", self.lexems[i][2])
                elif self.lexems[i][0] == UNK:
                    return (f"Unknown token, try renaming '{self.lexems[i][1]}' if it is a variable.", self.lexems[i][2])
                i+=1
            _name = self.lexems[i][1]
            if _name in self.variables:
                return (f"Redeclaration of variable '{_name}' found", self.lexems[i][2])
            _func = False
            _type = []
            j=i+1
            if self.lexems[j][0]=="[":
                j+=1
                k=1
                while j<e and k>0:
                    if self.lexems[j][0] == "[":
                        k += 1
                    elif self.lexems[j][0] == "]":
                        k -= 1
                    elif not self.lexems[j][0]==NUM:
                        return ("integer value expected",  self.lexems[j][2])
                    j+=1
                else:
                    if k>0:
                        return ("']' expected", self.lexems[j][2])
                    # rec point if multidimensional arrays needed
                    _type.append(ARR)

            if self.lexems[i-1][1]=="*":
                _type.append(PTR)
            _type.append(self.lexems[b][1])
            self.variables[_name]= _Var(name=_name, type=_type, func=_func, val=None)
            i = j
        return (False, 0)

    def checkE(self, b, e, **kwargs):
        if (self.lexems[b][0]==KW):
            if (self.lexems[b][1] in var_types):
                return self.definition(b, e)
            else:
                return (f"{self.lexems[b][1]} not implemented", self.lexems[b][2])
        elif (self.lexems[b][0]==VAR or self.lexems[b][0]==NUM) or \
            (self.lexems[b][1] in ["*","+","-","++","--"] and self.lexems[b+1][0]==VAR) or \
            (self.lexems[b][0]=="("):
            stack = self.lexems[b:e]
            for i in stack:
                if i[0]==VAR and i[1] not in self.variables:
                    return (f"Undefined variable/function '{i[1]}'", i[2])
                elif i[0]==UNK:
                    return (f"Unknown token, try renaming '{i[1]}' if it is a variable.", i[2])
                elif i[0]==KW:
                    return (f"Unexpected keyword '{i[1]}' found in regular expression", i[2])
            
            i = 0
            while i<len(stack):
                if (stack[i][0]=="("):
                    k = 1
                    j = i+1
                    while j<len(stack) and k>0:
                        if stack[j][0] == "(":
                            k += 1
                        elif stack[j][0] == ")":
                            k -= 1
                        j+=1
                    if k>0:
                        return ("')' expected", stack[j][2])
                    res, k = self.checkE(b+i+1, b+j-1)
                    if res: return (res, k)
                    if i>0 and stack[i-1][0]==VAR:
                        if self.variables[stack[i - 1][1]].func:
                            stack[i-1][0]=VAL
                            stack[i-1][3]=stack[j-1][3]
                            stack[i-1].append(k)
                        else:
                            return (f"'{stack[i-1][1]}' is not a function")
                    else:
                        if i==j-1:
                            stack.insert(j, [VAR, stack[i+1][1], stack[i][2], stack[j-1][3]])
                        else:
                            stack.insert(j, [VAL, k[1], stack[i][2], stack[j-1][3], k]) # TODO check for float
                    for d in range(i, j):
                        stack.pop(i)
                    i+=1
                elif (stack[i][0]=="["):
                    k = 1
                    j = i+1
                    while j<len(stack) and k>0:
                        if stack[j][0] == "[":
                            k += 1
                        elif stack[j][0] == "]":
                            k -= 1
                        j+=1
                    if k>0:
                        return ("']' expected", stack[j][2])
                    res, k = self.checkE(b+i+1, b+j-1)
                    if res: return (res, k)
                    if k[1] in ["double","float"]:
                        return (f"'{k[1]}' value can't be used as array index", stack[i][3])
                    elif k[0]==VAR and self.variables[k[1]].type[-1] in ["double", "float"]:
                        return (f"'{self.variables[k[1]].type[-1]}' value can't be used as array index", stack[i][3])
                    if i>0 and stack[i-1][0]==VAR and \
                        self.variables[stack[i - 1][1]].type[0]==ARR:
                        stack[i-1][0]=VAL
                        stack[i-1][3]=stack[j-1][3]
                        stack[i-1].append([self.variables[stack[i - 1][1]], k])
                        stack[i-1][1]=self.variables[stack[i - 1][1]].type[-1]
                    else:
                        return (f"'{stack[i-1][1]}' is not an array", stack[i-1][3])
                    for d in range(i, j):
                        stack.pop(i)
                    i+=1
                elif stack[i][1] in ["++", "--"]:
                    if i>0 and stack[i-1][0]==VAR:
                        stack[i-1][0]=VAL
                        stack[i-1][3]=stack[i][3]
                        stack[i-1].append([self.variables[stack[i - 1][1]], stack[i][1]])
                        stack[i-1][1]=self.variables[stack[i - 1][1]].type[-1]
                        stack.pop(i)
                    else: i+=1
                else: i+=1
            
            i = len(stack)-1
            while i>=0:
                if stack[i][1] in ["++", "--"]:
                    if i<len(stack)-1 and stack[i+1][0]==VAR:
                        stack[i+1][0]=VAL
                        stack[i+1][2]=stack[i][2]
                        stack[i+1].append([stack[i][1], self.variables[stack[i + 1][1]]])
                        stack[i+1][1]=self.variables[stack[i + 1][1]].type[-1]
                    else:
                        return (f"'{stack[i][1]}' is supposed to stay near a modifiable lvalue", stack[i][2])
                    stack.pop(i)
                elif stack[i][1] in ["+","-"]:
                    if not (i>0 and stack[i-1][0] in [VAR, VAL, NUM]):
                        if i<len(stack)-1 and stack[i+1][0]==VAR:
                            stack[i+1][0]=VAL
                            stack[i+1][2]=stack[i][2]
                            stack[i+1].append([stack[i][1], self.variables[stack[i + 1][1]]])
                            stack[i+1][1]=self.variables[stack[i + 1][1]].type[-1]
                        else:
                            return (f"'{stack[i][1]}' is supposed to stay near a modifiable value", stack[i][3])
                        stack.pop(i)
                elif stack[i][1]=="*":
                    if not (i>0 and stack[i-1][0] in [VAR, VAL, NUM]):
                        if i<len(stack)-1 and stack[i+1][0]==VAR:
                            stack[i+1][0]=VAL
                            stack[i+1][2]=stack[i][2]
                            stack[i+1].append([stack[i][1], self.variables[stack[i + 1][1]]])
                            stack[i+1][1]=self.variables[stack[i + 1][1]].type[-1]
                        else:
                            return (f"'{stack[i+1][1]}' is supposed to be a pointer", stack[i][3])
                        stack.pop(i)
                i-=1
            
            i = 0
            while i<len(stack):
                if stack[i][1] in ["*","/","%"]:
                    if (i<len(stack)-1 and stack[i+1][0] in [VAR,VAL,NUM]): 
                        if stack[i-1][0]==VAR:
                            k1 = (self.variables[stack[i - 1][1]])
                            _type1 = k1.type[-1]
                        elif stack[i-1][0]==VAL:
                            k1 = (stack[i-1][-1])
                            _type1 = k1[1]
                        else:
                            k1 = stack[i-1][1]
                            _type1 = "int"
                        if stack[i+1][0]==VAR:
                            k2 = (self.variables[stack[i + 1][1]])
                            _type2 = k2.type[-1]
                        elif stack[i+1][0]==VAL:
                            k2 = (stack[i+1][-1])
                            _type2 = k2[1]
                        else:
                            k2 = stack[i+1][1]
                            _type2 = "int"
                        if _type1=="double" or _type2=="double":
                            _type="double"
                        elif _type1=="float" or _type2=="float":
                            _type="float"
                        else:
                            _type="int"
                        stack.insert(i+2, [VAL, _type, stack[i-1][2], stack[i+1][3], [stack[i][1], k1, k2]]) # TODO check for float
                        [stack.pop(i-1) for l in range(i-1,i+2)]
                    else:
                        if i==len(stack)-1:
                            return (f"Expected another operand", stack[i+1][2])
                        else:
                            return (f"Expected rvalue, found '{stack[i+1][1]}'", stack[i+1][2])
                else: i+=1
            
            i = 0
            while i<len(stack):
                if stack[i][1] in ["+","-"]:
                    if (i<len(stack)-1 and stack[i+1][0] in [VAR,VAL]): 
                        if stack[i-1][0]==VAR:
                            k1 = (self.variables[stack[i - 1][1]])
                            _type1 = k1.type[-1]
                        elif stack[i-1][0]==VAL:
                            k1 = (stack[i-1][-1])
                            _type1 = k1[1]
                        else:
                            k1 = stack[i-1][1]
                            _type1 = "int"
                        if stack[i+1][0]==VAR:
                            k2 = (self.variables[stack[i + 1][1]])
                            _type2 = k2.type[-1]
                        elif stack[i+1][0]==VAL:
                            k2 = (stack[i+1][-1])
                            _type2 = k2[1]
                        else:
                            k2 = stack[i+1][1]
                            _type2 = "int"
                        if _type1=="double" or _type2=="double":
                            _type="double"
                        elif _type1=="float" or _type2=="float":
                            _type="float"
                        else:
                            _type="int"
                        stack.insert(i+2, [VAL, _type, stack[i-1][2], stack[i+1][3], [stack[i][1], k1, k2]]) # TODO check for float
                        [stack.pop(i-1) for l in range(i-1,i+2)]
                    else:
                        if i==len(stack)-1:
                            return (f"Expected another operand", stack[i+1][2])
                        else:
                            return (f"Expected rvalue, found '{stack[i+1][1]}'", stack[i+1][2])
                else: i+=1
            
            i = len(stack)-1
            while i>=0:# TODO to reverse polish
                if stack[i][1]=="=":
                    if (i>0 and stack[i-1][0]==VAR):
                        if (i<len(stack)-1 and stack[i+1][0] in [VAR,VAL,NUM]): 
                            k1 = (self.variables[stack[i - 1][1]])
                            k2 = (self.variables[stack[i + 1][1]]) if stack[i + 1][0] == VAR else\
                                (stack[i+1][-1]) if stack[i+1][0]==VAL else\
                                stack[i+1][1]
                            stack.insert(i+2, [VAL, k1.type[-1], stack[i-1][2], stack[i+1][3], [stack[i][1], k1, k2]]) # TODO check for float
                            [stack.pop(i-1) for l in range(i-1,i+2)]
                        else:
                            if i==len(stack)-1:
                                return (f"Expected another operand", stack[i+1][2])
                            else:
                                return (f"Expected rvalue, found '{stack[i+1][1]}'", stack[i+1][2])
                    else:
                        if i==0:
                            return (f"lvalue expected", stack[0][2])
                        else:
                            return (f"Expected lvalue, found '{stack[i-1][1]}'", stack[i-1][2])
                elif stack[i][1] in ["+=", "-=", "/=", "*="]:
                    if (i>0 and stack[i-1][0]==VAR):
                        if (i<len(stack)-1 and stack[i+1][0] in [VAR,VAL,NUM]): 
                            k1 = (self.variables[stack[i - 1][1]])
                            k2 = (self.variables[stack[i + 1][1]]) if stack[i + 1][0] == VAR else\
                                (stack[i+1][-1]) if stack[i+1][0]==VAL else\
                                stack[i+1][1]
                            stack.insert(i+2, [VAL, k1.type[-1], stack[i-1][2], stack[i+1][3], ["=", k1, [stack[i][1][0], k1, k2]]]) # TODO check for float
                            [stack.pop(i-1) for l in range(i-1,i+2)]
                        else:
                            if i==len(stack)-1:
                                return (f"Expected another operand", stack[i+1][2])
                            else:
                                return (f"Expected rvalue, found '{stack[i+1][1]}'", stack[i+1][2])
                    else:
                        if i==0:
                            return (f"lvalue expected", stack[0][2])
                        else:
                            return (f"Expected lvalue, found '{stack[i-1][1]}'", stack[i-1][2])
                i-=1
                    
            # i = 0
            # while i<len(stack):
            #     elif ",":
            return (False, stack[0])
        else:
            return (f"Expected 'var' or '(', found '{self.lexems[b][1]}' ", self.lexems[b][2])

    def main_analyze(self):
        l = 0
        while l<self.lexems_length:
            i = l
            while i<self.lexems_length:
                if self.lexems[i][0]==";":
                    res, k = self.checkE(l, i)
                    if res: return self.make_error_pointer_string(k, res)
                    i+=1
                    l=i
                    break
                i+=1
            else:
                if self.lexems[-2][0]!=";":
                    return self.make_error_pointer_string(self.lexems[-2][2], "';' expected")
                break
            
        return False

    def operator_check(self, char: str):
        return char in "-+*/%<>=!|&^~\x7b\x7d()[],;?:." or char == "sizeof"

    def unique_operator_check(self, char: str):
        return char in "\x7b\x7d()[],;?:."

    def analyze(self):
        self.get_lexems()
        print(self.lexems)
        self.res = self.main_analyze()
        if self.res: 
            return self.res
        else:
            return "No syntax errors found.\nAnalyzer returned exit code 0"
class _Var():
    def __init__(self, *args, **kwargs):
        self.name = kwargs["name"]
        self.type = kwargs["type"]
        self.func = kwargs["func"]
        self.val = kwargs["val"]

if __name__ == "__main__":
    text = "float *b, a[5]; int n; b+=a;"

    analizer = Lab6(string=text)

    print(f"\n{text}\n")
    print(analizer.analyze())
