import os
import pytest
from unittest.mock import patch, Mock, MagicMock
from duplicate_finder import get_file_hash, find_duplicates, DuplicateFinder
import tkinter as tk
import tkinter.messagebox
import tempfile


@pytest.fixture
def duplicate_finder():
    # Initialize DuplicateFinder with a Tk instance
    root = tk.Tk()
    root.init_welcome_screen = Mock()
    finder = DuplicateFinder(root)
    return finder


class TestDuplicateFinder:
    def test_get_file_hash_valid_file(self):
        # Create a temporary file with known content to hash
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"Test content")
            temp_file_path = temp_file.name

        hash_value = get_file_hash(temp_file_path)
        expected_hash = "9d9595c5d94fb65b824f56e9999527dba9542481580d69feb89056aabaa0aa87"
        assert hash_value == expected_hash

        os.remove(temp_file_path)

    def test_get_file_hash_invalid_file(self):
        # Test with a non-existent file
        hash_value = get_file_hash("non_existent_file.txt")
        assert hash_value is None

    def test_find_duplicates(self):
        # Test for find_duplicates function
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create duplicate files
            file_path1 = os.path.join(temp_dir, "file1.txt")
            file_path2 = os.path.join(temp_dir, "file2.txt")
            with open(file_path1, "w") as f1, open(file_path2, "w") as f2:
                f1.write("duplicate content")
                f2.write("duplicate content")

            duplicates = find_duplicates(temp_dir)
            assert len(duplicates) == 1  # expecting one duplicate hash
            assert len(duplicates[list(duplicates.keys())[0]]) == 2  # two files for the duplicate hash

    @patch("duplicate_finder.messagebox.showinfo")
    def test_open_directory(self, mock_showinfo, duplicate_finder):
        # Mock filedialog to return a test directory
        with patch("duplicate_finder.filedialog.askdirectory", return_value="test_directory"):
            duplicate_finder.open_directory()
            assert duplicate_finder.directory == "test_directory"
            mock_showinfo.assert_called_once_with("Directory selected", "Selected directory: test_directory")

    @patch("duplicate_finder.messagebox.showwarning")
    def test_start_search_no_directory(self, mock_showwarning, duplicate_finder):
        # Ensure warning message shows if directory is not selected
        duplicate_finder.start_search()
        mock_showwarning.assert_called_once_with("No directory", "Please select a directory first.")

    @patch("duplicate_finder.messagebox.showinfo")
    def test_start_search_no_duplicates(self, mock_showinfo, duplicate_finder):
        # Mock directory and empty find_duplicates result to simulate no duplicates
        duplicate_finder.directory = "test_directory"
        with patch("duplicate_finder.find_duplicates", return_value={}):
            duplicate_finder.start_search()
            mock_showinfo.assert_called_once_with("No duplicates", "No duplicate files found.")

    @patch("duplicate_finder.messagebox.showinfo")
    def test_delete_selected_no_selection(self, mock_showinfo, duplicate_finder):
        # Test deleting with no selection made
        duplicate_finder.listbox = MagicMock()
        duplicate_finder.listbox.curselection.return_value = []
        with patch("duplicate_finder.messagebox.showwarning") as mock_warning:
            duplicate_finder.delete_selected()
            mock_warning.assert_called_once_with("No selection", "Please select files to delete.")

    @patch("tkinter.messagebox.showwarning")
    @patch("tkinter.messagebox.askyesno", return_value=True)
    @patch("tkinter.messagebox.showerror")
    def test_delete_selected_with_error(self, mock_showerror, mock_askyesno, mock_showwarning, duplicate_finder):
        # Set up a mock listbox and simulate a selected file
        duplicate_finder.listbox = MagicMock()
        duplicate_finder.listbox.curselection.return_value = [0]
        duplicate_finder.listbox.get.return_value = "fake_file_path.txt"

        # Mock `os.remove` to raise an `OSError`, simulating a deletion failure
        with patch("os.remove", side_effect=OSError("Delete error")):
            duplicate_finder.delete_selected()

        # Verify `askyesno` was called to confirm the deletion
        mock_askyesno.assert_called_once_with(
            "Delete confirmation", "Are you sure you want to delete the selected files?"
        )

        # Verify the error message is shown when deletion fails
        mock_showerror.assert_called_once_with("Error", "Failed to delete file: Delete error")

    @patch("duplicate_finder.messagebox.showwarning")
    def test_open_selected_no_selection(self, mock_showwarning, duplicate_finder):
        # Test open selected with no file selected
        duplicate_finder.listbox = MagicMock()
        duplicate_finder.listbox.curselection.return_value = []
        duplicate_finder.open_selected()
        mock_showwarning.assert_called_once_with("No selection", "Please select files to open.")
