import click
import yaml

from .utils import (get_config, set_config, read_lessons, read_pairs,
                    daily_table, write_schedule)

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


@gamma.command()
def generate():
    """Generate files from yaml."""

    click.echo("generating files")

    for key in ["instructor_repo", "student_repo"]:

        lesson_df = read_lessons(config[key])
        pair_df = read_pairs(config[key])

        daily_table(config[key], lesson_df, pair_df)
        write_schedule(config[key], lesson_df, pair_df)
