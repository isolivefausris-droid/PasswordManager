from PyQt6 import QtCore,QtGui,QtWidgets
from PyQt6.QtCore import Qt, QSize
from classes.AuthManager import AuthManager
from classes.PasswordManager import PasswordManager
from windows.Ui_MainWindow import Ui_MainWindow
from windows.Ui_AddPassword import Ui_Dialog
import sys
class AddPasswordDialog(QtWidgets.QDialog):
    def __init__(self, password_manager,parent = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(QSize(470,350))
        self.pm = password_manager 

        self.ui.GeneratePassword.clicked.connect(self._on_generate)
        self.ui.OkButton.clicked.connect(self._on_ok_clicked)
        self.ui.CancelButton.clicked.connect(self.reject)
    def _on_generate(self):
        self.ui.PasswordLine.setText(self.pm.pass_gen())
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.ui.PasswordLine.text().strip())
    def _on_ok_clicked(self):
        if self.ui.LoginLine.text().strip() and self.ui.PasswordLine.text().strip():
            self.pm.add_password(self.ui.LoginLine.text().strip(), self.ui.PasswordLine.text().strip())
            self.ui.PasswordLine.clear()

            self.accept()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.PswdList.setStyleSheet("color: black; background-color: white;")
        self.setFixedSize(QSize(950, 650)) 

        auth = AuthManager()
        self.pm = PasswordManager(auth._get_pswd())

        self.model = QtGui.QStandardItemModel()
        self.ui.PswdList.setModel(self.model)
        
        self._refresh_list()
        self._connect_signals()

    def _refresh_list(self):
            self.model.clear()
            for login in self.pm.list_logins():
                item = QtGui.QStandardItem(login)
                item.setEditable(False)
                self.model.appendRow(item)
    def _connect_signals(self):
        self.ui.PswdList.clicked.connect(self._copy_password_to_clickboard)

        self.ui.PswdList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.PswdList.customContextMenuRequested.connect(self._show_context_menu)
    def _copy_password_to_clickboard(self,index: QtCore.QModelIndex):
        if not index.isValid():
            return 
        login = self.model.itemFromIndex(index).text()
        try:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(self.pm.get_password(login))
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', f"не удалось извлечь пароль:\n{e}")
    def _show_context_menu(self,pos):
        menu = QtWidgets.QMenu()
        add_action = menu.addAction('Добавить пароль')
        menu.addSeparator()

        index = self.ui.PswdList.indexAt(pos)
        delete_action = menu.addAction('Удалить')
        delete_action.setEnabled(index.isValid())

        action = menu.exec(self.ui.PswdList.viewport().mapToGlobal(pos))
        if action == add_action:
            self._add_password_dialog()
        elif action == delete_action and index.isValid():
            self._delete_login(index)
    def _add_password_dialog(self):
     dialog = AddPasswordDialog(self.pm, self)
     dialog.exec()
     self._refresh_list()

    def _delete_login(self, index: QtCore.QModelIndex):
        login = self.model.itemFromIndex(index).text()
        reply = QtWidgets.QMessageBox.question(
            self, "Удаление", f"Удалить пароль для '{login}'?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.pm.delete_pswd(login)
            self._refresh_list()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())