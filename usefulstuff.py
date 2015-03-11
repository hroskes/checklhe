class printablelist(list):
    def __str__(self, joiner = ", "):
        return "[" + joiner.join(str(a) for a in self) + "]"

    def __getattr__(self, name):
        return printablelist([(a if a is None else a.__getattribute__(name)) for a in self])

    def __call__(self, *args, **kwargs):
        return printablelist([(a if a is None else a(*args, **kwargs)) for a in self])
