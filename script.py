import numpy as np
from scipy.optimize import minimize
from scipy.io import loadmat
from math import sqrt
from numpy.linalg import inv
import scipy.io
import matplotlib.pyplot as plt
import pickle
def ldaLearn(X,y):
    # Inputs
    # X - a N x d matrix with each row corresponding to a training example
    # y - a N x 1 column vector indicating the labels for each training example
    #
    # Outputs
    # means - A d x k matrix containing learnt means for each of the k classes
    # covmat - A single d x d learnt covariance matrix 
    
    #trainingData is 150*2
    trainingData=X;
    rows=trainingData.shape[0];
    colums=trainingData.shape[1];
    #trueLabels is 150*1
    trueLables=y.reshape(y.size)
    #classLables will be in the range 1,2,3,4,5
    classLabels=np.unique(trueLables)
    #Means matrix dim will be 2*5
    means=np.zeros((colums,classLabels.size))
    #calculating the mean of the values where the classLabel=trueLabel
    ##mean matrix is 2*5 one row represents x mean,other y mean 
    for i in range(classLabels.size):
        means[:,i]=np.mean(trainingData[trueLables==classLabels[i]],axis=0)
    #covariance matrix is 2*2
    covmat=np.cov(X,rowvar=0)
    return means,covmat

def qdaLearn(X,y):
    # Inputs
    # X - a N x d matrix with each row corresponding to a training example
    # y - a N x 1 column vector indicating the labels for each training example
    #
    # Outputs
    # means - A d x k matrix containing learnt means for each of the k classes
    # covmats - A list of k d x d learnt covariance matrices for each of the k classes
    
    # IMPLEMENT THIS METHOD
     #trainingData is 150*2
    trainingData=X;
    rows=trainingData.shape[0];
    colums=trainingData.shape[1];
    #trueLabels is 150*1
    trueLables=y.reshape(y.size)
    #classLables will be in the range 1,2,3,4,5
    classLabels=np.unique(trueLables)
    #Means matrix dim will be 2*5
    means=np.zeros((colums,classLabels.size))
    #calculating the mean of the values where the classLabel=trueLabel
    covmats=[np.zeros((colums,colums))]*classLabels.size
    ##mean matrix is 2*5 one row represents x mean,other y mean 
    for i in range(classLabels.size):
        means[:,i]=np.mean(trainingData[trueLables==classLabels[i]],axis=0)
        covmats[i]=np.cov(trainingData[trueLables==classLabels[i]],rowvar=0)
  
    
    return means,covmats

def ldaTest(means,covmat,Xtest,ytest):
    # Inputs
    # means, covmat - parameters of the LDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    invcovmat = np.linalg.inv(covmat)
    covmatdet = np.linalg.det(covmat)
    pdf= np.zeros((Xtest.shape[0],means.shape[1]))
    for i in range(means.shape[1]):
        pdf[:,i] = np.exp(-0.5*np.sum((Xtest - means[:,i])* 
        np.dot(invcovmat, (Xtest - means[:,i]).T).T,1))/(np.sqrt(np.pi*2)*(np.power(covmatdet,2)))
    #Getting the index of the class with the highest probability
    trueLabel = np.argmax(pdf,1)
    #Index start from 0,class index start from 1.So to balance the index adding 1 to all the index
    trueLabel = trueLabel + 1
    ytest = ytest.reshape(ytest.size)
    #calculating the accuracy
    acc = 100*np.mean(trueLabel == ytest)
    # IMPLEMENT THIS METHOD
    return acc

def qdaTest(means,covmats,Xtest,ytest):
    # Inputs
    # means, covmats - parameters of the QDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    
    # IMPLEMENT THIS METHOD
    pdf= np.zeros((Xtest.shape[0],means.shape[1]))
    for i in range(means.shape[1]):
        invcovmat = np.linalg.inv(covmats[i])
        covmatdet = np.linalg.det(covmats[i])
        pdf[:,i] = np.exp(-0.5*np.sum((Xtest - means[:,i])* 
        np.dot(invcovmat, (Xtest - means[:,i]).T).T,1))/(np.sqrt(np.pi*2)*(np.power(covmatdet,2)))
    #Getting the index of the class with the highest probability
    trueLabel = np.argmax(pdf,1)
    #Index start from 0,class index start from 1.So to balance the index adding 1 to all the index
    trueLabel = trueLabel + 1
    ytest = ytest.reshape(ytest.size)
    #calculating the accuracy
    acc = 100*np.mean(trueLabel == ytest)
    return acc

def learnOLERegression(X,y):
    # Inputs:
    # X = N x d
    # y = N x 1
    # Output:
    # w = d x 1
    X_transpose = np.transpose(X)

    # Product of X-transpose and X
    prod1 = np.dot(X_transpose, X)
    # Inverse of the product above
    inverse = inv(prod1)
               
    w = np.dot(inverse, np.dot(X_transpose, y))
    return w

def learnRidgeRegression(X,y,lambd):
    # Inputs:
    # X = N x d                                                               
    # y = N x 1 
    # lambd = ridge parameter (scalar)
    # Output:                                                                  
    # w = d x 1                                                                

    N = X.shape[0]
    d = X.shape[1]
    # Make identity matrix
    identity = np.identity(d)
    
    # Product of lambda, N, and identity matrix
    lambda_identity = np.multiply(lambd, np.multiply(N, identity))
    
    X_transpose = np.transpose(X)

    # Product of X-transpose and X
    prod1 = np.dot(X_transpose, X)
    
    # Inverse of the sum of the lambda-identity matrix and the product above
    inverse = inv(np.add(lambda_identity, prod1))
               
    w = np.dot(inverse, np.dot(X_transpose, y))
    return w

def testOLERegression(w,Xtest,ytest):
    # Inputs:
    # w = d x 1
    # Xtest = N x d
    # ytest = X x 1
    N = Xtest.shape[0]
    diff = np.subtract(ytest, np.dot(Xtest, w));
                
    # Output:
    rmse = np.dot(np.transpose(diff), diff)
    rmse = np.divide(np.sqrt(rmse), N)
    return rmse

def regressionObjVal(w, X, y, lambd):

    # compute squared error (scalar) and gradient of squared error with respect
    # to w (vector) for the given data X and y and the regularization parameter
    # lambda                                                                  

    # IMPLEMENT THIS METHOD                                             
    return error, error_grad

def mapNonLinear(x,p):
    # Inputs:                                                                  
    # x - a single column vector (N x 1)                                       
    # p - integer (>= 0)                                                       
    # Outputs:
    # Xd - (N x (d+1))  
    
    N = x.shape[0]
    Xd = np.empty([N, p+1])
    for i in range(0, N):
        for j in range(0, p+1):
            Xd[i][j] = np.power(x[i], j)
    return Xd

# Main script
folderpath = '/home/hharwani/Downloads/ML-Project-2/'

# Problem 1
# load the sample data                                                                 

X,y,Xtest,ytest = pickle.load(open(folderpath + 'sample.pickle','rb'))            

def plotGraph(Y,Z):
    colorList=['r','g','b','y','c']
    for i in range (Y.shape[0]):
        plt.scatter(Y[i,0],Y[i,1],c=colorList[int(Z[i])-1])
    plt.plot()
    
def plotGraphPoints(Y,Z):
    colorList=['g','r','black','c','y']
    for i in range (Y.shape[0]):
        plt.scatter(Y[i,0],Y[i,1],c=colorList[int(Z[i])-1])
    plt.plot()
    
def generateMesh(means,covmat,qdaFlag):
    x1 = np.linspace(0,16,num=101)
    x2 = np.linspace(0,16,num=101)
    x=np.meshgrid(x1,x2)
    x=np.array(x)
    c=x[0].reshape(101*101,1)
    d=x[1].reshape(101*101,1)
    f=np.hstack((c,d))
    invcovmat = np.linalg.inv(covmat)
    covmatdet = np.linalg.det(covmat)
    if qdaFlag is False:
        pdf= np.zeros((f.shape[0],means.shape[1]))
        for i in range(means.shape[1]):
            pdf[:,i] = np.exp(-0.5*np.sum((f - means[:,i])* 
            np.dot(invcovmat, (f - means[:,i]).T).T,1))/(np.sqrt(np.pi*2)*(np.power(covmatdet,2)))
    else:
        pdf= np.zeros((f.shape[0],means.shape[1]))
        for i in range(means.shape[1]):
            invcovmat = np.linalg.inv(covmat[i])
            covmatdet = np.linalg.det(covmat[i])
            pdf[:,i] = np.exp(-0.5*np.sum((f - means[:,i])* 
            np.dot(invcovmat, (f - means[:,i]).T).T,1))/(np.sqrt(np.pi*2)*(np.power(covmatdet,2)))
    trueLabel = np.argmax(pdf,1)
    trueLabel = trueLabel + 1
    plotGraph(f,trueLabel)
    
def generatePoints(Xtest,means,covmat,qdaFlag):
    invcovmat = np.linalg.inv(covmat)
    covmatdet = np.linalg.det(covmat)
    if qdaFlag is False:
        pdf= np.zeros((Xtest.shape[0],means.shape[1]))
        for i in range(means.shape[1]):
            pdf[:,i] = np.exp(-0.5*np.sum((Xtest - means[:,i])* 
            np.dot(invcovmat, (Xtest - means[:,i]).T).T,1))/(np.sqrt(np.pi*2)*(np.power(covmatdet,2)))
    else:
        pdf= np.zeros((Xtest.shape[0],means.shape[1]))
        for i in range(means.shape[1]):
            invcovmat = np.linalg.inv(covmat[i])
            covmatdet = np.linalg.det(covmat[i])
            pdf[:,i] = np.exp(-0.5*np.sum((Xtest - means[:,i])* 
            np.dot(invcovmat, (Xtest - means[:,i]).T).T,1))/(np.sqrt(np.pi*2)*(np.power(covmatdet,2)))
    trueLabel = np.argmax(pdf,1)
    trueLabel = trueLabel + 1
    plotGraphPoints(Xtest,trueLabel)

# LDA
means,covmat = ldaLearn(X,y)
ldaacc = ldaTest(means,covmat,Xtest,ytest)
print('LDA Accuracy = '+str(ldaacc))
generateMesh(means,covmat,False)
generatePoints(Xtest,means,covmat,False)
plt.title("LDA")
plt.show()
# QDA

meansQda,covmatsQda = qdaLearn(X,y)
qdaacc = qdaTest(meansQda,covmatsQda,Xtest,ytest)
generateMesh(meansQda,covmatsQda,True)
generatePoints(Xtest,meansQda,covmatsQda,True)
plt.title("QDA")
print('QDA Accuracy = '+str(qdaacc))
plt.show()
# Problem 2

X,y,Xtest,ytest = pickle.load(open(folderpath + 'diabetes.pickle','rb'))   
# add intercept
X_i = np.concatenate((np.ones((X.shape[0],1)), X), axis=1)
Xtest_i = np.concatenate((np.ones((Xtest.shape[0],1)), Xtest), axis=1)

w = learnOLERegression(X,y)
mle = testOLERegression(w,Xtest,ytest)

w_i = learnOLERegression(X_i,y)
mle_i = testOLERegression(w_i,Xtest_i,ytest)

print('RMSE without intercept '+str(mle))
print('RMSE with intercept '+str(mle_i))

# Problem 3
k = 21
lambdas = np.linspace(0, 0.004, num=k)
i = 0
rmses3 = np.zeros((k,1))
for lambd in lambdas:
    w_l = learnRidgeRegression(X_i,y,lambd)
    rmses3[i] = testOLERegression(w_l,Xtest_i,ytest)
    i = i + 1
#plt.subplot(211)
#plt.plot(lambdas,rmses3)


# Problem 4
k = 21
lambdas = np.linspace(0, 0.004, num=k)
i = 0
rmses4 = np.zeros((k,1))
opts = {'maxiter' : 100}    # Preferred value.                                                
'''
w_init = np.zeros((X_i.shape[1],1))
for lambd in lambdas:
    args = (X_i, y, lambd)
    w_l = minimize(regressionObjVal, w_init, jac=True, args=args,method='CG', options=opts)
    w_l_1 = np.zeros((X_i.shape[1],1))
    for j in range(len(w_l.x)):
        w_l_1[j] = w_l.x[j]
    rmses4[i] = testOLERegression(w_l_1,Xtest_i,ytest)
    i = i + 1
plt.plot(lambdas,rmses4)
'''

# Problem 5
pmax = 7
lambda_opt = lambdas[np.argmin(rmses4)]
rmses5 = np.zeros((pmax,2))
for p in range(pmax):
    Xd = mapNonLinear(X[:,2],p)
    Xdtest = mapNonLinear(Xtest[:,2],p)
    w_d1 = learnRidgeRegression(Xd,y,0)
    rmses5[p,0] = testOLERegression(w_d1,Xdtest,ytest)
    w_d2 = learnRidgeRegression(Xd,y,lambda_opt)
    rmses5[p,1] = testOLERegression(w_d2,Xdtest,ytest)
plt.subplot(212)
plt.plot(range(pmax),rmses5)
plt.legend(('No regularization','With regularization'))

plt.axis('equal')
plt.show()
#plt.show()
