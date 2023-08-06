
import setuptools
import requests
  
with open("README.md", "r") as fh:
    description = fh.read()

def getRequirements():

    req = requests.get("https://raw.githubusercontent.com/rizki4106/interface/master/requirements.txt").content
    requirements = req.decode("utf-8").split("\n")[0:-1]
    return requirements
  
setuptools.setup(
    name="interfacedoc",
    version="0.0.3",
    author="rizki maulana",
    author_email="rizkimaulana348@gmail.com",
    description="Interface documentation installer",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/rizki4106/interface-installer",
    license='MIT',
    python_requires='>=3.0',
    install_requires=getRequirements(),
    entry_points= {
        'console_scripts': ['interfacedoc=interfacedoc.run:start']
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)