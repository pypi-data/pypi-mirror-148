import setuptools
"""
Setup
"""

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="secondstotext",
    version="1.0.3",
    author="Sumiza",
    author_email="sumiza@gmail.com",
    description="Converts seconds to human readable text or tuple",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sumiza/secondstotext/",
    project_urls={
        "Bug Tracker": "https://github.com/Sumiza/secondstotext/issues",
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
