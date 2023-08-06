from setuptools import setup

setup(
    name='quantsc',
    version='1.0.1.2',
    packages=['quantsc', 'quantsc.core', 'quantsc.data', 'quantsc.data.__random'],
    url='https://quantsc.org/',
    license='MIT',
    author='Yuanhao Lu, Jonathan Qin, Aditya Prasad ',
    author_email='terryl@usc.edu',
    description='A Quantitative Finance Library',
    install_requires=[
       'setuptools',
       'pandas',
        'numpy',
        'yfinance',
        'statsmodels==0.13.2',
        'scipy',
        'matplotlib',
        'plotly',
        'python-dateutil',
        'yahoo_fin'
    ]
)
