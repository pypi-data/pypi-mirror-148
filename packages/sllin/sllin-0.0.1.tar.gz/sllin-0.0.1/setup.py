import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sllin",
    version="0.0.1",
    author="Patrick Menschel",
    author_email="menschel.p@posteo.de",
    description="An alternative python lib for SLCAN based LIN adapters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/menschel/sllin",
    packages=setuptools.find_packages(exclude=["tests", "scripts", ]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "License :: Free for non-commercial use",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Embedded Systems",
    ],
    python_requires=">=3.9",
    keywords="LIN",
    requires=["pyserial", ],
)
