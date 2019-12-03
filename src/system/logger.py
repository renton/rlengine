from src.configs import CONFIG, LOG_MODE_SYSTEM

class Logger():
  def __init__(self):
    self.logs = []

  def add_log(self, log, mode = LOG_MODE_SYSTEM):
    if len(self.logs) >= CONFIG['log_store_max']:
      del self.logs[-1]
    self.logs.insert(0, (log, mode))

  def clear_logs(self):
    del self.logs
    self.logs = []

  def write_logs_to_file(self):
    #TODO STUB
    pass

log = Logger()
