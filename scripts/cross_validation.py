from api import get_app_flows
from preprocessor import preprocess_data

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import KFold, cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score


def extract_ground_truth(data):
    '''
    Extract the ground truth from the dataset
    '''
    X = data.drop("Tag", axis=1)
    y = data["Tag"]
    return X, y

def cross_validate_models(X, y):
    '''
    cross validate models with kfold = 5 on each model in the 'models' variable
    '''
    
    models = {
            'KNN': KNeighborsClassifier(n_neighbors=3),
            'GaussianNB': GaussianNB(),
            'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
            'MLP': MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
    }

    results = {}

    for modelname, model in models.items():
        print(modelname)

        n_folds = 5

        #  evaluation metrics
        scoring = {
            'accuracy': make_scorer(accuracy_score),
            'precision': make_scorer(precision_score),
            'recall': make_scorer(recall_score),
            'f1': make_scorer(f1_score)
        }

        #  kfold using sklearn object
        kf = KFold(n_splits=n_folds, shuffle=True)

        #  perform cross-validation
        cv_results = cross_validate(model, X, y, cv=kf, scoring=scoring)
        #  print or log the cross-validation results
        for metric, values in cv_results.items():
            print(f'{metric.capitalize()} (mean): {values.mean()}')
            print(f'{metric.capitalize()} (std): {values.std()}')    

def main():
    #  get data
    ssh_flows = get_app_flows('SSH')
    
    #  preprocess data
    ssh_flows = preprocess_data(ssh_flows)

    X, y = extract_ground_truth(ssh_flows)

    cross_validate_models(X, y)

if __name__ == "__main__":
    main()
