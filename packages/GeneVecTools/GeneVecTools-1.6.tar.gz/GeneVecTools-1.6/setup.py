from setuptools import setup, find_packages


setup(
    name="GeneVecTools",
    version="1.6",
    license="danielum16license",
    author="Daniel Um",
    author_email="danielum.16@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/gmyrianthous/example-publish-pypi",
    keywords="example project",
    install_requires=[
        # "scikit-learn",
        "pandas",
        "faiss",
        "numpy",
        "requests",
        # "io",
        "tensorflow",
        # "datetime",
        # "os",
        # "sys",
        "biopython",
        "pysam",
    ],
)
