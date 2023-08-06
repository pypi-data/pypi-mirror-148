
from importlib.metadata import entry_points
import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="interfacedoc",
    version="0.0.2",
    author="rizki maulana",
    author_email="rizkimaulana348@gmail.com",
    description="Interface documentation installer",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/rizki4106/interface-installer",
    license='MIT',
    python_requires='>=3.0',
    install_requires=[
        "beautifulsoup4==4.11.1",
        "click==8.1.2",
        "Flask==2.1.1",
        "importlib-metadata==4.11.3",
        "itsdangerous==2.1.2",
        "Jinja2==3.1.1",
        "Markdown==3.3.6",
        "MarkupSafe==2.1.1",
        "soupsieve==2.3.2.post1",
        "Werkzeug==2.1.1",
        "zipp==3.8.0",
        "colorama==0.4.4"
    ],
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