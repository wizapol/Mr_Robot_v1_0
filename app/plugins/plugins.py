import os
import importlib

class PluginManager:
    def __init__(self):
        self.plugins = []
        self.plugins_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plugins')
        self._load_plugins()

    def _load_plugins(self):
        plugin_files = [f[:-3] for f in os.listdir(self.plugins_path) if f.endswith('.py') and f != '__init__.py']
        for plugin_file in plugin_files:
            module = importlib.import_module(f'app.plugins.{plugin_file}')
            plugin_class = getattr(module, 'Plugin', None)
            if plugin_class:
                self.plugins.append(plugin_class())

    def apply_plugins(self, text):
        for plugin in self.plugins:
            text = plugin.process(text)
        return text
