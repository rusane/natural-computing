from sklearn.metrics import balanced_accuracy_score, roc_auc_score, confusion_matrix

from matplotlib import pyplot as plt


class Classifier:
    """Generic classifier class."""


    def __init__(self, clf, params={}):
        """
        Initialize Classifier instance.

        Args:
            clf    = [sklearn.base.BaseEstimator] classifier instance
            params = [dict] clasifier parameters
        """
        self.clf = clf
        self.clf.set_params(**params)


    def fit(self, X, y):
        """
        Fit the classifier on the training data.

        Args:
            X = [np.ndarray] training features
            y = [np.ndarray] training labels
        """
        self.clf.fit(X, y)


    def predict(self, X, prob=False):
        """
        Predict the labels based on the features.

        Args:
            X    = [np.ndarray] features
            prob = [boolean] if True, the predictions are probabilities (default=False)

        Returns [ndarray]:
            Predictions.
        """
        if prob:
            y_pred = self.clf.predict_proba(X)
        else:
            y_pred = self.clf.predict(X)
        return y_pred


    def BCA(self, X, y):
        """
        Balanced Classification Accuracy (BCA) metric.

        Args:
            X = [np.ndarray] features
            y = [np.ndarray] labels

        Returns [float]:
            BCA
        """
        y_pred = self.predict(X)
        BCA = balanced_accuracy_score(y, y_pred)
        return BCA


    def mAUC(self, X, y):
        """
        Multiclass Area Under the Receiver Operating Curve (mAUC) metric.

        Args:
            X = [np.ndarray] features
            y = [np.ndarray] labels

        Returns [float]:
            mAUC
        """
        y_pred = self.predict(X, prob=True)
        mAUC = roc_auc_score(y, y_pred, multi_class='ovo', average='macro')
        return mAUC


    def fit_predict(self, X_train, y_train, X_test, y_test, verbose=False):
        """
        Fit the classifier and make predictions.

        Args:
            X_train = [np.ndarray] training features
            y_train = [np.ndarray] training labels
            X_test  = [np.ndarray] test features
            y_test  = [np.ndarray] test labels
            verbose = [boolean] if True, print metrics (defaukt=False)

        Returns [(float,)*4]:
            BCA_train  = BCA on training set
            BCA_test   = BCA on test set
            mAUC_train = mAUC on training set
            mAUC_test  = mAUC on test set
        """
        self.fit(X_train, y_train)
        BCA_train = self.BCA(X_train, y_train)
        BCA_test = self.BCA(X_test, y_test)
        mAUC_train = self.mAUC(X_train, y_train)
        mAUC_test = self.mAUC(X_test, y_test)
        if verbose: 
            print('# Train metrics')    
            print('BCA_train:', BCA_train)
            print('mAUC_train:', mAUC_train)
            print('# Test metrics')   
            print('BCA_test:', BCA_test)
            print('mAUC_test:', mAUC_test)
        return BCA_train, BCA_test, mAUC_train, mAUC_test


    def showConfusionMatrix(self, X, y, label_dict):
        """
        Show the confusion matrix using the given data.

        Args:
            X          = [np.ndarray] features
            y          = [np.ndarray] labels
            label_dict = [dict] dictionary of labels
        """
        cm = confusion_matrix(y, self.clf.predict(X))
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(cm, cmap='GnBu')
        ax.grid(False)
        ax.xaxis.set(ticks=(0, 1, 2), ticklabels=('Predicted ' + label_dict[0], 
                                                  'Predicted ' + label_dict[1], 
                                                  'Predicted ' + label_dict[2]))
        ax.yaxis.set(ticks=(0, 1, 2), ticklabels=('Actual ' + label_dict[0], 
                                                  'Actual ' + label_dict[1], 
                                                  'Actual ' + label_dict[2]))
        for i in range(3):
            for j in range(3):
                ax.text(j, i, cm[i, j], ha='center', va='center', color='black')
        plt.title('Test Data Confusion Matrix')
        plt.show()
    