import pytest
from calculator import Calculator

class TestCalculator:
  
      # test case for print details of Snack
    def test_addition(self):
        c = Calculator(5,7)
        add_val = c.calc_add()
        print("testing addition")
        assert (5, 7, 12)  == (c.num1, c.num2, add_val)
  
    # test case for calculating exiry date of Snack
    def test_multiplication(self):
        c = Calculator(6,9)
        mult_val = c.calc_multiply()
        print("testing multiplication")
        assert (6, 9, 54)  == (c.num1, c.num2, mult_val)