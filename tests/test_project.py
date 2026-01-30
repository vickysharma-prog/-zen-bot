"""Tests for Zen-Bot - CS50P Required."""

import pytest
from project import process_command, is_exit_command, format_time


class TestProcessCommand:
    """Test process_command function."""
    
    def test_hello(self):
        assert "Hello" in process_command("hello")
    
    def test_hi(self):
        assert "Hello" in process_command("hi")
    
    def test_time(self):
        result = process_command("what time is it")
        assert "time" in result.lower() or "AM" in result or "PM" in result
    
    def test_date(self):
        result = process_command("what is the date")
        assert "Today" in result
    
    def test_name(self):
        result = process_command("what is your name")
        assert "Zen" in result
    
    def test_unknown(self):
        result = process_command("random xyz")
        assert "heard" in result.lower()


class TestIsExitCommand:
    """Test is_exit_command function."""
    
    def test_exit(self):
        assert is_exit_command("exit") == True
    
    def test_quit(self):
        assert is_exit_command("quit") == True
    
    def test_bye(self):
        assert is_exit_command("bye") == True
    
    def test_hello_not_exit(self):
        assert is_exit_command("hello") == False
    
    def test_case_insensitive(self):
        assert is_exit_command("EXIT") == True


class TestFormatTime:
    """Test format_time function."""
    
    def test_morning(self):
        assert format_time(9, 30) == "9:30 AM"
    
    def test_afternoon(self):
        assert format_time(14, 45) == "2:45 PM"
    
    def test_midnight(self):
        assert format_time(0, 0) == "12:00 AM"
    
    def test_noon(self):
        assert format_time(12, 0) == "12:00 PM"
    
    def test_invalid_hour(self):
        with pytest.raises(ValueError):
            format_time(25, 0)
    
    def test_invalid_minute(self):
        with pytest.raises(ValueError):
            format_time(10, 60)