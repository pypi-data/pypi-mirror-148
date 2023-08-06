# 必须要安装hyperopt
from hyperopt import hp, tpe, STATUS_OK, Trials, fmin
import numpy as np

def searching_fn(params, point, transformer):
    point = np.array(point)
    outputted_point = transformer.transform(np.array(params).reshape(1, -1)).reshape(-1, )[:point.shape[0]]
    error = outputted_point - point
    error = (error**2).sum()
    return error, outputted_point

def default_early_stop_fn(criterion=0.00001):
    def early_stop_fn(trials, *args, **wargs):
        best_loss = trials.best_trial["result"]["loss"]
        if best_loss < criterion:
            return True, dict(loss=trials.losses()[-1])
        else:
            return False, dict(loss=trials.losses()[-1])
    return early_stop_fn

# 让我们制定一个装饰函数来检测hpopt的参数是否符合规范
def check_hpopt_params(func):
    def wrapper(*args, **kargs):
        """
        args[0] - feature_ranges
        首先检测，是否为dict
        再检测dict内的值是否为list
        最后检测是否满足：1、list长度为2且均为float，此时对为上下限情况；2、list内为int元素且非空

        args[1] - target_point
        检测是否是二维点
        检测二维点内的数字是否是int或者float

        args[2] - transformer
        检测是否有transform方法
        """
        if not isinstance(args[0], dict):
            raise Exception(f"feature_ranges should be dict, not {type(args[0])}")
        for value in args[0].values():
            if not isinstance(value, list):
                raise Exception(f"range in feature_ranges should be list, not {type(value)}")
            for v in value:
                if not isinstance(v, (int, float, )):
                    raise Exception(f"range element should be float or int, not {type(v)}")
            if isinstance(value[0], float):
                if len(value) != 2:
                    raise Exception(f"if range element is float, range length should equal 2, not {len(value)}")
            if isinstance(value[0], int):
                if len(value) == 0:
                    raise Exception(f"range length should > 0.")

        # 判断args[1]，也就是target_point是否一个二维点或者三维点，且点是int或float
        #if len(args[1]) != 2 and len(args[1]) != 3:
        #    raise Exception(f"points length should equal 2 or 3")
        for tmp in args[1]:
            if not isinstance(tmp, (int, float, )):
                raise Exception(f"point element should be float or int, not {type(tmp)}")

        # 判断args[2]，也就是transformer是否有方法transformer
        if not "transform" in dir(args[2]):
            raise Exception("transformer should have member function 'transform'")

        f = func(*args, **kargs)
        return f
    return wrapper

@check_hpopt_params
def hpopt(feature_ranges, target_point, transformer, iteration, verbose, early_stop_fn):
    """

    feature_ranges包含的是特征们的上下限或者多个选择
    上下限的情况，则传入[start, end]，此时约定start与end均为float类型
    多个选择的情况，则传入[choice1, choice2, ...]，此时约定它们均为int类型

    feature_ranges自身为一个字典
    feature_ranges = dict(
        X1 = list(start, end),
        X2 = list(start, end),
        X3 = list(choice1, choice2)
    )

    target_point是一个二维点，比如[3.14, 1.45]

    transformer是一个拥有transform方法的对象，负责把feature_ranges内生成的点转变成二维点

    """

    # 在feature_ranges中迭代，制作hpopt所需要的space
    hpspace = []
    for fname, frange in feature_ranges.items():
        if isinstance(frange[0], float):
            hpobj = hp.uniform(fname, frange[0], frange[1])
        elif isinstance(frange[0], int):
            hpobj = hp.choice(fname, frange)
        hpspace.append(hpobj)

    def f(params):
        error = searching_fn(params, target_point, transformer)
        return {'loss': error[0], 'status': STATUS_OK}

    trials = Trials()
    best = fmin(fn=f, space=hpspace, algo=tpe.suggest, max_evals=iteration, verbose=verbose, trials=trials, early_stop_fn=early_stop_fn)

    best = np.array([ i for i in best.values()]).reshape(1, -1)

    return best


def scipy_minimizer(x, *args):
    transformer = args[1]
    t = args[0]
    print(x)
    x = transformer.transform(x.reshape(1, -1))[0, :len(t)]
    return ((x - t) ** 2).sum() ** 0.5

from scipy.optimize import minimize, Bounds
@check_hpopt_params
def scipy_minimize(feature_ranges, target_point, transformer, iteration, verbose, criterion):
    mins = []
    maxs = []
    fnames = []
    means = []
    for i,j in feature_ranges.items():
        fnames.append(i)
        mins.append(j[0])
        maxs.append(j[1])
        means.append(np.random.uniform(j[0], j[1]))
    bounds = Bounds(mins, maxs)
    res = minimize(scipy_minimizer, means, 
                   bounds=bounds, 
                   tol=criterion,
                   options={"verbose": int(verbose), 'maxiter': iteration,},
                   args=(target_point, transformer, ), 
                   method="trust-constr")
    return res.x.reshape(1, -1)