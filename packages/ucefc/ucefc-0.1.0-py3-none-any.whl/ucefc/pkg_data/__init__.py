def main(domain, port, api_key, credentials):
    from omnitools import p, def_template
    import userscloud
    import traceback
    import threadwrapper
    import threading
    import dwa
    if not isinstance(credentials[0], list):
        credentials = [credentials]
    uc_webs = []
    upload_sessions = []
    tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**2))
    es = {}
    for i, credential in enumerate(credentials):
        def job(i, credential):
            uc_web = userscloud.UC_WEB()
            try:
                uc_web.login(credential)
                upload_sessions.append(userscloud.UC_API(key=uc_web.get_api_key()).UploadServer)
                uc_webs.append(uc_web)
                p("[pre-start] logged in UC_WEB ({}/{})".format(i+1, len(credentials)))
            except:
                traceback.print_exc()
                return 1
        tw.add(job=def_template(job, i, credential), result=es, key=i)
        # es[i] = def_template(job, i, credential)()
    tw.wait()
    if any(list(es.values())):
        return
    def get_upload_session():
        import random
        return random.SystemRandom().choice(upload_sessions)()
    uc_api = userscloud.UC_API(key=api_key)
    dwa.handlers.BaseResponse.uc_api = uc_api
    dwa.handlers.BaseResponse.uc_webs = uc_webs
    dwa.workers.base_worker.uc_api = uc_api
    dwa.workers.base_worker.uc_webs = uc_webs
    dwa.DWA(domain, port, 365, {
        "clone_file_private": uc_api.FileClone,
        "get_upload_session": get_upload_session
    })
    tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**2))
    for i, uc_web in enumerate(uc_webs):
        def job(i, uc_web):
            try:
                uc_web.logout()
                p("[post-start] logged out UC_WEB ({}/{})".format(i+1, len(uc_webs)))
            except:
                pass
        tw.add(job=def_template(job, i, uc_web))
        # def_template(job, i, uc_web)()
    tw.wait()


