import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colorlog-jawide",
    version="0.0.1",
    author="jawide",
    author_email="jawide@qq.com",
    description="Enable the default logging to output with color",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jawide/colorlog",
    project_urls={
        "Bug Tracker": "https://github.com/jawide/colorlog/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)