import operator
def Read_Func_Annotate(function,file):
    #end of the function ==> specified by "Percent"!!
    newDict = {}
    next_line = file.next()
    while not next_line.__contains__("Percent"): #not reaching end of function
        #line should starts with "0.", otherwise it's a comment or C code!.
        # we need assembly code
        split_line = next_line.split()
        if split_line[0]==':' or split_line[0]=='0.00':
            next_line = file.next()
            continue
        op = split_line[3]
        percentage = float (split_line[0])
        if op in newDict.keys(): # first call of op in function!
            newDict[op] = newDict[op] + percentage
        else:
            newDict[op] = percentage
        next_line = file.next()
    return newDict

def Read_Results_Annotate (Raw_Data):
    newDict = {}
    RetDict = {}
    Final_Dict = {}
    new_paramter = ""
    sorted_x = {}
    i = 0

    #read desired functions
    functions = []
    func_read_file = open("functions.txt", 'r')
    for line in func_read_file:
        line = line.replace("\n", "")
        functions.append(line)
    Funcions_Dict = {}#contain each function's
    with open(Raw_Data, 'r') as f:
       for line in f:
           #there is a new function!!!
           if line.__contains__(">:"):
               function = (f.next().split()[1])[0:-3] # ==> eliminate "():" and extract func's name

               #if function is not in the list of desired functions, skip it!
               if not function in functions:
                   continue
               nextline = f.next()
               while not nextline.__contains__("{"): # wait to reach start of the function
                   nextline = f.next()
                   continue
               else: #extract each function's details.
                   stats = Read_Func_Annotate(function,f)
                   stats = sorted(stats.items(), key=operator.itemgetter(1), reverse=True)
                   Funcions_Dict[function] = stats

    print Funcions_Dict
Read_Results_Annotate("hamid.txt")
