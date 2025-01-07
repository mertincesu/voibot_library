# Python library publish configs
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="voibot",  
    version="0.1.10",  
    author="Mert Incesu", 
    author_email="mert.incesu03@gmail.com",  
    description="A Python library for creating virtual assistants using OpenAI and document retrieval",  # Short description of your library
    long_description=long_description, 
    long_description_content_type="text/markdown", 
    url="https://voiai.io", 
    packages=find_packages(), 
    install_requires=[ 
        "requests",
        "openai",
        "langchain",
        "langchain_openai",
        "langchain_community",
        "chromadb",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', 
)
