class NotCachedError(Exception):
    """ Raise when given source is not cached yet but --date option is given with source """
    pass


class NoNewsError(Exception):
    """ Raise when there is no news in a given date and source """
    pass


class InvalidFileFormatError(Exception):
    """ Raise when given file format is neither html nor pdf"""
    pass
