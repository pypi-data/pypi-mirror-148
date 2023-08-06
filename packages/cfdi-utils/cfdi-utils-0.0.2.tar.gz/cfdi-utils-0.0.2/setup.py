from setuptools import setup, find_packages

classiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name= "cfdi-utils",
    version= "0.0.2",
    description= "Utilities to work with CFDI",
    long_description= open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author= "Arturo Castillo",
    author_email= "arturguay@gmail.com",
    url= "",
    license= "MIT",
    packages= find_packages(),
    classifiers= classiers,
    keywords= "cfdi",
    install_requires= ['lxml', 'M2Crypto', 'pycryptodomex'],
)
