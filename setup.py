from setuptools import setup

setup(
    name="raenim",
    version="0.5.1",
    packages=["raenim"],
    install_requires=[
        "addict",
        "opencv-python",
        "manim",
        "noise"
    ],
)