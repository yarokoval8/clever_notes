#для начала скопируй сюда интерфейс "Умных заметок" и проверь его работу

#затем запрограммируй демо-версию функционала
#для начала скопируй сюда интерфейс "Умных заметок" и проверь его работу

#затем запрограммируй демо-версию функционала
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, \
    QHBoxLayout, QVBoxLayout, QFormLayout

app = QApplication([])
notes = []

'''Інтерфейс'''
# Параметри вікна
notes_win = QWidget()
notes_win.setWindowTitle('Розумні нотатки')
notes_win.resize(900, 600)

# Віджети
list_notes = QListWidget()
list_notes_label = QLabel('Список нотаток')

button_note_create = QPushButton('Створити нотатку')
button_note_del = QPushButton('Видалити нотатку')
button_save = QPushButton('Зберегти нотатку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Ввести тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Додати до нотатки')
button_tag_del = QPushButton('Видалити з нотатки')
button_tag_search = QPushButton('Шукати нотатки за тегом')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')

# Розмітки віджетів
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

# SAVE IN JSON
def save_notes_to_json():
    with open("notes_data.json", "w") as file:
        json.dump(notes, file, indent=4, ensure_ascii=False, sort_keys=True)

# upload in json
def load_notes_from_json():
    with open("notes_data.json", "w") as file:
        try:
            with open("notes_data.json", "w") as file:
                notes.extend(json.load(file))
        except FileNotFoundError:
            pass   

def show_note():
    key = list_notes.selectedItems()[0].text()
    for note in notes:
        if note["name"] == key:
            field_text.setText(note['content'])
            list_notes.clear()
            list_notes.addItems(note['tags'])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        for note in notes:
            if note['name'] == key:
                note['content'] = field_text.toPlainText()
                save_notes_to_json()
                print("Нотатка збережена:", note)
                break
    else:
        print("Необрано нотатки для зберігання!")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        for note in notes:
            if note['note'] == key:
                print(note['name'] + ' ' + key)
                notes.remove(note)
                list_notes.takeItem(list_notes.row(list_notes.selectedItems()[0]))
                print('Нотатка видалинна:', note)
                save_notes_to_json()
                break
    else:
        print("Необрано нотатки для видалення!:")
                
def add_note():
    note_name, ok = QInputDialog.getText(notes_win,"Додати нотатку", "І'мя нотатки:")
    if ok and note_name != "":
            note = {
                'name': note_name,
                'content': '',
                'tags': []
            }
            notes.append(note)
            list_notes.addItem(note['name'])
            print("Додано нотатку:", note)
            save_notes_to_json()

def add_teg():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        for note in notes:
            if note['name'] == key:
                if tag not in note['tags']:
                    note['tags'].append(tag)
                    list_tags.addItem(tag)
                    field_tag.clear()
                    save_notes_to_json()
                    print('Тег доданний до нотатки:', tag)
                break
    else:
        print('Необрано нотатки для додавання тегу!:')


# обробка подій
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_teg)
# Старт застосунку
notes_win.show()

# Додати всі з json до list_notes для подальшої роботи
for note in notes:
    list_notes.addItem(note['name'])



app.exec_()