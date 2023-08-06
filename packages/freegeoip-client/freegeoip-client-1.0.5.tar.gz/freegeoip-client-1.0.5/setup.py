from setuptools import find_packages, setup


def get_long_description():
    with open("README.md") as file:
        return file.read()


setup(
    name="freegeoip-client",
    version="1.0.5",
    description="FreeGeoIp's RESTful API client for Python",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Kevin Furjan",
    author_email="kfurjan@gmail.com",
    url="https://github.com/kfurjan/python-freegeoip-client",
    project_urls={
        "GitHub Project": "https://github.com/kfurjan/python-freegeoip-client",
        "Issue Tracker": "https://github.com/kfurjan/python-freegeoip-client/issues",
    },
    packages=find_packages(
        include=["freegeoip_client", "freegeoip_client.*"],
    ),
    package_data={
        "freegeoip_client": ["data/*.cfg"],
    },
    install_requires=[
        "requests==2.27.1",
    ],
    setup_requires=[
        "pytest-runner",
        "flake8==4.0.1",
    ],
    tests_require=[
        "pytest==7.1.2",
        "requests-mock==1.9.3",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[
        "FreeGeoIp",
        "Client",
        "REST API Client",
    ],
    license="MIT",
)
