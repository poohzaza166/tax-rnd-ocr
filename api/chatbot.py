from .plugin_base import PluginBase
import os
import importlib

class Chatbot:

    def __init__(self):
        self.plugins = []
        self.load_plugins()

    def process(self, text):
        for plugin in self.plugins:
            print(plugin)
            if plugin.can_handle(text):
                plugin.handle(text)

    def register_plugin(self, plugin):
        if not isinstance(plugin, PluginBase):
            raise ValueError("Plugin must extend PluginBase")
        self.plugins.append(plugin)
    def load_plugins(self):
        # Load all plugins in plugins folder
        plugins_folder = '/home/pooh/code/taxocr-urd-project/plugins'
        for file in os.listdir(plugins_folder):
            # print(file)
            if file.endswith('.py'):
                module = importlib.import_module(f'plugins.{file[:-3]}')
                for plugin_name in dir(module):
                    # print(plugin_name)
                    plugin = getattr(module, plugin_name)
                    print(plugin)
                    if issubclass(plugin, PluginBase):
                        print("found plugin")
                        print(f"Importing module {module}")
                        print(f"Registering plugin {plugin}")
                        instance = plugin()
                        self.register_plugin(instance)


