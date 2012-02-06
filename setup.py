from distutils.core import setup

long_description = """
i3-py is a Python module for communicating with i3 window manager.
"""

setup(
    name='i3-py',
    description='Python module for communicating with i3 window manager',
    long_description=long_description,
    author='Jure Ziberna',
    author_email='j.ziberna@gmail.com',
    url='https://github.com/jzib/i3-py',
    version='0.2.7',
    license='GNU GPL 3',
    py_modules=['i3']
)
