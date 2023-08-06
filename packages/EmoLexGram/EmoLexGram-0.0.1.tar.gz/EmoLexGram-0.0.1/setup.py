"""Setup for the EmoLexGram package."""


import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Moksha Thisarani",
    author_email="moksha.util@gmail.com",
    name='EmoLexGram',
    license="MIT",
    description='EmoLexGram is a python package for text-based emotion classification',
    version='v0.0.1',
    long_description=README,
    url='https://github.com/mary123mary/EmoLexGram',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=["pandas", "nltk", "requests"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers'
    ],
)