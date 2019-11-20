
import pandas as pd

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
