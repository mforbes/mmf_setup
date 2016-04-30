"""Regression test for Issue 12: enable_nbextension."""

from mmf_setup.notebook_configuration import ExtensionManager


def test_issue_12():
    manager = ExtensionManager()
    manager.enable('noop')
    manager.disable('noop')
