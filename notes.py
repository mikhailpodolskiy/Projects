from tkinter import *
import sqlite3


def db_start():
    global conn, cur

    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note TEXT)""")

def save_note():
    note = note_entry.get()
    cur.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()
    update_notes_list()
    note_entry.delete(0, END)

def delete_note():
    index = notes_list.curselection()
    if index:
        selected_note = notes_list.get(index)
        cur.execute("DELETE FROM notes WHERE note=?", (selected_note,))
        conn.commit()
        update_notes_list()

def update_notes_list():
    notes_list.delete(0, END)
    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()
    for note in notes:
        note_text = note[1]
        notes_list.insert(END, note_text)

def click():
    window = Tk()
    window.title("Окно добавления заметок")
    window.geometry("250x200")
    root.resizable(0, 0)
    window.wm_attributes("-topmost", 1)

    note_label = Label(window, text = "Введите название заметки")
    note_label.pack(pady=5)

    global note_entry
    note_entry = Entry(window)
    note_entry.pack(pady=5)

    save_button = Button(window, text="Добавить заметку", command= lambda: (save_note(), window.destroy()))
    save_button.pack(pady=5)

    window.mainloop()

root = Tk()
root.title("Application for notes")
root.geometry("400x400")
root.resizable(0, 0)

button = Button(root, text="Добавить заметку в новом окне", command=click)
button.pack(pady=5)

notes_list = Listbox(root, width=45, height=15)
notes_list.pack(pady=5)

delete_button = Button(root, text="Удалить заметку", command=delete_note)
delete_button.pack(pady=5)



db_start()
update_notes_list()

root.mainloop()
conn.close()
