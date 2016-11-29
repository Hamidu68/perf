import operator
def Avg_Results(Final_Dict, iteration, Avg):
    # for iteration number 0, we shoud create the dictionary
    #average of a singla varaiable
    Avg_Stats = {}
    sorted_x = {}
    for key_j in Final_Dict.keys():
        Dict = Final_Dict[key_j]
       # print key_j.split()[0]
        key = key_j.split()[0]
        if iteration == 0:#just to initialize!!! when it's the first time!!
            Avg_Stats = Dict
        else:
            Avg_Stats = Avg[key]

        for key_i in range(0,  min (20, len(Dict))):
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
    return Avg
       # sorted_x[key] = sorted(Avg_Stats.items(), key=operator.itemgetter(1), reverse=True)
   # print sorted_x
   # return sorted_x
