#!/usr/bin/env python3

import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

DATA_DIR = 'data'
DATA_FILE = DATA_DIR + '/raw_data.csv'

def main():
    df = pd.read_csv(DATA_FILE)

    x = df.drop(['rank1', 'rank2', 'rank3'], axis=1)
    y = df['rank1'] - 1

    print(x.head())
    print(y.head())

    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2)

    lgb_train = lgb.Dataset(x_train, y_train)
    lgb_valid = lgb.Dataset(x_val, y_val, reference=lgb_train)

    lgbm_params = {
            'objective': 'multiclass',
            'metric': 'multi_logloss',
            'num_class': 18
            }

    model = lgb.train(lgbm_params, train_set=lgb_train, valid_sets=lgb_valid)

    y_pred = model.predict(x_val)
    y_pred_class = np.argmax(y_pred, axis=1)
    print(y_pred)
    print(y_pred_class)

    accuracy = accuracy_score(y_val, y_pred_class)
    print(accuracy)

if __name__ == '__main__':
    main()
