
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyasync",
    version="0.0.2",
    author="weirdofeng",
    author_email="weirdofeng@gmail.com",
    description="Network async tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CG0047/pyasync",
    project_urls={
        # PyPI上显示的任意数量的额外链接。可以是官网地址、文档地址、GitIssues、个人博客地址等
        "Bug Tracker": "https://github.com/CG0047/pyasync/issues",
    },
    install_requires=[
        'gevent==1.4.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)


