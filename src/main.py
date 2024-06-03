import sys
import main_frame as mf
import matplotlib
from PyQt5.QtWidgets import QApplication


matplotlib.use('Qt5Agg')

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = mf.MainFrame()
    main_window.show()
    sys.exit(app.exec_())