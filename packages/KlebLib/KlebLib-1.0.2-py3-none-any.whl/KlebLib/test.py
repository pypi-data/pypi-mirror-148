from KlebLib import fraction, polynomial, baseconversion, universaladdition, series
from typing import Any

class Test:
    def __init__(self, testType:str, **kwargs):
        self.testType = testType
        self.kwargs = kwargs

    def test(self, *args:Any) -> str:
        if self.testType == 'fraction':
            return self._fraction_test(args)
        elif self.testType == 'polynomial':
            return self._polynomial_test(args)
        elif self.testType == 'baseconversion':
            return self._conversion_test(args)
        elif self.testType == 'universaladdition':
            return self._universal_addition_test(args)
        elif self.testType == 'series':
            return self._series_test(args)

    def __repr__(self):
        output = f'Test({self.testType}, '

        #print(f'kwargs are of length {len(self.kwargs)}') #debug
        for i, (k, v) in enumerate(self.kwargs.items()):
            output += f'{k}=\'{v}\''
            if i != len(self.kwargs.keys()) - 1:
                output += ', '

        output += ')'
        return output

    #Individual tests

    def _fraction_test(self, args):
        fraction1 = fraction.Fraction(self.kwargs['fraction1'])
        fraction2 = fraction.Fraction(self.kwargs['fraction2'])

        opType = self.kwargs['opType']
        if opType == 'add' or opType == '+':
            fraction3 = fraction1 + fraction2
        elif opType == 'subtract' or opType == '-':
            fraction3 = fraction1 - fraction2
        elif opType == 'multiply' or opType == '*':
            fraction3 = fraction1 * fraction2
        elif opType == 'divide' or opType == '/':
            fraction3 = fraction1 / fraction2

        return str(fraction3)

    def _polynomial_test(self, args):
        testPolynomial = polynomial.Polynomial(self.kwargs['polynomial'])

        differentiated = testPolynomial.differentiate(args[0])
        integrated = testPolynomial.integrate(args[0])

        return str({
            'polynomial': testPolynomial.polynomial,
            'readable': str(testPolynomial),
            'differentiated': differentiated.polynomial,
            'integrated': integrated.polynomial
        })

    def _conversion_test(self, args):
        num = self.kwargs['num']
        base = self.kwargs['base']
        convertedBase = self.kwargs['baseToConvertTo']

        return baseconversion.convert_base(num, base, convertedBase)

    def _universal_addition_test(self, args):
        num1 = self.kwargs['num1']
        num2 = self.kwargs['num2']
        base = self.kwargs['base']

        return universaladdition.add(base, num1, num2)

    def _series_test(self, args):
        testSeries = series.Series(self.kwargs['data'], self.kwargs['type'], self.kwargs['strictType'])
        return str({'base series': str(testSeries),
                    'base series + arg': str(testSeries + args[0])})