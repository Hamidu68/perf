import operator
def Avg_Results(Final_Dict, iteration, Avg,Avg_Events):
    # for iteration number 0, we shoud create the dictionary
    #average of a singla varaiable
    Avg_Stats = {}
    Tmp_Avg_Events = {}
    sorted_x = {}
    for key_j in Final_Dict.keys():
        Dict = Final_Dict[key_j]


        tmp_event = key_j.split()[0]
        key = key_j.split()[0]

        if iteration == 0:#just to initialize!!! when it's the first time!!
            Tmp_Avg_Events[key] = 0
            Avg_Stats = Dict
        else:
            Avg_Stats = Avg[key]
            Tmp_Avg_Events[key] = Avg_Events[key]
        Tmp_Avg_Events[key] = int (float(Tmp_Avg_Events[key]*iteration + int((key_j.split()[1])))/(iteration+1))
        for key_i in range(0,  min (len(Avg_Stats), len(Dict))):
            #print Dict[key_i]
            Variable = (Dict[key_i][0])
            Value = int((Dict[key_i][1])[0])
            # print Dict
           # print type(Avg_Stats)
            # for iteration number 0, we shoud create the dictionary
            if iteration == 0:
                (Avg_Stats[key_i][1])[0] = 0;

            if Variable in Avg_Stats[key_i]:
                (Avg_Stats[key_i][1])[0] = ((float((Avg_Stats[key_i][1])[0]) * iteration + Value) / (iteration + 1))
        # print Avg_Stats
        Avg[key] = Avg_Stats
    return [Avg,Tmp_Avg_Events]
