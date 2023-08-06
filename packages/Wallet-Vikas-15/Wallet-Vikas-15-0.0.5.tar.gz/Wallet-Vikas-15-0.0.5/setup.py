from setuptools import setup, find_packages

setup(
    name="Wallet-Vikas-15",
    version="0.0.5",
    author="Vikas Bhardwaj",
    author_email="viaksbhardwaj020@gmail.com",
    url="https://drive.google.com/file/d/123aztyIl9KSax3OkF6h_Rv6KlcCHkxo6/view?usp=sharing",
    description="An aplication that helps to maintain wallet balance",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["click", "pytz"],
    entry_points={"console_scripts": ["Wallet = Wallet"]},
)
