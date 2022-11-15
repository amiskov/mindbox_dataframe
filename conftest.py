import pytest

def pytest_addoption(parser):
    parser.addoption("--df_size", action="store")
