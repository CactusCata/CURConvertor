class Feeder:

    def __init__(self):
        self.dictNameValue = {}

    def set(self, name, value):
        print(f"{name}:{value}")
        self.dictNameValue[name] = value

    def get(self, name):
        return self.dictNameValue[name]

    def __str__(self):
        toSend = ""
        for name, value in self.dictNameValue.items():
            toSend += f"{name}: value\n"
        return toSend
