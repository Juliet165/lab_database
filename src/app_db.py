import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import pymssql

# Подключение к базе данных SQL Server
connection = pymssql.connect(
    server="localhost",
    user="sa",
    password="knopa12345",
    database="University"
)
cursor = connection.cursor()

# Функция для получения отображаемых значений вместо ID
def fetch_display_values(table_name):
    if table_name == "specializations":
        cursor.execute("SELECT id, name FROM specializations")
    elif table_name == "groups":
        cursor.execute("""
            SELECT groups.id, CONCAT('Курс: ', groups.course_number, 
                                      ', Группа: ', groups.group_number, 
                                      ', Специализация: ', specializations.name) 
            FROM groups 
            JOIN specializations ON groups.specialization_id = specializations.id
        """)
    elif table_name == "students":
        cursor.execute("SELECT id, full_name FROM students")
    return {row[0]: row[1] for row in cursor.fetchall()}

# Основное окно приложения
root = tk.Tk()
root.title("Справочники")
root.geometry("850x600")
root.configure(bg="#f1f1f1")  

footer_label = tk.Label(root, text="Каноплич Юлия Евгеньевна, 3 курс, 11 группа, 2024", bg="#f1f1f1", font=("Segoe UI", 12))
footer_label.pack(pady=10)

# Выпадающий список справочников
tables = ["specializations", "groups", "students"]
selected_table = tk.StringVar(value="specializations")

table_dropdown = ttk.Combobox(root, values=tables, textvariable=selected_table, font=("Segoe UI", 12), state="readonly")
table_dropdown.pack(pady=10)

# Таблица для отображения данных
tree = ttk.Treeview(root, style="Treeview")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Функция для загрузки данных
def load_table_data():
    for i in tree.get_children():
        tree.delete(i)

    table_name = selected_table.get()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    tree["columns"] = columns
    tree["show"] = "headings"

    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=150, anchor="center")

    for row in data:
        tree.insert("", tk.END, values=row)

# Функция для добавления записи
def add_record():
    table_name = selected_table.get()

    if table_name == "specializations":
        add_specialization()
    elif table_name == "groups":
        add_group()
    elif table_name == "students":
        add_student()

# Функция для добавления специализации
def add_specialization():
    new_window = tk.Toplevel(root)
    new_window.title("Добавить специализацию")
    new_window.geometry("400x300")
    new_window.configure(bg="#f5e1da")

    tk.Label(new_window, text="Название:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    name_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    name_entry.pack(pady=5)

    tk.Label(new_window, text="Описание:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    description_entry = tk.Text(new_window, height=5, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    description_entry.pack(pady=5)

    def save():
        name = name_entry.get()
        description = description_entry.get("1.0", tk.END).strip()
        cursor.execute("INSERT INTO specializations (name, description) VALUES (%s, %s)", (name, description))
        connection.commit()
        messagebox.showinfo("Успех", "Специализация добавлена.")
        new_window.destroy()
        load_table_data()

    tk.Button(new_window, text="Сохранить", command=save, bg="#49beb7", fg="white", font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2).pack(pady=10)

# Функция для добавления группы
def add_group():
    new_window = tk.Toplevel(root)
    new_window.title("Добавить группу")
    new_window.geometry("400x350")
    new_window.configure(bg="#f5e1da")

    tk.Label(new_window, text="Номер курса:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    course_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    course_entry.pack(pady=5)

    tk.Label(new_window, text="Номер группы:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    group_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    group_entry.pack(pady=5)

    tk.Label(new_window, text="Специализация:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    specialization_values = fetch_display_values("specializations")
    specialization_combobox = ttk.Combobox(
        new_window, values=list(specialization_values.values()), width=47, font=("Segoe UI", 12)
    )
    specialization_combobox.pack(pady=5)

    tk.Label(new_window, text="Количество студентов:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    student_count_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    student_count_entry.pack(pady=5)

    def save():
        course_number = course_entry.get()
        group_number = group_entry.get()
        specialization_name = specialization_combobox.get()
        specialization_id = next(
            key for key, value in specialization_values.items() if value == specialization_name
        )
        student_count = student_count_entry.get()

        cursor.execute(
            "INSERT INTO groups (course_number, group_number, specialization_id, student_count) VALUES (%s, %s, %s, %s)",
            (course_number, group_number, specialization_id, student_count)
        )
        connection.commit()
        messagebox.showinfo("Успех", "Группа добавлена.")
        new_window.destroy()
        load_table_data()

    tk.Button(new_window, text="Сохранить", command=save, bg="#49beb7", fg="white", font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2).pack(pady=10)

# Функция для добавления студента
def add_student():
    new_window = tk.Toplevel(root)
    new_window.title("Добавить студента")
    new_window.geometry("400x500")
    new_window.configure(bg="#f5e1da")

    tk.Label(new_window, text="ФИО:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    full_name_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    full_name_entry.pack(pady=5)

    tk.Label(new_window, text="Дата рождения:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    birth_date_entry = DateEntry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    birth_date_entry.pack(pady=5)

    tk.Label(new_window, text="Номер зачетки:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    record_book_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    record_book_entry.pack(pady=5)

    tk.Label(new_window, text="Дата зачисления:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    enrollment_date_entry = DateEntry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    enrollment_date_entry.pack(pady=5)

    tk.Label(new_window, text="Средний балл:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    average_grade_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    average_grade_entry.pack(pady=5)

    tk.Label(new_window, text="Группа:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    group_values = fetch_display_values("groups")
    group_combobox = ttk.Combobox(new_window, values=list(group_values.values()), width=47, font=("Segoe UI", 12))
    group_combobox.pack(pady=5)

    def save():
        full_name = full_name_entry.get()
        birth_date = birth_date_entry.get()
        record_book_number = record_book_entry.get()
        enrollment_date = enrollment_date_entry.get()
        average_grade = average_grade_entry.get()
        group_name = group_combobox.get()
        group_id = next(
            key for key, value in group_values.items() if value == group_name
        )

        cursor.execute(
            "INSERT INTO students (full_name, birth_date, group_id, record_book_number, "
            "enrollment_date, average_grade) VALUES (%s, %s, %s, %s, %s, %s)",
            (full_name, birth_date, group_id, record_book_number, enrollment_date, average_grade)
        )
        connection.commit()
        messagebox.showinfo("Успех", "Студент добавлен.")
        new_window.destroy()
        load_table_data()

    tk.Button(new_window, text="Сохранить", command=save, bg="#49beb7", fg="white", font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2).pack(pady=10)

# Функция редактирования записи
def edit_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Выберите запись для редактирования.")
        return

    selected_values = tree.item(selected_item)["values"]
    table_name = selected_table.get()

    if table_name == "specializations":
        edit_specialization(selected_values)
    elif table_name == "groups":
        edit_group(selected_values)
    elif table_name == "students":
        edit_student(selected_values)

# Функция редактирования специализации
def edit_specialization(values):
    new_window = tk.Toplevel(root)
    new_window.title("Редактировать специализацию")
    new_window.geometry("400x300")
    new_window.configure(bg="#f5e1da")

    tk.Label(new_window, text="Название:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    name_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    name_entry.insert(0, values[1]) 
    name_entry.pack(pady=5)

    tk.Label(new_window, text="Описание:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    description_entry = tk.Text(new_window, height=5, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    description_entry.insert("1.0", values[2]) 
    description_entry.pack(pady=5)

    def save():
        name = name_entry.get()
        description = description_entry.get("1.0", tk.END).strip()
        cursor.execute(
            "UPDATE specializations SET name=%s, description=%s WHERE id=%s",
            (name, description, values[0])  
        )
        connection.commit()
        messagebox.showinfo("Успех", "Специализация обновлена.")
        new_window.destroy()
        load_table_data()

    tk.Button(new_window, text="Сохранить", command=save, bg="#49beb7", fg="white", font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2).pack(pady=10)

# Функция редактирования группы
def edit_group(values):
    new_window = tk.Toplevel(root)
    new_window.title("Редактировать группу")
    new_window.geometry("400x350")
    new_window.configure(bg="#f5e1da")

    tk.Label(new_window, text="Номер курса:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    course_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    course_entry.insert(0, values[1]) 
    course_entry.pack(pady=5)

    tk.Label(new_window, text="Номер группы:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    group_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    group_entry.insert(0, values[2])  
    group_entry.pack(pady=5)

    tk.Label(new_window, text="Специализация:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    specialization_values = fetch_display_values("specializations")
    specialization_combobox = ttk.Combobox(
        new_window, values=list(specialization_values.values()), width=47, font=("Segoe UI", 12)
    )
    specialization_combobox.set(values[3]) 
    specialization_combobox.pack(pady=5)

    tk.Label(new_window, text="Количество студентов:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    student_count_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    student_count_entry.insert(0, values[4])  
    student_count_entry.pack(pady=5)

    def save():
        course_number = course_entry.get()
        group_number = group_entry.get()
        specialization_name = specialization_combobox.get()
        specialization_id = next(
            key for key, value in specialization_values.items() if value == specialization_name
        )
        student_count = student_count_entry.get()

        cursor.execute(
            "UPDATE groups SET course_number=%s, group_number=%s, specialization_id=%s, student_count=%s WHERE id=%s",
            (course_number, group_number, specialization_id, student_count, values[0])
        )
        connection.commit()
        messagebox.showinfo("Успех", "Группа обновлена.")
        new_window.destroy()
        load_table_data()

    tk.Button(new_window, text="Сохранить", command=save, bg="#49beb7", fg="white", font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2).pack(pady=10)

def edit_student(values):

    new_window = tk.Toplevel(root)
    new_window.title("Редактировать студента")
    new_window.geometry("500x500")
    new_window.configure(bg="#f5e1da")

    tk.Label(new_window, text="ФИО:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    full_name_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    full_name_entry.insert(0, values[1])  
    full_name_entry.pack(pady=5)

    tk.Label(new_window, text="Дата рождения:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    birth_date_entry = DateEntry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    birth_date = datetime.strptime(values[2], "%Y-%m-%d").date()
    birth_date_entry.set_date(birth_date)
    birth_date_entry.pack(pady=5)

    tk.Label(new_window, text="Номер зачетки:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    record_book_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    record_book_entry.insert(0, values[3])  
    record_book_entry.pack(pady=5)

    tk.Label(new_window, text="Дата зачисления:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    enrollment_date_entry = DateEntry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    enrollment_date = datetime.strptime(values[4], "%Y-%m-%d").date()
    enrollment_date_entry.set_date(enrollment_date)
    enrollment_date_entry.pack(pady=5)

    tk.Label(new_window, text="Средний балл:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)
    average_grade_entry = tk.Entry(new_window, width=50, font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
    average_grade_entry.insert(0, values[5])  
    average_grade_entry.pack(pady=5)

    tk.Label(new_window, text="Группа:", bg="#f5e1da", font=("Segoe UI", 12)).pack(pady=5)

    group_values = fetch_display_values("groups")  

    group_combobox = ttk.Combobox(new_window, values=list(group_values.values()), width=47, font=("Segoe UI", 12))

    group_id = values[3]  
    group_name = group_values.get(group_id)  

    if group_name:
        group_combobox.set(group_name)  
    else:
        group_combobox.set(list(group_values.values())[0])

    group_combobox.pack(pady=5)

    def save():
        full_name = full_name_entry.get()
        birth_date = birth_date_entry.get_date()  
        record_book_number = record_book_entry.get()
        enrollment_date = enrollment_date_entry.get_date() 
        average_grade = average_grade_entry.get()
        group_name = group_combobox.get()

        group_id = next(key for key, value in group_values.items() if value == group_name)
        cursor.execute(
            "UPDATE students SET full_name=%s, birth_date=%s, group_id=%s, record_book_number=%s, "
            "enrollment_date=%s, average_grade=%s WHERE id=%s",
            (full_name, birth_date, group_id, record_book_number, enrollment_date, average_grade, values[0])
        )
        connection.commit()
        messagebox.showinfo("Успех", "Студент обновлен.")
        new_window.destroy()
        load_table_data()

    tk.Button(new_window, text="Сохранить", command=save, bg="#49beb7", fg="white", font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2).pack(pady=10)


# Функция для удаления записи
def delete_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Выберите запись для удаления.")
        return

    result = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту запись?")
    if result:
        selected_values = tree.item(selected_item)["values"]
        table_name = selected_table.get()

        if table_name == "specializations":
            cursor.execute("DELETE FROM specializations WHERE id=%s", (selected_values[0],))
        elif table_name == "groups":
            cursor.execute("DELETE FROM groups WHERE id=%s", (selected_values[0],))
        elif table_name == "students":
            cursor.execute("DELETE FROM students WHERE id=%s", (selected_values[0],))

        connection.commit()
        messagebox.showinfo("Успех", "Запись удалена.")
        load_table_data()


def show_all_data():
    load_table_data()

# Кнопки управления
buttons_frame = tk.Frame(root, bg="#f1f1f1")
buttons_frame.pack(pady=10)

add_button = tk.Button(buttons_frame, text="Добавить", command=add_record, bg="#49beb7", fg="white", font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
add_button.pack(side=tk.LEFT, padx=10)

edit_button = tk.Button(buttons_frame, text="Редактировать", command=edit_record, bg="#49beb7", fg="white", font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
edit_button.pack(side=tk.LEFT, padx=10)

delete_button = tk.Button(buttons_frame, text="Удалить", command=delete_record, bg="#49beb7", fg="white", font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
delete_button.pack(side=tk.LEFT, padx=10)

show_button = tk.Button(buttons_frame, text="Показать все данные", command=show_all_data, bg="#49beb7", fg="white", font=("Segoe UI", 12), relief="solid", bd=2, borderwidth=2)
show_button.pack(side=tk.LEFT, padx=10)

load_table_data()
root.mainloop()