import pandas as pd

from tadpole import Tadpole
from classifier import Classifier
from sklearn.svm import SVC

class Evaluator():
    def __init__(self, clf, data, n_runs=30):
        """
        Args:
            clf     = [Classifier] classifier instance
            data    = [Tadpole] tadpole dataset class instance
            n_runs  = [int] number of evaluation runs (default=30)
        """
        self.clf = clf
        self.data = data
        self.n_runs = n_runs
        self.scores = []
        self.data.load()


    def evaluate(self):
        for i in range(self.n_runs):
            self.data.split(random_state=i)
            X_train, y_train, X_test, y_test = self.data.X_train, self.data.y_train, self.data.X_test, self.data.y_test
            BCA_train, BCA_test, mAUC_train, mAUC_test = self.clf.fit_predict(X_train, 
                                                                              y_train, 
                                                                              X_test, 
                                                                              y_test)
            self.scores.append({ 
                                'BCA_train': BCA_train, 
                                'BCA_test': BCA_test, 
                                'mAUC_train': mAUC_train, 
                                'mAUC_test': mAUC_test 
                               })


    def export_to_csv(self, filename):            
        df = pd.DataFrame(self.scores)
        df.to_csv(filename, index=False)


if __name__ == "__main__":
    tp = Tadpole()
    params = {'C': 1000, 'class_weight': 'balanced', 'gamma': 0.001, 'kernel': 'linear', 'tol': 1}
    svc = Classifier(SVC(probability=True), params)

    evaluator = Evaluator(svc, tp, n_runs=3)
    evaluator.evaluate()
    evaluator.export_to_csv('./results/test.csv')
