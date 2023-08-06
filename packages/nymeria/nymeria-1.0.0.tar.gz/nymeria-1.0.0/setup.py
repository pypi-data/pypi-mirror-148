from setuptools import setup

import nymeria

setup(
    name='nymeria',
    version=nymeria.__version__,
    description='Discover contact details such as phone numbers, email addresses and social links using Nymeria\'s service.',
    url='https://git.nymeria.io/nymeria.py',
    author=nymeria.__author__,
    author_email='dev@nymeria.io',
    license='MIT',
    packages=['nymeria'],
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)
