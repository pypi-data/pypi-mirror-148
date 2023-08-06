from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = "loto_online.py",
    version = "1.0.0",
    url = "https://github.com/Zakovskiy/loto_online.py",
    download_url = "https://github.com/Zakovskiy/loto_online.py/tarball/master",
    license = "MIT",
    author = "Zakovskiy",
    author_email = "gogrugu@gmail.com",
    description = "A library to create Loto Online bots.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords = [
        "loto",
        "online",
        "loto_online.py",
        "loto.py",
        "loto-bot",
        "rstgame",
        "rstgames",
        "api",
        "socket",
        "python",
        "python3",
        "python3.x",
        "zakovskiy",
        "official"
    ],
    install_requires = [
        "setuptools",
        "requests",
        "loguru",
    ],
    setup_requires = [
        "wheel"
    ],
    packages = find_packages()
)
