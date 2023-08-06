from pandas import DataFrame
import numpy as np
from .algorithms import hpopt, default_early_stop_fn, scipy_minimize

METHODS = ["hpopt", "scipy_minimize"]

# 考虑输入的内容：
# 1、变量范围
# 2、目标点
# 3、搜索方法选择？

class ReverseProjection(object):
    def __init__(self, 
                 feature_ranges=None, 
                 feature_values=None, 
                 transformer=None,
                 method="scipy_minimize",
                 iteration=1000,
                 criterion=0.001, 
                 verbose=False,
                 ):
        """
        feature_ranges 用于定义特征的范围
        期望格式:
        ranges = dict(
          x1 = [bottom, top],
          x2 = [choice1, choice2, ...]
        )

        feature_values 是自变量数据集
        如果feature_ranges没有定义的话,则应当从feature_values中生成
        因此2个参数不应同时为0
        feature_values应当为ndarray

        method 用于选择优化方法

        iteration 用于决定优化的轮数

        criterion 用于决定阈值，若达到了预期阈值，则可以提前结束

        verbose 用于决定是否开启消息打印，默认关闭

        """

        if not isinstance(feature_values, (np.ndarray, DataFrame)) and not None:
            raise Exception(f"feature_values should be ndarray or DataFrame, not {type(feature_values)}")
        # feature_ranges 与 feature_values不能同时为0
        if feature_ranges is None and feature_values is None:
            raise Exception("feature_ranges and feature_values should not be both None.")
        # 检查method是否正确
        if method not in METHODS:
            raise Exception(f"method should be one of {METHODS}")

        # 检查transformer
        if transformer is None:
            raise Exception("transformer should be given.")

        # 如果feature_ranges没给定义，那么从feature_values里生成
        if feature_ranges is None:
            feature_ranges = dict()
            if isinstance(feature_values, DataFrame):
                feature_names = feature_values.columns.tolist()
                feature_values = feature_values.values
            elif isinstance(feature_values, np.ndarray):
                feature_names = [ "X"+str(i) for i in range(feature_values.shape[1])]
            for i in range(feature_values.shape[1]):
                fvalues = feature_values[:, i]
                feature_ranges[feature_names[i]] = [fvalues.min(), fvalues.max()]
        self.feature_ranges = feature_ranges
        self.method = method
        self.verbose = verbose
        self.iteration = iteration
        self.criterion = criterion
        self.transformer = transformer
        self.feature_names = feature_names

    def search(self, target_point):
        if self.method == "hpopt":
            result = hpopt(self.feature_ranges, 
                           target_point, 
                           self.transformer, 
                           self.iteration, 
                           self.verbose, 
                           default_early_stop_fn(self.criterion))
        elif self.method == "scipy_minimize":
            result = scipy_minimize(self.feature_ranges,
                                    target_point,
                                    self.transformer,
                                    self.iteration,
                                    self.verbose,
                                    self.criterion)
        return dict(
            points=self.transformer.transform(result)[0, :len(target_point)].tolist(),
            features=result.tolist()[0],
            feature_names=self.feature_names
            )




