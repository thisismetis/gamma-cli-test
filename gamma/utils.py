from path import Path
import yaml

CONFIG_PATH = Path("~/.gamma/config.yaml").expanduser()


def get_config():

    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.makedirs()
        CONFIG_PATH.write_text(
            yaml.dump({"student_repo": "", "instructor_repo": ""}))

    return yaml.load(CONFIG_PATH.text())


def set_config(config_obj):

    # process paths to expanduser
    for key in ["student_repo", "instructor_repo"]:
        if "~" in config_obj[key]:
            config_obj[key] = str(Path(config_obj[key]).expanduser())

    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.makedirs()
    CONFIG_PATH.write_text(yaml.dump(config_obj))

    return True
