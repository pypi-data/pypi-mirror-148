import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="virtualcity",
    version="0.0.5",
    author="Shuang Li, Kabir Swain",
    author_email="lishuang@mit.edu, kswain98@icloud.com",
    description="Python API to communicate with the VirtualCity environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShuangLI59/virtualcity-python-api",
    project_urls={
        "Documentation": "https://virtualcity.readthedocs.io/en/latest/",
        "Bug Tracker": "https://github.com/ShuangLI59/virtualcity-python-api"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'gym',
        'ray',
        'tensorboardX',
        'wandb',
        'stable-baselines3',
        'python-socketio'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)