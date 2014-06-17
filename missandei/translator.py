
class TranslatorFormatException(Exception):
    """Exception raised when a given translation spec is not in a valid format."""
    pass


def get_value_at_path(obj, path):
    """
    Attempts to get the value of a field located at the given field path within the
    object. Recurses into child dicts as necessary. Very permissive - if the branch
    nodes on a given path do not exist, or even if they are of a different type,
    this will be handled and (False, None) will simply be returned.

    Path can be provided either as a dot-delimited string or as an array of path
    elements.

    Returns a two member tuple containing a boolean indicating whether the field was
    found and the value itself. If the value was not found the second returned value
    is None.
    """
    if isinstance(path, basestring):
        path = path.split('.')

    if path[0] in obj:
        if len(path) > 1:
            if not isinstance(obj[path[0]], dict):
                return False, None
            return get_value_at_path(obj[path[0]], path[1:])
        return True, obj[path[0]]

    return False, None

def set_value_at_path(obj, path, value):
    """
    Sets the given key in the given dict object to the given value. If the
    given path is nested, child dicts are created as appropriate.
    Accepts either a dot-delimited path or an array of path elements as the
    `path` variable.
    """
    if isinstance(path, basestring):
        path = path.split('.')
    if len(path) > 1:
        set_value_at_path(obj.setdefault(path[0], {}), path[1:], value)
    else:
        obj[path[0]] = value


class Translator(object):
    def __init__(self, spec):
        self.validate(spec)
        self.spec = spec

    def validate(self, spec):
        """
        Checks that the given spec is a valid spec that can be used by
        the Translator class.
        """
        for from_path, to_path in spec.iteritems():
            if not isinstance(to_path, basestring):
                raise TranslatorFormatException()

        # TODO:
        #  - check that we don't map a given path both as a lead and branch


    def forward(self, start):
        """
        Executes the dictionary translation encapsulated by this object on
        the given `start` dict in the "forward" direction.

        In practice this means a new dict is returned containing the values
        from the start dict of the keys on the left side of the Translator's
        given spec mapped to the key paths indicated on the right side of
        the spec.
        """
        end = {}
        for from_path, to_path in self.spec.iteritems():
            found, value = get_value_at_path(start, from_path)
            if found:
                set_value_at_path(end, to_path, value)
        return end

    def backward(self, end):
        """
        Executes the dictionary translation encapsulated by this object on
        the given `start` dict in the "backward" direction.

        In practice this means a new dict is returned containing the values
        from the end dict of the keys on the right side of the Translator's
        given spec mapped to the key paths indicated on the left side of
        the spec.
        """
        start = {}
        for from_path, to_path in self.spec.iteritems():
            found, value = get_value_at_path(end, to_path)
            if found:
                set_value_at_path(start, from_path, value)
        return start
