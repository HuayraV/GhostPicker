import sys
from Ui_MainMenu import MainWindow
from PyQt5.QtWidgets import QApplication
from Db_logic import Database
from settings import STYLE


if __name__ == '__main__':
    db = Database()
    db.ghosts_data_loader()
    db.typeInfo_data_loader()

    app = QApplication(sys.argv)
    main = MainWindow()
    main.setStyleSheet(STYLE)
    main.setupUi()
    main.show()
    sys.exit(app.exec_())
