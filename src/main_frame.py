import sys

import matplotlib
import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QApplication, \
    QStyleFactory, QTextEdit, QWidget, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mandelbrot_calc import MandelbrotCalculation

matplotlib.use('Qt5Agg')


class FractalCanvas(FigureCanvasQTAgg):
    """
    Class created for easy display of fractals
    """

    def __init__(self, width=30, height=20, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)

    def plot_mandelbrot_col(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111, position=[0.05, 0.05, 0.9, 0.9])

        mandel = MandelbrotCalculation()
        mandel.compute_mandelbrot_col()

        ax.scatter(mandel.x_array, mandel.y_array, 0.2 , mandel.c_array)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        self.draw()

    def plot_mandelbrot_bw(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111, position=[0.05, 0.05, 0.9, 0.9])

        mandel = MandelbrotCalculation(0.001, 30)
        mandel.compute_mandelbrot_bw()
        ax.scatter(mandel.x_array, mandel.y_array, 0.05 , (0,0,0))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        self.draw()

    def plot_logistical(self, x_array, y_array):
        self.figure.clear()
        ax = self.figure.add_subplot(111, position=[0.05, 0.05, 0.9, 0.9])
        ax.plot(x_array, y_array)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        # stolen code just for tests
        ax.scatter([.5], [.5], c='#0000FF', s=96000, label="face")
        ax.scatter([.35, .65], [.63, .63], c='k', s=1000, label="eyes")

        X = np.linspace(.3, .7, 100)
        Y = -2 * (X - .5) ** 2 + 0.45

        ax.plot(X, Y, c='k', linewidth=8, label="smile")

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        self.draw()


class MainFrame(QMainWindow):
    def __init__(self):
        super(MainFrame, self).__init__()
        self.setWindowIcon(QtGui.QIcon('img/lpf_icon.ico'))

        self.bold10 = QFont("Aptos", 10)
        self.bold10.setBold(True)

        self.terminal = QTextEdit()
        self.mandelbrot_canvas = FractalCanvas()
        self.bifurcation_canvas = FractalCanvas()

        self.plot_frame = QFrame()
        self.controls_frame = QFrame()

        #self.my_line_edit.setStyleSheet("color: red;")
        #self.my_line_edit.setStyleSheet("color: rgb(255, 0, 0);")
        #self.my_line_edit.setStyleSheet("""QLabel {color: red;}""")


        self.init_ui()

    def init_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        doc_menu = menu_bar.addMenu("&Documentation")

    def init_dark(self):
        self.setStyleSheet("background-color: #37006a;")

        #for label in self.findChildren(QLabel, options=Qt.FindDirectChildrenOnly):
         #   label.setStyleSheet("color: black;")

        #self.plot_frame.setStyleSheet(
        #    """QFrame { background-color: green; color: white }""")

    def init_plot_frame(self):
        self.plot_frame.setFrameShape(QFrame.StyledPanel)

        plot_frame_layout = QHBoxLayout(self.plot_frame)

        mandelbrot_sublayout = QVBoxLayout()

        mandelbrot_label = QLabel("Mandelbrot set:", self.plot_frame)
        mandelbrot_label.setFont(self.bold10)
        mandelbrot_sublayout.addWidget(mandelbrot_label)

        mandelbrot_sublayout.addWidget(self.mandelbrot_canvas, 70)
        mandelbrot_toolbar = NavigationToolbar(self.mandelbrot_canvas, self)
        mandelbrot_sublayout.addWidget(mandelbrot_toolbar, 4)

        bifurcation_sublayout = QVBoxLayout()

        bifurcation_label = QLabel("Logistical projection:", self.plot_frame)
        bifurcation_label.setFont(self.bold10)
        bifurcation_sublayout.addWidget(bifurcation_label)

        bifurcation_sublayout.addWidget(self.bifurcation_canvas, 70)
        bifurcation_toolbar = NavigationToolbar(self.bifurcation_canvas, self)
        bifurcation_sublayout.addWidget(bifurcation_toolbar, 4)

        plot_frame_layout.addLayout(mandelbrot_sublayout)
        plot_frame_layout.addLayout(bifurcation_sublayout)

        #just for shits and giggles
        arr=np.zeros(10)

        self.bifurcation_canvas.plot_logistical(arr,arr)
        self.mandelbrot_canvas.plot_mandelbrot_col()

        self.plot_frame.setLayout(plot_frame_layout)

    def init_controls_frame(self):
        self.controls_frame.setFrameShape(QFrame.StyledPanel)

        controls_layout = QVBoxLayout(self.controls_frame)

        control_label = QLabel('Controls:', self.controls_frame)
        control_label.setStyleSheet("padding :2px")
        control_label.setFont(self.bold10)
        controls_layout.addWidget(control_label, 1)

        controls_sublayout = QHBoxLayout(self.controls_frame)
        controls_layout.addLayout(controls_sublayout)

        tfield_label_layout = QVBoxLayout(self.controls_frame)
        controls_sublayout.addLayout(tfield_label_layout)

        precision_label = QLabel('Precision:', self.controls_frame)
        tfield_label_layout.addWidget(precision_label)

        precision_tfield = QtWidgets.QLineEdit(self)
        precision_tfield.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        tfield_label_layout.addWidget(precision_tfield)

        param1_label = QLabel('Param1:', self.controls_frame)
        tfield_label_layout.addWidget(param1_label)

        param1_tfield = QtWidgets.QLineEdit(self)
        param1_tfield.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        tfield_label_layout.addWidget(param1_tfield)

        param2_label = QLabel('Param2:', self.controls_frame)
        tfield_label_layout.addWidget(param2_label)

        param2_tfield = QtWidgets.QLineEdit(self)
        param2_tfield.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        tfield_label_layout.addWidget(param2_tfield)

        self.terminal.setStyleSheet("padding :5px")
        controls_sublayout.addWidget(self.terminal)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.init_menu()
        self.init_plot_frame()
        self.init_controls_frame()

        vbox = QVBoxLayout(central_widget)
        vbox.addWidget(self.plot_frame)
        vbox.addWidget(self.controls_frame)

        QApplication.setStyle(QStyleFactory.create(''))
        self.setGeometry(0, 0, 1200, 800)
        self.setWindowTitle('Fractals in logistic projection')

        #self.init_dark()

    # def look_for_enter_key(self):
    #    if self.term_edit.toPlainText().endswith('\n'):
    #       self.term_handler.get_command(self.term_edit, self.term_edit.toPlainText())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainFrame()
    main_window.show()
    sys.exit(app.exec_())
