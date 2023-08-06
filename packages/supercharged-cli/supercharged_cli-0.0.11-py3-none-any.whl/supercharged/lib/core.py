from peewee import *
import os
from jinja2 import Environment, PackageLoader, select_autoescape
import click

APP_NAME = 'supercharged'
app_directory = click.get_app_dir(APP_NAME)

def create_app_db():
    return SqliteDatabase(os.path.join(app_directory, 'data', 'installed_apps.db'))
    


def create_default_setup(path, domain, installed_apps=[], ports=None):
    env = Environment(
        loader=PackageLoader("supercharged"),
        autoescape=select_autoescape()
    )

    template = env.get_template("TRAFIK_TEMPLATE.yml")
    formatted_string = template.render({
        'frontend_app_path': path,
        'domain': domain,
        'ports': ports,
        'installed_apps': installed_apps
    })
    return formatted_string

def create_frontpage():
    env = Environment(
        loader=PackageLoader("supercharged"),
        autoescape=select_autoescape()
    )

    template = env.get_template("index.html")
    return template.render()
