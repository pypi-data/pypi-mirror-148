from typing import Dict
import pandas as pd
from fake_dataset.columns import Column

__all__ = [
    "DataGenerator"
]
class DataGenerator():

    def __init__(self, **columns: Dict[str, Column]):
        for c_name, c_type in columns.items():
            setattr(self, c_name, c_type)

    def sample(self, n_samples):
        out = {}
        for attr in filter(lambda x: issubclass(type(getattr(self, x)), Column), dir(self)):
            out[attr] = getattr(self, attr).sample(n_samples)
        return pd.DataFrame(out)