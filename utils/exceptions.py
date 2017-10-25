

class BadDataException(Exception):
    def __str__(self):
        return repr("Something went horribly wrong")

