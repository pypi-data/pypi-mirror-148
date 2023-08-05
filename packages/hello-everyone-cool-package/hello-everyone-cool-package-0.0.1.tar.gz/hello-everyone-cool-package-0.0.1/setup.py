from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A small example how to publish your package'
LONG_DESCRIPTION = 'A very long description about how to publish your own package'

# Setting up
setup(
    name="hello-everyone-cool-package",
    version=VERSION,
    author="Jean Carlos Alarcon",
    author_email="<jeancalarcon98@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)