import sys

import matplotlib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QApplication, \
    QStyleFactory, QTextEdit, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class FractalCanvas(FigureCanvasQTAgg):
    """
    Class created for easy display of fractals
    """

    def __init__(self, width=30, height=20, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)

    def plot_mandelbrot(self, x_array, y_array):
        self.figure.clear()
        ax = self.figure.add_subplot(111, position=[0.05, 0.05, 0.9, 0.9])
        ax.plot(x_array, y_array)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        self.draw()


class MainFrame(QMainWindow):
    def __init__(self):
        super(MainFrame, self).__init__()
        # self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.terminal = QTextEdit()
        self.main_plot_canvas = FractalCanvas()

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        hbox = QHBoxLayout(central_widget)

        controls_frame = QFrame()
        controls_frame.setFrameShape(QFrame.StyledPanel)

        control_label = QLabel('Controls:', controls_frame)
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.addWidget(control_label, 1)

        button = QPushButton("Hello")
        controls_layout.addWidget(button)
        button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        plotting_frame = QFrame()
        plotting_frame.setFrameShape(QFrame.StyledPanel)

        plot_panel_label = QLabel('Plot Panel:', plotting_frame)
        plot_frame_layout = QVBoxLayout(plotting_frame)

        plot_frame_layout.addWidget(plot_panel_label, 1)

        plot_sublayout = QHBoxLayout()
        plot_frame_layout.addLayout(plot_sublayout)
        plot_sublayout.addWidget(self.main_plot_canvas, 70)
        plotting_frame.setLayout(plot_frame_layout)

        hbox.addWidget(controls_frame)
        hbox.addWidget(plotting_frame)

        QApplication.setStyle(QStyleFactory.create(''))
        self.setGeometry(0, 0, 1200, 800)
        self.setWindowTitle('Fractals in logistic projection')

    # def look_for_enter_key(self):
    #    if self.term_edit.toPlainText().endswith('\n'):
    #       self.term_handler.get_command(self.term_edit, self.term_edit.toPlainText())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainFrame()
    main_window.show()
    sys.exit(app.exec_())
