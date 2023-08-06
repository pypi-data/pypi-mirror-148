import os
import click 
import yaml
import pkg_resources

from cookiecutter.main import cookiecutter

from .utils.execution import exec


@click.group()
@click.pass_context
def project(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Creating template project directory')

@project.command()
@click.option('--name', required=True, help='Project directory name, Project Id for Arche')
@click.option('--description', required=False, default="", help='Short description about the project')
@click.option('--tags', required=False, type=str, default="", help='tags related to the project')
def init(name, description, tags):
    """
    phobos project intialization

    \b
    $ phobos project init --name=NAME --description=DESCRIPTION --tags="TAG1,TAG2"
    """
    if not os.path.exists(name):
        click.echo("Creating template project directory!")
        cookiecutter(
            pkg_resources.resource_filename("phobos", "cli/cookiecutter-phobos-project"), 
            extra_context={
                'project_name': name,
            },
            no_input=True)
        with open(os.path.join(os.path.curdir, name, 'metadata.yaml'), 'r') as fp:
            config = yaml.safe_load(fp)
        
        config['project']['name'] = name
        config['project']['description'] = description
        config['project']['tags'] = tags.split(',')

        with open(os.path.join(os.path.curdir, name, 'metadata.yaml'), 'w') as fp:
            yaml.dump(config, fp, sort_keys=False)
        
        exec(f"cd {name}")
    else:
        click.echo(f"{name} already exist locally.")
