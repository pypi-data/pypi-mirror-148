"""
Converter to convert date packed strings to Discord formattable times.

@author: AstroWX
@name: htime
@version: 0.0.4
"""

import dateparser
import pytz

class HTimeParser():
    """
    Parent class for HTime parser
    """

    def __init__(self, defaultTimeZone = pytz.utc):
        self.defaultTimeZone = defaultTimeZone

    def __dateParserLocal__(self, time: str):
        """
        Use a try-catch statement to attempt to parse date string to datetime object
        """

        finished = None
        try:
            finished = dateparser.parse(time)
        except:
            raise UnknownTimeFormatError("Could not determine time format")

        return finished

    def __convertLocal__(self, time):
        """
        Parse date time and convert to epoch
        """
        pDf = self.__dateParserLocal__(time)
        epoch = int(pDf.timestamp())
        
        return epoch

    def parseShortTime(self, time: str):
        """Takes in time string and attempts to convert into a short time formatted string

        Args:
            time (str): A string in a date format
        
        Returns:
            str: A string in the Discord short time format
        """
        
        epoch = self.__convertLocal__(time)
        fSt = f"<t:{epoch}:t>"

        return fSt
    
    def parseLongTime(self, time: str):
        """Takes in time string and attempts to convert into a long time formatted string

        Args:
            time (str): A string in a date format
        
        Returns:
            str: A string in the Discord long time format
        """
        
        epoch = self.__convertLocal__(time)
        fSt = f"<t:{epoch}:T>"

        return fSt

    def parseShortDate(self, time: str):
        """Takes in time string and attempts to convert into a short date formatted string

        Args:
            time (str): A string in a date format
        
        Returns:
            str: A string in the Discord short date format
        """
        
        epoch = self.__convertLocal__(time)
        fSt = f"<t:{epoch}:d>"

        return fSt

    def parseLongDate(self, time: str):
        """Takes in time string and attempts to convert into a long date formatted string

        Args:
            time (str): A string in a date format
        
        Returns:
            str: A string in the Discord long date format
        """
        
        epoch = self.__convertLocal__(time)
        fSt = f"<t:{epoch}:D>"

        return fSt

    def parseShortDateTime(self, time: str):
        """Takes in time string and attempts to convert into a short date & time formatted string

        Args:
            time (str): A string in a date format
        
        Returns:
            str: A string in the Discord short date & time format
        """
        
        epoch = self.__convertLocal__(time)
        fSt = f"<t:{epoch}:f>"

        return fSt

    def parseLongDateTime(self, time: str):
        """Takes in time string and attempts to convert into a long date & time formatted string

        Args:
            time (str): A string in a date format
        
        Returns:
            str: A string in the Discord long date & time format
        """
        
        epoch = self.__convertLocal__(time)
        fSt = f"<t:{epoch}:F>"

        return fSt

    def parseRelativeTime(self, time: str):
        """Takes in time string and attempts to convert into a relative time formatted string

        Args:
            time (str): A string in a date format
        
        Returns:
            str: A string in the Discord relative time format
        """
        
        epoch = self.__convertLocal__(time)
        fSt = f"<t:{epoch}:R>"

        return fSt

class UnknownTimeFormatError(Exception):
    pass