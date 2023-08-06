from omnitools import file_size, randstr, p, encodeURIComponent, def_template
from sfx7z.utils import FILTER_COPY, new_multi_volume_fo, lzma_filter
from .utils import glob_fns, glob_fns_size, start_job
from ucefcdownloader import UCEFCDownloader
from userscloud import UC_API, UC_FTP
from py7zr import SevenZipFile
import threadwrapper
import threading
import requests
import zipfile
import random
import shutil
import json
import time
import os
import re


class UCEFCUploader:
    completed_path = "completed"
    failed_path = "failed"
    ready_path = "ready"
    compilation_path = "compilation"
    small_size = 8*1024*1024
    split_size = 4*1023*1023*1023
    max_size = 10*1024*1024*1024

    def __init__(self, domain, credentials):
        os.makedirs(self.completed_path, exist_ok=True)
        os.makedirs(self.failed_path, exist_ok=True)
        os.makedirs(self.ready_path, exist_ok=True)
        os.makedirs(self.compilation_path, exist_ok=True)
        self.domain = domain
        self.api_base = self.domain + "/api"
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "Chrome/96.0.13.59232"})
        self.s.post(self.api_base, {"op": "login", "username": credentials[0], "password": credentials[1]})
        self.root_folder = self.s.post(self.api_base, {"op": "get_folders"}).json()[0]

    def __del__(self):
        self.s.get(self.domain + "/logout")

    @staticmethod
    def fp_to_upload_fp(fp):
        return re.sub(r"^([A-Za-z]\:\\|[A-Za-z]\:$)", re.escape(os.path.sep), fp).replace(os.path.sep, "/")

    @staticmethod
    def split_file(fp, size):
        p("\r\t\t", fp, size, "splitting files", end="")
        mv_fo = new_multi_volume_fo(fp, volume=UCEFCUploader.split_size, ext_digits=3)
        sz_fo = SevenZipFile(mv_fo, "w", filters=[lzma_filter(id=FILTER_COPY)])
        def job():
            nonlocal sz_fo
            nonlocal mv_fo
            try:
                sz_fo.write(fp, os.path.basename(fp))
                sz_fo.close()
                mv_fo.close()
            except Exception as e:
                try:
                    for _fp in glob_fns(fp):
                        if os.path.isfile(_fp):
                            os.unlink(_fp)
                except:
                    pass
                return e
        result = []
        start_job(def_template(job), result)
        while not result:
            p("\r\t\t", fp, size, "splitting files", "{:.2f}%".format(glob_fns_size(fp)/size*100), end="")
            time.sleep(1)
        if not result[0]:
            return glob_fns(fp)
        else:
            raise result[0]

    @staticmethod
    def process_files(root, relative_path):
        p(root)
        skipped = []
        files = []
        sizes = []
        size = 0
        def is_compilation_zip(e):
            try:
                if file_size(e) < UCEFCUploader.small_size and UCEFCDownloader.check_zipfile(e, False):
                    return True
                raise
            except:
                return False
        for a, b, c in os.walk(os.path.join(root, relative_path)):
            b.sort()
            c.sort()
            for d in c:
                e = os.path.join(a, d)
                if is_compilation_zip(e):
                    skipped.append(e)
                else:
                    files.append(e)
                    sizes.append(file_size(e))
                    size += sizes[-1]/1024/1024/1024
                p("\r\t", e, end="")
        p("\r\t", relative_path, len(files), size, "skipped", len(skipped))
        for i, file in enumerate(files):
            p("\r\t\t", i+1, len(files), file, end="")
            filesize = file_size(file)
            if filesize >= UCEFCUploader.max_size:
                if glob_fns_size(file) < filesize:
                    UCEFCUploader.split_file(file, filesize)
        p()

    @staticmethod
    def upload_with_uc_ftp(root, relative_path, credentials, progress=None, overwrite_same_size=False, **kwargs):
        uc_ftp = UC_FTP(**kwargs)
        uc_ftp.login(credentials)
        db_port = random.randint(40000, 60000)
        p("uc_ftp.init_sqlq started at port {}".format(db_port))
        uc_ftp.init_sqlq(db_port=db_port)
        if uc_ftp.sqlqueue.sql(
            '''
            SELECT COUNT(*)
            FROM `queue`;
            ''',
            (),
            "list"
        )[0][0]:
            uc_ftp.start_upload_worker(
                8 * 1024 * 10,
                progress,
                overwrite_same_size=overwrite_same_size
            )
        else:
            uc_ftp.queue_upload(
                root,
                relative_path,
                8 * 1024 * 10,
                progress,
                overwrite_same_size=overwrite_same_size
            )
            time.sleep(10)
        while True:
            try:
                r = uc_ftp.sqlqueue.sql(
                    '''
                    SELECT COUNT(*)
                    FROM `queue`
                    WHERE `completed`
                    UNION ALL
                    SELECT COUNT(*)
                    FROM `queue`;
                    ''',
                    (),
                    "list"
                )
                if r[1][0] - r[0][0] == 0:
                    break
                if uc_ftp.terminated:
                    raise StopIteration
                p("queue", r[0][0], "/", r[1][0], end="")
                time.sleep(1)
            except KeyboardInterrupt:
                break
            except:
                import traceback
                traceback.print_exc()
                uc_ftp.sqlqueue.backup()
                uc_ftp.c.close()
                uc_ftp.c = UC_FTP(**kwargs).c
                uc_ftp.login(credentials)
                if uc_ftp.terminated:
                    uc_ftp.start_upload_worker(
                        8 * 1024 * 10,
                        progress,
                        overwrite_same_size=overwrite_same_size
                    )
        try:
            p("\r", "waiting worker to stop")
            uc_ftp.stop_upload_worker()
        except:
            pass
        finally:
            p("\r", "closing")
            uc_ftp.close()

    def import_from_userscloud(self, root, relative_path, api_key, fld_id, remote_base="/", files=None):
        def loop_folder(fld_id, path, tw):
            result = uc_api.FolderList(fld_id=fld_id)["result"]
            folders = result["folders"]
            files = result["files"]
            for folder in folders:
                tw.add(job=def_template(loop_folder, folder["fld_id"], os.path.join(path, decode(folder["name"])), tw))
                # loop_folder(folder["fld_id"], os.path.join(path, decode(folder["name"])))
            for file in files:
                decoded = decode(file["name"])
                remote_files.append([os.path.join(path, decoded), file["file_code"]])
                p("\r\t", "remote", remote_files[-1])
        def get_files():
            r = []
            p("\r", "fetching local files")
            for a, b, c in os.walk(os.path.join(root, relative_path)):
                for d in c:
                    r.append([
                        os.path.join(a, d),
                        None
                    ])
                    p("\r\t", "local", r[-1])
            return r
        p("importing files from userscloud")
        uc_api = UC_API(key=api_key)
        decode = UC_FTP.decode_file_line
        remote_files = []
        r = []
        def job():
            tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**3))
            tw.add(job=def_template(loop_folder, fld_id, os.path.join(root, relative_path), tw))
            tw.wait()
        start_job(def_template(job), r)
        big_files = dict(files or get_files())
        while not r:
            time.sleep(1)
        map = [_[0] for _ in remote_files]
        dups = [_ for _ in remote_files if map.count(_[0]) > 1]
        if dups:
            FileExistsError("same files were uploaded twice?\nthis is not supposed to happen\nplease check", dups)
        remote_files = dict(remote_files)
        datum = []
        for file in big_files.items():
            fp = file[0]
            if fp not in remote_files:
                raise FileNotFoundError
            code = remote_files[fp]
            dir = self.fp_to_upload_fp(os.path.join(remote_base, os.path.dirname(fp).replace(root, "")[1:]))
            hash = file[1] or "not_available"
            name = os.path.basename(fp)
            try:
                size = os.path.getsize(fp)
            except FileNotFoundError as e:
                mv_id = re.search(r"\.7z\.([0-9]{3})$", name)
                if mv_id:
                    try:
                        size_o = os.path.getsize(fp[:-4])
                    except FileNotFoundError:
                        size_o = os.path.getsize(fp[:-7])
                    part = int(mv_id[1])
                    size = self.split_size*part
                    if size > size_o:
                        size = size_o-self.split_size*(part-1)
                    else:
                        size = self.split_size
                else:
                    raise e
            data = {
                "op": "import_file",
                "code": code,
                "size": size,
                "hash": hash,
                "path": dir,
                "name": name
            }
            datum.append(data)
        p()
        p("importing files to ucefc")
        tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**1))
        for i, data in enumerate(datum):
            def job(i, data):
                p(i+1, len(datum), data)
                r = self.s.post(self.api_base, data)
                if r.status_code != 200:
                    raise ConnectionError
            tw.add(job=def_template(job, i, data))
        tw.wait()

    def generate_compilation(self, compilation):
        filename = compilation["display_name"] + ".zip"
        relative_path = compilation["relative_path"]
        _root = compilation["root"]
        drive = compilation["drive"]
        zip_fp = os.path.join(self.compilation_path, _root.strip("/"), relative_path, filename)
        os.makedirs(os.path.dirname(zip_fp), exist_ok=True)
        zip_fo = zipfile.ZipFile(zip_fp, "w")
        for file in compilation["files"]:
            fp = file[0].lstrip("/") + ".txt"
            zip_fo.writestr(fp, file[1].encode())
        h2d = b"http://code.foxe6.kozow.com/ucefcdownloader/executable/"
        h2dn = "how_to_download.txt"
        zip_fo.writestr(h2dn, h2d)
        zip_fo.close()
        session = randstr(32)
        query = "?session={}&folder={}&path={}&length={}&overwrite=1".format(
            session,
            self.root_folder,
            encodeURIComponent(self.fp_to_upload_fp(os.path.join(_root, relative_path))),
            file_size(zip_fp)
        )
        url = self.api_base + "/{}{}".format(filename, query)
        r = self.s.post(url, data=open(zip_fp, "rb"))
        if r.status_code == 200:
            return r.status_code, r.json()
        else:
            return r.status_code, r.content.decode()

    def generate_ready_compilation(self):
        for fn in os.listdir(self.ready_path):
            fp = os.path.join(self.ready_path, fn)
            compilation = json.loads(open(fp, "rb").read().decode())
            p("\t", "generating compilation", compilation["display_name"], end="")
            r = self.generate_compilation(compilation)
            if r[0] == 200:
                shutil.move(fp, os.path.join(self.completed_path, fn))
                p("\r\t", "generated compilation", compilation["display_name"], self.domain+"/"+r[1]["id"])
            else:
                shutil.move(fp, os.path.join(self.failed_path, fn))
                p("\r\t", "manual compilation", compilation["relative_path"], error=True)






