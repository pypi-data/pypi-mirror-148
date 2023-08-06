from datetime import datetime

class cstm_logger():

    def __init__(self, **kargs):
        self.set_log_lvl(kargs.get('log_lvl', 20))

    def set_log_lvl(self, new_log_lvl):
        self.debug, self.info, self.warn, self.critical, self.exception = \
            self._nan, self._nan, self._nan, self._nan, self._nan
        if new_log_lvl <= 10:
            self.debug = self._debug
        if new_log_lvl <= 20:
            self.info = self._info
        if new_log_lvl <= 30:
            self.warn = self._warn
        if new_log_lvl <= 40:
            self.critical = self._critical
        if new_log_lvl <= 50:
            self.exception = self._exception

    def _nan(self, *args, **kargs):
        return

    def _debug(self, s):
        print(datetime.now().strftime('%H:%M:%S')+f' | Debug: {s}')

    def _info(self, s):
        print(datetime.now().strftime('%H:%M:%S')+f' | Info:  {s}')

    def _warn(self, s):
        print(datetime.now().strftime('%H:%M:%S')+f' | WARNING:   {s}')

    def _critical(self, s):
        print(datetime.now().strftime('%H:%M:%S')+f' | CRITICAL:  {s}')

    def _exception(self, s, err=None):
        print(datetime.now().strftime('%H:%M:%S')+f' | EXCEPTION: {s}')
        if err is not None:
            raise err(s)
