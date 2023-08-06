from setuptools import setup

try:
    import torch
except ModuleNotFoundError:
    print("------------------------------------------------")
    print("torch not found")
    print("although it's not required for the installation")
    print("but please install it later")
    print("------------------------------------------------")

if __name__ == "__main__":
    setup()
