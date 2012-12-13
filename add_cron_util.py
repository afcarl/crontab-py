#!/usr/bin/env python

import logging
import os
import os
from crontab import CronTab

DEFAULT_LOG_DIR = '/tmp/log'

class CronJob():
    def __init__(self, name, schedule, cmd, logfile=None, logdir=DEFAULT_LOG_DIR):
        """
        If logfile is None, date-dependent file is used. 
        The logfile has precedence over logdir
        """
        self.name = name
        self.schedule = schedule
        self.cmd = cmd
        self.logfile = logfile
        self.logdir = os.path.expanduser(logdir)

        if not os.path.isdir(logdir):
            logging.info("Recursively creating directory: %s" % logdir)
            os.makedirs(logdir)


def merge_cron_jobs(job_lst, is_write):
    #my_cron_job '0 3 * * Tue', 
    #sun mon tue wed thu fri sat sun

    cron = CronTab()

    for l in job_lst:
        cron.remove_job(l.name)
        if l.logfile is None:
            logfile = os.path.join(l.logdir, l.name + r'.`date +\%Y\%m\%d\%H\%M\%S`.log')
        else:
            logfile = l.logfile

        cron.add_job('%-15s echo %s &>/dev/null && %s &>%s' % (l.schedule, l.name, l.cmd, logfile))

    cron.write(prefix="cron.", is_write=is_write)

    

