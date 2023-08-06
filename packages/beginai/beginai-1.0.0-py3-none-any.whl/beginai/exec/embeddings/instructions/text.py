class Length(object):
    """
    number of characters in a string.
    eg. length("I am rima") results 9
    """
    def __init__(self):
        pass
    def apply(self, value):
        return len(str(value))

class CountDigits(object):
    """
    count the number of digits in a string.
    eg. CountDigits("I am Rima 7") results in 1
    """
    def __init__(self):
        pass
    def apply(self, value):
        return sum(c.isdigit() for c in str(value))

class StandardName(object):
    """
    checks if a name is a standard english name.
    expects an array of standard english names.
    """
    def __init__(self, standard_names):
        self.names = standard_names #fill from api or cache.
    def apply(self, name):
        name = str(name)
        # some names have questions marks in them, killing the regex!
        s = name.replace("?","").replace('(', '').replace(')', '').split(' ')
        if len(s):
            s = s[0]
        #return standard_names_df.name.str.contains(s, case=False).any()
        return bool(s in self.names)


instructions_map = {
    "Length": Length,
    "CountDigits": CountDigits,
    "StandardName": StandardName
}
