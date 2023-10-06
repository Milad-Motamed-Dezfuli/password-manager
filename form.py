from tkinter import CENTER,Tk, Label , Button ,Entry ,Frame , END ,Toplevel
from tkinter import ttk
from sqlpart import DbOperations
from hashlib import sha256

import customtkinter
from customtkinter import StringVar

def encrypt_password(raw_pass):
    return sha256(raw_pass)


# form Cutomtk


class reg_window:
    def __init__(self,root,db):
        self.db=db
        self.registration=False
        self.root= root
        self.root.title("Register")
        self.root.geometry("500x350")   

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")

        self.pass1=StringVar()
        self.pass2=StringVar()

        def register():
            if self.pass1.get()==self.pass2.get():
                maspas = sha256(self.pass1.get().encode('utf-8'))
                self.db.record_masterpass(maspas.hexdigest())
                self.registration=True
                self.root.after(500,self.root.destroy) 


        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20 , padx=60 , fill="both" , expand=True)

        label= customtkinter.CTkLabel(master=frame , text="Enter Master Password Twice", font=("Ariel",24))
        label.pack(pady=12 , padx=10)

        entery1= customtkinter.CTkEntry(master=frame ,textvariable=self.pass1, placeholder_text="Enter Master password",show="*")
        entery1.pack(pady=12 , padx=10)

        entery2= customtkinter.CTkEntry(master=frame ,textvariable=self.pass2, placeholder_text="Enter password again",show="*")
        entery2.pack(pady=12 , padx=10)

        button = customtkinter.CTkButton(master=frame , text="Register" ,command=register)
        button.pack(pady=12 , padx=10)

        # checkbox = customtkinter.CTkCheckBox(master=frame , text="Remember me")
        # checkbox.pack(pady=12 , padx=10)

 



class login_window:
    def __init__(self,root,db):
        self.db=db
        self.login= False
        self.root= root
        self.root.title("login")
        self.root.geometry("500x350")   

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        pass1=StringVar()

        def get_pass():
            recs = self.db.get_masterpass()
            curpass = (sha256(pass1.get().encode('utf-8')).hexdigest(),)
            if curpass in recs:
                self.login= True
                self.root.after(500,self.root.destroy) 
            # else:
            #     print("WTF")

        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20 , padx=60 , fill="both" , expand=True)

        label= customtkinter.CTkLabel(master=frame , text="login system", font=("Ariel",24))
        label.pack(pady=12 , padx=10)

        entery1= customtkinter.CTkEntry(master=frame ,textvariable=pass1, placeholder_text="Enter Master password",show="*")
        entery1.pack(pady=12 , padx=10)

        button = customtkinter.CTkButton(master=frame , text="login" ,command=get_pass)
        button.pack(pady=12 , padx=10)





class root_window:
    def __init__(self,root, db):
        self.db=db
        self.root= root
        self.root.title("Password Manager")
        self.root.geometry("900x600+40+40")
        self.root.configure(bg='dark grey')        
        head_title= Label(self.root, text="Password Manager  by Milad.m.d",width=40,bg="Coral", font=("Courier new ", 20,), padx=10 , pady=10 ,justify="center" ,anchor="center").grid(columnspan=4,padx=140, pady=30 )
        
        
        self.crud_frame= Frame(self.root, highlightbackground='black',highlightthickness=1,padx=10,pady=30 )
        self.crud_frame.grid()
        self.create_entery_labels()
        self.create_entery_boxes()
        self.create_crub_buttons()
        
        # self.search_entry= Entry(self.crud_frame,width=20,font=('Ariel',12))
        # self.search_entry.grid(row=self.row_no,column=self.col_no)
        # Button(self.crud_frame, text='Search',bg='yellow',font=("Ariel",12),width=20).grid(row=self.row_no , column=self.col_no+1,padx=5,pady=25)
   
        self.create_records_tree()
        
    def create_entery_labels(self):
        self.col_no , self.row_no=0 , 0
        labels_info=('ID','Website' , 'Username' ,'Password')
        for Label_info in labels_info:
            Label(self.crud_frame, text=Label_info ,bg='grey' , fg='white' , font=('Ariel',12),padx=5 , pady=2).grid(row=self.row_no ,column=self.col_no ,  padx=5 , pady=2)
            self.col_no +=1
        
    def create_crub_buttons(self):
        self.row_no+=1
        self.col_no=0
        Buttons_info=(('save',"green",self.save_record),('update','blue',self.update_record),('delete','red',self.delete_record),('copy password','violet',self.copy_password),("Show Records","purple",self.show_records))  
        for btn_info in Buttons_info:
            if btn_info[0]=="Show Records":
                self.row_no+=1
                self.col_no=0
                
            Button(self.crud_frame, text=btn_info[0] ,bg=btn_info[1] , fg='white' , font=('Ariel',12),padx=2 , pady=1,width=20,command=btn_info[2] ).grid(row=self.row_no ,column=self.col_no ,  padx=5 , pady=10)
            self.col_no +=1
        
    def create_entery_boxes(self):
            self.row_no +=1
            self.entery_boxes= []
            self.col_no = 0
            for i in  range(4):
                show=""
                if i== 3:
                    show="*"
                entry_box= Entry(self.crud_frame,width=20 , background= 'lightgrey',font=("Ariel",12),show=show)
                entry_box.grid(row=self.row_no , column=self.col_no , padx=5, pady=2)
                self.col_no+=1
                self.entery_boxes.append(entry_box)

# Crud Functions
    def save_record(self):
        website= self.entery_boxes[1].get()
        username= self.entery_boxes[2].get()
        password= self.entery_boxes[3].get()
        data={ 'website': website,'username':username, 'password':password}
        self.db.create_record(data)
        self.show_records()

    
    
    def update_record(self):
        ID = self.entery_boxes[0].get()
        website= self.entery_boxes[1].get()
        username= self.entery_boxes[2].get()
        password= self.entery_boxes[3].get()
        data={ 'ID':ID , 'website': website,'username':username, 'password':password}
        self.db.update_record(data)
        self.show_records()
        
        
    def delete_record(self):
        ID = self.entery_boxes[0].get()
        self.db.delete_record(ID)
        self.show_records()

    
    def show_records(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        records_list= self.db.show_records()
        for record in records_list:
            self.records_tree.insert('',END, values=(record[0],record[3],record[4],record[5]))
            
    def create_records_tree(self):
        columns = ('ID', 'Website', 'Username', 'Password')
        self.records_tree=ttk.Treeview(self.root,column=columns,show='headings')
        self.records_tree.heading('ID',text='ID')
        self.records_tree.heading('Website',text='Website name')
        self.records_tree.heading('Username',text='Username')
        self.records_tree.heading('Password',text='Password')
        self.records_tree['displaycolumns']=('Website','Username')

        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item=self.records_tree.item(selected_item)
                record= item['values']
                for entry_box , item in zip(self.entery_boxes , record):
                    entry_box.delete(0 , END)
                    entry_box.insert(0 , item)
        
        self.records_tree.bind('<<TreeviewSelect>>',item_selected)


        self.records_tree.grid()
    #copy to clipboard
    def copy_password(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.entery_boxes[3].get())
        message= "Password Copied"
        title= "copy"
        if self.entery_boxes[3].get()=="":
            message="box is empty"
            title="Error"
        self.showmessage(title, message)
        
    def showmessage(self,title_box:str=None, message:str=None):
        TIME_TO_WAIT= 900 
        root=Toplevel(self.root)
        background='green'
        if title_box== 'Error':
            background='red'
        root.geometry('200x30+600+200')
        root.title(title_box)
        Label(root,text=message,background=background,font=("Ariel",15),fg='white').pack(padx=4,pady=2)
        try:
            root.after(TIME_TO_WAIT,root.destroy)
        except Exception as e:
            print("Error occured", e)
