from sklearn.linear_model import LogisticRegression
import pyexcel as pe
from sklearn import datasets
import numpy as np
import statsmodels.api as sm


def load_coded_data():
    """Load and return the sample coded dataset (classification).

    The socio-economic dataset is based from the survey data conducted in district-2 Quezon City.
    """

    """
    column[0] = mode
    column[1] = age
    column[2] = gender
    column[3] = income
    
    todo: sample.xlsx should not be from core directory
    """
    X = pe.get_array(file_name="sample.xlsx", start_column=1, column_limit=3)
    reader = pe.Reader("sample.xlsx").column[0]
    return X, reader


z, y = load_coded_data()
print(z, y)
clf = LogisticRegression(multi_class="multinomial").fit(z, y)

print(clf.predict(z))
print(clf.score(z, y))

# print(clf.coef_)
# print(clf)

X2 = sm.add_constant(z)
est = sm.MNLogit(y, X2)

print(est.fit().summary())
