from distutils.core import setup
import py2exe
import numpy
setup(windows=[{"script":"main.py", "icon_resources": [(1, "icon.ico")] }], options={"py2exe":{"includes":["sip", "Crypto"]}})