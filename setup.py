from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Security",
    "Topic :: Security :: Cryptography",
    "Topic :: Software Development",
    "Topic :: System :: Monitoring",
]


setup(
    name="pegnet-py",
    version="0.0.2",
    description="Python client library for the pegnetd API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    platforms=["OS Independent"],
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=["tests", "examples"]),
    include_package_data=True,
    install_requires=["requests>=2.20.0", "factom-api", "factom-keys"],
    url="https://github.com/pegnet/pegnet-py",
)
