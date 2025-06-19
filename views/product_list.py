from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableView, QAbstractItemView, QHeaderView
)
from PyQt5.QtCore import Qt, QAbstractTableModel


class ProductsTableModel(QAbstractTableModel):
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


class ProductListDialog(QDialog):
    def __init__(self, model, material_id, material_name, parent=None):
        super().__init__(parent)
        self.model = model
        self.material_id = material_id
        self.setWindowTitle(f"Продукция для материала: {material_name}")
        self.setWindowModality(Qt.ApplicationModal)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title_label = QLabel(f"Продукция, использующая материал:")
        layout.addWidget(self.title_label)

        self.table_view = QTableView()
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table_view)

    def load_data(self):
        material = self.model.get_material(self.material_id)
        if material and 'products' in material:
            headers = ["ID", "Наименование продукции", "Количество материала"]

            table_data = []
            for product in material['products']:
                table_data.append([
                    product['id'],
                    product['name'],
                    f"{product['amount']:.2f}"
                ])

            self.model_table = ProductsTableModel(table_data, headers)
            self.table_view.setModel(self.model_table)
            self.table_view.resizeColumnsToContents()
            self.table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)