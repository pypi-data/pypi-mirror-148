from setuptools import setup

setup(
    name='Zscaler-API-Talkers',
    version='2.1',
    author='Sergio Pereira',
    author_email='sergitopereira@hotmail.com',
    packages=['/Users/spereira/github/zscaler_api_talkers'],
    url='https://github.com/sergitopereira/zscaler_api_talkers.git',
    license='LICENSE.txt',
    description='An awesome package that does something',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    install_requires=[
        "requests",
        "appdirs",
        "ipython"
    ],
)
