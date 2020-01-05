import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time



def mapFeature(x1,x2,degree): # All possible Polynomial terms upto degree 'degree'
    #Just handling 2 variables
    out = np.ones(len(x1)).reshape(len(x1),1)
    for i in range(1,degree+1):
        for j in range(i+1):
            terms= (x1**(i-j) * x2**j).reshape(len(x1),1)
            out= np.hstack((out,terms))
    return out



def sigmoid(z):
    return 1/ (1 + np.exp(-z))

def costFunctionReg(theta, X, y ,Lambda):

    #Regularization and COmputes Gradient
    
    m=len(y)
    y=y[:,np.newaxis]
    predictions = sigmoid(X @ theta) # @ - matrix multiplication 
    error = (-y * np.log(predictions)) - ((1-y)*np.log(1-predictions))
    cost = 1/m * sum(error)
    regCost= cost + Lambda/(2*m) * sum(theta**2)
    
    # compute gradient ( Gradient Descent )
    j_0= 1/m * (X.transpose() @ (predictions - y))[0]
    j_1 = 1/m * (X.transpose() @ (predictions - y))[1:] + (Lambda/m)* theta[1:]
    grad= np.vstack((j_0[:,np.newaxis],j_1)) # returns j_0 and j_1
    
    return regCost[0], grad



# Genereating Noise
def noisevector( scale, Length ):

    r1 = np.random.uniform(0, 1, Length)#standard normal distribution
    n1 = np.linalg.norm( r1, 1 )#get the norm of this random vector
    r2 = r1 / n1#the norm of r2 is 1
    normn = np.random.gamma( Length, scale, 1 )#Generate the norm of noise according to gamma distribution
    res = r2 * normn#get the result noise vector
    return res


def gradientDescent(X,y,theta,alpha,num_iters,Lambda):

    # Generate theta (weights)
    
    m=len(y)
    J_history =[]
    
    for i in range(num_iters):
        cost, grad = costFunctionReg(theta,X,y,Lambda)
        theta = theta - (alpha * grad) 
        J_history.append(cost)
    
    return theta , J_history



def mapFeaturePlot(x1,x2,degree):

    # Returns all polynomials upto given degree
    out = np.ones(1)
    for i in range(1,degree+1):
        for j in range(i+1):
            terms= (x1**(i-j) * x2**j)
            out= np.hstack((out,terms))
    return out

def generate_and_save_graph(filepath, degree=6, epsilon=0.1, Lambda=1, alpha=1, epochs=800, split_ratio=1):
    print('making graph')
    df=pd.read_csv(filepath, header=None, sep = '[;,]', engine='python')
    df.head()

    X=df.iloc[:,:-1].values #features
    y=df.iloc[:,-1].values #labels

    pos , neg = (y==1).reshape(-1,1) , (y==0).reshape(-1,1)

    X = mapFeature(X[:,0], X[:,1],degree)

    initial_theta = np.zeros((X.shape[1], 1))

    theta , J_history = gradientDescent(X,y,initial_theta,alpha,epochs,Lambda)

    scale = 2/( len(X) * Lambda * epsilon) 
    noise = noisevector( scale,len(theta) )
    theta_dp = []
    for i in range(len(theta)):
     theta_dp.append(theta[i]+noise[i])
    
    plt.scatter(X[pos[:,0],1],X[pos[:,0],2],c="r",marker="+",label="+1")
    plt.scatter(X[neg[:,0],1],X[neg[:,0],2],c="b",marker="x",label="0")

    u_vals = np.linspace(-1,1.5,50)
    v_vals= np.linspace(-1,1.5,50)
    z=np.zeros((len(u_vals),len(v_vals)))
    z_dp=np.zeros((len(u_vals),len(v_vals)))
    for i in range(len(u_vals)):
        for j in range(len(v_vals)):
            z[i,j] =mapFeaturePlot(u_vals[i],v_vals[j],degree) @ theta
            z_dp[i,j] =mapFeaturePlot(u_vals[i],v_vals[j],degree) @ theta_dp
    plt.contour(u_vals,v_vals,z.T,0,colors='green')
    plt.contour(u_vals,v_vals,z_dp.T,0,colors='black')
    plt.xlabel("")
    plt.ylabel("")
    plt.legend(loc=0)
    name='static/images/Laplace'+str(time.time())+'.png'
    plt.savefig(name)
    plt.close()
    #print(np.array(theta_dp).tolist())
    return (name, np.array(theta_dp).reshape((-1,)).tolist())

def format_correct(filepath):
    PUMSdata=pd.read_csv(filepath, sep = '[;,]', engine='python')

    #Any Empty Values
    if np.any(pd.isnull(df)):
        return "File Contains Empty or Null Values"

    # X=df.iloc[:,:-1].values #features
    return True
    
