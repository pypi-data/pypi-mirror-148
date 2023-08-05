import numpy as np
from typing import Tuple, Any, List, Union
from abc import ABC, abstractmethod

__all__ = [
    "Column",
    "ColumnWithNA",
    "FloatRandomColumn",
    "IntegerRandomColumn",
    "CategoricalRandomColumn",
    "CategoricalProportionalColumn"
]
class Column(ABC):

    @abstractmethod
    def sample(self, n_samples):
        pass

class ColumnWithNA(Column):

    def __init__(self, na_value: Any, missing_rate: Tuple[float, float] = (0.0, 0.0)):
        self._missing_rate = missing_rate
        self._na_value = na_value

    def _build_sample(self, n_samples):
        raise NotImplementedError()

    def _drop_rows(self, out):
        n_samples = len(out)
        nan_rate = self._missing_rate[0] + (np.random.random() * (self._missing_rate[1] - self._missing_rate[0]))
        n_nans = int(np.ceil(n_samples*nan_rate))
        nan_idx = np.random.choice(n_samples, n_nans, replace=False)
        out[nan_idx] = self._na_value
        return out

    def sample(self, n_samples):
        out = self._build_sample(n_samples)
        out = self._drop_rows(out)
        return out



class FloatRandomColumn(ColumnWithNA):

    def __init__(self,
                 values_range: Tuple[float, float] =(0., 1.),
                 missing_rate: Tuple[float, float] = (0.0, 0.0)):

        super().__init__(na_value=np.nan, missing_rate=missing_rate)
        self._values_range = values_range

    def _build_sample(self, n_samples: int):
        out = np.random.rand(n_samples)
        out = self._values_range[0] + (out * (self._values_range[1] - self._values_range[0]))
        return out

class IntegerRandomColumn(ColumnWithNA):

    def __init__(self,
                 values_range: Tuple[int, int] =(0, 1),
                 missing_rate: Tuple[float, float] = (0.0, 0.0)):

        super().__init__(na_value=None, missing_rate=missing_rate)
        self._values_range = values_range

    def _build_sample(self, n_samples: int):
        out = np.random.randint(self._values_range[0], high=self._values_range[1] + 1, size=n_samples)
        return out.astype("object")

class CategoricalRandomColumn(ColumnWithNA):

    def __init__(self,
                 categories: List[Any],
                 missing_rate: Tuple[float, float] = (0.0, 0.0),
                 na_value: Any = None):
        super().__init__(na_value=na_value, missing_rate=missing_rate)
        self._categories = categories

    def _build_sample(self, n_samples: int):
        out = np.random.choice(self._categories, size=n_samples)
        return out.astype("object")

class CategoricalProportionalColumn(ColumnWithNA):

    def __init__(self,
                 categories: List[Any],
                 proportions: Union[List[float], np.array],
                 missing_rate: Tuple[float, float] = (0.0, 0.0),
                 na_value: Any = None,
                 shuffle: bool = True):
        super().__init__(na_value=na_value, missing_rate=missing_rate)
        self._categories = categories
        self._proportions = proportions
        self._shuffle = shuffle

    def _build_sample(self, n_samples: int):
        out = np.hstack([np.full(int(round(prop*n_samples)), cat) for cat, prop in zip(self._categories, self._proportions)])
        if self._shuffle:
            np.random.shuffle(out)
        return out.astype("object")