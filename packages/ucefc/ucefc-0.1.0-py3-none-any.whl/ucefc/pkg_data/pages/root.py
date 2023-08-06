from omnitools import randstr
from hashlib import sha256
from dwa import *
import threading
import time
import copy
import math
import json


server_name = "root"


class index_page(handlers.HTML):
    server = server_name
    file_name = "ucefc"

    def get_what(self, og_title=None, og_description=None):
        title = ""
        meta_desc = "ucefc, userscloud encrypted file copy, a foxe6 project"
        if self.path_args:
            id = self.path_args[0]
            r = self.sql(
                '''
                SELECT `date`, `name`, `size`, `hash`
                FROM `files`
                WHERE `id` = ?;
                ''',
                (id,),
                "list"
            )
            if r:
                date, name, size, hash = r[0]
                title = "{} | ".format(name)
                meta_desc = "Name: {} , Size: {} , Hash: {} , Date: {}".format(name, size, hash, date)
        return tornado.template.Loader(self.app_root).load("{}.html".format(self.file_name)).generate(
            title=title,
            meta_desc=meta_desc,
        )


class api_page(handlers.AJAX):
    server = server_name
    api_name = "ucefc"
    # sessions = {}
    # abort_relays = {}
    # relay_workers = {}
    # free_var = {"sessions": sessions, "abort_relays": abort_relays, "relay_workers": relay_workers}

    def check_xsrf_cookie(self):
        pass

    def get(self):
        raise tornado.web.HTTPError(405)


# @tornado.web.stream_request_body
# class upload_page(handlers.SuccessHandler):
#     server = server_name
#     GB = 1024*1024*1024
#     max_size = 10*GB
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.request.connection.set_max_body_size(self.max_size)
#         self.relayio = None
#         # self.ib = None
#         self.clen = -1
#         self.recv = 0
#         self.progress = 0
#         self.result = None
#         self.hash = None
#         self.chash = None
#         self.session = None
#         # self.hit_ib = 4
#         # self.arg_name = None
#         # self.arg_val = b""
#         # self.multi_args = []
#         self.tmpio = None
#         self.folder = None
#
#     def check_xsrf_cookie(self):
#         pass
#
#     def relay_upload_worker(self, session):
#         try:
#             try:
#                 api_page.relay_workers[session].name = "uploading"
#                 import random
#                 uc_web = random.SystemRandom().choice(self.uc_webs)
#                 api_page.abort_relays[session] = uc_web.upload_file_kill
#                 url = uc_web.upload_file(0, self.relayio).split("/")[-1]
#             except Exception as e:
#                 # print(session, api_page.relay_workers[session], e, flush=True)
#                 self.result = e
#                 return
#             r = None
#             try:
#                 api_page.relay_workers[session].name = "cloning"
#                 r = self.uc_api.FileClone(url)
#                 self.result = r["result"]["filecode"]
#             except Exception as e:
#                 # print(r, e, flush=True)
#                 self.result = Exception("failed to clone file, please re upload")
#         finally:
#             self.progress = 101
#             if session in api_page.relay_workers:
#                 api_page.relay_workers.pop(session)
#             if session in api_page.abort_relays:
#                 api_page.abort_relays.pop(session)()
#
#     def initiate(self):
#         import dwa.utils
#         params = dwa.utils.parse_params(self.request.arguments.items())
#         self.clen = int(params["length"][0])
#         try:
#             self.chash = params["hash"][0]
#         except:
#             pass
#         if int(self.clen) == 0:
#             self.write_error(400, msg="Empty Content")
#             return
#         session = self.get_cookie("session")
#         r = self.sql(
#             '''
#             SELECT `owners`.`id`
#             FROM `sessions`
#             JOIN `owners`
#             ON `sessions`.`owner` = `owners`.`id`
#             WHERE `sessions`.`id` = ?;
#             ''',
#             (session,),
#             "list"
#         )
#         if not r:
#             self.set_cookie("session", "", -1)
#             self.write_error(401, msg="Unauthorized")
#             return
#         owner_id = r[0][0]
#         self.folder = int(params["folder"][0])
#         r = self.sql(
#             '''
#             SELECT ROWID
#             FROM `folders`
#             WHERE `id` = ?
#             AND `owner` = ?;
#             ''',
#             (self.folder, owner_id),
#             "list"
#         )
#         if not r:
#             self.set_cookie("session", "", -1)
#             self.write_error(403, msg="Forbidden")
#             return
#         self.session = params["session"][0]
#         paths = params["path"][0].split("/")
#         if not paths[0]:
#             paths.pop(0)
#         if not paths[-1]:
#             paths.pop()
#         _paths = copy.deepcopy(paths)
#         create_paths = []
#         while _paths:
#             path = _paths.pop(0)
#             r = self.sql(
#                 '''
#                 SELECT `id`
#                 FROM `folders`
#                 WHERE `name` = ?
#                 AND `parent` = ?
#                 AND `owner` = ?;
#                 ''',
#                 (path, self.folder, owner_id),
#                 "list"
#             )
#             if not r:
#                 create_paths = [path]+_paths
#                 break
#             else:
#                 self.folder = r[0][0]
#         for path in create_paths:
#             self.sql(
#                 '''
#                 INSERT INTO `folders` (`name`, `owner`, `parent`, `public`)
#                 VALUES (?, ?, ?, 0);
#                 ''',
#                 (path, owner_id, self.folder)
#             )
#             self.folder = self.sql(
#                 '''
#                 SELECT `id`
#                 FROM `folders`
#                 WHERE `name` = ?
#                 AND `parent` = ?
#                 AND `owner` = ?;
#                 ''',
#                 (path, self.folder, owner_id),
#                 "list"
#             )[0][0]
#         overwrite = "overwrite" in params
#         r = self.sql(
#             '''
#             SELECT `id`, `hash`, `size`
#             FROM `files`
#             WHERE `name` = ?
#             AND `parent` = ?;
#             ''',
#             (self.path_args[0], self.folder),
#             "list"
#         )
#         if r:
#             if not overwrite:
#                 if self.chash and self.chash != r[0][1]:
#                     self.sql(
#                         '''
#                         DELETE FROM `files`
#                         WHERE `id` = ?;
#                         ''',
#                         (r[0][0],)
#                     )
#                 elif self.clen == r[0][2]:
#                     result = {
#                         "id": r[0][0],
#                         "name": self.path_args[0],
#                         "hash": r[0][1],
#                         "size": r[0][2],
#                     }
#                     self.write_error(409, msg=json.dumps(result))
#                     return
#                 else:
#                     self.sql(
#                         '''
#                         DELETE FROM `files`
#                         WHERE `id` = ?;
#                         ''',
#                         (r[0][0],)
#                     )
#             elif overwrite:
#                 if self.chash and self.chash == r[0][1]:
#                     result = {
#                         "id": r[0][0],
#                         "name": self.path_args[0],
#                         "hash": r[0][1],
#                         "size": r[0][2],
#                     }
#                     self.write_error(409, msg=json.dumps(result))
#                     return
#                 elif self.clen == r[0][2]:
#                     self.sql(
#                         '''
#                         DELETE FROM `files`
#                         WHERE `id` = ?;
#                         ''',
#                         (r[0][0],)
#                     )
#                 else:
#                     self.sql(
#                         '''
#                         DELETE FROM `files`
#                         WHERE `id` = ?;
#                         ''',
#                         (r[0][0],)
#                     )
#         return True
#
#     def initiate_relay(self):
#         r = self.initiate()
#         if not r:
#             return
#         from ftpfcs.utils import FTPRelayFO
#         # self.ib = self.request.headers["Content-Type"].split("; boundary=")[-1].encode()
#         self.relayio = FTPRelayFO(self.clen)
#         self.relayio.name = self.path_args[0]
#         api_page.sessions[self.session] = [
#             self.relayio.length,
#             lambda: float("{:.2f}".format(self.relayio.tell() / self.relayio.length * 100))
#         ]
#         self.hash = sha256()
#         p = threading.Thread(target=self.relay_upload_worker, args=(self.session,))
#         api_page.relay_workers[self.session] = p
#         p.name = "init"
#         p.daemon = True
#         p.start()
#         p = None
#         return True
#
#     def data_received(self, chunk: bytes):
#         if self.clen == -1:
#             if not self.initiate_relay():
#                 return
#         if not self.relayio:
#             return
#         # if self.relayio.buffer:
#         #     _ = self.relayio.buffer.pop().tobytes()
#         #     self.relayio.parts -= 1
#         # else:
#         #     _ = b""
#         # self.relayio.length -= len(_)
#         # chunk = memoryview(_+chunk)
#         # chunk = memoryview(chunk)
#         # _ = None
#         # while True:
#         #     try:
#         #         pos = chunk.tobytes().index(b"\n")
#         #         _ = chunk[:pos+1].tobytes()
#         #         __ = len(_)
#         #         if self.hit_ib == 4:  # arg_val
#         #             self.read += __
#         #             if __ <= len(self.ib)+2+2+2 and _.strip().startswith(b"--"+self.ib):  # skip ib
#         #                 self.hit_ib = 1
#         #                 if self.arg_name:
#         #                     nl = self.arg_val[-2:]
#         #                     if nl == b"\r\n":
#         #                         self.arg_val = self.arg_val[:-2]
#         #                     elif nl[-1:] == b"\n":
#         #                         self.arg_val = self.arg_val[:-1]
#         #                     self.multi_args.append([self.arg_name, self.arg_val])
#         #                 else:
#         #                     if self.relayio.buffer:
#         #                         lb = self.relayio.buffer.pop().tobytes()
#         #                         self.relayio.parts -= 1
#         #                         self.relayio.length -= len(lb)
#         #                         nl = lb[-2:]
#         #                         if nl == b"\r\n":
#         #                             lb = lb[:-2]
#         #                         elif nl[-1:] == b"\n":
#         #                             lb = lb[:-1]
#         #                         if lb:
#         #                             self.relayio.write(lb)
#         #                 self.arg_val = b""
#         #                 self.arg_name = None
#         #             else:
#         #                 if self.arg_name:
#         #                     self.arg_val += _
#         #                 else:
#         #                     self.relayio.write(_)
#         #         elif self.hit_ib == 1:  # skip disposition
#         #             self.read += __
#         #             _ = {_a.split("=", 1)[0].strip('"'): _a.split("=", 1)[1].strip('"') for _a in _.strip().decode().split("; ")[1:]}
#         #             if "filename" not in _:
#         #                 self.arg_name = _["name"]
#         #                 self.hit_ib = 3
#         #             else:
#         #                 self.hit_ib = 2
#         #                 self.relayio.name = _["filename"]
#         #         elif self.hit_ib == 2:  # skip content-type
#         #             self.read += __
#         #             self.hit_ib = 3
#         #         elif self.hit_ib == 3:  # skipline
#         #             self.read += __
#         #             self.hit_ib = 4
#         #         chunk = chunk[pos+1:]
#         #         _ = None
#         #         __ = None
#         #     except ValueError:
#         #         if chunk:
#         #             self.relayio.write(chunk.tobytes())
#         #         break
#         self.relayio.write(chunk)
#         self.recv += len(chunk)
#         self.hash.update(chunk)
#         if self.clen <= self.recv:
#             self.relayio.close()
#         return
#
#     @tornado.gen.coroutine
#     def get(self, name):
#         r = self.initiate()
#         if not r:
#             return
#         self.set_header("Content-Type", "application/json")
#         self.write(json.dumps(True))
#         yield self.flush()
#
#     # @tornado.gen.coroutine
#     # def post(self, name):
#     #     try:
#     #         if self.relayio:
#     #             prev_tell = 0
#     #             while True:
#     #                 if self.progress is None:
#     #                     raise
#     #                 if self.progress > 100:
#     #                     break
#     #                 tell = self.relayio.tell()
#     #                 if tell != prev_tell:
#     #                     prev_tell = tell
#     #                     self.progress = math.floor(tell/self.relayio.length*100)
#     #                     # self.write("{}\n".format(self.progress))
#     #                     # yield self.flush()
#     #                 yield tornado.gen.sleep(1/2)
#     #     except:
#     #         # traceback.print_exc()
#     #         self.result = None
#     #     if self._finished:
#     #         return
#     #     if not self.result:
#     #         self.result = IOError("relayio '{}' is empty ({})".format(self.relayio, self.progress))
#     #     if not isinstance(self.result, Exception):
#     #         if self.clen != self.recv:
#     #             self.result = Exception("file size not match")
#     #     if not isinstance(self.result, Exception):
#     #         id = randstr(16)
#     #         code = self.result
#     #         hash = self.hash.hexdigest()
#     #         size = self.relayio.length
#     #         try:
#     #             self.sql(
#     #                 '''
#     #                 INSERT INTO `files`
#     #                 VALUES (?, DATETIME('NOW', 'LOCALTIME'), ?, ?, ?, ?, ?);
#     #                 ''',
#     #                 (id, name, size, code, hash, self.folder)
#     #             )
#     #             result = {
#     #                 "id": id,
#     #                 "name": name,
#     #                 "hash": hash,
#     #                 "size": size,
#     #             }
#     #             self.write(json.dumps(result))
#     #             yield self.flush()
#     #         except Exception as e:
#     #             traceback.print_exc()
#     #             self.write_error(500, msg="{}: {}".format(type(e).__name__, e))
#     #     else:
#     #         e = self.result
#     #         e = "{}: {}".format(type(e).__name__, e)
#     #         print(e, flush=True)
#     #         self.write_error(500, msg=e)
#     #     id = None
#     #     hash = None
#     #     code = None
#     #     size = None
#     #     result = None
#     #     prev_tell = None
#
#     def on_finish(self) -> None:
#         super().on_finish()
#         self.on_end()
#
#     def on_connection_close(self) -> None:
#         super().on_connection_close()
#         if self.session in api_page.abort_relays:
#             api_page.abort_relays[self.session]()
#         self.on_end()
#
#     def on_end(self):
#         if self.session in api_page.sessions:
#             api_page.sessions.pop(self.session)
#         if self.session in api_page.relay_workers:
#             if not api_page.relay_workers[self.session].is_alive():
#                 api_page.relay_workers.pop(self.session)
#                 if self.session in api_page.abort_relays:
#                     api_page.abort_relays.pop(self.session)()
#         self.session = None
#         self.folder = None
#         self.relayio = None
#         self.result = None
#         self.hash = None
#         self.chash = None
#         self.clen = None
#         self.recv = None
#         self.progress = None


class static_page(handlers.File):
    server = server_name


class logout_page(handlers.SuccessHandler):
    server = server_name

    @tornado.gen.coroutine
    def get(self):
        session = self.get_cookie("session")
        self.sql(
            '''
            DELETE FROM `sessions`
            WHERE `id` = ?;
            ''',
            (session,)
        )
        self.set_cookie("session", "", -1)
        self.set_status(302)
        self.set_header("Location", "/")
        self.finish()


def get_settings():
    return [
        server_name,
        [
            [r"/logout", logout_page],
            [r"/(index(-[0-9]+)?.(html|css|js))", static_page],
            [r"/(sitemap.xml|robots.txt)", static_page],
            [r"/(google[a-z0-9]{16}.html)", static_page],
            [r"/(ucefc\.(?:js|css))$", static_page],
            # [r"/api/(.+)", upload_page],
            [r"/api", api_page],
            [r"/([A-Za-z0-9]+)?", index_page],
        ]
    ]

