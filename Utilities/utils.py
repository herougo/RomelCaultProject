import warnings
import numpy as np
import pandas as pd
import keras
import math


def get_closest_points(train, test, metric='euclidean', n=None, frac=1):
    """get n closest points or the fraction of train that is closest to the 
       points in test
      :returns: 3 lists
    """
    from sklearn.neighbors import NearestNeighbors
    import warnings

    if metric is None:
        warnings.warn("'metric' shouldn't be None. Correcting to be 'euclidean'.")
        metric = 'euclidean'

    if n is None:
        n = int(len(test) * frac)

    nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree', metric=metric).fit(train)
    distances, labels = nbrs.kneighbors(test)

    indices = np.array(list(range(len(test)))).reshape((-1, 1))
    concat = np.concatenate([distances, labels, indices], axis=1)
    
    # Don't use np.sort! It doesn't preserve rows.
    concat = concat[concat[:,0].argsort()]

    distances = list(concat[:n, 0].reshape((-1,)))
    labels = list(concat[:n, 1].reshape((-1,)).astype(int))
    indices = list(concat[:n, 2].reshape((-1,)).astype(int))

    return indices, distances, labels

def myshuffle(data):
    #warnings.warn('Use "np.random.shuffle(arr)" instead')
    warnings.warn('This does not distribute a matching shuffle across tuple elements.')
    if isinstance(data, (list, np.ndarray)):
        np.random.shuffle(data)
        # random.shuffle(l) # also works
    elif isinstance(data, tuple):
        for val in data:
            myshuffle(val)
    elif isinstance(data, pd.DataFrame):
        warnings.warn('You must assign this to the DataFrame')
        # when sampling, the indices move with the rows, so reset_index resets the index
        # to be 0, 1, 2, ... again
        return data.sample(frac=1).reset_index(drop=True)
    else:
        raise BaseException('Unseen data type {}'.format(type(data)))
        
def mysample(data, n=1, frac=None, p=None):
    #warnings.warn('Use "np.random.choice(arr, size=.., replace=False)" instead')
    # TODO: work for range & map objects, multidimensional numpy arrays
    if isinstance(data, list):
        warnings.warn('List is currently being converted to ndarray')
    if isinstance(data, (list, np.ndarray)):
        if frac is not None:
            n = int(len(data.shape) * frac)
        data = np.array(data)
        return np.random.choice(data, size=n, p=p, replace=False)
    elif isinstance(data, tuple):
        result = ()
        for val in data:
            result += (mysample(val),)
        return result
    elif isinstance(data, pd.DataFrame):
        if frac is None:
            return data.sample(n=n, replace=False) # replace=False shouldn't be needed
        else:
            return data.sample(frac=frac, replace=False)
    else:
        raise BaseException('Unseen data type {}'.format(type(data)))

def mysplit(data_and_labels, split=[0.6, 0.2, 0.2]):
    """
    Take a data set and split it according to split

    :param data_and_labels: tuple of 2 numpy arrays representing the data and labels
    :param split: list of 2 or 3 floats which sum to one
    :return: tuple of data-label tuples according to the split

    TODO: support DataStream
    """
    from sklearn.model_selection import train_test_split
    assert isinstance(data_and_labels, tuple) and len(data_and_labels) == 2
    data = data_and_labels[0]
    labels = data_and_labels[1]
    assert type(data, np.ndarray)
    assert type(labels, np.ndarray)
    x, x_test, y, y_test = train_test_split(data,labels,test_size=split[-1],train_size=(1-split[-1]))

    if len(split) == 2:
        return (x, y), (x_test, y_test)
    
    train_and_validation = split[0] + split[1]
    train = split[0]
    train_validation_ratio = train / train_and_validation
    x_train, x_cv, y_train, y_cv = train_test_split(
        x,y,test_size = 1-train_validation_ratio,train_size = train_validation_ratio)
    
    return (x_train, y_train), (x_cv, y_cv), (x_test, y_test)

def myconcat(a, b):
    # concat data batches
    assert type(a) == type(b), (type(a), type(b))
    if isinstance(a, tuple):
        return tuple(myconcat(a_val, b_val) for a_val, b_val in zip(a, b))
    elif isinstance(a, list):
        return [myconcat(a_val, b_val) for a_val, b_val in zip(a, b)]
    elif isinstance(a, np.ndarray):
        return np.concatenate([a, b], axis=0)  # axis=0 not necessary
    else:
        raise BaseException(f'Unhandled type {type(a)}')

def myshape(arr):
    """This is a more generalized version of the .shape property which can be used for
    numpy arrays, lists, tuples, and other variables which have a shape"""
    if isinstance(arr, list):
        return [myshape(val) for val in arr]
    elif isinstance(arr, tuple):
        return tuple(myshape(var) for var in arr)
    elif isinstance(arr, dict):
        return dict((k, myshape(v)) for k, v in arr.items())
    else:
        return arr.shape


def myencodelabels(arr):
    # onehot
    from sklearn.preprocessing import LabelEncoder
    return LabelEncoder().fit_transform(arr)

def myflatten(arr):
    try:
        result = []
        assert not isinstance(arr, str)
        for row in arr:
            result += myflatten(row)
        return result
    except:
        return [arr]

def myadd(x, y):
    # myadd(([1, 2], [3, 4]), ([1, 2], [3, 4]))
    assert type(x) == type(y), (x, y, type(x), type(y))
    if isinstance(x, list):
        assert len(x) == len(y), (len(x), len(y))
        return [myadd(a, b) for a, b in zip(x, y)]
    elif isinstance(x, tuple):
        assert len(x) == len(y), (len(x), len(y))
        return tuple(myadd(a, b) for a, b in zip(x, y))
    elif isinstance(x, dict):
        assert set(x.keys()) == set(y.keys()), (set(x.keys()), set(y.keys()))
        return dict((k, myadd(x[k], y[k])) for k in x.keys())
    else:
        return x + y

def myminus(x, y):
    # myadd(([1, 2], [3, 4]), ([1, 2], [3, 4]))
    assert type(x) == type(y), (x, y, type(x), type(y))
    if isinstance(x, list):
        assert len(x) == len(y), (len(x), len(y))
        return [myminus(a, b) for a, b in zip(x, y)]
    elif isinstance(x, tuple):
        assert len(x) == len(y), (len(x), len(y))
        return tuple(myminus(a, b) for a, b in zip(x, y))
    elif isinstance(x, dict):
        assert set(x.keys()) == set(y.keys()), (set(x.keys()), set(y.keys()))
        return dict((k, myminus(x[k], y[k])) for k in x.keys())
    else:
        return x - y

def mymultiply(x, y):
    # myadd(([1, 2], [3, 4]), ([1, 2], [3, 4]))
    assert type(x) == type(y), (x, y, type(x), type(y))
    if isinstance(x, list):
        assert len(x) == len(y), (len(x), len(y))
        return [myminus(a, b) for a, b in zip(x, y)]
    elif isinstance(x, tuple):
        assert len(x) == len(y), (len(x), len(y))
        return tuple(myminus(a, b) for a, b in zip(x, y))
    elif isinstance(x, dict):
        assert set(x.keys()) == set(y.keys()), (set(x.keys()), set(y.keys()))
        return dict((k, myminus(x[k], y[k])) for k in x.keys())
    else:
        return x * y

def messy_get_item(d, key):
    # MAYBE REFACTOR???????
    # - return an index path
    # - for lists maybe instead consider looking through lists of dictionaries
    if isinstance(key, list):
        return [messy_get_item(k) for k in key]
    elif isinstance(key, tuple):
        return tuple(messy_get_item(k) for k in key)
    elif isinstance(d, dict):
        if key in d.keys():
            answers = [d[key]]
            return 
        answers = []
        for k, val in d.items():
            new_result = messy_get_item(val, key)
            if new_result is not None:
                answers.append(new_result)
        if len(answers) > 0:
            if len(answers) > 1:
                warnings.warn(f'key {key} has multiple values for {d}')
            return answers[0]
    return None

def fix_keras_shape(keras_shape):
    """
    Convert shape in keras's format to the DataStream format
    :param keras_shape: a shape in the keras format (either input or output shape)
    :return: keras_shape in the DataStream format
    """
    if isinstance(keras_shape, list):
        return [fix_keras_shape(shape) for shape in keras_shape]
    elif isinstance(keras_shape, tuple):
        assert keras_shape[0] is None
        return keras_shape[1:]
    else:
        raise BaseException(f'Unrecognized type {type(model_output_shape)}')

def stream_len(data_stream, max_length=5e7):
    # return the length of a data_stream
    result = 0
    for i, point in enumerate(data_stream):
        if i == max_length:
            break
        result += 1
    return result

def fake_data(model, n=1, kind='ones'):
    input_shapes = fix_keras_shape(model.input_shape)
    output_shapes = fix_keras_shape(model.output_shape)
    if not isinstance(input_shapes, list):
        input_shapes = [input_shapes]
    if not isinstance(output_shapes, list):
        output_shapes = [output_shapes]
    x = []
    y = []
    for input_shape in input_shapes:
        x.append(np.ones((n,) + input_shape))
    for output_shape in output_shapes:
        y.append(np.ones((n,) + output_shape))
    return x, y



def to_categorical(x, n):
    # example: to_one_hot([np.array([1, 2, 3]), np.array(1)], 4) 
    if isinstance(x, list):
        return [to_categorical(val, n) for val in x]
    elif isinstance(x, tuple):
        return tuple(to_categorical(val, n) for val in x)
    elif isinstance(x, dict):
        return dict((k, to_categorical(x[k], n)) for k in x.keys())
    elif isinstance(x, np.ndarray):
        return keras.utils.np_utils.to_categorical(x, n)
    else:
        raise BaseException(f'to_one_hot unhandled type {type(x)}')

#used to apply basic mathematical functions on lists
def squareList(inputList):
    return [item ** 2 for item in inputList]

def sqrtList(inputList):
    return [math.sqrt(item) for item in inputList]

def rmsList(inputList):
    return math.sqrt(sum(squareList(inputList)) / len(inputList))

def minMaxList(inputList):
    return (max(inputList) - min(inputList))

def meanList(inputList):
    return (sum(inputList) / float(len(inputList)))

# removes the first and last fraction of a list depending on amount of divisions wanted, default is to remove 40% of list
def sliceDataSet(dataSet, amountOfDivisions=5):
    length = len(dataSet)
    start = int(length / amountOfDivisions)
    end = length - start
    slicedSet = dataSet[start:end]
    return slicedSet

# frequency domain conversion (FFT)
def fftConversion(dataSet):
    dataSetArray = np.asarray(dataSet)
    dataSetArray = dataSetArray[~np.isnan(dataSetArray)]
    freqDataSet = fft(dataSetArray)
    return freqDataSet

# allows functions to be applied on rolling windows of a Pandas dataframe
def functionOnWindow(inputList, function, corr=False, corrList=[], windowSize=200):
    if corr == True:
        return pd.Series(inputList).rolling(window=windowSize, min_periods=windowSize).corr(other=pd.Series(corrList),
                                                                                            pairwise=False).tolist()[
               windowSize:-windowSize]
    return pd.Series(inputList).rolling(min_periods=windowSize, window=windowSize).apply(func=function).values.tolist()[
           windowSize:-windowSize]