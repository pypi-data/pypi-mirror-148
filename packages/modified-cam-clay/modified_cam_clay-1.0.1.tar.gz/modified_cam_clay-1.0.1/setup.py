import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modified_cam_clay",
    version="1.0.1",
    author="Has",
    author_email="portabl3lapy@gmail.com",
    description="A model to predict stress-strain behavior of soil",
    long_description="modified cam clay with istropic plasticity and elasticity",
    long_description_content_type="text/markdown",
    url="https://github.com/QuantumNovice/ModifiedCamClay",
    project_urls={
        "Bug Tracker": "https://github.com/QuantumNovice/ModifiedCamClay/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    include_package_data=True,
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
          'matplotlib',
          'numpy'
      ],
)