#!/usr/bin/python3
"""Tests for the console create command."""

import re
import subprocess
import unittest


class TestConsoleCreate(unittest.TestCase):
    """Test the create command with parameters."""

    def run_console(self, commands):
        """Run console.py with the supplied commands."""
        if isinstance(commands, str):
            commands = [commands]

        input_data = "\n".join(commands) + "\nquit\n"

        process = subprocess.Popen(
            ["python3", "console.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate(
            input_data.encode("utf-8")
        )

        return stdout.decode("utf-8")

    def get_uuid(self, output):
        """Extract a UUID from console output."""
        match = re.search(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
            r"[0-9a-f]{4}-[0-9a-f]{12}",
            output
        )
        return match.group(0) if match else None

    def test_create_state(self):
        """Test creating a State without parameters."""
        output = self.run_console("create State")

        state_id = self.get_uuid(output)

        self.assertIsNotNone(state_id)

    def test_create_state_string(self):
        """Test string parameter and underscore conversion."""
        output = self.run_console(
            'create State name="My_little_house"'
        )

        state_id = self.get_uuid(output)

        self.assertIsNotNone(state_id)

    def test_invalid_parameters_are_skipped(self):
        """Test invalid parameters do not prevent object creation."""
        output = self.run_console(
            'create State name="California" invalid=abc'
        )

        state_id = self.get_uuid(output)

        self.assertIsNotNone(state_id)

    def test_create_place_numeric_parameters(self):
        """Test integer and float parameters."""
        output = self.run_console(
            'create Place city_id="0001" user_id="0001" '
            'name="Beautiful Place" number_rooms=3 '
            'number_bathrooms=2 max_guest=4 '
            'price_by_night=100 latitude=5.6037 '
            'longitude=-0.1870'
        )

        place_id = self.get_uuid(output)

        self.assertIsNotNone(place_id)

    def test_create_city(self):
        """Test creating a City with parameters."""
        output = self.run_console(
            'create City name="Accra" state_id="0001"'
        )

        city_id = self.get_uuid(output)

        self.assertIsNotNone(city_id)

    def test_create_user(self):
        """Test creating a User with parameters."""
        output = self.run_console(
            'create User email="test@example.com" '
            'password="secret" first_name="Test" last_name="User"'
        )

        user_id = self.get_uuid(output)

        self.assertIsNotNone(user_id)


if __name__ == "__main__":
    unittest.main()
