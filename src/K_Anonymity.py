from time import sleep

from model import *
import os
data=[]
g=open(attribute.txt, 'r')
attributes = eval(g.readline())
g.close()

g=open(kwargs.txt, 'r')
QID, DPID = eval(g.readline())
g.close()
#QID = (0,1) #input by the user
Anonymity_data=[]
Trees = GetTrees()   
Th = 0.4   


def Init():
   
    path = os.path.abspath('..')  
    data_path = 'data.txt'
    data_file = open(data_path, 'r')
    lines = data_file.readlines()
    for line in lines:
        i = line[:-1].split(',')
        data.append(i)



def Anonymity():
    Init()
    PayOffs=1
    Loss = 0
    length=len(data)
    for i in range(length):
        for num in QID:
            Loss = GetLoss(Trees[num],data[i][num])
            PayOff= GetPayOff(Trees[num],data[i][num])
            while Loss<Th:
                tmp_attribute=climb(Trees[num],data[i][num])
                PayOff = GetPayOff(Trees[num],tmp_attribute)    
                data[i][num]=tmp_attribute  
                Loss=GetLoss(Trees[num],data[i][num])   
            PayOffs=PayOff*PayOffs 
         #   data[i].append(PayOffs)
            PayOffs=1
    tmp_data=data[:]
    while tmp_data:
        EQ=tmp_data[0]
        EQ.append(1) 
        tmp_data.remove(tmp_data[0])
        Anonymity_data.append(EQ)
        for i in range(len(tmp_data)):
            each=tmp_data[i]
            if Equal(EQ[:-1], each, QID):
                Anonymity_data.append(each)
                EQ[-1] = EQ[-1] + 1 
        tmp_data=Remove(tmp_data,EQ[:-1],QID)

    return Anonymity_data

if __name__ == '__main__':
    
    Anonymity_data=Anonymity()
    Save2File(Anonymity_data)





