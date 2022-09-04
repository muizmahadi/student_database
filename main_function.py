import sqlite3
from tkinter import *
from tkinter.ttk import Treeview
from tkinter.messagebox import showinfo

dept_list=['manu', 'cie', 'com', 'mech', 'mat', 'civ', 'bio', 'auto', 'aero']



#Method that gives name of students whom age more than selected value by user
def get_list(connection):
    my_cursor=connection.cursor()
    my_cursor.execute('''SELECT * from student''')
    record=my_cursor.fetchall()
    return record

def  display_list(window3,):
    display=Toplevel(window3)
    display.config(padx=100,pady=100)
    tree=Treeview(display,column=("c1","c2","c3"),show="headings")
    tree.heading("c1",text="name")
    tree.heading("c2",text="age")
    tree.column("c2",anchor=CENTER)
    tree.heading("c3",text="dept")
    tree.column("c3",anchor=CENTER)
    
    with sqlite3.connect("db_student.sqlite") as connection:
        record=get_list(connection)
    for row in record:
            tree.insert("",END,values=(row[0],row[1],row[2]))
    tree.pack()
    display.mainloop()
    

def ask_list(connection,age):
    my_cursor=connection.cursor()
    name_list= my_cursor.execute(f'''select name from student where age >=:age''',{'age':age})
    result = name_list.fetchall()
    return result

#Method that gives name of students in selected programme, selected by user
def get_programme (connection,programme:str):
    # programme = programme+'\n'24
    my_cursor = connection.cursor()
    name_list =my_cursor.execute('select name from student where dept =:programme', {"programme" : programme})
    return (name_list.fetchall())

#Method that insert new students data,that was input by user
def get_new(connection,name,age,dept):
    my_cursor = connection.cursor()
    my_cursor.execute('insert into student values (?,?,?)',(name,age,dept))
    connection.commit()

#
def del_data(connection,name_del):
    my_cursor = connection.cursor()
    my_cursor.execute('delete from student where name =:name',{'name':name_del})
    connection.commit()

# ------------------------------gui main-----------------------------------------------------------------------------------------------------#
def gui_main():
    window=Tk()
    window.config(padx=100, pady=100)
    

    button1=Button(text="View students which age more than your choice (max=25)",command=lambda:gui_option_1(window,button1), width=50)
    button1.pack()

    button2=Button(window,text="View students from specific department",command=lambda:gui_option_2(window,button2), width=50)
    button2.pack()

    button3=Button(window,text="Add and remove new students",command=lambda:gui_option_3(), width=50)
    button3.pack()

    

    window.mainloop()


def close(button,window):
    button.config(state=NORMAL)
    window.destroy()


#-----------------------------------------------option 1 window-------------------------------------------------------------#

def gui_option_1(window,button1):
    
    button1.config(state=DISABLED)
    window1=Toplevel(window)
    window1.config(padx=100, pady=100)
    label=Label(window1,text="Age ? : ").pack()
    age=Entry(window1)
    age.pack()
    button=Button(window1,text="submit", command=lambda:output_option_1(age, window1))
    button.pack()
    window1.protocol("WM_DELETE_WINDOW",lambda:close(button1,window1))
    window1.mainloop()

#new window to display answer for option 1
def output_option_1(age:Entry, window1) :
    output_option_1=Toplevel(window1)
    output_option_1.config(padx=80, pady=80)
    age_input=age.get()
    with sqlite3.connect("db_student.sqlite") as connection:
        student_list= ask_list(connection,age_input)
        students=[student[0] for student in student_list]
    columns=("Num","Name")
    
    tree=Treeview(output_option_1,columns=columns,show="headings")
    
    tree.heading("Num",text="Index")
    tree.column("Num",anchor=CENTER)
    tree.heading("Name",text="Name")
    
    
    student_label=[]
    counter=1
    for student in students:
        
        student_temp=student.replace(" ","\ ")#for capturing string after space
        student_label.append(f"{counter} {student_temp}")
        counter+=1 
    
    for data in student_label:
        tree.insert("",END,values=data)
        
    tree.grid(row=0,column=0,sticky="nsew")

    scrollbar=Scrollbar(output_option_1,orient=VERTICAL,command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0,column=1,sticky="ns")
    

    output_option_1.mainloop()


#------------------------------------------------------option 2 window--------------------------------------------#

def gui_option_2(window,button2):
    button2.config(state=DISABLED)
    window2=Toplevel(window)
    window2.config(padx=100,pady=100)
    counter=1

    value_inside=StringVar(window2)
    value_inside.set("Select programme you wish to see")

    q_menu=OptionMenu(window2,value_inside,*dept_list)
    q_menu.pack()
    
    def ans():
        dept=value_inside.get()
        return dept
    
    button=Button(window2,text="submit",command=lambda:output_option_2(ans(),window2))
    button.pack()
    window2.protocol("WM_DELETE_WINDOW",lambda:close(button2,window2))
    window2.mainloop()

#new window to display output for option 2
def output_option_2(dept,window2):
    
    option2=Toplevel(window2)
    option2.config(padx=100,pady=100)
    with sqlite3.connect("db_student.sqlite") as connection:
        name_list=get_programme(connection,dept)
        name=[names[0] for names in name_list]
        counter =1
        for list in name:
            label=Label(option2,text=f"{counter}. {list}")
            label.pack()
            counter+=1
    

#------------------------------------------------------------------option 3 window------------------------------------------#   
def gui_option_3():
    with sqlite3.connect("db_student.sqlite") as connection:
        window3=Tk()
        window3.config(padx=100,pady=100)
        
    tree=Treeview(window3,column=("c1","c2","c3"),show="headings")
    tree.heading("c1",text="name")
    tree.heading("c2",text="age")
    tree.column("c2",anchor=CENTER)
    tree.heading("c3",text="dept")
    tree.column("c3",anchor=CENTER)
    
    with sqlite3.connect("db_student.sqlite") as connection:
        record=get_list(connection)
    for row in record:
            tree.insert("",END,values=(row[0],row[1],row[2]))
    tree.pack()
    

        
    # button=Button(window3,text="Display list",width=10,command=lambda:display_list(window3))
    # button.pack()
    button=Button(window3,text="Add student",command=lambda:option3(window3, tree),width=10)
    button.pack()
    button=Button(window3,text="delete student",command=lambda:option4(tree),width=10)
    button.pack()
    window3.mainloop()

    #
def option3(window3, tree):
    option3=Toplevel(window3)
    option3.config(padx=100,pady=100)

    t1=Entry(option3)
    t1.pack()
    t2=Entry(option3)
    t2.pack()
    t3=Entry(option3)
    t3.pack()

    
    def add_data(t1:Entry,t2:Entry,t3:Entry):
        with sqlite3.connect("db_student.sqlite") as connection:
            name=t1.get()
            age=t2.get()
            dept=t3.get()
            get_new(connection,name,age,dept)
            connection.commit()
        tree.insert("",END,values=(name,age,dept))

    button=Button(option3,text="Add student",command=lambda:add_data(t1,t2,t3),width=10)
    button.pack()
    option3.mainloop()
     
def option4(tree:Treeview):
    selected=tree.selection()
    name_del=tree.item(selected)['values'][0]
    tree.delete(selected)
    with sqlite3.connect ("db_student.sqlite") as connection:    
        del_data(connection,name_del)
        
    
#
def main():

    with sqlite3.connect("db_student.sqlite") as connection:
        print ('Press 1 to view students which age more than your choice,max=25')
        print ('Press 2 to view students from specific department')
        print ('Press 3 to add new students ')
        print ('Press 4 to remove students ')
        ans = int(input('What would you like to do ?: '))

        if ans== 1:
            age=input("age? :")
            student_list= ask_list(connection,age)
            list(map(print,student_list))
        
        elif ans == 2:
            for i in dept_list:
                print(f"Department :{i}")
            programme=input("what programme? (Refer to the top department list) : ")
            get_programme(connection,programme)
        
        elif ans == 3:
            name = input("Name : ")
            age = input("Age : ")
            dept = input(f"Department, as included in here {dept_list} : ")
            get_new(connection,name,age,dept)

        elif ans == 4:
            with open("new_name_student.txt") as text_file:
                name_list = text_file.readlines()
            for sub_text in name_list:
                print(sub_text)
            name_del = input("Whose name do you want to delete : ")
            del_data(connection,name_del)
        
        else:
            print("System Invalid")

gui_main()

     