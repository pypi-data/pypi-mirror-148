'''This module defines various partitioning classes which partitions samples in batches of training and test split. 
These classes must have the sklearn equivalent of a split method. The split method returns a list of train-test partitions; 
one for each fold in the experiment. See sklearn.model_selection.KFold for an example partitioner.'''

# imports
import numpy as np
from sklearn.model_selection import StratifiedGroupKFold
import copy 
import pandas as pd

class TrainTestPartitioner():
    def __init__(self, train_idx, test_idx):
        self.train_idx = train_idx
        self.test_idx = test_idx

    def split(self, X=None, y=None):
        return [[self.train_idx, self.test_idx]]

class TrainPartitioner():
    def __init__(self):
        pass
    def split(self, X=None, y=None):
        return [[np.arange(np.shape(X)[0]), []]]


class StratifiedGroupKFoldForEachUniqueY():
        def __init__(self, n_splits, shuffle=False, random_state=42):
            self.n_splits = n_splits
            self.shuffle = shuffle
            self.random_state = random_state

        def __str__(self):
            return "StratifiedGroupKFoldForEachUniqueY(n_splits=%d, shuffle=%r, random_state=%d"%(self.n_splits, self.shuffle, self.random_state)
        
        def split(self, X, y, groups):
                train = {}
                test = {}
                if isinstance(X, pd.core.frame.DataFrame):
                    X = X.values
                if isinstance(y, pd.core.frame.DataFrame):
                    y = y.values
                if isinstance(groups, pd.core.frame.DataFrame):
                    groups = groups.values

                for unique_y in np.unique(y):
                        idxs_unique_y = np.where(y == unique_y)[0]
                        cv = StratifiedGroupKFold(n_splits=self.n_splits, shuffle=self.shuffle, random_state=self.random_state)
                        splits = cv.split(X[idxs_unique_y], y[idxs_unique_y], groups[idxs_unique_y])
                        for i, split in enumerate(splits):
                                train_idxs = train.get(i, [])
                                test_idxs = test.get(i, [])
                                
                                train_idxs.extend(idxs_unique_y[split[0]])
                                test_idxs.extend(idxs_unique_y[split[1]])

                                train[i] = train_idxs
                                test[i] = test_idxs
                
                self.splits = []
                for k, train_list in train.items():
                        test_list = test[k]
                        temp = copy.copy(train_list)
                        temp.extend(test_list)
                        assert np.unique(temp).shape[0] == X.shape[0], 'All samples not present in the split'
                        self.splits.append([train_list, test_list])

                return self.splits