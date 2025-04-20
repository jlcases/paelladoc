from setuptools import setup, find_packages

setup(
    name="paelladoc",
    version="0.1.0",
    description="Documentation generator with AI capabilities",
    author="Jose Luis Cases",
    author_email="joseluiscases@gmail.com",
    package_dir={"": "src"},  # Tell setuptools packages are under src
    packages=find_packages(where="src"),  # List packages under src
    python_requires=">=3.8",
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        "console_scripts": [
            "paelladoc=paelladoc.cli:main",
        ],
    },
) 