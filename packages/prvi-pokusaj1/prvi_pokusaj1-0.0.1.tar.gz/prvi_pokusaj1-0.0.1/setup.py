from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Sudoku solver with number detection and recognision.'
1
# Setting up
setup(
    name="prvi_pokusaj1",
    version=VERSION,
    author="Nikola Ignjatovic",
    author_email="<nikola444555@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['opencv-python', 'keras', 'imutils'],
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