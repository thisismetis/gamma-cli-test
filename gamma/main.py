import click
import yaml
import pandas as pd
from path import Path
from tabulate import tabulate

from .utils import (get_config, set_config, read_lessons, read_pairs,
                    daily_table, write_schedule, parse_lesson_date)

config = get_config()


@click.group()
def gamma():
    """Hold place for command."""
    pass


@gamma.command()
def status():
    """Display status of gamma configuration"""
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
def configure(context, instructor_repo, student_repo):
    """Set the gamma configuration through the command line."""
    set_config(
        {"instructor_repo": instructor_repo, "student_repo": student_repo})

    student_repo = Path(student_repo)

    directory_flag = True
    for dir in ["curriculum", "lessons", "pairs"]:
        test_dir = student_repo/dir
        if not test_dir.isdir():
            directory_flag = False
            break

    if not directory_flag:
        if click.confirm('The student repo is missing one or more directories'
                         + 'needed for the curriculum. Would you like for me' +
                         'to create them?'):
            for dir in ["curriculum", "lessons", "pairs"]:
                make_dir = student_repo/dir
                make_dir.makedirs_p()

    if not (student_repo/"readme.md").exists():
        if click.confirm('The student repo is missing the main readme' +
                         'needed for the curriculum.' + 'to create it?'):

            (student_repo/"readme.md").write_text("\n\n# Daily Schedule\n\n")

    context.invoke(status)


@gamma.command()
def generate():
    """Generate the daily table and schedule files."""

    click.echo("generating files")

    for key in ["instructor_repo", "student_repo"]:

        lesson_df = read_lessons(config[key])
        pair_df = read_pairs(config[key])

        daily_table(config[key], lesson_df, pair_df)
        write_schedule(config[key], lesson_df, pair_df)


@gamma.command()
def excel():
    """Generate an excel file from content in the instructor repo."""

    pair_df = read_pairs(config["instructor_repo"])
    pair_df["type"] = "pair"
    pair_df["order"] = 0

    lesson_df = read_lessons(config["instructor_repo"])
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
        Path(config["instructor_repo"])/'gamma.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    combined_df.to_excel(writer, sheet_name='Sheet1', index=False)

    worksheet = writer.sheets['Sheet1']
    worksheet.add_table("A1:F150", {
        "columns": [{"header": c} for c in combined_df.columns]
    })
    writer.save()


@gamma.command()
@click.option('-d', "--date", type=click.Path(), default="w1d1",
              prompt="Move files up to and including which date?")
@click.pass_context
def move(date):
    """Move files from the instructor repo to student repo up to a date."""

    day, week = parse_lesson_date(date)

    instructor_lesson_df = read_lessons(config["instructor_repo"])
    instructor_pair_df = read_pairs(config["instructor_repo"])

    instructor_lesson_df = instructor_lesson_df.query(
        "day > 0 and  week > 0").query(
            "week < @week or (week == @week and day <= @day)")
    instructor_pair_df = instructor_pair_df.query(
        "day > 0 and  week > 0").query(
            "week < @week or (week == @week and day <= @day)")

    student_lesson_df = read_lessons(config["student_repo"])
    student_pair_df = read_pairs(config["student_repo"])

    instructor_lesson_df = instructor_lesson_df.loc[
        instructor_lesson_df.title.isin(student_lesson_df.title) == False, :]

    instructor_pair_df = instructor_pair_df.loc[instructor_pair_df.title.isin(
        student_pair_df.title) == False, :]

    headers = ["date", "title"]

    click.echo("The following lessons will be moved:")
    click.echo(tabulate(instructor_lesson_df.loc[:, headers], headers=headers))
    click.echo(tabulate(instructor_pair_df.loc[:, headers], headers=headers))

    student_repo = Path(config["student_repo"])
    instructor_repo = Path(config["instructor_repo"])
    if click.confirm("Do you wish to proceed?"):

        for project in instructor_lesson_df.project.unique():
            project_path = student_repo/"curriculum" /project
            if not project_path.exists():
                project_path.makedirs()

        for lesson in instructor_lesson_df.to_dict("records"):
            lesson_instructor = instructor_repo/"curriculum" /lesson[
                "project"]/lesson["lesson"]
            lesson_student = student_repo/"curriculum" /lesson[
                "project"]/lesson["lesson"]
            lesson_instructor.copytree(lesson_student)

        for pair in instructor_pair_df.to_dict("records"):
            pair_instructor = instructor_repo/"pairs" /pair["pair"]
            pair_student = student_repo/"pairs" /pair["pair"]
            pair_instructor.copytree(pair_student)
    context.invoke(generate)
