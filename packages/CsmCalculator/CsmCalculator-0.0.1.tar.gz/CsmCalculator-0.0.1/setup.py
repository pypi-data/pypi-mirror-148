from setuptools import setup, find_packages

classifiers = [ 
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='CsmCalculator',
    version='0.0.1',
    description='Simple Calculator',
    long_description=open('READMe.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Chiransh Singh Mehra',
    author_email='c.s.m6717@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)