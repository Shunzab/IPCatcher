import py_compile
try:
    py_compile.compile('IPCatcher.py')
except Exception as e:
    print(e)