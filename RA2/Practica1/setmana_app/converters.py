class NegativeIntConverter:
    regex = r'-?\d+'
    def to_python(self, value): return int(value)