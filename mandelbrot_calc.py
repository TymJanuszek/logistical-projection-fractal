import time
from random import Random

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


class MandelbrotCalculation:

    def __init__(self, step, precision):
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
        return (1 - 1 / self.precision * count), (1 - 1 / self.precision * count), (1 - 1 / self.precision * count / 2)

    def set_precision(self, precision):
        self.precision = precision

    def set_step_count(self, step):
        self.step = step

    def psych_grad(self, count):
        if count == self.precision:
            return (0, 0, 0)
        elif count == self.precision - 1:
            return (1, 1, 1)
        else:
            return (count / self.precision, 0.5 + count / 2 / self.precision, 0.25 + 0.75 * count / self.precision)

    def compute_mandelbrot_col(self):
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
    def __init__(self, step, precision):
        self.precision = precision
        self.step = step
        self.restart = -2.0
        self.restop = 0.5

        self.x_array = []
        self.r_array = []

    def compute_bifurcation(self):
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

    def set_precision(self, precision):
        self.precision = precision

    def set_step_count(self, step):
        self.step = step

# Start plotting using FractalCanvas or another method
# For example:
# mandelbrot = MandelbrotCalculation(0.005, 1000)
# mandelbrot.compute_mandelbrot_col()
# plt.scatter(mandelbrot.x_array, mandelbrot.y_array, c=mandelbrot.c_array, s=0.1)
# plt.show()
