from omnitools import file_size
import traceback
import threading
import os


def glob_fns(fp):
    name = os.path.basename(fp)
    dir = os.path.dirname(fp)
    return [os.path.join(dir, _) for _ in os.listdir(dir) if _.startswith(name + ".")]


def glob_fns_size(fp):
    return sum([file_size(_) for _ in glob_fns(fp)])


def start_job(job, result):
    def _job():
        try:
            result.append(job())
        except:
            result.append([400, traceback.format_exc()])

    t = threading.Thread(target=_job)
    t.daemon = True
    t.start()
