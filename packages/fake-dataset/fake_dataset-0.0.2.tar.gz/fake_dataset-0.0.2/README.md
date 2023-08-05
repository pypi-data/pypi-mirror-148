# Fake Dataset


[![image](https://img.shields.io/pypi/v/fake_dataset.svg)](https://pypi.python.org/pypi/fake_dataset)


**Toolkit for generating fake datasets.**


-   Free software: MIT license
-   Documentation: https://matheusfsa.github.io/fake_dataset

## How to Install

```bash
pip install fake-dataset
```

## Usage


    >>> from fake_dataset import columns, generators

    >>> data_gen = generators.DataGenerator(
    ...    vehicle=columns.CategoricalRandomColumn(categories=["car", "bus", "bicycle"], missing_rate=(0.2, 0.5), na_value="NA"),
    ...    year=columns.IntegerRandomColumn(values_range=(1950, 2010), missing_rate=(0.1, 0.2)),
    ...    value=columns.FloatRandomColumn(values_range=(10e4, 10e5), missing_rate=(0.0, 0.0)),
    ...    )

    >>> data_gen.sample(3)
               value vehicle  year
    0  823994.355388     car  2002
    1  903007.903927      NA  1952
    2  435372.320886      NA  None


## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.
