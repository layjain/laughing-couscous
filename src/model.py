import tree as a
import os

def Save2File(data):

    path = os.path.abspath('..') 
    data_path = 'Anonymity.txt'
    data_file = open(data_path, 'w')
    str1=''
    for each in data:
        str1=str1 + '{}\n'.format(each)
    data_file.write(str1)
    data_file.close()



def GetTrees():

    attribute = [] 
    infile = open("attribute.txt")   
    attribute_file = infile.readline()[:-1] 
    attribute = (attribute_file.split(','))
    print(attribute)
    trees = []
    for i in range(len(attribute)):
        path2 =  "attribute_" +attribute[i]+".txt"
        tree = a.Tree1()
        tree1 = tree.createTree(path2)
        trees.append(tree1)
    return trees



def GetPayOff(tree,attribute):

    node = tree.get_node(attribute)
    level_all = tree.depth() + 1  
    level_site = tree.depth() + 1 - tree.depth(node)   
    return float(level_site/level_all)   


def Equal(a,b,QID):

    for i in QID:
        if a[i]!=b[i]:
            return False
    if a[-1] ==b[-1] and a[-2]==b[-2]:
        return True
    else:
        return False


def climb(tree,attribute):

    node = tree.get_node(attribute)
    return (tree.parent(attribute).tag)   


def GetLoss(tree,attribute):

    if(IntTree(tree)==True):
        return GetNumLoss(tree,attribute)

    else:
        return GetCharLoss(tree,attribute)


def IntTree(tree):

    node = tree.nodes.keys()
    keys=[]
    for each in node:
        keys.append(each)
    if '-' in keys[0]:
        return True
    else:
        return False


def GetCharLoss(tree,str):

    Child_len = len(tree.children(str))  
    Child_all = Child_len
    if Child_len == 0:  
        return 0

    node = tree.get_node(str)
    level_site = tree.depth(node)  
    if (level_site == 0):  
        return 1

    parent = tree.parent(str).tag  
    childrens = tree.children(parent)  
    for i in range(len(childrens)): 
        if childrens[i].tag != str:
            parent1 = childrens[i].tag
            Child_all = Child_all + len(tree.children(parent1))  
    return (Child_len / Child_all)   



def GetNumLoss(tree,age):

    Numrange = []
    depth = tree.depth()   
    node = tree.get_node(age)   
    level_site = tree.depth(node)  
    if (level_site == 0): 
        return 1

    if (level_site == depth):   
        return 0

    child = age.split('-')
    Range = int(child[1]) - int(child[0])   
    parent = tree.parent(age).tag   
    Numrange = parent.split('-')
    Range1 = int(Numrange[1]) - int(Numrange[0])     
    return(Range/Range1)    

def Remove(data,EQ,QID ):
    remove_set=[]
    for i in range(len(data)):
        each = data[i]
        if Equal(EQ,each,QID):
            remove_set.append(i)
   # remove_set.sort(reverse=True)
    for j in remove_set:
        data.remove(data[j])
    return data
