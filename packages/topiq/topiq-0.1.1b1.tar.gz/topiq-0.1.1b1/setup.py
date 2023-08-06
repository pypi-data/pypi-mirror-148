from setuptools import setup, find_packages, Extension

with open('README.rst') as readme:
    __doc__ = readme.read()


# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ('*.py', '*.pyc', '*$py.class', '*~', '.*', '*.bak', '*.orig')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')


# Dynamically calculate the version based on topiq.VERSION.
version = __import__('topiq').get_version()

setup(
    name='topiq',
    version=version,
    description='Lightweigt embedded topiqs (based on kafka ideas)',
    long_description=__doc__,
    license='Apache 2.0',
    author='Vanya Usalko',
    author_email='iusalko@eu.spb.ru',
    url='https://github.com/usalko/topiq',
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
