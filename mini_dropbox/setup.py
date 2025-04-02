from setuptools import setup, find_packages

setup(
    name="mini_dropbox",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-multipart",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "pyyaml"
    ]
) 