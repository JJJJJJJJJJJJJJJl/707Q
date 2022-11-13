# MORE INFO: https://pythongeeks.org/python-unit-testing/

import unittest

def div(a,b):
    return a/b


class TestMethods(unittest.TestCase):
  def setUp(self): #Function that runs before each test to set any pre-requisites 
    pass

  def test_abs(self):
    self.assertEqual( abs(-5), 5) #tests if the absolute value of -5 is 5

  def test_pow(self):      #tests if 2 to the power of 5 is 32 
    self.assertEqual(pow(2,5),32)

  # Tests and returns TRUE if the boolean value is non empty or non 0
  # or else returns False.
  def test_bool(self):        
    self.assertTrue(bool(5))
    self.assertFalse(bool(''))

  # Returns true if the string splits and matches
  # the given output.
  def test_div(self):        
    s = 'hello world'
    self.assertEqual(div(2,5),0.4)
    with self.assertRaises(ZeroDivisionError):
      div(2,0)
        
if __name__ == '__main__':
    unittest.main()