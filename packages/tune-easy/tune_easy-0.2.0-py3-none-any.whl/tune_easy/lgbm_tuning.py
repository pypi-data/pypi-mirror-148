import time
import numpy as np
from lightgbm import LGBMRegressor, LGBMClassifier

from .param_tuning import ParamTuning
from seaborn_analyzer._cv_eval_set import cross_val_score_eval_set, init_eval_set

class LGBMRegressorTuning(ParamTuning):
    """
    Tuning class for LGBMRegressor

    See ``tune_easy.param_tuning.ParamTuning`` to see API Reference of all methods
    """

    # 共通定数
    _SEED = 42  # デフォルト乱数シード
    _CV_NUM = 5  # 最適化時のクロスバリデーションのデフォルト分割数
    
    # 学習器のインスタンス (LightGBM)
    ESTIMATOR = LGBMRegressor()
    # 学習時のパラメータのデフォルト値
    FIT_PARAMS = {'verbose': 0,  # 学習中のコマンドライン出力
                  'early_stopping_rounds': 10,  # 学習時、評価指標がこの回数連続で改善しなくなった時点でストップ
                  'eval_metric': 'rmse'  # early_stopping_roundsの評価指標
                  }
    # 最適化で最大化するデフォルト評価指標('r2', 'neg_mean_squared_error', 'neg_root_mean_squared_error', etc.)
    _SCORING = 'neg_root_mean_squared_error'

    # 最適化対象外パラメータ
    NOT_OPT_PARAMS = {'objective': 'regression',  # 最小化させるべき損失関数
                      'random_state': _SEED,  # 乱数シード
                      'boosting_type': 'gbdt',  # boosting_type
                      'n_estimators': 10000  # 最大学習サイクル数（評価指標がearly_stopping_rounds連続で改善しなければ打ち切り）
                      }

    # グリッドサーチ用パラメータ
    CV_PARAMS_GRID = {'reg_alpha': [0.0001, 0.003, 0.1],
                      'reg_lambda': [0.0001, 0.1],
                      'num_leaves': [2, 10, 50],
                      'colsample_bytree': [0.4, 1.0],
                      'subsample': [0.4, 1.0],
                      'subsample_freq': [0, 7],
                      'min_child_samples': [2, 10, 50]
                      }

    # ランダムサーチ用パラメータ
    N_ITER_RANDOM = 400  # ランダムサーチの試行数
    CV_PARAMS_RANDOM = {'reg_alpha': [0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1],
                        'reg_lambda': [0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1],
                        'num_leaves': [2, 8, 14, 20, 26, 32, 38, 44, 50],
                        'colsample_bytree': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        'subsample': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        'subsample_freq': [0, 1, 2, 3, 4, 5, 6, 7],
                        'min_child_samples': [0, 2, 8, 14, 20, 26, 32, 38, 44, 50]
                        }

    # ベイズ最適化用パラメータ
    N_ITER_BAYES = 60  # ベイズ最適化の試行数
    INIT_POINTS = 10  # 初期観測点の個数(ランダムな探索を何回行うか)
    _ACQ = 'ei'  # 獲得関数(https://ohke.hateblo.jp/entry/2018/08/04/230000)
    N_ITER_OPTUNA = 200  # Optunaの試行数
    BAYES_PARAMS = {'reg_alpha': (0.0001, 0.1),
                    'reg_lambda': (0.0001, 0.1),
                    'num_leaves': (2, 50),
                    'colsample_bytree': (0.4, 1.0),
                    'subsample': (0.4, 1.0),
                    'subsample_freq': (0, 7),
                    'min_child_samples': (0, 50)
                    }
    INT_PARAMS = ['num_leaves', 'subsample_freq', 'min_child_samples']  # 整数型のパラメータのリスト(ベイズ最適化時は都度int型変換する)

    # 範囲選択検証曲線用パラメータ範囲
    VALIDATION_CURVE_PARAMS = {'reg_alpha': [0, 0.0001, 0.001, 0.003, 0.01, 0.03, 0.1, 1, 10],
                               'reg_lambda': [0, 0.0001, 0.001, 0.003, 0.01, 0.03, 0.1, 1, 10],
                               'num_leaves': [2, 4, 8, 16, 32, 64, 96, 128, 192, 256],
                               'colsample_bytree': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                               'subsample': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                               'subsample_freq': [0, 1, 2, 3, 4, 5, 6, 7],
                               'min_child_samples': [0, 2, 5, 10, 20, 30, 50, 70, 100]
                               }
    # 検証曲線表示等で使用するパラメータのスケール('linear', 'log')
    PARAM_SCALES = {'reg_alpha': 'log',
                    'reg_lambda': 'log',
                    'num_leaves': 'linear',
                    'colsample_bytree': 'linear',
                    'subsample': 'linear',
                    'subsample_freq': 'linear',
                    'min_child_samples': 'linear'
                    }

    def _train_param_generation(self, estimator, src_fit_params):
        """
        入力データから学習時パラメータの生成 (eval_set)
        
        Parameters
        ----------
        estimator : Dict
            学習器
        src_fit_params : Dict
            処理前の学習時パラメータ
        """

        # fit_paramsにeval_metricが入力されており、eval_setが入力されていないときの処理
        fit_params, self.eval_set_selection = init_eval_set(
                self.eval_set_selection, src_fit_params, self.X, self.y)

        return fit_params

    def _bayes_evaluate(self, **kwargs):
        """
         ベイズ最適化時の評価指標算出メソッド
        """
        # 最適化対象のパラメータ
        params = kwargs
        params = self._pow10_conversion(params, self.param_scales)  # 対数パラメータは10のべき乗に変換
        params = self._int_conversion(params, self.int_params)  # 整数パラメータはint型に変換
        params.update(self.not_opt_params)  # 最適化対象以外のパラメータも追加
        # XGBoostのモデル作成
        estimator = self.estimator
        estimator.set_params(**params)

        # 全データ or 学習データ or テストデータをeval_setに入力して自作メソッドでクロスバリデーション
        scores = cross_val_score_eval_set(self.eval_set_selection, estimator, self.X, self.y, cv=self.cv, groups=self.cv_group,
                                          scoring=self.scoring, fit_params=self.fit_params, n_jobs=None)
        val = scores.mean()
        # 所要時間測定
        self._elapsed_times.append(time.time() - self._start_time)

        return val

    def _optuna_evaluate(self, trial):
        """
        Optuna最適化時の評価指標算出メソッド
        """
        # パラメータ格納
        params = {}
        for k, v in self.tuning_params.items():
            log = True if self.param_scales[k] == 'log' else False  # 変数のスケールを指定（対数スケールならTrue）
            if k in self.int_params:  # int型のとき
                params[k] = trial.suggest_int(k, v[0], v[1], log=log)
            else:  # float型のとき
                params[k] = trial.suggest_float(k, v[0], v[1], log=log)
        params.update(self.not_opt_params)  # 最適化対象以外のパラメータも追加
        # XGBoostのモデル作成
        estimator = self.estimator
        estimator.set_params(**params)
        
        # 全データ or 学習データ or テストデータをeval_setに入力して自作メソッドでクロスバリデーション
        scores = cross_val_score_eval_set(self.eval_set_selection, estimator, self.X, self.y, cv=self.cv, groups=self.cv_group,
                                          scoring=self.scoring, fit_params=self.fit_params, n_jobs=None)
        val = scores.mean()
        
        return val

class LGBMClassifierTuning(ParamTuning):
    """
    Tuning class for LGBMClassifier

    See ``tune_easy.param_tuning.ParamTuning`` to see API Reference of all methods
    """

    # 共通定数
    _SEED = 42  # デフォルト乱数シード
    _CV_NUM = 5  # 最適化時のクロスバリデーションのデフォルト分割数
    
    # 学習器のインスタンス (LightGBM)
    ESTIMATOR = LGBMClassifier()
    # 学習時のパラメータのデフォルト値
    FIT_PARAMS = {'verbose': 0,  # 学習中のコマンドライン出力
                  'early_stopping_rounds': 10,  # 学習時、評価指標がこの回数連続で改善しなくなった時点でストップ
                  'eval_metric': 'binary_logloss'  # early_stopping_roundsの評価指標
                  }
    # 最適化で最大化するデフォルト評価指標('neg_log_loss', 'roc_auc', 'roc_auc_ovr'など)
    _SCORING = 'neg_log_loss'

    # 最適化対象外パラメータ
    NOT_OPT_PARAMS = {'objective': None,  # 最小化させるべき損失関数
                      'random_state': _SEED,  # 乱数シード
                      'boosting_type': 'gbdt',  # boosting_type
                      'n_estimators': 10000  # 最大学習サイクル数（評価指標がearly_stopping_rounds連続で改善しなければ打ち切り）
                      }

    # グリッドサーチ用パラメータ
    CV_PARAMS_GRID = {'reg_alpha': [0.0001, 0.003, 0.1],
                      'reg_lambda': [0.0001, 0.1],
                      'num_leaves': [2, 10, 50],
                      'colsample_bytree': [0.4, 1.0],
                      'subsample': [0.4, 1.0],
                      'subsample_freq': [0, 7],
                      'min_child_samples': [2, 10, 50]
                      }

    # ランダムサーチ用パラメータ
    N_ITER_RANDOM = 400  # ランダムサーチの試行数
    CV_PARAMS_RANDOM = {'reg_alpha': [0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1],
                        'reg_lambda': [0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1],
                        'num_leaves': [2, 8, 14, 20, 26, 32, 38, 44, 50],
                        'colsample_bytree': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        'subsample': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        'subsample_freq': [0, 1, 2, 3, 4, 5, 6, 7],
                        'min_child_samples': [0, 2, 8, 14, 20, 26, 32, 38, 44, 50]
                        }

    # ベイズ最適化用パラメータ
    N_ITER_BAYES = 60  # ベイズ最適化の試行数
    INIT_POINTS = 10  # 初期観測点の個数(ランダムな探索を何回行うか)
    _ACQ = 'ei'  # 獲得関数(https://ohke.hateblo.jp/entry/2018/08/04/230000)
    N_ITER_OPTUNA = 200  # Optunaの試行数
    BAYES_PARAMS = {'reg_alpha': (0.0001, 0.1),
                    'reg_lambda': (0.0001, 0.1),
                    'num_leaves': (2, 50),
                    'colsample_bytree': (0.4, 1.0),
                    'subsample': (0.4, 1.0),
                    'subsample_freq': (0, 7),
                    'min_child_samples': (0, 50)
                    }
    INT_PARAMS = ['num_leaves', 'subsample_freq', 'min_child_samples']  # 整数型のパラメータのリスト(ベイズ最適化時は都度int型変換する)

    # 範囲選択検証曲線用パラメータ範囲
    VALIDATION_CURVE_PARAMS = {'reg_alpha': [0, 0.0001, 0.001, 0.003, 0.01, 0.03, 0.1, 1, 10],
                               'reg_lambda': [0, 0.0001, 0.001, 0.003, 0.01, 0.03, 0.1, 1, 10],
                               'num_leaves': [2, 4, 8, 16, 32, 64, 96, 128, 192, 256],
                               'colsample_bytree': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                               'subsample': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                               'subsample_freq': [0, 1, 2, 3, 4, 5, 6, 7],
                               'min_child_samples': [0, 2, 5, 10, 20, 30, 50, 70, 100]
                               }
    # 検証曲線表示等で使用するパラメータのスケール('linear', 'log')
    PARAM_SCALES = {'reg_alpha': 'log',
                    'reg_lambda': 'log',
                    'num_leaves': 'linear',
                    'colsample_bytree': 'linear',
                    'subsample': 'linear',
                    'subsample_freq': 'linear',
                    'min_child_samples': 'linear'
                    }

    def _train_param_generation(self, estimator, src_fit_params):
        """
        入力データから学習時パラメータの生成 (eval_setおよびクラス数に応じたeval_metricの修正)
        
        Parameters
        ----------
        src_fit_params : Dict
            処理前の学習時パラメータ
        """

        # fit_paramsにeval_metricが入力されており、eval_setが入力されていないときの処理
        fit_params, self.eval_set_selection = init_eval_set(
                self.eval_set_selection, src_fit_params, self.X, self.y)

        # fit_paramsにeval_metricが設定されているときのみ以下の処理を実施
        if 'eval_metric' in fit_params and fit_params['eval_metric'] is not None:
            # 2クラス分類のときeval_metricはbinary_logloss or binary_errorを、多クラス分類のときmulti_logloss or multi_errorを入力
            unique_labels = np.unique(self.y)
            if len(unique_labels) == 2:
                if fit_params['eval_metric'] in ['multi_logloss', 'multi_error']:
                    print('Labels are binary, but "eval_metric" is multiple, so "eval_metric" is set to "binary_logloss"')
                    fit_params['eval_metric'] = 'binary_logloss'
            else:
                if fit_params['eval_metric'] in ['binary_logloss', 'binary_error']:
                    print('Labels are multiple, but "eval_metric" is binary, so "eval_metric" is set to "multi_logloss"')
                    fit_params['eval_metric'] = 'multi_logloss'

        return fit_params

    def _bayes_evaluate(self, **kwargs):
        """
         ベイズ最適化時の評価指標算出メソッド
        """
        # 最適化対象のパラメータ
        params = kwargs
        params = self._pow10_conversion(params, self.param_scales)  # 対数パラメータは10のべき乗に変換
        params = self._int_conversion(params, self.int_params)  # 整数パラメータはint型に変換
        params.update(self.not_opt_params)  # 最適化対象以外のパラメータも追加
        # XGBoostのモデル作成
        estimator = self.estimator
        estimator.set_params(**params)

        # 全データ or 学習データ or テストデータをeval_setに入力して自作メソッドでクロスバリデーション
        scores = cross_val_score_eval_set(self.eval_set_selection, estimator, self.X, self.y, cv=self.cv, groups=self.cv_group,
                                          scoring=self.scoring, fit_params=self.fit_params, n_jobs=None)
        val = scores.mean()
        # 所要時間測定
        self._elapsed_times.append(time.time() - self._start_time)

        return val

    def _optuna_evaluate(self, trial):
        """
        Optuna最適化時の評価指標算出メソッド
        """
        # パラメータ格納
        params = {}
        for k, v in self.tuning_params.items():
            log = True if self.param_scales[k] == 'log' else False  # 変数のスケールを指定（対数スケールならTrue）
            if k in self.int_params:  # int型のとき
                params[k] = trial.suggest_int(k, v[0], v[1], log=log)
            else:  # float型のとき
                params[k] = trial.suggest_float(k, v[0], v[1], log=log)
        params.update(self.not_opt_params)  # 最適化対象以外のパラメータも追加
        # XGBoostのモデル作成
        estimator = self.estimator
        estimator.set_params(**params)
        
        # 全データ or 学習データ or テストデータをeval_setに入力して自作メソッドでクロスバリデーション
        scores = cross_val_score_eval_set(self.eval_set_selection, estimator, self.X, self.y, cv=self.cv, groups=self.cv_group,
                                          scoring=self.scoring, fit_params=self.fit_params, n_jobs=None)
        val = scores.mean()
        
        return val

    def _not_opt_param_generation(self, src_not_opt_params, seed, scoring):
        """
        チューニング対象外パラメータの生成(seed追加＆)
        通常はrandom_state追加のみだが、必要であれば継承先でオーバーライド

        Parameters
        ----------
        src_not_opt_params : Dict
            処理前のチューニング対象外パラメータ
        seed : int
            乱数シード
        scoring : str
            最適化で最大化する評価指標
        """
        # 2クラス分類のときobjectiveはbinaryを、多クラス分類のときmulticlassを入力
        unique_labels = np.unique(self.y)
        if len(unique_labels) == 2:
            if 'objective' in src_not_opt_params and src_not_opt_params['objective'] in ['multiclass', 'softmax', 'multiclassova', 'multiclass_ova', 'ova', 'ovr']:
                print('Labels are binary, but "objective" is multiple, so "objective" is set to "binary"')
                src_not_opt_params['objective'] = 'binary'
        else:
            if 'objective' in src_not_opt_params and src_not_opt_params['objective'] in ['binary']:
                print('Labels are multiple, but "objective" is binary, so "objective" is set to "multiclass"')
                src_not_opt_params['objective'] = 'multiclass'

        # 乱数シードをnot_opt_paramsのrandom_state引数に追加
        if 'random_state' in src_not_opt_params:
            src_not_opt_params['random_state'] = seed
        return src_not_opt_params