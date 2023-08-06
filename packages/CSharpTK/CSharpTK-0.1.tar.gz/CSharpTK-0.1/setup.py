import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CSharpTK",
    version="0.1",
    author="XiangQinxi",
    author_email="XiangQinxi@outlook.com",
    description="C# Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xiangqinxi/",
    project_urls={
        "Bug Tracker": "https://github.com/xiangqinxi",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
)