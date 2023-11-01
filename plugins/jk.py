from api.plugin_base import PluginBase

class SayJokePlugin(PluginBase):

    def can_handle(self, text):
        return "joke" in text.lower()

    def handle(self, text):
        print("Hello meme loard!")


