import re
from typing import Union

class Fraction:
    def __init__(self, fraction:Union[list, str, int, float]):
        self.skipSimplify = True
        
        if type(fraction) is list:
            self.num = fraction[0]
            self.dem = fraction[1]
            
        elif type(fraction) is str:
            fractionNums = fraction.split('/')
            fractionNums = [int(i) for i in fractionNums]
            self.num = fractionNums[0]
            self.dem = fractionNums[1]

        elif type(fraction) is int or type(fraction) is float:
            fractionNums = self._num_to_fraction(fraction)
            self.num = fractionNums[0]
            self.dem = fractionNums[1]
            
        else:
            raise TypeError(f'cannot parse type {type(fraction).__name__}')

        self._simplify()

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        
        if attr == 'num' or attr == 'dem':
            if self.skipSimplify and attr == 'dem':
                self.skipSimplify = False
            elif not self.skipSimplify:
                self._simplify()

    #Get the greatest common divisor of the numerator and denominator
    @property
    def GCD(self) -> int:
        num1 = self.num
        num2 = self.dem

        if num1 < num2:
            temp = num1
            num1 = num2
            num2 = temp

        remainder = num1 % num2
        while remainder != 0:
            num1 = num2
            num2 = remainder

            remainder = num1 % num2

        #print(f'GCD is {abs(num2)}') #debug
        return abs(num2)

    #Simplify the fraction
    def _simplify(self) -> None:
        #print(f'simplifying {self}') #debug
        self.skipSimplify = True
        
        num = self.num
        dem = self.dem

        #Ensure that negatives are represented in the numerator and there is no double negative
        if dem < 0:
            #print('flipping negatives') #debug
            num = -num
            dem = -dem

        num //= self.GCD
        dem //= self.GCD

        self.num = num
        self.dem = dem

    #Simplify a given fraction in list form
    def _simplify_nums(nums):
        return Fraction(nums, True).nums

    #Automatically simplify fractions
    def autosimplify(func):
        def inner(*args, **kwargs):
            fraction = func(*args, **kwargs)
            fraction.simplify
            return fraction
        return inner

    #Output the numbers as a fraction
    def __str__(self) -> str:
        return (f'{self.num}/{self.dem}')

    def __repr__(self) -> str:
        return f'fraction.Fraction([{self.num}, {self.dem}])'

    #Output the fraction as an int
    def __int__(self) -> int:
        return int(self.num / self.dem)

    #Output the fraction as a float
    def __float__(self) -> float:
        return self.num / self.dem

    #Compares this fraction to another
    def __eq__(self, other):
        return self.num == other.num and self.dem == other.dem

    #Compares this fraction to another and inverts
    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return float(self) > float(other)

    def __ge__(self, other):
        return float(self) >= float(other)

    def __lt__(self, other):
        return float(self) < float(other)

    def __le__(self, other):
        return float(self) <= float(other)

    #Adds two given fractions
    def _add(self, fraction1, fraction2):
        num = (fraction1.num * fraction2.dem) + (fraction1.dem * fraction2.num)
        dem = fraction1.dem * fraction2.dem

        return Fraction([num, dem])

    #Subtracts two given fractions
    def _sub(self, fraction1, fraction2):
        num = (fraction1.num * fraction2.dem) - (fraction1.dem * fraction2.num)
        dem = fraction1.dem * fraction2.dem

        return Fraction([num, dem])

    #Multiplies two given fractions
    def _mul(self, fraction1, fraction2):
        num = fraction1.num * fraction2.num
        dem = fraction1.dem * fraction2.dem

        return Fraction([num, dem])

    #Divides two given fractions
    def _truediv(self, fraction1, fraction2):
        num = fraction1.num * fraction2.dem
        dem = fraction1.dem * fraction2.num

        return Fraction([num, dem])

    #Adds another fraction to this one and returns a new fraction
    def __add__(self, other):
        if type(other) is not Fraction:
            try:
                other = self._num_to_fraction(other)
            except TypeError:
                raise TypeError(f'Cannot add type {type(other)} to fraction')
            
        return self._add(self, other)

    #Subtracts another fraction from this one and returns a new fraction
    def __sub__(self, other):
        if type(other) is not Fraction:
            try:
                other = self._num_to_fraction(other)
            except TypeError:
                raise TypeError(f'Cannot add type {type(other)} to fraction')
                
        return self._sub(self, other)

    #Multiplies another fraction by this one and returns a new fraction
    def __mul__(self, other):
        if type(other) is not Fraction:
            try:
                other = self._num_to_fraction(other)
            except TypeError:
                raise TypeError(f'Cannot add type {type(other)} to fraction')
                
        return self._mul(self, other)

    #Divides this fraction by another one and returns a new fraction
    def __truediv__(self, other):
        if type(other) is not Fraction:
            try:
                other = self._num_to_fraction(other)
            except TypeError:
                raise TypeError(f'Cannot add type {type(other)} to fraction')
                
        return self._truediv(self, other)

    #Adds another fraction to this one and returns a new fraction
    def __radd__(self, number):
        #print(f'adding self to {number}') #debug
        other = self._num_to_fraction(number)
            
        return self._add(other, self)

    #Subtracts another fraction from this one and returns a new fraction
    def __rsub__(self, number):
        #print(subtracting self from {number}') #debug
        other = self._num_to_fraction(number)
            
        return self._sub(other, self)

    #Multiplies another fraction by this one and returns a new fraction
    def __rmul__(self, number):
        #print(multiplying {number} by self') #debug
        other = self._num_to_fraction(number)
        
        return self._mul(other, self)

    #Divides this fraction by another one and returns a new fraction
    def __rtruediv__(self, number):
        #print(dividing {number} by self') #debug
        other = self._num_to_fraction(number)
        
        return self._truediv(other, self)

    #Adds this fraction to another one and replaces this fraction with the result
    def __iadd__(self, other):
        if type(other) is not Fraction:
            try:
                other = self._num_to_fraction(other)
            except TypeError:
                raise TypeError(f'Cannot add type {type(other)} to fraction')
                
        answer = self._add(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    #Subtracts another fraction from this one and replaces this fraction with the result
    def __isub__(self, other):
        if type(other) is not Fraction:
            try:
                other = self._num_to_fraction(other)
            except TypeError:
                raise TypeError(f'Cannot add type {type(other)} to fraction')
                
        answer = self._sub(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    #Multiplies this fraction by another one and replaces this fraction with the result
    def __imul__(self, other):
        if type(other) is not Fraction:
            try:
                other = self._num_to_fraction(other)
            except TypeError:
                raise TypeError(f'Cannot add type {type(other)} to fraction')
                
        answer = self._mul(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    #Divides this fraction by another one and replaces this fraction with the result
    def __itruediv__(self, other):
        if type(other) is not Fraction:
            try:
                other = self._num_to_fraction(other)
            except TypeError:
                raise TypeError(f'Cannot add type {type(other)} to fraction')
                
        answer = self._truediv(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    #Flips this fraction between positive and negative
    def __neg__(self):
        return Fraction([-self.num, self.dem])

    #Updates this fraction to its reciprocal
    def invert(self):
        return Fraction([self.dem, self.num])

    #Returns either the numerator or denominator, as if the fraction were a list in form [num, dem]
    def __getitem__(self, index):
        if index == 0:
            return self.num
        elif index == 1:
            return self.dem
        else:
            raise IndexError(f'Invalid value for index: {index}. Must be 0 or 1')
    
    #Returns a mixed fraction
    @property
    def mixed(self):
        integerPart = 0
        num = self.num
        dem = self.dem

        while num > dem:
            num -= dem
            integerPart += 1

        return [integerPart, [num, dem]]

    #Sets the fraction to the top-heavy form of a given mixed fraction
    @mixed.setter
    def mixed(self, fraction:Union[str, list]):
        #Fraction given in form [integerPart, [num, dem]] or 'integerPart num/dem'
        if type(fraction) is str:
            fraction = fraction.split(' ')
            temp = [int(i) for i in fraction[1].split('/')]
            fraction = [int(fraction[0]), temp]
            
        fraction[1][0] += fraction[0] * fraction[1][1]
        self.num = fraction[1][0]
        self.dem = fraction[1][1]

    #Returns a list of the numerator and denominator
    @property
    def nums(self):
        return ([self.num, self.dem])

    #Updates the fraction through the use of nums
    @nums.setter
    def nums(self, numsList:list):
        self.num = numsList[0]
        self.dem = numsList[1]

        self.simplify()

    def _num_to_fraction(self, number):
        if round(number, 0) == number:
            return Fraction([number, 1])
        else:
            decPlaces = len(str(number)[re.search(r'\.', str(number)).start() + 1:])
            number *= 10 ** decPlaces

            return Fraction([number, 10 ** decPlaces])