from bigxml import Parser, xml_handle_element
from dataclasses import dataclass
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from challenge2 import get_train_test_fp
from challenge2 import convert_to_integer
from challenge2 import parse_data
from challenge2 import preprocess_data

def get_confusion_matrix(train_fp):
    # Get training data
    print('parsing training data')
    X,y = parse_data(train_fp)
    print('preprocessing training data')
    X = preprocess_data(X)

    X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=42)

    # train a random forest classifier
    model = RandomForestClassifier()
    print('training model')
    model.fit(X_train,y_train)
    
    print('making predictions')
    y_pred=model.predict(X_test)
    print(confusion_matrix(y_test, y_pred))

if __name__=='__main__':
    train_fp,_ = get_train_test_fp()
    get_confusion_matrix(train_fp)
