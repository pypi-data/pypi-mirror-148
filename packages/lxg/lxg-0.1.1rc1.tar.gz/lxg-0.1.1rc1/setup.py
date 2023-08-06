from setuptools import setup, find_packages, Extension

with open('README.rst') as readme:
    __doc__ = readme.read()


# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ('*.py', '*.pyc', '*$py.class', '*~', '.*', '*.bak', '*.orig')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')


# Dynamically calculate the version based on lxg.VERSION.
version = __import__('lxg').get_version()

setup(
    name='lxg',
    version=version,
    description='Simple interface for quick append logger functionality to the class',
    long_description=__doc__,
    license='BSD',
    author='Vanya Usalko',
    author_email='iusalko@eu.spb.ru',
    url='https://github.com/usalko/lxg',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
    ],
    zip_safe=False,
    install_requires=[],
)
