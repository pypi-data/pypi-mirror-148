import argparse

from nlu_bf.cli.arguments.default_arguments import add_model_param
from nlu_bf.cli.arguments.run import add_server_arguments


def set_shell_arguments(parser: argparse.ArgumentParser):
    add_model_param(parser)
    add_server_arguments(parser)


def set_shell_nlu_arguments(parser: argparse.ArgumentParser):
    add_model_param(parser)
