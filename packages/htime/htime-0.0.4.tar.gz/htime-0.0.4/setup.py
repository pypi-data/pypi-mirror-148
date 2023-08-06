from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Converting date strings to hammertime strings'
LONG_DESCRIPTION = """A package to convert date oriented strings to Discord formatted hammtertime strings

### Example of fetching long time:
```py
import htime

# Define new parser class instance
HTimeParser = htime.HTimeParser()

# Parse time with date string
time = HTimeParser.parseLongTime("April 25th, 2022 2:00pm EDT")
```
"""

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