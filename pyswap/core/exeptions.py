import inspect


class ErrorOutOfRange(Exception):
    def __init__(self, value, range_min, range_max):


        self.value = value
        self.range_min = range_min
        self.range_max = range_max
        caller_locals = inspect.currentframe().f_back.f_locals

        for name, val in caller_locals.items():
            if val is value:
                self.arg_name = name
                break
        self.message = f"{self.arg_name} = {value} is outside of range [{range_min}, {range_max}]"
        super().__init__(self.message)


def check_range(num, range_min, range_max, left, right):
    if left == 'open' and right == 'open':
        if num <= range_min or num >= range_max:
            raise ErrorOutOfRange(num, range_min, range_max)
    elif left == 'closed' and right == 'closed':
        if num < range_min or num > range_max:
            raise ErrorOutOfRange(num, range_min, range_max)
    elif left == 'closed' and right == 'open':
        if num < range_min or num >= range_max:
            raise ErrorOutOfRange(num, range_min, range_max)
    elif left == 'open' and right == 'closed':
        if num <= range_min or num > range_max:
            raise ErrorOutOfRange(num, range_min, range_max)


class TypeErrorCheck(TypeError):
    def __init__(self, value, required_type):

        caller_locals = inspect.currentframe().f_back.f_locals

        for name, val in caller_locals.items():
            if val is value:
                self.arg_name = name
                break

        self.message = f"{self.arg_name} is not {required_type}. Instead it is {type(value)}"
        super().__init__(self.message)


def check_type(value, required_type):
    if not isinstance(value, required_type):
        raise TypeErrorCheck(value, required_type)


class ErrorMissingParameter(ValueError):
    def __init__(self, message=None):

        self.message = message

        super().__init__(self.message)


class ErrorDatesNotAligned(Exception):
    def __int__(self):
        pass

    def __str__(self):
        pass

class ErrorWrongNumberOfLayers(Exception):
    def __int__(self):
        pass

    def __str__(self):
        pass

