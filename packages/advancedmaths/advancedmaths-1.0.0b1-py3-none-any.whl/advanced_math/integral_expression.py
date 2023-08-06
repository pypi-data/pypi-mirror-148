'''
A module to calculate the integral expressions.
'''

class CoefficentError(Exception):
    '''
    The coefficent error class.
    '''

class ExponentialError(Exception):
    '''
    The exponential error class.
    '''

class Monomial():
    '''
    The monomial main class.
    '''
    def __init__(self, coefficient, num, exponential):
        '''
        coefficient - int / str only with numbers
        num - int / str / str with symbol 'x' ('5x', '5*x' and '6(x+2)' are all ok but '6(3+4)' is not ok)
        exponential - int / str only with numbers
        '''
        self.process_coefficient(coefficient)
        self.process_num(num)
        self.process_exponential(exponential)
    
    def process_coefficient(self, coefficient):
        try:
            int(str(coefficient).replace(' ', '').replace('+', '').replace('-', '')
            .replace('*', '').replace('*', '').replace('/', '')
            .replace('(', '').replace(')', ''))

        except ValueError:
            raise CoefficentError(f'Invalid coefficent \'{coefficient}\'') from None

        try:
            self.coe = eval(str(coefficient), {})

        except Exception:
            raise CoefficentError(f'Invalid coefficent \'{coefficient}\'') from None
    
    def process_num(self, num):
        self.num = str(num).replace(' ', '')
        index_x = 0
        for ignored in range(self.num.count('x')):
            try:
                int(self.num[self.num.index('x', index_x) - 1])

            except ValueError:
                pass

            else:
                self.num = self.num[:self.num.index('x', index_x)] + '*' + \
                    self.num[self.num.index('x', index_x):]
                index_x = self.num.index('x', index_x) + 1
        
        index_x = 0
        for ignored in range(self.num.count('(')):
            try:
                int(self.num[self.num.index('(', index_x) - 1])

            except ValueError:
                pass

            else:
                self.num = self.num[:self.num.index('(', index_x)] + '*' + \
                    self.num[self.num.index('(', index_x):]
                index_x = self.num.index('(', index_x) + 1
        
        for x in range(self.num.count('(')):
            pass
    
    def process_exponential(self, exponential):
        try:
            int(str(exponential).replace(' ', '').replace('+', '').replace('-', '')
            .replace('*', '').replace('*', '').replace('/', '')
            .replace('(', '').replace(')', ''))

        except ValueError:
            raise ExponentialError(f'Invalid exponential \'{exponential}\'') from None

        try:
            self.exp = eval(str(exponential), {})

        except Exception:
            raise ExponentialError(f'Invalid exponential \'{exponential}\'') from None

class Polynomial():
    '''
    The polynomial main class.
    '''
    def __init__(self, *monomial_or_symbol):
        '''
        monomial_or_symbol - monomial / str only with one symbol
        '''
        self.monomial_symbol_list = monomial_or_symbol

a = Monomial('5 + 2 * 2', '5x+6(2x+6+3x)+7-(2*x-2)', 2)
print(a.coe)
print(a.num)
print(a.exp)
b = Monomial(9, '33x+80', 2)
print(b.coe)
print(b.num)
print(b.exp)
c = Monomial(1, '2x', 2)
print(c.coe)
print(c.num)
print(c.exp)