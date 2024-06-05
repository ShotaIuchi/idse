from idse.idse_plugin import IdsePlugin
from googletrans import Translator


class IdseGoogletrans(IdsePlugin):
    def __init__(self) -> None:
        super().__init__()
        self.translator = Translator()

    def translate(self, original: str) -> str:
        return self.translator.translate(original, src='en', dest='ja').text
