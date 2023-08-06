import argparse
import logging

import pytest

from rss_reader.argument_parser.arg_parser import ArgParser


@pytest.fixture
def set_cli_args_options(monkeypatch):

    def mock_parse_args(*args, **kwargs):
        """ Mocks the behaviour cli argument options """

        return argparse.Namespace(source='some source', limit=2, json=True, loglevel=logging.DEBUG, date='20220410')

    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)
    args_1 = ArgParser()

    return args_1.cli_args


def test_arguments(set_cli_args_options):
    """ Test results of mocked arguments  """

    assert set_cli_args_options.source == 'some source'
    assert set_cli_args_options.limit == 2
    assert set_cli_args_options.json is True
    assert set_cli_args_options.loglevel == logging.DEBUG
    assert set_cli_args_options.date == '20220410'


