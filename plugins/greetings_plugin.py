from api.plugin_base import PluginBase

class GreetingsPlugin(PluginBase):

    def can_handle(self, text):
        if "hello" in text.lower():
            return True

    def handle(self, text):
        print("Hello there!")


