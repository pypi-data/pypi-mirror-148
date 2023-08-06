from setuptools import setup


def get_readme_md_contents():
    """read the contents of your README file"""
    with open("README.md", encoding='utf-8') as f:
        long_description = f.read()
        return long_description

setup(
    name="async-polygon",
    version="0.0.0a3",
    author = "Dmitry Skripka",
    description="Async Polygon REST API",
    author_email = "dmitrio.skripka@gmail.com",
    long_description=get_readme_md_contents(),
    long_description_content_type="text/markdown",
    url="https://github.com/mirage-deadline/async-polygon",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment"
    ],
    install_requires=[
        "aiohttp>=3.8.1",
        "pandas==1.4.2"
    ]
)