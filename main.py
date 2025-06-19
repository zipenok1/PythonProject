import sys
from PyQt5.QtWidgets import QApplication
from models.material_model import MaterialModel
from views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Инициализация модели
    model = MaterialModel()

    # Создание и отображение главного окна
    window = MainWindow(model)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()