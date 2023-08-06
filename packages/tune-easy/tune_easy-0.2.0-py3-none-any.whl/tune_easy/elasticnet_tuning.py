from sklearn.linear_model import ElasticNet
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .param_tuning import ParamTuning

class ElasticNetTuning(ParamTuning):
    """
    Tuning class for ElasticNet

    See ``tune_easy.param_tuning.ParamTuning`` to see API Reference of all methods
    """

    # 共通定数
    _SEED = 42  # デフォルト乱数シード
    _CV_NUM = 5  # 最適化時のクロスバリデーションのデフォルト分割数
    
    # 学習器のインスタンス (標準化+SVRのパイプライン)
    ESTIMATOR = Pipeline([("scaler", StandardScaler()), ("enet", ElasticNet())])
    # 学習時のパラメータのデフォルト値
    FIT_PARAMS = {}
    # 最適化で最大化するデフォルト評価指標('r2', 'neg_mean_squared_error', 'neg_root_mean_squared_error', etc.)
    _SCORING = 'neg_root_mean_squared_error'

    # 最適化対象外パラメータ
    NOT_OPT_PARAMS = {}

    # グリッドサーチ用パラメータ
    CV_PARAMS_GRID = {'alpha':[0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10],  # L1,L2正則化項の合計値（小さいほど過学習、大きいほど未学習寄り）
                      'l1_ratio': [0, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 0.9, 0.95, 0.99, 1]  # L1正則化項の比率（小さいほどRidge回帰、大きいほどLasso回帰寄り）
                      }

    # ランダムサーチ用パラメータ
    N_ITER_RANDOM = 250  # ランダムサーチの試行数
    CV_PARAMS_RANDOM = {'alpha':[0.0001, 0.0002, 0.0004, 0.0007, 0.001, 0.002, 0.004, 0.007, 0.01, 0.02, 0.04, 0.07, 0.1, 0.2, 0.4, 0.7, 1, 2, 4, 7, 10],  # L1,L2正則化項の合計値（小さいほど過学習、大きいほど未学習寄り）
                        'l1_ratio': [0, 0.0001, 0.0002, 0.0004, 0.0007, 0.001, 0.002, 0.004, 0.007, 0.01, 0.02, 0.04, 0.07, 0.1, 0.2, 0.4, 0.5, 0.6, 0.8, 0.9, 0.93, 0.96, 0.98, 0.99, 1]  # L1正則化項の比率（小さいほどRidge回帰、大きいほどLasso回帰寄り）
                        }

    # ベイズ最適化用パラメータ
    N_ITER_BAYES = 45  # BayesianOptimizationの試行数
    INIT_POINTS = 10  # BayesianOptimizationの初期観測点の個数(ランダムな探索を何回行うか)
    _ACQ = 'ei'  # BayesianOptimizationの獲得関数(https://ohke.hateblo.jp/entry/2018/08/04/230000)
    N_ITER_OPTUNA = 70  # Optunaの試行数
    BAYES_PARAMS = {'alpha': (0.0001, 10),
                    'l1_ratio': (0, 1)
                    }
    INT_PARAMS = []

    # 範囲選択検証曲線用パラメータ範囲
    VALIDATION_CURVE_PARAMS = {'alpha': [0, 0.00001, 0.0001, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 10, 100],
                               'l1_ratio': [0, 0.00001, 0.0001, 0.001, 0.01, 0.03, 0.1, 0.3, 0.5, 0.7, 0.9, 0.97, 0.99, 1]
                               }
    # 検証曲線表示等で使用するパラメータのスケール('linear', 'log')
    PARAM_SCALES = {'alpha': 'log',
                    'l1_ratio': 'linear'
                    }

    def _train_param_generation(self, estimator, src_fit_params):
        """
        入力データから学習時パラメータの生成 (eval_set)
        
        Parameters
        ----------
        src_fit_params : Dict
            処理前の学習時パラメータ
        """
        return src_fit_params