from dwa import *


class change_password_worker(workers.once_inverted_base_worker):
    def job(self) -> None:
        fp = os.path.join(self.app_root, "new_password.json")
        if os.path.isfile(fp):
            try:
                pw = json.loads(open(fp, "rb").read().decode())
                if not isinstance(pw, list):
                    raise ValueError("{} is not a list".join(fp))
                if not pw or pw and not isinstance(pw[0], list):
                    raise ValueError("{} is not a list of lists".join(fp))
                self.sql(
                    '''
                    UPDATE `owners`
                    SET `hash` = ?
                    WHERE `name` = ?;
                    ''',
                    tuple([tuple(_) for _ in pw])
                )
            except:
                traceback.print_exc()
            os.remove(fp)
        print("[workers] change_password_worker done")


class dummy_api_worker(workers.once_inverted_base_worker):
    api_keys_fp = None

    def job(self) -> None:
        import userscloud
        self.export_functions = {
            "get_dummy_api": self.get_dummy_api,
            "clone_file_public": lambda x: userscloud.UC_API(key=self.get_dummy_api()).FileClone(x),
        }
        fp = os.path.join(self.app_root, "dummy_api.txt")
        if os.path.isfile(fp):
            _fp = open(fp, "rb").read().decode()
            os.remove(fp)
            if os.path.isfile(_fp):
                self.api_keys_fp = _fp
        print("[workers] dummy_api_worker done")

    def get_dummy_api(self):
        if self.api_keys_fp:
            try:
                api_keys = json.loads(open(self.api_keys_fp, "rb").read().decode())
                if not isinstance(api_keys, list):
                    raise ValueError("{} is not a list".join(self.api_keys_fp))
            except:
                traceback.print_exc()
                return
            if api_keys:
                import random
                return random.SystemRandom().choice(api_keys)
            else:
                return
        else:
            return


class smart_validate_code_worker(workers.base_worker):
    def job(self):
        r = self.sql(
            '''
            SELECT `code`, `id`
            FROM `files`
            ORDER BY RANDOM()
            LIMIT 1;
            ''',
            (),
            "list"
        )
        try:
            rr = requests.get(self.uc_webs[0].domain+"/"+r[0][0])
            if rr.status_code == 200:
                if r[0][0].encode() not in rr.content:
                    open(os.path.join(self.app_root, "invalid_code.txt"), "ab").write((r[0][1]+"\n").encode())
                    print("[workers]", "smart_validate_code_worker", r[0][1], "invalid", flush=True)
        except:
            pass
        for i in range(0, 30):
            if self.terminate:
                return
            time.sleep(1)


class smart_renew_code_worker(workers.base_worker):
    def job2(self, limit):
        r = self.sql(
            '''
            SELECT `code`, `id`
            FROM `files`
            WHERE DATETIME('NOW', 'LOCALTIME') >= DATETIME(`date`, '+{} days')
            LIMIT 1;
            '''.format(int(limit)),
            (),
            "list"
        )
        if renew_code_worker.pending:
            return 
        if r:
            code, id = r[0]
            try:
                result = self.uc_api.FileClone(code)["result"]
                if result["filecode"].encode() not in self.uc_api.s.get(result["url"], timeout=60*2).content:
                    raise Exception(result["url"], "missing signature")
                data = (result["filecode"], omnitools.dt2yyyymmddhhmmss(hms_delimiter=":"), id)
                self.sql(
                    '''
                    UPDATE `files`
                    SET `code` = ?,
                    `date` = ?
                    WHERE `id` = ?;
                    ''',
                    data
                )
                print("\r[workers]", "smart_renew_code_worker", id, end="", flush=True)
                return True
            except Exception as e:
                return e
        return False

    def job(self) -> None:
        for limit in range(21-1, 7-1, -1):
            r = self.job2(limit)
            if r:
                if isinstance(r, Exception):
                    print("\r[workers]", "smart_renew_code_worker", type(r), str(r), flush=True)
                break
        for i in range(0, 30):
            if self.terminate:
                return
            time.sleep(1)


class renew_code_worker(workers.base_worker):
    pending = 0

    def job(self) -> None:
        r = self.sql(
            '''
            SELECT `code`, `id`
            FROM `files`
            WHERE DATETIME('NOW', 'LOCALTIME') >= DATETIME(`date`, '+21 days')
            LIMIT 1;
            ''',
            (),
            "list"
        )
        if r:
            if not self.pending:
                self.pending = self.sql(
                    '''
                    SELECT COUNT(*)
                    FROM `files`
                    WHERE DATETIME('NOW', 'LOCALTIME') >= DATETIME(`date`, '+21 days');
                    ''',
                    (),
                    "list"
                )[0][0]
            code, id = r[0]
            try:
                print("\r[workers] renew_code_worker {} items left".format(self.pending), end="", flush=True)
                result = self.uc_api.FileClone(code)["result"]
                if result["filecode"].encode() not in self.uc_api.s.get(result["url"], timeout=60*2).content:
                    raise
                data = (result["filecode"], omnitools.dt2yyyymmddhhmmss(hms_delimiter=":"), id)
                self.sql(
                    '''
                    UPDATE `files`
                    SET `code` = ?,
                    `date` = ?
                    WHERE `id` = ?;
                    ''',
                    data
                )
                self.pending -= 1
                if not self.pending:
                    print("\r[workers] renew_code_worker done", flush=True)
                return
            except:
                pass
        for i in range(0, 30):
            if self.terminate:
                return
            time.sleep(1)


class gen_sitemap_worker(workers.inverted_base_worker):
    def job(self) -> None:
        def loop_folder(id, path):
            if self.terminate:
                return
            r = self.sql(
                '''
                SELECT `id`, `name`
                FROM `folders`
                WHERE `parent` = ?;
                ''',
                (id,),
                "list"
            )
            for _ in r:
                loop_folder(_[0], path + _[1] + "/")
            r = self.sql(
                '''
                SELECT `id`, `name`, `hash`, `size`
                FROM `files`
                WHERE `parent` = ?;
                ''',
                (id,),
                "list"
            )
            for _ in r:
                _[1] = path + _[1]
                public_files.append(_)
        template = '''\
<html>
<head>
<title>Index | &#x01D59A;&#x01D588;&#x01D58A;&#x01D58B;&#x01D588;</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
<link href="./index.css" rel="stylesheet"/>
</head>
<body>
<h1>
    Loading<br/>
    Page is huge so please wait<br/>
    This should take around 10 seconds to render
</h1>
<h2>Index on &#x01D59A;&#x01D588;&#x01D58A;&#x01D58B;&#x01D588;</h2>
{}
<script src="./index.js"></script>
</body>
</html>'''
        table = '''<table>
<tr>
<th>folder</th><th>name</th><th>size</th><th>hash</th><th>link</th>
</tr>
{}
</table>'''
        tr = '''<tr>
{}
<td>{}</td>
<td>{} B</td>
<td>{}</td>
<td><a href='./{}' target='_blank'>&#x01F517;</a></td>
</tr>'''
        table2 = '''<table>
<tr>
<th class='dn'>folder</th><th>name</th><th>size</th><th class='dn'>hash</th><th>link</th>
</tr>
{}
</table>'''
        tr2 = '''<tr>
{}
<td>{}</td>
<td>{} B</td>
<td class='dn'>{}</td>
<td><a href='./{}' target='_blank'>&#x01F517;</a></td>
</tr>'''
        r = self.sql(
            '''
            SELECT `id`, `name`
            FROM `folders`
            WHERE `public`;
            ''',
            (),
            "list"
        )
        sitemap = []
        public_files = []
        index = ""
        for i, row in enumerate(r):
            id = row[0]
            loop_folder(id, "/" + row[1] + "/")
            if self.terminate:
                return
            public_files.sort(key=lambda x: [os.path.dirname(x[1]), os.path.basename(x[1])])
            _ = ""
            prev_folder = None
            chunk = ""
            rowspan = 1
            sizes = 0
            for id, name, hash, size in public_files:
                sizes += size
                folder = "/".join(name.split("/")[:-1])
                name = name.split("/")[-1]
                if folder != prev_folder:
                    _ += chunk.replace("<rowspan>", str(rowspan))
                    chunk = ""
                    rowspan = 1
                    chunk += tr.format("<td rowspan='<rowspan>'>{}</td>".format(folder), name, size, hash, id)
                else:
                    rowspan += 1
                    chunk += tr.format("", name, size, hash, id)
                prev_folder = folder
            index += tr2.format("<td rowspan='1' class='dn'></td>", row[1], sizes, "", "index-{}.html".format(row[0]))
            if chunk:
                _ += chunk.replace("<rowspan>", str(rowspan))
            sitemap.append("index-{}.html".format(row[0]))
            open(os.path.join(self.app_root, "root", "index-{}.html".format(row[0])), "wb").write(template.format(table.format(_)).encode())
            chunk = ""
            _ = ""
            public_files = []
            open(os.path.join(self.app_root, "root", "index.html"), "wb").write(template.format(table2.format(index)).encode())
        index = ""
        xml = '''<?xml version="1.0" encoding="UTF-8"?>'''
        xml += '''<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
        url = '''
    <url>
        <loc>{}/{{}}</loc>
        <priority>{{}}</priority>
    </url>'''.format("http://"+self.cookies_domain[1:])
        sitemap.insert(0, "")
        sitemap.insert(1, "index.html")
        for _ in sitemap:
            xml += url.format(_, "1.0")
        xml += '''</urlset>'''
        open(os.path.join(self.app_root, "root", "sitemap.xml"), "wb").write(xml.encode())
        xml = ""
        print("[workers] gen_sitemap_worker done")



