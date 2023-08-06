import click 


@click.group()
@click.pass_context
def model(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Get details of all models implemented in Phobos')

@click.option('--type', required=False, default=None, help='Type of problem ImageClassification/Segmentation/ObjectDetection/Segmentation')
@click.pass_context
def ls(ctx, type):
    pass 