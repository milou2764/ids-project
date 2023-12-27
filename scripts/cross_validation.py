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
    cross validate models with kfold = 5 and return the metrics
    '''
    
    models = {
            'KNN': KNeighborsClassifier(),
            'GaussianNB': GaussianNB(),
            'RandomForest': RandomForestClassifier(),
            'MLP': MLPClassifier(max_iter=1000)
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

        results[model] = cv_results

        #  print or log the cross-validation results
        for metric, values in cv_results.items():
            print(f'{metric.capitalize()} (mean): {values.mean()}')
            print(f'{metric.capitalize()} (std): {values.std()}')

    return results

def select_best_model(models_results):
    best=(None,0)
    for modelname,cv_results in models_results.items():
        mean_accuracy=cv_results['test_accuracy'].mean()
        if mean_accuracy>best[1]:
            best=(modelname,mean_accuracy)
    return best

def get_best_model(app):
    '''
    performs cross validation over several models and return the one with the best accuracy
    '''
    flows = get_app_flows(app)
    flows = preprocess_data(flows)
    X, y = extract_ground_truth(flows)

    results = cross_validate_models(X, y)
    best_model=select_best_model(results)
    print('The best model is',best_model[0],'with an average accuracy of',best_model[1])
    return best_model[0], X, y 

def main():
    print('example with SSH app flows')
    get_best_model('SSH')

if __name__ == "__main__":
    main()
