from ib_calculator import calculator

def main():
    c = calculator.Calculator(3,4)
    add_val = c.calc_add()
    print( "result of addition " + str(add_val))
    mult_val = c.calc_multiply()
    print( "result of multiplication " + str(mult_val))

if __name__ == '__main__':
    main()