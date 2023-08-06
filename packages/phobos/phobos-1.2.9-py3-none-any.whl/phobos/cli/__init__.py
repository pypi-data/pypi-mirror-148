import os
import click
import json
from appdirs import user_config_dir

from phobos import __version__ as version

from .dataset import dataset 
from .model import model 
from .metric import metric 
from .loss import loss 
from .experiment import experiment 
from .project import project

    
@click.group()
@click.version_option(version, message='%(version)s')
def cli():
    config_dir = user_config_dir('phobos')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(os.path.join(config_dir, "config.json")):
        fout = open(os.path.join(config_dir, "config.json"), "w")
        json.dump({"url": None, "email": None, "passwd": None, "accessToken": None, "refreshToken": None}, fout)
        fout.close()

cli.add_command(project)
# cli.add_command(model)
# cli.add_command(loss)
# cli.add_command(metric)
cli.add_command(dataset)
cli.add_command(experiment)


if __name__ == "__main__":
    cli()
