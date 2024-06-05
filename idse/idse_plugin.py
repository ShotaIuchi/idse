class IdsePlugin:
    def name(self):
        return self.__class__.__name__

    def translate(self, original: str) -> str:
        raise NotImplementedError("Plugin must implement `execute` method")
