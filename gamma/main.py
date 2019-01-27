import click
import yaml
import pandas as pd
from path import Path
from tabulate import tabulate
import platform

from .utils import (get_config, set_config, read_lessons, read_pairs,
                    daily_table, write_schedule, parse_lesson_date,
                    check_config)

import pkg_resources

__version__ = pkg_resources.get_distribution('gamma').version

REC_INSTALL = """\n\b
    mkdir -p ~/.gamma
    git clone git@github.com:thisismetis/gamma-cli.git ~/.gamma/gamma-cli
    pip install -e ~/.gamma/gamma-cli\n"""


@click.group()
def gamma():
    """Hold place for command."""
    pass


@gamma.command()
def status():
    """Display status of gamma configuration"""

    config = get_config()

    click.echo(f"platform: {platform.platform()}")

    install_loc = Path(__file__)
    rec_install_loc = Path("~/.gamma/gamma-cli/gamma/main.py").expanduser()
    rec_install_flag = install_loc == rec_install_loc

    click.echo(f"Gamma-cli version: {__version__}, "
               f"Install location: {install_loc}")
    if not rec_install_flag:
        click.secho(
            'Your current install location is different from the recommended '
            'location.', bg='red', fg='white')
        click.echo(f"It is recommended that you install with {REC_INSTALL}")

    click.secho('Your current configuration is:', bg='magenta', fg='white')
    click.echo(yaml.dump(config, default_flow_style=False))

    if not check_config(config):
        click.secho(
            "Warning: your config file doesn't appear to be "
            "properly set", bg='red', fg='white')
        click.echo("""Set it with
    gamma configure
""")


CONFIG = get_config()


@gamma.command()
@click.option('-i', "--instructor_repo", type=click.Path(),
              default=CONFIG["instructor_repo"],
              prompt="Enter the path to the instructor repo",
              help="Absolute path to instructor repo")
@click.option('-s', "--student_repo", type=click.Path(),
              default=CONFIG["student_repo"],
              prompt="Enter the path to the student repo",
              help="Absolute path to student repo")
@click.pass_context
def configure(context, instructor_repo, student_repo):
    """Set the gamma configuration through the command line."""
    set_config(
        {"instructor_repo": instructor_repo, "student_repo": student_repo})
    curr_config = get_config()
    student_repo = Path(curr_config["student_repo"])

    dirs = ["curriculum", "schedule", "pairs"]

    directory_flag = True
    for dir in dirs:
        test_dir = student_repo / dir
        if not test_dir.isdir():
            directory_flag = False
            break

    if not directory_flag:
        if click.confirm(
                'The student repo is missing one or more directories ' +
                'needed for the curriculum. Would you like for me ' +
                'to create them?'):
            for dir in dirs:
                make_dir = student_repo / dir
                make_dir.makedirs_p()

    if not (student_repo / "readme.md").exists():
        if click.confirm('The student repo is missing the main readme ' +
                         'needed for the curriculum. ' + 'to create it?'):

            (student_repo / "readme.md").write_text("\n\n# Daily Schedule\n\n")

    context.invoke(status)


@gamma.command()
def generate():
    """Generate the daily table and schedule files."""

    click.echo("generating files")
    config = get_config()

    for key in ["instructor_repo", "student_repo"]:

        lesson_df = read_lessons(config[key])
        pair_df = read_pairs(config[key])

        if pair_df.empty:
            click.secho(
                f"Warning: there are no valid pairs in {key}."
                "Ensure that your config is set properly and that your "
                "instructor repo is up to date.", bg='red', fg='white')

        if lesson_df.empty:
            click.secho(
                f"Warning: there are no valid lessons in {key}."
                "Ensure that your config is set properly and that your "
                "instructor repo is up to date.", bg='red', fg='white')

        if pair_df.empty and lesson_df.empty:
            continue

        daily_table(config[key], lesson_df, pair_df)
        write_schedule(config[key], lesson_df, pair_df)


@gamma.command()
def excel():
    """Generate an excel file from content in the instructor repo."""
    config = get_config()

    pair_df = read_pairs(config["instructor_repo"])
    lesson_df = read_lessons(config["instructor_repo"])

    if pair_df.empty:
        click.secho(
            "Warning: there are no valid pairs in the instructor repo."
            "Ensure that your config is set properly and that your "
            "instructor repo is up to date.", bg='red', fg='white')
        return
    if lesson_df.empty:
        click.secho(
            "Warning: there are no valid lessons in the instructor repo."
            "Ensure that your config is set properly and that your "
            "instructor repo is up to date.", bg='red', fg='white')
        return

    pair_df["type"] = "pair"
    pair_df["order"] = 0

    lesson_df["type"] = "lesson"

    combined_df = pd.concat([pair_df, lesson_df], sort=False,
                            ignore_index=True)

    combined_df = combined_df.query("(day > 0) and (week > 0)").sort_values(
        ["week", "day", "order"]).reset_index()

    combined_df = combined_df.loc[:,
                                  ["week", "day", "title", "type", "duration"]]
    combined_df["instructor"] = ""

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(
        Path(config["instructor_repo"]) / 'gamma.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    combined_df.to_excel(writer, sheet_name='Sheet1', index=False)

    worksheet = writer.sheets['Sheet1']
    worksheet.add_table("A1:F150", {
        "columns": [{"header": c} for c in combined_df.columns]
    })
    writer.save()


@gamma.command()
@click.option('-d', "--date", type=str, default="w1d1",
              prompt="Move files up to and including which date?",
              help="Date to move files. Example: w2d4")
@click.pass_context
def move(context, date):
    """Move files from the instructor repo to student repo up to a date."""

    config = get_config()

    day, week = parse_lesson_date(date, "move command")

    instructor_lesson_df = read_lessons(config["instructor_repo"])
    instructor_pair_df = read_pairs(config["instructor_repo"])

    if instructor_pair_df.empty:
        click.secho(
            "Warning: there are no valid pairs in the instructor repo. "
            "Ensure that your config is set properly and that your "
            "instructor repo is up to date.", bg='red', fg='white')
        return
    if instructor_lesson_df.empty:
        click.secho(
            "Warning: there are no valid lessons in the instructor repo. "
            "Ensure that your config is set properly and that your "
            "instructor repo is up to date.", bg='red', fg='white')
        return

    instructor_lesson_df = instructor_lesson_df.query(
        "day > 0 and  week > 0").query(
            "week < @week or (week == @week and day <= @day)")
    instructor_pair_df = instructor_pair_df.query(
        "day > 0 and  week > 0").query(
            "week < @week or (week == @week and day <= @day)")

    student_lesson_df = read_lessons(config["student_repo"])
    student_pair_df = read_pairs(config["student_repo"])

    if not student_lesson_df.empty:
        instructor_lesson_df = instructor_lesson_df.loc[
            instructor_lesson_df.title.isin(
                student_lesson_df.title) == False, :]  # noqa: E712
    if not student_pair_df.empty:
        instructor_pair_df = instructor_pair_df.loc[
            instructor_pair_df.title.isin(
                student_pair_df.title) == False, :]  # noqa: E712

    headers = ["date", "title"]

    click.echo("\nThe following lessons will be moved:")
    click.echo(
        tabulate(instructor_lesson_df.loc[:, headers], headers=headers) + "\n")
    click.echo("The following pairs will be moved:")
    click.echo(
        tabulate(instructor_pair_df.loc[:, headers], headers=headers) + "\n")

    student_repo = Path(config["student_repo"])
    instructor_repo = Path(config["instructor_repo"])
    if click.confirm("Do you wish to proceed?"):

        for project in instructor_lesson_df.project.unique():
            project_path = student_repo / "curriculum" / project
            if not project_path.exists():
                project_path.makedirs()

        for lesson in instructor_lesson_df.to_dict("records"):
            lesson_instructor = instructor_repo / "curriculum" / lesson[
                "project"] / lesson["lesson"]
            lesson_student = student_repo / "curriculum" / lesson[
                "project"] / lesson["lesson"]
            lesson_instructor.copytree(lesson_student)

        for pair in instructor_pair_df.to_dict("records"):
            pair_instructor = instructor_repo / "pairs" / pair["pair"]
            pair_student = student_repo / "pairs" / pair["pair"]
            pair_instructor.copytree(pair_student)

    click.echo("Lessons have been move. Regenerating schedule...")
    context.invoke(generate)
