from setuptools import setup, find_packages

setup(
    name="tabbycat-api",
    version="0.1.2",
    description="Tabbycat API wrapper",
    
    author="Satoshi Inoue",
    author_email="sato4inoue2003@gmail.com",
    
    packages=find_packages(),
    install_requires=["httpx", "parse"],
)