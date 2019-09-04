import pandas
import numpy as np
import matplotlib.pyplot as plt

def _clip(x, lower, upper):
    if lower>upper:
        raise ValueError('Cannot clip with lower more than upper')
    clipped=x
    if clipped<lower:
        return lower
    if clipped>upper:
        return upper
    return clipped
clip=np.vectorize(_clip)

def lap(mean, scale, size):
    #size=number of random nos needed
    rand=np.random.rand(size)-0.5
    randGen=mean-scale*np.sign(rand)*np.log(1-2*np.abs(rand))
    ###NOTE: contrary to given, np.sign returns 0 for 0, want to change?
    return randGen
    
def meanDP(x, lower, upper, epsilon):
    if upper<lower:
        raise ValueError
    n=len(x)
    sensitivity=(upper-lower)/n
    scale=sensitivity/epsilon
    x_clipped=clip(x, lower, upper)
    sensitiveValue=np.mean(x_clipped)
    DPrelease=sensitiveValue+lap(0, scale, 1)
    return {'release':DPrelease, 'true':sensitiveValue}

#Mean Release    
def generate_and_save_histogram (filepath="https://raw.githubusercontent.com/privacytoolsproject/cs208/master/data/FultonPUMS5full.csv",
                                 label='age',
                                 epsilon=1):
    #filepath="https://raw.githubusercontent.com/privacytoolsproject/cs208/master/data/FultonPUMS5full.csv"
    PUMSdata=pandas.read_csv(filepath)
    data=np.array(PUMSdata['age'])
    count=0
    release=[None for _ in range(2000)]
    true=[None for _ in range(2000)]
    for k in range(2000):
        DPmean=meanDP(x=data, lower=1, upper=125, epsilon=epsilon)
        release[k]=float(DPmean['release'])
        true[k]=DPmean['true']
        if release[k]<0:
            count+=1
    plt.hist(release, bins=10)
    plt.title("Histogram of released DP means")
    plt.xlabel(" Differentially Private Mean Age")
    plt.ylabel("frequency")
    plt.show()
    print(true[0])
    print(count)
    #plt.savefig('static/images/Laplace.png')
    
        
