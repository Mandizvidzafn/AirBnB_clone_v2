import unittest
import mysql.connector
from models import storage
from console import HBNBCommand

class TestConsole(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set up the MySQL database for testing """
        cls.db = mysql.connector.connect(
            user='hbnb_test',
            password='hbnb_test_pwd',
            host='localhost',
            database='hbnb_test_db'
        )
        cls.cursor = cls.db.cursor()
        cls.command = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """ Clean up the MySQL database after testing """
        cls.cursor.execute("DROP TABLE states")
        cls.cursor.close()
        cls.db.close()

    def setUp(self):
        """ Set up the test environment """
        self.cursor.execute("TRUNCATE TABLE states")

    def test_create_command_with_mysql(self):
        """ Test that create command adds a new record to the MySQL database """
        # Get the initial number of records in the table
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]

        # Execute the console command
        self.command.onecmd("create State name='California'")

        # Get the final number of records in the table
        self.cursor.execute("SELECT COUNT(*) FROM states")
        final_count = self.cursor.fetchone()[0]

        # Assert that the difference in counts is 1
        self.assertEqual(final_count - initial_count, 1)


class TestCreateCommand(unittest.TestCase):

    def setUp(self):
        self.cli = HBNBCommand()

    def test_create_with_params(self):
        # test creating an object with parameters
        class_name = "BaseModel"
        params = 'name="My little house" age=30 is_occupied=True'
        result = self.cli.onecmd(f"create {class_name} {params}")
        self.assertIn("My little house", result)
        self.assertIn("30", result)
        self.assertIn("True", result)

    def test_create_with_invalid_params(self):
        # test creating an object with invalid parameters
        class_name = "BaseModel"
        params = 'invalid_param="invalid_value" valid_param=10'
        result = self.cli.onecmd(f"create {class_name} {params}")
        self.assertNotIn("invalid_value", result)
        self.assertIn("10", result)

if __name__ == '__main__':
    unittest.main()
