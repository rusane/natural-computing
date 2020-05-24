import warnings
warnings.filterwarnings(action='ignore') # to ignore warnings when loading data

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler


def preprocess(df):
    """
    Preprocesses the data.

    Args:
      df = [pd.DataFrame] `TADPOLE_D1_D2.csv` as a dataframe

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
    
    # filter out only baseline visits
    df = df[df["VISCODE"] == "bl"].reset_index(drop=True).drop(columns='VISCODE')
    
    # fix "DX" column
    df['DX'] = df['DX'].fillna('nan')
    
    # remove rows with nan DX values
    df = df[df['DX'] != 'nan'].reset_index(drop=True)
    
    # fix "ABETA_UPENNBIOMK9_04_19_17, TAU_UPENNBIOMK9_04_19_17, PTAU_UPENNBIOMK9_04_19_17" column
    err_cols = ["ABETA_UPENNBIOMK9_04_19_17", "TAU_UPENNBIOMK9_04_19_17", "PTAU_UPENNBIOMK9_04_19_17"]
    for c in err_cols:
        df[c] = df[c].apply(lambda x: None if x == ' ' or '<' in x or '>' in x else x)
        df[c] = df[c].astype(float)
    
    # convert "DX_bl" and "DX" to categorical values
    df[['DX_bl', 'DX']] = df[['DX_bl', 'DX']].apply(LabelEncoder().fit_transform)
    
    # handle missing data (imputation by interpolation)
    impcols = [c for c in df.columns if c not in ['RID', 'DX_bl']]
    features = df.drop(columns=['RID', 'DX_bl']).to_numpy()    
    features = SimpleImputer(missing_values=np.nan, strategy='mean').fit(features).transform(features)
    df[impcols] = pd.DataFrame(features)
    
    # normalize data
    contcols = [c for c in df.columns if df[c].dtype == np.float64]
    df[contcols] = MinMaxScaler().fit_transform(df[contcols])
    
    return df


def get_data(path):
  """
  Main function to retrieve preprocessed data.

  Args:
    path = [string] the directory in which `TADPOLE_D1_D2.csv` resides

  Returns [(np.ndarray, np.ndarray)]:
    X = features
    y = labels
  """
  df = pd.read_csv(path + "TADPOLE_D1_D2.csv")
  df = preprocess(df)
  X = df.drop(columns=['DX_bl', 'RID', 'DX', 'ADAS13', 'Ventricles']).to_numpy()
  y = df['DX_bl'].to_numpy()
  return X, y


if __name__ == "__main__":
    pass
