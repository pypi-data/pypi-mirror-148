import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytrackunit",
    version="2.3.7",
    author="Marius Schlueter",
    author_email="themrslue@googlemail.com",
    description="Easy access for TrackUnit REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/einsteinmaster/TrackUnitPython",
    project_urls={
        "Bug Tracker": "https://github.com/einsteinmaster/TrackUnitPython/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["pytrackunit"],
    install_requires=["aiohttp", "aiofiles", "tqdm", "python-dateutil", "aiosqlite"],
    python_requires=">=3.8",
)