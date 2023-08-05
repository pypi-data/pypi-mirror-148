from setuptools import setup
import setuptools

__project__ = "finvizscrapper"
__version__ = "0.0.4"
__description__ = "this library scrapes importa information from finviz.com"
#__packages__ = ["fscrapper"]
__requires__ = ["pandas", "bs4", "urllib3", "matplotlib", "lxml"]
__author__ = "Kaio"
__author_email__ = "kaio@crimson.ua.edu"

setup(
    name = __project__,
    version = __version__,
    url = "https://github.com/kaiomarques93/finviz_scrapper",
    description = __description__,
    packages=['finvizscrapper'],
    author = __author__,
    author_email = __author_email__,
    install_requires = __requires__,
)