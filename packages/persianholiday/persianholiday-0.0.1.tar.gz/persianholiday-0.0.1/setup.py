import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="persianholiday",
    version="0.0.1",
    author="Saman Jalinous",
    author_email="saman.jalinous@gmail.com",
    description="Get Holidays from time.ir",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/algobits/irholiday",
    project_urls={
        "Bug Tracker": "https://github.com/algobits/irholiday/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['persianholiday'],
    python_requires=">=3.6",
    install_requires=[
        'requests',
        'pandas',
        'jdatetime',
        'convert-numbers',
        'beautifulsoup4'
    ]
)
