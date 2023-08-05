from setuptools import setup, find_packages
import os

# find all json files in honkaiDex/data/
data_files = []
for root, dirs, files in os.walk("honkaiDex/data"):
    for file in files:
        if file.endswith(".json"):
            data_files.append(os.path.join(root, file))

setup(
    name="honkaidex",
    version="0.2.4",
    author="celtica, kiyandere",
    author_email="celticaxp@gmail.com, kiyanhalcyon0707@gmail.com",
    description="Honkai Impact 3 Database",
    long_description="".join(open("README.md", "r").readlines()),
    long_description_content_type="text/markdown",
    url="https://github.com/HiganHana/HonkaiDex",
    packages=[
        "honkaiDex",
        "honkaiDex.base",
        "honkaiDex.profile",
        "honkaiDex.data",
        "honkaiDex.parse_v1",
        "honkaiDex.game",
    ],
    data_files=data_files,
    install_requires=[
        "zw-util-lib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)