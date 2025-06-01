from setuptools import setup, find_packages

setup(
    name="vector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "weaviate-client>=3.24.1",
        "openai>=1.12.0",
        "python-dotenv>=1.0.0",
    ],
) 