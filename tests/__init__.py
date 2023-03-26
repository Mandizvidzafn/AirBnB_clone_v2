import unittest
import os
import mysql.connector
from models.state import State
from models import storage


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "not testing db storage")
class TestStateDB(unittest.TestCase):
    ''' Tests State class with MySQL '''

    def setUp(self):
        ''' Set up the test environment '''
        # Connect to the test database
        self.db = mysql.connector.connect(user=os.getenv("HBNB_MYSQL_USER"),
                                   passwd=os.getenv("HBNB_MYSQL_PWD"),
                                   host=os.getenv("HBNB_MYSQL_HOST"),
                                   db=os.getenv("HBNB_MYSQL_DB"))
        # Create a cursor for executing queries
        self.cursor = self.db.cursor()
        # Create a test state
        self.test_state = State(name="California")
        self.test_state.save()

    def tearDown(self):
        ''' Tear down the test environment '''
        # Delete the test state
        self.cursor.execute("DELETE FROM states WHERE id='{}'"
                             .format(self.test_state.id))
        self.db.commit()
        # Close the database connection
        self.cursor.close()
        self.db.close()

    def test_create_state(self):
        ''' Test the create State command '''
        # Get the number of current records in the states table
        self.cursor.execute("SELECT COUNT(*) FROM states")
        count_before = self.cursor.fetchone()[0]
        # Create a new state using the console command
        state = State(name="Nevada")
        state.save()
        # Get the number of current records in the states table again
        self.cursor.execute("SELECT COUNT(*) FROM states")
        count_after = self.cursor.fetchone()[0]
        # Assert that the number of records increased by 1
        self.assertEqual(count_after, count_before + 1)

    def test_create_with_params(self):
        """Test creating objects with parameters"""
        # Test creating a State with name parameter
        self.console.do_create("State name=\"California\"")
        self.assertTrue(len(self.console.all("State")) == 1)
    
        # Test creating a Place with multiple parameters
        self.console.do_create("Place city_id=\"0001\" user_id=\"0001\" name=\"My_little_house\" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297")
        self.assertTrue(len(self.console.all("Place")) == 1)
    
        # Test creating an object with invalid parameter
        self.console.do_create("Place invalid_param=5")
        self.assertTrue(len(self.console.all("Place")) == 1)
    
        # Test creating an object with invalid value for parameter
        self.console.do_create("Place city_id=invalid_value")
        self.assertTrue(len(self.console.all("Place")) == 1)
    
        # Test creating an object with incomplete parameter syntax
        self.console.do_create("Place city_id")
        self.assertTrue(len(self.console.all("Place")) == 1)
    
        # Test creating an object with missing parameter value
        self.console.do_create("Place city_id=")
        self.assertTrue(len(self.console.all("Place")) == 1)
    
        # Test creating an object with float parameter value
        self.console.do_create("Place price_by_night=300.50")
        self.assertTrue(len(self.console.all("Place")) == 2)
    
        # Test creating an object with integer parameter value
        self.console.do_create("Place max_guest=5")
        self.assertTrue(len(self.console.all("Place")) == 3)
    
        # Test creating an object with string parameter value containing double quote
        self.console.do_create("Place name=\"My\"\"little\"\"house\"")
        self.assertTrue(len(self.console.all("Place")) == 4)
    
        # Test creating an object with string parameter value containing underscore
        self.console.do_create("Place name=My_little_house")
        self.assertTrue(len(self.console.all("Place")) == 5)


if __name__ == '__main__':
    unittest.main()
