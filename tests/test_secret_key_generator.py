import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch, Mock
import pytest
from secret_key_generator import SecretKeyGenerator


@pytest.fixture
def generator():
    # Create a root Tkinter instance and mock the init_welcome_screen method
    root = tk.Tk()
    root.init_welcome_screen = Mock()
    generator = SecretKeyGenerator(root)
    return generator


class TestSecretKeyGenerator:
    def test_initialization(self, generator):
        # Test the initialization without errors
        assert isinstance(generator, SecretKeyGenerator)

    @patch("secret_key_generator.messagebox.showinfo")
    def test_generate_secret_key_valid_length(self, mock_info, generator):
        # Test generation with a valid length
        generator.length_var.set("16")
        generator.generate_secret_key()
        mock_info.assert_called_once()

    @patch("secret_key_generator.messagebox.showerror")
    def test_generate_secret_key_invalid_length(self, mock_error, generator):
        # Test with an invalid length (0)
        generator.length_var.set("0")
        generator.generate_secret_key()
        mock_error.assert_called_once_with("Error", "Invalid value: Number of characters must be greater than zero.")

    @patch("secret_key_generator.messagebox.showerror")
    def test_generate_secret_key_non_integer_length(self, mock_error, generator):
        # Test with a non-integer input
        generator.length_var.set("not_an_integer")
        generator.generate_secret_key()
        mock_error.assert_called_once_with("Error",
                                           "Invalid value: invalid literal for int() with base 10: 'not_an_integer'")

    def test_copy_to_clipboard(self, generator):
        # Test if copy_to_clipboard works as expected
        generator.copy_to_clipboard("test_key")
        assert generator.clipboard_get() == "test_key"
