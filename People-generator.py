import os
import sqlite3
from tkinter import Tk, Text, Button, Listbox, SINGLE, WORD, END
from mimesis import Person, Datetime, Address
from mimesis.enums import Gender
from random import choice as ch
from PIL import Image

# Amount of data in quantity of strings in the main table
data_amount=20

column_names=['ID', 'first_name', 'last_name', 'gender', 'age',
            'date_of_birth', 'city_of_birth', 'address',
            'phone', 'email', 'image']

def Show_image_func():
    try: Image.open('temporary.jpg').show()
    except: pass

def Listbox_filling():
    global listbox
    listbox=Listbox(window, height=37, width=15, selectmode=SINGLE)
    for line in cursor.execute('''SELECT * FROM main_table'''):
        listbox.insert(END, line[2])
    listbox.place(x=405, y=0)

def Re_generate_func():
    global data_amount
    new_data_amount=amount_input.get(1.0, END)[0:-1]
    if new_data_amount.isdigit() and int(new_data_amount)>0:
        data_amount=int(new_data_amount)
    cursor.execute('''DELETE FROM main_table''')
    db.commit()
    Create_table_func()
    Listbox_filling()

def Search_func():
    info_text.delete(1.0, END)
    index=listbox.curselection()
    if index:
        elem=listbox.get(index)
        cursor.execute(f'''SELECT * FROM main_table WHERE last_name="{elem}"''')
        line=cursor.fetchall()[0]
        for i in range(len(line)-1): info_text.insert(eval(f'{(len(column_names)-1)*2}.0'), column_names[i]+': '+line[i]+'\n'*2)
        temporary_file=open('temporary.jpg','wb')
        temporary_file.write(line[len(line)-1])
        temporary_file.close()

def Create_table_func():
    for i in range(data_amount):
        data_list=[]
        data_list.append(''.join([str(i) for j in range(3)]))
        person=Person('en')
        gender=person.gender()
        if 'a' in gender: arg=(eval(f'Gender.{gender.upper()}'), gender)
        else: arg=ch([(Gender.MALE, 'Male'), (Gender.FEMALE, 'Female')])
        data_list.extend([person.name(gender=arg[0]), person.last_name(gender=arg[0])])
        datetime=Datetime()
        date_of_birth=datetime.date(start=1930, end=2020)
        age=2021-int(str(date_of_birth)[:4])
        if age<=15: age_='0' 
        elif 50>=age>15: age_='1'
        else: age_='2'
        data_list.extend([arg[1], age, date_of_birth])
        address=Address()
        data_list.extend([address.city(), address.address()])
        data_list.extend([person.telephone(), person.email()])
        files=[]
        for file_ in os.listdir('Images'):
            if file_[:-8]==arg[1] and file_[-8:-7]==age_ or file_[0]==age_: files.append(file_)  
        image_binary_data=sqlite3.Binary(open(f'Images\\{ch(files)}', 'rb').read())
        cursor.execute(f'''INSERT INTO main_table VALUES
                        ({','.join(f'"{j}"' for j in data_list)}, ?)''', (image_binary_data,))
    db.commit()

db=sqlite3.connect('people.db')
cursor=db.cursor()
cursor.execute(f'''CREATE TABLE IF NOT EXISTS main_table
                ({','.join(i+' text' for i in column_names)})''')
db.commit()

window=Tk()
window.geometry('500x600')  
window.title('People-generator')
window.resizable(False, False)
search_button=Button(window, width=57, height=1, text='Search', bg='#8FBC8F', command=Search_func)
info_text=Text(window, width=37, height=24, font='Arial 14', wrap=WORD)
show_image_button=Button(window, width=57, height=1, text='Show image', bg='#ADD8E6', command=Show_image_func)
amount_input=Text(window, width=37, height=1, font='Arial 14', wrap=WORD)
amount_input.insert(1.0, '*Data amount')
re_generate_button=Button(window, width=57, height=1, text='Re-generate the data', bg='#F08080', command=Re_generate_func)
Listbox_filling()

search_button.place(x=0, y=0)
info_text.place(x=0, y=26)
show_image_button.place(x=0, y=517)
amount_input.place(x=0, y=543)
re_generate_button.place(x=0, y=569)

window.mainloop()