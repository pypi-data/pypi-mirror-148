from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'devyl',
    version = '0.0.6',
    description = 'Metrics evaluation for binary classification model',
    long_description = open('README.txt').read(),
    url=  'https://github.com/devyratnasari/devyl',
    author= 'Devy Ratnasari',
    author_email= 'imthedevyl@gmail.com',
    license= 'MIT',
    classifiers= classifiers,
    keywords= 'metrics',
    packages= find_packages(),
    install_requires = [
        'scikit-learn',
        'matplotlib',
        'pandas'
    ]
)