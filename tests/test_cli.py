from gamma import status
from click.testing import CliRunner


def test_status():

    runner = CliRunner()
    result = runner.invoke(status)
    assert result.exit_code == 0
