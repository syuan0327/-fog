from collections import Counter
from sklearn.datasets import make_classification
from imblearn.under_sampling import RandomUnderSampler 
X, y = make_classification(n_classes=2, class_sep=2,weights=[0.1, 0.9], n_informative=3, n_redundant=1, flip_y=0,
n_features=20, n_clusters_per_class=1, n_samples=1000, random_state=10)
print('Original dataset shape %s' % Counter(y))
print(X.shape)
rus = RandomUnderSampler(random_state=42)
X_res, y_res = rus.fit_resample(X, y)
print(X_res.shape)
print('Resampled dataset shape %s' % Counter(y_res))
