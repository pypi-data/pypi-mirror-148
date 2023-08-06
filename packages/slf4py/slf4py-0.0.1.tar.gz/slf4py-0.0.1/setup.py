from setuptools import setup, find_packages

setup(
    name='slf4py',
    version='0.0.1',
    author='taiyo tamura',
    author_email='gtaiyou24@gmail.com',
    description='Simple Logging Facade for Python',
    packages=find_packages(where="src"),
    package_dir={"": "src"}
)
