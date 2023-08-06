try:
    from .fraction import Fraction, EgyptFraction

except ImportError:
    from fraction import Fraction, EgyptFraction

def fraction_test():
    test1 = Fraction(2, 6)
    test2 = Fraction(5, 6)
    test3 = Fraction(15, 7)
    test3 += 1
    test4 = test2 - test1
    test5 = Fraction(3, 2)
    test6 = Fraction(1, 33554432)
    test7 = test6
    test8 = Fraction(100, 97)
    test9 = Fraction(808, 990)
    test10 = Fraction(5.8737125)
    test11 = Fraction('12.213488')
    test12 = Fraction('12.[21]')
    test13 = Fraction('12.8[34]')

    print(test1)
    print(test1.numerator)
    print(test1.denominator)
    print(test2.gcd(test3))
    print(test2.lcm(test3))
    test4.simplify()
    print(repr(test4))
    print(test1 * test5 < test4)
    print(test1 * test5 > test4)
    print(test1 * test5 == test4)
    print(test1 * test5 <= test4)
    print(test1 * test5 >= test4)
    print(test1 * test5 != test4)
    print(1 + test1 + test2 + test3 + 1)
    print(1 - test4 - test1 - 1)
    print(3 * test4 * test3 * 2)
    print(3 / test4 / test3 / 2)
    print(333 // test4 // test3 // 2)
    print(2 ** (-test1) ** -test2 ** -3)
    print(2 ** -test1 ** (-test2) ** -3)
    print(test6.to_decimal_string())
    print(test7.to_decimal_float())
    print(test3.to_decimal_string())
    print(test8.to_decimal_string())
    print(test9.to_decimal_string())
    print(test10)
    print(test11)
    print(test12)
    print(test13)

def egyptfractiontest():
    test1 = EgyptFraction(5, 11)
    test2 = EgyptFraction('0.[09]')
    test3 = test1 + test2
    test4 = EgyptFraction('0.[09756]')
    test5 = EgyptFraction(3, 97)
    
    print(test1.to_list())
    print(test1.to_list(use_string = False))
    print(test4)
    print(test5)
    print(Fraction(test3))

def main():
    fraction_test()
    egyptfractiontest()

if __name__ == '__main__':
    main()