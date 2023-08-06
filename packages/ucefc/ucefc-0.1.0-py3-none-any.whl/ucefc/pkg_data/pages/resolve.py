from omnitools import encodeURI
from dwa import *
import random


server_name = "resolve"


class api_page(handlers.SuccessHandler):
    server = server_name

    def check_xsrf_cookie(self):
        pass

    @tornado.concurrent.run_on_executor
    def _get(self, code):
        domain = self.uc_webs[0].domain
        ss = [uc_web.s for uc_web in self.uc_webs]
        random.SystemRandom().shuffle(ss)
        for s in ss:
            try:
                r = s.post(domain + "/" + code, {"op": "download2", "id": code}, allow_redirects=False)
                if 300 < r.status_code < 400:
                    url = r.headers["Location"]
                    try:
                        url = bytes([ord(_) for _ in url]).decode()
                    except (UnicodeDecodeError, ValueError):
                        pass
                    return encodeURI(url)
            except:
                pass

    @tornado.gen.coroutine
    def get(self, *args):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET')
        r = yield self._get(args[0])
        if r:
            self.set_header("Content-Type", "text/plain")
            self.write(r)
            self.finish()
        else:
            raise tornado.web.HTTPError()


def get_settings():
    return [
        server_name,
        [
            [r"/([a-z0-9]+)", api_page],
        ]
    ]

