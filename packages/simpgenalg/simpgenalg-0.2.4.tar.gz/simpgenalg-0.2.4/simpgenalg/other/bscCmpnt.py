from simpcfg import config
from simptoolbox import toolbox
from .cstm_logger import cstm_logger

class basicComponent():

    __slots__ = ('config', 'toolbox', 'log', 'runsafe')

    def __init__(self, *args, **kargs):

        self.config = kargs.get('config')
        if self.config is None:
            self.config = config(kargs.get('config_name', 'simpgenalg'))

        # Try to load in logger or use a basic custom logger
        self.log = kargs.get('logger')
        if self.log is None:
            log_lvl = kargs.get('log_lvl')
            if log_lvl is None:
                log_lvl = self.config.get('log_lvl',20,dtype=int)
            self.log = cstm_logger(log_lvl=log_lvl)

        self.toolbox = kargs.get('toolbox')
        if self.toolbox is None:
            self.toolbox = toolbox(kargs.get('toolbox_name', 'simpgenalg'))

        self.runsafe = kargs.get('runsafe', None)

        if self.runsafe is None:
            try:
                self.runsafe = self.config.get('runsafe', True, dtype=bool)
            except:
                self.runsafe = True

    def __del__(self):
        self.log, self.config, self.toolbox, self.runsafe = \
                                                    None, None, None, None
        #super().__del__()

    def _is_iter(self, obj):
        try:
            iter(obj)
            return True
        except:
            return False

    def _is_hash(self, obj):
        try:
            hash(obj)
            return True
        except:
            return False

    def get_log(self):
        return self.log

    def get_toolbox(self):
        return self.toolbox

    def get_config(self):
        return self.config

    def get_runsafe(self):
        return self.runsafe
