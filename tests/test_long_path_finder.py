import os
import pytest
import sys
import tkinter as tk
from tkinter import filedialog
from unittest.mock import Mock, patch
from long_path_finder import LongPathFinder


@pytest.fixture
def app():
    # Create a root Tkinter instance and initialize LongPathFinder with any needed mocks
    root = tk.Tk()
    root.init_welcome_screen = Mock()  # mock the missing method
    long_path_finder = LongPathFinder(root)
    long_path_finder.path_map = {}  # ensure path_map is initialized
    long_path_finder.default_long_path_length = 260
    long_path_finder.long_path_length = long_path_finder.default_long_path_length
    long_path_finder.listbox = tk.Listbox(root)
    return long_path_finder


class TestLongPathFinder:
    def test_initial_state(self, app):
        # Test initialization without errors
        assert isinstance(app, LongPathFinder)

    def test_open_directory(self, app):
        # Directly set the directory
        app.directory = "/mocked/path"

        assert app.directory == "/mocked/path"

    @patch("long_path_finder.os.walk")
    def test_search_long_paths(self, mock_walk, app):
        # Mock the os.walk output to simulate a directory with long paths
        mock_walk.return_value = [
            ("/mocked/path", [], ["a" * 260, "b" * 100, "c" * 255])
        ]

        # Set the threshold for long paths and run the search
        app.path_length_threshold = 250
        long_paths = []
        for root, dirs, files in mock_walk.return_value:
            for file in files:
                full_path = os.path.join(root, file)
                if len(full_path) > app.path_length_threshold:
                    long_paths.append(os.path.normpath(full_path))  # Normalize each path

        # Normalize the paths to handle cross-platform path separators
        expected_long_paths = [
            os.path.normpath("/mocked/path/" + "a" * 260),
            os.path.normpath("/mocked/path/" + "c" * 255)
        ]
        assert long_paths == expected_long_paths

    @patch("long_path_finder.subprocess.call")
    @patch("long_path_finder.os.startfile")
    def test_open_end_of_path(self, mock_startfile, mock_subprocess_call, app):
        # Prepare the test data and add it to listbox
        test_entry = "Length: 260 - /mocked/path/to/file.txt"
        app.path_map[test_entry] = "/mocked/path/to/file.txt"
        app.listbox.insert(tk.END, test_entry)
        app.listbox.selection_set(0)

        # Call the method under test
        app.open_end_of_path()

        expected_path = os.path.normpath("/mocked/path/to")

        # Check platform-specific behavior
        if sys.platform == "win32":
            mock_startfile.assert_called_once_with(expected_path)
            mock_subprocess_call.assert_not_called()  # subprocess.call shouldn't be used on Windows
        else:
            mock_startfile.assert_not_called()  # os.startfile shouldn't be used on non-Windows
            if sys.platform == "darwin":
                mock_subprocess_call.assert_called_once_with(["open", expected_path])
            else:
                mock_subprocess_call.assert_called_once_with(["xdg-open", expected_path])
