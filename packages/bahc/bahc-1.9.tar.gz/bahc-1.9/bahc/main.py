import numpy as np
import fastcluster
from statsmodels.stats.correlation_tools import cov_nearest
import random


def dist(R):
    N = R.shape[0]
    d = R[idx]
    out = fastcluster.average(d)
    rho = 1-out[:,2]
    #
    #Genealogy Set
    dend = [([i],[]) for i in range(N)]+[[] for _ in range(out.shape[0])]
    
    for i,(a,b) in enumerate(out[:,:2].astype(int)):
        dend[i+N] = dend[a][0]+dend[a][1],dend[b][0]+dend[b][1]
    
    return dend[N:],rho


def AvLinkC(Dend,rho,R):

	N = R.shape[0]
	Rs = np.zeros((N,N))

	for (a,b),r in zip(Dend,rho):
		z = np.array(a).reshape(-1,1),np.array(b).reshape(1,-1)
		Rs[z] = r

	Rs = Rs+Rs.T

	np.fill_diagonal(Rs,1)
	return Rs	
    
def noise(N,T,epsilon=1e-10):
    return np.random.normal(0,epsilon ,size=(N,T))
    
def no_neg(x):
    l,v = np.linalg.eigh(x)
    p = l>0
    l,v = l[p],v[:,p]
    return np.dot(v*l,v.T)
    
def near(x,niter=100,eigtol=1e-6,conv=1e-8):
    
    D = np.zeros(x.shape)
    diag = x.diagonal()

    for _ in range(niter):

        y = x
        R = x - D
        x = no_neg(R)
        D = x - R
        np.fill_diagonal(x,diag)
        
        if np.linalg.norm(x-y,ord=np.inf)/np.linalg.norm(y,ord=np.inf)<conv:
            break
    else:
        print("it didn't converge")
    return x


def HigherOrder(C,K):

    Cf = np.identity(C.shape[0])
    for i in range(max(K)):
        res = C - Cf
        dend,rho =  dist(1-res)
        res = AvLinkC(dend,rho,res)
        np.fill_diagonal(res,0)
        Cf += res
        if i+1 in K:
            yield Cf.copy()

def filterCovariance(x,K=1,Nboot=100,method='near',is_correlation=False):
	'''
	Fiter covariance with k-BAHC
	input
	x: Data Matrix NxT
	K = recursion order. K can be a list if you want to compute different order simultaneusly, K=1 is the standard BAHC.
	Nboot: Number of bootstraps
	method: regularization of negative eigenvalues. 'no-neg' set them to zeros, 'near' find the neareset semi-positive matrix
	is_correlation: Set to True if you want to filter the correlation

	output
	Fitered covariance matrix NxN. If K is a list, then is then the output is a list of matrices NxN
	'''
	is_int = type(K)==int
	if is_int==True:
		K = [K]

	f = {'no-neg':no_neg,'near':cov_nearest}

	N,T = x.shape
	global idx    
	idx = np.triu_indices(N,1)
	ns = noise(N,T)
	rT = list(range(T))
	C = np.zeros((len(K),N,N))
	s = x.std(axis=1)
	
	if Nboot==0:
		Cb = np.corrcoef(x)
		C = np.array(list(map(f[method],(np.array(list(HigherOrder(Cb,K)))))))
		if is_correlation==False:
			C = C*np.outer(s,s)
		if is_int==True:
			return C[0]
		else:
			return C

	for _ in range(Nboot):
		xboost = x[:,random.choices(rT,k=T)] + ns

		Cb = np.corrcoef(xboost)
		C += np.array(list(map(f[method],(np.array(list(HigherOrder(Cb,K)))))))
		
	if is_correlation==False:
		C = (C/Nboot)*np.outer(s,s)
	else:
		C = (C/Nboot)

	if is_int==True:
		C = C[0]

	return C


'''
if __name__=='__main__':
	x = np.random.normal(0,1,size=(10,100))
	print(filterCovariance(x,K=[10,15],is_correlation=True,	method='near'))

'''
