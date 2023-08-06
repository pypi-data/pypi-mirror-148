class BasePlugin:
    requirements = []

    def __init__(self):
        self.name = self.__class__.__name__
        self.miner = None
        self.logger = None  # Plugin Logger will be inited in prepare stage

    def prepare(self, miner, *args, **kwargs):
        # Can be used for Monkey Patch Operations
        self.miner = miner

    # Plugin Data Begin
    def load_state_dict(self, state):
        pass

    def state_dict(self):
        return {}

    # Plugin Data End

    def set_miner(self, miner):
        """
        This function is deprecated.
        :param miner:
        :return:
        """
        self.miner = miner

    # Hook Functions Begin
    def before_init(self, *args, **kwargs):
        self.logger = self.miner.get_logger(self.name)

    def after_init(self, *args, **kwargs):
        pass

    def before_train_epoch_start(self, *args, **kwargs):
        pass

    def before_train_iteration_start(self, *args, **kwargs):
        pass

    def after_train_iteration_end(self, *args, **kwargs):
        pass

    def after_train_epoch_end(self, *args, **kwargs):
        pass

    def before_val_epoch_start(self, *args, **kwargs):
        pass

    def before_val_iteration_start(self, *args, **kwargs):
        pass

    def after_val_iteration_ended(self, *args, **kwargs):
        pass

    def after_val_epoch_end(self, *args, **kwargs):
        pass

    def before_checkpoint_persisted(self, *args, **kwargs):
        pass

    def after_checkpoint_persisted(self, *args, **kwargs):
        pass

    def before_quit(self, *args, **kwargs):
        pass


class PluginManager:
    def __init__(self, miner, plugins: list):
        self.miner = miner
        if plugins:
            self.plugins = plugins
            self.plugin_names = [i.name for i in self.plugins]
            self.maper = dict(zip(self.plugin_names, self.plugins))
            self.prepare()  # Prepare is the earliest
            self.logger = miner.get_logger("PluginManager")
            self.check_requirements()
        else:
            self.plugins = []

    def check_requirements(self):
        """
        Check Requirements of each Plugins
         - Requirements are set in restrict string
        :return:
        """
        error = False
        for p in self.plugins:
            self.logger.debug(f"Checking Requirements of {p.name}.")
            for r in p.requirements:
                if r not in self.plugin_names:
                    self.logger.error(f"Requirement {r} of {p.name} is not Find.")
                    error = True
        if not error:
            self.logger.info("Successfully Passed Plugin Requirements Check with no Errors.")
        # TODO: Try to import Unmet needs

    def status(self):
        """
        Print the Status of all registered Plugins
        :return:
        """
        self.logger.info(f"Registered Plugins:{self.plugins}")

    def call(self, hook, **payload):
        """
        Call Hook Functions
        :return:
        """
        for plugin in self.plugins:
            getattr(plugin, hook)(miner=self, **payload)  # !!! `miner=self` is totally different with just `self`

    def prepare(self):
        """
        prepare a given Plugin
        :return:
        """
        for p in self.plugins:
            p.prepare(self.miner)

    def load(self, checkpoint):
        # load plugin states
        for plugin in self.plugins:
            key = f"__plugin.{plugin.__class__.__name__}__"
            plugin.load_state_dict(checkpoint.get(key, {}))

    def save(self):
        temp = {}
        for p in self.plugins:
            temp[f"__plugin.{p.__class__.__name__}__"] = p.state_dict()
        return temp

    def get(self, name):
        """
        Get A Plugin From Plugin Manager.
        :param string name: Plugin name
        :return:
        """
        return self.maper[name]
