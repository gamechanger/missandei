from functools import partial


class TranslatorFormatException(Exception):
    """Exception raised when a given translation spec is not in a valid format."""
    pass


def get_value_at_path(path, obj):
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
                return
            return get_value_at_path(path[1:], obj[path[0]])
        return obj[path[0]]


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


def validate_spec(spec):
    """
    Checks that the given spec is a valid spec that can be used by
    the Translator class.
    """
    for from_path, to_path in spec.iteritems():
        if isinstance(to_path, basestring):
            continue
        elif callable(to_path):
            continue

        raise TranslatorFormatException()


def decorate_spec(spec):
    """
    Returns a copy of the given spec with simple key-based lookups replaced
    which functions which will actually implement those lookups.
    """
    decorated = {}
    for dest_path, source_path in spec.iteritems():
        if isinstance(source_path, basestring):
            decorated[dest_path] = partial(get_value_at_path, source_path)
        elif callable(source_path):
            decorated[dest_path] = source_path
    return decorated




def translator(spec):
    validate_spec(spec)
    spec = decorate_spec(spec)

    def impl(source):
        """
        Executes the dictionary translation encapsulated by this object on
        the given `source` dict.
        """
        end = {}
        for dest_path, source_fn in spec.iteritems():
            set_value_at_path(end, dest_path, source_fn(source))
        return end

    return impl
