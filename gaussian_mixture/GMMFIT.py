
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import mixture
import joblib


df = pd.read_csv("/Users/jpoullet/Documents/MIT/Thesis/ML6867_project/data_UPS/list_tuesday.csv")
X = df.to_numpy()
print(X)

# fit a Gaussian Mixture Model, n_components corresponds to K
clf = mixture.GaussianMixture(n_components=50, covariance_type='full')
clf.fit(X)

# output the mixture
joblib.dump(clf, 'test.joblib')

# read the mixture
clf = joblib.load('test.joblib')

#Sample generation. Labels are not useful for us, they refer to the gaussian component used to generate sample
sample_X, _ = clf.sample(n_samples=1000)
print(sample_X)

maxK = 20
bicscore = np.zeros(maxK)
for i in range(0,maxK):
    print(i)
    clfi = mixture.GaussianMixture(n_components=i+1, covariance_type='full')
    clfi.fit(X)
    bicscore[i] = clfi.bic(X)
print(bicscore)
bicgradient = np.zeros(maxK-1)
#plt.plot(range(maxK),bicscore)
for i in range(maxK -1):
    bicgradient[i] = bicscore[i+1] - bicscore[i]
plt.plot(range(maxK-1),bicgradient)
plt.title("Gradient of BIC scores")
plt.xlabel("Number of components")
plt.ylabel("Value of gradient")
plt.show()

plt.plot(range(maxK-1),bicscore[:(maxK-1)])
plt.title("BIC scores")
plt.xlabel("Number of components")
plt.ylabel("Value of BIC")
plt.show()
