class Translator(object):
    def __init__(self, spec):
        self.validate(spec)
        self.spec = spec

    def validate(self, spec):
        """
        Checks that the given spec is a valid spec that can be used by
        the Translator class.
        """
        pass
