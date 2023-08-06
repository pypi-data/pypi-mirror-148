from core.number.BigFloat import BigFloat


class BigFloatAdd:

    def __init__(self, amount: BigFloat, other: BigFloat):
        self.number = 0
        self.leading_zeros = 0
        self.amount = amount
        self.other = other
        self.__pad_fractions()

    def __pad_fractions(self):
        fraction_length = self.amount.fraction_leading_zeros + self.__size(self.amount.fraction)
        other_fraction_length = self.other.fraction_leading_zeros + self.__size(self.other.fraction)
        if fraction_length > other_fraction_length:
            pad = fraction_length - other_fraction_length
            self.other.fraction = self.other.fraction * (10 ** pad)
        elif fraction_length < other_fraction_length:
            pad = other_fraction_length - fraction_length
            self.amount.fraction = self.amount.fraction * (10 ** pad)

    @staticmethod
    def __size(number):
        return len(str(number))

    def __largest(self, number, another):
        number_size = self.__size(number)
        another_number_size = self.__size(another)
        if number_size > another_number_size:
            return number_size
        elif another_number_size > number_size:
            return another_number_size
        return another_number_size

    def result(self):
        self.number = self.amount.number + self.other.number
        self.leading_zeros = self.calculate_different_leading_zeros()
        fraction = self.add_fractions()
        return BigFloat(self.number, fraction, self.leading_zeros)

    def add_fractions(self):
        largest_fraction_size_before = self.__largest(self.amount.fraction, self.other.fraction)
        fraction = self.amount.fraction + self.other.fraction
        fraction_size_after = self.__size(fraction)
        if fraction_size_after > largest_fraction_size_before:
            leading_zeros = self.leading_zeros - (fraction_size_after - largest_fraction_size_before)
            if leading_zeros < 0:
                number_to_add = fraction // (10 * abs(leading_zeros))
                self.number = self.number + number_to_add
                fraction = fraction % (10 * abs(leading_zeros))
                self.leading_zeros = 0
            else:
                self.leading_zeros = leading_zeros
        return fraction

    def calculate_different_leading_zeros(self):
        if self.amount.fraction_leading_zeros > self.other.fraction_leading_zeros:
            return self.other.fraction_leading_zeros
        elif self.amount.fraction_leading_zeros < self.other.fraction_leading_zeros:
            return self.amount.fraction_leading_zeros
        return self.amount.fraction_leading_zeros
