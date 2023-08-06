import glob

from setuptools import find_namespace_packages, setup

from vmray import __version__


EXAMPLE_SCRIPTS = list(glob.glob("examples/*.py"))


setup(
    # metadata
    name="vmray_rest_api",
    version=__version__,
    url="https://www.vmray.com",
    author="VMRay",
    author_email="info@vmray.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    license="Proprietary",
    description="VMRay REST API Client and Integration Kit",

    # options
    python_requires=">=3.6",
    install_requires=[
        "dataclasses; python_version < '3.7'",
        "packaging",
        "requests",
        "six",
        "urllib3",
    ],
    packages=find_namespace_packages(include=["vmray.*"]),
    scripts=EXAMPLE_SCRIPTS,
    data_files=[
        ("", ["LICENSE", "README.md"]),
    ],
    zip_safe=False,
)
