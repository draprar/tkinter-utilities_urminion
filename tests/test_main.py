import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Application


class TestMain:
    @pytest.fixture
    def app(self, mocker):
        """
        Create Application instance.
        Mock Tkinter Tk instance.
        """
        mock_tk = MagicMock()
        mocker.patch('tkinter.Tk', return_value=mock_tk)

        mocker.patch.object(Application, 'title', return_value=None)
        mocker.patch.object(Application, 'geometry', return_value=None)

        return Application()

    def test_app_initialization(self, app):
        """
        Test Application initialization with correct title and dimensions.
        """
        app.title.assert_called_once_with("UrMinion")
        app.geometry.assert_called_once_with("1024x768")
