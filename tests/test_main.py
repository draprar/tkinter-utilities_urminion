import pytest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Application


class TestMain:
    @pytest.fixture
    def app(self, mocker):
        """
        Create Application instance.
        Mock Tkinter mainloop and other methods.
        """
        mocker.patch('tkinter.Tk.__init__', return_value=None)
        return Application()

    def test_app_initialization(self, app):
        """
        Test Application initialization with correct title and dimensions.
        """
        assert app.title() == 'UrMinion'
        assert app.winfo_width() == 1024
        assert app.winfo_height() == 768
