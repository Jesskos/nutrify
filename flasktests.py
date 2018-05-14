
from unittest import TestCase
from server import app 
from model import connect_to_db, db, example_data



    def test_for_new_user_registering(self):
        result = client.post("/add-registration-info", data= {'first_name':'Harry',
                                                                    'last_name':'Potter',
                                                                    'email':'hpotter@hogwarts.edu',
                                                                    'password':'Ginny'} )
        self.assertIn('Please Log In!', result.data)



if __name__ == '__main__':

    import unittest
    unittest.main()