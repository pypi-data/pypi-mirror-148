 # Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="astrop__pat",
    description="Un paquet bidon, qu'est-ce qu'on s'amuse !",
    name="bidongorx",
    version="0.1.0",
    packages=find_packages(include=["bidongorx", "bidongorx.*"]),
    python_requires=">=3.1",
    install_requires=["tqdm>3"],
)