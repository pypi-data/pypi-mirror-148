from setuptools import setup, find_packages

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("./requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'supercharged_cli',
    version = '0.0.10',
    author = 'Shariq Torres',
    author_email = 'shariq.torres@gmail.com',
    license = 'GNU General',
    description = 'CLI to setup a website connected to the Supercharged Network',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/ShenpaEngineering/Supercharged',
    packages = find_packages(),
    package_data = {
        'supercharged': ['templates/*']
    },
    install_requires = [requirements],
    python_requires = '>3.7',
    entry_points = '''
        [console_scripts]
        supercharged=supercharged.lib.__main__:cli
    '''
)