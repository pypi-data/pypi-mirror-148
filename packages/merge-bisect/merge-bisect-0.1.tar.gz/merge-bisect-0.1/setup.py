import os

from setuptools import find_packages, setup


def read(fname):
    return (
        open(os.path.join(os.path.dirname(__file__), fname), "rb")
        .read()
        .decode("utf-8")
    )


setup(
    name="merge-bisect",
    version="0.1",
    author="Miroslav Shubernetskiy",
    description="Like git bisect, but only with merge commits.",
    long_description=read("README.rst"),
    url="https://github.com/miki725/merge-bisect",
    packages=find_packages(exclude=["test", "test.*"]),
    entry_points={
        "console_scripts": ["merge-bisect = merge_bisect.__main__:main"],
    },
    keywords=" ".join(
        [
            "git",
            "bisect",
        ]
    ),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
    ],
    license="MIT",
)
