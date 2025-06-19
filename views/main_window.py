from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableView, QPushButton,
    QLabel, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QIcon


class MaterialsTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None


class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("Система учета материалов")
        self.setGeometry(100, 100, 800, 600)

        # Центральный виджет
        central_widget = QWidget()
        central_widget.setStyleSheet('background-color: #e0e0e0;')
        self.setCentralWidget(central_widget)

        # Основной layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        central_widget.setStyleSheet('background-color: rgba(130, 203, 172, 1);')

        # Заголовок
        title_label = QLabel("Учет материалов на складе")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Таблица материалов
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.doubleClicked.connect(self.edit_material)
        layout.addWidget(self.table_view)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.setStyleSheet('background-color:#e9e9e9;')
        self.add_button.clicked.connect(self.add_material)
        buttons_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.clicked.connect(self.edit_material)
        buttons_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_material)
        buttons_layout.addWidget(self.delete_button)

        self.products_button = QPushButton("Продукция")
        self.products_button.clicked.connect(self.show_products)
        buttons_layout.addWidget(self.products_button)

        layout.addLayout(buttons_layout)

    def load_data(self):
        materials = self.model.get_all_materials()
        if materials:
            headers = [
                "ID", "Тип", "Наименование", "Цена (р/ед)",
                "Ед. изм.", "В упаковке", "На складе",
                "Мин. кол-во", "Требуется"
            ]

            table_data = []
            for material in materials:
                table_data.append([
                    material['id'],
                    material['type'],
                    material['name'],
                    f"{material['price']:.2f}",
                    material['unit'],
                    material['package_amount'],
                    f"{material['stock_amount']:.2f}",
                    material['min_amount'],
                    f"{material['required_amount']:.2f}" if material['required_amount'] else "0.00"
                ])

            self.model_table = MaterialsTableModel(table_data, headers)
            self.table_view.setModel(self.model_table)
            self.table_view.resizeColumnsToContents()
            self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def add_material(self):
        from views.add_edit_material import AddEditMaterialDialog
        dialog = AddEditMaterialDialog(self.model, parent=self)
        if dialog.exec_():
            self.load_data()

    def edit_material(self):
        selected = self.table_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите материал для редактирования")
            return

        material_id = self.model_table.data(selected[0].siblingAtColumn(0), Qt.DisplayRole)
        from views.add_edit_material import AddEditMaterialDialog
        dialog = AddEditMaterialDialog(self.model, material_id=material_id, parent=self)
        if dialog.exec_():
            self.load_data()

    def delete_material(self):
        selected = self.table_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите материал для удаления")
            return

        material_id = self.model_table.data(selected[0].siblingAtColumn(0), Qt.DisplayRole)
        material_name = self.model_table.data(selected[0].siblingAtColumn(2), Qt.DisplayRole)

        reply = QMessageBox.question(
            self, 'Подтверждение',
            f'Вы уверены, что хотите удалить материал "{material_name}"?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.model.delete_material(material_id):
                QMessageBox.information(self, "Успех", "Материал успешно удален")
                self.load_data()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить материал")

    def show_products(self):
        selected = self.table_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите материал для просмотра продукции")
            return

        material_id = self.model_table.data(selected[0].siblingAtColumn(0), Qt.DisplayRole)
        material_name = self.model_table.data(selected[0].siblingAtColumn(2), Qt.DisplayRole)

        from views.product_list import ProductListDialog
        dialog = ProductListDialog(self.model, material_id, material_name, parent=self)
        dialog.exec_()

    def closeEvent(self, event):
        self.model.close()
        event.accept()