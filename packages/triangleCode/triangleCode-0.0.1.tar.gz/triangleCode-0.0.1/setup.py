from setuptools import setup, find_packages



setup(
    name = 'triangleCode',
    version = '0.0.1',
    description = 'a very basic addition function',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/saurabhpl/sampleCode',
    author='Saurabh Pratap Singh',
    license='MIT',
    keywords='',
    packages=find_packages(),
)