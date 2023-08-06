from setuptools import setup

setup(
    name="py-shardeum-explorer",
    version="0.0.1",
    description="A minimal, complete, python API for Shardeum Explorer.",
    url="https://github.com/iSumitBanik/py-shardeum-explorer",
    author="Sumit Banik",
    license="MIT",
    packages=[
        "shardeumexplorer"
    ],
    python_requires='>=3.8',
    install_requires=["requests"],
    include_package_data=True,
    zip_safe=False,
)