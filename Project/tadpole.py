# import libraries
import warnings
warnings.filterwarnings(action='ignore') # to ignore warnings when loading data

import pickle
import pandas as pd
import numpy as np

# import sklearn libraries
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV

class Tadpole():
    def __init__(self, basepath="./tadpole_challenge/", filename="TADPOLE_D1_D2.csv", 
                 savepath="./models/", isCorr=False, debug=False):
        """
        Description:
            init method for class
        """
        self.basepath = basepath
        self.filename = filename
        self.savepath = savepath
        self.isCorr   = isCorr
        self.debug    = debug

        # load data on initialization
        self.load() 
    
    def preprocess(self, df, isCorr):
        """
        Description:
            method to preprocess the tadpole data.
        Arguments:
          df     - [pd.DataFrame] `TADPOLE_D1_D2.csv` as a dataframe
          isCorr - [boolean] if True, remove correlated features
        Returns [pd.DataFrame]:
          df - preprocessed data
        """
        # list of columns as features (starting point)
        getting_started = ["RID", "VISCODE", "DX_bl",
                           "DX", "ADAS13", "Ventricles",
                           "CDRSB", "ADAS11", "MMSE", "RAVLT_immediate",
                           "Hippocampus", "WholeBrain", "Entorhinal", "MidTemp",
                           "FDG", "AV45",
                           "ABETA_UPENNBIOMK9_04_19_17", "TAU_UPENNBIOMK9_04_19_17", "PTAU_UPENNBIOMK9_04_19_17",
                           "APOE4", "AGE"]

        # select columns
        df = df[getting_started]

        # based on EDA remove correlated features per class of biomarkers
        # Cognitive tests:
        # ADAS11 because it might be too correlated with DX_bl, MMSE because of missing values; 
        # we keep both CDRSB and RAVLT_immediate, since they are not correlated

        # MRI:
        # Entorhinal, MidTemp, Hippocampus based on nr of missing values

        # PET:
        # AV45 based on nr of missing values

        # CSF:
        # TAU_UPENNBIOMK9_04_19_17 (tau level), PTAU_UPENNBIOMK9_04_19_17 (phosphorylated tau level)

        if isCorr:
            df = df.drop(columns=["ADAS11","MMSE", 
                                  "Entorhinal", "MidTemp", "Hippocampus", 
                                  "TAU_UPENNBIOMK9_04_19_17", "PTAU_UPENNBIOMK9_04_19_17"])

        # filter out only baseline visits
        df = df[df["VISCODE"] == "bl"].reset_index(drop=True).drop(columns='VISCODE')

        # fix "DX" column
        df['DX'] = df['DX'].fillna('nan')

        # remove rows with nan DX values
        df = df[df['DX'] != 'nan'].reset_index(drop=True)

        # fix "ABETA_UPENNBIOMK9_04_19_17, TAU_UPENNBIOMK9_04_19_17, PTAU_UPENNBIOMK9_04_19_17" column
        if isCorr:
            err_cols = ["ABETA_UPENNBIOMK9_04_19_17"]
        else:
            err_cols = ["ABETA_UPENNBIOMK9_04_19_17", "TAU_UPENNBIOMK9_04_19_17", "PTAU_UPENNBIOMK9_04_19_17"]
        for c in err_cols:
            df[c] = df[c].apply(lambda x: None if x == ' ' or '<' in x or '>' in x else x)
            df[c] = df[c].astype(float)

        # convert "DX_bl" to categorical values
        df = df.drop(columns=['DX'])

        # Reduce to 3 categories: AD, MCI, CN
        df = df.replace('LMCI', 'MCI')
        df = df.replace('EMCI', 'MCI')
        df = df.replace('SMC', 'MCI')

        le = LabelEncoder()
        df[['DX_bl']] = df[['DX_bl']].apply(le.fit_transform)
        keys = [0, 1, 2]
        label_dict = dict(zip(keys, le.inverse_transform(keys)))

        # handle missing data (imputation by interpolation)
        impcols = [c for c in df.columns if c not in ['RID', 'DX_bl']]
        features = df.drop(columns=['RID', 'DX_bl']).to_numpy()  
        features = SimpleImputer(missing_values=np.nan, strategy='mean').fit(features).transform(features)
        df[impcols] = pd.DataFrame(features)

        # normalize data
        contcols = [c for c in df.columns if df[c].dtype == np.float64]
        df[contcols] = MinMaxScaler().fit_transform(df[contcols])
        return df, label_dict

    def load(self):
        """
        Description:
            function to retrieve preprocessed data.
        Arguments:
            path - [string] the directory in which `TADPOLE_D1_D2.csv` resides
            isCorr - [boolean] if True, remove correlated features
        Returns [(np.ndarray, np.ndarray)]:
            X - features
            y - labels
            label_dict - label dictionary
        """
        if self.debug:
            print("loading tadpole dataset")
        d1_d2_df = pd.read_csv(self.basepath + self.filename)
        
        if self.debug:
            print("pre-processing dataset")
        self.df, self.label_dict = self.preprocess(d1_d2_df, self.isCorr)
        self.X = self.df.drop(columns=['DX_bl', 'RID', 'ADAS13', 'Ventricles']).to_numpy()
        self.y = self.df['DX_bl'].to_numpy()
    
    def split(self, random_state=0, test_size=0.2, sfm_file="sfm_2.pkl", refit=False):
        """
        Description:
            method to split dataset into train and test
        """
        if self.debug:
            print("splitting dataset to train and test datasets")
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, 
                                                                                test_size=test_size, 
                                                                                random_state=random_state, 
                                                                                stratify=self.y)
        if refit:
            self.refit_data(sfm_file)
        return self.X_train, self.X_test, self.y_train, self.y_test                                                                                
        
    def save(self, model, modelname):
        """
        Description:
            method to save trained model
        
        Arguments:
            model - trained model
        """
        if self.debug:
            print("saving trained model")
        with open(self.savepath + modelname, 'wb') as file:
            pickle.dump(model, file)
    
    def refit_data(self, sfm_file):
        """
        Description:
            function to refit data based on fitted SelectFromModel
        
        Arguments:
            sfm_file (str) - file name of sfm model
                sfm_1.pkl: threshold = 0.04
                sfm_2.pkl: threshold = 0.01
        """
        if self.debug:
            print("refitting data")
        with open(self.savepath + sfm_file, 'rb') as file:
            sfm = pickle.load(file)
        self.X_train = sfm.transform(self.X_train)
        self.X_test = sfm.transform(self.X_test)
    
    def gridsearch(self, param_grid, clf, scoring=None, k=5, n_jobs=4, verbose=2):
        """
        Description:
            method to perform Grid Search CV
        Arguments:
            param_grid - [dictionary] parameter grid settings
            clf - [sklearn] classifier model for grid search
            k - [int] k-fold value
            n_jobs - [int] number of jobs (Parallelization)
        Returns:
            cv_clf - [sklearn] trained model after grid search
        """
        if self.debug:
            print("performing grid search")
        cv_clf = GridSearchCV(clf, param_grid, scoring=scoring, refit='BA', n_jobs=n_jobs, cv=k, verbose=verbose)
        cv_clf.fit(self.X_train, self.y_train)
        return cv_clf
