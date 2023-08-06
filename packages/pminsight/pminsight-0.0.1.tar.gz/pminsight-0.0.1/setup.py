from setuptools import setup, find_packages

setup(
    name="pminsight",
    version="0.0.1",
    keywords=['pip', 'pm', 'pmInsight'],
    description="Tools for Product manager",
    long_description="Tools for Product manager (long)",
    license="MIT License",

    url="https://github.com/AlexTengT/pminsight",
    author="Alex Teng",
    author_email="",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["matplotlib"]
)
