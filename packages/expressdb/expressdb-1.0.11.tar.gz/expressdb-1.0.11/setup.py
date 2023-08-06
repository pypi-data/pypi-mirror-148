from setuptools import setup, find_packages

setup(
    name="expressdb",
    version="1.0.11",
    license='MIT',
    author="Nguyen Anh Khai",
    author_email="anhkhainguyen9@gmail.com",
    description="A python module for database.",
    long_description="See guide in https://github.com/nguyenanhkhai/expressdb/blob/master/README.md.",
    url="https://github.com/nguyenanhkhai/expressdb",
    packages=find_packages(),
    install_requires=[
        'shortuuid',
        'numpy',
        "pandas",
    ]
)
