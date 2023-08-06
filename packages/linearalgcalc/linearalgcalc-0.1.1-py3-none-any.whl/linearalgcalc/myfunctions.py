import math


class Complex:
    """
    This class is used to hold complex number objects.
    """

    def __init__(self, real, imaginary):
        """
        Initializes the complex class.

        :param real: The real float or integer of the complex number.
        :param imaginary: The imaginary float or integer of the complex number.
        """
        if type(real) != int and type(real) != float:
            raise TypeError("The real number should be an integer or float!")

        if type(imaginary) != int and type(imaginary) != float:
            raise TypeError("The imaginary number should be an integer or float!")

        self.real = real
        self.imaginary = imaginary

    def re(self):
        """
        Returns the real part of a complex number.
        :return: the real number.
        """

        return self.real

    def im(self):
        """
        Returns the imaginary part of a complex number.
        :return: the imaginary number.
        """

        return self.imaginary

    def addition(self, complex2):
        """
        Calculates the sum of two complex numbers.

        :param complex2: an instance of the complex class
        :return: a new instance of the complex class
        """
        if type(complex2) != Complex:
            raise TypeError("The variable complex2 must be an instance of the Complex class")

        return Complex(self.real + complex2.real, self.imaginary + complex2.imaginary)

    def subtraction(self, complex2):
        """
        Calculates the sum of two complex numbers.

        :param complex2: an instance of the complex class
        :return: a new instance of the complex class
        """
        if type(complex2) != Complex:
            raise TypeError("The variable complex2 must be an instance of the Complex class")

        return Complex(self.real - complex2.real, self.imaginary - complex2.imaginary)

    def multiplication(self, complex2):
        """
        Calculates the product of two complex numbers.

        :param complex2: an instance of the complex class
        :return: a new instance of the complex class
        """
        if type(complex2) != Complex:
            raise TypeError("The variable complex2 must be an instance of the Complex class")

        return Complex(self.real * complex2.real - self.imaginary * complex2.imaginary,
                       self.imaginary * complex2.real + self.real * complex2.imaginary)

    def conjugate(self):
        """
        Calculates and returns the complex conjugate.

        :return: a new instance of the complex class
        """

        return Complex(self.real, self.imaginary * -1)

    def modulus(self):
        """
        Calculates and returns the modulus (magnitude and size) of the complex number.

        :return: the modulus of the complex number
        """

        return (self.real ** 2 + self.imaginary ** 2) ** 0.5

    def polar_form(self):
        """
        Calculates and returns the polar form of the complex number.

        All arguments must be integers or floats.

        :return: the polar form as a string
        """
        r = self.modulus()

        theta = math.atan(self.imaginary / self.real)

        return "{}(cos{} + jsin{})".format(r, theta, theta)

    def exponent(self, exponent):
        """
        Calculates and returns the exponent of a complex number.

        All arguments must be integers or floats.

        :param exponent: the exponent
        :return: a new instance of the complex class
        """

        if type(exponent) != int and type(exponent) != float:
            raise Exception("The exponent number is not an integer or float.")

        r = self.modulus()
        theta = math.atan(self.imaginary / self.real)

        return Complex((r ** exponent) * math.cos(exponent * theta), (r ** exponent) * math.sin(exponent * theta))

    def roots(self, root):
        """
        Calculates and returns the nth roots of a complex number.

        All arguments can be integers or floats.

        :param root: the root
        :return: a list of instances of the complex class of the n roots of the complex number
        """
        if type(root) != int and type(root) != float:
            raise TypeError("The root number is not an integer or float.")

        r = self.modulus()
        theta = math.atan(self.imaginary / self.real)

        root_list = []

        for k in range(root):
            temp_complex = Complex((r ** (1 / root) * (math.cos((theta + math.pi * 2 * k) / root))), (
                    r ** (1 / root) * (math.sin((theta + math.pi * 2
                                                 * k) / root))))
            root_list.append(temp_complex)

        return root_list


class Vector:
    """
    This class is used to hold vector objects.
    """

    def __init__(self, numbers):
        """
        Initializes the vector class.
        :param numbers: A list of the integers or floats in the vector.
        """
        if type(numbers) != list:
            raise TypeError("Numbers should be a list of the numbers in the vector!")

        for num in numbers:
            if type(num) != float and type(num) != int:
                raise TypeError("The values in the list should be a float or integer!")

        self.numbers = numbers

    def addition(self, vector2):
        """
        Calculates and returns the sum of two vectors.

        Both vectors must be of the same size, and must have integers.

        :param vector2: an instance of the vector class
        :return: an instance of the vector class
        """

        if type(vector2) != Vector:
            raise TypeError("The vector2 variable must be of type Vector")

        vector_result = []

        if len(self.numbers) != len(vector2.numbers):
            raise Exception("The two vectors aren't of the same size")

        for i in range(len(self.numbers)):
            vector_result.append(self.numbers[i] + vector2.numbers[i])

        return Vector(vector_result)

    def subtraction(self, vector2):
        """
        Calculates and returns the difference of two vectors.

        Both vectors must be of the same size, and must have integers.

        :param vector2: an instance of the vector class
        :return: an instance of the vector class
        """

        vector_result = []
        if type(vector2) != Vector:
            raise TypeError("The vector2 variable must be of type Vector")

        if len(self.numbers) != len(vector2.numbers):
            raise Exception("The two vectors aren't of the same size")

        for i in range(len(self.numbers)):
            vector_result.append(self.numbers[i] - vector2.numbers[i])

        return Vector(vector_result)

    def scalar_multiplication(self, scalar):
        """
        Calculates and returns the product of a vector with a scalar.

        The scalar parameter must be an integer or float.

        :param scalar: an integer or float
        :return: the product of the vector and scalar
        """

        vector_result = []

        if type(scalar) != int and type(scalar) != float:
            raise Exception("The scalar is not a number.")

        for i in range(len(self.numbers)):
            vector_result.append(self.numbers[i] * scalar)

        return Vector(vector_result)

    def norm(self):
        """
        Calculates and returns the norm of a vector.

        :return: the norm of a vector as an integer or float
        """
        result = 0

        for i in range(len(self.numbers)):
            result += self.numbers[i] ** 2

        return math.sqrt(result)

    def dot_product(self, vector2):
        """
        Calculates and returns the dot product of two vectors.

        The vectors must be of the same size

        :param vector2: a list of numbers
        :return: the dot product of both vectors
        """
        if type(vector2) != Vector:
            raise TypeError("The vector2 variable must be of type Vector")

        if len(vector2.numbers) != len(self.numbers):
            raise ValueError("The vectors need to be the same size.")

        result = 0

        for i in range(len(self.numbers)):
            result += self.numbers[i] * vector2.numbers[i]

        return result

    def angle_between(self, vector2):
        """
        Calculates and returns the angle between two vectors.

        :param vector2: an instance of the vector class
        :return: the dot product of both vectors
        """
        if type(vector2) != Vector:
            raise TypeError("The vector2 variable must be of type Vector")

        if len(vector2.numbers) != len(self.numbers):
            raise ValueError("The vectors need to be the same size.")

        dot = self.dot_product(vector2)

        magnitude = self.norm() * vector2.norm()

        return math.acos(dot / magnitude)

    def cross_product(self, vector2):
        """
        Calculates and returns the cross product of two vectors in R3.

        All vectors must have a length of 3.

        :param vector2: an instance of the vector class
        :return: the cross product of both vectors.
        """
        if type(vector2) != Vector:
            raise TypeError("The vector2 variable must be of type Vector")

        if len(vector2.numbers) != 3 or len(self.numbers) != 3:
            raise ValueError("The vectors need to have a length of 3.")

        return Vector([(self.numbers[1] * vector2.numbers[2]) - (self.numbers[2] * vector2.numbers[1]),
                       (self.numbers[2] * vector2.numbers[0]) - (self.numbers[0] * vector2.numbers[2]),
                       (self.numbers[0] * vector2.numbers[1]) - (self.numbers[1] * vector2.numbers[0])])

    def projection(self, vector2):
        """
        Calculates and returns the projection of vector1 onto vector2.

        All vectors must be lists of integers or floats with the same dimensions.

        :param vector2: a list of numbers
        :return: the projection of vector1 onto vector2
        """

        if len(self.numbers) != len(vector2.numbers):
            raise Exception("The vectors must be of the same length.")

        dot = self.dot_product(vector2)
        magnitude = (vector2.norm()) ** 2

        scalar = dot / magnitude

        return vector2.scalar_multiplication(scalar)

    def unit_vector(self):
        """
        Returns the unit vector equivalent of the vector.
        :return: an instance of the vector class.
        """

        return self.scalar_multiplication(1 / self.norm())

    def parallelepiped_volume(self, vector2, vector3):
        """
        Calculates and returns the volume of a parallelepiped constructed by three vectors.

        All vectors must be lists of integers or floats in R3.

        :param vector2: an instance of the Vector class
        :param vector3: an instance of the Vector class
        :return: the volume of the parallelepiped
        """
        if len(self.numbers) != 3 or len(vector2.numbers) != 3 or len(vector3.numbers) != 3:
            raise Exception("The vectors don't have the correct dimensions")

        return abs(self.dot_product(vector2.cross_product(vector3)))

    def isParallel(self, vector2):
        """
        Returns a boolean value that is dependent on whether the two vectors are parallel or not.

        Both vectors must be lists of floats or integers with the same size.

        :param vector2: an instance of the Vector class that has the same dimensions as this object.
        :return: a boolean value that is dependent on whether the two vectors are parallel or not.
        """
        if type(vector2) != Vector:
            raise TypeError("Vector2 should be an instance of the vector class.")

        if len(self.numbers) != len(vector2.numbers):
            raise ValueError("The length of both vectors should be the same.")

        comparison = self.numbers[0] / vector2.numbers[0]

        for i in range(len(self.numbers)):
            if comparison != self.numbers[i] / vector2.numbers[i]:
                return False

        return True


class ComplexVector:
    """
    This class is used to hold complex vector objects.
    """

    def __init__(self, numbers):
        """
        Initializes the complex vector class.
        :param numbers: a list of complex number objects.
        """

        if type(numbers) != list:
            raise TypeError("Numbers should be a list of the complex numbers in the vector!")

        for num in numbers:
            if type(num) != Complex:
                raise TypeError("The values in the list should be complex objects!")

        self.numbers = numbers

    def addition(self, complex_vector2):
        """
        Returns the sum of two complex vectors.

        :param complex_vector2: a complex vector of the same size as the current instance.
        :return: the complex vector sum of two complex vectors.
        """
        if type(complex_vector2) != ComplexVector:
            raise TypeError("The complexVector2 variable should be a ComplexVector object.")

        if len(complex_vector2.numbers) != len(self.numbers):
            raise ValueError("The length of both complex vectors should be the same.")

        new_list = []

        for i in range(len(complex_vector2.numbers)):
            new_list.append(self.numbers[i].addition(complex_vector2.numbers[i]))

        return ComplexVector(new_list)

    def subtraction(self, complex_vector2):
        """
        Returns the difference of two complex vectors.

        :param complex_vector2: a complex vector of the same size as the current instance.
        :return: the complex vector difference of two complex vectors.
        """
        if type(complex_vector2) != ComplexVector:
            raise TypeError("The complexVector2 variable should be a ComplexVector object.")

        if len(complex_vector2.numbers) != len(self.numbers):
            raise ValueError("The length of both complex vectors should be the same.")

        new_list = []

        for i in range(len(complex_vector2.numbers)):
            new_list.append(self.numbers[i].subtraction(complex_vector2.numbers[i]))

        return ComplexVector(new_list)

    def scalar_multiplication(self, scalar):
        """
        Returns the product between a complex vector and a scalar.

        :param scalar: an integer or float value.
        :return: a new complex vector which is the product between a complex vector and a scalar.
        """

        if type(scalar) != float and type(scalar) != int:
            raise TypeError("The scalar variable should be a float or integer.")

        new_list = []

        for i in range(len(self.numbers)):
            new_list.append(Complex(self.numbers[i].real * scalar, self.numbers[i].imaginary * scalar))

        return ComplexVector(new_list)

    def norm(self):
        """
        Returns the complex vector norm.
        :return: the value of the complex vector norm.
        """
        total = 0

        for num in self.numbers:
            total += num.multiplication(num.conjugate()).real

        return math.sqrt(total)

    def inner_product(self, complex_vector2):
        """
        Returns the complex vector inner product.
        :param complex_vector2: a complex vector of the same size as the current instance.
        :return: a new instance of the complex vector.
        """
        if type(complex_vector2) != ComplexVector:
            raise TypeError("The variable complex_vector2 must be an instance of the ComplexVector class")

        if len(complex_vector2.numbers) != len(self.numbers):
            raise ValueError("The two complex vector must be the same size.")

        total_re = 0
        total_im = 0
        for i in range(len(self.numbers)):
            total_re += self.numbers[i].conjugate().multiplication(complex_vector2.numbers[i]).real
            total_im += self.numbers[i].conjugate().multiplication(complex_vector2.numbers[i]).imaginary

        return Complex(total_re, total_im)


def matrix_addition(matrix1, matrix2):
    """
    Calculates and returns the sum of two matrices.

    All matrices must be nested lists of integers or floats with each row being the same size.

    :param matrix1: a nested list of numbers
    :param matrix2: a nested list of numbers
    :return: the sum as a nested list of numbers
    """
    if len(matrix1) != len(matrix2):
        raise Exception("The two matrices aren't of the same dimensions.")

    for row in range(len(matrix1)):
        if len(matrix1[row]) != len(matrix2[row]):
            raise Exception("The two matrices aren't of the same dimensions.")

        for item in range(len(matrix1[row])):
            if (type(matrix1[row][item]) != int and type(matrix1[row][item]) != float) or (
                    type(matrix2[row][item]) != int and type(matrix2[row][item]) != float):
                raise Exception("The matrix contains a value not of the correct type.")

            matrix1[row][item] += matrix2[row][item]

    return matrix1


def matrix_scalar_multiplication(matrix1, scalar):
    """
    Calculates and returns the product of a matrix and a scalar.

    All matrices must be nested lists of integers or floats with each row being the same size.

    :param matrix1: a nested list of numbers
    :param scalar: an integer or float
    :return: the product of a matrix and a scalar
    """
    length = len(matrix1[0])

    for row in range(len(matrix1)):
        if len(matrix1[row]) != length:
            raise Exception("The matrix rows aren't of the same dimensions.")

        for item in range(len(matrix1[row])):
            if type(matrix1[row][item]) != int and type(matrix1[row][item]) != float:
                raise Exception("The matrix contains a value not of the correct type.")

            matrix1[row][item] *= scalar

    return matrix1


def matrix_transpose(matrix1):
    """
    Calculates and returns the transpose of a matrix.

    All matrices must be nested lists of integers or floats with each row being the same size.

    :param matrix1: a nested list of numbers
    :return: the transpose of a matrix
    """

    new_matrix = [[0 for _ in range(len(matrix1))] for _ in range(len(matrix1[0]))]

    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            if type(matrix1[i][j]) != int and type(matrix1[i][j]) != float:
                raise Exception("The matrix contains a value not of the correct type.")

            new_matrix[j][i] = matrix1[i][j]

    return new_matrix


def matrix_multiplication(matrix1, matrix2):
    """
    Calculates and returns the product of two matrices.

    All matrices must be nested lists of integers or floats, with each row being the same size.

    :param matrix1: a nested list of numbers
    :param matrix2: a nested list of numbers that contains as many lists as there are values per row in matrix1
    :return: the product of both matrices
    """

    if len(matrix1[0]) != len(matrix2):
        raise Exception("The number of values in each row of the first matrix should equal the number of values in a "
                        "column for the second matrix")

    new_matrix = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]

    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                new_matrix[i][j] += matrix1[i][k] * matrix2[k][j]

    return new_matrix


def matrix_determinant(matrix1, total=0):
    """
    Returns the determinant of a matrix

    All matrices must be nested lists of integers or floats, the matrix must be a square matrix.

    :param matrix1: a nested list of numbers
    :param total: totals all the returns from the recursion
    :return: the matrix's determinant

    Credits: Thom Ives https://github.com/ThomIves/BasicLinearAlgebraToolsPurePy/blob/master/LinearAlgebraPurePython.py
    """
    indices = list(range(len(matrix1)))

    if len(matrix1) == 2 and len(matrix1[0]) == 2:
        det = (matrix1[0][0] * matrix1[1][1]) - (matrix1[1][0] * matrix1[0][1])
        return det

    for column in indices:
        submatrix = [ele[:] for ele in matrix1]
        submatrix = submatrix[1:]

        h = len(submatrix)

        for i in range(h):
            submatrix[i] = submatrix[i][0:column] + submatrix[i][column + 1:]

        sign = (-1) ** (column % 2)

        sub_det = matrix_determinant(submatrix)

        total += sign * matrix1[0][column] * sub_det

    return total

# Potentially add system of equations - test consistency with rank - RREF - matrix inverse
