import gamma
from click.testing import CliRunner


def test_gamma():

    runner = CliRunner()
    result = runner.invoke(gamma)
    assert result.exit_code == 0


def test_status():

    runner = CliRunner()
    result = runner.invoke(gamma.status)
    assert result.exit_code == 0
