import pandas as pd
import numpy as np
import gain
from missingpy import MissForest

def unique_non_null(col_data, col_name):
    cat = col_data.dropna().unique()
    return [col_name + '_' + x for x in cat]

''' 
This function extract all the uniques values for each categorical column
'''
def get_all_unique_categories(df: object) -> object:
    categories = []  # keep all categories
    for i in df.columns:
        if df[i].dtype in ['object', 'bool', 'category']:
            categories.extend(unique_non_null(df[i], i))
        else:
            categories.append(i)
    return categories

class ImputeTransformer():
    def __init__(self,categories):
        self.categories = categories
        print('In saisakul transformer')

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        #get dummies
        x_dummies = pd.get_dummies(x)
        x_dummies = x_dummies.reindex(columns = self.categories, fill_value = 0)

        #for each categorical column, change all 0 to Nan
        for c in x.columns:
            extracted_cols = [s for s in self.categories if s.startswith(c + '_')]
            if extracted_cols:
                zero_cond = (x_dummies[extracted_cols] == 0).all(axis=1)
                x_dummies.loc[zero_cond, extracted_cols] = np.nan
        return x_dummies


def impute_gain(df, categories = None, gain_param =None, no_set = 1):
    if categories is None:
        categories = get_all_unique_categories(df)

    if gain_param is None:
        gain_param = {'batch_size': min(len(df), 16, 32, 64, 128, 256), 'hint_rate': 0.3, 'alpha': 0.3, 'iterations': 100}

    im = ImputeTransformer(categories=categories)
    im.fit(df)
    df_trans = im.transform(df)

    imputed_data = []
    for i in range(no_set):
        imputed = gain.gain(df_trans.to_numpy(), gain_param)
        imputed_data.append(pd.DataFrame(imputed, columns=categories, index = df.index))
    return imputed_data

def impute_missforest(df):
    imputer = MissForest()
    imputed = imputer.fit_transform(df)
    return imputed