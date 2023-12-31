from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
#from sklearn.neighbors import KNeighborsClassifier

from challenge2 import parse_data, preprocess_data, get_train_test_fp

train_fp,_ = get_train_test_fp()
print('parsing data')
X,y = parse_data(train_fp)
print('preprocessing data')
X = preprocess_data(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

#models = [GaussianNB(), RandomForestClassifier(), MLPClassifier(max_iter=1000),KNeighborsClassifier(n_neighbors=3)]
models = [GaussianNB(), RandomForestClassifier(), MLPClassifier(max_iter=1000)]
for model in models:
    print(model)
    model.fit(X_train,y_train)
    print('mean accuracy:',model.score(X_test,y_test))
