import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame): #контейнер создали
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):

        '''THAT IS TOOLBAR'''

        toolbar = tk.Frame()
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog = ttk.Button(toolbar, text='Расчет', command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        btn_edit_dialog = ttk.Button(toolbar, text='Редактировать', command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        btn_search = ttk.Button(toolbar, text='Поиск', command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)


        '''______________________'''

        '''LINE FOR ID AND OTHER ON MAIN MENU'''
        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'costs', 'total'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('description', width=365, anchor=tk.CENTER)
        self.tree.column('costs', width=150, anchor=tk.CENTER)
        self.tree.column('total', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('costs', text='Статья дохода/расхода')
        self.tree.heading('total', text='Сумма')

        self.tree.pack()

        '''_____________________'''

    def records(self, description, costs, total):
        self.db.insert_data(description, costs, total)
        self.view_records()

    def update_records(self, description, costs, total):
        self.db.c.execute('''UPDATE finance SET description=?, costs=?, total=? WHERE ID=?''',
                          (description, costs, total, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM finance''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


    
    def open_dialog(self):
        Child()


    def open_update_dialog(self):
        Update()


    def open_search_dialog(self):
        Search()








class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):#Дочернее окно
        self.title('Расчет')
        self.geometry('400x220+400+300')
        self.resizable(False, False)




        label_discription = ttk.Label(self, text='Наименование:')
        label_discription.place(x=50, y=50)

        label_select = ttk.Label(self, text='Статья дохода/расхода:')
        label_select.place(x=50, y=80)

        label_suma = ttk.Label(self, text='Сумма:')
        label_suma.place(x=50, y=110)



        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Доход', 'Расход'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)



        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=30, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=200, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                  self.combobox.get(),
                                                                  self.entry_money.get(),
                                                                  ))


        self.grab_set()
        self.focus_set()


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.search_child()
        self.view = app


    def search_child(self):
        self.title('Поиск')
        self.geometry('600x500+400+300')
        self.resizable(True, True)

        label_search_name = ttk.Label(self, text='Имя клиента')
        label_search_name.place(x=50, y=50)

        label_search_lastname = ttk.Label(self, text='Фамилия клиента')
        label_search_lastname.place(x=50, y=90)

        self.entery_name = ttk.Entry(self)
        self.entery_name.place(x=200, y=50)

        self.entery_lastname = ttk.Entry(self)
        self.entery_lastname.place(x=200, y=90)











class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Редактировать')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_records(self.entry_description.get(),
                                                                           self.combobox.get(),
                                                                           self.entry_money.get()))
        self.btn_ok.destroy()










class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS finance (id INTEGER PRIMARY KEY, description TEXT,
                costs TEXT, total REAL)'''
        )

        self.conn.commit()

    def insert_data(self, description, costs, total):
        self.c.execute('''INSERT INTO finance(description, costs, total) VALUES (?, ?, ?)''',
                       (description, costs, total))
        self.conn.commit()#save change


    def read_from_db(self):
        self.c




if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Расчет')
    root.geometry('650x450+300+200')
    root.resizable(False, False)
    root.mainloop()