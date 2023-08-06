import pages
import jobs
from dwa import *


def app_workers() -> tuple:
    return (
        jobs.root.change_password_worker(),
        jobs.root.dummy_api_worker(),
        jobs.root.smart_validate_code_worker(),
        jobs.root.smart_renew_code_worker(),
        jobs.root.renew_code_worker(),
        jobs.root.gen_sitemap_worker(),
    )


def app_settings_template(app_root: str, domain: str, port: int, cookies_expires_day: float) -> dict:
    def sql_watcher(*args, **kwargs):
        return True
    def raise_backend_errors(header, reason):
        pass
    settings = {}
    db = "db/db.db"
    settings["cookie_secret"] = ""
    settings["port"] = port
    settings["db"] = db
    settings["db_port"] = 38766
    settings["writer_port"] = 38767
    settings["domain"] = domain
    settings["cookies_expires_day"] = cookies_expires_day
    settings["extra_headers"] = {
        "Cache-Control": "must-revalidate, max-age=0",
    }
    settings["sql_watcher"] = sql_watcher
    settings["raise_backend_errors"] = raise_backend_errors
    settings["admin_contact"] = "<div>Admin contact: foxe6@pm.me</div>"
    settings["grr_secret"] = "google recaptcha secret key"
    servers = [
        pages.root.get_settings(),
        pages.resolve.get_settings(),
    ]
    settings["servers"] = {k: v for k, v in servers}
    return settings


def app_settings(app_root: str) -> dict:
    return app_settings_template(app_root, None, None, None)


