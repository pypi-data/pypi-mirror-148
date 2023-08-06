import pytest
import click
from click.testing import CliRunner
from lib.__main__ import main, APP_NAME
import os
class TestInitFunction():
    runner = CliRunner()
    def test_init_makes_data_folders(self):
        result = self.runner.invoke(main, ['init', 'test.local'])
        print(result.stdout)
        assert result.exit_code == 0
        assert os.path.isdir(os.path.join(click.get_app_dir( APP_NAME), 'data'))

    