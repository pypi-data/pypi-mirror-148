from sklearn.model_selection import TimeSeriesSplit
from sklearn.utils.validation import check_array
import numpy as np

class GroupTimeSeriesSplit(TimeSeriesSplit):
    """
    Split time series data by grouping indices

    Parameters
    ----------
    n_splits : int
        Number of splits. If None, n_groups - 1
    n_test_group : int
        Number of groups in test data.
    """

    def __init__(self, n_splits=None, n_test_group=1):
        self.n_splits = n_splits  # クロスバリデーション分割数
        self.n_test_groups = n_test_group  # テストデータとして使用するグループ数
    
    def split(self, X, y, groups):
        """Generate indices to split data into training and test set.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data, where n_samples is the number of samples
            and n_features is the number of features.

        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.

        groups : array-like of shape (n_samples,)
            Group labels for the samples used while splitting the dataset into
            train/test set. NaN data should be removed before split.
        """
        # CV数を計算
        n_splits = self.get_n_splits(X, y, groups)
        n_groups = len(np.unique(groups))
        if n_groups - self.n_test_groups - n_splits < 0:
            raise ValueError(f"Too many splits={n_splits} for number of groups={n_groups}")
        # グループで昇順ソート
        sorted_groups = np.sort(np.unique(groups))

        # groupsにNaNが含まれていたら除外
        if np.sum(np.isnan(groups)) > 0:
            raise ValueError("NaN data should be removed before split")
        # 全インデックスを取得
        indices = np.arange(len(groups))

        # CV実行
        for i in range(n_splits):
            test_start_group = n_groups - self.n_test_groups - n_splits + 1  # 最初のテストデータのグループ番号
            # テストデータとするグループ
            test_group_indices = np.arange(test_start_group + i, test_start_group + i + self.n_test_groups)
            test_groups = sorted_groups[test_group_indices]
            is_test = np.isin(groups, test_groups)
            test_indices = indices[is_test]
            # 学習データとするグループ
            traing_group_indices = np.arange(test_start_group + i)
            train_groups = sorted_groups[traing_group_indices]
            is_train = np.isin(groups, train_groups)
            train_indices = indices[is_train]

            yield train_indices, test_indices

    def get_n_splits(self, X=None, y=None, groups=None):
        """Returns the number of splitting iterations in the cross-validator

        Parameters
        ----------
        X : object
            Always ignored, exists for compatibility.

        y : object
            Always ignored, exists for compatibility.

        groups : array-like of shape (n_samples,)
            Group labels for the samples used while splitting the dataset into
            train/test set.

        Returns
        -------
        n_splits : int
            Returns the number of splitting iterations in the cross-validator.
        """

        if self.n_splits is None:  # n_splits未指定時
            if groups is None:
                raise ValueError("The `groups` argument should not be None")
            groups = check_array(groups, ensure_2d=False, dtype=None)
            return len(np.unique(groups)) - self.n_test_groups
        else:
            return self.n_splits