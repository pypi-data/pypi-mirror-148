'''
A module to calculate the fractions which are better than floats.
'''

from math import gcd, lcm, ceil, floor, trunc, sqrt

class Fraction():
    '''
    The fraction main class.
    '''
    def __init__(self, numerator = None, denominator = None):
        '''
        numerator - the numerator
        denominator - the denominator
        numerator -> None, denominator -> None: fraction 0/1
        numerator -> int/float/string, denominator -> None: fraction to express numerator
        numerator -> None, denominator -> int/float/string: fraction to express 1/denominator
        numerator -> int/string, denominator -> int: fraction to express numerator/denominator (both are int)
        note: string '0.[3]' -> 0.333..., string '5.0[6] -> 5.0666...
        '''
        self.reverse = False
        self.numerator = 1
        self.denominator = 1
        if numerator is None and denominator is None:
            self.numerator = 0
            self.denominator = 1

        elif numerator is not None and denominator is None:
            if isinstance(numerator, float):
                self._process_float(numerator)
            
            elif isinstance(numerator, str):
                if '[' in numerator:
                    self._process_repeated_float(numerator)
                
                else:
                    self._process_float(float(numerator))
            
            else:
                self.numerator = numerator
                self.denominator = 1

        elif numerator is None and denominator is not None:
            if denominator == 0:
                raise ZeroDivisionError('The denominator mustn\'t be 0!')
            
            self.reverse = True

            if isinstance(denominator, float):
                self._process_float(denominator)
            
            elif isinstance(denominator, str):
                if '[' in denominator:
                    self._process_repeated_float(denominator)
                
                else:
                    self._process_float(float(denominator))
            
            else:
                self.numerator = denominator
                self.denominator = numerator
            
            self.reverse = False

        else:
            if int(numerator) == numerator and int(denominator) == denominator:
                if int(denominator) == 0:
                    raise ZeroDivisionError('The denominator mustn\'t be 0!')
                    
                self.numerator = int(numerator)
                self.denominator = int(denominator)

            else:
                raise ValueError('The numerator and the denominator must be a int!')

    def _process_float(self, numerator: float):
        '''
        Internal function.
        '''
        if numerator == 0:
            self.numerator = 0
            self.denominator = 1
            return

        x = numerator
        while True:
            x = int(x * 10) + float('0.' + str(x).split('.')[1][1:])
            str_x = str(x)
            str_x = str_x.rstrip('0')
            str_x = str_x.rstrip('.')
            if '.' not in str_x:
                x = int(str_x)
                gcd_two = gcd(int(x), int(x / numerator))
                if self.reverse:
                    self.denominator = int(x / gcd_two)
                    self.numerator = int(x / numerator / gcd_two)
                
                else:
                    self.numerator = int(x / gcd_two)
                    self.denominator = int(x / numerator / gcd_two)

                break
    
    def _process_repeated_float(self, numerator: str):
        '''
        Internal function.
        '''
        negative = False
        if numerator[0] == '-':
            negative = True
            numerator = numerator[1:]

        repeated = numerator.split('[')[1][:-1]
        not_repeated = numerator.split('.')[1].split('[')[0]
        decimal = numerator.split('.')[1].replace('[', '').replace(']', '')
        int_part = int(numerator.split('.')[0])

        y = int(len(repeated) * '9' + len(not_repeated) * '0')
        if numerator[numerator.find('.') + 1] == '[':
            x = int(repeated)
        
        else:
            x = int(decimal) - int(not_repeated)
        
        x += int_part * y

        gcd_two = gcd(x, y)
        if self.reverse:
            self.denominator = int(x / gcd_two)
            self.numerator = int(y / gcd_two)
                
        else:
            self.numerator = int(x / gcd_two)
            self.denominator = int(y / gcd_two)

        if negative:
            self.numerator = -self.numerator
    
    def __delattr__(self, item):
        raise AttributeError(f'The item \'{item}\' cannot be deleted.')
    
    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)

        return f'{self.numerator}/{self.denominator}'
    
    def __repr__(self):
        return f'fraction({self.numerator}, {self.denominator})'
    
    def __bool__(self):
        return self.numerator != 0
    
    def __pos__(self):
        return self
    
    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)
    
    def __abs__(self):
        return Fraction(abs(self.numerator), self.denominator)
    
    def __invert__(self):
        return Fraction(-self.numerator - 1, self.denominator)
    
    def __round__(self, n):
        return round(float(self), n)
    
    def __ceil__(self):
        return ceil(float(self))
    
    def __floor__(self):
        return floor(float(self))
    
    def __trunc__(self):
        return trunc(self)
    
    def __sqrt__(self):
        return Fraction(sqrt(self.numerator), sqrt(self.denominator))
    
    def __add__(self, f):
        if isinstance(f, Fraction):
            if self.denominator == f.denominator:
                return Fraction(self.numerator + f.numerator, self.denominator).simplify()

            else:
                lcm_of_denominator = lcm(self.denominator, f.denominator)
                f1_mul = lcm_of_denominator / self.denominator
                f2_mul = lcm_of_denominator / f.denominator
                return (Fraction(self.numerator * f1_mul, self.denominator * f1_mul) + \
                    Fraction(f.numerator * f2_mul, f.denominator * f2_mul)).simplify()
        
        else:
            return self + Fraction(f)
    
    def __radd__(self, f):
        return self + f
    
    def __iadd__(self, f):
        self = self + f
        return self
    
    def __sub__(self, f):
        return self + -f
    
    def __rsub__(self, f):
        return -self + f
    
    def __isub__(self, f):
        self = self + -f
        return self
    
    def __mul__(self, f):
        if isinstance(f, Fraction):
            return Fraction(self.numerator * f.numerator, self.denominator * f.denominator).simplify()
        
        else:
            return Fraction(self.numerator * f, self.denominator).simplify()
    
    def __rmul__(self, f):
        return self * f
    
    def __imul__(self, f):
        self = self * f
        return self
    
    def __truediv__(self, f):
        if isinstance(f, Fraction):
            return Fraction(self.numerator * f.denominator, self.denominator * f.numerator).simplify()
        
        else:
            return Fraction(self.numerator, self.denominator * f).simplify()
    
    def __rtruediv__(self, f):
        if isinstance(f, Fraction):
            return Fraction(self.denominator * f.numerator, self.numerator * f.denominator).simplify()
        
        else:
            return Fraction(self.denominator * f, self.numerator).simplify()
    
    def __itruediv__(self, f):
        self = self / f
        return self
    
    def __floordiv__(self, f):
        return int(self / f)
    
    def __rfloordiv__(self, f):
        return int(f / self)
    
    def __ifloordiv__(self, f):
        self = self / f
        return int(self)
    
    def __pow__(self, f):
        return float(self) ** f
    
    def __rpow__(self, f):
        return f ** float(self)
    
    def __ipow__(self, f):
        self = Fraction(float(self) ** f)
        return self

    def __float__(self):
        return self.numerator / self.denominator
    
    def __int__(self):
        return self.numerator // self.denominator
    
    def __long__(self):
        return self.numerator // self.denominator
    
    def __cmp__(self, f):
        if float(self) < f:
            return -1
        elif float(self) > f:
            return 1
        else:
            return 0
    
    def __eq__(self, f):
        if not isinstance(f, Fraction):
            f = Fraction(f).simplify()

        a = self.simplify()
        return a.numerator == f.numerator and a.denominator == f.denominator
    
    def __ne__(self, f):
        if not isinstance(f, Fraction):
            f = Fraction(f).simplify()

        a = self.simplify()
        return a.numerator != f.numerator or a.denominator != f.denominator
    
    def __lt__(self, f):
        if not isinstance(f, Fraction):
            f = Fraction(f)
        
        lcm_two = lcm(self.denominator, f.denominator)
        return self.numerator * lcm_two / self.denominator < f.numerator * lcm_two / f.denominator
    
    def __gt__(self, f):
        return f < self
    
    def __le__(self, f):
        return self < f or self == f
    
    def __ge__(self, f):
        return self > f or self == f

    def simplify(self):
        '''
        Simpify the fraction of self.
        '''
        gcd_two = gcd(abs(self.numerator), abs(self.denominator))
        self.numerator //= gcd_two
        self.denominator //= gcd_two
        return self
    
    def gcd(self, f):
        return Fraction(gcd(self.numerator, f.numerator), lcm(self.denominator, f.denominator)).simplify()

    def lcm(self, f):
        return Fraction(lcm(self.numerator, f.numerator), gcd(self.denominator, f.denominator)).simplify()
    
    def to_decimal_string(self):
        self.simplify()
        if self.numerator / self.denominator == self.numerator // self.denominator:
            return str(self.numerator // self.denominator)

        deno = self.denominator
        t1 = False
        t2 = False
        while True:
            deno /= 2
            t = deno
            if deno == 1:
                t1 = True
                break
            elif int(t) != deno:
                break
        
        deno = self.denominator
        while True:
            deno /= 5
            t = deno
            if deno == 1:
                t2 = True
                break
            elif int(t) != deno:
                break
        
        i_num = self.numerator // self.denominator
        con = self.numerator % self.denominator * 10 // self.denominator
        r = self.numerator % self.denominator * 10 % self.denominator
        all_num = [[con, r]]

        while True:
            con = r * 10 // self.denominator
            r = r * 10 % self.denominator
            all_num.append([con, r])
            if t1 or t2:
                if r == 0:
                    output = str(i_num) + '.'
                    for x in all_num:
                        output += str(x[0])

                    return output

            else:
                if all_num.count([con, r]) == 2:
                    all_num = all_num[:-1]
                    repeat_start_index = all_num.index([con, r])
                    output = str(i_num) + '.'
                    i = 0
                    for x in all_num:
                        if i == repeat_start_index:
                            output += '['

                        output += str(x[0])
                        i += 1
                    
                    output += ']'
                    return output

    def to_decimal_float(self):
        '''
        May causes a precision loss.
        '''
        result = self.to_decimal_string()
        if '[' in result:
            raise ValueError('This fraction can\'t be converted to a float.')
        else:
            return float(result)

class EgyptFraction(Fraction):
    '''
    The egypt fraction main class.
    '''
    def __str__(self):
        output = ''
        l = self.to_list()
        for x in l:
            output += x
            if x != l[-1]:
                output += ', '

        return output

    def __repr__(self):
        return f'egyptfraction({self.numerator}, {self.denominator})'
    
    def to_list(self, *, use_string = True):
        output = []
        tmp = []
        t = self
        while True:
            a = t.numerator
            b = t.denominator
            temp = b % a
            if not temp:
                f = Fraction(a, b)
                if use_string:
                    o = str(f)
                
                else:
                    o = f

                output.append(o)
                tmp.append(o)
                break

            f = Fraction(1, b // a + 1)
            if use_string:
                o = str(f)
                
            else:
                o = f

            output.append(o)
            tmp.append(o)
            t -= f
        
        return output