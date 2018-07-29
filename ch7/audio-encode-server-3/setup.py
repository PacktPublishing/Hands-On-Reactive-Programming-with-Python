import os, sys
try:
    from setuptools import setup, find_packages
    use_setuptools = True
except ImportError:
    from distutils.core import setup
    use_setuptools = False

try:
    with open('README.rst', 'rt') as readme:
        description = '\n' + readme.read()
except IOError:
    # maybe running setup.py from some other dir
    description = ''

python_requires='>=3.5'
install_requires = [
    'rx>=1.6',
    'cyclotron-aio>=0.4',
    'cyclotron-std>=0.3',
    'sox>=1.3',
    'boto3>=1.7',
]

setup(
    name="audio-encode-server",
    version='0.3.0',
    url='https://github.com/PacktPublishing/Hands-On-Reactive-Programming-with-Python.git',
    license='MIT',
    description="An example audio encoder",
    long_description=description,
    author='Romain Picard',
    author_email='romain.picard@oakbits.com',
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    scripts=[
        'script/audio-encode-server',
    ],
)
