from setuptools import setup, find_packages


setup(
    name='thoughtful',
    version='0.0.1',
    author="Thoughtful Automation",
    author_email='contact@thoughtfulautomation.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},

)