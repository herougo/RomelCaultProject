import numpy as np
import warnings

def _concat(a, b):
    assert type(a) == type(b), (type(a), type(b))
    if isinstance(a, tuple):
        return tuple(_concat(a_val, b_val) for a_val, b_val in zip(a, b))
    elif isinstance(a, list):
        return [_concat(a_val, b_val) for a_val, b_val in zip(a, b)]
    elif isinstance(a, np.ndarray):
        return np.concatenate([a, b], axis=0)  # axis=0 not necessary
    else:
        raise BaseException(f'Unhandled type {type(a)}')


class DataSet:
    """
    Manages datasets of numpy arrays x, y, and w

    Future Improvements:
    - slicing returns a DataSet
    - rename as DataArrayTuple
    - handle tuple of lists of arrays
    """

    def __init__(self, x, y, w, one_hot=True, max_nbytes=100_000_000):
        self._x = x
        self._y = y
        self._w = w
        self._one_hot = one_hot
        self._max_nbytes = max_nbytes

    def __getitem__(self, item):
        x = self._x[item]
        y = self._y[item]
        w = self._w[item]
        return x, y, w

    def __len__(self):
        x = self._x
        if isinstance(x, list):
            x = x[0]
        return len(x)

    def __iter__(self):
        for x, y, w in zip(*self.xyw):
            yield x, y, w

    def shuffle(self):
        permutation = np.random.permutation(len(self))
        self._x, self._y, self._w = self._shuffle_helper(self.xyw, permutation)

    def _shuffle_helper(self, to_shuffle, permutation):
        if isinstance(to_shuffle, tuple):
            return tuple(self._shuffle_helper(elem, permutation) for elem in to_shuffle)
        elif isinstance(to_shuffle, list):
            return [self._shuffle_helper(elem, permutation) for elem in to_shuffle]
        elif isinstance(to_shuffle, np.ndarray):
            return to_shuffle[permutation]
        else:
            raise BaseException(f'Unhandled type {to_shuffle}')

    def append_dataset(self, other):
        if isinstance(other, DataSet):
            self._x, self._y, self._w = _concat(self.xyw, other.xyw)
        else:
            raise BaseException(f'Unhandled type {type(other)}')

    def append_point(self, other):
        import warnings
        warnings.warn('This may be wrong since Dataset shape has n_examples first')
        if isinstance(other, (DataStream, tuple)):
            self._x, self._y, self._w = _concat(self.xyw, other)
        else:
            raise BaseException(f'Unhandled type {type(other)}')

    @property
    def xyw(self):
        return self._x, self._y, self._w

    @property
    def xy(self):
        return self._x, self._y

    def copy(self):
        import copy
        return copy.deepcopy(self)

    def __str__(self):
        return self.xyw.__str__()

    def __repr__(self):
        return self.xyw.__repr__()

    @property
    def nbytes(self):
        return self._x.nbytes + self._y.nbytes + self._w.nbytes

    def __add__(self, other):
        result = self.copy()
        result.append_dataset(other)
        return result

    def split_by_p(self, p):
        """
        Partition the data into DataSet objects according to distribution p
        Example: p = [0.25, 0.75] means the first DataSet is the first 0.25 of the data and the
                 second DataSet is the rest of the data
        :param p: list of >= 0 floats which sum to 1
        :return: list of DataSets corresponding to splitting according to p
        """
        assert np.isclose(np.sum(p), 1)
        data_len = len(self)
        lengths = [int(data_len * frac) for frac in p]
        # missing points at the end
        lengths[-1] += data_len - sum(lengths)
        ptr = 0
        result = []
        for length in lengths:
            result.append(DataSet(*self[ptr:ptr + length]))
            ptr += length
        return result

    def split_uniformly(self, n):
        # split into alist of n roughly, equally sized DataSet objects
        return self.split_by_p([1.0 / n] * n)

    def split_by_category(self, categories):
        """
        The categories argument labels each example with an category id.
        Split self so that each DataSet corresponds to all examples with a particular category id.
        :param categories: list of >= 0 integers with length the same as self
        :return: list of DataSet objects
        """
        assert len(categories) == len(self), (len(categories), len(self))

        category_indices = dict([(category, []) for category in set(categories)])
        for i, category in enumerate(categories):
            category_indices[category].append(i)

        return [DataSet(*self[category_indices[category]]) for category in
                sorted(category_indices.keys())]

    @property
    def int_category_y(self):
        """ If the y is format is categorical output return it in its non-one-hot vector form"""
        y_values = self._y.astype(int)
        if self._one_hot:
            y_values = np.argmax(y_values, axis=1)
        return y_values

    def split_by_y(self):
        """
        Partition self into multiple DataSets based on the categorial class indicated by y
        :return: list of DataSet objects
        """
        y_values = self.int_category_y

        assert len(y_values.shape) == 1, y_values.shape
        return self.split_by_category(y_values)

    def split_tvt(self, p):
        """
        Split into train, validation, and test DataSets
        :param p: list of 3 floats (ie [train_frac, val_frac, test_frac]) which sum to 1
        :return: list of 3 DataSet objects
        """
        assert len(p) == 3, p
        return self.split_by_p(p)

    def split_tt(self, p):
        """
        Split into train and test DataSets
        :param p: list of 2 floats (ie [train_frac, test_frac]) which sum to 1
        :return: list of 2 DataSet objects
        """
        assert len(p) == 2, p
        return self.split_by_p(p)

    def split_by_index(self, index):
        """
        Given an iterable of indices, partition self into 2 DataSet objects:
        - one including examples with indices in index
        - other data
        :param index: indices of examples to include
        :return: tuple of 2 DataSet objects
        """
        out_index = list(set(range(len(self))) - set(index))
        return DataSet(*self[index]), DataSet(*self[out_index])

    def sample_index(self, n=None, frac=None, p=None):
        """
        Sample_Problem data point indices without replacements
        :param n: number of examples to sample
        :param frac: fraction of examples in self to sample
        :param p: distribution over all examples when sampling
        :return: 1-dimensional numpy array of sampled indices
        """
        if frac is not None:
            n = int(len(self) * frac)
        return np.random.choice(list(range(len(self))), size=n, p=p, replace=False)

    def sample(self, n=None, frac=None, p=None):
        # sample data points without replacement
        index = self.sample_index(n=n, frac=frac, p=p)
        return DataSet(*self[index])

    def filter_by_y(self, y_filter):
        """
        Return a DataSet with examples filtered by whether the y value is in argument y
        :param y_filter: integer or list of integers
        :return: DataSet of filtered results
        """
        if not isinstance(y_filter, list):
            y_filter = [y_filter]
        y_values = self.int_category_y
        mask = np.isin(y_values, y_filter)
        return DataSet(*self[mask])

    def closest_points(self, test, metric='euclidean', n=None, frac=1):
        """
        Get n closest points or the fraction of the data that is closest to the
        points in test with respect to x

        :returns: 3 lists
        """
        from sklearn.neighbors import NearestNeighbors
        import warnings

        if metric is None:
            warnings.warn("'metric' shouldn't be None. Correcting to be 'euclidean'.")
            metric = 'euclidean'

        if n is None:
            n = int(len(test) * frac)

        nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree', metric=metric).fit(self._x)
        distances, labels = nbrs.kneighbors(test._x)

        indices = np.array(list(range(len(test)))).reshape((-1, 1))
        concat = np.concatenate([distances, labels, indices], axis=1)

        # Don't use np.sort! It doesn't preserve rows.
        concat = concat[concat[:, 0].argsort()]

        distances = list(concat[:n, 0].reshape((-1,)))
        labels = list(concat[:n, 1].reshape((-1,)).astype(int))
        indices = list(concat[:n, 2].reshape((-1,)).astype(int))

        return indices, distances, labels

    def class_count(self):
        """
        :return: dictionary mapping classes (as integers) to the occurrence count in self
        """
        categories = self.int_category_y
        from collections import Counter
        return dict(Counter(categories))

    @classmethod
    def from_stream(self, stream, max_len=100_000):
        result_len = stream_len(stream, max_len)
        assert result_len > 0
        batcher = Batcher(stream, result_len)
        x, y, w = list(islice(batcher, 1))[0]
        x, y, w = copy.deepcopy((x, y, w))
        return DataSet(x, y, w)

    def to_stream(self, shape=None):
        if shape is None:
            warnings.warn('to_stream is unstable without the shape argument')
        xyw_iter = copy.deepcopy(list(self))
        return IterDataStream(xyw_iter, shape=shape)

    @classmethod
    def from_hdf(self, file_path):
        NotImplementedError()

    def to_hdf(self, file_path):
        NotImplementedError()