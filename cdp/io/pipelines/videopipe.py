class VideoPipe:
    def __init__(self, func=None):
        if not callable(func):
            raise TypeError("""
VideoPipe requires a video url collection function to initialize.
Given: {func_type}
Please view our documentation for an example.
""".format(func_type=type(func)))

        self.getter = func
