from PyQt5.QtCore import QRect, QSize
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QTextEdit
import sqlite3 as sql


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        with sql.connect('db.db') as con:
            cur = con.cursor()
            cur.execute("""SELECT type FROM ghosts""")
            g_fetch = cur.fetchall()
        
        self.types_list = [el[0] for el in g_fetch]
        self.evidence = [
            'Not',
            'EMF 5',
            'Ghost Orb',
            'Spirit Box',
            'Freezing Temperatures',
            'Fingerprints',
            'Ghost Writing',
            'D.O.T.S'
        ]
    
    def setupUi(self):
        self.setWindowTitle(
            'GhostPicker by WoollySensed SoftWare | ver. 3.0.0'
        )
        self.setMinimumSize(QSize(600, 155))
        self.setMaximumSize(QSize(600, 155))
        self.setObjectName('MainWindow')

        """CentralWidget"""
        self.central_widget = QWidget(self)
        self.central_widget.setGeometry(QRect(5, 5, 200, 600))
        self.central_widget.setObjectName('MainWindow')

        self.lbl_choose = QLabel(self.central_widget)
        self.lbl_choose.setText('Какие улики были найдены?')
        self.lbl_choose.setGeometry(QRect(0, 0, 200, 30))
        self.lbl_choose.setObjectName('MW_lbl_choose')

        self.cb_types = QComboBox(self.central_widget)
        self.cb_types.setGeometry(QRect(0, 30, 200, 20))
        self.cb_types.addItems(self.evidence)
        self.cb_types.setObjectName('MW_cb_types')
        
        self.cb_types_2 = QComboBox(self.central_widget)
        self.cb_types_2.setGeometry(QRect(0, 50, 200, 20))
        self.cb_types_2.addItems(self.evidence)
        self.cb_types_2.setObjectName('MW_cb_types')
        
        self.cb_types_3 = QComboBox(self.central_widget)
        self.cb_types_3.setGeometry(QRect(0, 70, 200, 20))
        self.cb_types_3.addItems(self.evidence)
        self.cb_types_3.setObjectName('MW_cb_types')
        
        self.btn_accept = QPushButton(self.central_widget)
        self.btn_accept.setText('Проверить'.upper())
        self.btn_accept.setGeometry(QRect(0, 100, 200, 20))
        self.btn_accept.clicked.connect(self.data_process_clicked)
        self.btn_accept.setObjectName('MW_btn_accept')
        
        self.btn_clear_text = QPushButton(self.central_widget)
        self.btn_clear_text.setText('Очистить результат'.upper())
        self.btn_clear_text.setGeometry(QRect(0, 125, 200, 20))
        self.btn_clear_text.clicked.connect(self.clear_text_clicked)
        self.btn_clear_text.setObjectName('MW_btn_accept')
        """/CentralWidget"""

        """DisplayInfo"""
        self.display_info = QWidget(self)
        self.display_info.setGeometry(QRect(210, 5, 385, 145))
        self.display_info.setObjectName('MainWindow')

        self.text = QTextEdit(self.display_info)
        self.text.setGeometry(QRect(0, 0, 385, 145))
        self.text.setObjectName('MW_text')
        """/DisplayInfo"""
    
    def converter_for_db(self, evidence: list) -> list:
        """Конвертирует записи из комбобокса в записи,
        которые может принять таблица, возврящая список
        """
        converted_list = []

        for el in evidence:
            if el == 'EMF 5':
                converted_list.append('emf5')
            elif el == 'Ghost Orb':
                converted_list.append('orb')
            elif el == 'Spirit Box':
                converted_list.append('spirit_box')
            elif el == 'Freezing Temperatures':
                converted_list.append('freezing_temp')
            elif el == 'Fingerprints':
                converted_list.append('fingerprints')
            elif el == 'Ghost Writing':
                converted_list.append('ghost_writing')
            elif el == 'D.O.T.S':
                converted_list.append('dots')
        
        if len(converted_list) != 0:
            converted_list = list(set(converted_list))
            return converted_list
        else: return []

    def data_checker(self, evidence: list) -> list:
        """Возвращает список из кортежей, в котором:
        0. Тип призрака
        1. Рассудок
        2. Скорость
        """
        with sql.connect('db.db') as con:
            cur = con.cursor()
            
            if len(evidence) == 1:
                cur.execute(f"""SELECT type, sanity, speed FROM ghosts
                    WHERE ({evidence[0]}=1)"""
                )
                data_result = cur.fetchall()
                return data_result

            elif len(evidence) == 2:
                cur.execute(f"""SELECT type, sanity, speed FROM ghosts
                    WHERE ({evidence[0]}=1 AND {evidence[1]}=1)"""
                )
                data_result = cur.fetchall()
                return data_result
            
            elif len(evidence) == 3:
                cur.execute(f"""SELECT type, sanity, speed FROM ghosts WHERE
                    ({evidence[0]}=1 AND {evidence[1]}=1 AND {evidence[2]})"""
                )
                data_result = cur.fetchall()
                return data_result
    
    def search_detect_methods(self, data_result: list) -> list:
        """Возвращает список из data_result+список методов обнаружения"""
        with sql.connect('db.db') as con:
            cur = con.cursor()

            data_result_and_methods = []
            try:
                for el in data_result:
                    cur.execute(f"""SELECT detect_method FROM type_info
                        WHERE (type='{el[0]}')"""
                    )
                    data_result_and_methods.append((
                        f'{el[0]}', f'{el[1]}', f'{el[2]}',
                        [method[0] for method in cur.fetchall()]
                    ))
                else: return data_result_and_methods
            except TypeError: return []
    
    def data_display(self, data_result_and_methods: list):
        """Отображает всю нужную информацию в self.text"""
        if len(data_result_and_methods) != 0:
            for el in data_result_and_methods:
                self.text.insertPlainText(
                    f'Тип призрака: {el[0]}' +
                    f'\nРассудок для атаки: {el[1]}' +
                    f'\nСкорость призрака: {el[2]}' +
                    '\nМетоды для определения:'
                )
                for method in el[3]:
                    self.text.insertPlainText(f'\n|> {method}')
                else: self.text.insertPlainText('\n\n')
        else: self.text.insertPlainText('Мне нужны улики для ответа...\n')
    
    def data_process_clicked(self):
        evidence = [
            self.cb_types.currentText(),
            self.cb_types_2.currentText(),
            self.cb_types_3.currentText()
        ]
        data_result_and_methods = self.search_detect_methods(
            self.data_checker(self.converter_for_db(evidence))
        )
        self.data_display(data_result_and_methods)
    
    def clear_text_clicked(self): self.text.clear()
