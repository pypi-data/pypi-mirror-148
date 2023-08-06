# pyflx
-------
Python Flexible Utility Library

Command to prepare the cli

### Preparing the packages
```
python3 setup.py sdist bdist_wheel
```

This creates a `dist` directory with `.tar.gz` and `.whl` files

### Uploading to pypi repository

Install `twine` package
```
pip install twine
```

Upload the package via `dist` folder created with above step

```
twine upload dist/*
```


### TODO:
~~1. auto retry mechanism for failure cases (based on limit)
2. cron job 
3. logger~~
4. converters (time, storage, currency etc)  (not a decorator)
5. ML Decorators

Some cli operations