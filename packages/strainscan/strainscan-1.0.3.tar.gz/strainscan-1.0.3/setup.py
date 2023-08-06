import setuptools

setuptools.setup(
    name="strainscan",
    version="1.0.3",
    author="Liao Herui and Ji Yongxin",
    author_email="heruiliao2-c@my.cityu.edu.hk",
    description="One efficient and accurate strain-level microbiome composition analysis tool based on reference genomes and k-mers.",
    long_description="StrainScan takes reference database and sequencing data as input, outputs strain-level microbiome compistion analysis report.",
    long_description_content_type="text/markdown",
    url="https://github.com/liaoherui/StrainScan",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,
    package_data={"StrainScan":["library/jellyfish-linux","library/hier.R","library/dashing_s128","library/seqpy.c","library/seqpy.cpython-37m-x86_64-linux-gnu.so"]},
    install_requires=[
    "numpy==1.17.3",
    "pandas==1.0.1",
    "biopython==1.74",
    "scipy==1.3.1",
    "scikit-learn==0.23.1",
    "bidict==0.21.3",
    "treelib==1.6.1"
    ],
    entry_points={
        'console_scripts':[
        "strainscan = StrainScan.StrainScan:main",
        "strainscan_build = StrainScan.StrainScan_build:main",
        ]
    },
    python_requires='~=3.7',
    classifiers=[
    'Programming Language :: Python :: 3.7',
    ],
)
