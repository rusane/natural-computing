from evaluator import Evaluator


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
