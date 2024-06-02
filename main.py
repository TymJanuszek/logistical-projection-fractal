import os
import sys
from datetime import datetime

import matplotlib
import numpy as np
from IPython.core.inputtransformer import tr
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QFile, QTextStream, QEvent, QObject, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QApplication, \
    QStyleFactory, QTextEdit, QWidget, QLineEdit, QFileDialog, QPushButton, QSplitter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mandelbrot_calc import MandelbrotCalculation, BifurcationCalculation
import console_handler as chand
from PyQt5.QtCore import Qt
import threading as thread
matplotlib.use('Qt5Agg')


class FractalCanvas(FigureCanvasQTAgg):
    """
    Class created for easy display of fractals
    """

    def __init__(self, width=30, height=20, dpi=100):
        self.mandel = None
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)

    def plot_mandelbrot_col(self, step=0.05, precision=20):
        self.figure.clear()
        ax = self.figure.add_subplot(111, position=[0.05, 0.05, 0.9, 0.9])

        self.mandel = MandelbrotCalculation(step, precision)
        self.mandel.compute_mandelbrot_col()

        ax.scatter(self.mandel.x_array, self.mandel.y_array, 0.2, self.mandel.c_array)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        self.draw()

    def plot_mandelbrot_bw(self, step=0.00001, precision=100):
        self.figure.clear()
        ax = self.figure.add_subplot(111, position=[0.05, 0.05, 0.9, 0.9])

        self.mandel = MandelbrotCalculation(step, precision)
        self.mandel.compute_mandelbrot_bw()
        ax.scatter(self.mandel.x_array, self.mandel.y_array, 0.05, color='b')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        self.draw()

    def plot_logistical(self, step=0.00001, precision=100):
        self.figure.clear()
        ax = self.figure.add_subplot(111, position=[0.05, 0.05, 0.9, 0.9])

        logi = BifurcationCalculation(step, precision)
        logi.compute_bifurcation()
        ax.scatter(logi.r_array, logi.x_array, 0.05, 'b')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        self.draw()

    def plot_bifurcation_from_point(self, real, imag, step=0.00001, precision=100):
        self.figure.clear()
        ax = self.figure.add_subplot(111, position=[0.05, 0.05, 0.9, 0.9])

        logi = BifurcationCalculation(step, precision)
        logi.compute_bifurcation_from_point(real, imag)
        ax.scatter(logi.r_array, logi.x_array, 0.05, 'b')

        ax.set_xlim(-2, 0.5)
        ax.set_ylim(-0.6, 0.4)

        ax.grid(True)

        ax.set_xlabel('r')
        ax.set_ylabel('x')

        self.draw()

    def clear_plot(self):
        self.figure.clear()
        self.draw()


class KeyListener(QObject):
    def __init__(self, mandelbrot_canvas, logistic_canvas):
        super().__init__()
        self.mandelbrot_canvas = mandelbrot_canvas
        self.logistic_canvas = logistic_canvas
        self.mandelbrot_canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if event.inaxes is not None and event.canvas == self.mandelbrot_canvas:
            x, y = event.xdata, event.ydata
            print(f"Clicked coordinates: x={x}, y={y}")
            self.logistic_canvas.plot_bifurcation_from_point(x, y)



class FVThread(QObject):
    finished = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, func, *args):
        super(FVThread, self).__init__()
        self.func = func
        self.args = args

    @pyqtSlot()
    def run(self):
        self.progress.emit("Regenerating plot. This may take a while...")
        self.func(*self.args)
        self.finished.emit("Plot regeneration completed!")

class MainFrame(QMainWindow):
    def __init__(self):
        super(MainFrame, self).__init__()
        self.key_listener = None
        self.console = QTextEdit()
        self.setWindowIcon(QtGui.QIcon('img/lpf_icon.ico'))

        self.bold10 = QFont("Aptos", 10)
        self.bold10.setBold(True)

        self.mandelbrot_canvas = FractalCanvas()
        self.bifurcation_canvas = FractalCanvas()

        self.plot_frame = QFrame()
        self.controls_frame = QFrame()

        self.console_handler = chand.Console_handler(self)


        self.init_ui()

    def init_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        self.saveall = file_menu.addAction("&Save All", )
        self.saveall.triggered.connect(self.save_all)
        self.savesession = file_menu.addAction("&Save Session")
        self.settings = file_menu.addAction("&Settings")
        self.quit = file_menu.addAction("&Quit")
        view = menu_bar.addMenu("&View")
        self.setStyleType = view.addMenu("&Choose Theme")
        self.DarkMode = self.setStyleType.addAction("&Dark Theme")
        self.DarkMode.triggered.connect(lambda: self.load_qt_stylesheet("dark_stylesheet.css"))
        self.LightMode = self.setStyleType.addAction("&Light Theme")
        self.LightMode.triggered.connect(lambda: self.load_qt_stylesheet( "light_stylesheet.css"))
        self.Classic = self.setStyleType.addAction("&Classic Theme")
        self.Classic.triggered.connect(lambda: self.load_qt_stylesheet("classic_stylesheet.css"))
        self.LoadTheme = self.setStyleType.addAction("&Load External Theme file")
        self.LoadTheme.triggered.connect(lambda: self.load_external_qt_stylesheet())
        doc_menu = menu_bar.addMenu("&About")
        self.documentation = doc_menu.addAction("&Documentation")
        self.manual = doc_menu.addAction("&User Manual")
        self.contact = doc_menu.addAction("&Help and contact info")

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
        self.key_listener = KeyListener(self.mandelbrot_canvas, self.bifurcation_canvas)
        #just for shits and giggles
        arr=np.zeros(10)
        self.t1 = thread.Thread(self.bifurcation_canvas.plot_logistical())
        self.t2 = thread.Thread(self.mandelbrot_canvas.plot_mandelbrot_col())
        self.t1.start()
        self.t2.start()
        self.plot_frame.setLayout(plot_frame_layout)

    def init_controls_frame(self):
        self.controls_frame.setFrameShape(QFrame.StyledPanel)
        controls_layout = QHBoxLayout(self.controls_frame)

        control_layout = QVBoxLayout()
        console_layout = QVBoxLayout()

        mandelbrot_ctrl_layout = QVBoxLayout()
        logistical_ctrl_layout = QVBoxLayout()

        mandel_logi_layout = QHBoxLayout()

        control_label = QLabel("Controls")
        console_label = QLabel("Console: ")

        font = control_label.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 2)
        control_label.setFont(font)
        console_label.setFont(font)

        mandelbrot_label = QLabel("Plot options for Mandelbrot: ")
        logistical_label = QLabel("Plot options for Logistical: ")

        precision_mandel_label = QLabel('Precision :')
        self.mandel_precision_tfield = QtWidgets.QLineEdit(self)
        self.mandel_precision_tfield.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        step_mandel_label = QLabel('Step count: ')
        self.mandel_step_tfield = QtWidgets.QLineEdit(self)
        self.mandel_step_tfield.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        precision_logi_label = QLabel('Precision :')
        self.logi_precision_tfield = QtWidgets.QLineEdit(self)
        self.logi_precision_tfield.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        step_logi_label = QLabel('Step count: ')
        self.logi_step_tfield = QtWidgets.QLineEdit(self)
        self.logi_step_tfield.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        split_line = QFrame()
        split_line.setFrameShape(QFrame.VLine)
        split_line.setFrameShadow(QFrame.Sunken)

        mandelbrot_ctrl_layout.addWidget(mandelbrot_label)
        mandelbrot_ctrl_layout.addWidget(precision_mandel_label)
        mandelbrot_ctrl_layout.addWidget(self.mandel_precision_tfield)
        mandelbrot_ctrl_layout.addWidget(step_mandel_label)
        mandelbrot_ctrl_layout.addWidget(self.mandel_step_tfield)
        self.mandel_regen = QPushButton("Regenerate Mandelbrot plot")
        self.mandel_regen.pressed.connect(self.regenerate_mandel_plot)
        mandelbrot_ctrl_layout.addWidget(self.mandel_regen)

        logistical_ctrl_layout.addWidget(logistical_label)
        logistical_ctrl_layout.addWidget(precision_logi_label)
        logistical_ctrl_layout.addWidget(self.logi_precision_tfield)
        logistical_ctrl_layout.addWidget(step_logi_label)
        logistical_ctrl_layout.addWidget(self.logi_step_tfield)
        self.logi_regen = QPushButton("Regenerate Logistical plot")
        self.logi_regen.pressed.connect(self.regenerate_logistical_plot)
        logistical_ctrl_layout.addWidget(self.logi_regen)

        mandel_logi_layout.addLayout(mandelbrot_ctrl_layout)
        mandel_logi_layout.addWidget(split_line)
        mandel_logi_layout.addLayout(logistical_ctrl_layout)

        control_layout.addWidget(control_label, 10)
        control_layout.addLayout(mandel_logi_layout, 90)

        self.console.setStyleSheet("padding: 5px")
        console_layout.addWidget(console_label)
        console_layout.addWidget(self.console)
        self.console.installEventFilter(self)

        controls_layout.addLayout(control_layout)
        controls_layout.addLayout(console_layout)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.init_menu()
        self.init_plot_frame()
        self.init_controls_frame()

        splitter = QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.plot_frame)
        splitter.addWidget(self.controls_frame)
        splitter.setSizes([700, 300])

        layout = QVBoxLayout(central_widget)
        layout.addWidget(splitter)
        central_widget.setLayout(layout)

        QApplication.setStyle(QStyleFactory.create(''))
        self.setGeometry(0, 0, 1200, 800)
        self.setWindowTitle('Fractal Visualizer')


    def load_qt_stylesheet(self, stylesheet):
        with open(stylesheet, 'r', encoding='utf-8') as file:
            str = file.read()
        self.setStyleSheet(str)

    def check_text_is_number_float(self, line_edit):
        text = line_edit.text()
        if text:
            try:
                float(text)
                return True
            except ValueError:
                self.console.setText("ERROR: Incorrect value type (The number should be of floating point type). \n")
                return False
        return False

    def check_text_is_number_int(self, line_edit):
        text = line_edit.text()
        if text:
            try:
                int(text)
                return True
            except ValueError:
                self.console.setText("ERROR: Incorrect value type. (The number should be of integer type). \n")
                return False
        return False


    def regenerate_mandel_plot(self):
        if self.check_text_is_number_int(self.mandel_precision_tfield):
            precision = int(self.mandel_precision_tfield.text())
        if self.check_text_is_number_float(self.mandel_step_tfield):
            step=float(self.mandel_step_tfield.text())
        self.t1 = thread.Thread(target=self.mandelbrot_canvas.plot_mandelbrot_col,args=(step, precision))
        self.t1.start()
        self.console.append("Regenerating plot. This may take a while...")
        if self.t1.is_alive():
            self.console.append("Mandelbrot set plot regeneration completed!")

    def regenerate_logistical_plot(self):
        if self.check_text_is_number_int(self.logi_precision_tfield):
            precision = int(self.logi_precision_tfield.text())
        if self.check_text_is_number_float(self.logi_precision_tfield):
            step = float(self.logi_step_tfield.text())
        self.t1 = thread.Thread(target=self.bifurcation_canvas.plot_logistical, args=(step, precision))
        self.t1.start()
        self.console.append("Regenerating plot. This may take a while...")
        if self.t1.is_alive():
            self.console.append("Logistical plot regeneration completed!")

    def load_external_qt_stylesheet(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter(tr("StyleSheets (*.qss *.css)"))
        stylesheet = dialog.getOpenFileName()
        self.load_qt_StyleSheet(stylesheet)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and event.key() == QtCore.Qt.Key_Return and source is self.console:
            text_line = self.console.toPlainText()
            self.console_handler.get_console_input(text_line)
            return True
        return super(MainFrame, self).eventFilter(source, event)

    def regenerate_mandel_plot(self):
        if self.check_text_is_number_int(self.mandel_precision_tfield):
            precision = int(self.mandel_precision_tfield.text())
        if self.check_text_is_number_float(self.mandel_step_tfield):
            step = float(self.mandel_step_tfield.text())
        if precision / step <= 250000:
            self.console.append("Starting Mandelbrot plot regeneration...")
            self.run_thread(self.mandelbrot_canvas.plot_mandelbrot_col, step, precision)
        else:
            self.console.append(f"Your pc probably wont handle performing {int(precision/step)} complex calculations. The "
                                f"limit is 250000")
            self.console.append("Reduce precision value or increase step value and try again.")

    def regenerate_logistical_plot(self):
        if self.check_text_is_number_int(self.logi_precision_tfield):
            precision = int(self.logi_precision_tfield.text())
        if self.check_text_is_number_float(self.logi_step_tfield):
            step = float(self.logi_step_tfield.text())
        if precision/step <=10000000:
            self.console.append("Starting Logistical plot regeneration...")
            self.run_thread(self.bifurcation_canvas.plot_logistical, step, precision)
        else:
            self.console.append(f"Your pc probably wont handle performing {int(precision/step)} complex calculations. The "
                                f"limit is 10000000")
            self.console.append("Reduce precision value or increase step value and try again.")

    def run_thread(self, func, *args):
        self.thread = QThread()
        self.fv_thread = FVThread(func, *args)
        self.fv_thread.moveToThread(self.thread)

        self.thread.started.connect(self.fv_thread.run)
        self.fv_thread.finished.connect(self.on_thread_finished)
        self.fv_thread.progress.connect(self.on_thread_progress)
        self.fv_thread.finished.connect(self.thread.quit)
        self.fv_thread.finished.connect(self.fv_thread.deleteLater)
        self.fv_thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_thread_finished(self, message):
        self.console.append(message)

    def on_thread_progress(self, message):
        self.console.append(message)

    def save_all(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            mandelbrot_filename = os.path.join(file,f"mandelbrot_{timestamp}.png")
            logistical_filename = os.path.join(file, f"logistical_{timestamp}.png")
            self.mandelbrot_canvas.figure.savefig(mandelbrot_filename)
            self.bifurcation_canvas.figure.savefig(logistical_filename)
            self.console.append(f"Mandelbrot plot saved to {mandelbrot_filename}")
            self.console.append(f"Logistical plot saved to {logistical_filename}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainFrame()
    main_window.show()
    sys.exit(app.exec_())
