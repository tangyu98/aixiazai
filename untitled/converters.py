class YYConverters:
    regex = '(19|20)/d{2}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)
