from setuptools import setup, find_packages

setup(
    name='pySWAP',
    version='0.1.0',
    description='Package for creating and running SWAP models from Python',
    author='Mateusz Zawadzki',
    author_email='mateusz.zawadzki@vub.be',
    url='',
    packages=find_packages(),
    package_data={
        'pyswap.libs.swap420-exe': ['swap.exe'],
        'pyswap.libs.swap420-linux': ['swap420'],
        'pyswap.testcase.data': ['*'],
    }
)
