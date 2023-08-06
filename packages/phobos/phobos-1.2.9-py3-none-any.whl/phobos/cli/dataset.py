import click 

from .connections import Europa 


@click.group()
@click.pass_context
def dataset(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Preparing Europa dataset for training')

@dataset.command()
@click.option('--url', required=False, type=str, default='https://api.granular.ai', help='URL of Europa')
@click.option('--email', required=False, type=str, default=None, help='Email registered on Europa')
@click.option('--passwd', required=False, type=str, default=None, help='Password registered in Europa')
def ls(url, email, passwd):
    """List all the dataset available in Europa

    Examples:

    \b
    $ phobox dataset ls --email=EMAIL --passwd=PASSWD
    """
    europa = Europa(url, email, passwd)
    europa.get_tasks()
    return 

@dataset.command()
@click.option('--id', required=True, type=str, default=None, help="ID of the dataset")
@click.option('--url', required=False, type=str, default='https://api.granular.ai', help='URL of Europa')
@click.option('--email', required=False, type=str, default=None, help='Email registered on Europa')
@click.option('--passwd', required=False, type=str, default=None, help='Password registered in Europa')
def describe(id, url, email, passwd):
    """Get details of a Europa dataset

    Examples:

    \b
    $ phobox dataset describe --id=ID --email=EMAIL --passwd=PASSWD
    """
    europa = Europa(url, email, passwd)
    if id:
        europa.get_task_details(id)
    return 

@dataset.command()
@click.option('--id', required=True, type=str, default=None, help="ID of the dataset")
@click.option('--url', required=False, type=str, default='https://api.granular.ai', help='URL of Europa')
@click.option('--email', required=False, type=str, default=None, help='Email registered on Europa')
@click.option('--passwd', required=False, type=str, default=None, help='Password registered in Europa')
def export(id, url, email, passwd):
    """Export Europa dataset

    Examples:

    \b
    $ phobox dataset export --id=ID --email=EMAIL --passwd=PASSWD
    """
    europa = Europa(url, email, passwd)
    if id:
        europa.export_annotations(id)
    return 