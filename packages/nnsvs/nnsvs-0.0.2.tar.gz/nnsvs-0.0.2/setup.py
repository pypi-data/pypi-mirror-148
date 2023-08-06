from importlib.machinery import SourceFileLoader
from os.path import exists

from setuptools import find_packages, setup

version = SourceFileLoader("nnsvs.version", "nnsvs/version.py").load_module().version

packages = find_packages()
if exists("README.md"):
    with open("README.md", "r", encoding="UTF-8") as fh:
        LONG_DESC = LONG_DESC = fh.read()
else:
    LONG_DESC = ""

setup(
    name="nnsvs",
    version=version,
    description="DNN-based singing voice synthesis library",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    package_data={"": ["_example_data/*"]},
    packages=packages,
    include_package_data=True,
    install_requires=[
        "numpy",
        "cython",
        "torch >= 1.1.0",
        "torchaudio",
        "hydra-core >= 1.1.0, < 1.2.0",
        "hydra_colorlog >= 1.1.0",
        "librosa >= 0.7.0",
        "pysptk",
        "pyworld",
        "tensorboard",
        "nnmnkwii",
        "pysinsy",
    ],
    extras_require={
        "docs": [
            "sphinx",
            "sphinx-autobuild",
            "sphinx_rtd_theme",
            "nbsphinx>=0.8.6",
            "sphinxcontrib-bibtex",
            "Jinja2>=3.0.1,<=3.0.3",
            "pandoc",
            "ipython",
            "jupyter",
            "matplotlib>=1.5",
        ],
        "lint": [
            "pysen",
            "types-setuptools",
            "mypy<=0.910",
            "black>=19.19b0,<=20.8",
            "flake8>=3.7,<4",
            "flake8-bugbear",
            "isort>=4.3,<5.2.0",
            "click<8.1.0",
        ],
        "test": ["pytest"],
    },
    entry_points={
        "console_scripts": [
            "nnsvs-prepare-features = nnsvs.bin.prepare_features:entry",
            "nnsvs-fit-scaler = nnsvs.bin.fit_scaler:entry",
            "nnsvs-preprocess-normalize = nnsvs.bin.preprocess_normalize:entry",
            "nnsvs-train = nnsvs.bin.train:entry",
            "nnsvs-train-resf0 = nnsvs.bin.train_resf0:entry",
            "nnsvs-generate = nnsvs.bin.generate:entry",
            "nnsvs-synthesis = nnsvs.bin.synthesis:entry",
        ],
    },
)
