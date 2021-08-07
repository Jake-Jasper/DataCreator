from setuptools import setup, find_packages




VERSION = '0.0.1'
DESCRIPTION = 'Python Tkinter app for creating artificial data'
LONG_DESCRIPTION = 'A package that provides a graphical user interface that can be used to design data with specific visual properties'

# Setting up
setup(
    name="DataCreator",
    version=VERSION,
    author="Jake Jasper (JLJ)",
    author_email="<jakeljasper@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION ,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tkinter', 'data'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Anyone",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
