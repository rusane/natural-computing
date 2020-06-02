import warnings
warnings.filterwarnings(action='ignore') # to ignore warnings when loading data

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler


def preprocess(df, isCorr = False):
    """
    Preprocesses the data.

    Args:
      df     = [pd.DataFrame] `TADPOLE_D1_D2.csv` as a dataframe
      isCorr = [boolean] if True, remove correlated features

    Returns [pd.DataFrame]:
      df = preprocessed data
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
    # ADAS11 because it might be too correlated with DX_bl, MMSE because of missing values; we keep both CDRSB and RAVLT_immediate, since they are not correlated
    
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


def get_data(path, isCorr = False):
  """
  Main function to retrieve preprocessed data.

  Args:
    path = [string] the directory in which `TADPOLE_D1_D2.csv` resides
    isCorr = [boolean] if True, remove correlated features

  Returns [(np.ndarray, np.ndarray)]:
    X = features
    y = labels
    label_dict = label dictionary
  """
  df = pd.read_csv(path + "TADPOLE_D1_D2.csv")
  df, label_dict = preprocess(df, isCorr)
  X = df.drop(columns=['DX_bl', 'RID', 'ADAS13', 'Ventricles']).to_numpy()
  y = df['DX_bl'].to_numpy()
  return X, y, label_dict
 

if __name__ == "__main__":
    pass
