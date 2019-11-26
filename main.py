EOF, UNK, VAR, NUM, OPR, KW, VAL = range(7)
ARR, PTR = -1, -2
TYPES = ["float", "char", "int", "unsigned", "short", "long", "double", "void"] # TODO check for float
C_KEYW = ["auto",       "break",    "case",     "char",     "const",    "continue",
          "default",    "do",       "double",   "else",     "enum",     "extern", 
          "float",      "for",      "goto",     "if",       "int",      "long", # TODO check for float
          "register",   "return",   "short",    "signed",   "static",   "struct",   
          "switch"      "typedef",  "union",    "unsigned", "void",     "volatile", "while"]
class _Var():
    def __init__(self, *args, **kwargs):
        self.name = kwargs["name"]
        self.type = kwargs["type"]
        self.func = kwargs["func"]
        self.val = kwargs["val"]

class Lab6():
    def __init__(self, *args, **kwargs):
        self.s = kwargs["s"]
        self.lex = []
        self.vars = dict()
        self.n = len(self.s)

    def is_oper(self, char : str):
        return char in "-+*/%<>=!|&^~\x7b\x7d()[],;?:." or char=="sizeof"
        
    def is_unq_oper(self, char : str):
        return char in "\x7b\x7d()[],;?:."

    def lex_an(self):
        self.lex = []
        i = 0
        self.n = len(self.s)
        k = 0
        while i<self.n:
            if self.s[i].isspace():   # skip spaces
                i+=1
                while self.s[i].isspace():
                    i+=1
            elif self.s[i].isalpha() or self.s[i]=="_":         # start parsing id
                j = i+1
                while self.s[j].isalnum() or self.s[j]=="_":
                    j += 1
                if self.is_oper(self.s[j]) or self.s[j].isspace():   # found valid id
                    iden = self.s[i:j]
                    if (iden in C_KEYW):                    # id is keyword
                        self.lex.append([KW, iden, i, j, k])
                    else:                                   # id is variable
                        self.lex.append([VAR, iden, i, j, k])
                else:                                       # found unk
                    while not (self.is_oper(self.s[j]) or self.s[j].isspace()):
                        j += 1
                    self.lex.append([UNK, self.s[i:j], i, j, k])
                k += 1
                i = j
            elif self.s[i].isnumeric():                      # start parsing num
                j = i+1
                while self.s[j].isnumeric():
                    j += 1
                if self.is_oper(self.s[j]) or self.s[j].isspace():     # found num
                    self.lex.append([NUM, self.s[i:j], i, j, k])
                else:                                   # found unk
                    while not (self.is_oper(self.s[j]) or self.s[j].isspace()):
                        j += 1
                    self.lex.append([UNK, self.s[i:j], i, j, k])
                k += 1
                i = j
            elif self.is_unq_oper(self.s[i]):
                self.lex.append([self.s[i], self.s[i], i, i+1, k])
                k += 1
                i += 1
            elif self.is_oper(self.s[i]):
                j = i+1
                if self.s[i] == "=":
                    if self.s[j] == "=":
                        self.lex.append([OPR, self.s[i:j+1], i, j+1, k])
                        i=j+1
                    else:
                        self.lex.append([OPR, self.s[i], i, i+1, k])
                        i=j
                elif self.s[j] == "=":
                    if self.s[i] in ["+", "-", "*", "/", "%", "<", ">", "&", "^", "|", "!"]:
                        self.lex.append([OPR, self.s[i:j+1], i, j+1, k])
                    else:
                        self.lex.append([UNK, self.s[i:j+1], i, j+1, k])
                    i=j+1
                elif (self.s[j] == "|" or self.s[j] == "&" or self.s[j] == "+" or self.s[j] == "-"):
                    if (self.s[i] == self.s[j]):
                        self.lex.append([OPR, self.s[i:j+1], i, j+1, k])
                    else:
                        self.lex.append([UNK, self.s[i:j+1], i, j+1, k])
                    i=j+1
                elif (self.s[j] == ">" or self.s[j] == "<"):
                    if self.s[j+1] == "=":
                        self.lex.append([OPR, self.s[i:j+2], i, j+2, k])
                        i=j+2
                    elif self.s[i] == self.s[j]:
                        self.lex.append([OPR, self.s[i:j+1], i, j+1, k])
                        i=j+1
                    else:
                        self.lex.append([UNK, self.s[i:j+1], i, j+2, k])
                        i=j+1
                    continue
                else:
                    self.lex.append([OPR, self.s[i], i, j, k])      
                    i=j
                k += 1
            else:
                j = i+1
                while not (self.is_oper(self.s[j]) or self.s[j].isspace()):
                    j += 1
                self.lex.append([UNK, self.s[i:j], i, j, k])
                k += 1
                i = j
        else:
            self.lex.append([EOF, EOF, self.n, self.n, k])
            k+=1
        self.nlex = len(self.lex)

    def errstr(self, link, expl):
        return self.s+"\n"+"".join(["^" if i==link else " " for i in range(self.n)])+"\n"+expl

    def definition(self, b, e):
        
        # def reccurPointers(i, rec=0):
        #     result = []
        #     v, p = i, i
        #     t1,t2 = i, i
        #     while t1>=0 or t2>=0:
        #         if t2>=0 and t2+1<=e and self.lex[t2+1][0]=="[":
        #             i+=1
        #             p = t2
        #             while i+1<=e:
        #                 i+=1
        #                 if lex[i][0]=="]":
        #                     res = self.checkE(p+1, i, type="whole")
        #                     if res: 
        #                         return res
        #                     else:
        #                         result.extend([[ARR, p+1, i]])
        #                         if not self.lex[i+1][0]=="[":
        #                             if not self.lex[i+1][0]==")":
        #                                 result = self.errstr(self.lex[i+1][2], f"unexpected expression {lex[i+1][1]}")
        #                             elif self.lex[i+1][1]==";" or self.lex[i+1][1]=="=":
        #                                 t2 = -1
        #                         else:
        #                             t2 = i
        #                             res, t2 = self.definition(t2, rec=1)
        #                             result.extend(res)
        #         elif t1-1>=b and self.lex[t1-1][0]=="*":
        #             p = t1
        #             result.extend([[PTR]])
        #             res, t1 = self.definition(t1, rec=1)
        #             result.extend(res)
                
        #     if not rec: return result
        #     else: return (result, term)
        i = b
        while i<e:
            if self.lex[i][0]==KW or self.lex[i][0]==",":
                i+=1
            elif self.lex[i][1]=="=":
                return (f"Assignment in definition statement not implemented", self.lex[i][2]) # May need to be implemented
            else:
                return (f"',' or ';' or '=' expected, '{self.lex[i][1]}' found", self.lex[i][2])
            while i<=e and self.lex[i][0]!=VAR:
                if self.lex[i][0]==";":
                    return ("VAR expected in definition statement", self.lex[i][2])
                elif self.lex[i][0]==NUM:
                    return ("unexpected NUM in definition statement", self.lex[i][2])
                elif self.lex[i][0] == OPR or self.lex[i][0]==self.lex[i][1]:
                    if self.lex[i][1] not in "*(,)":
                        return ("unexpected operator in definition statement", self.lex[i][2])
                elif self.lex[i][0] == UNK:
                    return (f"Unknown token, try renaming '{self.lex[i][1]}' if it is a variable.", self.lex[i][2])
                i+=1
            _name = self.lex[i][1]
            if _name in self.vars:
                return (f"Redeclaration of variable '{_name}' found", self.lex[i][2])
            _func = False
            _type = []
            j=i+1
            if self.lex[j][0]=="[":
                j+=1
                k=1
                while j<e and k>0:
                    if self.lex[j][0] == "[":
                        k += 1
                    elif self.lex[j][0] == "]":
                        k -= 1
                    elif not self.lex[j][0]==NUM:
                        return ("integer value expected",  self.lex[j][2])
                    j+=1
                else:
                    if k>0:
                        return ("']' expected", self.lex[j][2])
                    # rec point if multidimensional arrays needed
                    _type.append(ARR)

            if self.lex[i-1][1]=="*":
                _type.append(PTR)
            _type.append(self.lex[b][1])
            self.vars[_name]= _Var(name=_name, type=_type, func=_func, val=None)
            i = j
        return (False, 0)

    def checkE(self, b, e, **kwargs):
        if (self.lex[b][0]==KW):
            if (self.lex[b][1] in TYPES):
                return self.definition(b, e)
            else:
                return (f"{self.lex[b][1]} not implemented", self.lex[b][2])
        elif (self.lex[b][0]==VAR) or \
            (self.lex[b][1] in ["*","+","-","++","--"] and self.lex[b+1][0]==VAR) or \
            (self.lex[b][0]=="("):
            stack = self.lex[b:e]
            for i in stack:
                if i[0]==VAR and i[1] not in self.vars:
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
                    res, k = self.checkE(i+1, j-2)
                    if res: return (res, k)
                    if i>0 and stack[i-1][0]==VAR:
                        if self.vars[stack[i-1][1]].func:
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
                    elif k[0]==VAR and self.vars[k[1]].type[-1] in ["double","float"]:
                        return (f"'{self.vars[k[1]].type[-1]}' value can't be used as array index", stack[i][3])
                    if i>0 and stack[i-1][0]==VAR and \
                        self.vars[stack[i-1][1]].type[0]==ARR:
                        stack[i-1][0]=VAL
                        stack[i-1][3]=stack[j-1][3]
                        stack[i-1].append([self.vars[stack[i-1][1]], k])
                        stack[i-1][1]=self.vars[stack[i-1][1]].type[-1]
                    else:
                        return (f"'{stack[i-1][1]}' is not an array", stack[i-1][3])
                    for d in range(i, j):
                        stack.pop(i)
                    i+=1
                elif stack[i][1] in ["++", "--"]:
                    if i>0 and stack[i-1][0]==VAR:
                        stack[i-1][0]=VAL
                        stack[i-1][3]=stack[i][3]
                        stack[i-1].append([self.vars[stack[i-1][1]], stack[i][1]])
                        stack[i-1][1]=self.vars[stack[i-1][1]].type[-1]
                        stack.pop(i)
                    else: i+=1
                else: i+=1
            
            i = len(stack)-1
            while i>=0:
                if stack[i][1] in ["++", "--"]:
                    if i<len(stack)-1 and stack[i+1][0]==VAR:
                        stack[i+1][0]=VAL
                        stack[i+1][2]=stack[i][2]
                        stack[i+1].append([stack[i][1], self.vars[stack[i+1][1]]])
                        stack[i+1][1]=self.vars[stack[i+1][1]].type[-1]
                    else:
                        return (f"'{stack[i][1]}' is supposed to stay near a modifiable lvalue", stack[i][2])
                    stack.pop(i)
                elif stack[i][1] in ["+","-"]:
                    if not (i>0 and stack[i-1][0] in [VAR, VAL, NUM]):
                        if i<len(stack)-1 and stack[i+1][0]==VAR:
                            stack[i+1][0]=VAL
                            stack[i+1][2]=stack[i][2]
                            stack[i+1].append([stack[i][1], self.vars[stack[i+1][1]]])
                            stack[i+1][1]=self.vars[stack[i+1][1]].type[-1]
                        else:
                            return (f"'{stack[i][1]}' is supposed to stay near a modifiable value", stack[i][3])
                        stack.pop(i)
                elif stack[i][1]=="*":
                    if not (i>0 and stack[i-1][0] in [VAR, VAL, NUM]):
                        if i<len(stack)-1 and stack[i+1][0]==VAR:
                            stack[i+1][0]=VAL
                            stack[i+1][2]=stack[i][2]
                            stack[i+1].append([stack[i][1], self.vars[stack[i+1][1]]])
                            stack[i+1][1]=self.vars[stack[i+1][1]].type[-1]
                        else:
                            return (f"'{stack[i+1][1]}' is supposed to be a pointer", stack[i][3])
                        stack.pop(i)
                i-=1
            
            i = 0
            while i<len(stack):
                if stack[i][1] in ["*","/","%"]:
                    if (i<len(stack)-1 and stack[i+1][0] in [VAR,VAL,NUM]): 
                        if stack[i-1][0]==VAR:
                            k1 = (self.vars[stack[i-1][1]])
                            _type1 = k1.type[-1]
                        elif stack[i-1][0]==VAL:
                            k1 = (stack[i-1][-1])
                            _type1 = k1[1]
                        else:
                            k1 = stack[i-1][1]
                            _type1 = "int"
                        if stack[i+1][0]==VAR:
                            k2 = (self.vars[stack[i+1][1]])
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
                            k1 = (self.vars[stack[i-1][1]])
                            _type1 = k1.type[-1]
                        elif stack[i-1][0]==VAL:
                            k1 = (stack[i-1][-1])
                            _type1 = k1[1]
                        else:
                            k1 = stack[i-1][1]
                            _type1 = "int"
                        if stack[i+1][0]==VAR:
                            k2 = (self.vars[stack[i+1][1]])
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
                            k1 = (self.vars[stack[i-1][1]])
                            k2 = (self.vars[stack[i+1][1]]) if stack[i+1][0]==VAR else\
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
                            k1 = (self.vars[stack[i-1][1]])
                            k2 = (self.vars[stack[i+1][1]]) if stack[i+1][0]==VAR else\
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
            return (f"Expected 'var' or '(', found '{self.lex[b][1]}' ")


    def synt_an(self):
        l = 0
        while l<self.nlex:
            i = l
            while i<self.nlex:
                if self.lex[i][0]==";":
                    res, k = self.checkE(l, i)
                    if res: return self.errstr(k, res)
                    i+=1
                    l=i
                    break
                i+=1
            else:
                if self.lex[-2][0]!=";":
                    return self.errstr(self.lex[-2][2], "';' expected")
                break
            
        return False


    def analyze(self):
        self.lex_an()
        self.res = self.synt_an()
        if self.res: 
            return self.res
        else:
            return "No syntax errors found.\nAnalyzer returned exit code 0"

if __name__ == "__main__":
    text1 = "float b,a,c,*d;b=(2*a+c/d)*2*a;" #"float b,a,c,*d;b=(2*a+c/d)*2*a;"
    text2 = "float *b, a[5]; int n; b+=a[n];"
    text3 = "float *b,a[5]; char n; b+=a[--n];" # main
    text4 = "double *a; int b;b=sin(2*a);b=2*a;"
    analizer1 = Lab6(s=text1)
    analizer2 = Lab6(s=text2)
    analizer3 = Lab6(s=text3)
    analizer4 = Lab6(s=text4)
    print(f"\n---------------\n{text1}\n")
    print(analizer1.analyze())
    print(f"\n---------------\n{text2}\n")
    print(analizer2.analyze())
    print(f"\n---------------\n{text3}\n")
    print(analizer3.analyze())
    print(f"\n---------------\n{text4}\n")
    print(analizer4.analyze())