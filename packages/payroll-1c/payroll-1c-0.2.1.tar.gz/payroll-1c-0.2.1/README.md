1C Payrolls
===========
[![PyPI](https://img.shields.io/pypi/pyversions/payroll-1c.svg)](https://pypi.org/project/payroll-1c/ "Latest version on PyPI")
[![codecov](https://codecov.io/gh/voronind/payroll-1c/branch/master/graph/badge.svg)](https://codecov.io/gh/voronind/payroll-1c "Coverage")

Parse 1C Payrolls XML file

Install
-------
```commandline
pip install payroll_1c
```

Usage
-----

```python
>>> from payroll_1c import Payroll1C
>>> payroll = Payroll1C('1C-payroll.xml')
>>> payroll = Payroll1C(fromstring='<СчетаПК>...</СчетаПК>')
>>> payroll['ДатаФормирования'] == '2022-01-01'
>>> for employee in payroll:
...    print(employee['Фамилия'])
...    print(employee['Сумма'])
```

Development
-----------
We need installed `pyenv` and `pipenv`.
```console
git clone git@github.com:odoo-ru/payroll-1c.git

cd payroll-1c
pipenv install --dev
```

Run tests:
```console
pipenv run fulltest
```
