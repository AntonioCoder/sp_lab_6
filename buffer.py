EOF = 0
UNK = 1
VAR = 2
NUM = 3
OPR = 4
KW = 5
VAL = 6
ARR = -1
PTR = -2
var_types = ["float",  "int","short", "long","char", "unsigned", "double", "void"]
keywords = ["auto", "break", "case", "char", "const", "continue",
          "default", "do", "double", "else", "enum", "extern",
          "float", "for", "goto", "if", "int", "long",
          "register", "return", "short", "signed", "static", "struct",
          "switch"      "typedef", "union", "unsigned", "void", "volatile", "while"]





class Lab6():
    def __init__(self, *args, **kwargs):
        self.string = kwargs["string"]
        self.lexems = []
        self.variables = dict()
        self.n = len(self.string)

    @staticmethod
    def operator_valid(char: str):
        return char in "-+*/%<>=!|&^~\x7b\x7d()[],;?:." or char == "sizeof"

    @staticmethod
    def unique_operator_valid(char: str):
        return char in "\x7b\x7d()[],;?:."

    def get_lexems(self):
        self.lexems = []
        i = 0
        self.n = len(self.string)
        k = 0
        while i < self.n:
            if self.string[i].isspace():  # skip spaces
                i += 1
                while self.string[i].isspace():
                    i += 1
            elif self.string[i].isalpha() or self.string[i] == "_":  # start parsing id
                j = i + 1
                while self.string[j].isalnum() or self.string[j] == "_":
                    j += 1
                if self.operator_valid(self.string[j]) or self.string[j].isspace():  # found valid id
                    iden = self.string[i:j]
                    if (iden in keywords):  # id is keyword
                        self.lexems.append([KW, iden, i, j, k])
                    else:  # id is variable
                        self.lexems.append([VAR, iden, i, j, k])
                else:  # found unk
                    while not (self.operator_valid(self.string[j]) or self.string[j].isspace()):
                        j += 1
                    self.lexems.append([UNK, self.string[i:j], i, j, k])
                k += 1
                i = j
            elif self.string[i].isnumeric():  # start parsing num
                j = i + 1
                while self.string[j].isnumeric():
                    j += 1
                if self.operator_valid(self.string[j]) or self.string[j].isspace():  # found num
                    self.lexems.append([NUM, self.string[i:j], i, j, k])
                else:  # found unk
                    while not (self.operator_valid(self.string[j]) or self.string[j].isspace()):
                        j += 1
                    self.lexems.append([UNK, self.string[i:j], i, j, k])
                k += 1
                i = j
            elif self.unique_operator_valid(self.string[i]):
                self.lexems.append([self.string[i], self.string[i], i, i + 1, k])
                k += 1
                i += 1
            elif self.operator_valid(self.string[i]):
                j = i + 1
                if self.string[i] == "=":
                    if self.string[j] == "=":
                        self.lexems.append([OPR, self.string[i:j + 1], i, j + 1, k])
                        i = j + 1
                    else:
                        self.lexems.append([OPR, self.string[i], i, i + 1, k])
                        i = j
                elif self.string[j] == "=":
                    if self.string[i] in ["+", "-", "*", "/", "%", "<", ">", "&", "^", "|", "!"]:
                        self.lexems.append([OPR, self.string[i:j + 1], i, j + 1, k])
                    else:
                        self.lexems.append([UNK, self.string[i:j + 1], i, j + 1, k])
                    i = j + 1
                elif (self.string[j] == "|" or self.string[j] == "&" or self.string[j] == "+" or self.string[j] == "-"):
                    if (self.string[i] == self.string[j]):
                        self.lexems.append([OPR, self.string[i:j + 1], i, j + 1, k])
                    else:
                        self.lexems.append([UNK, self.string[i:j + 1], i, j + 1, k])
                    i = j + 1
                elif (self.string[j] == ">" or self.string[j] == "<"):
                    if self.string[j + 1] == "=":
                        self.lexems.append([OPR, self.string[i:j + 2], i, j + 2, k])
                        i = j + 2
                    elif self.string[i] == self.string[j]:
                        self.lexems.append([OPR, self.string[i:j + 1], i, j + 1, k])
                        i = j + 1
                    else:
                        self.lexems.append([UNK, self.string[i:j + 1], i, j + 2, k])
                        i = j + 1
                    continue
                else:
                    self.lexems.append([OPR, self.string[i], i, j, k])
                    i = j
                k += 1
            else:
                j = i + 1
                while not (self.operator_valid(self.string[j]) or self.string[j].isspace()):
                    j += 1
                self.lexems.append([UNK, self.string[i:j], i, j, k])
                k += 1
                i = j
        else:
            self.lexems.append([EOF, EOF, self.n, self.n, k])
            k += 1
        self.nlex = len(self.lexems)

    def make_error_pointer_string(self, link, expl):
        return self.string + "\n" + "".join(["^" if i == link else " " for i in range(self.n)]) + "\n" + expl

    def definition(self, b, e):
        i = b
        while i < e:
            if self.lexems[i][0] == KW or self.lexems[i][0] == ",":
                i += 1
            elif self.lexems[i][1] == "=":
                return ("Assignment in definition not implemented", self.lexems[i][2])  # May need to be implemented
            else:
                return (", or ; or = expected, {} found".format(self.lexems[i][1]), self.lexems[i][2])
            while i <= e and self.lexems[i][0] != VAR:
                if self.lexems[i][0] == ";":
                    return ("variable expected in definition statement", self.lexems[i][2])
                elif self.lexems[i][0] == NUM:
                    return ("unexpected number in definition statement", self.lexems[i][2])
                elif self.lexems[i][0] == OPR or self.lexems[i][0] == self.lexems[i][1]:
                    if self.lexems[i][1] not in "*(,)":
                        return ("unexpected operator in definition statement", self.lexems[i][2])
                elif self.lexems[i][0] == UNK:
                    return ("Unknown token".format(self.lexems[i][1]), self.lexems[i][2])
                i += 1
            _name = self.lexems[i][1]
            if _name in self.variables:
                return ("Redeclaration of variable {} found".format(_name), self.lexems[i][2])
            _func = False
            _type = []
            j = i + 1
            if self.lexems[j][0] == "[":
                j += 1
                k = 1
                while j < e and k > 0:
                    if self.lexems[j][0] == "[":
                        k += 1
                    elif self.lexems[j][0] == "]":
                        k -= 1
                    elif not self.lexems[j][0] == NUM:
                        return ("integer value expected", self.lexems[j][2])
                    j += 1
                else:
                    if k > 0:
                        return ("] expected", self.lexems[j][2])
                    # rec point if multidimensional arrays needed
                    _type.append(ARR)

            if self.lexems[i - 1][1] == "*":
                _type.append(PTR)
            _type.append(self.lexems[b][1])
            self.variables[_name] = _Var(name=_name, type=_type, func=_func, val=None)
            i = j
        return (False, 0)

    def main(self):
        self.get_lexems()
        self.res = self.main_analyze()
        if self.res:
            return self.res
        else:
            return "No syntax errors found."

    def main_analyze(self):
        l = 0
        while l < self.nlex:
            i = l
            while i < self.nlex:
                if self.lexems[i][0] == ";":
                    self.poped = 0
                    res, k = self.check_expression(l, i)
                    if res: return self.make_error_pointer_string(k, res)
                    i += 1
                    l = i
                    break
                i += 1
            else:
                if self.lexems[-2][0] != ";":
                    return self.make_error_pointer_string(self.lexems[-2][2], "';' expected")
                break

        return False

    def check_expression(self, b, e):
        if (self.lexems[b][0] == KW):
            if (self.lexems[b][1] in var_types):
                return self.definition(b, e)
            else:
                return ("{} not implemented".format(self.lexems[b][1]), self.lexems[b][2])
        elif (self.lexems[b][0] == VAR or self.lexems[b][0] == NUM) or \
                (self.lexems[b][1] in ["*", "+", "-", "++", "--"] and self.lexems[b + 1][0] == VAR) or \
                (self.lexems[b][0] == "("):
            buffer = self.lexems[b:e]
            for i in buffer:
                if i[0] == VAR and i[1] not in self.variables:
                    return ("Undefined variable '{}'".format(i[1]), i[2])
                elif i[0] == UNK:
                    return ("Unknown token", i[2])
                elif i[0] == KW:
                    return ("Unexpected keyword {} found in regular expression".format(i[1]), i[2])

            i = 0
            while i < len(buffer):
                if (buffer[i][0] == "("):
                    k = 1
                    j = i + 1
                    while j < len(buffer) and k > 0:
                        if buffer[j][0] == "(":
                            k += 1
                        elif buffer[j][0] == ")":
                            k -= 1
                        j += 1
                    if k > 0:
                        return (") expected", buffer[j][2])
                    res, k = self.check_expression(self.poped + b + i + 1, self.poped + b + j - 1)
                    if res: return (res, k)
                    if i > 0 and buffer[i - 1][0] == VAR:
                        if self.variables[buffer[i - 1][1]].func:
                            buffer[i - 1][0] = VAL
                            buffer[i - 1][3] = buffer[j - 1][3]
                            buffer[i - 1].append(k)
                        else:
                            return ("{} is not a function".format(buffer[i - 1][1]))
                    else:
                        if i + 1 == j - 2:
                            buffer.insert(j, [VAR, buffer[i + 1][1], buffer[i][2], buffer[j - 1][3]])
                        else:
                            buffer.insert(j, [VAL, k[1], buffer[i][2], buffer[j - 1][3], k])
                    for d in range(i, j):
                        self.poped += 1
                        buffer.pop(i)
                    self.poped -= 1
                    i += 1
                elif (buffer[i][0] == ')' or buffer[i][0] == ']'):
                    return ("Unexpected {}".format(buffer[i][0]), buffer[i][2])
                elif (buffer[i][0] == "["):
                    k = 1
                    j = i + 1
                    while j < len(buffer) and k > 0:
                        if buffer[j][0] == "[":
                            k += 1
                        elif buffer[j][0] == "]":
                            k -= 1
                        j += 1
                    if k > 0:
                        return ("']' expected", buffer[j][2])
                    res, k = self.check_expression(self.poped + b + i + 1, self.poped + b + j - 1)
                    if res: return (res, k)
                    if k[1] in ["double", "float"]:
                        return ("'{}' value can't be used as array index".format(k[1]), buffer[i][3])
                    elif k[0] == VAR and self.variables[k[1]].type[-1] in ["double", "float"]:
                        return ("'{}' value can't be used as array index".format(self.variables[k[1]].type[-1]), buffer[i][3])
                    if i > 0 and buffer[i - 1][0] == VAR and \
                            self.variables[buffer[i - 1][1]].type[0] == ARR:
                        buffer[i - 1][0] = VAL
                        buffer[i - 1][3] = buffer[j - 1][3]
                        buffer[i - 1].append([self.variables[buffer[i - 1][1]], k])
                        buffer[i - 1][1] = self.variables[buffer[i - 1][1]].type[-1]
                    else:
                        return ("'{}' is not an array".format(buffer[i - 1][1]), buffer[i - 1][3])
                    for d in range(i, j):
                        self.poped += 1
                        buffer.pop(i)
                    i += 1
                elif buffer[i][1] in ["++", "--"]:
                    if i > 0 and buffer[i - 1][0] == VAR:
                        buffer[i - 1][0] = VAL
                        buffer[i - 1][3] = buffer[i][3]
                        buffer[i - 1].append([self.variables[buffer[i - 1][1]], buffer[i][1]])
                        buffer[i - 1][1] = self.variables[buffer[i - 1][1]].type[-1]
                        self.poped += 1
                        buffer.pop(i)
                    else:
                        i += 1
                elif buffer[i][0] == VAR and self.variables[buffer[i][1]].type[0] == ARR:
                    if b + i < len(self.lexems) - 1:
                        if not self.lexems[b + i + 1][0] == "[":
                            if not (self.lexems[b + i + 1][0] == ")" and b + i > 0 and self.lexems[b + i - 1][
                                0] == "("):
                                return ("'[' expected", buffer[i][3])
                            i += 1
                        i += 1
                    else:
                        return ("'[' expected", buffer[i][3])
                else:
                    i += 1

            i = len(buffer) - 1
            while i >= 0:
                if buffer[i][1] in ["++", "--"]:
                    if i < len(buffer) - 1 and buffer[i + 1][0] == VAR:
                        buffer[i + 1][0] = VAL
                        buffer[i + 1][2] = buffer[i][2]
                        buffer[i + 1].append([buffer[i][1], self.variables[buffer[i + 1][1]]])
                        buffer[i + 1][1] = self.variables[buffer[i + 1][1]].type[-1]
                    else:
                        return ("'{}' is supposed to stay near a modifiable lvalue".format(buffer[i][1]), buffer[i][2])
                    self.poped += 1
                    buffer.pop(i)
                elif buffer[i][1] in ["+", "-"]:
                    if not (i > 0 and buffer[i - 1][0] in [VAR, VAL, NUM]):
                        if i < len(buffer) - 1 and buffer[i + 1][0] == VAR:
                            buffer[i + 1][0] = VAL
                            buffer[i + 1][2] = buffer[i][2]
                            buffer[i + 1].append([buffer[i][1], self.variables[buffer[i + 1][1]]])
                            buffer[i + 1][1] = self.variables[buffer[i + 1][1]].type[-1]
                        else:
                            return ("'{}' is supposed to stay near a modifiable value".format(buffer[i][1]), buffer[i][3])
                        self.poped += 1
                        buffer.pop(i)
                elif buffer[i][1] == "*":
                    if not (i > 0 and buffer[i - 1][0] in [VAR, VAL, NUM]):
                        if i < len(buffer) - 1 and buffer[i + 1][0] == VAR:
                            buffer[i + 1][0] = VAL
                            buffer[i + 1][2] = buffer[i][2]
                            buffer[i + 1].append([buffer[i][1], self.variables[buffer[i + 1][1]]])
                            buffer[i + 1][1] = self.variables[buffer[i + 1][1]].type[-1]
                        else:
                            return ("'{}' is supposed to be a pointer".format(buffer[i + 1][1]), buffer[i][3])
                        self.poped += 1
                        buffer.pop(i)
                i -= 1

            i = 0
            while i < len(buffer):
                if buffer[i][1] in ["*", "/", "%"]:
                    if (i < len(buffer) - 1 and buffer[i + 1][0] in [VAR, VAL, NUM]):
                        if buffer[i - 1][0] == VAR:
                            k1 = (self.variables[buffer[i - 1][1]])
                            _type1 = k1.type[-1]
                        elif buffer[i - 1][0] == VAL:
                            k1 = (buffer[i - 1][-1])
                            _type1 = k1[1]
                        else:
                            k1 = buffer[i - 1][1]
                            _type1 = "int"
                        if buffer[i + 1][0] == VAR:
                            k2 = (self.variables[buffer[i + 1][1]])
                            _type2 = k2.type[-1]
                        elif buffer[i + 1][0] == VAL:
                            k2 = (buffer[i + 1][-1])
                            _type2 = k2[1]
                        else:
                            k2 = buffer[i + 1][1]
                            _type2 = "int"
                        if _type1 == "double" or _type2 == "double":
                            _type = "double"
                        elif _type1 == "float" or _type2 == "float":
                            _type = "float"
                        else:
                            _type = "int"
                        buffer.insert(i + 2, [VAL, _type, buffer[i - 1][2], buffer[i + 1][3],
                                              [buffer[i][1], k1, k2]])
                        for l in range(i - 1, i + 2):
                            self.poped += 1
                            buffer.pop(i - 1)
                        self.poped -= 1
                    else:
                        if i == len(buffer) - 1:
                            return ("Expected another operand", buffer[i + 1][2])
                        else:
                            return ("Expected rvalue, found '{}'".format(buffer[i + 1][1]), buffer[i + 1][2])
                else:
                    i += 1

            i = 0
            while i < len(buffer):
                if buffer[i][1] in ["+", "-"]:
                    if (i < len(buffer) - 1 and buffer[i + 1][0] in [VAR, VAL, NUM]):
                        if buffer[i - 1][0] == VAR:
                            k1 = (self.variables[buffer[i - 1][1]])
                            _type1 = k1.type[-1]
                        elif buffer[i - 1][0] == VAL:
                            k1 = (buffer[i - 1][-1])
                            _type1 = k1[1]
                        else:
                            k1 = buffer[i - 1][1]
                            _type1 = "int"
                        if buffer[i + 1][0] == VAR:
                            k2 = (self.variables[buffer[i + 1][1]])
                            _type2 = k2.type[-1]
                        elif buffer[i + 1][0] == VAL:
                            k2 = (buffer[i + 1][-1])
                            _type2 = k2[1]
                        else:
                            k2 = buffer[i + 1][1]
                            _type2 = "int"
                        if _type1 == "double" or _type2 == "double":
                            _type = "double"
                        elif _type1 == "float" or _type2 == "float":
                            _type = "float"
                        else:
                            _type = "int"
                        buffer.insert(i + 2, [VAL, _type, buffer[i - 1][2], buffer[i + 1][3],
                                              [buffer[i][1], k1, k2]])
                        for l in range(i - 1, i + 2):
                            self.poped += 1
                            buffer.pop(i - 1)
                        self.poped -= 1
                    else:
                        if i == len(buffer) - 1:
                            return ("Expected another operand", buffer[i + 1][2])
                        else:
                            return ("Expected rvalue, found '{}'".format(buffer[i + 1][1]), buffer[i + 1][2])
                else:
                    i += 1

            i = len(buffer) - 1
            while i >= 0:
                if buffer[i][1] == "=":
                    if (i > 0 and buffer[i - 1][0] == VAR):
                        if (i < len(buffer) - 1 and buffer[i + 1][0] in [VAR, VAL, NUM]):
                            k1 = (self.variables[buffer[i - 1][1]])
                            k2 = (self.variables[buffer[i + 1][1]]) if buffer[i + 1][0] == VAR else \
                                (buffer[i + 1][-1]) if buffer[i + 1][0] == VAL else \
                                    buffer[i + 1][1]
                            buffer.insert(i + 2, [VAL, k1.type[-1], buffer[i - 1][2], buffer[i + 1][3],
                                                  [buffer[i][1], k1, k2]])
                            for l in range(i - 1, i + 2):
                                self.poped += 1
                                buffer.pop(i - 1)
                            self.poped -= 1
                        else:
                            if i == len(buffer) - 1:
                                return ("Expected another operand", buffer[i + 1][2])
                            else:
                                return ("Expected rvalue, found '{}'".format(buffer[i + 1][1]), buffer[i + 1][2])
                    else:
                        if i == 0:
                            return ("lvalue expected", buffer[0][2])
                        else:
                            return ("Expected lvalue, found '{}'".format(buffer[i - 1][1]), buffer[i - 1][2])
                elif buffer[i][1] in ["+=", "-=", "/=", "*="]:
                    if (i > 0 and buffer[i - 1][0] == VAR):
                        if (i < len(buffer) - 1 and buffer[i + 1][0] in [VAR, VAL, NUM]):
                            k1 = (self.variables[buffer[i - 1][1]])
                            k2 = (self.variables[buffer[i + 1][1]]) if buffer[i + 1][0] == VAR else \
                                (buffer[i + 1][-1]) if buffer[i + 1][0] == VAL else \
                                    buffer[i + 1][1]
                            buffer.insert(i + 2, [VAL, k1.type[-1], buffer[i - 1][2], buffer[i + 1][3],
                                                  ["=", k1, [buffer[i][1][0], k1, k2]]])
                            for l in range(i - 1, i + 2):
                                self.poped += 1
                                buffer.pop(i - 1)
                            self.poped -= 1
                        else:
                            if i == len(buffer) - 1:
                                return ("Expected another operand", buffer[i + 1][2])
                            else:
                                return ("Expected right value, found '{}'".format(buffer[i + 1][1]), buffer[i + 1][2])
                    else:
                        if i == 0:
                            return ("left value expected", buffer[0][2])
                        else:
                            return ("Expected left value, found '{}'".format(buffer[i - 1][1]), buffer[i - 1][2])
                i -= 1

            return (False, buffer[0])
        else:
            return ("Expected 'var' or '(', found '{}' ".format(self.lexems[b][1]), self.lexems[b][2])


class _Var:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.type = kwargs["type"]
        self.func = kwargs["func"]
        self.val = kwargs["val"]


text = "float *b, a[5]; int n; b+=(a)[n]+(2+6);"
analizer = Lab6(string=text)
print("\n{}\n".format(text))
print(analizer.main())
