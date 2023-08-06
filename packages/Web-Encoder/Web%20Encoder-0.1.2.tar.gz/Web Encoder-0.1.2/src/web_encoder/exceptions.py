class WebEncoderException(Exception):
    pass


class InvalidEncodingErrors(WebEncoderException):
    """Exception raised for errors in the input value of encoding_errors attribute of WebEncoder class.

    Args:
        message: explanation of the error
    """

    def __init__(self, message=None):
        self.message = (
            message
            or "Invalid encoding_errors value. It should be 'strict', 'ignore', 'replace' or 'xmlcharrefreplace'."
        )
        super().__init__(self.message)


class InvalidStringType(WebEncoderException):
    """Exception raised for errors in the input value of _string into _string_to_bytes method of WebEncoder class.

    Args:
        message: explanation of the error
    """

    def __init__(self, message=None):
        self.message = message or "The _string need to be str type."
        super().__init__(self.message)


class InvalidBytesType(WebEncoderException):
    """Exception raised for errors in the input value of _bytes into methods of WebEncoder class.

    Args:
        message: explanation of the error
    """

    def __init__(self, message=None):
        self.message = message or "The _bytes need to be bytes type."
        super().__init__(self.message)


class InvalidDataType(WebEncoderException):
    """Exception raised for errors in the input value of data into encode method of WebEncoder class.

    Args:
        message: explanation of the error
    """

    def __init__(self, message=None):
        self.message = message or "The data need to be str type."
        super().__init__(self.message)


class InvalidEncodedDataType(WebEncoderException):
    """Exception raised for errors in the input value of encoded_data into decode method of WebEncoder class.

    Args:
        message: explanation of the error
    """

    def __init__(self, message=None):
        self.message = message or "The encoded_data need to be str type."
        super().__init__(self.message)


class DataDecodeError(WebEncoderException):
    """Exception raised for data decoding error in _bytes_to_string of WebEncoder class.

    Args:
        message: explanation of the error
    """

    def __init__(self, message=None):
        self.message = message or "Could not decode the message."
        super().__init__(self.message)


class CannotBeCompressed(WebEncoderException):
    """Exception raised for errors in the _compress_data method of WebEncoder class.

    Args:
        message: explanation of the error
    """

    def __init__(self, message=None):
        self.message = message or "The data cannot be compressed."
        super().__init__(self.message)


class CannotBeDecompressed(WebEncoderException):
    """Exception raised for errors in the _decompress_data method of WebEncoder class.

    Args:
        message: explanation of the error
    """

    def __init__(self, message=None):
        self.message = message or "The data cannot be decompressed."
        super().__init__(self.message)
