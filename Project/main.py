from evaluator import Evaluator


def run(clf, data, n_runs=30, output=None):    
    evaluator = Evaluator(clf, data, n_runs=n_runs)
    evaluator.evaluate()
    if output:
        evaluator.export_to_csv(output)
    return evaluator.get_scores()


if __name__ == "__main__":
    pass
