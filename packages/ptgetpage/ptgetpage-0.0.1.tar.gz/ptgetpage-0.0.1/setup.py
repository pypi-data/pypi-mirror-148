import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ptgetpage",
    description="Get page content & HTTP headers",
    author="Penterep",
    author_email="info@penterep.com",
    url="https://www.penterep.com/",
    version="0.0.1",
    license="GPLv3+",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Environment :: Console"
    ],
    python_requires='>=3.6',
    install_requires=["requests", "ptlibs>=0.0.6"],
    entry_points = {'console_scripts': ['ptgetpage = ptgetpage.ptgetpage:main']},
    long_description=long_description,
    long_description_content_type="text/markdown",
)