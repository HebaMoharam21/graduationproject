class Terminal:

        def __init__(self, value):
            self.value = value
        def __str__(self):
            return self.value

class NonTerminal:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class LHS:
    def __init__(self, value):
        self.value = value

class RHS :
    def __init__(self):
        self.rhslist = []
        
    def add(self, obj):
        self.rhslist.append(obj)


class ProductionRule:
    def __init__(self,lhs,rhs):
        self.lhs = lhs
        self.rhs = rhs

    def get_rhs(self, lhs):
        return self.rules.get(lhs, None)
    
    def get_all_rules(self):
        return self.rules
    
    def print_rule(self):
        print(self.lhs.value, '--> ', end=' ')
        print(*self.rhs.rhslist)
        
        

class Grammar:
    def __init__(self, startsymbol):
        self.prules = []
        self.startsymbol = startsymbol
        self.NonTerminalsDict = {}
        self.TerminalsDict = {}
        self.NonTerminals_num = -1
        self.Terminals_num = -1

    def addRule(self, obj):
        self.prules.append(obj)

    def print_rules(self):
        for i in self.prules:
            i.print_rule()

    def addNonterminal(self, n):
        self.NonTerminals_num += 1
        self.NonTerminalsDict[n] = self.NonTerminals_num

    def addTerminal(self, t):
        self.Terminals_num += 1
        self.TerminalsDict[t] = self.Terminals_num

    def get_NonterminalList(self):
        return list(self.NonTerminalsDict.keys())

    def get_TerminalList(self):
        return list(self.TerminalsDict.keys())

    def get_rules_with_lhs(self, l):
        lhs_rules = []
        for rule in self.prules:
            if rule.lhs.value == l.value:
                lhs_rules.append(rule)
        return lhs_rules

    def get_rules_contain(self, l):
        rules = []
        for i in self.prules:
            R = [K.value for K in i.rhs.rhslist]
            if l.value in R:
                rules.append(i)
        return rules
    
class Terminal:
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return self.value

class NonTerminal:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class LHS:
    def __init__(self, value):
        self.value = value

class RHS :
    def __init__(self):
        self.rhslist = []
        
    def add(self, obj):
        self.rhslist.append(obj)

class ProductionRule:
        def __init__(self,lhs,rhs):
            self.lhs = lhs
            self.rhs = rhs

        def get_rhs(self, lhs):
            return self.rules.get(lhs, None)
        
        def get_all_rules(self):
            return self.rules
        
        def print_rule(self):
            print(self.lhs.value, '--> ', end=' ')
            print(*self.rhs.rhslist)
            
class Grammar:
    def __init__(self, startsymbol):
        self.prules = []
        self.startsymbol = startsymbol
        self.NonTerminalsDict = {}
        self.TerminalsDict = {}
        self.NonTerminals_num = -1
        self.Terminals_num = -1

    def addRule(self, obj):
        self.prules.append(obj)

    def print_rules(self):
        for i in self.prules:
            i.print_rule()

    def addNonterminal(self, n):
        self.NonTerminals_num += 1
        self.NonTerminalsDict[n] = self.NonTerminals_num

    def addTerminal(self, t):
        self.Terminals_num += 1
        self.TerminalsDict[t] = self.Terminals_num

    def get_NonterminalList(self):
        return list(self.NonTerminalsDict.keys())

    def get_TerminalList(self):
        return list(self.TerminalsDict.keys())

    def get_rules_with_lhs(self, l):
        lhs_rules = []
        for rule in self.prules:
            if rule.lhs.value == l.value:
                lhs_rules.append(rule)
        return lhs_rules

    def get_rules_contain(self, l):
        rules = []
        for i in self.prules:
            R = [K.value for K in i.rhs.rhslist]
            if l.value in R:
                rules.append(i)
        return rules
    
class Token:
        PLUS = "plus"
        MULT= "mult"
        MINUS= "minus"
        DIV= "div"
        INTEGER= "integer"
        ENDSOURCE= "$"
        ERROR= "error"
        a="a"
        b="b"
        c="c"
        d="d"
        e="e"
        f="f"
        g="g"
        h="h"
        i="i"
        j="j"
        k="k"
        l="l"
        m="m"
        n="n"
        o="o"
        p="p"
        q="q"
        r="r"
        s="s"
        t="t"
        u="u"
        v="v"
        w="w"
        x="x"
        y="y"
        z="z"
        ep="?"
    
class Parser:
    def __init__(self,g ,text):
        self.g=g
        self.text=text
        self.table=[]
        
    def getFirst(self,x,Gram):
        first=[]
        if type(x) == Terminal:
            first.append(x)
            return first
        
        rules=Gram.get_rules_with_lhs(x)
        for i in rules:
            j = i.getrhs_prule()[0]
            first1=self.getFirst(j)
            first1_is_epslon=False
            for k in first1 :
                if k!='?':
                    first.append(k)
                else:
                    first1_is_epslon=True

            if first1_is_epslon == False :
                break
            else:
                first.append('?')
                    
        first= list(set(first))
        return first
    
    def displayFirst(self,x):
            F = self.getFirst(x)
            print("first ( " , end="")
            print(x.value, end="")
            print(" ) = { ", end="")
            for f in F:
                if type(f) == Terminal:
                    print(f.value, end="")
                else:
                    print(f, end="")
            print(" }")
    
    def getFollow(self,x,Gram):
            if type(x)== Terminal:
                print("the input has to be a nonTerminal ")
                exit(1)
            follow=[]
            if x == Gram.startsymbol:
                follow.append("EOF")
                return follow
            
            rules = Gram.get_rules_contain(x)
            for i in rules :
                j=0
                while j<len(i.getrhs_prule()) and i.getrhs_prule()[j] != x:
                    j += 1
                y=i.getrhs_prule()[j+1]
                first=self.getFirst(y)
                first_has_epslon= False
                for m in first:
                    if m != "?":
                        follow.append(m)
                    else:
                        first_has_epslon = True
                            
                if first_has_epslon == False:
                    break
                        
                else:
                    z=i.getlhs_prule()
                    if z!=x:
                        follow1= self.getFollow(z)
                        follow.extend(follow1)
                        
            follow=list(set(follow))
            return follow
    
    def displayFollow(self,x):
        follow=self.getFollow(x)
        print("follow (" , end="")
        print(x.value, end="")
        print(") = { ", end="")
        for f in follow:
            if type(f) == Terminal:
                print(f.value, end="")
            else:
                print(f, end="")
        print(" }")
    

    def parseTable(self,Gram):
        for _ in range(Gram.NonTerminals_num+1): 
            row=[''] * (Gram.Terminals_num+1) 
            self.table.append(row)
        for nonterm, vi in Gram.NonTerminalsDict.items():
                for term, vj in Gram.TerminalsDict.items():        
                    rules = Gram.get_rules_with_lhs(nonterm)
                for rule in rules:
                    if term in self.getFirst(nonterm):
                        self.table[vi][vj]=rule
                    elif "?" in self.getFirst(nonterm):
                        if term in self.getFollow(nonterm):
                                self.table[vi][vj]= rule
                
        return self.table

    def getToken(self):
            
            if not self.text:
                return Token.ENDSOURCE
                
            tokens = []
        
            while self.text:
                ch = self.text[0]
                if ch.isspace():
                    self.text = self.text[1:]
                elif ch=="a":
                    self.text = self.text[1:]
                    tokens.append(Token.a)
                elif ch=="b":
                    self.text = self.text[1:]
                    tokens.append(Token.b)
                elif ch=="c":
                    self.text = self.text[1:]
                    tokens.append(Token.c)
                elif ch=="d":
                    self.text = self.text[1:]
                    tokens.append(Token.d)
                elif ch=="e":
                    self.text = self.text[1:]
                    tokens.append(Token.e)
                elif ch=="f":
                    self.text = self.text[1:]
                    tokens.append(Token.f)
                elif ch=="g":
                    self.text = self.text[1:]
                    tokens.append(Token.g)
                elif ch=="h":
                    self.text = self.text[1:]
                    tokens.append(Token.h)
                elif ch=="i":
                    self.text = self.text[1:]
                    tokens.append(Token.i)
                elif ch=="j":
                    self.text = self.text[1:]
                    tokens.append(Token.j)
                elif ch=="k":
                    self.text = self.text[1:]
                    tokens.append(Token.k)
                elif ch=="l":
                    self.text = self.text[1:]
                    tokens.append(Token.l)
                elif ch=="m":
                    self.text = self.text[1:]
                    tokens.append(Token.m)
                elif ch=="n":
                    self.text = self.text[1:]
                    tokens.append(Token.n)
                elif ch=="o":
                    self.text = self.text[1:]
                    tokens.append(Token.o)
                elif ch=="p":
                    self.text = self.text[1:]
                    tokens.append(Token.p)
                elif ch=="q":
                    self.text = self.text[1:]
                    tokens.append(Token.q)
                elif ch=="r":
                    self.text = self.text[1:]
                    tokens.append(Token.r)
                elif ch=="s":
                    self.text = self.text[1:]
                    tokens.append(Token.s)
                elif ch=="t":
                    self.text = self.text[1:]
                    tokens.append(Token.t)
                elif ch=="u":
                    self.text = self.text[1:]
                    tokens.append(Token.u)
                elif ch=="v":
                    self.text = self.text[1:]
                    tokens.append(Token.v)
                elif ch=="w":
                    self.text = self.text[1:]
                    tokens.append(Token.w)
                elif ch=="x":
                    self.text = self.text[1:]
                    tokens.append(Token.x)
                elif ch=="y":
                    self.text = self.text[1:]
                    tokens.append(Token.y)
                elif ch=="z":
                    self.text = self.text[1:]
                    tokens.append(Token.z)
    
            
                elif ch.isdigit():
                    s=ch
                    while self.text and self.text[0].isdigit():
                        s+=self.text[0]
                        self.text=self.text[1:]
                    tokens.append(Token.INTEGER)
    
                elif ch =="+":
                    self.text = self.text[1:]
                    tokens.append(Token.PLUS)
                elif ch=="-":
                    self.text = self.text[1:]
                    tokens.append(Token.MINUS)
                elif ch=="*":
                    self.text = self.text[1:]
                    tokens.append(Token.MULT)
                elif ch=="/":
                    self.text = self.text[1:]
                    tokens.append(Token.DIV)
                elif ch=="?":
                    self.text = self.text[1:]
                    tokens.append(Token.ep)
                elif ch =="$":
                    self.text = self.text[1:]
                    tokens.append(Token.ENDSOURCE) 
                elif not self.text:
                    self.text = self.text[1:]
                    tokens.append(Token.ENDSOURCE)
    
                else:
                    self.text = self.text[1:]
                    tokens.append(Token.ERROR)
    
            return tokens
    
    def match(self, t, tokens):
            if tokens[0]== t:
                print("accept")
                tokens.pop(0)
            else:
                 print("not")

    def LL1Parse(self,Gram):
            stack=[]
    #         stack.append("$")
            stack.append(Gram.startsymbol)
    #         print(stack)
            tokens = self.getToken()
            while stack and tokens:
    #             for CT in tokens:
                    x=stack[-1]
                    CT= tokens[0]
                    if x in Gram.TerminalsDict.keys():
                        print('x value: ',x.value)
                        print('CT: ',CT)
                        self.match(x.value,tokens)
                        stack.pop()
                        
                    else:
                            if x in Gram.NonTerminalsDict.keys():
                                print('x : ',x.value)
                                print('CT: ',CT)
                                for k, v in Gram.TerminalsDict.items():
                                    if(k.value == CT):
                                        rule=self.table[Gram.NonTerminalsDict[x]][v]
                                        break
    
                                if rule == "":
                                    print("syntax error")
                                    return "NOT ACCEPTED"
                                else:
                                    stack.pop()
                                    for j in reversed(rule.getrhs_prule()):
                                        stack.append(j)
                            else:
                                return "NOT ACCEPTED"
            print(stack)
            print(tokens)
            if stack or tokens:
                return "NOT ACCEPTED"
            else:
                return "ACCEPTED"

