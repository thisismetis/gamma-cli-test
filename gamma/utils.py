import click
from path import Path
import yaml
import frontmatter
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup

CONFIG_PATH = Path("~/.gamma/config.yaml").expanduser()


def get_config():

    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.makedirs()
        CONFIG_PATH.write_text(
            yaml.dump({"student_repo": "", "instructor_repo": ""}))

    curr_config = yaml.load(CONFIG_PATH.text())

    if "~" in curr_config["student_repo"]:
        curr_config["student_repo"] = Path(
            curr_config["student_repo"]).expanduser()
        CONFIG_PATH.write_text(yaml.dump(curr_config))
    if "~" in curr_config["instructor_repo"]:
        curr_config["instructor_repo"] = Path(
            curr_config["instructor_repo"]).expanduser()
        CONFIG_PATH.write_text(yaml.dump(curr_config))

    return curr_config


def set_config(config_obj):

    # process paths to expanduser
    for key in ["student_repo", "instructor_repo"]:
        if "~" in config_obj[key]:
            config_obj[key] = str(Path(config_obj[key]).expanduser())

    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.makedirs()
    CONFIG_PATH.write_text(yaml.dump(config_obj))

    return True


def parse_lesson_date(date):
    """Parses date format in lesson yaml

    Args:
        - date: date in gamma format, i.e. "w01d04"

    Returns:
        (day, week) tuple of integers
    """

    lesson_week = int(date.split("d")[0][1:])
    lesson_day = int(date.split("d")[-1])

    return lesson_day, lesson_week


def parse_lesson_duration(duration):
    """Parses duration format in lesson yaml

    Args:
        - duration: duration in gamma format, i.e. "60"

    Returns:
        - dur: int
    """

    if duration == 'todo':
        dur = 60
    else:
        dur_str = "".join([c for c in duration if c.isdecimal()])
        dur = int(dur_str)

    return dur


CONFIG = get_config()


def read_lessons(repo_path):
    """Build a dataframe from yaml files."""

    topics = Path(repo_path).glob("curriculum/*/*")

    def test(x):
        return (x.isdir() and ("project" in x))

    topics = [t for t in topics if test(t)]

    list_of_dicts = []
    for current_topic in topics:

        post = frontmatter.load(current_topic/"readme.md")
        lesson_dict = post.metadata
        if "order" not in lesson_dict:
            lesson_dict["order"] = 10
        lesson_dict["lesson"] = current_topic.split("/")[-1]
        lesson_dict["project"] = current_topic.split("/")[-2]
        day, week = parse_lesson_date(lesson_dict["date"])
        lesson_dict["day"] = day
        lesson_dict["week"] = week
        list_of_dicts.append(lesson_dict)

    lesson_df = pd.DataFrame(list_of_dicts)

    first_cols = ['date', 'title', 'maintainer', 'duration', 'project']

    last_cols = [c for c in lesson_df.columns if c not in first_cols]

    lesson_df = lesson_df.loc[:, first_cols + last_cols]
    lesson_df.sort_values(by=["date", "lesson"], inplace=True)

    return lesson_df


def read_pairs(repo_path):
    """Build a dataframe from pair yaml files."""

    pairs = Path(repo_path).glob("pairs/*")

    list_of_dicts = []
    for current_pair in pairs:
        post = frontmatter.load(f"{current_pair}/readme.md")
        pair_dict = post.metadata

        pair_dict["pair"] = current_pair.split("/")[-1]

        no_title = "title" not in pair_dict
        none_title = pair_dict["title"] is None
        if no_title or none_title:
            pair_dict["title"] = pair_dict["pair"]

        day, week = parse_lesson_date(pair_dict["date"])
        pair_dict["day"] = day
        pair_dict["week"] = week
        list_of_dicts.append(post.metadata)

    pair_df = pd.DataFrame(list_of_dicts)

    first_cols = ['date', 'title', 'maintainer', 'duration']

    last_cols = [c for c in pair_df.columns if c not in first_cols]

    pair_df = pair_df.reindex(columns=first_cols + last_cols)
    pair_df.sort_values(by=["date", "title"], inplace=True)

    return pair_df


def daily_table(repo_path, lesson_df, pair_df):
    """Generte daily table."""
    repo_path = Path(repo_path)
    readme_path = repo_path/"readme.md"

    if not readme_path.exists():
        click.echo(f"The file {readme_path} does not exist. Please create it.")
        return

    if not ("# Daily Schedule" in readme_path.text()):
        click.echo(f"The file {readme_path} should contain the heading" +
                   "`# Daily Schedule`. Please add it.")
        return

    template_dir = Path(__file__).parent/"templates"

    env = Environment(
        loader=FileSystemLoader(template_dir, followlinks=True),
        autoescape=False)
    template = env.get_template("daily.html.py")

    soup = BeautifulSoup(
        template.render(lesson_df=lesson_df, pair_df=pair_df), 'html.parser')

    daily_table = soup.prettify()

    readme_path = repo_path/"readme.md"
    readme_text = readme_path.text()
    start = readme_text.find("# Daily Schedule") + len("# Daily Schedule")
    end = readme_text.find("#", start)

    readme_path.write_text(readme_text[:start] + "\n\n" + daily_table +
                           "\n\n" + readme_text[end:])


def write_schedule(repo_path, lesson_df, pair_df):
    """Writes schedule files based on lesson metadata."""

    repo_path = Path(repo_path)

    max_week = max(pair_df.week.max(), lesson_df.week.max())

    for week_i in range(1, max_week + 1):

        week_str = f"# Week {week_i} \n"

        for day_i, day in enumerate(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]):

            week_str += f"\n\n{day}\n"

            pair_list = pair_df.query(
                f"(day == {day_i+1}) and (week == {week_i})").to_dict(
                    "records")
            if pair_list:
                pair = pair_list[0]
                week_str += f"* Pair: [{pair['title']}](/pairs/{pair['pair']})"
                week_str += f" ({pair['duration']} m)  \n"

            lessons = lesson_df.query(
                f"(day == {day_i+1}) and (week == {week_i})").sort_values(
                    "order").to_dict("records")

            for lesson in lessons:
                week_str += f"* [{lesson['title']}]"
                week_str += (f"(/curriculum/{lesson['project']}" +
                             f"/{lesson['lesson']})")
                week_str += f" ({lesson['duration']} m)  \n"

            week_path = repo_path/"schedule" /f"week-{week_i:02d}.md"
            week_path.write_text(week_str)
