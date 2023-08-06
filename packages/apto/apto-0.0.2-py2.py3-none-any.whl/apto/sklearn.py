# Author: Sergey Kolesnikov (scitator@gmail.com)
# Licence: Apache 2.0
import numpy as np
from scipy.special import expit
from sklearn.linear_model import LogisticRegression, SGDClassifier


class MultilabelLinearClassifier:
    """Extension for LogisticRegression/SGDClassifier for multi-label support."""

    def _predict_proba(self, X):
        scores = self.decision_function(X)
        expit(scores, out=scores)
        if scores.ndim == 1:
            return np.vstack([1 - scores, scores]).T
        else:
            return scores

    def predict_proba(self, X):
        return self._predict_proba(X=X)


class MultilabelLogisticRegression(LogisticRegression, MultilabelLinearClassifier):
    pass


class MultilabelSGDClassifier(SGDClassifier, MultilabelLinearClassifier):
    pass


__all__ = [
    "MultilabelLinearClassifier",
    "MultilabelLogisticRegression",
    "MultilabelSGDClassifier",
]
