import setuptools

setuptools.setup(
    name="mexc", # 
    version="0.0.1",
    author="Shawn Kuo",
    author_email="shawnkuo.p@mexc.com",
    description="The only official certified sdk of MEXC",
    url="https://github.com/mxcdevelop/mexc-api-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)