from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import normalize
import numpy as np
import scipy.sparse as sp


class TfdcfTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, use_product=False, norm='l2', relative=True, sublinear_tf=False, binary=False, exclude=None):
        assert norm in [None, 'l1', 'l2']
        if exclude is None:
            exclude = []

        self.use_product = use_product
        self.norm = norm
        self.relative = relative
        self.sublinear_tf = sublinear_tf
        self.binary = binary
        self.exclude = exclude
        self._dcf_diag = None

    def fit(self, X, y):
        if not sp.issparse(X):
            X = sp.csc_matrix(X)

        n_samples, n_features = X.shape
        y_array = np.array(y)
        available_classes = set(y_array)

        def term_frequencies_for_class(selected_class):
            assert selected_class in available_classes, 'Class "%s" is not available' % selected_class
            class_indexes, = np.where(y_array == selected_class)
            frequencies = X[class_indexes, :]

            if self.binary:
                frequencies = frequencies.sign()
            if self.relative:
                average_per_class = float(len(y))/len(available_classes)
                frequencies = frequencies.multiply(average_per_class/len(class_indexes))

            return frequencies.sum(axis=0)

        freqs_for_classes = np.concatenate([term_frequencies_for_class(c) for c in available_classes if c not in self.exclude], axis=0)

        if self.use_product:
            dcf = 1.0 / np.product(1 + np.log(1 + freqs_for_classes), axis=0)
        else:
            dcf = 1.0 / (1 + np.sum(np.log(1 + freqs_for_classes), axis=0))

        self._dcf_diag = sp.spdiags(dcf, diags=0, m=n_features, n=n_features)

        return self

    def transform(self, X, copy=True):
        assert self._dcf_diag is not None, 'dcf vector is not fitted'

        if hasattr(X, 'dtype') and np.issubdtype(X.dtype, np.float):
            # preserve float family dtype
            X = sp.csr_matrix(X, copy=copy)
        else:
            # convert counts or binary occurrences to floats
            X = sp.csr_matrix(X, dtype=np.float64, copy=copy)

        n_samples, n_features = X.shape

        if self.sublinear_tf:
            np.log(X.data, X.data)
            X.data += 1

        expected_n_features = self._dcf_diag.shape[0]
        if n_features != expected_n_features:
            raise ValueError("Input has n_features=%d while the model"
                             " has been trained with n_features=%d" % (
                                 n_features, expected_n_features))
        # *= doesn't work
        X = X * self._dcf_diag
        if self.norm is not None:
            X = normalize(X, norm=self.norm, copy=False)

        return X

    @property
    def dcf_(self):
        if self._dcf_diag is not None:
            return np.ravel(self._dcf_diag.sum(axis=0))
        else:
            return None


