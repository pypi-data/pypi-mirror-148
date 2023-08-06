 # -*- coding: utf-8 -*-

"""
To upload to PyPI, PyPI test, or a local server:
python setup.py bdist_wheel upload -r <server_identifier>
"""
from setuptools import setup, find_packages

setup(
    name="EMAI",
    version="0.1.8",
    author="Kevin M. Roccapriore",
    description="Electron microscopy AI tools",
    # packages = ["EMAI"],
    packages = find_packages(),
    install_requires=["matplotlib >= 3.2, < 3.4", 
                      "numpy >= 1.18.5", 
                      "scipy >= 1.3.0", 
                      "torch >= 1.0.0", 
                      "scikit-image >= 0.16.2", 
                      "opencv-python >= 4.1.0", 
                      "scikit-learn >= 0.22.1", 
                      "atomai >= 0.7.0",
                      "networkx>=2.5"
                      "mendeleev<=0.6.1",
                      "torchvision>=0.8.0",
                      "gpytorch>=1.4.0"
                      ],

    python_requires='~=3.6',

    keywords = ['EMAI', 'pycroscopy', 'atomai', 'stemtool']
)


# cd "Dropbox (ORNL)\ELIT testing\plugin for ELIT\!PACKAGE"
# python setup.py sdist bdist_wheel
# twine upload dist/*
# twine upload --skip-existing dist/*