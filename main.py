from sqlpart import DbOperations
import customtkinter
from form import *

if __name__=="__main__" :
    # create table if doesn't exist
    db_class= DbOperations()
    db_class.create_table("pass_info")
    db_class.create_user_table()
    # create tkinter window


    h=db_class.get_masterpass()
    if h==[]:
        # if there is master passwords open this panel
        root= customtkinter.CTk()
        registerwindow=reg_window(root,db_class)
        root.mainloop()

    h=db_class.get_masterpass()
    if h!=[]:
        root= customtkinter.CTk()
        loginpage=login_window(root,db_class)
        root.mainloop()

        if loginpage.login:
            root= Tk()
            root_class = root_window(root, db_class)
            root.mainloop()
