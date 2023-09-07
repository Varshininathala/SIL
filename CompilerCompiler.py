import sys
class Stack():
    def __init__(self):
        self.ar = []

    def push(self, ar):
        self.ar.append(ar)				

    def pop(self):
        return self.ar.pop()
    def getStack(self):
        return self.ar
def equation(e,dict1):
    #print(e)
    new=""
    t=""

    for i in e:
        if i.isalpha():
            if i in dict1:
                new=new+str(dict1[i])
            else:
                t=t+i
                if t in dict1:
                    new=new+str(dict1[t])
                    t=""
                
                
        elif i == " ":
            continue
        else:
            new=new+i
    return new
def precedence(op):
	if op == '+' or op == '-':
		return 1
	if op == '*' or op == '/':
		return 2
def evaluateif(s):
    if "<" in s:
        a1=s.split("<")
        return evaluate(a1[0])<evaluate(a1[1])
    elif ">" in s:
        a1=s.split(">")
        return evaluate(a1[0])>evaluate(a1[1])
    elif "=" in s:
        a1=s.split("=")
        return evaluate(a1[0])==evaluate(a1[1])
    elif "!" in s:
        a1=s.split("!")
        return evaluate(a1[0])!=evaluate(a1[1])
        
    
    
def evaluate(s):
	v = []
	o = []
	i = 0
	while i < len(s):
		
		if s[i].isdigit():
			x = 0
			while (i < len(s) and
				s[i].isdigit()):
			
				x = x * 10 + int(s[i])
				i += 1
			v.append(x)
			i-=1
		else:
			while (len(o) != 0 and
				precedence(o[-1]) >= precedence(s[i])):
				v2 = v.pop()
				v1 = v.pop()
				op = o.pop()
				exp=0
				if op == "*":
				    exp=v1*v2
				elif op == "/":
				    exp = v1/v2
				elif op == "+":
				    exp= v1+v2
				elif op == "-":
				    exp = v1 - v2
				v.append(exp)
			o.append(s[i])		
		i += 1
	while len(o) != 0:
		
		v2 = v.pop()
		v1 = v.pop()
		op = o.pop()
		exp=0
		if op == "*":
		    exp=v1*v2
		elif op == "/":
		    exp=v1//v2
		elif op=="+":
		    exp=v1+v2
		elif op=="-":
		    exp=v1-v2
		    
		v.append(exp)
	return v[len(v)-1]
with open('./input.txt') as f:
    st=Stack()
    ln=Stack()
    dict1={}
    dict2={}
    for line in f:
       sub=' '
       index = line.find(sub)
       k, v = line[:index].strip(),line[index:].strip().upper()
       dict2[int(k)] = v
    
    d=0
    t1={}
    for i in dict2.keys():
        t1[d]=i 
        d+=1
    g=0
    j=0
    ta=[]
    
    while j<len(dict2):
        #if t1[j] not in ln: 
        if dict2[t1[j]][0:5]!="GOSUB" and  dict2[t1[j]][0:3]!="RET":
        
            ln.push(t1[j])
            
        elif dict2[t1[j]][0:5]=="GOSUB":
            
            #gl=temp[t1[j]][6:]
            ta.append(j)
            
            j=list(t1.keys())[list(t1.values()).index(int(dict2[t1[j]][6:].strip()))]
            continue
            
        elif dict2[t1[j]][0:3]=="RET" and len(ta)>0:
            ln.push(t1[j])
            j=ta.pop()
                
        j=j+1   
    i=0
    #print(ln)
    ln1=ln.getStack()
    while i< len(ln1):
        #if(ln[i]<g):
            
            #continue
        #print(ln[i])
        l=dict2[ln1[i]]
        
        if "INTEGER" in l:

            l=l[8:]
            
            v=l.strip()
            
            v_array=v.split(",")
            for j in v_array:
                dict1[j]=0
            
        elif "INPUT" in l:
            
            l=l[6:]
            
            inp=l.strip()
            
            inp_array=inp.split(",")
            input1=input()
            input1_array=input1.split()
            if len(inp_array)!=len(input1_array):
                print("Line n missing input value")
                sys.exit()
            for k in range(len(inp_array)):
                dict1[inp_array[k]]=int(input1_array[k])

            
        elif "LET" in l:
            
            l=l.strip("LET ")
            if "+" in l or "*" in l or "-"  in l or "/" in l:
                
                e=l.split("=")
                
                dict1[e[0].strip()]= evaluate(equation(e[1].strip(),dict1))   
                
                
            else:
                a1=l.split("=")
                dict1[a1[0].strip()]=evaluate(equation(a1[1].strip(),dict1))
        
        elif l[0:2]=="IF":
            
            l=l[3:]
            l=l.strip()
            ifl=l.split(" THEN ")
            
            if(evaluateif(equation(ifl[0],dict1))):
                if "PRINTLN" in ifl[1]:
                    m=ifl[1]

                    m=m.strip()
                    m=m.strip("PRINTLN ")
                    m=m.strip()
                    
                    if m[0]=='"':
                        print(m.strip('"'))
                    else:
                        print(int(evaluate(equation(m,dict1))))
                elif "PRINT" in ifl[1]:
                    m=ifl[1]

                    m=m.strip()
                    m=m.strip("PRINT ")
                    m=m.strip()
                    
                    if m[0]=='"':
                        print(m.strip('"'),end="")
                    else:
                        print(int(evaluate(equation(m,dict1))),end="")
                elif "GOTO" in ifl[1]:
                    m=ifl[1]
                    m=m.strip()
                    m=m.strip("GOTO ")
                    
                    i=ln1.index(int(m))
                    continue
        elif l[0:7]=="PRINTLN":
            
            main=l[8:]
            p1=main.strip()
            p=p1.split(",")
            if(len(p)==1):
                if p[0][0]=='"':
                    print(p[0].strip('"'))
                else:
                    print(int(evaluate(equation(p[0],dict1))))
            else:
                print(p[0].strip().strip('"'),end="")
                print(int(evaluate(equation(p[1],dict1))))
        elif l[0:5]=="PRINT":
            
            main=l.strip("PRINT ")
            p=main.strip()
            if p[0]=='"':
                print(p.strip('"'),end="")
            else:
                print(int(evaluate(equation(p,dict1))),end="")
        elif l[0:4]=="PUSH":
            main=l[5:]
            p=main.strip()
            st.push(int(evaluate(equation(p,dict1))))
        elif l[0:3]=="POP":
            main=l[4:]
            p=main.strip()
            dict1[p]=st.pop()
        elif l[0:4]=="GOTO":
            main=l[5:]
            p=main.strip()
            i=ln1.index(int(p))
            continue
        elif "END" in l:
            sys.exit()
        i+=1
   