from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import tkinter.tix as tk
from click import command
import requests
import bs4
import matplotlib.pyplot as plt
import numpy as np


def f1(): 								# add button ka function
    add_window.deiconify()
    main_window.withdraw()

def add():
    con = None
    try:
        con = connect("ems.db")
        cursor = con.cursor()
        sql1 = "select id from employee"
        cursor.execute(sql1)
        data = cursor.fetchall()
        id_lst = []
        for d in data:
            id_lst.append(d[0])
        sql = "insert into employee values('%d', '%s', '%f')"
        id = None
        try:
            id = int(aw_ent_id.get())
            if id < 1:
                raise Exception("Invalid Id")
            elif id in id_lst:
                raise Exception("Id already exists")
        except ValueError:
            id1 = str(aw_ent_id.get())
            if len(id1) == 0:
                raise Exception("Id cannot be empty")
            elif id1.isspace():
                raise Exception("Spaces not allowed")
            else:
                raise Exception("Integers Only")

        name = aw_ent_name.get()
        if len(name) < 2:
            raise Exception("Invalid name")
        elif name.isalpha():
            pass
        else:
            raise Exception("Name should contain alphabets only")

        sal = None
        try:
            sal = float(aw_ent_sal.get())
            if sal < 8000:
                raise Exception("Invalid Salary")
        except ValueError:
            raise Exception("Salary cannot be empty")
       
        cursor.execute(sql % (id, name, sal))
        con.commit()
        showinfo("Success", "Record Inserted Successfully!")

        aw_ent_id.delete(0, END)
        aw_ent_name.delete(0, END)
        aw_ent_sal.delete(0, END)


    except Exception as e:
        showerror("Issue :  ", e)
        con.rollback()

    finally:
        if con is not None:
            con.close()


def f2(): 								# back button ka function
    main_window.deiconify()
    add_window.withdraw()


def f3():								# view button ka function
    view_window.deiconify()
    main_window.withdraw()
    vw_st_data.delete(1.0, END)
    info = ""
    con = None
    try:
        con = connect("ems.db")
        cursor = con.cursor()
        sql = "select * from employee"
        cursor.execute(sql)
        data = cursor.fetchall()
        for d in data:
            info = info + " id: " + str(d[0]) + "\t name: " + str(d[1])  + "\t\t salary: " + str(d[2]) + "\n"
        vw_st_data.insert(INSERT, info)

    except Exception as e:
        showerror("Issue :  ", e)

    finally:
        if con is not None:
            con.close()


def f4(): 								# back button ka function
    main_window.deiconify()
    view_window.withdraw()


def f5(): 								# update button ka function
    update_window.deiconify()
    main_window.withdraw()


def update():
    con = None
    try:
        con = connect("ems.db")
        print("connected")
        cursor = con.cursor()
        sql1 = "select id from employee"
        cursor.execute(sql1)
        data = cursor.fetchall()
        id_lst = []
        for d in data:
            id_lst.append(d[0])
        sql = "update employee set name = '%s', sal = '%f' where id = '%d' "
        id = None
        try:
            id = int(uw_ent_id.get())
            if id < 1:
                raise Exception("Invalid Id")
            elif id not in id_lst:
                raise Exception("Id does not exists")
        except ValueError:
            id1 = str(uw_ent_id.get())
            if len(id1) == 0:
                raise Exception("Id cannot be empty")
            elif id1.isspace():
                raise Exception("Spaces not allowed")
            else:
                raise Exception("Integers Only")

        name = uw_ent_name.get()
        if len(name) < 2:
            raise Exception("Invalid name")
        elif name.isalpha():
            pass
        else:
            raise Exception("Name should contain alphabets only")

        sal = None
        try:
            sal = float(uw_ent_sal.get())
            if sal < 8000:
                raise Exception("Invalid Salary")
        except ValueError:
            raise Exception("Salary cannot be empty")

        cursor.execute(sql % (name, sal, id))
        if cursor.rowcount == 1:
            con.commit()
            showinfo("Success", "Record Updated")
        else:
            showerror("Issue :  ", "Some Issue Found")
        uw_ent_id.delete(0, END)
        uw_ent_name.delete(0, END)
        uw_ent_sal.delete(0, END)

    except Exception as e:
        showinfo("issue ", e)
        con.rollback()

    finally:
        if con is not None:
            con.close()



def f6(): 								# back button ka function
    main_window.deiconify()
    update_window.withdraw()


def f7(): 								# delete button ka function
    delete_window.deiconify()
    main_window.withdraw()


def delete():
    con = None
    try:
        con = connect("ems.db")
        print("connected")
        cursor = con.cursor()
        sql1 = "select id from employee"
        cursor.execute(sql1)
        data = cursor.fetchall()
        id_lst = []
        for d in data:
            id_lst.append(d[0])
        sql = "delete from employee where id = '%d' "
        id = None
        try:
            id = int(dw_ent_id.get())
            if id < 1:
                raise Exception("Invalid Id")
            elif id not in id_lst:
                raise Exception("Id does not exists")
        except ValueError:
            id1 = str(dw_ent_id.get())
            if len(id1) == 0:
                raise Exception("Id cannot be empty")
            elif id1.isspace():
                raise Exception("Spaces not allowed")
            else:
                raise Exception("Integers Only")
        cursor.execute(sql % (id))
        if cursor.rowcount == 1:
            con.commit()
            showinfo("Success", "Record deleted")
        else:
            showinfo("Success", "Record does not exists")
        dw_ent_id.delete(0, END)

    except Exception as e:
        showerror("Issue :  ", e)
        con.rollback()

    finally:
        if con is not None:
            con.close()


def f8(): 								# back button ka function
    main_window.deiconify()
    delete_window.withdraw()

def Nmaxelements(list1, N):
	final_list = []
	for i in range(0, N):
		max1 = max(list1)
		final_list.append(max1)
		list1.remove(max1)
	return final_list

def charts():
	con = None
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "select sal from employee"
		cursor.execute(sql)
		data = cursor.fetchall()
		sal_lst = []
		for d in data:
			sal_lst.append(d[0])
		#print(lst)
		N=5
		final_list = Nmaxelements(sal_lst, N)
		#print(final_list)
		
		n_lst=[]
		for i in range(0, len(final_list)):
			sql1 = "select name from employee where sal='%f'"
			cursor.execute(sql1 % (final_list[i]))
			data1 = cursor.fetchall()
			for d in data1:
				if d[0] not in n_lst:
					n_lst.append(d[0])
		#print(n_lst)
		
		fig = plt.figure()
		fig.patch.set_facecolor('xkcd:pink')
		ax= plt.gca()
		ax.set_facecolor('xkcd:pink')
		plt.bar(n_lst, final_list, color='black')
		plt.xlabel("Employee")
		plt.ylabel("Salary")
		plt.title("Top Employees")
		plt.show()
        
		
	except Exception as e:
		con.rollback()
		showerror("Issue", e)
	finally:
		if con is not None:
			con.close()

def f9(): 								# back button ka function
    charts_window.deiconify()
    main_window.withdraw()

def f10(): 								# back button ka function
    main_window.deiconify()
    charts_window.withdraw()

# data extraction for quote
try:

	wa= "https://www.wow4u.com/quote-of-the-day/"
	res = requests.get(wa) 
	#print (res)

	data = bs4.BeautifulSoup(res.text, "html.parser") 
	#print (data)

	info = data.find("img")
	#print(info)

# get the text

	quote = info["alt"]
	#print(type(quote))
	print("Quote : ", quote)
	#print(type(quote))
except Exception as e:
    print("Issue :  ", e)

# main window
main_window = Tk()
main_window.title("E. M. S")
main_window.geometry("700x700+100+100")
main_window['bg'] = 'light green'

f = ("Segoe Print", 16, "bold italic")
fo1 = ("Segoe Print", 12, "bold")
mw_btn_add = Button(main_window, text="Add", font=f, width=10, command=f1)
mw_btn_view = Button(main_window, text="View", font=f, width=10, command=f3)
mw_btn_update = Button(main_window, text="Update",
                       font=f, width=10, command=f5)
mw_btn_delete = Button(main_window, text="Delete",
                       font=f, width=10, command=f7)
mw_btn_charts = Button(main_window, text="Charts",
                       font=f, width=10, command=f9)
mw_lbl_qotd = Label(main_window, text="Quote of the Day : ", font=fo1)
mw_lbl_quote = Label(main_window,text=quote, wraplength=450,font=fo1)

mw_btn_add.pack(pady=10)
mw_btn_view.pack(pady=10)
mw_btn_update.pack(pady=10)
mw_btn_delete.pack(pady=10)
mw_btn_charts.pack(pady=10)
mw_lbl_qotd.pack(pady=10)
mw_lbl_quote.pack(pady=10)

# add employee
add_window = Toplevel(main_window)
add_window.title("Add Employee")
add_window.geometry("700x550+100+100")
add_window['bg'] = 'light blue'

aw_lbl_id = Label(add_window, text="Enter id : ", font=f)
aw_ent_id = Entry(add_window, font=f, bd=4)
aw_lbl_name = Label(add_window, text="Enter name : ", font=f)
aw_ent_name = Entry(add_window, font=f, bd=4)
aw_lbl_sal = Label(add_window, text="Enter salary : ", font=f)
aw_ent_sal = Entry(add_window, font=f, bd=4)
aw_btn_save = Button(add_window, text="Save", font=f, width=10, command=add)
aw_btn_back = Button(add_window, text="Back", font=f, width=10, command=f2)

aw_lbl_id.pack(pady=5)
aw_ent_id.pack(pady=5)
aw_lbl_name.pack(pady=5)
aw_ent_name.pack(pady=5)
aw_lbl_sal.pack(pady=5)
aw_ent_sal.pack(pady=5)
aw_btn_save.pack(pady=5)
aw_btn_back.pack(pady=5)

add_window.withdraw()

# view window

view_window = Toplevel(main_window)
view_window.title("View Employee")
view_window.geometry("700x550+100+100")
view_window['bg'] = 'light yellow'

vw_st_data = ScrolledText(view_window, width=40, height=10, font=f)
vw_btn_back = Button(view_window, text="Back", font=f, command=f4)
vw_st_data.pack(pady=10)
vw_btn_back.pack(pady=10)

view_window.withdraw()

# update window

update_window = Toplevel(main_window)
update_window.title("Update Window")
update_window.geometry("700x550+100+100")
update_window['bg'] = 'light coral'

uw_lbl_id = Label(update_window, text="Enter id : ", font=f)
uw_ent_id = Entry(update_window, font=f, bd=4)
uw_lbl_name = Label(update_window, text="Enter name : ", font=f)
uw_ent_name = Entry(update_window, font=f, bd=4)
uw_lbl_sal = Label(update_window, text="Enter salary : ", font=f)
uw_ent_sal = Entry(update_window, font=f, bd=4)
uw_btn_update = Button(update_window, text="Update",
                     font=f, width=10, command=update)
uw_btn_back = Button(update_window, text="Back", font=f, width=10, command=f6)

uw_lbl_id.pack(pady=5)
uw_ent_id.pack(pady=5)
uw_lbl_name.pack(pady=5)
uw_ent_name.pack(pady=5)
uw_lbl_sal.pack(pady=5)
uw_ent_sal.pack(pady=5)
uw_btn_update.pack(pady=5)
uw_btn_back.pack(pady=5)

update_window.withdraw()

# delete window

delete_window = Toplevel(main_window)
delete_window.title("Delete Employee")
delete_window.geometry("700x550+100+100")
delete_window['bg'] = 'medium purple'

dw_lbl_id = Label(delete_window, text="Enter id : ", font=f)
dw_ent_id = Entry(delete_window, font=f, bd=4)

dw_btn_delete = Button(delete_window, text="Delete",
                     font=f, width=10, command=delete)
dw_btn_back = Button(delete_window, text="Back", font=f, width=10, command=f8)

dw_lbl_id.pack(pady=5)
dw_ent_id.pack(pady=5)
dw_btn_delete.pack(pady=5)
dw_btn_back.pack(pady=5)

delete_window.withdraw()

# charts window

charts_window = Toplevel(main_window)
charts_window.title("Charts")
charts_window.geometry("700x550+100+100")
charts_window['bg'] = 'blanched almond'

cw_btn_view = Button(charts_window, text="View",
                     font=f, width=10, command=charts)
cw_btn_back = Button(charts_window, text="Back", font=f, width=10, command=f10)

cw_btn_view.pack(pady=15)
cw_btn_back.pack(pady=15)

charts_window.withdraw()


def close():
    if askyesno("Quit", "Do you really want to quit???"):
        main_window.destroy()


main_window.protocol("WM_DELETE_WINDOW", close)
main_window.mainloop()
