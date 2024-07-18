from setuptools import setup, find_packages
from xnxxdl import __version__ 

setup(
    name='xnxx-dl',
    version=__version__,
    description='A web scraping and URL filtering tool for xnxx.com',
    author='Joannes J.A. Wyckmans',
    author_email='johan.wyckmans@gmail.com',
    url='https://github.com/thisisawesome1994/xnxx-dl',  # Replace with your GitHub repo URL
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'urllib3',
        'argparse',
        'youtube-dl',
    ],
    entry_points={
        'console_scripts': [
            'xnxx-dl = xnxxdl.main:main',  # Assuming your main function is in a file called 'main.py'
        ],
    },
)