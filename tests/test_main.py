import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Application


class TestMain:
    @pytest.fixture
    def app(self):
        """
        Create Application instance.
        """
        return Application()

    def test_app_initialization(self, app):
        """
        Test Application initialization with correct title and dimensions.
        """
        assert app.title() == 'UrMinion'
        assert app.winfo_width() == 1024
        assert app.winfo_height() == 768
