from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="persisted",
    version="1.0.0b2",
    description="A two-way data persistence framework for watching file changes / updating files based on changes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexkoay/persisted",
    author="Alex Koay",
    author_email="alexkoay88@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
    keywords="persistence watch reload save",
    packages=["persisted"],
    package_dir={"persisted": "persisted"},
    python_requires=">=3.7, <4",
    extras_require={
        "dev": ["black", "mypy", "isort"],
    },
)
