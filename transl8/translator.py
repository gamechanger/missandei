
class TranslatorFormatException(Exception):
    pass


def get_value_at_path(obj, path):
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
    if isinstance(path, basestring):
        path = path.split('.')
    if len(path) > 1:
        set_value_at_path(obj.setdefault(path[0], {}), path[1:], value)
    else:
        obj[path[0]] = value

def translate(from_path, to_path, from_source, to_dest):
    found, value = get_value_at_path(from_source, from_path)
    if found:
        set_value_at_path(to_dest, to_path, value)


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
        end = {}
        for from_path, to_path in self.spec.iteritems():
            translate(from_path, to_path, start, end)
        return end

    def backward(self, end):
        start = {}
        for from_path, to_path in self.spec.iteritems():
            translate(to_path, from_path, end, start)
        return start
