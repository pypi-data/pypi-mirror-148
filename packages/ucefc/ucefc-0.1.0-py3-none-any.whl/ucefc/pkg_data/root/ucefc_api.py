def api_post(*args, **kwargs):
    import json
    import copy
    import time
    from omnitools import randstr, sha512hd
    params = kwargs["params"]
    free_var = kwargs["free_var"]
    cookies = kwargs["cookies"]
    sql = kwargs["sql"]
    export_functions = kwargs["export_functions"]
    jsons = "Not implemented"
    class HTTPError(Exception):
        pass
    class Unauthorized(Exception):
        pass
    class NotFound(Exception):
        pass
    class BadRequest(Exception):
        pass
    def get_owner_id_from_session():
        try:
            session = cookies["get"]("session")
            if not session:
                return None
            return sql(
                '''
                SELECT `owners`.`id`
                FROM `sessions`
                JOIN `owners`
                ON `sessions`.`owner` = `owners`.`id`
                WHERE `sessions`.`id` = ?;
                ''',
                (session,),
                "list"
            )[0][0]
        except:
            raise Unauthorized()
    # def get_relay_progress():
    #     session = params["session"][0]
    #     sessions = free_var["sessions"]
    #     if session not in sessions:
    #         raise NotFound()
    #     progress = sessions[session][1]()
    #     return progress
    # get_server_progress = get_relay_progress
    # def get_relay_info():
    #     def get_speed():
    #         load = 0
    #         for session, (length, progress) in free_var["sessions"].items():
    #             try:
    #                 load += length*progress()/100
    #             except:
    #                 pass
    #         return load
    #     print(free_var)
    #     free_var["relay_workers"] = {k: v for k, v in free_var["relay_workers"].items() if v.is_alive()}
    #     _free_var = {k: len(v) for k, v in free_var.items()}
    #     _free_var["relay_workers"] = [{"state": v.name, "alive": v.is_alive()} for k, v in free_var["relay_workers"].items()]
    #     prev = get_speed()
    #     time.sleep(1)
    #     return {
    #         "speed": get_speed()-prev,
    #         "free_var": _free_var
    #     }
    # def abort_relay():
    #     session = params["session"][0]
    #     abort_relays = free_var["abort_relays"]
    #     if session not in abort_relays:
    #         raise NotFound()
    #     abort_relays[session]()
    #     return True
    # def abort_orphan_relays():
    #     sessions = list(free_var["sessions"].keys())
    #     abort_relays = free_var["abort_relays"]
    #     for k, abort_relay in abort_relays.items():
    #         if k not in sessions:
    #             abort_relay()
    #     return True
    def get_file():
        r = sql(
            '''
            SELECT `name`,
            `size`,
            `hash`,
            `date`
            FROM `files`
            WHERE `id` = ?;
            ''',
            (params["id"][0],)
        )
        if not r:
            raise NotFound()
        return r
    def get_all_folders():
        owner_id = get_owner_id_from_session()
        if not owner_id:
            raise Unauthorized()
        return sql(
            '''
            SELECT `id`, `name`, `parent`
            FROM `folders`
            WHERE `owner` = ?;
            ''',
            (owner_id,),
            "list"
        )
    def get_folders():
        def get_public_folder():
            def check_parent_is_public(_id):
                parent = None
                public = False
                while True:
                    r = sql(
                        '''
                        SELECT `id`, `parent`, `public`
                        FROM `folders`
                        WHERE `id` = ?;
                        ''',
                        (_id,),
                        "list"
                    )
                    if not r:
                        break
                    _id = r[0][1]
                    if not parent:
                        parent = _id
                    if r[0][2]:
                        if id == r[0][0]:
                            parent = None
                        public = True
                        break
                    if not r[0][1]:
                        break
                return public, parent
            public, parent = check_parent_is_public(id)
            if public:
                folders = sql(
                    '''
                    SELECT `id`, `name`, `public`
                    FROM `folders`
                    WHERE `parent` = ?;
                    ''',
                    (id,),
                    "list"
                )
                files = sql(
                    '''
                    SELECT `id`, `name`, `size`, `hash`
                    FROM `files`
                    WHERE `parent` = ?;
                    ''',
                    (id,),
                    "list"
                )
                return [
                    id,
                    folders,
                    files,
                    parent
                ]
            else:
                raise Unauthorized()
        def get_private_folder():
            def check_parent(_id):
                if _id != owner_id:
                    r = sql(
                        '''
                        SELECT `parent`
                        FROM `folders`
                        WHERE `id` = ?
                        AND `owner` = ?;
                        ''',
                        (id, owner_id),
                        "list"
                    )
                    if not r:
                        raise Unauthorized()
                    parent = r[0][0]
                else:
                    parent = None
                return parent
            parent = check_parent(id)
            folders = sql(
                '''
                SELECT `id`, `name`, `public`
                FROM `folders`
                WHERE `owner` = ?
                AND `parent` = ?;
                ''',
                (owner_id, id),
                "list"
            )
            files = sql(
                '''
                SELECT `id`, `name`, `size`, `hash`
                FROM `files`
                WHERE `parent` = ?;
                ''',
                (id,),
                "list"
            )
            return [
                id,
                folders,
                files,
                parent
            ]
        owner_id = get_owner_id_from_session()
        if "id" in params:
            id = int(params["id"][0])
        else:
            id = owner_id
        if not owner_id:
            return get_public_folder()
        else:
            return get_private_folder()
    def get_folder_name():
        r = get_folders()[0]
        if r == get_owner_id_from_session():
            return
        r = sql(
            '''
            SELECT `name`
            FROM `folders`
            WHERE `id` = ?;
            ''',
            (r,),
            "list"
        )
        if not r:
            raise NotFound()
        return r[0][0]
    def folder_access():
        owner_id = get_owner_id_from_session()
        if not owner_id:
            raise Unauthorized()
        folder = int(params["id"][0])
        def check_folder_access(folder):
            r = sql(
                '''
                SELECT `public`
                FROM `folders`
                WHERE `owner` = ?
                AND `id` = ?;
                ''',
                (owner_id, folder),
                "list"
            )
            if not r:
                raise Unauthorized()
            return r[0][0]
        folder_access = check_folder_access(folder)
        sql(
            '''
            UPDATE `folders`
            SET `public` = ?
            WHERE `id` = ?;
            ''',
            (0 if folder_access else 1, folder)
        )
        return True
    def new_folder():
        owner_id = get_owner_id_from_session()
        if not owner_id:
            raise Unauthorized()
        name = params["name"][0]
        parent = int(params["parent"][0])
        def check_parent(parent):
            r = sql(
                '''
                SELECT ROWID
                FROM `folders`
                WHERE `owner` = ?
                AND `id` = ?;
                ''',
                (owner_id, parent),
                "list"
            )
            if not r:
                raise Unauthorized()
        check_parent(parent)
        sql(
            '''
            INSERT INTO `folders` (`name`, `owner`, `parent`, `public`)
            VALUES (?, ?, ?, 0);
            ''',
            (name, owner_id, parent)
        )
        return True
    def remove_file():
        owner_id = get_owner_id_from_session()
        if not owner_id:
            raise Unauthorized()
        def check_files(files):
            for file in files:
                r = sql(
                    '''
                    SELECT 0
                    FROM `files`
                    JOIN `folders`
                    ON `files`.`parent` = `folders`.`id`
                    WHERE `folders`.`owner` = ?
                    AND `files`.`id` = ?;
                    ''',
                    (owner_id, file)
                )
                if not r:
                    raise Unauthorized()
        files = params["id"]
        check_files(files)
        sql(
            '''
            DELETE FROM `files`
            WHERE `id` IN ({});
            '''.format(",".join(["?"]*len(files))),
            tuple(files)
        )
        return True
    def rename_folder():
        owner_id = get_owner_id_from_session()
        if not owner_id:
            raise Unauthorized()
        def check_folder(folder):
            r = sql(
                '''
                SELECT ROWID
                FROM `folders`
                WHERE `owner` = ?
                AND `id` = ?;
                ''',
                (owner_id, folder)
            )
            if not r:
                raise Unauthorized()
        folder = int(params["id"][0])
        check_folder(folder)
        sql(
            '''
            UPDATE `folders`
            SET `name` = ?
            WHERE `id` = ?
            AND `owner` = ?;
            ''',
            (params["name"][0], folder, owner_id)
        )
        return True
    def remove_folder():
        owner_id = get_owner_id_from_session()
        if not owner_id:
            raise Unauthorized()
        def check_folders(folders):
            for folder in folders:
                r = sql(
                    '''
                    SELECT ROWID
                    FROM `folders`
                    WHERE `owner` = ?
                    AND `id` = ?;
                    ''',
                    (owner_id, folder)
                )
                if not r:
                    raise Unauthorized()
        folders = params["id"]
        check_folders(folders)
        sql(
            '''
            DELETE FROM `folders`
            WHERE `id` IN ({})
            AND `id` != ?
            AND `owner` = ?;
            '''.format(",".join(["?"]*len(folders))),
            tuple(folders+[owner_id]*2)
        )
        return True
    def move_file():
        owner_id = get_owner_id_from_session()
        if not owner_id:
            raise Unauthorized()
        folder = int(params["folder"][0])
        ids = params["id"]
        file_ids = [_ for _ in ids if not _.isdigit()]
        folder_ids = [_ for _ in ids if _ not in file_ids]
        q = []
        if file_ids:
            def check_files(file_ids):
                for file_id in file_ids:
                    r = sql(
                        '''
                        SELECT `files`.`id`
                        FROM `files`
                        JOIN `folders`
                        ON `files`.`parent` = `folders`.`id`
                        WHERE `folders`.`owner` = ?
                        AND `files`.`id` = ?;
                        ''',
                        (owner_id, file_id),
                        "list"
                    )
                    if not r:
                        raise Unauthorized()
            def check_folder(folder):
                r = sql(
                    '''
                    SELECT `id`
                    FROM `folders`
                    WHERE `owner` = ?
                    AND `id` = ?;
                    ''',
                    (owner_id, folder),
                    "list"
                )
                if not r:
                    raise Unauthorized()
            check_files(file_ids)
            check_folder(folder)
            q.append([
                '''
                UPDATE `files`
                SET `parent` = ?
                WHERE `id` IN ({});
                '''.format(",".join(["?"]*len(file_ids))),
                tuple([folder]+file_ids)
            ])
        if folder_ids:
            def check_folders(folder_ids):
                for folder_id in folder_ids:
                    r = sql(
                        '''
                        SELECT `id`
                        FROM `folders`
                        WHERE `owner` = ?
                        AND `id` = ?;
                        ''',
                        (owner_id, folder_id),
                        "list"
                    )
                    if not r:
                        raise Unauthorized()
            check_folders(folder_ids)
            q.append([
                '''
                UPDATE `folders`
                SET `parent` = ?
                WHERE `id` IN ({});
                '''.format(",".join(["?"]*len(folder_ids))),
                tuple([folder]+folder_ids)
            ])
        for _sql, _data in q:
            sql(_sql, _data)
        return True
    def clone_file():
        result = sql(
            '''
            SELECT `code`
            FROM `files`
            WHERE `id` = ?;
            ''',
            (params["id"][0],)
        )
        try:
            url = export_functions("clone_file_public", result[0]["code"])["result"]["url"]
            if not url:
                raise
        except:
            raise NotFound()
        return url
    def _check_file(folder=None):
        owner_id = get_owner_id_from_session()
        if not owner_id:
            raise Unauthorized()
        name = params["name"][0]
        if "hash" in params:
            hash = params["hash"][0]
        else:
            hash = "unknown_due_to_imported_file"
        if "size" in params:
            size = int(params["size"][0])
        else:
            size = 0
        if "overwrite" in params:
            overwrite = int(params["overwrite"][0])
        else:
            overwrite = 0
        paths = params["path"][0].split("/")
        if not paths[0]:
            paths.pop(0)
        if not paths[-1]:
            paths.pop()
        def create_paths(folder, paths):
            _paths = copy.deepcopy(paths)
            create_paths = []
            if folder is None:
                folder = owner_id
            while _paths:
                path = _paths.pop(0)
                r = sql(
                    '''
                    SELECT `id`
                    FROM `folders`
                    WHERE `name` = ?
                    AND `parent` = ?
                    AND `owner` = ?;
                    ''',
                    (path, folder, owner_id),
                    "list"
                )
                if not r:
                    create_paths = [path]+_paths
                    break
                else:
                    folder = r[0][0]
            for path in create_paths:
                sql(
                    '''
                    INSERT INTO `folders` (`name`, `owner`, `parent`, `public`)
                    VALUES (?, ?, ?, 0);
                    ''',
                    (path, owner_id, folder)
                )
                folder = sql(
                    '''
                    SELECT `id`
                    FROM `folders`
                    WHERE `name` = ?
                    AND `parent` = ?
                    AND `owner` = ?;
                    ''',
                    (path, folder, owner_id),
                    "list"
                )[0][0]
            return folder
        id = None
        folder = create_paths(folder, paths)
        r = sql(
            '''
            SELECT `id`, `hash`, `size`
            FROM `files`
            WHERE `name` = ?
            AND `parent` = ?;
            ''',
            (name, folder),
            "list"
        )
        r2 = 1
        # 0: receive file, remove duplicate
        # 1: receive file, no duplicate
        # 2: skip file, return duplicate
        if r:
            id = r[0][0]
            if not overwrite:
                if "_" not in hash and hash != r[0][1]:
                    r2 = 0
                else:
                    r2 = 2
            else:
                if "_" not in hash and hash == r[0][1]:
                    r2 = 2
                else:
                    r2 = 0
        return [name, hash, size, overwrite, folder], r2, id
    def check_file(folder=None):
        r = _check_file(folder)
        return r[2] if r[1] == 2 else None
    def import_file(folder=None):
        owner_id = get_owner_id_from_session()
        if not owner_id:
            raise Unauthorized()
        try:
            code = export_functions("clone_file_private", params["code"][0])["result"]["filecode"]
            if not code:
                raise
        except:
            raise BadRequest()
        id = randstr(16)
        r, r2, did = _check_file(folder)
        name, hash, size, overwrite, folder = r
        def proceed_insert():
            sql(
                '''
                INSERT INTO `files`
                VALUES (?, DATETIME('NOW', 'LOCALTIME'), ?, ?, ?, ?, ?);
                ''',
                (id, name, size, code, hash, folder)
            )
        def delete_dup_file():
            sql(
                '''
                DELETE FROM `files`
                WHERE `id` = ?;
                ''',
                (did,)
            )
        if r2 == 0:
            delete_dup_file()
            proceed_insert()
        elif r2 == 1:
            proceed_insert()
        elif r2 == 2:
            id = did
        return {"id": id}
    def get_dummy_api():
        r = export_functions("get_dummy_api")
        if not r:
            return NotFound()
        return r
    def get_upload_session():
        r = export_functions("get_upload_session")
        try:
            return [
                r["result"],
                r["sess_id"]
            ]
        except:
            return []
    def import2():
        owner_id = get_owner_id_from_session()
        if not owner_id:
            raise Unauthorized()
        folder = int(params["folder"][0])
        if "id" in params:
            def check_folder(folder):
                r = sql(
                    '''
                    SELECT ROWID
                    FROM `folders`
                    WHERE `id` = ?
                    AND `owner` = ?;
                    ''',
                    (folder, owner_id),
                    "list"
                )
                if not r:
                    raise Unauthorized()
            check_folder(folder)
            id = params["id"][0]
            r = sql(
                '''
                SELECT `date`, `name`, `size`, `code`, `hash`
                FROM `files`
                WHERE `id` = ?;
                ''',
                (id,),
                "list"
            )
            if r:
                id = randstr(16)
                sql(
                    '''
                    INSERT INTO `files`
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    ''',
                    tuple([id]+r[0]+[folder])
                )
                return True
            else:
                raise BadRequest()
        elif "dir" in params:
            def loop_folder(id, path):
                r = sql(
                    '''
                    SELECT `id`, `name`
                    FROM `folders`
                    WHERE `parent` = ?;
                    ''',
                    (id,),
                    "list"
                )
                for _ in r:
                    loop_folder(_[0], path+_[1]+"/")
                r = sql(
                    '''
                    SELECT `name`, `size`, `code`, `hash`
                    FROM `files`
                    WHERE `parent` = ?;
                    ''',
                    (id,),
                    "list"
                )
                if not r:
                    return
                for _ in r:
                    params.clear()
                    params.update({
                        "name": [_[0]],
                        "size": [_[1]],
                        "code": [_[2]],
                        "hash": [_[3]],
                        "path": [path],
                    })
                    import_file(folder)
            def check_recursion(_id, dir0):
                # _id = folder
                recursion = _id == dir0
                if recursion:
                    raise BadRequest()
                while True:
                    r = sql(
                        '''
                        SELECT `parent`
                        FROM `folders`
                        WHERE `id` = ?;
                        ''',
                        (_id,),
                        "list"
                    )
                    if not r:
                        break
                    _id = r[0][0]
                    if not _id:
                        break
                    if _id == dir0:
                        recursion = True
                        break
                if recursion:
                    raise BadRequest()
            def check_public(_id):
                # _id = dir0
                public = False
                while True:
                    r = sql(
                        '''
                        SELECT `owner`, `parent`, `public`
                        FROM `folders`
                        WHERE `id` = ?;
                        ''',
                        (_id,),
                        "list"
                    )
                    if not r:
                        break
                    if r[0][0] == owner_id:
                        public = True
                        break
                    _id = r[0][1]
                    if r[0][2]:
                        public = True
                        break
                    if not _id:
                        break
                if not public:
                    raise Unauthorized()
            dir0 = int(params["dir"][0])
            check_public(dir0)
            check_recursion(folder, dir0)
            r = sql(
                '''
                SELECT `name`
                FROM `folders`
                WHERE `id` = ?;
                ''',
                (dir0,),
                "list"
            )
            if not r:
                raise BadRequest()
            loop_folder(dir0, "/{}/".format(r[0][0]))
            return True
        else:
            raise BadRequest()
    def login():
        session = randstr(32)
        owner_id = sql(
            '''
            SELECT `id`
            FROM `owners`
            WHERE `name` = ?
            AND `hash` = ?;
            ''',
            (params["username"][0], sha512hd(sha512hd(sha512hd(params["password"][0])))),
            "list"
        )
        if not owner_id:
            raise Unauthorized()
        owner_id = owner_id[0][0]
        sql(
            '''
            INSERT INTO `sessions`
            VALUES (?, ?, DATETIME('NOW', 'LOCALTIME', '+365 days'));
            ''',
            (session, owner_id)
        )
        cookies["set"]("session", session)
        return True
    try:
        # if params["op"][0] == "get_server_progress":
        #     jsons = get_server_progress()
        # elif params["op"][0] == "get_relay_progress":
        #     jsons = get_relay_progress()
        # elif params["op"][0] == "abort_relay":
        #     jsons = abort_relay()
        # elif params["op"][0] == "abort_orphan_relays":
        #     jsons = abort_orphan_relays()
        if params["op"][0] == "get_file":
            jsons = get_file()
        elif params["op"][0] == "get_all_folders":
            jsons = get_all_folders()
        elif params["op"][0] == "get_folders":
            jsons = get_folders()
        elif params["op"][0] == "get_folder_name":
            jsons = get_folder_name()
        elif params["op"][0] == "folder_access":
            jsons = folder_access()
        elif params["op"][0] == "new_folder":
            jsons = new_folder()
        elif params["op"][0] == "remove_file":
            jsons = remove_file()
        elif params["op"][0] == "rename_folder":
            jsons = rename_folder()
        elif params["op"][0] == "remove_folder":
            jsons = remove_folder()
        elif params["op"][0] == "move_file":
            jsons = move_file()
        elif params["op"][0] == "clone_file":
            jsons = clone_file()
        elif params["op"][0] == "import_file":
            jsons = import_file()
        elif params["op"][0] == "check_file":
            jsons = check_file()
        elif params["op"][0] == "get_dummy_api":
            jsons = get_dummy_api()
        elif params["op"][0] == "get_upload_session":
            jsons = get_upload_session()
        elif params["op"][0] == "import2":
            jsons = import2()
        elif params["op"][0] == "login":
            jsons = login()
        # elif params["op"][0] == "get_relay_info":
        #     jsons = get_relay_info()
        try:
            return json.dumps(jsons)
        except:
            return jsons
    except Unauthorized:
        cookies["set"]("session", "", -1)
        return HTTPError("401 Unauthorized")
    except NotFound:
        return HTTPError("404 Not Found")
    except BadRequest:
        return HTTPError("400 Bad Request")
    except Exception as e:
        return e

