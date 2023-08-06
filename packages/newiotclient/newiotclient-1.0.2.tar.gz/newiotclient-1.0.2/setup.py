import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="newiotclient",
    version="1.0.2",
    author="Laonan",
    author_email="hello@laonan.net",
    description="python client for iot.lonelyassistant.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laonan/newiot-pyclient",  # github url
    project_urls={
        "Bug Tracker": "https://github.com/laonan/newiot-pyclient/issues",
    },
    include_package_data=True,
    package_data={
        "newiotclient": ["cert/*.crt"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
            'requests>=2.27.1',
            'paho-mqtt>=1.6.1',
    ],
    zip_safe=True,
    python_requires=">=3.6",
)
