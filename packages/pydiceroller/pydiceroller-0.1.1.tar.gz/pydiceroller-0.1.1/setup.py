from setuptools import setup


setup(
    name="pydiceroller",
    version="0.1.1",
    description="a minimal dice roller",
    long_description="The complete description/installation/use/FAQ is available at : https://github.com/thib1984/pydiceroller#readme",
    url="https://github.com/thib1984/pydiceroller",
    author="thib1984",
    author_email="thibault.garcon@gmail.com",
    license="MIT",
    packages=["pydiceroller"],
    install_requires=[],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "pydiceroller=pydiceroller.pydiceroller:pydiceroller"
        ],
    },
    classifiers=[       
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
