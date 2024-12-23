from database import *
from tkinter import *
from tkinter import ttk, messagebox

window = Tk()
window.title("Транспорт")
window.geometry("1400x720")
window.minsize(750, 400)

#adding comment for lab

class Transport:
    def __init__(self, db_id, type, capacity, length, width, height, reservation_date):
        self.db_id = db_id
        self.type = type
        self.capacity = capacity
        self.length = length
        self.width = width
        self.height = height
        self.reservation_date = reservation_date


all_transport = []


def update_transport():
    global all_transport
    all_transport = []
    for transport in get_all_transport():
        all_transport.append(
            Transport(transport[0], transport[1], transport[2], transport[3], transport[4], transport[5], transport[6]))


update_transport()


def frame_clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def view():
    def frame_soft_clear():
        for widget in window.winfo_children():
            if widget not in table_labels and widget not in widgets_to_keep:
                widget.destroy()

    def sort_by(what):
        for label in table_labels:
            label.destroy()
        data = []
        for transport in all_transport:
            data.append([transport.db_id, transport.type, transport.capacity, transport.length, transport.width,
                         transport.height, transport.reservation_date])
        if what == "capacity":
            data = sorted(data, key=lambda x: float(x[2]), reverse=True)
        if what == "length":
            data = sorted(data, key=lambda x: float(x[3]), reverse=True)
        if what == "width":
            data = sorted(data, key=lambda x: float(x[4]), reverse=True)
        if what == "height":
            data = sorted(data, key=lambda x: float(x[5]), reverse=True)
        if what == "reserved":
            data = sorted(data, key=lambda x: x[6], reverse=True)
        if what == "default":
            pass
        last_row = 0
        for row, row_data in enumerate(data):
            if row_data[-1] == "Нет":
                color = "#00ff00"
            else:
                color = "#ff0000"
            for col, cell_data in enumerate(row_data):
                label = Label(text=cell_data, relief=RIDGE, padx=10, pady=5, background=color)
                table_labels.append(label)
                label.grid(row=row + 1, column=col, sticky="nsew")
                last_row = row + 2
        return last_row

    def change():
        def add_transport():
            def add_to_db():
                try:
                    cap = float(capacity_entry.get())
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверное значение")
                    capacity_entry.delete(0, END)
                    return
                try:
                    leng = float(len_entry.get())
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверное значение")
                    len_entry.delete(0, END)
                    return
                try:
                    wid = float(wid_entry.get())
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверное значение")
                    wid_entry.delete(0, END)
                    return
                try:
                    hei = float(hei_entry.get())
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверное значение")
                    hei_entry.delete(0, END)
                    return
                if cap <= 50 and leng <= 20 and wid <= 4 and hei <= 3 and cap > 0 and leng > 0.5 and wid > 0.5 and hei > 0.5:
                    create_new(type_entry.get(), cap, leng, wid, hei)
                    view()
                else:
                    messagebox.showerror("Ошибка", "Неверные габариты")
                    capacity_entry.delete(0, END)
                    len_entry.delete(0, END)
                    wid_entry.delete(0, END)
                    hei_entry.delete(0, END)

            frame_soft_clear()
            ttk.Label(text="Введите тип:").grid(row=0, column=7)
            ttk.Label(text="Введите грузоподъемность:").grid(row=1, column=7)
            ttk.Label(text="Введите длину:").grid(row=2, column=7)
            ttk.Label(text="Введите ширину:").grid(row=3, column=7)
            ttk.Label(text="Введите высоту:").grid(row=4, column=7)
            type_entry = ttk.Entry()
            type_entry.grid(row=0, column=8)
            capacity_entry = ttk.Entry()
            capacity_entry.grid(row=1, column=8)
            len_entry = ttk.Entry()
            len_entry.grid(row=2, column=8)
            wid_entry = ttk.Entry()
            wid_entry.grid(row=3, column=8)
            hei_entry = ttk.Entry()
            hei_entry.grid(row=4, column=8)
            ttk.Button(text="Добавить", command=add_to_db).grid(row=5, column=7)
            ttk.Button(text="Назад", command=view).grid(row=5, column=8)

        def del_transport():
            def del_from_db():
                picked_id = id_entry.get()
                if transport_exists(picked_id):
                    destroy_transport(picked_id)
                    view()
                else:
                    messagebox.showerror("Ошибка", "Неверное значение")
                    id_entry.delete(0, END)

            frame_soft_clear()
            ttk.Label(text="Введите id:").grid(row=0, column=7)
            id_entry = ttk.Entry()
            id_entry.grid(row=0, column=8)
            ttk.Button(text="Удалить", command=del_from_db).grid(row=5, column=7)
            ttk.Button(text="Назад", command=view).grid(row=5, column=8)

        frame_soft_clear()
        ttk.Button(text="Добавить", command=add_transport).grid(row=0, column=7)
        ttk.Button(text="Удалить", command=del_transport).grid(row=1, column=7)
        ttk.Button(text="Назад", command=view).grid(row=2, column=7)

    def reserve():
        def reserve_in_db():
            picked_id = id_entry.get()
            if transport_exists(picked_id) and not is_reserved(picked_id):
                add_reservation(picked_id)
                view()
            else:
                messagebox.showerror("Ошибка", "Неверное значение")
                id_entry.delete(0, END)

        frame_soft_clear()
        ttk.Label(text="Введите id:").grid(row=0, column=7)
        id_entry = ttk.Entry()
        id_entry.grid(row=0, column=8)
        ttk.Button(text="Забронировать", command=reserve_in_db).grid(row=5, column=7)
        ttk.Button(text="Назад", command=view).grid(row=5, column=8)

    def cancel_reserve():
        def cancel_reserve_in_db():
            picked_id = id_entry.get()
            if transport_exists(picked_id) and is_reserved(picked_id):
                cancel_reservation(picked_id)
                view()
            else:
                messagebox.showerror("Ошибка", "Неверное значение")
                id_entry.delete(0, END)

        frame_soft_clear()
        ttk.Label(text="Введите id:").grid(row=0, column=7)
        id_entry = ttk.Entry()
        id_entry.grid(row=0, column=8)
        ttk.Button(text="Отменить бронь", command=cancel_reserve_in_db).grid(row=5, column=7)
        ttk.Button(text="Назад", command=view).grid(row=5, column=8)

    def gabarites():
        def search():
            try:
                cap = float(capacity_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Неверное значение")
                capacity_entry.delete(0, END)
                return
            try:
                leng = float(len_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Неверное значение")
                len_entry.delete(0, END)
                return
            try:
                wid = float(wid_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Неверное значение")
                wid_entry.delete(0, END)
                return
            try:
                hei = float(hei_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Неверное значение")
                hei_entry.delete(0, END)
                return
            capable = []
            for transport in all_transport:
                if transport.capacity >= cap and transport.length >= leng and transport.width >= wid and transport.height >= hei:
                    capable.append(transport)
            if len(capable) > 0:
                info = ""
                for t in capable:
                    info += f"{t.db_id}. {t.type}\n"
                messagebox.showinfo("Доступный транспорт:", info)
                capacity_entry.delete(0, END)
                len_entry.delete(0, END)
                wid_entry.delete(0, END)
                hei_entry.delete(0, END)

            else:
                messagebox.showerror("Ошибка", "Нет подходящего транспорта")
                capacity_entry.delete(0, END)
                len_entry.delete(0, END)
                wid_entry.delete(0, END)
                hei_entry.delete(0, END)

        frame_soft_clear()
        ttk.Label(text="Введите вес груза:").grid(row=0, column=7)
        ttk.Label(text="Введите длину груза:").grid(row=1, column=7)
        ttk.Label(text="Введите ширину груза:").grid(row=2, column=7)
        ttk.Label(text="Введите высоту груза:").grid(row=3, column=7)
        capacity_entry = ttk.Entry()
        capacity_entry.grid(row=0, column=8)
        len_entry = ttk.Entry()
        len_entry.grid(row=1, column=8)
        wid_entry = ttk.Entry()
        wid_entry.grid(row=2, column=8)
        hei_entry = ttk.Entry()
        hei_entry.grid(row=3, column=8)
        ttk.Button(text="Подобрать", command=search).grid(row=5, column=7)
        ttk.Button(text="Назад", command=view).grid(row=5, column=8)

    global all_transport
    frame_clear(window)
    update_transport()
    table_labels = []
    widgets_to_keep = []

    header_labels = ["id", "Тип", "Грузоподъемность, т.", "Длина, м.", "Ширина, м.", "Высота, м.", "Дата бронирования"]
    for col, header in enumerate(header_labels):
        label = Label(text=header, relief=RIDGE, padx=10, pady=5)
        label.grid(row=0, column=col, sticky="nsew")
        widgets_to_keep.append(label)
    last_row = sort_by("default")
    btn = ttk.Button(text="Сортировать по умолчанию", command=lambda: sort_by("default"))
    btn.grid(row=last_row, column=1, sticky="nsew")
    widgets_to_keep.append(btn)
    btn = ttk.Button(text="Сортировать по грузоподъемности", command=lambda: sort_by("capacity"))
    btn.grid(row=last_row, column=2, sticky="nsew")
    widgets_to_keep.append(btn)
    btn = ttk.Button(text="Сортировать по длине", command=lambda: sort_by("length"))
    btn.grid(row=last_row, column=3, sticky="nsew")
    widgets_to_keep.append(btn)
    btn = ttk.Button(text="Сортировать по ширине", command=lambda: sort_by("width"))
    btn.grid(row=last_row, column=4, sticky="nsew")
    widgets_to_keep.append(btn)
    btn = ttk.Button(text="Сортировать по высоте", command=lambda: sort_by("height"))
    btn.grid(row=last_row, column=5, sticky="nsew")
    widgets_to_keep.append(btn)
    btn = ttk.Button(text="Свободные сверху", command=lambda: sort_by("reserved"))
    btn.grid(row=last_row, column=6, sticky="nsew")
    widgets_to_keep.append(btn)
    btn = ttk.Button(text="Выход", command=exit)
    btn.grid(row=last_row + 1, column=1, sticky="nsew")
    widgets_to_keep.append(btn)
    btn = ttk.Button(text="Редактировать", command=change)
    btn.grid(row=last_row + 1, column=2, sticky="nsew")
    widgets_to_keep.append(btn)
    btn = ttk.Button(text="Забронировать", command=reserve)
    btn.grid(row=last_row + 1, column=3, sticky="nsew")
    widgets_to_keep.append(btn)
    btn = ttk.Button(text="Отменить бронь", command=cancel_reserve)
    btn.grid(row=last_row + 1, column=4, sticky="nsew")
    widgets_to_keep.append(btn)
    btn = ttk.Button(text="Подобрать", command=gabarites)
    btn.grid(row=last_row + 1, column=5, sticky="nsew")
    widgets_to_keep.append(btn)


if __name__ == "__main__":

    view()

    window.mainloop()
