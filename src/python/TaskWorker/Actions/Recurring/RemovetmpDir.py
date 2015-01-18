import os
import time
import shutil

from datetime import date

from TaskWorker.Actions.Recurring.BaseRecurringAction import BaseRecurringAction

days = 86400*30

class RemovetmpDir(BaseRecurringAction):
    pollingTime = 60*24 #minutes

    def _execute(self, resthost, resturi, config, task):
        self.logger.info('Checking for directory older than 30 days..')
        now = time.time()
        for dirpath, dirnames, filenames in os.walk(config.TaskWorker.scratchDir):
            for dir in dirnames:
                timestamp = os.path.getmtime(os.path.join(dirpath,dir))
                if now-days > timestamp:
                    try:
                        self.logger.info('Removing:')
                        self.logger.info(os.path.join(dirpath,dir))
                        shutil.rmtree(os.path.join(dirpath,dir))
                    except Exception, e:
                        self.logger.exception(e)
                    else:
                        self.logger.info('Directory removed.')
