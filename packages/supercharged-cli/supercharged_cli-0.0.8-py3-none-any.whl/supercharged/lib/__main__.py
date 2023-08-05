import click
import os
from peewee import *
import json
from .core import create_app_db, create_default_setup, create_frontpage
import subprocess
import requests
import uuid
import docker
import shutil


APP_NAME = 'supercharged'
DB  = create_app_db()
class BaseModel(Model):
    class Meta:
        database = DB

class InstalledApp(BaseModel):
    name = CharField(null=False)
    installed = BooleanField(default=False)
    dl_filename = CharField(null=False)
    portA = IntegerField(null=True)
    portB = IntegerField(null=True)


@click.group()
def main():
    pass

@click.command()
@click.option('--site_path', default=None, help='This is the path where all of the installed apps and config files will go to')
@click.argument('domain')
def init(site_path, domain):
    """Builds the folder for project
    DOMAIN is the domain that the supercharged site will run on
    """
    click.echo('Choose a master username and password. This will be how you will log into the admin section of each downloaded')
    username = click.prompt('What will be your username?')
    password = click.prompt('What is the password?', hide_input=True, confirmation_prompt=True)
    click.echo("Init is running...")
    click.echo("Making data directory")
    app_directory = click.get_app_dir(APP_NAME)
    if os.path.isdir(os.path.join(app_directory, 'data')) == False:
        try:
            os.makedirs(os.path.join(app_directory, 'data'))
           
        except Exception as e:
            click.error("Man, I couldn't create the data folder. Do you have permission to make folders here: " + app_directory + "?")
    if site_path == None:
        installed_app_drive = os.getcwd()
    else:
        installed_app_drive = site_path
    
    if os.path.isdir(os.path.join(installed_app_drive, 'installed_apps')) == False:
        try:
            os.makedirs(os.path.join(installed_app_drive, 'installed_apps'))
        except Exception as e:
            click.echo("Hey, I couldn't create the installed_apps folder. Do you have permission to make folders here: " + installed_app_drive)
    DB.create_tables([InstalledApp])
    frontend_installed_drive = os.path.join(installed_app_drive, "installed_apps", "frontend")
    if os.path.isdir(frontend_installed_drive) == False:
        try:
            os.makedirs(frontend_installed_drive)
            os.makedirs(os.path.join(frontend_installed_drive, "src"))
        except Exception as e:
            click.echo("Hey, I couldn't create the frontend folder for a default app. Do you have permission to make folders here: " + frontend_installed_drive)
        
    default_trafik_config = create_default_setup(os.path.join(frontend_installed_drive, "src"), domain)
    fp = click.open_file(os.path.join(installed_app_drive, 'docker-compose.yml'), 'w+')
    fp.write(default_trafik_config)
    fp.close()

    fp = click.open_file(os.path.join(app_directory, "config.json"), 'w+')
    fp.write(json.dumps({
        'installed_app_directory': os.path.join(installed_app_drive, 'installed_apps'),
        'site_path': installed_app_drive,
        'domain': domain,
        'username': username,
        'password': password
        }))
    fp.close()

    default_homepage = create_frontpage()
    fp = click.open_file(os.path.join(frontend_installed_drive, "src", "index.html"), 'w')
    fp.write(default_homepage)
    fp.close()


@click.command()
@click.argument('url')
def download_package(url):
    """Downloads a package manifest from a repository
    
    URL will point to the manifest.json file. 
    """
    # download package manifest from URL
    rand_file_id = uuid.uuid1()
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 404:
        click.echo("There isn't any package manifest at " + url + ". Check the address again!")
        exit()
    manifest = response.json()
    print(manifest)
    
    app_directory = click.get_app_dir(APP_NAME)
    fp = click.open_file(os.path.join(app_directory, "config.json"), 'r')
    config_data = json.loads(fp.read())
    print(config_data)
    try:
        os.makedirs(os.path.join(config_data['installed_app_directory'], manifest['name']))
    except Exception as e:
        click.echo('Could not create a folder for this package.')
    

    response = requests.get(manifest['source_tarball'])
    print(response)
    # move to temp folder
    dl_filename = "supercharged_pkg-" + str(rand_file_id) + ".tar.gz"
    pkg_tarball_fp = open("/tmp/" + dl_filename, 'wb')
    pkg_tarball_fp.write(response.content)
    pkg_tarball_fp.close()
    print(rand_file_id)
    DB.connect()
    new_app = InstalledApp(name=manifest['name'])
    new_app.dl_filename = dl_filename
    if 'ports' in manifest.keys():
        new_app.portA = manifest['ports'][0]
        if len(manifest['ports']) == 2:
            new_app.portB = manifest['ports'][1]
    new_app.save()
    DB.close()



@click.command()
@click.argument('package')
def install_package(package):
    """Activates a previously downloaded package. 

    PACKAGE refers to the name of the downloaded package
    """
    # get installed_apps dircetory for install
    app_directory = click.get_app_dir(APP_NAME)
    fp = click.open_file(os.path.join(app_directory, "config.json"), 'r')
    config_data = json.loads(fp.read())
    DB.connect()
    package_to_install = InstalledApp.select().where(InstalledApp.name == package).get()
    package_to_install.installed = 1
    package_to_install.save()
    # unzip the tarball from temp folder and move to installed_apps directory
    destination_folder = os.path.join(config_data['installed_app_directory'], package)
    frontend_installed_drive = os.path.join(config_data['installed_app_directory'], 'frontend')
    try:
        subprocess.run(['tar', '-xvf', '/tmp/' + package_to_install.dl_filename, "-C", destination_folder], check=True)
    except Exception as e:
        click.echo("Coudn't open the package file to install it. Sorry. " + str(e))
        exit()
    # build the Docker image
    docker_client = docker.from_env()
    image = docker_client.images.build(path=destination_folder, tag=package, dockerfile=destination_folder + "/images/Dockerfile")
    print(image[0])
    
    # add the image and port info to the trafik template
    installed_package_list = []
    for app in InstalledApp.select().where(InstalledApp.installed == 1).dicts():
        installed_package_list.append(app)
    default_trafik_config = create_default_setup(os.path.join(frontend_installed_drive, "src"), config_data['domain'], installed_package_list)
    fp = click.open_file(os.path.join(config_data['site_path'], 'docker-compose.yml'), 'w+')
    fp.write(default_trafik_config)
    fp.close()
    DB.close()

@click.command()
@click.argument('package')
def uninstall_package(package):
    """Deactivates a previously installed packaged

    PACKAGE refers to the name of the installed packaged
    """
    app_directory = click.get_app_dir(APP_NAME)
    fp = click.open_file(os.path.join(app_directory, "config.json"), 'r')
    config_data = json.loads(fp.read())
    frontend_installed_drive = os.path.join(config_data['installed_app_directory'], 'frontend')

    DB.connect()
    selected_package = InstalledApp.select().where(InstalledApp.name==package).get()
    selected_package.installed = 0
    selected_package.save()
    DB.close()
    # add the image and port info to the trafik template
    installed_package_list = []
    for app in InstalledApp.select().where(InstalledApp.installed == 1).dicts():
        installed_package_list.append(app)
    default_trafik_config = create_default_setup(os.path.join(frontend_installed_drive, "src"), config_data['domain'], installed_package_list)
    fp = click.open_file(os.path.join(config_data['site_path'], 'docker-compose.yml'), 'w+')
    fp.write(default_trafik_config)
    fp.close()

@click.command()
@click.argument('package')
def delete_package(package):
    """Deletes a downloaded package

    PACKAGE refers to the name of the installed package
    """
    app_directory = click.get_app_dir(APP_NAME)
    fp = click.open_file(os.path.join(app_directory, "config.json"), 'r')
    config_data = json.loads(fp.read())
    package_folder = os.path.join(config_data['installed_app_directory'], package)
    shutil.rmtree(package_folder, ignore_errors=True)
    DB.connect()
    package_record = InstalledApp.delete().where(InstalledApp.name == package)
    package_record.execute()
    DB.close()


@click.command()
def list_packages():
    """Lists all downloaded packages
    """
    installed_apps = []
    DB.connect()
    for app in InstalledApp.select().dicts():
        installed_apps.append(app.name)
    DB.close()
    if len(installed_apps) == 0:
        click.echo("No apps installed")
        return 
    for app in installed_apps:
        click.echo(app.name + " is " + app.installed)


@click.command()
@click.pass_context
def uninstall(ctx):
    """Uninstalls the supercharged configuration,
    database, and packages.
    """
    # remove and delete all installed packages
    DB.connect()
    for app in InstalledApp.select():
        ctx.invoke(uninstall_package, app.name)
        ctx.invoke(delete_package, app.name)
        click.echo("Uninstalling " + app.name)
    DB.close()
    app_directory = click.get_app_dir(APP_NAME)
    fp = click.open_file(os.path.join(app_directory, "config.json"), 'r')
    config_data = json.loads(fp.read())
    os.remove(os.path.join(config_data['site_path'], "docker-compose.yml"))
    shutil.rmtree(os.path.join(config_data['site_path'], "installed_apps"))
    os.remove(os.path.join(app_directory, "config.json"))
    shutil.rmtree(os.path.join(app_directory, "data"), ignore_errors=True)
    shutil.rmtree(app_directory)
    click.echo("Uninstalled!")


main.add_command(uninstall)
main.add_command(delete_package)
main.add_command(list_packages)
main.add_command(uninstall_package)
main.add_command(download_package)
main.add_command(install_package)
main.add_command(init)