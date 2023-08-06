import click 

@click.group()
@click.pass_context
def loss(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Get details of all metrics supported in Phobos')

@click.option('--type', required=False, default=None, help='Type of problem ImageClassification/Segmentation/ObjectDetection/Segmentation')
@click.pass_context
def ls(ctx, type):
    pass

@click.option('--name', required=True, help='Detail of the metric')
@click.pass_context
def describe(ctx, name):
    pass