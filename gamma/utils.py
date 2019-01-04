from path import Path
import yaml


def get_config():

    config_path = Path("~/.gamma/config.yaml").expanduser()

    if not config_path.exists():
        config_path.parent.makedirs()
        config_path.write_text(
            yaml.dump({"student_repo": "", "instructor_repo": ""}))

    return yaml.load(config_path.text())
