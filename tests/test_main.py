import pytest
import sys
import os
import tkinter as tk
from unittest.mock import patch, MagicMock
from main import ascii_art, DuplicateFinder, LongPathFinder, SecretKeyGenerator

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
        mocker.patch.object(Application, 'iconbitmap', return_value=None)

        return Application()

    def test_app_initialization(self, app):
        """
        Test Application initialization with correct title and dimensions.
        """
        app.title.assert_called_once_with("UrMinion")
        app.geometry.assert_called_once_with("1024x768")
        app.iconbitmap.asser_called_once_with(app.icon_path)

    def test_init_styles(self, app):
        """
        Test styles to initialize correctly.
        """
        with patch('tkinter.ttk.Style') as mock_style:
            Application.init_styles()
            style_instance = mock_style.return_value
            style_instance.configure.assert_any_call("TButton", font=("Helvetica", 12), padding=10)
            style_instance.configure.assert_any_call("TLabel", font=("Helvetica", 14))
            style_instance.configure.assert_any_call("Header.TLabel", font=("Helvetica", 16, "bold"))

    def test_init_welcome_screen(self, app, mocker):
        """
        Test welcome screen to initialize correctly.
        """
        # Mock the clear_screen function
        mock_clear_screen = mocker.patch('main.clear_screen')

        # Mock ttk.Label
        mock_label = mocker.patch('tkinter.ttk.Label')

        # Mock ttk.Button
        mock_button = mocker.patch('tkinter.ttk.Button')

        # Run the welcome screen init
        app.init_welcome_screen()

        # Assert the screen was cleared first
        mock_clear_screen.assert_called_once_with(app)

        # Check all Labels added
        mock_label.assert_any_call(app, text=ascii_art, font=("Courier", 10), justify=tk.LEFT)
        mock_label.assert_any_call(app, text="Select one of the options below:", style="Header.TLabel")
        mock_label.assert_any_call(app, text="", font=("Helvetica", 12))

        # Check all Buttons added
        button_calls = mock_button.call_args_list

        # Extract button texts from the calls
        button_texts = [call[1]['text'] for call in button_calls if 'text' in call[1]]

        # Define expected button texts
        expected_button_texts = [
            "Find duplicates in directory",
            "Find too long file/directory paths",
            "Generate password/secret key",
        ]

        # Check that all expected buttons were created
        for expected in expected_button_texts:
            assert expected in button_texts, f"Button with text '{expected}' not found."

    def test_init_find_duplicates_screen(self, app, mocker):
        """
         Test that DuplicateFinder is initialized correctly.
        """
        # Mock the clear_screen function
        mock_clear_screen = mocker.patch('main.clear_screen')

        # Mock DuplicateFinder
        mock_duplicate_finder = mocker.patch('main.DuplicateFinder', autospec=True)

        # Run the init_find_duplicates_screen method
        app.init_find_duplicates_screen()

        # Assert the screen was cleared first
        mock_clear_screen.assert_called_once_with(app)

        # Check that DuplicateFinder was initialized and packed correctly
        mock_duplicate_finder.assert_called_once_with(app)
        mock_duplicate_finder.return_value.pack.assert_called_once_with(fill="both", expand=True)

    def test_init_find_long_paths_screen(self, app, mocker):
        """
         Test that LongPathFinder is initialized correctly.
        """
        # Mock the clear_screen function
        mock_clear_screen = mocker.patch('main.clear_screen')

        # Mock LongPathFinder
        mock_long_paths_finder = mocker.patch('main.LongPathFinder', autospec=True)

        # Run the init_find_long_paths_screen
        app.init_find_long_paths_screen()

        # Assert the screen was cleared first
        mock_clear_screen.assert_called_once_with(app)

        # Check that LongPathFinder was initialized and packed correctly
        mock_long_paths_finder.assert_called_once_with(app)
        mock_long_paths_finder.return_value.pack.assert_called_once_with(fill="both", expand=True)

    def test_init_secret_key_generator_screen(self, app, mocker):
        """
         Test that SecretKeyGenerator is initialized correctly.
        """
        # Mock the clear_screen function
        mock_clear_screen = mocker.patch('main.clear_screen')

        # Mock SecretKeyGenerator
        mock_secret_key_generator = mocker.patch('main.SecretKeyGenerator', autospec=True)

        # Run the init_secret_key_generator_screen
        app.init_secret_key_generator_screen()

        # Assert the screen was cleared first
        mock_clear_screen.assert_called_once_with(app)

        # Check that LongPathFinder was initialized and packed correctly
        mock_secret_key_generator.assert_called_once_with(app)
        mock_secret_key_generator.return_value.pack.assert_called_once_with(fill="both", expand=True)
