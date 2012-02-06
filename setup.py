from distutils.core import setup

long_description = """
i3-py contains tools for i3 users and developers

The contents of i3-py project are:

 - i3.py, a Python module for communicating with i3-wm
 - i3-ipc, a command-line script that wraps some of i3.py's features
 - i3wsbar, a Python implementation of i3-wm workspace bar

"""

setup(
    name='i3-py',
    description='tools for i3 users and developers',
    long_description=long_description,
    author='Jure Ziberna',
    author_email='j.ziberna@gmail.com',
    url='https://github.com/jzib/i3-py',
    version='0.3.1',
    license='GNU GPL 3',
    py_modules=['i3', 'i3wsbar']
)
