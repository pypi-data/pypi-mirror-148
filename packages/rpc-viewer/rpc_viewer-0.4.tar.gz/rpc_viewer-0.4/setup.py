import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpc_viewer",
    version="0.4",
    author="Lukas Stockmann",
    author_email="lukas.stockmann@t-online.de",
    description="Application to visualize MTS PRC3 files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/t8237/rpc_viewer",
    packages=setuptools.find_packages(),
    install_requires=['setuptools',
                      'wheel',
                      'numpy',
                      'matplotlib',
                      'rpc_reader'
                      ],
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'rpc_viewer=rpc_viewer.rpc_viewer:main',
        ],
    },
)
