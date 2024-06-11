import time
from random import Random

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

class MandelbrotCalculation:
    """
    A class for performing Mandelbrot set calculations with different coloring schemes.

    Attributes:
        precision (int): The maximum number of iterations for the Mandelbrot calculation.
        step (float): The step size for the calculation grid.
        imstart (float): The starting value for the imaginary part of the complex grid.
        imstop (float): The stopping value for the imaginary part of the complex grid.
        restart (float): The starting value for the real part of the complex grid.
        restop (float): The stopping value for the real part of the complex grid.
        x_array (list): List to store x-coordinates of the calculated points.
        y_array (list): List to store y-coordinates of the calculated points.
        c_array (list): List to store color values of the calculated points.
    """

    def __init__(self, step, precision):
        """
        Initialize the MandelbrotCalculation class with the specified step size and precision.

        Args:
            step (float): The step size for the calculation grid.
            precision (int): The maximum number of iterations for the Mandelbrot calculation.
        """
        self.precision = precision
        self.step = step
        self.imstart = -1
        self.imstop = 1
        self.restart = -2
        self.restop = 0.5

        self.x_array = []
        self.y_array = []
        self.c_array = []

    def blue_grad(self, count):
        """
        Generate a blue gradient color based on the iteration count.

        Args:
            count (int): The iteration count.

        Returns:
            tuple: A tuple representing the RGB color.
        """
        return (1 - 1 / self.precision * count), (1 - 1 / self.precision * count), (1 - 1 / self.precision * count / 2)

    def set_precision(self, precision):
        """
        Set the precision (maximum number of iterations) for the calculation.

        Args:
            precision (int): The maximum number of iterations.
        """
        self.precision = precision

    def set_step_count(self, step):
        """
        Set the step size for the calculation grid.

        Args:
            step (float): The step size for the calculation grid.
        """
        self.step = step

    def psych_grad(self, count):
        """
        Generate a psychedelic gradient color based on the iteration count.

        Args:
            count (int): The iteration count.

        Returns:
            tuple: A tuple representing the RGB color.
        """
        if count == self.precision:
            return (1, 1, 1)
        elif count == self.precision - 1:
            return (0, 0, 0)
        else:
            return (count / self.precision, 0.5 + count / 2 / self.precision, 0.25 + 0.75 * count / self.precision)

    def compute_mandelbrot_col(self):
        """
        Compute the Mandelbrot set with coloring based on iteration count and update the arrays.
        """
        re_array = np.linspace(self.restart - 0.1, self.restop + 0.1, int((self.restop - self.restart) / self.step + 1))
        im_array = np.linspace(self.imstart - 0.1, self.imstop + 0.1, int((self.imstop - self.imstart) / self.step + 1))

        re_array, im_array = np.meshgrid(re_array, im_array)
        c = re_array + 1j * im_array
        z = tf.zeros_like(c, dtype=tf.complex64)
        m = tf.fill(c.shape, self.precision)

        for i in range(self.precision):
            mask = tf.abs(z) < 2
            z = tf.where(mask, z * z + c, z)
            m = tf.where(mask, tf.fill(m.shape, i), m)

        x_array = re_array[m.numpy() < self.precision]
        y_array = im_array[m.numpy() < self.precision]
        c_array = [self.psych_grad(count) for count in m.numpy()[m.numpy() < self.precision]]

        self.x_array.extend(x_array.flatten())
        self.y_array.extend(y_array.flatten())
        self.c_array.extend(c_array)

    def compute_mandelbrot_bw(self):
        """
        Compute the Mandelbrot set in black and white and update the arrays.
        """
        re_array = np.linspace(self.restart, self.restop, int((self.restop - self.restart) / self.step + 1))
        im_array = np.linspace(self.imstart, self.imstop, int((self.imstop - self.imstart) / self.step + 1))

        re_array, im_array = np.meshgrid(re_array, im_array)
        c = re_array + 1j * im_array
        z = tf.zeros_like(c, dtype=tf.complex64)
        m = tf.fill(c.shape, self.precision)

        for i in range(self.precision):
            mask = tf.abs(z) < 2
            z = tf.where(mask, z * z + c, z)
            m = tf.where(mask, tf.fill(m.shape, i), m)

        x_array = re_array[m.numpy() < self.precision]
        y_array = im_array[m.numpy() < self.precision]

        self.x_array.extend(x_array.flatten())
        self.y_array.extend(y_array.flatten())


class BifurcationCalculation:
    """
    A class for performing bifurcation calculations for logistic maps.

    Attributes:
        precision (int): The number of iterations for each calculation.
        step (float): The step size for the calculation grid.
        restart (float): The starting value for the parameter r.
        restop (float): The stopping value for the parameter r.
        x_array (list): List to store x-coordinates of the calculated points.
        r_array (list): List to store r values used in the calculation.
    """

    def __init__(self, step, precision):
        """
        Initialize the BifurcationCalculation class with the specified step size and precision.

        Args:
            step (float): The step size for the calculation grid.
            precision (int): The number of iterations for each calculation.
        """
        self.precision = precision
        self.step = step
        self.restart = -2.0
        self.restop = 0.5

        self.x_array = []
        self.r_array = []

    def compute_bifurcation(self):
        """
        Compute the bifurcation diagram for the logistic map and update the arrays.
        """
        self.r_array = np.linspace(self.restart, self.restop, int((self.restop - self.restart) / self.step + 1))

        for r in self.r_array:
            count = 0
            x = np.float64(0.2)
            switcheroo = Random()
            s = switcheroo.randint(0, 10)

            while count < self.precision + s:
                x = r * x * (1 - x)
                count += 1
            self.x_array.append(x)

        plt.xlim(-2, -0.5)

    def compute_bifurcation_x(self, x):
        """
        Compute the bifurcation diagram for the logistic map starting from a specific x value and update the arrays.

        Args:
            x (float): The initial x value for the logistic map.
        """
        self.r_array = np.linspace(self.restart, self.restop, int((self.restop - self.restart) / self.step + 1))

        for r in self.r_array:
            count = 0
            switcheroo = Random()
            s = switcheroo.randint(0, 10)

            while count < self.precision + s:
                x = r * x * (1 - x)
                count += 1
            self.x_array.append(x)

        plt.xlim(-2, -0.5)

    def compute_bifurcation_from_point(self, real, imag):
        """
        Compute the bifurcation diagram for the logistic map starting from a complex point and update the arrays.

        Args:
            real (float): The real part of the initial complex value.
            imag (float): The imaginary part of the initial complex value.
        """
        self.r_array = np.linspace(self.restart, self.restop, int((self.restop - self.restart) / self.step + 1))
        c = complex(real, imag)

        for r in self.r_array:
            count = 0
            x = np.float64(0.2)
            switcheroo = Random()
            s = switcheroo.randint(0, 10)

            while count < self.precision + s:
                x = r * x * (1 - x)
                count += 1
            self.x_array.append(np.abs(c) * x * (1 - x))

        plt.xlim(-2, -0.5)

    def set_precision(self, precision):
        """
        Set the precision (number of iterations) for the bifurcation calculation.

        Args:
            precision (int): The number of iterations for each calculation.
        """
        self.precision = precision

    def set_step_count(self, step):
        """
        Set the step size for the calculation grid.

        Args:
            step (float): The step size for the calculation grid.
        """
        self.step = step
