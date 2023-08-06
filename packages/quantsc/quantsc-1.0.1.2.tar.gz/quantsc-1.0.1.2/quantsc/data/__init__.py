# Allows user to call data.random.func instead of data.__random.func
# We need this since random is a default package in python and there's
# no way to work around that other than changing the source code of import

# add . before rand.py to let init know we are import a .py file instead of a module
from .data import *
#from data import __random