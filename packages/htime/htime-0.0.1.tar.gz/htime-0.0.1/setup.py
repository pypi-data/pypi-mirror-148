from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Converting date strings to hammertime strings'
LONG_DESCRIPTION = 'A package to convert date oriented strings to Discord formatted hammtertime strings'

# Setting up
setup(
    name="htime",
    version=VERSION,
    author="AstroWX",
    author_email="<multiidev@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pytz', 'dateparser'],
    keywords=['python', 'discord', 'hammertime', 'converter'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)