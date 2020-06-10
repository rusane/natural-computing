from evaluator import Evaluator

"""
Optimal parameters from grid search for each base learner.
"""
params = {
    'dtc': {},   
    
    'svc': {'C': 1000, 
            'class_weight': 'balanced',
            'gamma': 0.001, 
            'kernel': 'linear', 
            'tol': 1},
    
    'lra': {'C': 0.08858667904100823, 
            'class_weight': 'balanced', 
            'dual': False, 
            'penalty': 'l1', 
            'solver': 'liblinear', 
            'tol': 0.0001},
    
    'ann': {'activation': 'relu', 
            'alpha': 0.05, 
            'hidden_layer_sizes': (50, 50, 50), 
            'learning_rate': 'adaptive', 
            'solver': 'adam'}
}


def get_params(key):
    return params[key]


def run(clf, data, n_runs=30, output=None):    
    """
    Run the evaluation of a classifier for n times.

    Args:
        clf    = [Classifier] classifier to evaluate 
        data   = [Tadpole] Tadpole dataset
        n_runs = [int] number of runs
        output = [string] save path of the output

    Returns [pd.DataFrame]:
        Scores from the evaluation of the classifier.
    """
    evaluator = Evaluator(clf, data, n_runs=n_runs)
    evaluator.evaluate()
    if output:
        evaluator.export_to_csv(output)
    return evaluator.get_scores()


if __name__ == "__main__":
    pass
