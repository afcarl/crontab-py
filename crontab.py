#!/usr/bin/env python

import sys
import logging
import os
import tempfile

class CronTab():
    def __init__(self):
        self.job_lst = []
        self.read()
        logging.debug(self.job_lst)

    def read_execute(self):
        return "crontab -l"

    def read(self):
        lines = os.popen(self.read_execute()).readlines()
        for line in lines:
            self.job_lst.append(line.strip())
    
    def write(self, prefix="cron_py", is_write=False):
        with tempfile.NamedTemporaryFile(prefix= prefix, dir="/tmp/") as wfh:
            print >>wfh, "\n" . join(self.job_lst)
            wfh.flush()
            logging.debug("temporary file: " + wfh.name)

            print >>sys.stderr, ""
            os.system("cat %s" % wfh.name)
            print >>sys.stderr, ""
            if is_write:
                os.system("crontab %s"% wfh.name)

    def add_job(self, ln):
        self.job_lst.append(ln)

    def remove_job(self, search_term):
        found_lst = []
        for i, job in enumerate(self.job_lst):
            if job[0] == '#':
                continue
            if job.find(search_term) >= 0:
                found_lst.append(i)
        
        if len(found_lst) == 0:
            pass
        elif len(found_lst) == 1:
            self.job_lst.pop(found_lst[0])
        else:
            raise Exception("More than one entry found for search-term: %s" % search_term)





    

