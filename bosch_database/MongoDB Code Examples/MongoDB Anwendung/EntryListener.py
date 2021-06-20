class EntryListener:
    def __init__(self, callback):
        self.callback = callback

    def setEntry(self, entry):
        self.entry = entry

    def method(self, *args):
        self.callback(self.entry)
