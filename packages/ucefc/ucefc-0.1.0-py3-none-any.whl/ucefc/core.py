class UCEFC:
    def __init__(self, *, domain, port, api_key, credentials, new_password=None):
        from omnitools import sha512hd, p
        import json
        import os
        import re
        p("[pre-run] linking jobs resource files")
        cwd = os.path.dirname(os.path.abspath(__file__))
        fp = os.path.join(cwd, "pkg_data", "dummy_api.txt")
        open(fp, "wb").write(os.path.join(os.getcwd(), "dummy_api.json").encode())
        if new_password:
            open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pkg_data", "new_password.json"), "wb").write(
                json.dumps([[sha512hd(sha512hd(sha512hd(_[1]))), _[0]] for _ in new_password]).encode()
            )
        p("[pre-run] changing DWA config")
        fp = os.path.join(cwd, "pkg_data", "app.py")
        r = open(fp, "rb").read().decode()
        r = re.sub(r"(settings[\"db_port\"] = )[0-9]+", r"\g<1>{}".format(port+1), r)
        r = re.sub(r"(settings[\"writer_port\"] = )[0-9]+", r"\g<1>{}".format(port+1), r)
        open(fp, "wb").write(r.encode())
        # fp = os.path.join(cwd, "pkg_data", "pages", "root.py")
        # r = open(fp, "rb").read().decode()
        # r = re.sub(r"(max_size = )[0-9]+(\*GB)", r"\g<1>{}\g<2>".format(10 if credentials else 5), r)
        # open(fp, "wb").write(r.encode())
        # fp = os.path.join(cwd, "pkg_data", "root", "ucefc.js")
        # r = open(fp, "rb").read().decode()
        # r = re.sub(r"(max_size = )[0-9]+(\*GB)", r"\g<1>{}\g<2>".format(10 if credentials else 5), r)
        # open(fp, "wb").write(r.encode())
        from .pkg_data import main
        domain = "ucefc."+domain
        main(domain, port, api_key, credentials)
        p("[post-run] exited")




