from setuptools import setup, find_packages


setup(
    name='pyflxy',
    version='0.4',
    license='MIT',
    author="Sourav Suresh, Dilip Debsingha",
    author_email='souravs0506@gmail.com, ddsinha.cob@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/souravsuresh/pyflx.git',
    keywords='pyflxy',
    install_requires=[
        'requests',
        'schedule'
    ],
)