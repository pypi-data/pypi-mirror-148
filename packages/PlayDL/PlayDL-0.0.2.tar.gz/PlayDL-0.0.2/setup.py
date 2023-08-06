import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PlayDL",
    version="0.0.2",
    author="Xin Zhong",
    author_email="1140091006@qq.com",
    description="A package with presentations of various deep learning methods",
    long_description_content_type="text/markdown",
    url="https://github.com/",
    license="MIT Licence",
    # packages=setuptools.find_packages("自制库/ZxSci"),
    # packages=["matplotlib"],
    install_requires=['torch','torchvision','functools','numpy','PIL','opencv-python'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # include_package_data = True,
    # platforms = "any",
    # install_requires = ['chardet']

)