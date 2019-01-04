import click
import yaml

from .utils import get_config, set_config

config = get_config()


@click.group()
def gamma():
    """Hold place for command."""
    pass


@gamma.command()
def status():
    config = get_config()
    click.secho('Your current configuration is:', bg='magenta', fg='white')
    click.echo(yaml.dump(config, default_flow_style=False))


@gamma.command()
@click.option('-i', "--instructor_repo", type=click.Path(),
              default=config["instructor_repo"],
              prompt="Enter the path to the instructor repo")
@click.option('-s', "--student_repo", type=click.Path(),
              default=config["student_repo"],
              prompt="Enter the path to the student repo")
@click.pass_context
def init(context, instructor_repo, student_repo):
    set_config(
        {"instructor_repo": instructor_repo, "student_repo": student_repo})
    context.invoke(status)
