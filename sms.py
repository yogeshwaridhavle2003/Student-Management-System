from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import pymysql
import pandas


def iexit():
    result=messagebox.askyesno('Confirm','Do yoy want to exits?')
    if result:
        root.destroy()
    else:
        pass


def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studentTable.get_children()
    newlist=[]
    for index in indexing:
        content=studentTable.item(index)
        datalist=content['values']
        newlist.append(datalist)

    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile','Email','Address','Gender','DOB','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Sucess','Data is saved Successfully')

def update_student():
    def update_data():
        if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
            messagebox.showerror('Error', 'All Fields are required', parent=update_window)
        else:
            try:
                query = '''
                UPDATE student 
                SET name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date_added=%s, time_added=%s 
                WHERE id=%s
                '''
                mycursor.execute(query, (nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), date, currenttime, idEntry.get()))
                con.commit()
                messagebox.showinfo('Success', f'Id {idEntry.get()} is modified successfully', parent=update_window)
                update_window.destroy()
                show_student()
            except pymysql.Error as e:
                messagebox.showerror('Error', f'Error: {str(e)}', parent=update_window)

    update_window = Toplevel()
    update_window.title('Update Student')
    update_window.grab_set()
    update_window.resizable(False, False)

    fields = ['Id', 'Name', 'Phone', 'Email', 'Address', 'Gender', 'D.O.B']
    entries = {}

    for idx, field in enumerate(fields):
        label = Label(update_window, text=field, font=('times new roman', 20, 'bold'))
        label.grid(row=idx, column=0, padx=30, pady=15, sticky=W)
        entry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
        entry.grid(row=idx, column=1, pady=15, padx=10)
        entries[field] = entry

    idEntry = entries['Id']
    nameEntry = entries['Name']
    phoneEntry = entries['Phone']
    emailEntry = entries['Email']
    addressEntry = entries['Address']
    genderEntry = entries['Gender']
    dobEntry = entries['D.O.B']

    update_student_button = ttk.Button(update_window, text='UPDATE', command=update_data)
    update_student_button.grid(row=len(fields), columnspan=2, pady=15)

    indexing = studentTable.focus()
    
    if indexing:
        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])
    else:
        messagebox.showwarning('Warning', 'No student selected for update', parent=update_window)
        update_window.destroy()






def show_student():
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)



def delete_student():
    indexing = studentTable.focus()
    if not indexing:  # Check if there's a selected item
        messagebox.showwarning('Warning', 'No student selected to delete')
        return
    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'DELETE FROM student WHERE id=%s'
    try:
        mycursor.execute(query, (content_id,))
        con.commit()
        messagebox.showinfo('Deleted', f'Id {content_id} deleted successfully')
    except pymysql.Error as e:
        messagebox.showerror('Error', f'Error: {str(e)}')
    refresh_student_table()

def refresh_student_table():
    query = 'SELECT * FROM student'
    try:
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('', 'end', values=data)
    except pymysql.Error as e:
        messagebox.showerror('Error', f'Error: {str(e)}')











def search_student():
    def search_data():
        query = '''
        SELECT * FROM student 
        WHERE id=%s OR name=%s OR email=%s OR mobile=%s OR address=%s OR gender=%s OR dob=%s
        '''
        values = (idEntry.get(), nameEntry.get(), emailEntry.get(), phoneEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get())
        try:
            mycursor.execute(query, values)
            studentTable.delete(*studentTable.get_children())
            fetched_data = mycursor.fetchall()
            for data in fetched_data:
                studentTable.insert('', END, values=data)
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error: {str(e)}', parent=search_window)

    search_window = Toplevel()
    search_window.title('Search Student')
    search_window.grab_set()
    search_window.resizable(False, False)

    fields = ['Id', 'Name', 'Phone', 'Email', 'Address', 'Gender', 'D.O.B']
    entries = {}

    for idx, field in enumerate(fields):
        label = Label(search_window, text=field, font=('times new roman', 20, 'bold'))
        label.grid(row=idx, column=0, padx=30, pady=15, sticky=W)
        entry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
        entry.grid(row=idx, column=1, pady=15, padx=10)
        entries[field] = entry

    idEntry = entries['Id']
    nameEntry = entries['Name']
    phoneEntry = entries['Phone']
    emailEntry = entries['Email']
    addressEntry = entries['Address']
    genderEntry = entries['Gender']
    dobEntry = entries['D.O.B']

    search_student_button = ttk.Button(search_window, text='SEARCH', command=search_data)
    search_student_button.grid(row=len(fields), columnspan=2, pady=15)


 

def add_student():
    def add_data():
        if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
            messagebox.showerror('Error', 'All Fields are required', parent=add_window)
        else:
            try:
                currentdate = time.strftime('%d/%m/%Y')
                currenttime = time.strftime('%H:%M:%S')
                query = 'INSERT INTO student (id, name, mobile, email, address, gender, dob, date_added, time_added) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                values = (idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), currentdate, currenttime)
                mycursor.execute(query, values)
                con.commit()
                result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clear the form?', parent=add_window)
                if result:
                    # Clear the form
                    idEntry.delete(0, END)
                    nameEntry.delete(0, END)
                    phoneEntry.delete(0, END)
                    emailEntry.delete(0, END)
                    addressEntry.delete(0, END)
                    genderEntry.delete(0, END)
                    dobEntry.delete(0, END)


                    
                query='select *from student'
                mycursor.execute(query)
                fetched_data=mycursor.fetchall()
                print(fetched_data)
                studentTable.delete(*studentTable.get_children())

                for data in fetched_data:
                    
                    studentTable.insert('',END,values=data)

            except pymysql.Error as e:
                messagebox.showerror('Error', f'Error: {str(e)}', parent=add_window)





            

    add_window=Toplevel()
    add_window.grab_set()
    add_window.resizable(False,False)

    idLabel=Label(add_window,text='Id',font=('times new roman',20,'bold'))
    idLabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    idEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    idEntry.grid(row=0,column=1,pady=15,padx=10)

    
    nameLabel=Label(add_window,text='Name',font=('times new roman',20,'bold'))
    nameLabel.grid(row=1,column=0,padx=30,pady=15,sticky=W)
    nameEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    nameEntry.grid(row=1,column=1,pady=15,padx=10)

    
    phoneLabel=Label(add_window,text='Phone',font=('times new roman',20,'bold'))
    phoneLabel.grid(row=2,column=0,padx=30,pady=15,sticky=W)
    phoneEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    phoneEntry.grid(row=2,column=1,pady=15,padx=10)

    
    emailLabel=Label(add_window,text='Email',font=('times new roman',20,'bold'))
    emailLabel.grid(row=3,column=0,padx=30,pady=15,sticky=W)
    emailEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    emailEntry.grid(row=3,column=1,pady=15,padx=10)

    
    addressLabel=Label(add_window,text='Address',font=('times new roman',20,'bold'))
    addressLabel.grid(row=4,column=0,padx=30,pady=15,sticky=W)
    addressEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    addressEntry.grid(row=4,column=1,pady=15,padx=10)

    
    genderLabel=Label(add_window,text='Gender',font=('times new roman',20,'bold'))
    genderLabel.grid(row=5,column=0,padx=30,pady=15,sticky=W)
    genderEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    genderEntry.grid(row=5,column=1,pady=15,padx=10)

    
    dobLabel=Label(add_window,text='D.O.B',font=('times new roman',20,'bold'))
    dobLabel.grid(row=6,column=0,padx=30,pady=15,sticky=W)
    dobEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    dobEntry.grid(row=6,column=1,pady=15,padx=10)


    add_student_button=ttk.Button(add_window,text='ADD STUDENT',command=add_data)
    add_student_button.grid(row=7,columnspan=2,pady=15)




def connect_database():
    def connect():
        global mycursor,con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=userEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()

            # Create database if it doesn't exist
            query_create_db = 'CREATE DATABASE IF NOT EXISTS studentmanagementsystem'
            mycursor.execute(query_create_db)

            # Switch to the created database
            query_use_db = 'USE studentmanagementsystem'
            mycursor.execute(query_use_db)

            # Create 'student' table if it doesn't exist
            query_create_table = '''
            CREATE TABLE IF NOT EXISTS student (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(30),
                mobile VARCHAR(10),
                email VARCHAR(30),
                address VARCHAR(100),
                gender VARCHAR(20),
                dob VARCHAR(20),
                date_added VARCHAR(50),
                time_added VARCHAR(50)
            )
            '''
            mycursor.execute(query_create_table)

            messagebox.showinfo('Success', 'Database Connection and Setup Successful', parent=connectWindow)

            connectWindow.destroy()

        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error: {str(e)}', parent=connectWindow)


        finally:
            if 'con' in locals():
                con.close()


        
            addstudentButton.config(state=NORMAL)
            searchstudentButton.config(state=NORMAL)
            showstudentButton.config(state=NORMAL)
            updatestudentButton.config(state=NORMAL)
            deletestudentButton.config(state=NORMAL)
            exportstudentButton.config(state=NORMAL)

             
             



    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)


    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)


    
    usernameLabel=Label(connectWindow,text='User Name',font=('arial',20,'bold'))
    usernameLabel.grid(row=1,column=0,padx=20)

    
    userEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    userEntry.grid(row=1,column=1,padx=40,pady=20)


    
    passwordLabel=Label(connectWindow,text='Password',font=('arial',20,'bold'))
    passwordLabel.grid(row=2,column=0,padx=20)


    
    passwordEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    passwordEntry.grid(row=2,column=1,padx=40,pady=20)


    connectButton=ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2)

count=0
text=''

def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)

def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    dattimeLabel.config(text=f'    Date: {date}\n Time: {currenttime}')
    dattimeLabel.after(1000,clock)


root=ttkthemes.ThemedTk()


root.get_themes()

root.set_theme('radiance')

root.geometry('1174x680+0+0')
root.resizable(0,0)
root.title('Student Management System')


dattimeLabel=Label(root,font=('times new roman',18,'bold'))
dattimeLabel.place(x=5,y=5)
clock()

s='Student Management System'
sliderLabel=Label(root,font=('arial',28,'italic bold'),width=30)
sliderLabel.place(x=200,y=0)
slider()


connectButton=ttk.Button(root,text='Connect database',command=connect_database)
connectButton.place(x=980,y=0)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

logo_image=PhotoImage(file='studentt.png')
logo_label=Label(leftFrame,image=logo_image)
logo_label.grid(row=0,column=0)


addstudentButton=ttk.Button(leftFrame,text='Add Student',width=25,state=DISABLED,command=add_student)
addstudentButton.grid(row=1,column=0,pady=20)

searchstudentButton=ttk.Button(leftFrame,text='Search Student',width=25,state=DISABLED,command=search_student)
searchstudentButton.grid(row=2,column=0,pady=20)

deletestudentButton=ttk.Button(leftFrame,text='Delete Student',width=25,state=DISABLED,command=delete_student)
deletestudentButton.grid(row=3,column=0,pady=20)

updatestudentButton=ttk.Button(leftFrame,text='Update Student',width=25,state=DISABLED,command=update_student)
updatestudentButton.grid(row=4,column=0,pady=20)

showstudentButton=ttk.Button(leftFrame,text='Show Student',width=25,state=DISABLED,command=show_student)
showstudentButton.grid(row=5,column=0,pady=20)

exportstudentButton=ttk.Button(leftFrame,text='Export Data',width=25,state=DISABLED,command=export_data)
exportstudentButton.grid(row=6,column=0,pady=20)

exitstudentButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitstudentButton.grid(row=7,column=0,pady=20)



rightFrame=Frame(root)
rightFrame.place(x=350,y=80,width=820,height=600)


ScrollbarX=Scrollbar(rightFrame,orient=HORIZONTAL)
ScrollbarY=Scrollbar(rightFrame,orient=VERTICAL)

studentTable=ttk.Treeview(rightFrame,columns=('Id','Name','Mobile','Email','Address','Gender','D.O.B','Added Date','Added Time'),xscrollcommand=ScrollbarX.set,yscrollcommand=ScrollbarY.set)
ScrollbarX.config(command=studentTable.xview)
ScrollbarY.config(command=studentTable.yview)

ScrollbarX.pack(side=BOTTOM,fill=X)
ScrollbarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=1)



studentTable.heading('Id',text='Id')
studentTable.heading('Name',text='Name')
studentTable.heading('Mobile',text='Mobile No')
studentTable.heading('Email',text='Email Address')
studentTable.heading('Address',text='Address')
studentTable.heading('Gender',text='Gender')
studentTable.heading('D.O.B',text='D.O.B')
studentTable.heading('Added Date',text='Added Date')
studentTable.heading('Added Time',text='Added Time')


studentTable.column('Id',width=50,anchor=CENTER)
studentTable.column('Name',width=300,anchor=CENTER)
studentTable.column('Mobile',width=300,anchor=CENTER)
studentTable.column('Email',width=200,anchor=CENTER)
studentTable.column('Address',width=300,anchor=CENTER)
studentTable.column('Gender',width=100,anchor=CENTER)
studentTable.column('D.O.B',width=100,anchor=CENTER)
studentTable.column('Added Date',width=200,anchor=CENTER)
studentTable.column('Added Time',width=200,anchor=CENTER)


style=ttk.Style()
style.configure('Treeview',rowheight=40,font=('arial',12,'bold'),background='white',fieldbackground='white')
style.configure('Treeview.Heading',font=('arial',14,'bold'),foreground='red')





studentTable.config(show='headings')

root.mainloop()