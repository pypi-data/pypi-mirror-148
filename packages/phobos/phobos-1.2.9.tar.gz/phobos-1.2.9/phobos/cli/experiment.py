import os
import yaml
import click
from functools import reduce
 
from phobos.grain import expand

from .utils.polyaxonfile import getExpConfigs
from .utils.execution import exec
from .connections import Arche


def checkValidRoot():
    root_path = os.curdir
    required_files = ['train.py', 'metadata.yaml']
    return reduce(
        lambda x, y: x and y,
        [os.path.exists(
            os.path.join(root_path, fl)
            ) for fl in required_files])


@click.group()
@click.pass_context
def experiment(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Running Experiments')

@experiment.command()
@click.option('--where', required=False, default="local", help='Train locally or on arche')
@click.option('--description', required=False, default="", help="Description for the experiment")
@click.option('--tags', required=False, default="", help="Tags for the experiment")
def run(where, description, tags):
    """Running a phobos experiment

    Examples:

    \b
    $ phobos experiment run --where=local
    """
    if not checkValidRoot():
        click.echo("To run this command. Make sure you are inside project directory.")
        return
        
    if where == 'local':
        exec("POLYAXON_NO_OP=true python train.py", pipe=False)
        return
    elif where == 'arche':
        config_file = 'polyaxonfile.yaml'

        with open('metadata.yaml', 'r') as fp:
            meta = dict(yaml.safe_load(fp.read()))
            meta = expand(meta, meta)
        expmap, polymap, url = getExpConfigs(meta)
        
        yaml.Dumper.ignore_aliases = lambda *args : True
        with open('polyaxonfile.yaml', 'w') as fp:
            yaml.dump(polymap, fp, sort_keys=False)

        click.echo("Run the project. Make sure you are inside project directory.")
        print(f'Running: {config_file}')

        archeClient = Arche(url)
        archeClient.createRun(
            project=expmap,
            polyaxon_file=config_file
        )
    else:
        click.echo("Please provide where to run the experiment (local/arche)")

# @click.command()
# @click.option(
#     '--uuid',
#     required=True,
#     help='"uuid" for single uuid or "uuid-1,..,uuid-n" for multiple uuids')
# def tensorboard(uuid):
#     '''
#     phobos tensorboard

#     Runs tensorboard for a given uuid/project

#     Params:
#     ------
#     uuid:           Experiment uuid/uuid1,..,uuidn
#     '''
#     if not checkValidRoot():
#         click.echo("To run this command the project. Make sure you are inside project directory.")
#         return
    
#     with open('metadata.yaml', 'r') as fp:
#         meta = dict(yaml.safe_load(fp.read()))
#         meta = expand(meta, meta)

#     expmap, polymap, url = getExpConfigs(meta)

#     uuids = uuid.split(',')
    
#     archeClient = Arche()

#     archeClient.run_tensorboard(project=expmap, uuid=uuids)