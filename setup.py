from distutils.core import setup

try:
    with open('README.rst') as file:
            long_description = file.read()
except IOError:
    long_description = "a module to display progress bars in terminals"

setup(
    name='progress_bar',
    version='5.0',
    license='Apache License v2',
    author='Florian Leitner',
    author_email='florian.leitner@gmail.com',
    url='https://github.com/fnl/progress_bar',
    description='A progress bar for command line tools.',
    long_description=long_description,
    py_modules=['progress_bar'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
)
