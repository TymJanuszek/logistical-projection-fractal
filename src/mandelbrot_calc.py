import time

import matplotlib.pyplot as plt
import numpy as np

class MandelbrotCalculation:

    def __init__(self, step=0.005, precision=20):
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

    def psych_grad(self, count):
        if count == self.precision:
            return (0, 0, 0)
        elif count == self.precision - 1:
            return (1, 1, 1)
        else:
            return (count / self.precision, 0.5 + count / 2 / self.precision, 0.25 + 0.75 * count / self.precision)

    def compute_mandelbrot_col(self):
        re_array = np.linspace(self.restart-0.1, self.restop+0.1, int((self.restop - self.restart) / self.step + 1))
        im_array = np.linspace(self.imstart-0.1, self.imstop+0.1, int((self.imstop - self.imstart) / self.step + 1))



        for re in re_array:
            for im in im_array:
                z = 0
                c = complex(re, im)
                count = 0
                while count < self.precision and abs(z) < 2:
                    z = z * z + c
                    count += 1

                self.x_array.append(re)
                self.y_array.append(im)
                self.c_array.append(self.psych_grad(count))
        #plt.scatter(x_array, y_array, self.step*50, c_array)

    def compute_mandelbrot_bw(self):
        re_array = np.linspace(self.restart, self.restop, int((self.restop - self.restart) / self.step + 1))
        im_array = np.linspace(self.imstart, self.imstop, int((self.imstop - self.imstart) / self.step + 1))

        for re in re_array:
            for im in im_array:
                z = 0
                c = complex(re, im)
                count = 0
                while count < self.precision and abs(z) < 2:
                    z = z * z + c
                    count += 1
                if abs(z) < 2:
                    self.x_array.append(re)
                    self.y_array.append(im)
        #plt.scatter(x_array, y_array, self.step*50, (0, 0, 0))


#start_time = time.time()
# compute_mandelbrot_bw(sta, sto, ste, prc)

#mandelbrot = MandelbrotCalculation()
#mandelbrot.compute_mandelbrot_col()

#print("runtime %s" % (time.time() - start_time))

#plt.show()

