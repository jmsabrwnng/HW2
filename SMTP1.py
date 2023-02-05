# parse.py
# James Browning
# I certify that no unauthorized assistance has been received or given in the completion of this work.


import fileinput

result = "250 OK" #variable to contain the response to our email
num = 0              #marker for the letter we are parsing
ele = 1              #marker for which part of the grammar we are on
dele = 0             #marker for whether we are on the first element of domain
eele = 1             #marker for whether we are on the first character of element
texttype = ""
data = 0
path = ""
reversepath = ""
forwardpathgrp = []
forwarddata = ""

def checktext(num):
    global ele
    global texttype
    if(ele==1) and (inp[num]=="M"):
        texttype = "From"
    if(ele==1) and (inp[num]=="R"):
        if(texttype == "From") or (texttype == "Rcpt":
            texttype = "Rcpt"
        else:
            texttype = ""
            result = "503 Bad sequence of commands"
    if(ele==1) and (inp[num]=="D"):
        if(texttype == "Rcpt"):
            texttype = "Data"
        else:
            texttype = ""
            result = "503 Bad sequence of commands"
    if(ele==1) and (texttype == ""):
        result = "500 Syntax error: command unrecognized"
    return text(texttype)

def text(text):
    global texttype
    global ele
    global result
    if(result != "250 OK") or (result != "354 Start mail input; end with <CRLF>.<CRLF>"):
        ele == 20
        return 0
    if(text=="From"):
        return mailfromcmd(num)
    if(text=="Rcpt"):
        return mailrcptcmd(num)
    if(text=="Data"):
        return data(num)
    if(data==1):
        return getdata(num)

#our main parsing function
def mailfromcmd(num):
    global result
    global ele
#the first 10 elements check if we have the basic MAIL FROM: grammar including variable spaces
    if (inp[num]=="M") and (ele==1):
        return num+1
    if (inp[num]=="A") and (ele==2):
        return num+1
    if (inp[num]=="I") and (ele==3):
        return num+1
    if (inp[num]=="L") and (ele==4):
        return num+1
    if (SP(inp[num])) and (ele==5):
        return whitespace(num)
    if (inp[num]=="F") and (ele==6):
        return num+1
    if (inp[num]=="R") and (ele==7):
        return num+1
    if (inp[num]=="O") and (ele==8):
        return num+1
    if (inp[num]=="M") and (ele==9):
        return num+1
    if (inp[num]==":") and (ele==10):
        return num+1
#if anything has gone wrong then immediately throw an error
    if (ele<=10):
        result = "500 Syntax error: command unrecognized" 
        ele = 20
        return 0
#here we check for the nullspace with variable whitespace before and after the reversepath
    if (ele==11) or (ele==17):
        return nullspace(num)
#here we go check the reversepath
    if (ele>=12) and (ele<17):
        return reversepath(num)
#after everything else if the final character is not a crlf then we throw an error
    if ("\n" in inp) and (ele==18):
        return num
    elif (ele==18) and (result==""):
        result = "501 Syntax error in parameters or arguments"
        return 1

def mailrcptcmd(num):
    global result
    global ele
#the first 10 elements check if we have the basic MAIL FROM: grammar including variable spaces
    if (inp[num]=="R") and (ele==1):
        return num+1
    if (inp[num]=="C") and (ele==2):
        return num+1
    if (inp[num]=="P") and (ele==3):
        return num+1
    if (inp[num]=="T") and (ele==4):
        return num+1
    if (SP(inp[num])) and (ele==5):
        return whitespace(num)
    if (inp[num]=="T") and (ele==6):
        return num+1
    if (inp[num]=="O") and (ele==7):
        return num+1
    if (inp[num]==":") and (ele>==8) and (ele<=10):
        ele+=2
        return num+1
#if anything has gone wrong then immediately throw an error
    if (ele<=10):
        result = "500 Syntax error: command unrecognized"
        ele = 20
        return 0
#here we check for the nullspace with variable whitespace before and after the reversepath
    if (ele==11) or (ele==17):
        return nullspace(num)
#here we go check the reversepath
    if (ele>=12) and (ele<17):
        return forwardpath(num)
#after everything else if the final character is not a crlf then we throw an error
    if ("\n" in inp) and (ele==18):
        return num
    elif (ele==18) and (result==""):
        result = "501 Syntax error in parameters or arguments"
        return 1

def data(num):
    global result
    global ele
    global data
    if(ele==1) and (inp[num]=="D"):
        return num+1
    if(ele==2) and (inp[num]=="A"):
        return num+1
    if(ele==3) and (inp[num]=="T"):
        return num+1
    if(ele==4) and (inp[num]=="A"):
        return num+1
    if(ele==5):
        return nullspace(num)
    if(ele==6) and ("\n" in inp):
        data=1
        return num
    if(ele<=6):
        result="500 Syntax error: command unrecognized"
        ele= 20
        return 0
    else:
        result = "354 Start mail input; end with <CRLF>.<CRLF>"
        data = 1
        return getdata(num)

def getdata(num):
    global data
    global ele
    global forwarddata
    if(data==1) and ("\n" in inp) and (inp[num]==".") and (len(inp)==2):
        forwarddata = forwarddate + inp
        data=0
        ele=20
        return 0
    if(data==1):
        forwarddata = forwarddata + inp
        ele=20
        return 0

#our basic function for checking out our variable white space
def whitespace(num):
    if (SP(inp[num])):
        return whitespace(num + 1)
    return num

#a function designed to test whether a character is a space or tab
def SP(char):
    if (char==" ") or (char=="    "):
        return True
    return False

#a function that tests whether the nullspace is empty or has a variable whitespace
def nullspace(num):
    if (SP(inp[num])):
        return whitespace(num+1)
    return num

#this function breaks the path down to its various parts
def reversepath(num):
    global result
    global ele
    global reversepath
    global path
    char = inp[num]
#if the first character isn't a < then just throw an error and end the parse
    if (char=="<") and (ele==12):
        return num+1
    elif (char!="<") and (ele==12):
        result = "501 Syntax error in parameters or arguments"
        ele == 20
        return 0
#get into the meat of the mailbox
    if (ele >= 13) or (ele < 16):
        return mailbox(num)
#if the character following a valid mailbox isn't > then throw an error and end the parse
    if (char==">") and (ele == 16):
        reversepath = path
        path = ""
        return num+1
    elif (char!=">") and (ele == 16):
        result = "501 Syntax error in parameters or arguments"
        ele == 20
        return 0

def forwardpath(num):
    global result
    global ele
    global forwarpathgrp
    global path
    char = inp[num]
#if the first character isn't a < then just throw an error and end the parse
    if (char=="<") and (ele==12):
        return num+1
    elif (char!="<") and (ele==12):
        result = "501 Syntax error in parameters or arguments"
        ele == 20
        return 0
#get into the meat of the mailbox
    if (ele >= 13) or (ele < 16):
        return mailbox(num)
#if the character following a valid mailbox isn't > then throw an error and end the parse
    if (char==">") and (ele == 16):
        forwardpathgrp.append(path)
        path = ""
        return num+1
    elif (char!=">") and (ele == 16) and (result==""):
        result = "501 Syntax error in parameters or arguments"
        ele == 20
        return 0

#this function breaks up the mailbox into its parts
def mailbox(num):
    global result
    global ele
    global path
#check theat the localpart is valid
    if (ele==13):
        return localpart(num)
#make sure there is an @ sumbol otherwise throw an error
    if (inp[num]=="@") and (ele==14):
        path = path + "@"
        return num+1
    elif (ele==14):
        result = "ERROR -- @"
        ele == 20
        return 0
#check that the domain is valid
    if (ele==15):
        return domain(num)
    if (ele>15):
        return num

#a function that checks that checks that localpart is a string
def localpart(num):
    global result
    global ele
    global path
    if(char(num)):
        path = path + inp[num]
        return string(num+1)
    else:
        result = "ERROR -- local-part"
        ele = 20
        return 0

#function that walks through the entire string
def string(num):
    if(char(num)):
        return string(num+1)
    else:
        return num

#a function that checks the validity of the domain
def domain(num):
    global result
    global ele
    global dele
    global path
#as long as the firest character is not a . then check if it is an element
    if(inp[num]!=".") and (dele==0):
        dele=1
        return element(num)
#as long as the next character is not a . then check if it is an element
    elif(inp[num]!=".") and (dele>=1):
        return element(num)
#if it is not the first character and it is a . then check if a valid element follows it
    elif(inp[num]==".") and (dele>=1):
        path = path + inp[num]
        return element(num+1)
#otherwise if the first character is a . then throw an error
    elif(dele==0):
        result = "ERROR -- domain"
        ele = 20
        return 0
#otherwise just exit the function
    else:
        return num

def element(num):
    global eele
    global dele
    global path
    char=inp[num]
#check that the first character is a letter
    if(eele==1) and (letter(char)):
        eele += 1
        path = path + char
        return element(num+1)
#check that the next characters are letters or digits
    elif(eele>1) and (letdigstr(char)):
        path = path + char
        return element(num+1)
#if we find a period then reset eele and return to domain
    elif(char=="."):
        path = path + char
        eele=1
        return domain(num)
#else just exit the whole thing
    else:
        return num

#function to check if a character is a valid letter or digit
def letdigstr(char):
    if(letter(char)) or (digit(char)):
        return True
    else:
        return False

#check if a character is a valid letter
def letter(char):
    if(char=="a")or(char=="A")or(char=="b")or(char=="B")or(char=="c")or(char=="C")or(char=="d")or(char=="D")or(char=="e")or(char=="E")or(char=="f")or(char=="F")or(char=="g")or(char=="G")or(char=="h")or(char=="H")or(char=="i")or(char=="I")or(char=="j")or(char=="J")or(char=="k")or(char=="K")or(char=="l")or(char=="L")or(char=="m")or(char=="M")or(char=="n")or(char=="N")or(char=="o")or(char=="O")or(char=="p")or(char=="P")or(char=="q")or(char=="Q")or(char=="r")or(char=="R")or(char=="s")or(char=="S")or(char=="t")or(char=="T")or(char=="u")or(char=="U")or(char=="v")or(char=="V")or(char=="w")or(char=="W")or(char=="x")or(char=="X")or(char=="y")or(char=="Y")or(char=="z")or(char=="Z"):
        return True
    else:
        return False

#check if a character is a valid digit
def digit(char):
    if(char=="1")or(char=="2")or(char=="3")or(char=="4")or(char=="5")or(char=="6")or(char=="7")or(char=="8")or(char=="9")or(char=="0"):
        return True
    else:
        return False

#check if a character is not a space or special character
def char(num):
    if(SP(inp[num])==False) and (special(inp[num])==False):
        return True
    else:
        return False

#check for special characters
def special(char):
    if(char=="<")or(char==">")or(char=="(")or(char==")")or(char=="[")or(char=="]")or(char=="\\")or(char==".")or(char==",")or(char==";")or(char==":")or(char=="@")or(char=="\""):
        return True
    else:
        return False

#our main loop to check emails from the standard input
for inp in fileinput.input():
    if "end-of-file" == inp.rstrip():
        break
    while ele <= 18:
        num = mailfromcmd(num)
        ele += 1
    print(inp)
    print(result)
    if(result != "250 OK") or (result != "354 Start mail input; end with <CRLF>.<CRLF>"):
        break
    for path in forwardpathgrp:
        filepath = 'forward/' + path + '.txt.'
        f = open(filepath, 'a')
        f.append("From: <" + reversepath + ">\n")
        for path in forwardpathgrp:
            f.append("To: <" + path + ">\n")
        f.append(forwarddata)
        f.close()
    result = "250 OK"
    num = 0 
    ele = 1 
    dele = 0
    eele = 1
    texttype = ""
    data = 0
    path = ""
    reversepath = ""
    forwardpathgrp = []
    forwarddata = ""



