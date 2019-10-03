from tkinter import *
import pymysql
from tkinter import messagebox
from tkinter import ttk
import re
import time
import hashlib
import datetime

class AtlantaBeltline:
    def __init__(self):
        # Invoke createLoginWindow; Invoke buildLoginWindow, Set loginWindow as mainloop
        #Connect to the database
        self.db = self.connect()
        self.cursor = self.db.cursor()

    #test functionality
        #self.creatRegisterNavigationWindow()
        #self.buildRegisterNavigationWindow(self.registerNavigationWindow)
        #self.registerNavigationWindow.mainloop()
        # Login Window
        self.createLoginWindow()
        self.buildLoginWindow(self.loginWindow)
        self.loginWindow.mainloop()
        #self.result_searchForExhibit_Visitor = []
        #self.tag = 1
        #sys.exit()

#  =======1 Login Window=======
    def createLoginWindow(self):
        # Create blank Login Window
        self.loginWindow = Tk()
        self.loginWindow.title("Atlanta BeltLine")

        self.loginWindow.withdraw()
        self.loginWindow.update_idletasks()  # Update "requested size" from geometry manager
        x = (self.loginWindow.winfo_screenwidth() - self.loginWindow.winfo_reqwidth()) / 2
        y = (self.loginWindow.winfo_screenheight() - self.loginWindow.winfo_reqheight()) / 2
        self.loginWindow.geometry("+%d+%d" % (x, y))
        self.loginWindow.deiconify()
        self.loginWindow.geometry("350x120")

    def buildLoginWindow(self, loginWindow):
        # Add component for Login Window
        # Login Label
        self.tag = 1
        loginLabel = Label(loginWindow, text="Atlanta Beltline Login",font = "Verdana 13 bold ")
        loginLabel.grid(row=1, column=3, sticky=W+E)

        # Username Label
        usernameLabel = Label(loginWindow, text="Email")
        usernameLabel.grid(row=2, column=2, sticky=W)

        # Password Label
        passwordLabel = Label(loginWindow, text="Password")
        passwordLabel.grid(row=4, column=2, sticky=W)

        # Email Entry
        self.loginEmail = StringVar()
        emailAddressEntry = Entry(loginWindow, textvariable=self.loginEmail, width=20)
        emailAddressEntry.grid(row=2, column=3, sticky=W + E)


        # Password Entry
        self.loginPassword = StringVar()
        passwordEntry = Entry(loginWindow, textvariable=self.loginPassword, show = '*', width=20)
        passwordEntry.grid(row=4, column=3, sticky=W + E)

        # Login Buttons
        loginButton = Button(loginWindow, text="Login", command=self.loginWindowLoginButtonClicked)
        loginButton.grid(row=6, column=3)

        # Register Button
        registerButton = Button(loginWindow, text="Register", command=self.loginWindowRegisterButtonClicked)
        registerButton.grid(row=6, column=4, sticky=E)

    def loginWindowLoginButtonClicked(self):
        # Click the button on Login Window:
        # Withdraw Login Window;
        self.loginEmailAddress = self.loginEmail.get()#loginemail not defined
        self.password = self.loginPassword.get()
        # self.passwordNonhash = self.loginPassword.get()
        h = hashlib.md5(self.password.encode())
        self.password = h.hexdigest()
        print(self.password)
        if not self.loginEmailAddress:
            messagebox.showwarning("Email input is empty", "Please enter Email.")
            return False
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        isEmail = self.cursor.execute("SELECT * FROM UserEmail WHERE Email = %s", self.loginEmailAddress)
        if not isEmail:
           messagebox.showwarning("Email is not valid.", "Please enter Email.")
           return False
        useremailAndPasswordMatch = self.cursor.execute(
           "SELECT * FROM (UserEmail JOIN User ON UserEmail.Username=User.Username) WHERE (Email = %s AND Password = %s)", (self.loginEmailAddress, self.password))
        if not useremailAndPasswordMatch:
           messagebox.showwarning("Email and password don\'t match", "Sorry, the Email and password you entered"
                                                                        + " do not match.")
           return False

        isAdminName = self.cursor.execute("SELECT * FROM (Administrator JOIN UserEmail ON Administrator.Username=UserEmail.Username) WHERE  UserEmail.Email = %s", self.loginEmailAddress)
        isVisitorName = self.cursor.execute("SELECT * FROM (Visitor JOIN UserEmail ON Visitor.Username=UserEmail.Username) WHERE  UserEmail.Email = %s", self.loginEmailAddress)
        isStaffName = self.cursor.execute("SELECT * FROM (Staff JOIN UserEmail ON Staff.Username=UserEmail.Username) WHERE  UserEmail.Email = %s", self.loginEmailAddress)
        isManagerName = self.cursor.execute("SELECT * FROM (Manager JOIN UserEmail ON Manager.Username=UserEmail.Username) WHERE  UserEmail.Email = %s", self.loginEmailAddress)

        if isAdminName and isVisitorName:
            print("Yes Admin & Visitor")
            self.cursor.execute("SELECT Username FROM UserEmail WHERE Email = %s", self.loginEmailAddress)
            result = self.cursor.fetchall()
            self.username = result[0]
            self.loginWindow.withdraw()
            self.createAdministratorVisitorFunctionalityWindow()
            self.buildAdministratorVisitorFunctionalityWindow(self.administratorVisitorFunctionalityWindow)
        elif isManagerName and isVisitorName:
            print("Yes Manager & Visitor")
            self.cursor.execute("SELECT Username FROM UserEmail WHERE Email = %s", self.loginEmailAddress)
            result = self.cursor.fetchall()
            self.username = result[0]
            self.loginWindow.withdraw()
            self.createManagerVisitorFunctionalityWindow()
            self.buildManagerVisitorFunctionalityWindow(self.managerVisitorFunctionalityWindow)
        elif isStaffName and isVisitorName:
            print("Yes Staff & Visitor")
            self.cursor.execute("SELECT Username FROM UserEmail WHERE Email = %s", self.loginEmailAddress)
            result = self.cursor.fetchall()
            self.username = result[0]
            self.loginWindow.withdraw()
            self.createStaffVisitorFunctionalityWindow()
            self.buildStaffVisitorFunctionalityWindow(self.staffVisitorFunctionalityWindow)
        elif isAdminName:
            print("Yes Admin")
            self.cursor.execute("SELECT Username FROM UserEmail WHERE Email = %s", self.loginEmailAddress)
            result = self.cursor.fetchall()
            self.username = result[0]
            self.loginWindow.withdraw()
            self.createAdministratorOnlyFunctionalityWindow()
            self.buildAdministratorOnlyFunctionalityWindow(self.administratorOnlyFunctionalityWindow)
        elif isVisitorName:
            print("Hello Visitor")
            self.cursor.execute("SELECT Username FROM UserEmail WHERE Email = %s", self.loginEmailAddress)
            result = self.cursor.fetchall()
            self.username = result[0]
            self.loginWindow.withdraw()
            self.createChooseFunctionalityWindow()
            self.buildChooseFunctionalityWindow(self.chooseFunctionalityWindow)
        elif isStaffName:
            print("Hi Staff")
            self.cursor.execute("SELECT Username FROM UserEmail WHERE Email = %s", self.loginEmailAddress)
            result = self.cursor.fetchall()
            self.username = result[0]
            self.loginWindow.withdraw()
            self.createStaffOnlyFunctionalityWindow()
            self.buildStaffOnlyFunctionalityWindow(self.staffOnlyFunctionalityWindow)
        elif isManagerName:
            print("Yeah Manager")
            self.cursor.execute("SELECT Username FROM UserEmail WHERE Email = %s", self.loginEmailAddress)
            result = self.cursor.fetchall()
            self.username = result[0]
            self.loginWindow.withdraw()
            self.createManagerOnlyFunctionalityWindow()
            self.buildManagerOnlyFunctionalityWindow(self.managerOnlyFunctionalityWindow)
        else:
            print("Hey User")
            self.cursor.execute("SELECT Username FROM UserEmail WHERE Email = %s", self.loginEmailAddress)
            result = self.cursor.fetchall()
            self.username = result[0]
            self.loginWindow.withdraw()
            self.createUserFunctionalityWindow()
            self.buildUserFunctionalityWindow(self.userFunctionalityWindow)
        return True

    def loginWindowRegisterButtonClicked(self):
        # Click button on Login Window:
        # Invoke createNewUserRegistrationWindow; Invoke buildNewUserRegistrationWindow;
        # Hide Login Window; Set newUserRegistrationWindow on the top
        self.creatRegisterNavigationWindow()
        self.buildRegisterNavigationWindow(self.registerNavigationWindow)
        self.loginWindow.withdraw()

#======2 New User Registration Window==============

    def creatRegisterNavigationWindow(self):
        # Create blank newUserRegistrationWindow
        self.registerNavigationWindow = Toplevel()
        self.registerNavigationWindow.title("Atlanta BeltLine")
        self.registerNavigationWindow.geometry("200x300")
        self.loginWindow.withdraw()

    def buildRegisterNavigationWindow(self, registerNavigationWindow):
        # New User Rigestration Label
        registerLabel = Label(registerNavigationWindow, text="Register Navigation", font="Verdana 13 bold ")
        registerLabel.grid(row=1, column=3, sticky=W+E)

        # Create User Only Button
        createButton = Button(registerNavigationWindow, text="User Only", command=self.newUserOnlyCreateButtonClicked)
        createButton.grid(row=2, column=3, sticky=W+E)

        # Create Visitor Only Button
        createButton = Button(registerNavigationWindow, text="Visitor Only", command=self.newVisitorOnlyCreateButtonClicked)
        createButton.grid(row=3, column=3, sticky=W+E)

        # Create Employee Only Button
        createButton = Button(registerNavigationWindow, text="Employee Only",
                              command=self.newEmployeeOnlyCreateButtonClicked)
        createButton.grid(row=4, column=3, sticky=W+E)

        # Create Employee-Visitor Button
        createButton = Button(registerNavigationWindow, text="Employee-Visitor",
                              command=self.newEmployeeVisitorCreateButtonClicked)
        createButton.grid(row=5, column=3, sticky=W+E)

        # Create Back Button
        createButton = Button(registerNavigationWindow, text="Back",
                              command=self.RegisterNavigationBackButtonClicked)
        createButton.grid(row=6, column=3, sticky=W+E)

    def newUserOnlyCreateButtonClicked(self):
        # Click button on Register Navigation Window:
        # Invoke createNewRegisterUserOnlyWindow; Invoke buildNewRegisterUserOnlyWindow;
        # Hide Register Navigation Window; Set newRegisterUserOnlyWindow on the top
        self.createNewRegisterUserOnlyWindow()
        self.buildNewRegisterUserOnlyWindow(self.newRegisterUserOnlyWindow)
        self.registerNavigationWindow.withdraw()

    def newVisitorOnlyCreateButtonClicked(self):
        # Click button on Register Navigation Window:
        # Invoke createNewRegisterUserOnlyWindow; Invoke buildNewRegisterUserOnlyWindow;
        # Hide Register Navigation Window; Set newRegisterUserOnlyWindow on the top
        self.createNewRegisterVisitorOnlyWindow()
        self.buildNewRegisterVisitorOnlyWindow(self.newRegisterVisitorOnlyWindow)
        self.registerNavigationWindow.withdraw()

    def newEmployeeOnlyCreateButtonClicked(self):
        # Click button on Register Navigation Window:
        # Invoke createNewRegisterUserOnlyWindow; Invoke buildNewRegisterUserOnlyWindow;
        # Hide Register Navigation Window; Set newRegisterUserOnlyWindow on the top
        self.createNewRegisterEmployeeOnlyWindow()
        self.buildNewRegisterEmployeeOnlyWindow(self.newRegisterEmployeeOnlyWindow)
        self.registerNavigationWindow.withdraw()

    def newEmployeeVisitorCreateButtonClicked(self):
        # Click button on Register Navigation Window:
        # Invoke createNewRegisterUserOnlyWindow; Invoke buildNewRegisterUserOnlyWindow;
        # Hide Register Navigation Window; Set newRegisterUserOnlyWindow on the top
        self.createNewRegisterEmployeeVisitorWindow()
        self.buildNewRegisterEmployeeVisitorWindow(self.newRegisterEmployeeVisitorWindow)
        self.registerNavigationWindow.withdraw()

    def RegisterNavigationBackButtonClicked(self):
        self.createLoginWindow()
        self.buildLoginWindow(self.loginWindow)
        self.registerNavigationWindow.withdraw()

#======3 register user only==============

    def createNewRegisterUserOnlyWindow(self):
        self.newRegisterUserOnlyWindow = Toplevel()
        self.newRegisterUserOnlyWindow.title("Atlanta BeltLine")
        self.registerNavigationWindow.withdraw()

    def buildNewRegisterUserOnlyWindow(self, newRegisterUserOnlyWindow):
        # New User Only Registration Label
        RegisterUserOnlyLabel = Label(newRegisterUserOnlyWindow, text="Register User",font = "Verdana 13 bold ")
        RegisterUserOnlyLabel.grid(row=1, column=3, sticky=W+E)

        # First Name Label
        firstNameLabel = Label(newRegisterUserOnlyWindow, text="First Name")
        firstNameLabel.grid(row=2, column=1)
        # Last Name Label
        lastNameLabel = Label(newRegisterUserOnlyWindow, text="Last Name")
        lastNameLabel.grid(row=2, column=3, sticky=E)
        # Username Label
        usernameLabel = Label(newRegisterUserOnlyWindow, text="Username")
        usernameLabel.grid(row=3, column=1)
        # Password Label
        passwordLabel = Label(newRegisterUserOnlyWindow, text="Password")
        passwordLabel.grid(row=4, column=1)
        # Confirm Password Label
        confirmPasswordLabel = Label(newRegisterUserOnlyWindow, text="Confirm Password")
        confirmPasswordLabel.grid(row=4, column=3, sticky=E)
        # Email Address Label
        emailLabel = Label(newRegisterUserOnlyWindow, text="Email")
        emailLabel.grid(row=5, column=1)

        # First Name Entry
        self.registrationFirstName = StringVar()
        firstNameEntry = Entry(newRegisterUserOnlyWindow, textvariable=self.registrationFirstName, width=20)
        firstNameEntry.grid(row=2, column=2, sticky=W+E)
        # Last Name Entry
        self.registrationLastName = StringVar()
        lastNameEntry = Entry(newRegisterUserOnlyWindow, textvariable=self.registrationLastName, width=20)
        lastNameEntry.grid(row=2, column=4, sticky=E)
        # Username Entry
        self.registrationUsername = StringVar()
        usernameEntry = Entry(newRegisterUserOnlyWindow, textvariable=self.registrationUsername, width=20)
        usernameEntry.grid(row=3, column=2, sticky=W+E)
        # Password Entry
        self.registrationPassword = StringVar()
        passwordEntry = Entry(newRegisterUserOnlyWindow, textvariable=self.registrationPassword, show='*', width=20)
        passwordEntry.grid(row=4, column=2, sticky=W+E)
        # Confirm Password Entry
        self.registrationConfirmPassword = StringVar()
        confirmPasswordEntry = Entry(newRegisterUserOnlyWindow, textvariable=self.registrationConfirmPassword, show='*',
                                     width=20)
        confirmPasswordEntry.grid(row=4, column=4, sticky=E)
        # Email Address Entry
        # self.registrationEmailAddress = StringVar()
        # emailAddressEntry = Entry(newRegisterUserOnlyWindow, textvariable=self.registrationEmailAddress,width=20)
        # emailAddressEntry.grid(row=5, column=2, sticky=W+E)
        # Email Address Entry
        EntryRow = 5
        Email = []  # can be used to register database
        EmailLabels = []
        removeButton = []
        EmailAddress = StringVar()
        emailAddressEntry = Entry(newRegisterUserOnlyWindow, textvariable=EmailAddress, width=20)

        # reconfigurate
        def reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton):
            for i in range(len(removeButton)):
                removeButton[i].grid(row=5 + i, column=3, sticky=W)
                EmailLabels[i].grid(row=5 + i, column=2, sticky=W)
            self.addButton_newRegisterUserOnlyWindow.destroy()
            self.addButton_newRegisterUserOnlyWindow = Button(newRegisterUserOnlyWindow, text="Add",
                                                              command=lambda: addRow(self, EntryRow, Email, EmailLabels,
                                                                                     removeButton, emailAddressEntry,
                                                                                     EmailAddress, backButton,
                                                                                     registerButton))
            self.addButton_newRegisterUserOnlyWindow.grid(row=EntryRow, column=3, sticky=W)
            emailAddressEntry.grid(row=EntryRow, column=2, sticky=W)
            backButton.grid(row=EntryRow + 1, column=3)
            registerButton.grid(row=EntryRow + 1, column=2)

        def removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton, emailAddressEntry, backButton,
                      registerButton):
            indexToRemove = removeButton.index(temp)
            for i in range(len(Email)):
                removeButton[i].grid_remove()
                removeButton[i].destroy()
                EmailLabels[i].grid_remove()
                EmailLabels[i].destroy()
            del Email[indexToRemove]
            EntryRow = len(Email) + 5
            removeButton = []
            EmailLabels = []
            # addButton.grid_remove()
            # addButton.destroy()
            for i in range(len(Email)):
                temp = Button(newRegisterUserOnlyWindow, text='remove',
                              command=lambda: removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton,
                                                        emailAddressEntry, backButton, registerButton))
                removeButton.append(temp)
                tempEmailLabel = Label(newRegisterUserOnlyWindow, text=Email[i])
                EmailLabels.append(tempEmailLabel)
            # addButton = Button(newRegisterUserOnlyWindow, text="Add", command=lambda: addRow(EntryRow,Email,EmailLabels,removeButton,emailAddressEntry,EmailAddress,addButton,backButton,registerButton))
            reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

        def addRow(self, EntryRow, Email, EmailLabels, removeButton, emailAddressEntry, EmailAddress, backButton,
                   registerButton):
            Email.append(EmailAddress.get())
            EntryRow = EntryRow + 1
            # creat remove button
            temp = Button(newRegisterUserOnlyWindow, text='remove',
                          command=lambda: removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton,
                                                    emailAddressEntry, backButton, registerButton))
            removeButton.append(temp)
            tempEmailLabel = Label(newRegisterUserOnlyWindow, text=EmailAddress.get())
            EmailLabels.append(tempEmailLabel)

            reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

        '''
        我在这里加了一个functioin“resigterButton”，这个function把email这个list以变量的形式传到buttonclick里边
        '''

        def registerButtonClick():
            Email.append(EmailAddress.get())
            self.newRegisterUserOnlyRegisterButtonClicked(Email)

        # Create Add Button
        backButton = Button(newRegisterUserOnlyWindow, text="Back", command=self.registerUserOnlyBackButtonClicked)
        registerButton = Button(newRegisterUserOnlyWindow, text="Register", command=registerButtonClick)
        self.addButton_newRegisterUserOnlyWindow = Button(newRegisterUserOnlyWindow, text="Add",
                                                          command=lambda: addRow(self, EntryRow, Email, EmailLabels,
                                                                                 removeButton, emailAddressEntry,
                                                                                 EmailAddress, backButton,
                                                                                 registerButton))
        reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

    def registerUserOnlyBackButtonClicked(self):
        self.creatRegisterNavigationWindow()
        self.buildRegisterNavigationWindow(self.registerNavigationWindow)
        self.newRegisterUserOnlyWindow.withdraw()

    def newRegisterUserOnlyRegisterButtonClicked(self,Email):
        # Click the Create Button on New User Registration Window:
        # Invoke createChooseFunctionalityWindow; Invoke buildChooseFunctionalityWindow;
        # Destroy New User Registration Window
        self.firstName = self.registrationFirstName.get()
        self.lastName = self.registrationLastName.get()
        self.username = self.registrationUsername.get()
        self.emailAddress = Email
        self.password = self.registrationPassword.get()
        self.confirmPassword = self.registrationConfirmPassword.get()
        if not self.firstName:
            messagebox.showwarning("First name is empty", "Please enter first name.")
            return False
        if not self.lastName:
            messagebox.showwarning("Last name is empty", "Please enter last name.")
            return False
        if not self.username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        if len(self.emailAddress)==0:
            messagebox.showwarning("E-mail input is empty", "Please enter E-mail.")
            return False
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        if len(self.password) < 8:
            messagebox.showwarning("info", "Password must be at least 8 digits")
            return False
        if not self.confirmPassword:
            messagebox.showwarning("Confirm password input is empty", "Please enter confirm password")
            return False

        isUsername = self.cursor.execute("SELECT * FROM User WHERE Username = %s", self.username)
        if isUsername:
           messagebox.showwarning("This username has been used.",
                                  "Please input another username.")
           return False
        for element in self.emailAddress:
            isEmail = self.cursor.execute("SELECT * FROM UserEmail WHERE Email = %s", element)
            if isEmail:
               messagebox.showwarning("This E-mail address has been used.",
                                      "Please input another E-mail address.")
               return False
        if not (self.password == self.confirmPassword):
           messagebox.showwarning("Password does not match the confirm password.",
                                  "Please reconfirm the password.")
           return False

        h1 = hashlib.md5(self.password.encode())
        h2 = hashlib.md5(self.confirmPassword.encode())
        self.password = h1
        self.confirmPassword = h2
        print(h1.hexdigest())
        print(h2.hexdigest())
        print(self.password.hexdigest())
        print(self.confirmPassword.hexdigest())

        email = self.emailAddress

        def myfunction():
            self.cursor.execute("INSERT INTO User VALUES (%s, %s, %s, %s, %s)",
                                (self.username, self.password.hexdigest(), self.firstName, self.lastName, "Pending"))
            self.db.commit()
            for i in range(len(self.emailAddress)):
                self.cursor.execute("INSERT INTO UserEmail VALUES (%s, %s)", (self.username, self.emailAddress[i]))
                self.db.commit()
            messagebox.showinfo("info", "Register User successfully!")
            self.createLoginWindow()
            self.buildLoginWindow(self.loginWindow)
            self.newRegisterUserOnlyWindow.destroy()

        for it in email:
            if re.match("^[A-Za-z0-9._%\-+!#$&/=?^|~]+@[A-Za-z0-9-]+[.][A-Za-z]+$", it, re.IGNORECASE):
                continue
            else:
                messagebox.showwarning("info", "This is not a valid email address")

        myfunction()

#======4 register visitor only==============

    def createNewRegisterVisitorOnlyWindow(self):
        self.newRegisterVisitorOnlyWindow = Toplevel()
        self.newRegisterVisitorOnlyWindow.title("Atlanta BeltLine")
        self.registerNavigationWindow.withdraw()

    def buildNewRegisterVisitorOnlyWindow(self, newRegisterVisitorOnlyWindow):
        # New User Only Registration Label
        RegisterVisitorOnlyLabel = Label(newRegisterVisitorOnlyWindow, text="Register Visitor",font = "Verdana 13 bold ")
        RegisterVisitorOnlyLabel.grid(row=1, column=3, sticky=W+E)

        # First Name Label
        firstNameLabel = Label(newRegisterVisitorOnlyWindow, text="First Name")
        firstNameLabel.grid(row=2, column=1)
        # Last Name Label
        lastNameLabel = Label(newRegisterVisitorOnlyWindow, text="Last Name")
        lastNameLabel.grid(row=2, column=3, sticky=E)
        # Username Label
        usernameLabel = Label(newRegisterVisitorOnlyWindow, text="Username")
        usernameLabel.grid(row=3, column=1)
        # Password Label
        passwordLabel = Label(newRegisterVisitorOnlyWindow, text="Password")
        passwordLabel.grid(row=4, column=1)
        # Confirm Password Label
        confirmPasswordLabel = Label(newRegisterVisitorOnlyWindow, text="Confirm Password")
        confirmPasswordLabel.grid(row=4, column=3, sticky=E)
        # Email Address Label
        emailLabel = Label(newRegisterVisitorOnlyWindow, text="Email")
        emailLabel.grid(row=5, column=1)

        # First Name Entry
        self.registrationFirstName = StringVar()
        firstNameEntry = Entry(newRegisterVisitorOnlyWindow, textvariable=self.registrationFirstName, width=20)
        firstNameEntry.grid(row=2, column=2, sticky=W + E)
        # Last Name Entry
        self.registrationLastName = StringVar()
        lastNameEntry = Entry(newRegisterVisitorOnlyWindow, textvariable=self.registrationLastName, width=20)
        lastNameEntry.grid(row=2, column=4, sticky=E)
        # Username Entry
        self.registrationUsername = StringVar()
        usernameEntry = Entry(newRegisterVisitorOnlyWindow, textvariable=self.registrationUsername, width=20)
        usernameEntry.grid(row=3, column=2, sticky=W + E)
        # Password Entry
        self.registrationPassword = StringVar()
        passwordEntry = Entry(newRegisterVisitorOnlyWindow, textvariable=self.registrationPassword, show='*', width=20)
        passwordEntry.grid(row=4, column=2, sticky=W + E)
        # Confirm Password Entry
        self.registrationConfirmPassword = StringVar()
        confirmPasswordEntry = Entry(newRegisterVisitorOnlyWindow, textvariable=self.registrationConfirmPassword, show='*',
                                     width=20)
        confirmPasswordEntry.grid(row=4, column=4, sticky=E)
        # Email Address Entry
        # self.registrationEmailAddress = StringVar()
        # emailAddressEntry = Entry(newRegisterVisitorOnlyWindow, textvariable=self.registrationEmailAddress, width=20)
        # emailAddressEntry.grid(row=5, column=2, sticky=W + E)
        #
        # # Create Remove Button
        # # Create Add Button
        # # Create Back Button
        # createButton = Button(newRegisterVisitorOnlyWindow, text="Back", command=self.registerVisitorOnlyBackButtonClicked)
        # createButton.grid(row=6, column=2)
        # # Create Register Button
        # createButton = Button(newRegisterVisitorOnlyWindow, text="Register",
        #                       command=self.newRegisterVisitorOnlyRegisterButtonClicked)
        # createButton.grid(row=6, column=3)

        EntryRow = 5
        Email = []  # can be used to register database
        EmailLabels = []
        removeButton = []
        EmailAddress = StringVar()
        emailAddressEntry = Entry(newRegisterVisitorOnlyWindow, textvariable=EmailAddress, width=20)

        # reconfigurate
        def reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton):
            for i in range(len(removeButton)):
                removeButton[i].grid(row=5 + i, column=3, sticky=W)
                EmailLabels[i].grid(row=5 + i, column=2, sticky=W)
            self.addButton_newRegisterVisitorOnlyWindow.destroy()
            self.addButton_newRegisterVisitorOnlyWindow = Button(newRegisterVisitorOnlyWindow, text="Add",
                                                              command=lambda: addRow(self, EntryRow, Email, EmailLabels,
                                                                                     removeButton, emailAddressEntry,
                                                                                     EmailAddress, backButton,
                                                                                     registerButton))
            self.addButton_newRegisterVisitorOnlyWindow.grid(row=EntryRow, column=3, sticky=W)
            emailAddressEntry.grid(row=EntryRow, column=2, sticky=W)
            backButton.grid(row=EntryRow + 1, column=3)
            registerButton.grid(row=EntryRow + 1, column=2)

        def removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton, emailAddressEntry, backButton,
                      registerButton):
            indexToRemove = removeButton.index(temp)
            for i in range(len(Email)):
                removeButton[i].grid_remove()
                removeButton[i].destroy()
                EmailLabels[i].grid_remove()
                EmailLabels[i].destroy()
            del Email[indexToRemove]
            EntryRow = len(Email) + 5
            removeButton = []
            EmailLabels = []
            # addButton.grid_remove()
            # addButton.destroy()
            for i in range(len(Email)):
                temp = Button(newRegisterVisitorOnlyWindow, text='remove',
                              command=lambda: removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton,
                                                        emailAddressEntry, backButton, registerButton))
                removeButton.append(temp)
                tempEmailLabel = Label(newRegisterVisitorOnlyWindow, text=Email[i])
                EmailLabels.append(tempEmailLabel)
            # addButton = Button(newRegisterUserOnlyWindow, text="Add", command=lambda: addRow(EntryRow,Email,
            #                    EmailLabels,removeButton,emailAddressEntry,EmailAddress,addButton,backButton,registerButton))
            reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

        def addRow(self, EntryRow, Email, EmailLabels, removeButton, emailAddressEntry, EmailAddress, backButton,
                   registerButton):
            Email.append(EmailAddress.get())
            EntryRow = EntryRow + 1
            # creat remove button
            temp = Button(newRegisterVisitorOnlyWindow, text='remove',
                          command=lambda: removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton,
                                                    emailAddressEntry, backButton, registerButton))
            removeButton.append(temp)
            tempEmailLabel = Label(newRegisterVisitorOnlyWindow, text=EmailAddress.get())
            EmailLabels.append(tempEmailLabel)

            reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

        '''
        我在这里加了一个functioin“resigterButton”，这个function把email这个list以变量的形式传到buttonclick里边
        '''

        def registerButtonClick():
            Email.append(EmailAddress.get())
            self.newRegisterVisitorOnlyRegisterButtonClicked(Email)

        # Create Add Button
        backButton = Button(newRegisterVisitorOnlyWindow, text="Back", command=self.registerVisitorOnlyBackButtonClicked)
        registerButton = Button(newRegisterVisitorOnlyWindow, text="Register", command=registerButtonClick)
        self.addButton_newRegisterVisitorOnlyWindow = Button(newRegisterVisitorOnlyWindow, text="Add",
                                                          command=lambda: addRow(self, EntryRow, Email, EmailLabels,
                                                                                 removeButton, emailAddressEntry,
                                                                                 EmailAddress, backButton,
                                                                                 registerButton))
        reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

    def registerVisitorOnlyBackButtonClicked(self):
        self.creatRegisterNavigationWindow()
        self.buildRegisterNavigationWindow(self.registerNavigationWindow)
        self.newRegisterVisitorOnlyWindow.withdraw()

    def newRegisterVisitorOnlyRegisterButtonClicked(self, Email):
        # Click the Create Button on New User Registration Window:
        # Invoke createChooseFunctionalityWindow; Invoke buildChooseFunctionalityWindow;
        # Destroy New User Registration Window
        self.firstName = self.registrationFirstName.get()
        self.lastName = self.registrationLastName.get()
        self.username = self.registrationUsername.get()
        self.emailAddress = Email
        self.password = self.registrationPassword.get()
        self.confirmPassword = self.registrationConfirmPassword.get()
        if not self.firstName:
            messagebox.showwarning("First name is empty", "Please enter first name.")
            return False
        if not self.lastName:
            messagebox.showwarning("Last name is empty", "Please enter last name.")
            return False
        if not self.username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        if len(self.emailAddress)==0:
            messagebox.showwarning("E-mail input is empty", "Please enter E-mail.")
            return False
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        if len(self.password) < 8:
            messagebox.showwarning("info", "Password must be at least 8 digits")
            return False
        if not self.confirmPassword:
            messagebox.showwarning("Confirm password input is empty", "Please enter confirm password")
            return False

        isUsername = self.cursor.execute("SELECT * FROM User WHERE Username = %s", self.username)
        if isUsername:
           messagebox.showwarning("This username has been used.",
                                  "Please input another username.")
           return False
        for element in self.emailAddress:
            isEmail = self.cursor.execute("SELECT * FROM UserEmail WHERE Email = %s", element)
            if isEmail:
               messagebox.showwarning("This E-mail address has been used.",
                                      "Please input another E-mail address.")
               return False
        if not (self.password == self.confirmPassword):
           messagebox.showwarning("Password does not match the confirm password.",
                                  "Please reconfirm the password.")
           return False

        h1 = hashlib.md5(self.password.encode())
        h2 = hashlib.md5(self.confirmPassword.encode())
        self.password = h1
        self.confirmPassword = h2
        print(h1.hexdigest())
        print(h2.hexdigest())
        print(self.password.hexdigest())
        print(self.confirmPassword.hexdigest())

        email = self.emailAddress

        def myfunction():
            self.cursor.execute("INSERT INTO User VALUES (%s, %s, %s, %s, %s)",
                                (self.username, self.password.hexdigest(), self.firstName, self.lastName, "Pending"))
            self.db.commit()
            for i in range(len(self.emailAddress)):
                self.cursor.execute("INSERT INTO UserEmail VALUES (%s, %s)", (self.username, self.emailAddress[i]))
                self.db.commit()
            self.cursor.execute("INSERT INTO Visitor VALUES (%s)", self.username)
            self.db.commit()
            messagebox.showinfo("info","Register Visitor successfully!")
            self.createLoginWindow()
            self.buildLoginWindow(self.loginWindow)
            self.newRegisterVisitorOnlyWindow.destroy()

        for it in email:
            if re.match("^[A-Za-z0-9._%\-+!#$&/=?^|~]+@[A-Za-z0-9-]+[.][A-Za-z]+$", it, re.IGNORECASE):
                continue
            else:
                messagebox.showwarning("info", "This is not a valid email address")
        myfunction()

#======5 register Employee only==============

    def createNewRegisterEmployeeOnlyWindow(self):
        self.newRegisterEmployeeOnlyWindow = Toplevel()
        self.newRegisterEmployeeOnlyWindow.title("Atlanta BeltLine")
        self.registerNavigationWindow.withdraw()

    def buildNewRegisterEmployeeOnlyWindow(self, newRegisterEmployeeOnlyWindow):
        # New Employee Only Registration Label
        RegisterEmployeeOnlyLabel = Label(newRegisterEmployeeOnlyWindow, text="Register Employee", font = "Verdana 13 bold ")
        RegisterEmployeeOnlyLabel.grid(row=1, column=3, sticky=W+E)

        # First Name Label
        firstNameLabel = Label(newRegisterEmployeeOnlyWindow, text="First Name")
        firstNameLabel.grid(row=2, column=1)
        # Last Name Label
        lastNameLabel = Label(newRegisterEmployeeOnlyWindow, text="Last Name")
        lastNameLabel.grid(row=2, column=3)
        # Username Label
        usernameLabel = Label(newRegisterEmployeeOnlyWindow, text="Username")
        usernameLabel.grid(row=3, column=1)
        # User Type
        userTypeLabel = Label(newRegisterEmployeeOnlyWindow, text="User Type")
        userTypeLabel.grid(row=3, column=3)
        # Password Label
        passwordLabel = Label(newRegisterEmployeeOnlyWindow, text="Password")
        passwordLabel.grid(row=4, column=1)
        # Confirm Password Label
        confirmPasswordLabel = Label(newRegisterEmployeeOnlyWindow, text="Confirm Password")
        confirmPasswordLabel.grid(row=4, column=3)
        # Phone Label
        phoneLabel = Label(newRegisterEmployeeOnlyWindow, text="Phone")
        phoneLabel.grid(row=5, column=1)
        # Address Label
        addressLabel = Label(newRegisterEmployeeOnlyWindow, text="Address")
        addressLabel.grid(row=5, column=3)
        # City Label
        cityLabel = Label(newRegisterEmployeeOnlyWindow, text="City")
        cityLabel.grid(row=6, column=1)
        # State Label
        stateLabel = Label(newRegisterEmployeeOnlyWindow, text="State")
        stateLabel.grid(row=6, column=3)
        # Zipcode Label
        zipcodeLabel = Label(newRegisterEmployeeOnlyWindow, text="Zipcode")
        zipcodeLabel.grid(row=6, column=5)
        # Email Address Label
        emailLabel = Label(newRegisterEmployeeOnlyWindow, text="Email")
        emailLabel.grid(row=7, column=1)

        # First Name Entry
        self.registrationFirstName = StringVar()
        firstNameEntry = Entry(newRegisterEmployeeOnlyWindow, textvariable=self.registrationFirstName, width=20)
        firstNameEntry.grid(row=2, column=2, sticky=W+E)
        # Last Name Entry
        self.registrationLastName = StringVar()
        lastNameEntry = Entry(newRegisterEmployeeOnlyWindow, textvariable=self.registrationLastName, width=20)
        lastNameEntry.grid(row=2, column=4, sticky=E)
        # Username Entry
        self.registrationUsername = StringVar()
        usernameEntry = Entry(newRegisterEmployeeOnlyWindow, textvariable=self.registrationUsername, width=20)
        usernameEntry.grid(row=3, column=2, sticky=W+E)
        # User Type drop down menu
        self.registrationUserType = StringVar()
        self.registrationUserType.set("Manager")
        lst1 = ["Manager", "Staff"]
        optionButton = OptionMenu(newRegisterEmployeeOnlyWindow, self.registrationUserType, *lst1)
        optionButton.grid(row=3, column=4, sticky=E)
        # Password Entry
        self.registrationPassword = StringVar()
        passwordEntry = Entry(newRegisterEmployeeOnlyWindow, textvariable=self.registrationPassword, show='*', width=20)
        passwordEntry.grid(row=4, column=2, sticky=W+E)
        # Confirm Password Entry
        self.registrationConfirmPassword = StringVar()
        confirmPasswordEntry = Entry(newRegisterEmployeeOnlyWindow, textvariable=self.registrationConfirmPassword, show='*',
                                     width=20)
        confirmPasswordEntry.grid(row=4, column=4, sticky=E)
        # Phone Entry
        self.registrationPhone = StringVar()
        phoneEntry = Entry(newRegisterEmployeeOnlyWindow, textvariable=self.registrationPhone, width=9)
        phoneEntry.grid(row=5, column=2, sticky=W+E)
        # Address Entry
        self.registrationAddress = StringVar()
        addressEntry = Entry(newRegisterEmployeeOnlyWindow, textvariable=self.registrationAddress, width=30)
        addressEntry.grid(row=5, column=4, sticky=E)
        # City Entry
        self.registrationCity = StringVar()
        cityEntry = Entry(newRegisterEmployeeOnlyWindow, textvariable=self.registrationCity, width=10)
        cityEntry.grid(row=6, column=2, sticky=W+E)
        # State drop down menu
        self.registrationState = StringVar()
        self.registrationState.set("WA")
        lst2 = ["WA", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
               "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
               "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WV", "WI", "WY"]
        optionButtonState = OptionMenu(newRegisterEmployeeOnlyWindow, self.registrationState, *lst2)
        optionButtonState.grid(row=6, column=4, sticky=W+E)
        # Zipcode Entry
        self.registrationZipcode = StringVar()
        zipcodeEntry = Entry(newRegisterEmployeeOnlyWindow, textvariable=self.registrationZipcode, width=5)
        zipcodeEntry.grid(row=6, column=6, sticky=E)
        # Email Address Entry
        EntryRow = 7
        Email = []  # can be used to register database
        EmailLabels = []
        removeButton = []
        EmailAddress = StringVar()
        emailAddressEntry = Entry(newRegisterEmployeeOnlyWindow, textvariable=EmailAddress, width=20)

        # reconfigurate
        def reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton):
            for i in range(len(removeButton)):
                removeButton[i].grid(row=7 + i, column=3, sticky=W)
                EmailLabels[i].grid(row=7 + i, column=2, sticky=W)
            self.addButton_newRegisterEmployeeOnlyWindow.destroy()
            self.addButton_newRegisterEmployeeOnlyWindow = Button(newRegisterEmployeeOnlyWindow, text="Add",
                                                              command=lambda: addRow(self, EntryRow, Email, EmailLabels,
                                                                                     removeButton, emailAddressEntry,
                                                                                     EmailAddress, backButton,
                                                                                     registerButton))
            self.addButton_newRegisterEmployeeOnlyWindow.grid(row=EntryRow, column=3, sticky=W)
            emailAddressEntry.grid(row=EntryRow, column=2, sticky=W)
            backButton.grid(row=EntryRow + 1, column=3)
            registerButton.grid(row=EntryRow + 1, column=2)

        def removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton, emailAddressEntry, backButton,
                      registerButton):
            indexToRemove = removeButton.index(temp)
            for i in range(len(Email)):
                removeButton[i].grid_remove()
                removeButton[i].destroy()
                EmailLabels[i].grid_remove()
                EmailLabels[i].destroy()
            del Email[indexToRemove]
            EntryRow = len(Email) + 7
            removeButton = []
            EmailLabels = []
            # addButton.grid_remove()
            # addButton.destroy()
            for i in range(len(Email)):
                temp = Button(newRegisterEmployeeOnlyWindow, text='remove',
                              command=lambda: removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton,
                                                        emailAddressEntry, backButton, registerButton))
                removeButton.append(temp)
                tempEmailLabel = Label(newRegisterEmployeeOnlyWindow, text=Email[i])
                EmailLabels.append(tempEmailLabel)
            # addButton = Button(newRegisterUserOnlyWindow, text="Add", command=lambda: addRow(EntryRow,Email,
            #                    EmailLabels,removeButton,emailAddressEntry,EmailAddress,addButton,backButton,registerButton))
            reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

        def addRow(self, EntryRow, Email, EmailLabels, removeButton, emailAddressEntry, EmailAddress, backButton,
                   registerButton):
            Email.append(EmailAddress.get())
            EntryRow = EntryRow + 1
            # creat remove button
            temp = Button(newRegisterEmployeeOnlyWindow, text='remove',
                          command=lambda: removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton,
                                                    emailAddressEntry, backButton, registerButton))
            removeButton.append(temp)
            tempEmailLabel = Label(newRegisterEmployeeOnlyWindow, text=EmailAddress.get())
            EmailLabels.append(tempEmailLabel)

            reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

        '''
        我在这里加了一个functioin“resigterButton”，这个function把email这个list以变量的形式传到buttonclick里边
        '''

        def registerButtonClick():
            Email.append(EmailAddress.get())
            self.newRegisterEmployeeOnlyRegisterButtonClicked(Email)

        # Create Add Button
        backButton = Button(newRegisterEmployeeOnlyWindow, text="Back", command=self.registerEmployeeOnlyBackButtonClicked)
        registerButton = Button(newRegisterEmployeeOnlyWindow, text="Register", command=registerButtonClick)
        self.addButton_newRegisterEmployeeOnlyWindow = Button(newRegisterEmployeeOnlyWindow, text="Add",
                                                          command=lambda: addRow(self, EntryRow, Email, EmailLabels,
                                                                                 removeButton, emailAddressEntry,
                                                                                 EmailAddress, backButton,
                                                                                 registerButton))
        reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

    def registerEmployeeOnlyBackButtonClicked(self):
        self.creatRegisterNavigationWindow()
        self.buildRegisterNavigationWindow(self.registerNavigationWindow)
        self.newRegisterEmployeeOnlyWindow.withdraw()

    def newRegisterEmployeeOnlyRegisterButtonClicked(self,Email):
        self.firstName = self.registrationFirstName.get()
        self.lastName = self.registrationLastName.get()
        self.username = self.registrationUsername.get()
        self.userType = self.registrationUserType.get()
        self.emailAddress = Email
        self.password = self.registrationPassword.get()
        self.confirmPassword = self.registrationConfirmPassword.get()
        self.phone = self.registrationPhone.get()
        self.address = self.registrationAddress.get()
        self.city = self.registrationCity.get()
        self.state = self.registrationState.get()
        self.zipcode = self.registrationZipcode.get()
        if not self.firstName:
            messagebox.showwarning("First name is empty", "Please enter first name.")
            return False
        if not self.lastName:
            messagebox.showwarning("Last name is empty", "Please enter last name.")
            return False
        if not self.username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        if len(self.emailAddress)==0:
            messagebox.showwarning("E-mail input is empty", "Please enter E-mail.")
            return False
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password.")
            return False
        if len(self.password) < 8:
            messagebox.showwarning("info", "Password must be at least 8 digits.")
            return False
        if not self.confirmPassword:
            messagebox.showwarning("Confirm password input is empty", "Please enter confirm password.")
            return False
        if not self.phone:
            messagebox.showwarning("Phone input is empty", "Please enter phone number.")
            return False
        if len(self.phone) != 9:
            messagebox.showwarning("info", "Phone must be a 9-digit number.")
            return False
        if not self.address:
            messagebox.showwarning("Address input is empty", "Please enter address.")
            return False
        if not self.city:
            messagebox.showwarning("City input is empty", "Please enter city.")
            return False
        if not self.zipcode:
            messagebox.showwarning("Zipcode is empty", "Please enter zipcode")
            return False
        if len(self.zipcode) != 5:
            messagebox.showwarning("info", "Zipcode must be a 5-digit number.")
            return False

        isUsername = self.cursor.execute("SELECT * FROM User WHERE Username = %s", self.username)
        if isUsername:
            messagebox.showwarning("This username has been used.",
                                   "Please input another username.")
            return False
        for element in self.emailAddress:
            isEmail = self.cursor.execute("SELECT * FROM UserEmail WHERE Email = %s", element)
            if isEmail:
               messagebox.showwarning("This E-mail address has been used.",
                                      "Please input another E-mail address.")
               return False
        isPhone = self.cursor.execute("SELECT * FROM Employee WHERE Phone = %s", self.phone)
        if isPhone:
            messagebox.showwarning("This phone number has been used.", "Please enter another phone number.")
            return False
        if not (self.password == self.confirmPassword):
            messagebox.showwarning("Password does not match the confirm password.",
                                   "Please reconfirm the password.")
            return False

        h1 = hashlib.md5(self.password.encode())
        h2 = hashlib.md5(self.confirmPassword.encode())
        self.password = h1
        self.confirmPassword = h2
        print(h1.hexdigest())
        print(h2.hexdigest())
        print(self.password.hexdigest())
        print(self.confirmPassword.hexdigest())

        email = self.emailAddress

        def myfunction():
            self.cursor.execute("INSERT INTO User VALUES (%s, %s, %s, %s, %s)",
                                (self.username, self.password.hexdigest(), self.firstName, self.lastName, "Pending"))
            self.db.commit()
            for i in range(len(self.emailAddress)):
                self.cursor.execute("INSERT INTO UserEmail VALUES (%s, %s)", (self.username, self.emailAddress[i]))
                self.db.commit()
            self.cursor.execute("INSERT INTO Employee VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (self.username, self.phone, self.phone, self.address, self.city, self.state, self.zipcode))
            self.db.commit()
            if self.userType == "Staff":
                self.cursor.execute("INSERT INTO Staff VALUES (%s)", self.username)
            elif self.userType == "Manager":
                self.cursor.execute("INSERT INTO Manager VALUES (%s)", self.username)
            self.db.commit()
            messagebox.showinfo("info", "Register employee successfully!")
            self.createLoginWindow()
            self.buildLoginWindow(self.loginWindow)
            self.newRegisterEmployeeOnlyWindow.destroy()

        for it in email:
            if re.match("^[A-Za-z0-9._%\-+!#$&/=?^|~]+@[A-Za-z0-9-]+[.][A-Za-z]+$", it, re.IGNORECASE):
                continue
            else:
                messagebox.showwarning("info", "This is not a valid email address")
        myfunction()

#======6 register Employee Visitor==============

    def createNewRegisterEmployeeVisitorWindow(self):
        self.newRegisterEmployeeVisitorWindow = Toplevel()
        self.newRegisterEmployeeVisitorWindow.title("Atlanta BeltLine")
        self.registerNavigationWindow.withdraw()

    def buildNewRegisterEmployeeVisitorWindow(self, newRegisterEmployeeVisitorWindow):
        # New Employee-Visitor Registration Label
        RegisterEmployeeVisitorLabel = Label(newRegisterEmployeeVisitorWindow, text="Register Employee-Visitor", font="Verdana 13 bold ")
        RegisterEmployeeVisitorLabel.grid(row=1, column=3, sticky=W + E)

        # First Name Label
        firstNameLabel = Label(newRegisterEmployeeVisitorWindow, text="First Name")
        firstNameLabel.grid(row=2, column=1)
        # Last Name Label
        lastNameLabel = Label(newRegisterEmployeeVisitorWindow, text="Last Name")
        lastNameLabel.grid(row=2, column=3)
        # Username Label
        usernameLabel = Label(newRegisterEmployeeVisitorWindow, text="Username")
        usernameLabel.grid(row=3, column=1)
        # User Type
        userTypeLabel = Label(newRegisterEmployeeVisitorWindow, text="User Type")
        userTypeLabel.grid(row=3, column=3)
        # Password Label
        passwordLabel = Label(newRegisterEmployeeVisitorWindow, text="Password")
        passwordLabel.grid(row=4, column=1)
        # Confirm Password Label
        confirmPasswordLabel = Label(newRegisterEmployeeVisitorWindow, text="Confirm Password")
        confirmPasswordLabel.grid(row=4, column=3)
        # Phone Label
        phoneLabel = Label(newRegisterEmployeeVisitorWindow, text="Phone")
        phoneLabel.grid(row=5, column=1)
        # Address Label
        addressLabel = Label(newRegisterEmployeeVisitorWindow, text="Address")
        addressLabel.grid(row=5, column=3)
        # City Label
        cityLabel = Label(newRegisterEmployeeVisitorWindow, text="City")
        cityLabel.grid(row=6, column=1)
        # State Label
        stateLabel = Label(newRegisterEmployeeVisitorWindow, text="State")
        stateLabel.grid(row=6, column=3)
        # Zipcode Label
        zipcodeLabel = Label(newRegisterEmployeeVisitorWindow, text="Zipcode")
        zipcodeLabel.grid(row=6, column=5)
        # Email Address Label
        emailLabel = Label(newRegisterEmployeeVisitorWindow, text="Email")
        emailLabel.grid(row=7, column=1)

        # First Name Entry
        self.registrationFirstName = StringVar()
        firstNameEntry = Entry(newRegisterEmployeeVisitorWindow, textvariable=self.registrationFirstName, width=20)
        firstNameEntry.grid(row=2, column=2, sticky=W + E)
        # Last Name Entry
        self.registrationLastName = StringVar()
        lastNameEntry = Entry(newRegisterEmployeeVisitorWindow, textvariable=self.registrationLastName, width=20)
        lastNameEntry.grid(row=2, column=4, sticky=E)
        # Username Entry
        self.registrationUsername = StringVar()
        usernameEntry = Entry(newRegisterEmployeeVisitorWindow, textvariable=self.registrationUsername, width=20)
        usernameEntry.grid(row=3, column=2, sticky=W + E)
        # User Type drop down menu
        self.registrationUserType = StringVar()
        self.registrationUserType.set("Manager")
        lst1 = ["Manager", "Staff"]
        optionButton = OptionMenu(newRegisterEmployeeVisitorWindow, self.registrationUserType, *lst1)
        optionButton.grid(row=3, column=4, sticky=E)
        # Password Entry
        self.registrationPassword = StringVar()
        passwordEntry = Entry(newRegisterEmployeeVisitorWindow, textvariable=self.registrationPassword, show='*', width=20)
        passwordEntry.grid(row=4, column=2, sticky=W + E)
        # Confirm Password Entry
        self.registrationConfirmPassword = StringVar()
        confirmPasswordEntry = Entry(newRegisterEmployeeVisitorWindow, textvariable=self.registrationConfirmPassword,
                                     show='*',
                                     width=20)
        confirmPasswordEntry.grid(row=4, column=4, sticky=E)
        # Phone Entry
        self.registrationPhone = StringVar()
        phoneEntry = Entry(newRegisterEmployeeVisitorWindow, textvariable=self.registrationPhone, width=9)
        phoneEntry.grid(row=5, column=2, sticky=W + E)
        # Address Entry
        self.registrationAddress = StringVar()
        addressEntry = Entry(newRegisterEmployeeVisitorWindow, textvariable=self.registrationAddress, width=30)
        addressEntry.grid(row=5, column=4, sticky=E)
        # City Entry
        self.registrationCity = StringVar()
        cityEntry = Entry(newRegisterEmployeeVisitorWindow, textvariable=self.registrationCity, width=10)
        cityEntry.grid(row=6, column=2, sticky=W + E)
        # State drop down menu
        self.registrationState = StringVar()
        self.registrationState.set("WA")
        lst2 = ["WA", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
                "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
                "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WV", "WI", "WY"]
        optionButtonState = OptionMenu(newRegisterEmployeeVisitorWindow, self.registrationState, *lst2)
        optionButtonState.grid(row=6, column=4, sticky=W + E)
        # Zipcode Entry
        self.registrationZipcode = StringVar()
        zipcodeEntry = Entry(newRegisterEmployeeVisitorWindow, textvariable=self.registrationZipcode, width=5)
        zipcodeEntry.grid(row=6, column=6, sticky=E)
        # Email Address Entry
        EntryRow = 7
        Email = []  # can be used to register database
        EmailLabels = []
        removeButton = []
        EmailAddress = StringVar()
        emailAddressEntry = Entry(newRegisterEmployeeVisitorWindow, textvariable=EmailAddress, width=20)

        # reconfigurate
        def reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton):
            for i in range(len(removeButton)):
                removeButton[i].grid(row=7 + i, column=3, sticky=W)
                EmailLabels[i].grid(row=7 + i, column=2, sticky=W)
            self.addButton_newRegisterEmployeeVisitorWindow.destroy()
            self.addButton_newRegisterEmployeeVisitorWindow = Button(newRegisterEmployeeVisitorWindow, text="Add",
                                                                  command=lambda: addRow(self, EntryRow, Email,
                                                                                         EmailLabels,
                                                                                         removeButton,
                                                                                         emailAddressEntry,
                                                                                         EmailAddress, backButton,
                                                                                         registerButton))
            self.addButton_newRegisterEmployeeVisitorWindow.grid(row=EntryRow, column=3, sticky=W)
            emailAddressEntry.grid(row=EntryRow, column=2, sticky=W)
            backButton.grid(row=EntryRow + 1, column=3)
            registerButton.grid(row=EntryRow + 1, column=2)

        def removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton, emailAddressEntry, backButton,
                      registerButton):
            indexToRemove = removeButton.index(temp)
            for i in range(len(Email)):
                removeButton[i].grid_remove()
                removeButton[i].destroy()
                EmailLabels[i].grid_remove()
                EmailLabels[i].destroy()
            del Email[indexToRemove]
            EntryRow = len(Email) + 7
            removeButton = []
            EmailLabels = []
            # addButton.grid_remove()
            # addButton.destroy()
            for i in range(len(Email)):
                temp = Button(newRegisterEmployeeVisitorWindow, text='remove',
                              command=lambda: removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton,
                                                        emailAddressEntry, backButton, registerButton))
                removeButton.append(temp)
                tempEmailLabel = Label(newRegisterEmployeeVisitorWindow, text=Email[i])
                EmailLabels.append(tempEmailLabel)
            # addButton = Button(newRegisterUserOnlyWindow, text="Add", command=lambda: addRow(EntryRow,Email,
            #                    EmailLabels,removeButton,emailAddressEntry,EmailAddress,addButton,backButton,registerButton))
            reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

        def addRow(self, EntryRow, Email, EmailLabels, removeButton, emailAddressEntry, EmailAddress, backButton,
                   registerButton):
            Email.append(EmailAddress.get())
            EntryRow = EntryRow + 1
            # creat remove button
            temp = Button(newRegisterEmployeeVisitorWindow, text='remove',
                          command=lambda: removeRow(self, temp, EntryRow, Email, EmailLabels, removeButton,
                                                    emailAddressEntry, backButton, registerButton))
            removeButton.append(temp)
            tempEmailLabel = Label(newRegisterEmployeeVisitorWindow, text=EmailAddress.get())
            EmailLabels.append(tempEmailLabel)

            reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

        '''
        我在这里加了一个functioin“resigterButton”，这个function把email这个list以变量的形式传到buttonclick里边
        '''

        def registerButtonClick():
            Email.append(EmailAddress.get())
            self.newRegisterEmployeeVisitorRegisterButtonClicked(Email)

        # Create Add Button
        backButton = Button(newRegisterEmployeeVisitorWindow, text="Back",
                            command=self.registerEmployeeVisitorBackButtonClicked)
        registerButton = Button(newRegisterEmployeeVisitorWindow, text="Register", command=registerButtonClick)
        self.addButton_newRegisterEmployeeVisitorWindow = Button(newRegisterEmployeeVisitorWindow, text="Add",
                                                              command=lambda: addRow(self, EntryRow, Email, EmailLabels,
                                                                                     removeButton, emailAddressEntry,
                                                                                     EmailAddress, backButton,
                                                                                     registerButton))
        reConfig(self, EntryRow, EmailLabels, removeButton, emailAddressEntry, backButton, registerButton)

    def registerEmployeeVisitorBackButtonClicked(self):
        self.creatRegisterNavigationWindow()
        self.buildRegisterNavigationWindow(self.registerNavigationWindow)
        self.newRegisterEmployeeVisitorWindow.withdraw()

    def newRegisterEmployeeVisitorRegisterButtonClicked(self,Email):
        self.firstName = self.registrationFirstName.get()
        self.lastName = self.registrationLastName.get()
        self.username = self.registrationUsername.get()
        self.userType = self.registrationUserType.get()
        self.emailAddress = Email
        self.password = self.registrationPassword.get()
        self.confirmPassword = self.registrationConfirmPassword.get()
        self.phone = self.registrationPhone.get()
        self.address = self.registrationAddress.get()
        self.city = self.registrationCity.get()
        self.state = self.registrationState.get()
        self.zipcode = self.registrationZipcode.get()
        if not self.firstName:
            messagebox.showwarning("First name is empty", "Please enter first name.")
            return False
        if not self.lastName:
            messagebox.showwarning("Last name is empty", "Please enter last name.")
            return False
        if not self.username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        if len(self.emailAddress)==0:
            messagebox.showwarning("E-mail input is empty", "Please enter E-mail.")
            return False
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password.")
            return False
        if len(self.password) < 8:
            messagebox.showwarning("info", "Password must be at least 8 digits.")
            return False
        if not self.confirmPassword:
            messagebox.showwarning("Confirm password input is empty", "Please enter confirm password.")
            return False
        if not self.phone:
            messagebox.showwarning("Phone input is empty", "Please enter phone number.")
            return False
        if len(self.phone) != 9:
            messagebox.showwarning("info", "Phone must be a 9-digit number.")
            return False
        if not self.address:
            messagebox.showwarning("Address input is empty", "Please enter address.")
            return False
        if not self.city:
            messagebox.showwarning("City input is empty", "Please enter city.")
            return False
        if not self.zipcode:
            messagebox.showwarning("Zipcode is empty", "Please enter zipcode")
            return False
        if len(self.zipcode) != 5:
            messagebox.showwarning("info", "Zipcode must be a 5-digit number.")
            return False

        isUsername = self.cursor.execute("SELECT * FROM User WHERE Username = %s", self.username)
        if isUsername:
            messagebox.showwarning("This username has been used.",
                                   "Please input another username.")
            return False
        for element in self.emailAddress:
            isEmail = self.cursor.execute("SELECT * FROM UserEmail WHERE Email = %s", element)
            if isEmail:
               messagebox.showwarning("This E-mail address has been used.",
                                      "Please input another E-mail address.")
               return False
        isPhone = self.cursor.execute("SELECT * FROM Employee WHERE Phone = %s", self.phone)
        if isPhone:
            messagebox.showwarning("This phone number has been used.", "Please enter another phone number.")
            return False
        if not (self.password == self.confirmPassword):
            messagebox.showwarning("Password does not match the confirm password.",
                                   "Please reconfirm the password.")
            return False

        h1 = hashlib.md5(self.password.encode())
        h2 = hashlib.md5(self.confirmPassword.encode())
        self.password = h1
        self.confirmPassword = h2
        print(h1.hexdigest())
        print(h2.hexdigest())
        print(self.password.hexdigest())
        print(self.confirmPassword.hexdigest())

        email = self.emailAddress

        def myfunction():
            self.cursor.execute("INSERT INTO User VALUES (%s, %s, %s, %s, %s)",
                                (self.username, self.password.hexdigest(), self.firstName, self.lastName, "Pending"))
            self.db.commit()
            for i in range(len(self.emailAddress)):
                self.cursor.execute("INSERT INTO UserEmail VALUES (%s, %s)", (self.username, self.emailAddress[i]))
                self.db.commit()
            self.cursor.execute("INSERT INTO Visitor VALUES (%s)", self.username)
            self.db.commit()
            self.cursor.execute("INSERT INTO Employee VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (self.username, self.phone, self.phone, self.address, self.city, self.state, self.zipcode))
            self.db.commit()
            if self.userType == "Staff":
                self.cursor.execute("INSERT INTO Staff VALUES (%s)", self.username)
            elif self.userType == "Manager":
                self.cursor.execute("INSERT INTO Manager VALUES (%s)", self.username)
            self.db.commit()
            messagebox.showinfo("info", "Register employee-visitor successfully!")
            self.createLoginWindow()
            self.buildLoginWindow(self.loginWindow)
            self.newRegisterEmployeeVisitorWindow.destroy()

        for it in email:
            if re.match("^[A-Za-z0-9._%\-+!#$&/=?^|~]+@[A-Za-z0-9-]+[.][A-Za-z]+$", it, re.IGNORECASE):
                continue
            else:
                messagebox.showwarning("info", "This is not a valid email address")
        myfunction()

##========== Screen 7 User Functionality Window================

    def createUserFunctionalityWindow(self):
        # Create blank userFunctionalityWindow
        self.userFunctionalityWindow = Toplevel()
        self.userFunctionalityWindow.title("User Functionality")

    def buildUserFunctionalityWindow(self,userFunctionalityWindow):

        #User Functionality Label
        userFunctionalityLabel = Label(userFunctionalityWindow, text="User Functionality",font = "Verdana 10 bold ")
        userFunctionalityLabel.grid(row=1, column=2, sticky=W+E)

        # Take Transit
        takeTransitWindow = Button(userFunctionalityWindow, text="Take Transit",
                              command=self.takeTransit_user)
        takeTransitWindow.grid(row=3, column=2, sticky=W+E)

        # View Transit History
        transitHistoryWindow = Button(userFunctionalityWindow, text="View Transit History",
                              command=self.transitHistory_user)
        transitHistoryWindow.grid(row=5, column=2, sticky=W+E)

        # Back Buttons
        backButton = Button(userFunctionalityWindow, text="Back",
                        command=self.userFunctionalityWindowBackButtonClicked)
        backButton.grid(row=7, column=2, sticky=W+E)

    def takeTransit_user(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.userFunctionalityWindow
        self.userFunctionalityWindow.withdraw()

    def transitHistory_user(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        self.previous = self.userFunctionalityWindow
        self.userFunctionalityWindow.withdraw()

    def userFunctionalityWindowBackButtonClicked(self):
        # Click Log Out Buttion on Choose Functionality Window:
        # Destroy Choose Functionality Window
        # Display Login Window
        self.userFunctionalityWindow.destroy()
        self.loginWindow.deiconify()

    def createAdministratorOnlyFunctionalityWindow(self):
        # Create blank administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow = Toplevel()
        self.administratorOnlyFunctionalityWindow.title("Administrator-Only Functionality")

    def buildAdministratorOnlyFunctionalityWindow(self,administratorOnlyFunctionalityWindow):

        #User Functionality Label
        administratorOnlyFunctionalityLabel = Label(administratorOnlyFunctionalityWindow, text="Administrator Functionality",font = "Verdana 10 bold ")
        administratorOnlyFunctionalityLabel.grid(row=1, column=1, sticky=W+E)

        # Manage Profile
        manageProfileWindow = Button(administratorOnlyFunctionalityWindow, text="Manage Profile",
                                  command=self.manageProfile_administratorOnly)
        manageProfileWindow.grid(row=3, column=1)

        # Take Transit
        takeTransitWindow = Button(administratorOnlyFunctionalityWindow, text="Take Transit",
                              command=self.takeTransit_administratorOnly)
        takeTransitWindow.grid(row=3, column=3)

        # Manage User
        manageUserWindow = Button(administratorOnlyFunctionalityWindow, text="Manage User",
                              command=self.manageUser_administratorOnly)
        manageUserWindow.grid(row=5, column=1)

        # Transit History
        viewVisitHistoryWindow = Button(administratorOnlyFunctionalityWindow, text="View Transit History",
                                      command=self.transitHistory_administratorOnly)
        viewVisitHistoryWindow.grid(row=5, column=3)

        # Manage Transit
        manageTransitWindow = Button(administratorOnlyFunctionalityWindow, text="Manage Transit",
                                  command=self.manageTransit_administratorOnly)
        manageTransitWindow.grid(row=7, column=1)

        # Back Buttons
        backButton = Button(administratorOnlyFunctionalityWindow, text="Back",
                        command=self.administratorOnlyFunctionalityWindowBackButtonClicked)
        backButton.grid(row=7, column=3)

        # Manage Site
        manageSiteWindow = Button(administratorOnlyFunctionalityWindow, text="Manage Site",
                              command=self.manageSite_administratorOnly)
        manageSiteWindow.grid(row=9, column=1)

    def manageProfile_administratorOnly(self):
        self.createEmployeeManageProfileWindow()
        self.buildEmployeeManageProfileWindow(self.employeeManageProfileWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()

    def takeTransit_administratorOnly(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()

    def manageUser_administratorOnly(self):
        self.createAdminManageUserWindow()
        self.buildAdminManageUserWindow(self.manageUserWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()

    def transitHistory_administratorOnly(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()

    def manageTransit_administratorOnly(self):
        self.createManageTransitWindow()
        self.buildManageTransitWindow(self.manageTransitWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()

    def administratorOnlyFunctionalityWindowBackButtonClicked(self):
        # Click Log Out Buttion on Choose Functionality Window:
        # Destroy Choose Functionality Window
        # Display Login Window
        self.administratorOnlyFunctionalityWindow.destroy()
        self.loginWindow.deiconify()

    def manageSite_administratorOnly(self):
        self.createAdminManageSiteWindow()
        self.buildAdminManageSiteWindow(self.manageSiteWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()


##========== Screen 9 Administrator-Visitor Functionality Window================

    def createAdministratorVisitorFunctionalityWindow(self):
        # Create blank administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow = Toplevel()
        self.administratorVisitorFunctionalityWindow.title("Administrator-Visitor Functionality")

    def buildAdministratorVisitorFunctionalityWindow(self,administratorVisitorFunctionalityWindow):

        #User Functionality Label
        administratorVisitorFunctionalityLabel = Label(administratorVisitorFunctionalityWindow, text="Administrator Functionality",font = "Verdana 10 bold ")
        administratorVisitorFunctionalityLabel.grid(row=1, column=1, sticky=W+E)

        # Manage Profile
        manageProfileWindow = Button(administratorVisitorFunctionalityWindow, text="Manage Profile",
	                              command=self.manageProfile_administratorVisitor)
        manageProfileWindow.grid(row=3, column=1)

        # Manage User
        manageUserWindow = Button(administratorVisitorFunctionalityWindow, text="Manage User",
                              command=self.manageUser_administratorVisitor)
        manageUserWindow.grid(row=3, column=3)

        # Manage Transit
        manageTransitWindow = Button(administratorVisitorFunctionalityWindow, text="Manage Transit",
	                              command=self.manageTransit_administratorVisitor)
        manageTransitWindow.grid(row=5, column=1)

        # Take Transit
        takeTransitWindow = Button(administratorVisitorFunctionalityWindow, text="Take Transit",
                              command=self.takeTransit_administratorVisitor)
        takeTransitWindow.grid(row=5, column=3)

        # Manage Site
        manageSiteWindow = Button(administratorVisitorFunctionalityWindow, text="Manage Site",
                              command=self.manageSite_administratorVisitor)
        manageSiteWindow.grid(row=7, column=1)

        # Explore Site
        exploreSiteWindow = Button(administratorVisitorFunctionalityWindow, text="Explore Site",
                              command=self.exploreSite_administratorVisitor)
        exploreSiteWindow.grid(row=7, column=3)

        # Explore Event
        exploreEventWindow = Button(administratorVisitorFunctionalityWindow, text="Explore Event",
                              command=self.exploreEvent_administratorVisitor)
        exploreEventWindow.grid(row=9, column=1)

        # View Visit History
        viewVisitHistoryWindow = Button(administratorVisitorFunctionalityWindow, text="View Visit History",
		                              command=self.viewVisitHistory_administratorVisitor)
        viewVisitHistoryWindow.grid(row=9, column=3)

		# View Transit History
        transitHistoryWindow = Button(administratorVisitorFunctionalityWindow, text="View Transit History",
		                              command=self.transitHistory_administratorVisitor)
        transitHistoryWindow.grid(row=11, column=1)

        # Back Buttons
        backButton = Button(administratorVisitorFunctionalityWindow, text="Back",
			        	command=self.administratorVisitorFunctionalityWindowBackButtonClicked)
        backButton.grid(row=11, column=3)

    def manageProfile_administratorVisitor(self):
        self.createEmployeeManageProfileWindow()
        self.buildEmployeeManageProfileWindow(self.employeeManageProfileWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def takeTransit_administratorVisitor(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def manageUser_administratorVisitor(self):
        self.createAdminManageUserWindow()
        self.buildAdminManageUserWindow(self.manageUserWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def transitHistory_administratorVisitor(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def manageTransit_administratorVisitor(self):
        self.createManageTransitWindow()
        self.buildManageTransitWindow(self.manageTransitWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def manageSite_administratorVisitor(self):
        self.createAdminManageSiteWindow()
        self.buildAdminManageSiteWindow(self.manageSiteWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def exploreSite_administratorVisitor(self):
        self.createExploreSiteWindow()
        self.buildExploreSiteWindow(self.exploreSiteWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def exploreEvent_administratorVisitor(self):
        self.createExploreEventWindow()
        self.buildExploreEventWindow(self.exploreEventWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def viewVisitHistory_administratorVisitor(self):
        self.createViewVisitHistoryWindow()
        self.buildViewVisitHistoryWindow(self.viewVisitHistoryWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()


    def administratorVisitorFunctionalityWindowBackButtonClicked(self):
        # Click Log Out Buttion on Choose Functionality Window:
        # Destroy Choose Functionality Window
        # Display Login Window
        self.administratorVisitorFunctionalityWindow.destroy()
        self.loginWindow.deiconify()


#================== 10-ManagerOnlyFunctionalityWindow =========================
    def createManagerOnlyFunctionalityWindow(self):

        # Create blank ManagerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow = Toplevel()
        self.managerOnlyFunctionalityWindow.title("Atlanta Betline : Manager Only")

    def buildManagerOnlyFunctionalityWindow(self,managerOnlyFunctionalityWindow):

        managerOnlyFunctionalityLabel = Label(managerOnlyFunctionalityWindow, text="Manager Functionality", font="Verdana 14 bold ")
        managerOnlyFunctionalityLabel.grid(row=1, column=1, sticky=W + E)

        # Manage Profile
        managerManageProfile = Button(managerOnlyFunctionalityWindow, text="Manage Profile", command=self.manageProfile_managerOnly) #need command
        managerManageProfile.grid(row=2, column=1)
        # View Site Report
        managerViewSiteReport = Button(managerOnlyFunctionalityWindow, text="View Site Report", command=self.viewSiteReport_managerOnly) #need command
        managerViewSiteReport.grid(row=2, column=2)
        # Manage Event
        managerManageEvent = Button(managerOnlyFunctionalityWindow, text="Manage Event", command=self.manageEvent_managerOnly) #need command
        managerManageEvent.grid(row=3, column=1)
        # Take Transit
        managerTakeTransit = Button(managerOnlyFunctionalityWindow, text="Take Transit", command=self.takeTransit_managerOnly) #need command
        managerTakeTransit.grid(row=3, column=2)
        # View Staff
        managerViewStaff = Button(managerOnlyFunctionalityWindow, text="View Staff", command=self.viewStaff_managerOnly) #need command
        managerViewStaff.grid(row=4, column=1)
        # View Transit History
        managerViewTransitHistory = Button(managerOnlyFunctionalityWindow, text="View Transit History", command=self.viewTransitHistory_managerOnly) #need command
        managerViewTransitHistory.grid(row=4, column=2)

        backButton = Button(managerOnlyFunctionalityWindow, text="Back", command=self.managerOnlyFunctionalityWindowBackButtonClicked_managerOnly) #need command
        backButton.grid(row=5, column=1, sticky=E)

    def manageProfile_managerOnly(self):
        self.createEmployeeManageProfileWindow()
        self.buildEmployeeManageProfileWindow(self.employeeManageProfileWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def viewSiteReport_managerOnly(self):
        self.createSiteReportWindow()
        self.buildSiteReportWindow(self.siteReportWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def manageEvent_managerOnly(self):
        self.createManageEventWindow()
        self.buildManageEventWindow(self.manageEventWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def takeTransit_managerOnly(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def viewStaff_managerOnly(self):
        self.createManageStaffWindow()
        self.buildManageStaffWindow(self.manageStaffWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def viewTransitHistory_managerOnly(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def managerOnlyFunctionalityWindowBackButtonClicked_managerOnly(self):
        self.managerOnlyFunctionalityWindow.destroy()
        self.loginWindow.deiconify()

#================== 11-ManagerVisitorFunctionalityWindow =========================
    def createManagerVisitorFunctionalityWindow(self):

        # Create blank ManagerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow = Toplevel()
        self.managerVisitorFunctionalityWindow.title("Atlanta Betline : Manager-Visitor")

    def buildManagerVisitorFunctionalityWindow(self,managerVisitorFunctionalityWindow):

        managerVisitorFunctionalityLabel = Label(managerVisitorFunctionalityWindow, text="Manager Functionality", font="Verdana 14 bold ")
        managerVisitorFunctionalityLabel.grid(row=1, column=1, sticky=W + E)

        # Manage Profile
        managerManageProfile = Button(managerVisitorFunctionalityWindow, text="Manage Profile",
                                        command=self.manageProfile_managerVisitor)
        managerManageProfile.grid(row=2, column=1)
        # Manage Event
        managerManageEvent = Button(managerVisitorFunctionalityWindow, text="Manage Event",
                                        command=self.manageEvent_managerVisitor) #need command
        managerManageEvent.grid(row=2, column=2)
        # View Staff
        managerViewStaff = Button(managerVisitorFunctionalityWindow, text="View Staff",
                                        command=self.viewStaff_managerVisitor) #need command
        managerViewStaff.grid(row=3, column=1)
        # View Site Report
        managerViewSiteReport = Button(managerVisitorFunctionalityWindow, text="View Site Report",
                                        command=self.siteReport_managerVisitor) #need command
        managerViewSiteReport.grid(row=3, column=2)
        # Explore Site
        exploreSite = Button(managerVisitorFunctionalityWindow, text="Explore Site",
                                        command=self.exploreSite_managerVisitor) #need command
        exploreSite.grid(row=4, column=1)
        # Explore Event
        exploreEvent = Button(managerVisitorFunctionalityWindow, text="Explore Event",
                                        command=self.exploreEvent_managerVisitor) #need command
        exploreEvent.grid(row=4, column=2)
        # Take Transit
        managerTakeTransit = Button(managerVisitorFunctionalityWindow, text="Take Transit",
                                        command=self.takeTransit_managerVisitor) #need command
        managerTakeTransit.grid(row=5, column=1)
        # View Transit History
        managerViewTransitHistory = Button(managerVisitorFunctionalityWindow, text="View Transit History",
                                        command=self.transitHistory_managerVisitor) #need command
        managerViewTransitHistory.grid(row=5, column=2)
        # View Visit History
        viewVisitHistory = Button(managerVisitorFunctionalityWindow, text="View Visit History",
                                        command=self.visitHistory_managerVisitor) #need command
        viewVisitHistory.grid(row=6, column=1)

        backButton = Button(managerVisitorFunctionalityWindow, text="Back",
                                        command=self.managerVisitorFunctionalityWindowBackButtonClicked) #need command
        backButton.grid(row=6, column=2, sticky=E)

    def manageProfile_managerVisitor(self):
        self.createEmployeeManageProfileWindow()
        self.buildEmployeeManageProfileWindow(self.employeeManageProfileWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def manageEvent_managerVisitor(self):
        self.createManageEventWindow()
        self.buildManageEventWindow(self.manageEventWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def viewStaff_managerVisitor(self):
        self.createManageStaffWindow()
        self.buildManageStaffWindow(self.manageStaffWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def siteReport_managerVisitor(self):
        self.createSiteReportWindow()
        self.buildSiteReportWindow(self.siteReportWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def exploreSite_managerVisitor(self):
        self.createExploreSiteWindow()
        self.buildExploreSiteWindow(self.exploreSiteWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def exploreEvent_managerVisitor(self):
        self.createExploreEventWindow()
        self.buildExploreEventWindow(self.exploreEventWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def takeTransit_managerVisitor(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def transitHistory_managerVisitor(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def visitHistory_managerVisitor(self):
        self.createViewVisitHistoryWindow()
        self.buildViewVisitHistoryWindow(self.viewVisitHistoryWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def managerVisitorFunctionalityWindowBackButtonClicked(self):
        # Click Log Out Buttion on Choose Functionality Window:
        # Destroy Choose Functionality Window
        # Display Login Window
        self.managerVisitorFunctionalityWindow.destroy()
        self.loginWindow.deiconify()

##========== Screen 8 Administrator-Only Functionality Window================
    '''
    def createAdministratorOnlyFunctionalityWindow(self):
        # Create blank administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow = Toplevel()
        self.administratorOnlyFunctionalityWindow.title("Administrator-Only Functionality")

    def buildAdministratorOnlyFunctionalityWindow(self,administratorOnlyFunctionalityWindow):

        #User Functionality Label
        administratorOnlyFunctionalityLabel = Label(administratorOnlyFunctionalityWindow, text="Administrator Functionality",font = "Verdana 10 bold ")
        administratorOnlyFunctionalityLabel.grid(row=1, column=1, sticky=W+E)

        # Manage Profile
        manageProfileWindow = Button(administratorOnlyFunctionalityWindow, text="Manage Profile",
	                              command=self.manageProfile_administratorOnly)
        manageProfileWindow.grid(row=3, column=1)

        # Take Transit
        takeTransitWindow = Button(administratorOnlyFunctionalityWindow, text="Take Transit",
                              command=self.takeTransit_administratorOnly)
        takeTransitWindow.grid(row=3, column=3)

        # Manage User
        manageUserWindow = Button(administratorOnlyFunctionalityWindow, text="Manage User",
                              command=self.manageUser_administratorOnly)
        manageUserWindow.grid(row=5, column=1)

        # Transit History
        viewVisitHistoryWindow = Button(administratorOnlyFunctionalityWindow, text="View Transit History",
		                              command=self.transitHistory_administratorOnly)
        viewVisitHistoryWindow.grid(row=5, column=3)

        # Manage Transit
        manageTransitWindow = Button(administratorOnlyFunctionalityWindow, text="Manage Transit",
	                              command=self.manageTransit_administratorOnly)
        manageTransitWindow.grid(row=7, column=1)

        # Back Buttons
        backButton = Button(administratorOnlyFunctionalityWindow, text="Back",
			        	command=self.administratorOnlyFunctionalityWindowBackButtonClicked)
        backButton.grid(row=7, column=3)

        # Manage Site
        manageSiteWindow = Button(administratorOnlyFunctionalityWindow, text="Manage Site",
                              command=self.manageSite_administratorOnly)
        manageSiteWindow.grid(row=9, column=1)

    def manageProfile_administratorOnly(self):
        self.createEmployeeManageProfileWindow()
        self.buildEmployeeManageProfileWindow(self.employeeManageProfileWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()

    def takeTransit_administratorOnly(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()

    def manageUser_administratorOnly(self):
        self.createAdminManageUserWindow()
        self.buildAdminManageUserWindow(self.manageUserWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()

    def transitHistory_administratorOnly(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()

    def manageTransit_administratorOnly(self):
        self.createManageTransitWindow()
        self.buildManageTransitWindow(self.manageTransitWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()

    def administratorOnlyFunctionalityWindowBackButtonClicked(self):
        # Click Log Out Buttion on Choose Functionality Window:
        # Destroy Choose Functionality Window
        # Display Login Window
        self.administratorOnlyFunctionalityWindow.destroy()
        self.loginWindow.deiconify()

    def manageSite_administratorOnly(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.administratorOnlyFunctionalityWindow
        self.administratorOnlyFunctionalityWindow.withdraw()

##========== Screen 9 Administrator-Visitor Functionality Window================

    def createAdministratorVisitorFunctionalityWindow(self):
        # Create blank administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow = Toplevel()
        self.administratorVisitorFunctionalityWindow.title("Administrator-Visitor Functionality")

    def buildAdministratorVisitorFunctionalityWindow(self,administratorVisitorFunctionalityWindow):

        #User Functionality Label
        administratorVisitorFunctionalityLabel = Label(administratorVisitorFunctionalityWindow, text="Administrator Functionality",font = "Verdana 10 bold ")
        administratorVisitorFunctionalityLabel.grid(row=1, column=1, sticky=W+E)

        # Manage Profile
        manageProfileWindow = Button(administratorVisitorFunctionalityWindow, text="Manage Profile",
	                              command=self.manageProfile_administratorVisitor)
        manageProfileWindow.grid(row=3, column=1)

        # Manage User
        manageUserWindow = Button(administratorVisitorFunctionalityWindow, text="Manage User",
                              command=self.manageUser_administratorVisitor)
        manageUserWindow.grid(row=3, column=3)

        # Manage Transit
        manageTransitWindow = Button(administratorVisitorFunctionalityWindow, text="Manage Transit",
	                              command=self.manageTransit_administratorVisitor)
        manageTransitWindow.grid(row=5, column=1)

        # Take Transit
        takeTransitWindow = Button(administratorVisitorFunctionalityWindow, text="Take Transit",
                              command=self.takeTransit_administratorVisitor)
        takeTransitWindow.grid(row=5, column=3)

        # Manage Site
        manageSiteWindow = Button(administratorVisitorFunctionalityWindow, text="Manage Site",
                              command=self.manageSite_administratorVisitor)
        manageSiteWindow.grid(row=7, column=1)

        # Explore Site
        exploreSiteWindow = Button(administratorVisitorFunctionalityWindow, text="Explore Site",
                              command=self.exploreSite_administratorVisitor)
        exploreSiteWindow.grid(row=7, column=3)

        # Explore Event
        exploreEventWindow = Button(administratorVisitorFunctionalityWindow, text="Explore Event",
                              command=self.exploreEvent_administratorVisitor)
        exploreEventWindow.grid(row=9, column=1)

        # View Visit History
        viewVisitHistoryWindow = Button(administratorVisitorFunctionalityWindow, text="View Visit History",
		                              command=self.viewVisitHistory_administratorVisitor)
        viewVisitHistoryWindow.grid(row=9, column=3)

		# View Transit History
        transitHistoryWindow = Button(administratorVisitorFunctionalityWindow, text="View Transit History",
		                              command=self.transitHistory_administratorVisitor)
        transitHistoryWindow.grid(row=11, column=1)

        # Back Buttons
        backButton = Button(administratorVisitorFunctionalityWindow, text="Back",
			        	command=self.administratorVisitorFunctionalityWindowBackButtonClicked)
        backButton.grid(row=11, column=3)

    def manageProfile_administratorVisitor(self):
        self.createEmployeeManageProfileWindow()
        self.buildEmployeeManageProfileWindow(self.employeeManageProfileWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def takeTransit_administratorVisitor(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def manageUser_administratorVisitor(self):
        self.createAdminManageUserWindow()
        self.buildAdminManageUserWindow(self.manageUserWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def transitHistory_administratorVisitor(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def manageTransit_administratorVisitor(self):
        self.createManageTransitWindow()
        self.buildManageTransitWindow(self.manageTransitWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def manageSite_administratorVisitor(self):
        self.createAdminManageSiteWindow()
        self.buildAdminManageSiteWindow(self.manageSiteWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def exploreSite_administratorVisitor(self):
        self.createExploreSiteWindow()
        self.buildExploreSiteWindow(self.exploreSiteWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def exploreEvent_administratorVisitor(self):
        self.createExploreEventWindow()
        self.buildExploreEventWindow(self.exploreEventWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def viewVisitHistory_administratorVisitor(self):
        self.createViewVisitHistoryWindow()
        self.buildViewVisitHistoryWindow(self.viewVisitHistoryWindow)
        self.previous = self.administratorVisitorFunctionalityWindow
        self.administratorVisitorFunctionalityWindow.withdraw()

    def administratorVisitorFunctionalityWindowBackButtonClicked(self):#pguo
        # Click Log Out Buttion on Choose Functionality Window:
        # Destroy Choose Functionality Window
        # Display Login Window
        self.administratorVisitorFunctionalityWindow.destroy()
        self.loginWindow.deiconify()

#================== 10-ManagerOnlyFunctionalityWindow =========================
    def createManagerOnlyFunctionalityWindow(self):

        # Create blank ManagerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow = Toplevel()
        self.managerOnlyFunctionalityWindow.title("Atlanta Betline : Manager Only")

    def buildManagerOnlyFunctionalityWindow(self,managerOnlyFunctionalityWindow):

        managerOnlyFunctionalityLabel = Label(managerOnlyFunctionalityWindow, text="Manager Functionality", font="Verdana 14 bold ")
        managerOnlyFunctionalityLabel.grid(row=1, column=1, sticky=W + E)

        # Manage Profile
        managerManageProfile = Button(managerOnlyFunctionalityWindow, text="Manage Profile", command=self.manageProfile_managerOnly) #need command
        managerManageProfile.grid(row=2, column=1)
        # View Site Report
        managerViewSiteReport = Button(managerOnlyFunctionalityWindow, text="View Site Report", command=self.viewSiteReport_managerOnly) #need command
        managerViewSiteReport.grid(row=2, column=2)
        # Manage Event
        managerManageEvent = Button(managerOnlyFunctionalityWindow, text="Manage Event", command=self.manageEvent_managerOnly) #need command
        managerManageEvent.grid(row=3, column=1)
        # Take Transit
        managerTakeTransit = Button(managerOnlyFunctionalityWindow, text="Take Transit", command=self.takeTransit_managerOnly) #need command
        managerTakeTransit.grid(row=3, column=2)
        # View Staff
        managerViewStaff = Button(managerOnlyFunctionalityWindow, text="View Staff", command=self.viewStaff_managerOnly) #need command
        managerViewStaff.grid(row=4, column=1)
        # View Transit History
        managerViewTransitHistory = Button(managerOnlyFunctionalityWindow, text="View Transit History", command=self.viewTransitHistory_managerOnly) #need command
        managerViewTransitHistory.grid(row=4, column=2)

        backButton = Button(managerOnlyFunctionalityWindow, text="Back", command=self.managerOnlyFunctionalityWindowBackButtonClicked_managerOnly) #need command
        backButton.grid(row=5, column=1, sticky=E)

    def manageProfile_managerOnly(self):
        self.createEmployeeManageProfileWindow()
        self.buildEmployeeManageProfileWindow(self.employeeManageProfileWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def viewSiteReport_managerOnly(self):
        self.createSiteReportWindow()
        self.buildSiteReportWindow(self.siteReportWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def manageEvent_managerOnly(self):
        self.createManageEventWindow()
        self.buildManageEventWindow(self.manageEventWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def takeTransit_managerOnly(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def viewStaff_managerOnly(self):
        self.createManageStaffWindow()
        self.buildManageStaffWindow(self.manageStaffWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def viewTransitHistory_managerOnly(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        self.previous = self.managerOnlyFunctionalityWindow
        self.managerOnlyFunctionalityWindow.withdraw()

    def managerOnlyFunctionalityWindowBackButtonClicked_managerOnly(self):
        self.managerOnlyFunctionalityWindow.destroy()
        self.loginWindow.deiconify()

#================== 11-ManagerVisitorFunctionalityWindow =========================
    def createManagerVisitorFunctionalityWindow(self):

        # Create blank ManagerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow = Toplevel()
        self.managerVisitorFunctionalityWindow.title("Atlanta Betline : Manager-Visitor")

    def buildManagerVisitorFunctionalityWindow(self,managerVisitorFunctionalityWindow):

        managerVisitorFunctionalityLabel = Label(managerVisitorFunctionalityWindow, text="Manager Functionality", font="Verdana 14 bold ")
        managerVisitorFunctionalityLabel.grid(row=1, column=1, sticky=W + E)

        # Manage Profile
        managerManageProfile = Button(managerVisitorFunctionalityWindow, text="Manage Profile",
                                        command=self.manageProfile_managerVisitor)
        managerManageProfile.grid(row=2, column=1)
        # Manage Event
        managerManageEvent = Button(managerVisitorFunctionalityWindow, text="Manage Event",
                                        command=self.manageEvent_managerVisitor) #need command
        managerManageEvent.grid(row=2, column=2)
        # View Staff
        managerViewStaff = Button(managerVisitorFunctionalityWindow, text="View Staff",
                                        command=self.viewStaff_managerVisitor) #need command
        managerViewStaff.grid(row=3, column=1)
        # View Site Report
        managerViewSiteReport = Button(managerVisitorFunctionalityWindow, text="View Site Report",
                                        command=self.siteReport_managerVisitor) #need command
        managerViewSiteReport.grid(row=3, column=2)
        # Explore Site
        exploreSite = Button(managerVisitorFunctionalityWindow, text="Explore Site",
                                        command=self.exploreSite_managerVisitor) #need command
        exploreSite.grid(row=4, column=1)
        # Explore Event
        exploreEvent = Button(managerVisitorFunctionalityWindow, text="Explore Event",
                                        command=self.exploreEvent_managerVisitor) #need command
        exploreEvent.grid(row=4, column=2)
        # Take Transit
        managerTakeTransit = Button(managerVisitorFunctionalityWindow, text="Take Transit",
                                        command=self.takeTransit_managerVisitor) #need command
        managerTakeTransit.grid(row=5, column=1)
        # View Transit History
        managerViewTransitHistory = Button(managerVisitorFunctionalityWindow, text="View Transit History",
                                        command=self.transitHistory_managerVisitor) #need command
        managerViewTransitHistory.grid(row=5, column=2)
        # View Visit History
        viewVisitHistory = Button(managerVisitorFunctionalityWindow, text="View Visit History",
                                        command=self.visitHistory_managerVisitor) #need command
        viewVisitHistory.grid(row=6, column=1)

        backButton = Button(managerVisitorFunctionalityWindow, text="Back",
                                        command=self.managerVisitorFunctionalityWindowBackButtonClicked) #need command
        backButton.grid(row=6, column=2, sticky=E)

    def manageProfile_managerVisitor(self):
        self.createEmployeeManageProfileWindow()
        self.buildEmployeeManageProfileWindow(self.employeeManageProfileWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def manageEvent_managerVisitor(self):
        self.createManageEventWindow()
        self.buildManageEventWindow(self.manageEventWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def viewStaff_managerVisitor(self):
        self.createManageStaffWindow()
        self.buildManageStaffWindow(self.manageStaffWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def siteReport_managerVisitor(self):
        self.createSiteReportWindow()
        self.buildSiteReportWindow(self.siteReportWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def exploreSite_managerVisitor(self):
        self.createExploreSiteWindow()
        self.buildExploreSiteWindow(self.exploreSiteWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def exploreEvent_managerVisitor(self):
        self.createExploreEventWindow()
        self.buildExploreEventWindow(self.exploreEventWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def takeTransit_managerVisitor(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def transitHistory_managerVisitor(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def visitHistory_managerVisitor(self):
        self.createViewVisitHistoryWindow()
        self.buildViewVisitHistoryWindow(self.viewVisitHistoryWindow)
        self.previous = self.managerVisitorFunctionalityWindow
        self.managerVisitorFunctionalityWindow.withdraw()

    def managerVisitorFunctionalityWindowBackButtonClicked(self):#pguo
        # Click Log Out Buttion on Choose Functionality Window:
        # Destroy Choose Functionality Window
        # Display Login Window
        self.managerVisitorFunctionalityWindow.destroy()
        self.loginWindow.deiconify()
    '''
#================== 12-staffOnlyFunctionalityWindow =========================
    def createStaffOnlyFunctionalityWindow(self):

        # Create blank staffOnlyFunctionalityWindow
        self.staffOnlyFunctionalityWindow = Toplevel()
        self.staffOnlyFunctionalityWindow.title("Atlanta Betline : Staff Only")
        self.staffOnlyFunctionalityWindow.geometry("500x300")

    def buildStaffOnlyFunctionalityWindow(self,staffOnlyFunctionalityWindow):

        staffOnlyFunctionalityLabel = Label(staffOnlyFunctionalityWindow, text="Staff Functionality", font="Verdana 14 bold ")
        staffOnlyFunctionalityLabel.grid(row=1, column=2, sticky=W + E,pady=3)

        # Manage Profile
        staffManageProfile = Button(staffOnlyFunctionalityWindow, text="Manage Profile",command =self.manageProfile_StaffOnlyFunctionalityWindow)
        staffManageProfile.grid(row=2, column=2,sticky=W+E,pady=3)
        # View schedule
        staffViewSiteReport = Button(staffOnlyFunctionalityWindow, text="View Schedule",command = self.viewSite_StaffOnlyFunctionalityWindow)
        staffViewSiteReport.grid(row=3, column=2,sticky=W+E,pady=3)
        # take transit
        staffManageEvent = Button(staffOnlyFunctionalityWindow, text="Take Transit",command =self.takeTransit_StaffOnlyFunctionalityWindow)
        staffManageEvent.grid(row=4, column=2,sticky=W+E,pady=3)
        # view History
        staffTakeTransit = Button(staffOnlyFunctionalityWindow, text="View Transit History",command=self.viewHistory_StaffOnlyFunctionalityWindow)
        staffTakeTransit.grid(row=5, column=2,sticky=W+E,pady=3)
        # View Staff
        staffViewStaff = Button(staffOnlyFunctionalityWindow, text="Back",command=self.back_StaffOnlyFunctionalityWindow)
        staffViewStaff.grid(row=6, column=2,sticky=W+E,pady=3)

    def manageProfile_StaffOnlyFunctionalityWindow(self):
        self.createEmployeeManageProfileWindow()
        self.buildEmployeeManageProfileWindow(self.employeeManageProfileWindow)
        self.previous = self.staffOnlyFunctionalityWindow
        self.staffOnlyFunctionalityWindow.withdraw()

    def viewSite_StaffOnlyFunctionalityWindow(self):
        self.createStaffViewScheduleWindow()
        self.buildStaffViewScheduleWindow(self.staffViewScheduleWindow)
        self.previous = self.staffOnlyFunctionalityWindow
        self.staffOnlyFunctionalityWindow.withdraw()

    def takeTransit_StaffOnlyFunctionalityWindow(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.staffOnlyFunctionalityWindow
        self.staffOnlyFunctionalityWindow.withdraw()

    def viewHistory_StaffOnlyFunctionalityWindow(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        self.previous = self.staffOnlyFunctionalityWindow
        self.staffOnlyFunctionalityWindow.withdraw()

    def back_StaffOnlyFunctionalityWindow(self):
        self.staffOnlyFunctionalityWindow.withdraw()
        self.loginWindow.deiconify()

#================== 13-staffVisitorFunctionalityWindow =========================

    def createStaffVisitorFunctionalityWindow(self):

        # Create blank staffVisitorFunctionalityWindow
        self.staffVisitorFunctionalityWindow = Toplevel()
        self.staffVisitorFunctionalityWindow.title("Atlanta Betline : staff-Visitor")
        self.staffVisitorFunctionalityWindow.geometry("500x300")

    def buildStaffVisitorFunctionalityWindow(self,staffVisitorFunctionalityWindow):

        staffVisitorFunctionalityLabel = Label(staffVisitorFunctionalityWindow, text="staff Functionality", font="Verdana 14 bold ")
        staffVisitorFunctionalityLabel.grid(row=1, column=1, sticky=W+E,pady=3)

        # Manage Profile
        staffManageProfile = Button(staffVisitorFunctionalityWindow, text="Manage Profile",command = self.manageProfile_StaffVisitorFunctionalityWindow)
        staffManageProfile.grid(row=2, column=1,sticky=W+E,pady=3)
        # Manage Event
        staffManageEvent = Button(staffVisitorFunctionalityWindow, text="Explore Event",command = self.exploreEvent_StaffVisitorFunctionalityWindow)
        staffManageEvent.grid(row=2, column=2,sticky=W+E,pady=3)
        # View Staff
        staffViewStaff = Button(staffVisitorFunctionalityWindow, text="View Schedule",command = self.viewSchedule_StaffVisitorFunctionalityWindow)
        staffViewStaff.grid(row=3, column=1,sticky=W+E,pady=3)
        # View Site Report
        staffViewSiteReport = Button(staffVisitorFunctionalityWindow, text="Explore Site",command = self.exploreSite_StaffVisitorFunctionalityWindow)
        staffViewSiteReport.grid(row=3, column=2,sticky=W+E,pady=3)
        # Explore Site
        exploreSite = Button(staffVisitorFunctionalityWindow, text="Take Transit",command = self.takeTransit_StaffVisitorFunctionalityWindow)
        exploreSite.grid(row=4, column=1,sticky=W+E,pady=3)
        # Explore Event
        exploreEvent = Button(staffVisitorFunctionalityWindow, text="View Visit History",command = self.viewVisitHistory_StaffVisitorFunctionalityWindow)
        exploreEvent.grid(row=4, column=2,sticky=W+E,pady=3)
        # Take Transit
        staffTakeTransit = Button(staffVisitorFunctionalityWindow, text="View Transit History",command = self.viewTransitHistory_StaffVisitorFunctionalityWindow)
        staffTakeTransit.grid(row=5, column=1,sticky=W+E,pady=3)
        # View Transit History
        staffViewTransitHistory = Button(staffVisitorFunctionalityWindow, text="Back",command =self.back_StaffVisitorFunctionalityWindow )
        staffViewTransitHistory.grid(row=5, column=2,sticky=W+E,pady=3)

    def manageProfile_StaffVisitorFunctionalityWindow(self):
        self.createEmployeeManageProfileWindow()
        self.buildEmployeeManageProfileWindow(self.employeeManageProfileWindow)
        self.previous = self.staffVisitorFunctionalityWindow
        self.staffVisitorFunctionalityWindow.withdraw()

    def viewSite_StaffVisitorFunctionalityWindow(self):
        self.createStaffViewScheduleWindow()
        self.buildStaffViewScheduleWindow(self.staffViewScheduleWindow)
        self.previous = self.staffVisitorFunctionalityWindow
        self.staffVisitorFunctionalityWindow.withdraw()

    def takeTransit_StaffVisitorFunctionalityWindow(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.staffVisitorFunctionalityWindow
        self.staffVisitorFunctionalityWindow.withdraw()

    def viewTransitHistory_StaffVisitorFunctionalityWindow(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        self.previous = self.staffVisitorFunctionalityWindow
        self.staffVisitorFunctionalityWindow.withdraw()

    def viewVisitHistory_StaffVisitorFunctionalityWindow(self):
        self.createViewVisitHistoryWindow()
        self.buildViewVisitHistoryWindow(self.viewVisitHistoryWindow )
        self.previous = self.staffVisitorFunctionalityWindow
        self.staffVisitorFunctionalityWindow.withdraw()

    def exploreEvent_StaffVisitorFunctionalityWindow(self):
        self.createExploreEventWindow()
        self.buildExploreEventWindow(self.exploreEventWindow)
        self.previous = self.staffVisitorFunctionalityWindow
        self.staffVisitorFunctionalityWindow.withdraw()

    def exploreSite_StaffVisitorFunctionalityWindow(self):
        self.createExploreSiteWindow()
        self.buildExploreSiteWindow(self.exploreSiteWindow)
        self.previous = self.staffVisitorFunctionalityWindow
        self.staffVisitorFunctionalityWindow.withdraw()

    def viewSchedule_StaffVisitorFunctionalityWindow(self):
        self.createStaffViewScheduleWindow()
        self.buildStaffViewScheduleWindow(self.staffViewScheduleWindow)
        self.previous = self.staffVisitorFunctionalityWindow
        self.staffVisitorFunctionalityWindow.withdraw()

    def back_StaffVisitorFunctionalityWindow(self):
        self.staffVisitorFunctionalityWindow.withdraw()
        self.loginWindow.deiconify()

##========== 14 Visitor Choose Functionality Window================

    def createChooseFunctionalityWindow(self):
        self.chooseFunctionalityWindow = Tk()
        self.chooseFunctionalityWindow.title("AtlantaBeltline: Visitor")
        self.chooseFunctionalityWindow.withdraw()
        self.chooseFunctionalityWindow.update_idletasks()  # Update "requested size" from geometry manager
        x = (self.chooseFunctionalityWindow.winfo_screenwidth() - self.chooseFunctionalityWindow.winfo_reqwidth()) / 2
        y = (self.chooseFunctionalityWindow.winfo_screenheight() - self.chooseFunctionalityWindow.winfo_reqheight()) / 2
        self.chooseFunctionalityWindow.geometry("+%d+%d" % (x, y))
        self.chooseFunctionalityWindow.deiconify()

    def buildChooseFunctionalityWindow(self,chooseFunctionalityWindow):
        chooseFunctionalityLabel = Label(chooseFunctionalityWindow, text="Visitor Functionality",font = "Verdana 10 bold ")
        chooseFunctionalityLabel.grid(row=1, column=1, sticky=W+E,  padx=15, pady=15)

        exploreEvent = Button(chooseFunctionalityWindow, text="Explore Event", command=self.exploreEvent)
        exploreEvent.grid(row=3, column=1,sticky=W+E, padx=15, pady=5)

        exploreSite = Button(chooseFunctionalityWindow, text="Explore Site", command=self.exploreSite)
        exploreSite.grid(row=4, column=1,sticky=W+E, padx=15, pady=5)

        viewVisitHistory = Button(chooseFunctionalityWindow, text="View Visit History", command=self.viewVisitHistory)
        viewVisitHistory.grid(row=5, column=1,sticky=W+E, padx=15, pady=5)

        takeTransit = Button(chooseFunctionalityWindow, text="Take Transit",
                              command=self.takeTransit)
        takeTransit.grid(row=6, column=1,sticky=W+E, padx=15, pady=5)

        viewTransitHistory = Button(chooseFunctionalityWindow, text="View Transit History",
                              command=self.viewTransitHistory)
        viewTransitHistory.grid(row=7, column=1,sticky=W+E, padx=15, pady=5)

        backButton = Button(chooseFunctionalityWindow, text="Back",
                                command=self.chooseFunctionalityWindowBackButtonClicked)
        backButton.grid(row=8, column=1,sticky=W+E, padx=15, pady=5)

    def exploreEvent(self):
        self.createExploreEventWindow()
        self.buildExploreEventWindow(self.exploreEventWindow)
        self.previous = self.chooseFunctionalityWindow
        self.chooseFunctionalityWindow.withdraw()

    def exploreSite(self):
        self.createExploreSiteWindow()
        self.buildExploreSiteWindow(self.exploreSiteWindow)
        self.previous = self.chooseFunctionalityWindow
        self.chooseFunctionalityWindow.withdraw()

    def viewVisitHistory(self):
        self.createViewVisitHistoryWindow()
        self.buildViewVisitHistoryWindow(self.viewVisitHistoryWindow)
        self.previous = self.chooseFunctionalityWindow
        self.chooseFunctionalityWindow.withdraw()

    def takeTransit(self):
        self.createTakeTransitWindow()
        self.buildTakeTransitWindow(self.takeTransitWindow)
        self.previous = self.chooseFunctionalityWindow
        self.chooseFunctionalityWindow.withdraw()

    def viewTransitHistory(self):
        self.createTransitHistory()
        self.buildTransitHistory(self.transitHistoryWindow)
        selfpreviouus = self.chooseFunctionalityWindow
        self.chooseFunctionalityWindow.withdraw()

    def chooseFunctionalityWindowBackButtonClicked(self):
        self.chooseFunctionalityWindow.destroy()
        self.loginWindow.deiconify()

#=========Screen 15 Take Transit Window============
    def createTakeTransitWindow(self):
        self.takeTransitWindow = Toplevel()
        self.takeTransitWindow.title("Take Transit")

    def buildTakeTransitWindow(self,takeTransitWindow):
        self.result_searchForExhibit_Visitor = []
        # Title Label
        viewExhibitLabel = Label(takeTransitWindow, text="Take Transit", font="Verdana 20 bold ")
        viewExhibitLabel.grid(row=1, column=2, sticky=W + E)

        # site label
        viewContainSiteLabel = Label(takeTransitWindow, text="Site", font="Verdana 10 bold")
        viewContainSiteLabel.grid(row=3, column=1)
        SQLCommand = "SELECT DISTINCT SiteName from Connect"
        self.cursor.execute(SQLCommand)
        SiteTuple = self.cursor.fetchall()
        SiteList = []
        for element in SiteTuple: SiteList.append(element[0])
        Site = StringVar()
        Site.set(SiteList[0])
        SiteMenu = OptionMenu(takeTransitWindow, Site, *SiteList)
        SiteMenu.config(width= 20)
        SiteMenu.grid(row=3, column=2)

        #transport type
        viewTransportTypeLabel = Label(takeTransitWindow, text="Transport Type", font="Verdana 10 bold ")
        viewTransportTypeLabel.grid(row=3, column=3,sticky=E,pady=5)
        TransportTypeList = ["--ALL--","MARTA","Bus","Bike"]
        TransportType = StringVar()
        TransportType.set(TransportTypeList[0])
        TransportTypeMenu = OptionMenu(takeTransitWindow, TransportType, *TransportTypeList)
        TransportTypeMenu.config(width= 10)
        TransportTypeMenu.grid(row=3, column=4)
        TransportTypeMenu.config(bg = "gray97", relief=GROOVE)

        # price range label
        priceRangeLabel = Label(takeTransitWindow, text = "Price Range", font = "Verdana 10 bold")
        priceRangeLabel.grid(row=5, column = 1)
        minPrice = StringVar()
        minPriceEntry = Entry(takeTransitWindow, textvariable=minPrice, width=10)
        minPriceEntry.grid(row=5, column=2)
        dash = Label(takeTransitWindow, text = "-", font = "Verdana 10 bold")
        dash.grid(row=5, column = 3)
        maxPrice = StringVar()
        maxPriceEntry = Entry(takeTransitWindow, textvariable=maxPrice, width=10)
        maxPriceEntry.grid(row=5, column=4)

        def filterBottonFun():
            self.filterTakeTransit_15(TransportType.get(), Site.get(), minPrice.get(), maxPrice.get())

        # filter Button
        filterButton = Button(takeTransitWindow, text="Filter", command=filterBottonFun)
        filterButton.grid(row=5, column=5)

        # back Button
        backButton = Button(takeTransitWindow, text="Return", command=self.takeTransitWindowBackButtonClicked)
        backButton.grid(row=8, column=1)

        # transite date label
        transitDateLabel = Label(takeTransitWindow, text = "Transit Date", font = "Verdana 10 bold")
        transitDateLabel.grid(row=8, column = 2)
        transitDate = StringVar()
        date = Entry(takeTransitWindow, textvariable=transitDate, width=10)
        date.grid(row=8, column=3)

        def logTransitButtonClicked():
            curItem = self.tv.item(self.tv.focus())
            print(curItem)
            LogRoute = str(curItem['values'][0])
            LogType = curItem['values'][1]
            self.logTransit_15(str(LogRoute), str(LogType), str(transitDate.get()))

        # log transit label
        logTransitLabel = Button(takeTransitWindow, text = "Log Transit", command=logTransitButtonClicked)
        logTransitLabel.grid(row=8, column = 5)

        # search table
        self.tv = ttk.Treeview(takeTransitWindow)
        self.tv['columns'] = ("Route", "Transport Type", "Price", "Connected Sites")

        self.tv.heading("Route", text='Route', anchor='w')
        self.tv.column("Route", minwidth=2)

        self.tv.heading("Transport Type", text="Transport Type", anchor='w')
        self.tv.column("Transport Type",  minwidth=2)

        self.tv.heading("Price", text="Price")
        self.tv.column("Price", minwidth=2)

        self.tv.heading("Connected Sites", text="# Connected Sites")
        self.tv.column("Connected Sites",  minwidth=2)

        self.tv['show'] = 'headings'
        self.tv.grid(row=7, column=1, columnspan = 5  )

    def logTransit_15(self, Route, TransportType, Date):

        if Date and Route:
            print("\nLog Transit\n")
        else:
            messagebox.showwarning("Please Date and Route.")

        self.searchEmployeeInformation()################################################### do it in login window
        print(self.Username)
        sql = "INSERT INTO TakeTransit (Username, TransitType,TransitRoute,TransitDate) VALUES ( '"+self.Username+"', '"+TransportType+"', '"+Route+"', '"+Date+"' );"
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def filterTakeTransit_15(self, TransportType, Site, minPrice, maxPrice):

        SQL = "SELECT T.TransitRoute, T.TransitType, TransitPrice from Transit T join Connect C on C.TransitType=T.TransitType and C.TransitRoute=T.TransitRoute"

        SQL+=" where "
        index = 0;#how many conditions have been added

        if Site:
            SQL = SQL + " SiteName = '"+Site+"'";
            index+=1;
        if TransportType != "--ALL--":
            if index >0: SQL+=" AND "
            SQL = SQL + " T.TransitType = '"+  TransportType+"'";
            index+=1;
        if minPrice:
            if index >0: SQL+=" AND "
            SQL = SQL + " T.TransitPrice >= '"+minPrice+"'";
            index+=1;
        if maxPrice:
            if index >0: SQL+=" AND "
            SQL = SQL + " TransitPrice <= '"+maxPrice+"'";
            index+=1;
        SQL = SQL+';'
        print(SQL)
        self.cursor.execute(SQL)
        temp= self.cursor.fetchall()
        print(temp)
        TransitType = []
        TransitRoute = []
        TransitPrice = []
        SiteCounted = []
        for i in range(len(temp)):
            TransitType.append(str(temp[i][0]))
            TransitRoute.append(temp[i][1])
            TransitPrice.append(str(temp[i][2]))
        for i in range(len(TransitRoute)):
            SQL = "SELECT count(*) FROM Connect where TransitType = '"+TransitType[i]+"' and TransitRoute = '"+TransitRoute[i]+"';"
            self.cursor.execute(SQL)
            temp2= self.cursor.fetchall()
            SiteCounted.append(temp2[0][0])
        j=0
        self.tv.delete(*self.tv.get_children())
        for i in range(len(TransitRoute)):
            self.tv.insert("",j, value=(str(TransitType[i]),str(TransitRoute[i]),str(TransitPrice[i]),str(SiteCounted[i])))
            j+=1

        self.db.commit()

    def takeTransitWindowBackButtonClicked(self):
        self.takeTransitWindow.destroy()
        self.previous.deiconify()

#==========Screen 16 User Transit History=======================#

    def createTransitHistory(self):
        self.transitHistoryWindow = Toplevel()
        self.transitHistoryWindow.title("Transit History")
        self.transitHistoryWindow.columnconfigure(1, weight=1)
        self.transitHistoryWindow.geometry("850x400")

    def buildTransitHistory(self,transitHistoryWindow):

        viewTransitHistoryLabel = Label(transitHistoryWindow, text = "Transit History", font = ("Verdana", 20))
        viewTransitHistoryLabel.grid(row=2, column=4, sticky=W,pady=3)

        #transport type
        viewTransportTypeLabel = Label(transitHistoryWindow, text="Transport Type", font="Verdana 10 bold ")
        viewTransportTypeLabel.grid(row=3, column=2,sticky=E,pady=5,padx=5)
        TransportTypeList = ["--ALL--","MARTA","Bus","Bike"]
        TransportType = StringVar()
        TransportType.set(TransportTypeList[0])
        TransportTypeMenu = OptionMenu(transitHistoryWindow, TransportType, *TransportTypeList)
        TransportTypeMenu.config(width= 10)
        TransportTypeMenu.grid(row=3, column=3,sticky=W,pady=5,padx=5)
        TransportTypeMenu.config(bg = "gray97", relief=GROOVE)

        #contain site
        viewContainSiteLabel = Label(transitHistoryWindow, text="Contain Site", font="Verdana 10 bold")
        viewContainSiteLabel.grid(row=3, column=4,sticky=E,pady=5,padx=5)
        SQLCommand = "SELECT DISTINCT SiteName from VisitSite"
        self.cursor.execute(SQLCommand)
        SiteTuple = self.cursor.fetchall()
        SiteList = []
        for element in SiteTuple: SiteList.append(element[0])
        Site = StringVar()
        Site.set(SiteList[0])
        SiteMenu = OptionMenu(transitHistoryWindow, Site, *SiteList)
        SiteMenu.config(width= 20)
        SiteMenu.grid(row=3, column=5,sticky=W,pady=5,padx=5)

        #route
        viewRouteLabel = Label(transitHistoryWindow, text="Route", font="Verdana 10 bold")
        viewRouteLabel.grid(row=4, column=2,sticky=W,pady=5,padx=5)
        Route = StringVar()
        showRoute = Entry(transitHistoryWindow, textvariable=Route)
        showRoute.config(width= 10)
        showRoute.grid(row=4, column=2, sticky=E,pady=5,padx=5)

        #Start date
        viewStartDateLabel = Label(transitHistoryWindow, text="Start Date", font="Verdana 10 bold")
        viewStartDateLabel.grid(row=4, column=3,sticky=E,pady=5,padx=5)
        StartDate= StringVar(value='YYYY-MM-DD')
        showStartDate = Entry(transitHistoryWindow, textvariable=StartDate, width=10)
        showStartDate.grid(row=4, column=4,sticky=W,pady=5,padx=5)

        #End date
        viewEndDateLabel = Label(transitHistoryWindow, text="End Date", font="Verdana 10 bold")
        viewEndDateLabel.grid(row=4, column=4,sticky=E,padx=5,pady=5)
        EndDate= StringVar(value='YYYY-MM-DD')
        showEndDate = Entry(transitHistoryWindow, textvariable=EndDate, width=10)
        showEndDate.grid(row=4, column=5,sticky=W,padx=5,pady=5)

        # TABLE
        self.view_transit_history = ttk.Treeview(transitHistoryWindow)
        self.view_transit_history['columns'] = ("Date", "Route", "Transport Type","Price")

        self.view_transit_history.heading("Date", text='Date', anchor='w')
        self.view_transit_history.column("Date", minwidth=5)

        self.view_transit_history.heading("Route", text="Route", anchor='w')
        self.view_transit_history.column("Route",  minwidth=2)

        self.view_transit_history.heading("Transport Type", text="Transport Type")
        self.view_transit_history.column("Transport Type", minwidth=2)

        self.view_transit_history.heading("Price", text="Price")
        self.view_transit_history.column("Price", minwidth=2)

        self.view_transit_history['show'] = 'headings'
        self.view_transit_history.grid(row=5, column=2, columnspan = 4,sticky=W,padx=5,pady=5)

        def filterBottonFun():
            print(str(TransportType.get()), str(Site.get()),
                  str(Route.get()), str(StartDate.get()), str(EndDate.get()))
            self.filterTransitHistory(TransportType.get(), Site.get(),
                Route.get(), StartDate.get(), EndDate.get())

        FilterButton = Button(transitHistoryWindow, text="Filter", command=filterBottonFun)
        FilterButton.grid(row=15, column=3,pady=5,padx=5)

        #Return Button
        BackButton = Button(transitHistoryWindow, text="Back", command=self.transitHistoryWindowBackButtonClicked)
        BackButton.grid(row=15, column=4,pady=5,padx=5)

    def filterTransitHistory(self,TransportType,Site,Route,StartDate,EndDate):
        SQL = "SELECT TransitDate, C.TransitRoute, C.TransitType, TransitPrice\
        from Connect C\
        join TakeTransit TT on C.TransitType = TT.TransitType and C.TransitRoute = TT.TransitRoute\
        join Transit T on C.TransitType = T.TransitType and C.TransitRoute = T.TransitRoute"

        if TransportType != "--ALL--" or Site or Route or StartDate != "YYYY-MM-DD" or EndDate != "YYYY-MM-DD":
            SQL+=" where "
            index = 0;#how many conditions have been added

        if TransportType != "--ALL--":
            if index >0: SQL+=" AND "
            SQL = SQL + " C.TransitType = '"+  TransportType+"'";
            index+=1;
        if Site:
            if index >0: SQL+=" AND "
            SQL = SQL + " C.SiteName = '"+Site+"'";
            index+=1;
        if Route:
            if index >0: SQL+=" AND "
            SQL = SQL + " C.TransitRoute = '"+Route+"'";
            index+=1;
        if StartDate != "YYYY-MM-DD":
            if index >0: SQL+=" AND "
            SQL = SQL + " TT.TransitDate >= '"+StartDate+"'";
            index+=1;
        if EndDate != "YYYY-MM-DD":
            if index >0: SQL+=" AND "
            SQL = SQL + " TT.TransitDate <= '"+EndDate+"'";
            index+=1;
        SQL = SQL+';'
        print(SQL)

        self.cursor.execute(SQL)
        result_check = self.cursor.fetchall()
        self.view_transit_history.delete(*self.view_transit_history.get_children())
        print(result_check)
        for i, result in enumerate(result_check):
            self.view_transit_history.insert("",i, value=(str(result[0]),str(result[1]),str(result[2]),str(result[3])))
        self.db.commit()

    def transitHistoryWindowBackButtonClicked(self):
        # Click Return Button on Exhibit History Window:
        # Destroy Exhibit History Window
        # Display Choose Functionality Window
        self.transitHistoryWindow.destroy()
        self.previous.deiconify()

#==========17 Employee Manage Profile================================#
    def createEmployeeManageProfileWindow(self):
        self.employeeManageProfileWindow = Toplevel()
        self.employeeManageProfileWindow.title("Employee Manage Profile")
        self.employeeManageProfileWindow.geometry("850x400")

    def buildEmployeeManageProfileWindow(self, employeeManageProfileWindow):
        #get searchEmployeeInformation
        self.searchEmployeeInformation()

        # New User Only Registration Label
        RegisterUserOnlyLabel = Label(employeeManageProfileWindow, text="Manage Profile",font = "Verdana 13 bold ")
        RegisterUserOnlyLabel.grid(row=1, column=3, sticky=W+E)

        # First Name Label
        firstNameLabel = Label(employeeManageProfileWindow, text="First Name")
        firstNameLabel.grid(row=2, column=1,sticky=W)
        # Last Name Label
        lastNameLabel = Label(employeeManageProfileWindow, text="Last Name")
        lastNameLabel.grid(row=2, column=3, sticky=W)
        # Username Label
        userNameLabel = Label(employeeManageProfileWindow, text="Username")
        userNameLabel.grid(row=3, column=1,sticky=W)
        # showUsername Label
        showUserNameLabel = Label(employeeManageProfileWindow, text=self.Username)
        showUserNameLabel.grid(row=3, column=2,sticky=W)
        #site name Label
        siteNameLabel = Label(employeeManageProfileWindow, text="Sitename")
        siteNameLabel.grid(row=3, column=3,sticky=W)
        #site name label/entry
        sql = "SELECT SiteName FROM Site WHERE ManagerUsername = '"+self.Username+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        if temp:
            Sitename = temp[0][0]
            showSiteNameLabel = Label(employeeManageProfileWindow, text=Sitename)
            siteNameLabel.grid(row=3, column=4,sticky=W)
        # EmployeeID Label
        employeeIDLabel = Label(employeeManageProfileWindow, text="EmployeeID")
        employeeIDLabel.grid(row=4, column=1,sticky=W)
        showEmployeeIDLabel = Label(employeeManageProfileWindow, text=self.EmployeeID)
        showEmployeeIDLabel.grid(row=4, column=2,sticky=W)
        # Username Label
        emailLabel = Label(employeeManageProfileWindow, text="Email")
        emailLabel.grid(row=7, column=1,sticky=W)
        # Phone Label
        phoneLabel = Label(employeeManageProfileWindow, text="Phone")
        phoneLabel.grid(row=4, column=3, sticky=W)
        self.employeeManageProfileWindow_Phone = StringVar(value=self.Phone)
        phoneEntry = Entry(employeeManageProfileWindow, textvariable=self.employeeManageProfileWindow_Phone , width=20)
        phoneEntry.grid(row=4, column=4, sticky=W)
        # First Name Entry
        self.employeeManageProfileWindow_FirstName = StringVar(value=self.Firstname)
        firstNameEntry = Entry(employeeManageProfileWindow, textvariable=self.employeeManageProfileWindow_FirstName , width=20)
        firstNameEntry.grid(row=2, column=2, sticky=W)
        # Last Name Entry
        self.employeeManageProfileWindow_LastName = StringVar(value=self.Lastname)
        lastNameEntry = Entry(employeeManageProfileWindow, textvariable=self.employeeManageProfileWindow_LastName, width=20)
        lastNameEntry.grid(row=2, column=4, sticky=W)
        #Address
        addressLabel = Label(employeeManageProfileWindow,text="Address")
        addressLabel.grid(row=5, column=1,sticky=W)
        showAddressLabel = Label(employeeManageProfileWindow,text=self.EmployeeAddress+", "+self.EmployeeCity+", "+self.EmployeeState+" "+self.EmployeeZipcode)
        showAddressLabel.grid(row=5, column=2,sticky=W)
        #check Button visitor
        sql = "Select Username from Visitor where Username = '"+self.Username+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        if len(temp)>0:
            self.isVisitor = StringVar(value='YES');
        else:
            self.isVisitor = StringVar(value='NO');
        visitorLabel = Label(employeeManageProfileWindow,text="Is this a Visitor Account? (YES/NO)")
        visitorLabel.grid(row=6, column=1,sticky=W)
        checkVisitorButton = Entry(employeeManageProfileWindow,textvariable=self.isVisitor, width = 5)
        checkVisitorButton.grid(row=6, column=2,sticky=W)

        # Email Address Entry
        EntryRow = 7
        Email = [] #can be used to update database
        EmailLabels = []
        removeButton=[]
        EmailAddress = StringVar()
        emailAddressEntry = Entry(employeeManageProfileWindow, textvariable=EmailAddress,width=20)

        sql = "select Email from UserEmail where UserName = '"+self.Username+"';"
        self.cursor.execute(sql)
        temp=self.cursor.fetchall()
        if temp:
            for element in temp:
                Email.append(element[0])
                EntryRow = EntryRow + 1
                temp = Button(employeeManageProfileWindow, text='remove', command=lambda: removeRow(self,temp,EntryRow,Email,EmailLabels,removeButton,emailAddressEntry,backButton,updateButton))
                removeButton.append(temp)
                tempEmailLabel = Label(employeeManageProfileWindow, text=element[0])
                EmailLabels.append(tempEmailLabel)

         #reconfigurate
        def reConfig(self,EntryRow,EmailLabels,removeButton,emailAddressEntry,backButton,updateButton ):
            for i in range(len(Email)):
                removeButton[i].grid(row=7+i, column=3,sticky=W)
                EmailLabels[i].grid(row=7+i, column=2,sticky=W)
            self.addButton_employeeManageProfileWindow.grid(row=EntryRow, column=3,sticky=W)
            emailAddressEntry.grid(row=EntryRow, column=2,sticky=W)
            backButton.grid(row=EntryRow+1, column=3)
            updateButton.grid(row=EntryRow+1, column=2)

        def removeRow(self,temp,EntryRow,Email,EmailLabels,removeButton,emailAddressEntry,backButton,updateButton):
            indexToRemove = removeButton.index(temp)
            for i in range(len(Email)):
                removeButton[i].grid_remove()
                removeButton[i].destroy()
                EmailLabels[i].grid_remove()
                EmailLabels[i].destroy()
            del Email[indexToRemove]
            EntryRow = len(Email)+7
            removeButton=[]
            EmailLabels = []
            #addButton.grid_remove()
            #addButton.destroy()
            for i in range(len(Email)):
                temp = Button(employeeManageProfileWindow, text='remove', command=lambda: removeRow(self,temp,EntryRow,Email,EmailLabels,removeButton,emailAddressEntry,backButton,updateButton))
                removeButton.append(temp)
                tempEmailLabel = Label(employeeManageProfileWindow, text=Email[i])
                EmailLabels.append(tempEmailLabel)
            #addButton = Button(employeeManageProfileWindow, text="Add", command=lambda: addRow(EntryRow,Email,EmailLabels,removeButton,emailAddressEntry,EmailAddress,addButton,backButton,updateButton))
            reConfig(self,EntryRow,EmailLabels,removeButton,emailAddressEntry,backButton,updateButton)

        def addRow(self,EntryRow,Email,EmailLabels,removeButton,emailAddressEntry,EmailAddress,backButton,updateButton):
            Email.append(EmailAddress.get())
            EntryRow = EntryRow + 1
            self.addButton_employeeManageProfileWindow.destroy()
            self.addButton_employeeManageProfileWindow = Button(employeeManageProfileWindow, text="Add", command=lambda: addRow(self,EntryRow,Email,EmailLabels,removeButton,emailAddressEntry,EmailAddress,backButton,updateButton))
            #creat remove button
            temp = Button(employeeManageProfileWindow, text='remove', command=lambda: removeRow(self,temp,EntryRow,Email,EmailLabels,removeButton,emailAddressEntry,backButton,updateButton))
            removeButton.append(temp)
            tempEmailLabel = Label(employeeManageProfileWindow, text=EmailAddress.get())
            EmailLabels.append(tempEmailLabel)

            reConfig(self,EntryRow,EmailLabels,removeButton,emailAddressEntry,backButton,updateButton)

        # Create Add Button
        backButton = Button(employeeManageProfileWindow, text="back",command=self.managerManageProfileBackButtonClicked)
        updateButton = Button(employeeManageProfileWindow, text="update")
        self.addButton_employeeManageProfileWindow = Button(employeeManageProfileWindow, text="Add", command=lambda: addRow(self,EntryRow,Email,EmailLabels,removeButton,emailAddressEntry,EmailAddress,backButton,updateButton))
        reConfig(self,EntryRow,EmailLabels,removeButton,emailAddressEntry,backButton,updateButton)

    def employeeManageProfileUpdateButtonClicked(self,Email,Phone,Firstname,Lastname,isVisitor):
        #print(Email,Phone,self.Phone,Firstname,Lastname,isVisitor)
        if Phone != self.Phone:
            sql = "UPDATE Employee SET Phone ='"+Phone+"' where Username = '"+self.Username+"';"
            self.cursor.execute(sql)
            self.Phone = Phone
        if Firstname != self.Firstname:
            sql = "UPDATE User SET Phone ='"+Firstname+"' where Username = '"+self.Username+"';"
            self.cursor.execute(sql)
            self.Firstname = Firstname
        if Lastname != self.Lastname:
            sql = "UPDATE User SET Phone ='"+Lastname+"' where Username = '"+self.Username+"';"
            self.cursor.execute(sql)
            self.Firstname = Lastname
        sql = "SELECT * FROM Visitor where Username='"+self.Username+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        if len(temp)>0 and isVistor=='NO':
            sql ="DELETE FROM Visitor where Username='"+self.Username+"';"
            self.cursor.execute(sql)
        elif len(temp)==0 and isVisitor =='YES':
            sql ="Insert into Visitor(Username) Values('"+self.Username+"');"
            self.cursor.execute(sql)

        sql = "Select Email from UserEmail;"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        existEmail =[]
        for element in temp:
            existEmail.append(element[0])
        for element in Email:
            if element not in existEmail:
                sql="Insert into UserEmail(Username,Email) values('"+self.Username+"','"+element+"');"
                self.cursor.execute(sql)
        self.db.commit()

    def managerManageProfileBackButtonClicked(self):
        self.employeeManageProfileWindow.withdraw()
        print("getback")
        self.previous.deiconify()

#============ 18-AdministratorManageUserWindow ============================
    def createAdminManageUserWindow(self):
        self.manageUserWindow = Toplevel()
        self.manageUserWindow.title("Administrator Manage User")

    def buildAdminManageUserWindow(self,manageUserWindow):
        # Title
        manageUserLabel = Label(manageUserWindow, text="Manage User", font="Verdana 14 bold ")
        manageUserLabel.grid(row=1, column=1, sticky=W + E)

        # Username
        usernameLabel = Label(manageUserWindow, text="Username", font="Verdana 10")
        usernameLabel.grid(row=2, column=1)
        username = StringVar()
        username.set("")
        nameEntry = Entry(manageUserWindow, textvariable=username, width=10)
        nameEntry.grid(row=2, column=2)
        # Type
        typeLabel = Label(manageUserWindow, text="Type", font="Verdana 10")
        typeLabel.grid(row=2, column=4)
        typeList = ["User","Visitor","Staff","Manager"]
        typeSelected = StringVar()
        typeSelected.set(typeList[0])
        typeMenu = OptionMenu(manageUserWindow, typeSelected, *typeList)
        typeMenu.config(width= 10)
        typeMenu.grid(row=2, column=5)
        # Status
        statusLabel = Label(manageUserWindow, text="Status", font="Verdana 10")
        statusLabel.grid(row=2, column=8)
        statusList = ["--All--","Approved","Pending","Declined"]
        statusSelected = StringVar()
        statusSelected.set(statusList[0])
        statusMenu = OptionMenu(manageUserWindow, statusSelected, *statusList)
        statusMenu.config(width= 10)
        statusMenu.grid(row=2, column=9)

        # Filter
        def manageUserWindowFilterBottonFun():
            self.filterUser(username.get(),typeSelected.get(),statusSelected.get())
        filterUserButton = Button(manageUserWindow, text="Filter", command=manageUserWindowFilterBottonFun)
        filterUserButton.grid(row=3, column=1)

        # Approve
        def manageUserWindowApproveBottonFun():
            self.approveUser(self.user_detail_table.focus())
        approveButton = Button(manageUserWindow, text="Approve", command=manageUserWindowApproveBottonFun)
        approveButton.grid(row=3, column=7)

        # Decline
        def manageUserWindowDeclineBottonFun():
            self.declineUser(self.user_detail_table.focus())
        declineButton = Button(manageUserWindow, text="Decline", command=manageUserWindowDeclineBottonFun)
        declineButton.grid(row=3, column=9)

        # Table
        self.user_detail_table = ttk.Treeview(manageUserWindow)
        self.user_detail_table['columns'] = ("Username", "Email count", "User Type", "Status")

        self.user_detail_table.heading("Username", text='     Username     ▼', anchor='w')
        self.user_detail_table.column("Username", minwidth=2)

        self.user_detail_table.heading("Email count", text=" Email count ▼", anchor='w')
        self.user_detail_table.column("Email count",  minwidth=2)

        self.user_detail_table.heading("User Type", text="    User Type    ▼")
        self.user_detail_table.column("User Type", minwidth=2)

        self.user_detail_table.heading("Status", text="   Status   ▼")
        self.user_detail_table.column("Status",  minwidth=2)

        self.user_detail_table['show'] = 'headings'
        self.user_detail_table.grid(row=4, column=1, columnspan =9)

        # Back
        backButton = Button(manageUserWindow, text="Back", command = self.manageUserWindowBackButtom) #luna
        backButton.grid(row=5, column=9)

    def manageUserWindowBackButtom(self): # NOT DONE #luna
        self.manageUserWindow.destroy()
        self.previous.deiconify()

    def filterUser(self, username, usertype, status): #luna
        # username, status, {type}, emailCount
        self.user_detail_table.delete(*self.user_detail_table.get_children())
        sql = "SELECT Username, Status FROM User"
        if username or status != "--All--":
            sql += " WHERE "
            index = 0
        if username :
            if index >0: sql+=" AND "
            sql += "Username = '"+username+"'"
            index+=1
        if status != "--All--":
            if index >0: sql+=" AND "
            sql += "Status = '"+status+"'"
        sql += ";"
        self.cursor.execute(sql)
        result = list(map(list,self.cursor.fetchall()))
        for i in range(len(result)):
            person = result[i]
            person.append({'UserType':[]})
            sql_visitor= "SELECT * FROM Visitor WHERE Username = '"+person[0]+"';"
            sql_staff= "SELECT * FROM Staff WHERE Username = '"+person[0]+"';"
            sql_manager= "SELECT * FROM Manager WHERE Username = '"+person[0]+"';"
            self.cursor.execute(sql_visitor)
            if self.cursor.fetchall():
                person[2]['UserType'].append('Visitor')
            self.cursor.execute(sql_staff)
            if self.cursor.fetchall():
                person[2]['UserType'].append('Staff')
            self.cursor.execute(sql_manager)
            if self.cursor.fetchall():
                person[2]['UserType'].append('Manager')
            sql = "SELECT COUNT(*) FROM UserEmail WHERE Username = '"+person[0]+"';"
            self.cursor.execute(sql)
            emailCount = self.cursor.fetchall()[0]
            person.append(emailCount[0])
            result[i] = person
        i = 0
        for p in result:
            if usertype == "User":
                i+=1
                self.user_detail_table.insert("",i,value=(p[0],p[3],p[2]['UserType'],p[1]))
            elif usertype in p[2]['UserType']:
                i+=1
                self.user_detail_table.insert("",i,value=(p[0],p[3],p[2]['UserType'],p[1]))

    def approveUser(self, selection):
        person = self.user_detail_table.item(selection)['values']
        sql = "UPDATE User SET Status = 'Approved' WHERE Username = '"+person[0]+"';"
        self.cursor.execute(sql)
        self.db.commit()
        person[3] = "Approved"
        self.user_detail_table.item(selection,values=person)

    def declineUser(self, selection):
        person = self.user_detail_table.item(selection)['values']
        sql = "UPDATE User SET Status = 'Declined' WHERE Username = '"+person[0]+"';"
        self.cursor.execute(sql)
        self.db.commit()
        person[3] = "Declined"
        self.user_detail_table.item(selection, values=person)

#==================19=======================

    def createAdminManageSiteWindow(self):
        self.manageSiteWindow = Toplevel()
        self.manageSiteWindow.title("Administrator Manage Site")
        self.manageSiteWindow.geometry("700x500")

    def buildAdminManageSiteWindow(self,manageSiteWindow):
        # Title
        manageSiteLabel = Label(manageSiteWindow, text="Manage Site", font="Verdana 14 bold ")
        manageSiteLabel.grid(row=1, column=1, sticky=W + E)

        # Site
        siteLabel = Label(manageSiteWindow, text="Site", font="Verdana 10")
        siteLabel.grid(row=2, column=1)
        sql = "SELECT SiteName FROM Site;"
        self.cursor.execute(sql)
        siteTuple = self.cursor.fetchall()
        siteList = []
        siteList.append("--All--")
        for i in siteTuple:
            siteList.append(i[0])
        siteSelect = StringVar()
        siteSelect.set(siteList[0])
        siteMenu = OptionMenu(manageSiteWindow, siteSelect, *siteList)
        siteMenu.config(width= 10)
        siteMenu.grid(row=2, column=2)

        # Manager
        managerLabel = Label(manageSiteWindow, text="Manager", font="Verdana 10")
        managerLabel.grid(row=2, column=3)
        sql = "SELECT Username FROM Manager;"
        self.cursor.execute(sql)
        managerTuple = self.cursor.fetchall()
        managerList = []
        managerList.append("--All--")
        for i in managerTuple:
            managerList.append(i[0])
        managerSelect = StringVar()
        managerSelect.set(managerList[0])
        managerMenu = OptionMenu(manageSiteWindow, managerSelect, *managerList)
        managerMenu.config(width= 15)
        managerMenu.grid(row=2, column=4)

        # Open Everyday
        openEverydayLabel = Label(manageSiteWindow, text="Open Everyday", font="Verdana 10")
        openEverydayLabel.grid(row=3, column=2)
        openEveryday = ["--All--","Yes", "No"]
        openSelected = StringVar()
        openSelected.set(openEveryday[0])
        openMenu = OptionMenu(manageSiteWindow, openSelected, *openEveryday)
        openMenu.config(width= 15)
        openMenu.grid(row=3, column=3)

        # Filter
        def manageSiteWindowFilterBottonFun():
            self.manageSiteWindow_filterSite(siteSelect.get(),managerSelect.get(),openSelected.get())
        filterSiteButton = Button(manageSiteWindow, text="Filter", command=manageSiteWindowFilterBottonFun)
        filterSiteButton.grid(row=4, column=1)

        # Create
        createButton = Button(manageSiteWindow, text="Create", command=self.manageSiteWindowCreateBottom) #need command
        createButton.grid(row=4, column=2)

        # Edit
        def manageSiteWindowEditBottom():
            self.editSite(self.site_detail_table.focus())
        editButton = Button(manageSiteWindow, text="Edit", command=manageSiteWindowEditBottom)
        editButton.grid(row=4, column=3)

        # Delete
        deleteButton = Button(manageSiteWindow, text="Delete",command = self.site_delete_Button_Clicked)  #need command
        deleteButton.grid(row=4, column=4)

        # Table
        self.site_detail_table = ttk.Treeview(manageSiteWindow)
        self.site_detail_table['columns'] = ("Name","Manager","Open Everyday")

        self.site_detail_table.heading("Name", text='     Name     ▼', anchor='w')
        self.site_detail_table.column("Name", width=200)

        self.site_detail_table.heading("Manager", text="  Manager   ▼", anchor='w')
        self.site_detail_table.column("Manager",  width=150)

        self.site_detail_table.heading("Open Everyday", text="Open Everyday▼")
        self.site_detail_table.column("Open Everyday", width=150)

        self.site_detail_table['show'] = 'headings'
        self.site_detail_table.grid(row=5, column=1, columnspan =4)

        # Back
        backButton = Button(manageSiteWindow, text="Back", command = self.manageSiteWindowBackButtom) #need command
        backButton.grid(row=6, column=4, sticky=E)

    def manageSiteWindowBackButtom(self):
        self.manageSiteWindow.destroy()
        self.previous.deiconify()
        # back to 8/9?
    def site_delete_Button_Clicked(self): #luna
        print ("site_delete_Button_Clicked")
        curItem = self.site_detail_table.item(self.site_detail_table.focus())
        siteName = curItem['values'][0]
        sql = "DELETE FROM Site WHERE Sitename = '"+siteName+"';"
        self.cursor.execute(sql);
        messagebox.showwarning("Delete site successfully!")
        self.db.commit()

    def manageSiteWindowCreateBottom(self):
        self.previous = self.manageSiteWindow
        self.manageSiteWindow.withdraw()
        self.createCreateSiteWindow()
        self.buildCreateSiteWindow(self.createSiteWindow)
        self.createSiteWindow.mainloop()

    def manageSiteWindow_filterSite(self,site, manager, openEveryday): #luna
        self.site_detail_table.delete(*self.site_detail_table.get_children())
        sql = "SELECT SiteName, ManagerUsername, OpenEveryday FROM Site"
        if site != "--All--" or manager != "--All--" or openEveryday != "--All--":
            sql += " WHERE "
            index = 0
        if site != "--All--":
            if index >0: sql+=" AND "
            sql += "SiteName = '"+site+"'"
            index+=1
        if manager != "--All--":
            if index >0: sql+=" AND "
            sql += "ManagerUsername = '"+manager+"'"
        if openEveryday != "--All--":
            if index >0: sql+=" AND "
            sql += "OpenEveryday = '"+openEveryday+"'"
        sql += ";"
        self.cursor.execute(sql)
        result = list(map(list,self.cursor.fetchall()))
        i = 0
        for s in result:
            self.site_detail_table.insert("",i,value=(s[0],s[1],s[2]))

    def editSite(self, selection):
        site = self.site_detail_table.item(selection)['values']
        sql = "SELECT * FROM Site WHERE SiteName ='"+site[0]+"';"
        self.cursor.execute(sql)
        site=list(map(list,self.cursor.fetchall()))[0]
        self.manageSiteWindow.destroy()
        self.createEditSiteWindow()
        self.buildEditSiteWindow(self.editSiteWindow,site)
        self.editSiteWindow.mainloop()

#================== 20-Administrator Edit Site ===================================

    def createEditSiteWindow(self):
        self.editSiteWindow = Toplevel()
        self.editSiteWindow.title("Edit Site")

    def buildEditSiteWindow(self,editSiteWindow,siteInfo): # SiteName, ManagerUsername, SiteAddress, SiteZipcode, OpenEveryday
        # Title
        editSiteLabel = Label(editSiteWindow, text="Edit Site", font="Verdana 14 bold ")
        editSiteLabel.grid(row=1, column=1, sticky=W + E)

        # Name
        sitenameLabel = Label(editSiteWindow, text="Name", font="Verdana 10")
        sitenameLabel.grid(row=2, column=1)
        sitename = StringVar()
        sitename.set(siteInfo[0])
        sitenameEntry = Entry(editSiteWindow, textvariable=sitename, width=20)
        sitenameEntry.grid(row=2, column=2, sticky=W)

        # Zipcode
        zipcodeLabel = Label(editSiteWindow, text="Zipcode", font="Verdana 10")
        zipcodeLabel.grid(row=2, column=3)
        zipcode = StringVar()
        zipcode.set(siteInfo[3])
        zipcodeEntry = Entry(editSiteWindow, textvariable=zipcode, width=10)
        zipcodeEntry.grid(row=2, column=4)

        # Address
        addressLabel = Label(editSiteWindow, text="Address", font="Verdana 10")
        addressLabel.grid(row=3, column=1)
        address = StringVar()
        address.set(siteInfo[2])
        addressEntry = Entry(editSiteWindow, textvariable=address, width=40)
        addressEntry.grid(row=3, column=2, columnspan=3)

        # Manager
        managerLabel = Label(editSiteWindow, text="Manager", font="Verdana 10")
        managerLabel.grid(row=4, column=1)
        sql = "SELECT Username FROM Manager;"
        self.cursor.execute(sql)
        managerTuple = self.cursor.fetchall()
        managerList = []
        managerList.append("")
        for i in managerTuple:
            managerList.append(i[0])
        managerSelect = StringVar()
        managerSelect.set(siteInfo[1])
        managerMenu = OptionMenu(editSiteWindow, managerSelect, *managerList)
        managerMenu.config(width= 15)
        managerMenu.grid(row=4, column=2)

        # Open Everyday
        openEveryday =  StringVar()
        openEveryday.set(siteInfo[4])
        openEverydayBox = Checkbutton(editSiteWindow ,text="Open Everyday" ,variable=openEveryday, command = openEveryday.set("No"))
        openEverydayBox.grid(row=4, column=4)

        # Back
        backButton = Button(editSiteWindow, text="Back", command = self.editSiteWindowBackButtom)
        backButton.grid(row=5, column=1, sticky=E)

        # Update
        def editSiteWindowUpdateButtom(): #luna
            self.updateSite(siteInfo[0],sitename.get(), managerSelect.get(), address.get(), zipcode.get(), openEveryday.get())
        updateButton = Button(editSiteWindow, text="Update", command=editSiteWindowUpdateButtom)
        updateButton.grid(row=5, column=4, sticky=W)

    def editSiteWindowBackButtom(self):
        self.editSiteWindow.destroy()
        self.createAdminManageSiteWindow()
        self.buildAdminManageSiteWindow(self.manageSiteWindow)
        self.manageSiteWindow.mainloop()

    def updateSite(self,oldsitename,sitename,manager,address,zipcode,openEveryday): #luna
        # SiteName, ManagerUsername, SiteAddress, SiteZipcode, OpenEveryday
        if openEveryday == '1':
            openEveryday = "Yes"
        else:
            openEveryday= "No"
        sql = "UPDATE Site SET SiteName = '"+sitename+"', ManagerUsername = '"+manager+"', SiteAddress = '"+address+"', SiteZipcode = '"+zipcode+"', OpenEveryday = '"+openEveryday+"' WHERE SiteName = '"+oldsitename+"';"
        self.cursor.execute(sql)
        self.db.commit()

#================== 21-Administrator Create Site ===================================
    def createCreateSiteWindow(self):
        self.createSiteWindow = Toplevel()
        self.createSiteWindow.title("Create Site")

    def buildCreateSiteWindow(self,createSiteWindow):
        # Title
        createSiteLabel = Label(createSiteWindow, text="Create Site", font="Verdana 14 bold ")
        createSiteLabel.grid(row=1, column=1, sticky=W + E)

        # Name
        sitenameLabel = Label(createSiteWindow, text="Name", font="Verdana 10")
        sitenameLabel.grid(row=2, column=1)
        sitename = StringVar()
        sitenameEntry = Entry(createSiteWindow, textvariable=sitename, width=20)
        sitenameEntry.grid(row=2, column=2, sticky=W)

        # Zipcode
        zipcodeLabel = Label(createSiteWindow, text="Zipcode", font="Verdana 10")
        zipcodeLabel.grid(row=2, column=3)
        zipcode = StringVar()
        zipcodeEntry = Entry(createSiteWindow, textvariable=zipcode, width=10)
        zipcodeEntry.grid(row=2, column=4)

        # Address
        addressLabel = Label(createSiteWindow, text="Address", font="Verdana 10")
        addressLabel.grid(row=3, column=1)
        address = StringVar()
        addressEntry = Entry(createSiteWindow, textvariable=address, width=40)
        addressEntry.grid(row=3, column=2, columnspan=3)

        # Manager
        managerLabel = Label(createSiteWindow, text="Manager", font="Verdana 10")
        managerLabel.grid(row=4, column=1)
        sql = "SELECT Username FROM Manager;" #not sure
        self.cursor.execute(sql)
        managerTuple = self.cursor.fetchall()
        managerList = []
        managerList.append("")
        for i in managerTuple:
            managerList.append(i[0])
        managerSelect = StringVar()
        managerSelect.set(managerList[0])
        managerMenu = OptionMenu(createSiteWindow, managerSelect, *managerList)
        managerMenu.config(width= 15)
        managerMenu.grid(row=4, column=2)

        # Open Everyday
        openEveryday =  StringVar()
        openEveryday.set("No")
        openEverydayBox = Checkbutton(createSiteWindow ,text="Open Everyday" ,variable=openEveryday, command = openEveryday.set("No"))
        openEverydayBox.grid(row=4, column=4)

        # Back
        backButton = Button(createSiteWindow, text="Back", command = self.createSiteWindowBackButtom) #need command
        backButton.grid(row=5, column=1, sticky=E)

        #create
        def creatButtonOneClick(): #luna
            SiteName = sitename.get()
            SiteAddress = address.get()
            SiteZipcode = zipcode.get()
            OpenEveryDate = openEveryday.get()#"Yes or NO"
            ManagerUsername =  managerSelect.get()
            if len(SiteZipcode) == 5 and SiteZipcode.isdigit():
                print("Zipcode input is valid.")
            else:
                messagebox.showwarning("The Zipcode inputed is not a Five digit length!")
                return False
            self.createSiteWindowCreateButtom(SiteName,SiteAddress,SiteZipcode,OpenEveryDate,ManagerUsername)
        # Create
        createButton = Button(createSiteWindow, text="Create",command=creatButtonOneClick) #need command
        createButton.grid(row=5, column=4, sticky=W)

    def createSiteWindowCreateButtom(self,SiteName,SiteAddress,SiteZipcode,OpenEveryDat,ManagerUsername): #luna
        if OpenEveryDat == '1':
            OpenEveryDat = "Yes"
        else:
            OpenEveryDat= "No"
        sql = "Insert INTO Site (SiteName, SiteAddress, SiteZipcode, OpenEveryDay, ManagerUsername)VALUES ('"+SiteName+"','"+SiteAddress+"','"+SiteZipcode+"','"+OpenEveryDat+"','"+ManagerUsername+"');"
        print(sql)
        self.cursor.execute(sql)
        messagebox.showwarning("Create successfully!")
        self.db.commit()

    def createSiteWindowBackButtom(self): #luna
        self.createSiteWindow.withdraw()
        self.createAdminManageSiteWindow()
        self.buildAdminManageSiteWindow(self.manageSiteWindow)

#================== 22-Administrator Manage Transit ==============================

    def createManageTransitWindow(self):
        self.manageTransitWindow = Toplevel()
        self.manageTransitWindow.title("Administrator Manage Transit")

    def buildManageTransitWindow(self,manageTransitWindow):
        # Title
        manageTransitLabel = Label(manageTransitWindow, text="Manage Transit", font="Verdana 14 bold ")
        manageTransitLabel.grid(row=1, column=1, sticky=W + E)

        # Transport Type
        transportTypeLabel = Label(manageTransitWindow, text="Transport Type", font="Verdana 10")
        transportTypeLabel.grid(row=2, column=1)
        transportTypeList = ["--All--","MARTA","BUS","BIKE"]
        transitTypeSelect = StringVar()
        transitTypeSelect.set(transportTypeList[0])
        transportTypeMenu = OptionMenu(manageTransitWindow, transitTypeSelect, *transportTypeList)
        transportTypeMenu.config(width= 10)
        transportTypeMenu.grid(row=2, column=2)

        # Route
        routeLabel = Label(manageTransitWindow, text="Route", font="Verdana 10")
        routeLabel.grid(row=2, column=3)
        route = StringVar()
        routeEntry = Entry(manageTransitWindow, textvariable=route, width=15)
        routeEntry.grid(row=2, column=4, sticky=W, columnspan=3)

        # Contain Site
        siteLabel = Label(manageTransitWindow, text="Contain Site", font="Verdana 10")
        siteLabel.grid(row=3, column=1)
        sql = "SELECT SiteName FROM Site;"
        self.cursor.execute(sql)
        siteTuple = self.cursor.fetchall()
        siteList = []
        siteList.append("--All--")
        for i in siteTuple:
            siteList.append(i[0])
        siteSelect = StringVar()
        siteSelect.set(siteList[0])
        siteMenu = OptionMenu(manageTransitWindow, siteSelect, *siteList)
        siteMenu.config(width= 10)
        siteMenu.grid(row=3, column=2)

        # Price Range
        priceRangeLabel = Label(manageTransitWindow, text="Price Range", font="Verdana 10")
        priceRangeLabel.grid(row=3, column=3)
        priceMin = StringVar()
        priceMinEntry = Entry(manageTransitWindow, textvariable=priceMin, width=5)
        priceMinEntry.grid(row=3, column=4)
        dashLabel = Label(manageTransitWindow, text="--", font="Verdana 10")
        dashLabel.grid(row=3, column=5)
        priceMax = StringVar()
        priceMaxEntry = Entry(manageTransitWindow, textvariable=priceMax, width=5)
        priceMaxEntry.grid(row=3, column=6)

        # Filter
        def filterBottonFun():
            self.filterTransit(transitTypeSelect.get(),route.get(),siteSelect.get(),priceMin.get(),priceMax.get())
        filterTransitButton = Button(manageTransitWindow, text="Filter", command=filterBottonFun)
        filterTransitButton.grid(row=4, column=1)

        # Create
        createButton = Button(manageTransitWindow, text="Create", command=self.manageTransitWindowCreateButtom)
        createButton.grid(row=4, column=2)

        # Edit
        def manageTransitWindowEditBottom():
            self.editTransit(self.transit_detail_table.focus())
        editButton = Button(manageTransitWindow, text="Edit", command=manageTransitWindowEditBottom)
        editButton.grid(row=4, column=3)

        # Delete
        def manageTransitWindowDeleteBottum():
            self.deleteTranist(self.transit_detail_table.focus())
        deleteButton = Button(manageTransitWindow, text="Delete", command=manageTransitWindowDeleteBottum)
        deleteButton.grid(row=4, column=4)

        # Table
        self.transit_detail_table = ttk.Treeview(manageTransitWindow)
        self.transit_detail_table['columns'] = ("Route","Transit Type","Price","# Connected Sites","# Transit Logged")

        self.transit_detail_table.heading("Route", text=' Route ▼', anchor='w')
        self.transit_detail_table.column("Route", minwidth=2)

        self.transit_detail_table.heading("Transit Type", text="Transit Type▼", anchor='w')
        self.transit_detail_table.column("Transit Type",  minwidth=2)

        self.transit_detail_table.heading("Price", text=' Price ▼', anchor='w')
        self.transit_detail_table.column("Price", minwidth=2)

        self.transit_detail_table.heading("# Connected Sites", text="# Connected Sites ▼")
        self.transit_detail_table.column("# Connected Sites", minwidth=2)

        self.transit_detail_table.heading("# Transit Logged", text="# Transit Logged▼")
        self.transit_detail_table.column("# Transit Logged",  minwidth=2)

        self.transit_detail_table['show'] = 'headings'
        self.transit_detail_table.grid(row=5, column=1, columnspan=6)

        # Back
        backButton = Button(manageTransitWindow, text="Back", command=self.manageTransitWindowBackButton) #need command
        backButton.grid(row=6, column=3, sticky=E)

    def filterTransit(self,transitType,route,site,priceMin,priceMax):
        self.transit_detail_table.delete(*self.transit_detail_table.get_children())
        sql = "SELECT TransitType, TransitRoute, TransitPrice FROM Transit"
        if transitType != "--All--" or route or priceMax or priceMin:
            sql += " WHERE "
            index = 0
        if transitType != "--All--":
            if index >0: sql+=" AND "
            sql += "TransitType = '"+transitType+"'"
            index+=1
        if route:
            if index >0: sql+=" AND "
            sql += "TransitRoute = '"+route+"'"
            index+=1
        if priceMin:
            if index >0: sql+=" AND "
            sql += "TransitPrice >="+priceMin+""
            index+=1
        if priceMax:
            if index >0: sql+=" AND "
            sql += "TransitPrice <="+priceMax+""
            index+=1
        sql += ";"
        print(sql)
        self.cursor.execute(sql)
        result = list(map(list,self.cursor.fetchall()))
        for t in result:
            sql = "SELECT SiteName FROM Connect WHERE TransitType = '"+t[0]+"' AND TransitRoute = '"+t[1]+"' ;"
            self.cursor.execute(sql)
            connectedSites=self.cursor.fetchall()
            t.append({'connectSites':[]})
            for s in connectedSites:
                t[3]['connectSites'].append(s[0])
            # t[2]=float(t[2])
            sql= "SELECT COUNT(*) FROM TakeTransit WHERE TransitType = '"+t[0]+"' AND TransitRoute = '"+t[1]+"' ;"
            self.cursor.execute(sql)
            num_logged = self.cursor.fetchall()
            t.append(num_logged[0][0])
        # [[type,route,price,{connectedSites:[a,v,s]},#logged],...]
        i=0
        for t in result:
            if site == "--All--":
                i+=1
                self.transit_detail_table.insert("",i,value=(t[1],t[0],t[2],len(t[3]['connectSites']),t[4]))
            elif site in t[3]['connectSites']:
                i+=1
                self.transit_detail_table.insert("",i,value=(t[1],t[0],t[2],len(t[3]['connectSites']),t[4]))

    def deleteTranist(self,selection):
        transit = self.transit_detail_table.item(selection)['values']
        sql = "DELETE FROM Transit WHERE TransitType = '"+transit[1]+"' AND TransitRoute = '"+transit[0]+"';"
        self.cursor.execute(sql)
        self.db.commit()
        # delete from view
        self.transit_detail_table.delete(selection)

    def editTransit(self,selection):
        transit = self.transit_detail_table.item(selection)['values']
        self.manageTransitWindow.destroy()
        self.createEditTransitWindow()
        self.buildEditTransitWindow(self.editTransitWindow, transit[1], transit[0])
        self.editTransitWindow,mainloop()

    def manageTransitWindowCreateButtom(self):
        self.manageTransitWindow.destroy()
        self.createCreateTransitWindow()
        self.buildCreateTransitWindow(self.createTransitWindow)
        self.createTransitWindow.mainloop()

    def manageTransitWindowBackButton(self):
        self.manageTransitWindow.destroy()
        self.previous.deiconify()

#================== 23-Administrator Edit Transit =================================

    def createEditTransitWindow(self):
        self.editTransitWindow = Toplevel()
        self.editTransitWindow.title("Administrator Edit Transit")

    def buildEditTransitWindow(self,editTransitWindow, TransitType, TransitRoute):
        # Title
        editTransitLabel = Label(editTransitWindow, text="Edit Transit", font="Verdana 14 bold ")
        editTransitLabel.grid(row=1, column=1, sticky=W + E)

        old_price, old_connectedSites = self.findTransitDetial(TransitType, TransitRoute)
        old_route = TransitRoute
        sql = "SELECT SiteName FROM Site;"
        self.cursor.execute(sql)
        siteList = self.cursor.fetchall()
        # Transport Type
        transportTypeLabel = Label(editTransitWindow, text="Transport Type", font="Verdana 10")
        transportTypeLabel.grid(row=2, column=1)
        TransitTypeShow = Label(editTransitWindow, text=TransitType, font="Verdana 10 bold")
        TransitTypeShow.grid(row=2, column=2)
        # Route
        routeLabel = Label(editTransitWindow, text="Route", font="Verdana 10")
        routeLabel.grid(row=2, column=3)
        route = StringVar()
        route.set(TransitRoute)
        routeEntry = Entry(editTransitWindow, textvariable=route, width=10)
        routeEntry.grid(row=2, column=4, sticky=W)
        # Price
        priceLabel = Label(editTransitWindow, text="Price($)", font="Verdana 10")
        priceLabel.grid(row=2, column=5)
        priceEdit = StringVar()
        priceEdit.set(old_price[0])
        priceEntry = Entry(editTransitWindow, textvariable=priceEdit, width=5)
        priceEntry.grid(row=2, column=6, sticky=W)
        # Connected Sites
        sitesLabel = Label(editTransitWindow, text="Connected Sites", font="Verdana 10")
        sitesLabel.grid(row=3, column=1, sticky=N+S)
        listbox = Listbox(editTransitWindow, width=20, height=10, selectmode=MULTIPLE)
        listbox.grid(row=3,column=2, columnspan=4)
        for i in range(len(siteList)):
            listbox.insert(i+1,siteList[i])
            if siteList[i] in old_connectedSites:
                listbox.select_set(i)

        # Back
        backButton = Button(editTransitWindow, text="Back", command = self.editTransitWindowBackButtom)
        backButton.grid(row=4, column=2)

        # Update
        def editTransitWindowUpdateButtom(): #所有都要重新输入
            sitesSelect = [listbox.get(idx) for idx in listbox.curselection()]
            self.updateTransit(TransitType,old_route,old_price[0],old_connectedSites,route.get(), priceEdit.get(),sitesSelect)
        updateButton = Button(editTransitWindow, text="Update", command = editTransitWindowUpdateButtom)
        updateButton.grid(row=4, column=4)

    def editTransitWindowBackButtom(self):
        self.editTransitWindow.destroy()
        self.createManageTransitWindow()
        self.buildManageTransitWindow(self.manageTransitWindow)
        self.manageTransitWindow.mainloop()

    def updateTransit(self,transitType,oldRoute,oldPrice,OldSites,newRoute,newPrice,newSites): #luna
        sql = "DELETE FROM Transit WHERE TransitType = '"+transitType+"' AND TransitRoute = '"+str(oldRoute)+"';"
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        connectSites = [ i[0] for i in newSites]
        sql = "INSERT INTO Transit (TransitType, TransitRoute, TransitPrice) VALUES ('"+transitType+"', '"+str(newRoute)+"', "+newPrice[0]+");"
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        for cs in connectSites:
            sql = "INSERT INTO Connect (SiteName, TransitType, TransitRoute) VALUES ('"+cs+"', '"+transitType+"', '"+str(newRoute)+"');"
            print(sql)
            self.cursor.execute(sql)
            self.db.commit()

    def findTransitDetial(self, TransitType, TransitRoute): #luna
        sql = "SELECT TransitPrice FROM Transit WHERE TransitType = '"+TransitType+"' And TransitRoute = '"+str(TransitRoute)+"';"
        self.cursor.execute(sql)
        price = self.cursor.fetchall()
        sql = "SELECT SiteName FROM Connect WHERE TransitType = '"+TransitType+"' And TransitRoute = '"+str(TransitRoute)+"';"
        self.cursor.execute(sql)
        connectedSites = self.cursor.fetchall()
        return price, connectedSites

#================== 24-Administrator Create Transit ===============================

    def createCreateTransitWindow(self):
        self.createTransitWindow = Toplevel()
        self.createTransitWindow.title("Administrator Create Transit")

    def buildCreateTransitWindow(self,createTransitWindow):
        # Title
        createTransitLabel = Label(createTransitWindow, text="Create Transit", font="Verdana 14 bold ")
        createTransitLabel.grid(row=1, column=1, sticky=W + E)

        sql = "SELECT SiteName FROM Site;"
        self.cursor.execute(sql)
        siteList = self.cursor.fetchall()
        # Transport Type
        transportTypeLabel = Label(createTransitWindow, text="Transport Type", font="Verdana 10")
        transportTypeLabel.grid(row=2, column=1)
        transportTypeList = ["MARTA","BUS","BIKE"]
        transitTypeSelect = StringVar()
        transitTypeSelect.set(transportTypeList[0])
        transportTypeMenu = OptionMenu(createTransitWindow, transitTypeSelect, *transportTypeList)
        transportTypeMenu.config(width= 10)
        transportTypeMenu.grid(row=2, column=2)
        # Route
        routeLabel = Label(createTransitWindow, text="Route", font="Verdana 10")
        routeLabel.grid(row=2, column=3)
        route = StringVar()
        routeEntry = Entry(createTransitWindow, textvariable=route, width=10)
        routeEntry.grid(row=2, column=4, sticky=W)
        # Price
        priceLabel = Label(createTransitWindow, text="Price($)", font="Verdana 10")
        priceLabel.grid(row=2, column=5)
        priceEdit = StringVar()
        priceEntry = Entry(createTransitWindow, textvariable=priceEdit, width=5)
        priceEntry.grid(row=2, column=6, sticky=W)
        # Connected Sites
        sitesLabel = Label(createTransitWindow, text="Connected Sites", font="Verdana 10")
        sitesLabel.grid(row=3, column=1, sticky=N+S)
        listbox = Listbox(createTransitWindow, width=20, height=10, selectmode=MULTIPLE)
        listbox.grid(row=3,column=2, columnspan=4)
        for i in range(len(siteList)):
            listbox.insert(i+1,siteList[i])

        # Back
        backButton = Button(createTransitWindow, text="Back", command = self.createTransitWindowBackButtom)
        backButton.grid(row=4, column=2) #luna
        # Create
        def createTransitWindowCreateButtom():
            sitesSelect = [listbox.get(idx) for idx in listbox.curselection()]
            self.createTransit(transitTypeSelect.get(), route.get(), priceEdit.get(),sitesSelect)
        createButton = Button(createTransitWindow, text="Create" , command = createTransitWindowCreateButtom)
        createButton.grid(row=4, column=4)

    def createTransit(self, Transittype, route, price, sites):
        connectSites = [ i[0] for i in sites]
        sql = "INSERT INTO Transit (TransitType, TransitRoute, TransitPrice) VALUES ('"+Transittype+"', '"+route+"', "+price+");"
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        for cs in connectSites:
            sql = "INSERT INTO Connect (SiteName, TransitType, TransitRoute) VALUES ('"+cs+"', '"+Transittype+"', '"+route+"');"
            print(sql)
            self.cursor.execute(sql)
            self.db.commit()

    def createTransitWindowBackButtom(self):
        self.createTransitWindow.destroy()
        self.createManageTransitWindow()
        self.buildManageTransitWindow(self.manageTransitWindow)
        self.manageTransitWindow.mainloop()

#=========Screen 25 Manager Manage Event Window============

    def createManageEventWindow(self):
        self.manageEventWindow = Toplevel()
        self.manageEventWindow.title("Manage Event")
        self.manageEventWindow.geometry("700x500")

    def buildManageEventWindow(self,manageEventWindow):

        # Title Label
        manageEventLabel = Label(manageEventWindow, text="Manage Event", font="Verdana 10 bold ")
        manageEventLabel.grid(row=1, column=2, sticky=W + E,pady=5)

		# name label
        nameLabel = Label(manageEventWindow, text="Name", font="Verdana 10 bold")
        nameLabel.grid(row=3, column=1,pady=5)
        eventName = StringVar()
        name = Entry(manageEventWindow, textvariable=eventName, width=20)
        name.grid(row=3, column=2,pady=5)

        # description keyword entry
        keywordLabel = Label(manageEventWindow, text="Description Keyword", font="Verdana 10 bold")
        keywordLabel.grid(row=5, column=1,pady=5)
        descriptionKeyword = StringVar()
        keyword = Entry(manageEventWindow, textvariable=descriptionKeyword, width=20)
        keyword.grid(row=5, column=2,pady=5)

        # start date entry
        startLabel = Label(manageEventWindow, text="Start Date", font="Verdana 10 bold")
        startLabel.grid(row=7, column=1,pady=5)
        startDate = StringVar(value='YYYY-MM-DD')
        start = Entry(manageEventWindow, textvariable=startDate, width=20)
        start.grid(row=7, column=2,pady=5)

        # end date entry
        endLabel = Label(manageEventWindow, text="End Date", font="Verdana 10 bold")
        endLabel.grid(row=9, column=1,pady=5)
        endDate = StringVar(value='YYYY-MM-DD')
        end = Entry(manageEventWindow, textvariable=endDate, width=20)
        end.grid(row=9, column=2,pady=5)

        # duration range label
        durationRangeLabel = Label(manageEventWindow, text = "Duration Range", font = "Verdana 10 bold")
        durationRangeLabel.grid(row=3, column = 3,pady=5)
        minDuration = StringVar()
        minDurationEntry = Entry(manageEventWindow, textvariable=minDuration, width=10)
        minDurationEntry.grid(row=3, column=4,pady=5)
        dash1 = Label(manageEventWindow, text = "-", font = "Verdana 10 bold")
        dash1.grid(row=3, column = 5,pady=5)
        maxDuration = StringVar()
        maxDurationEntry = Entry(manageEventWindow, textvariable=maxDuration, width=10)
        maxDurationEntry.grid(row=3, column=6,pady=5)

        # total visits range label
        visitsRangeLabel = Label(manageEventWindow, text = "Total Visits Range", font = "Verdana 10 bold")
        visitsRangeLabel.grid(row=5, column = 3,pady=5)
        minVisits = StringVar()
        minVisitsEntry = Entry(manageEventWindow, textvariable=minVisits, width=10)
        minVisitsEntry.grid(row=5, column=4,pady=5)
        dash2 = Label(manageEventWindow, text = "-", font = "Verdana 10 bold")
        dash2.grid(row=5, column = 5,pady=5)
        maxVisits = StringVar()
        maxVisitsEntry = Entry(manageEventWindow, textvariable=maxVisits, width=10)
        maxVisitsEntry.grid(row=5, column=6,pady=5)

        # total revenue range label
        revenueRangeLabel = Label(manageEventWindow, text = "Total Revenue Range", font = "Verdana 10 bold")
        revenueRangeLabel.grid(row=7, column = 3,pady=5)
        minRevenue = StringVar()
        minRevenueEntry = Entry(manageEventWindow, textvariable=minRevenue, width=10)
        minRevenueEntry.grid(row=7, column=4,pady=5)
        dash3 = Label(manageEventWindow, text = "-", font = "Verdana 10 bold")
        dash3.grid(row=7, column = 5,pady=5)
        maxRevenue = StringVar()
        maxRevenueEntry = Entry(manageEventWindow, textvariable=maxRevenue, width=10)
        maxRevenueEntry.grid(row=7, column=6,pady=5)

        def manageEventWindowFilterBottonClicked():
            self.filterManageEvent(eventName.get(), descriptionKeyword.get(), startDate.get(), endDate.get(),
	            	minVisits.get(), maxVisits.get(), minRevenue.get(), maxRevenue.get(), minDuration.get(), maxDuration.get())

        # filter Button
        filterButton = Button(manageEventWindow, text="Filter", command=manageEventWindowFilterBottonClicked)
        filterButton.grid(row=11, column=1,pady=5)

        # create Button
        createButton = Button(manageEventWindow, text="Create", command=self.manageEventWindowCreateButtonClicked)
        createButton.grid(row=11, column=3,pady=5)

        # view/edit Button
        viewEditButton = Button(manageEventWindow, text="View/Edit", command=self.manageEventWindowEditButtonClicked)
        viewEditButton.grid(row=11, column=4,pady=5)

        # delete Button
        deleteButton = Button(manageEventWindow, text="Delete", command=self.manage_event_delete_Button_Clicked)
        deleteButton.grid(row=11, column=5,pady=5)

        # back Button
        backButton = Button(manageEventWindow, text="Return", command=self.manageEventWindowBackButtonClicked)
        backButton.grid(row=14, column=3,pady=5)

        # search table
        self.manage_event_tb = ttk.Treeview(manageEventWindow)
        self.manage_event_tb['columns'] = ("Event Number","Name", "Staff Count", "Duration (Days)", "Total Visits", "Total Revenue")

        self.manage_event_tb.heading("Event Number", text=' Event Number ▼ ', anchor='w')
        self.manage_event_tb.column("Event Number", width=100)

        self.manage_event_tb.heading("Name", text=' Name ▼ ', anchor='w')
        self.manage_event_tb.column("Name", width=100)

        self.manage_event_tb.heading("Staff Count", text="Staff Count ▼", anchor='w')
        self.manage_event_tb.column("Staff Count",  width=100)

        self.manage_event_tb.heading("Duration (Days)", text=" Duration (Days) ▼")
        self.manage_event_tb.column("Duration (Days)", width=100)

        self.manage_event_tb.heading("Total Visits", text="Total Visits ▼")
        self.manage_event_tb.column("Total Visits",  width=100)

        self.manage_event_tb.heading("Total Revenue", text="Total Revenue ($) ▼")
        self.manage_event_tb.column("Total Revenue",  width=100)

        self.manage_event_tb['show'] = 'headings'
        self.manage_event_tb.grid(row=13, column=1, columnspan = 6,pady=5)

    def manage_event_delete_Button_Clicked(self):
        self.searchEmployeeInformation()
        SQL = "SELECT SiteName  from Site where ManagerUsername = '" + self.Username + "'";
        self.cursor.execute(SQL)
        temp= self.cursor.fetchall()
        self.manageSiteName = str(temp[0][0])
        curItem = self.manage_event_tb.item(self.manage_event_tb.focus())
        siteName = curItem['values'][1]
        sql = "DELETE FROM Event WHERE EventName = '"+siteName+"' and Sitename = '"+self.manageSiteName+"';"
        self.cursor.execute(sql);
        self.db.commit()

    def filterManageEvent(self,name,description,startDate,endDate,minVisits,maxVisits,minRevenue,maxRevenue,minDuration,maxDuration):
        self.searchEmployeeInformation()
        SQL = "SELECT SiteName  from Site where ManagerUsername = '" + self.Username + "'";
        self.cursor.execute(SQL)
        temp= self.cursor.fetchall()
        self.manageSiteName = str(temp[0][0])

        sql = "SELECT EventName, EndDate-E.StartDate as duration, count(VisitorUsername) as TotalVisits,\
        count(VisitorUsername)*EventPrice as TotalRevenue, E.StartDate from Event E\
        join VisitEvent V on VisitEventName = EventName and V.SiteName = E.SiteName and V.StartDate = E.StartDate\
        where E.SiteName = '"+ self.manageSiteName+"'"

        if name:
            sql = sql + " AND E.EventName = '"+name+"'";
        if description:
            sql = sql + " AND Description like '"+description+"'";
        if startDate != "YYYY-MM-DD":
            sql = sql + " AND E.StartDate >= '"+startDate+"'";
        if endDate != "YYYY-MM-DD":
            sql = sql + " AND E.EndDate <= '"+endDate+"'";
        sql = sql+" group by EventName,E.StartDate;"                                ############################################????????group by username
        # print(sql)
        self.cursor.execute(sql)
        temp= self.cursor.fetchall()
        # print(temp)
        EventName = []
        Duration = []
        TotalVisits = []
        TotalRevenue = []
        StartDateList = []
        StaffCount = []
        ShowList = []

        for i in range(len(temp)):
            EventName.append(str(temp[i][0]))
            Duration.append(int(temp[i][1]))
            TotalVisits.append(int(temp[i][2]))
            TotalRevenue.append(int(temp[i][3]))
            StartDateList.append(str(temp[i][4]))

        for i in range(len(EventName)):
            sql = "select count(StaffUsername) from AssignTo where SiteName = '"+self.manageSiteName+"' and StartDate = '"+StartDateList[i]+"' and EventName = '"+EventName[i]+"';"
            self.cursor.execute(sql)
            temp= self.cursor.fetchall()
            StaffCount.append(temp[0][0])
            ShowList.append(1)
            if minVisits:
                if ShowList[i] == 1:
                    if (TotalVisits[i] >= int(minVisits)) == False: ShowList[i] = 0
            if maxVisits:
                if ShowList[i] == 1:
                    if (TotalVisits[i] <= int(maxVisits)) == False: ShowList[i] = 0
            if minRevenue:
                if ShowList[i] == 1:
                    if (TotalRevenue[i] >= int(minRevenue)) == False: ShowList[i] = 0
            if maxRevenue:
                if ShowList[i] == 1:
                    if (TotalRevenue[i] >= int(maxRevenue)) == False: ShowList[i] = 0
            if minDuration:
                if ShowList[i] == 1:
                    if (Duration[i] >= int(minDuration)) == False: ShowList[i] = 0
            if maxDuration:
                if ShowList[i] == 1:
                    if (Duration[i] >= int(maxDuration)) == False: ShowList[i] = 0

        #for i in range(len(EventName)):
        self.manage_event_tb_showdata = []
        j=0
        self.manage_event_tb.delete(*self.manage_event_tb.get_children())
        for i in range(len(EventName)):
            if ShowList[i]==1:
               self.manage_event_tb.insert("",j, value=(j,str(EventName[i]),str(TotalRevenue[i]),str(Duration[i]),str(TotalVisits[i]),str(TotalRevenue[i])))
               self.manage_event_tb_showdata.append([j,str(EventName[i]),StartDateList[i],self.manageSiteName])
               j+=1

        self.db.commit()

    def manageEventWindowBackButtonClicked(self):
        self.manageEventWindow.destroy()
        self.previous.deiconify()

    def manageEventWindowCreateButtonClicked(self):
        # Click Return Buttion on Search Exhibit Window:
        # Destroy Search Exhibit Window
        # Display Choose Functionality Window
        self.createCreateEventWindow()
        self.buildCreateEventWindow(self.createEventWindow)
        self.manageEventWindow.withdraw()

    def manageEventWindowEditButtonClicked(self):
        # Click Return Buttion on Search Exhibit Window:
        # Destroy Search Exhibit Window
        # Display Choose Functionality Window
        curItem = self.manage_event_tb.item(self.manage_event_tb.focus())
        index = curItem['values'][0]
        self.createViewEditEventWindow()
        self.buildViewEditEventWindow(self.viewEditEventWindow,index)
        self.manageEventWindow.withdraw()


#=========Screen 26 Manager View/Edit Event Window============

    def createViewEditEventWindow(self):
        self.viewEditEventWindow = Toplevel()
        self.viewEditEventWindow.title("View/Edit Event")
        self.manageEventWindow.geometry("700x800")

    def buildViewEditEventWindow(self,viewEditEventWindow,index):
        temp=self.manage_event_tb_showdata[index]
        sql = "select * from Event where EventName='"+temp[1]+"' and StartDate =  '"+str(temp[2])+"' and SiteName = '"+temp[3]+"';"
        self.cursor.execute(sql)
        initialData = self.cursor.fetchall()
        # Title Label
        manageEventLabel = Label(viewEditEventWindow, text="View/Edit Event", font="Verdana 10 bold ")
        manageEventLabel.grid(row=1, column=2, sticky=W + E,pady=5)

		# name label
        nameLabel = Label(viewEditEventWindow, text="Name", font="Verdana 10 bold")
        nameLabel.grid(row=2, column=1,pady=5)
        nameContent = Label(viewEditEventWindow, text=initialData[0][0], font="Verdana 10 bold")
        nameContent.grid(row=2, column=2,pady=5)

		# price label
        priceLabel = Label(viewEditEventWindow, text="Price ($)", font="Verdana 10 bold")
        priceLabel.grid(row=2, column=3,pady=5)
        priceContent = Label(viewEditEventWindow, text=initialData[0][4], font="Verdana 10 bold")
        priceContent.grid(row=2, column=4,pady=5)

        # start date label
        startLabel = Label(viewEditEventWindow, text="Start Date", font="Verdana 10 bold")
        startLabel.grid(row=3, column=1,pady=5)
        startContent = Label(viewEditEventWindow, text=initialData[0][2], font="Verdana 10 bold")
        startContent.grid(row=3, column=2,pady=5)

        # end date label
        endLabel = Label(viewEditEventWindow, text="End Date", font="Verdana 10 bold")
        endLabel.grid(row=3, column=3,pady=5)
        endContent = Label(viewEditEventWindow, text=initialData[0][3], font="Verdana 10 bold")
        endContent.grid(row=3, column=4,pady=5)

        # staff label
        staffLabel = Label(viewEditEventWindow, text="Minimun Staff Required", font="Verdana 10 bold")
        staffLabel.grid(row=4, column=1,pady=5)
        staffContent = Label(viewEditEventWindow, text=initialData[0][7], font="Verdana 10 bold")
        staffContent.grid(row=4, column=2,pady=5)

        # capacity label
        capacityLabel = Label(viewEditEventWindow, text="Capacity", font="Verdana 10 bold")
        capacityLabel.grid(row=4, column=3,pady=5)
        capacityContent = Label(viewEditEventWindow, text=initialData[0][5], font="Verdana 10 bold")
        capacityContent.grid(row=4, column=4,pady=5)

        # Description label
        descriptionLabel = Label(viewEditEventWindow, text="Description", font="Verdana 10 bold")
        descriptionLabel.grid(row=5, column=1,pady=5)
        #description = StringVar(value = initialData[0][6])
        #descriptionEntry = Entry(viewEditEventWindow, textvariable=description, width=20)
        #descriptionEntry.grid(row=5, column=2, columnspan=3, sticky=W+E,pady=5)
        text = Text(viewEditEventWindow, width=60, height=5)
        text.insert(INSERT,initialData[0][6])
        #text = Text(viewEditEventWindow, textvariable=root, width=20)
        text.grid(row=5, column=2, columnspan=3, sticky=W+E,pady=5)
        # staff assined label
        sql = "select StaffUsername from AssignTo where EventName='"+temp[1]+"' and StartDate =  '"+str(temp[2])+"' and SiteName = '"+temp[3]+"';"
        self.cursor.execute(sql)
        initialStaff = []
        for element in self.cursor.fetchall():initialStaff.append(element[0])
        self.cursor.execute("select * from Staff;")
        staffList = []
        for element in self.cursor.fetchall():staffList.append(element[0])
        assignLabel = Label(viewEditEventWindow, text="Staff Assigned", font="Verdana 10 bold")
        assignLabel.grid(row=6, column=1,pady=5)
        listbox = Listbox(viewEditEventWindow, width=20, height=5, selectmode=MULTIPLE)
        listbox.grid(row=6,column=2, columnspan=4,pady=5)
        for i in range(len(staffList)):
            listbox.insert(i+1,staffList[i])
            if staffList[i] in initialStaff:
                listbox.select_set(i)

        # daily visits range label
        visitsRangeLabel = Label(viewEditEventWindow, text = "Daily Visits Range", font = "Verdana 10 bold")
        visitsRangeLabel.grid(row=8, column = 1)
        # minimum visits entry
        minVisitsLabel = Label(viewEditEventWindow, text = "Min", font = "Verdana 10 bold")
        minVisitsLabel.grid(row=7, column = 2)
        self.minVisitsEntry = StringVar()
        minVisits = Entry(viewEditEventWindow, textvariable=self.minVisitsEntry, width=10)
        minVisits.grid(row=8, column=2)
        # maximum visits entry
        maxVisitsLabel = Label(viewEditEventWindow, text = "Max", font = "Verdana 10 bold")
        maxVisitsLabel.grid(row=7, column = 3)
        self.maxVisitsEntry = StringVar()
        maxVisits = Entry(viewEditEventWindow, textvariable=self.maxVisitsEntry, width=10)
        maxVisits.grid(row=8, column=3,pady=5)

        # daily revenue range label
        revenueRangeLabel = Label(viewEditEventWindow, text = "Daily Revenue Range", font = "Verdana 10 bold")
        revenueRangeLabel.grid(row=10, column = 1)
        # minimum revenue entry
        minRevenueLabel = Label(viewEditEventWindow, text = "Min", font = "Verdana 10 bold")
        minRevenueLabel.grid(row=9, column = 2)
        self.minRevenueEntry = StringVar()
        minRevenue = Entry(viewEditEventWindow, textvariable=self.minRevenueEntry, width=10)
        minRevenue.grid(row=10, column=2)
        # maximum revenue entry
        maxRevenueLabel = Label(viewEditEventWindow, text = "Max", font = "Verdana 10 bold")
        maxRevenueLabel.grid(row=9, column = 3)
        self.maxRevenueEntry = StringVar()
        maxRevenue = Entry(viewEditEventWindow, textvariable=self.maxRevenueEntry, width=10)
        maxRevenue.grid(row=10, column=3)

        # search table
        self.tv_manage_view_event = ttk.Treeview(viewEditEventWindow)
        self.tv_manage_view_event['columns'] = ("Date", "Daily Visits", "Daily Revenue ($)")

        self.tv_manage_view_event.heading("Date", text='                     Date                           ', anchor='w')
        self.tv_manage_view_event.column("Date", minwidth=2)

        self.tv_manage_view_event.heading("Daily Visits", text="                     Daily Visits               ", anchor='w')
        self.tv_manage_view_event.column("Daily Visits",  minwidth=2)

        self.tv_manage_view_event.heading("Daily Revenue ($)", text="               Daily Revenue ($)              ")
        self.tv_manage_view_event.column("Daily Revenue ($)", minwidth=2)

        self.tv_manage_view_event['show'] = 'headings'
        self.tv_manage_view_event.grid(row=13, column=1, columnspan = 4 ,pady=5 )

        #filt button
        def viewEditEventWindowFilterBottonClicked():
            eventName = initialData[0][0]
            eventPrice = initialData[0][4]
            startDate = str(initialData[0][2])
            endDate =str( initialData[0][3])
            if startDate and endDate :
                startDate_date = datetime.datetime.strptime(startDate,'%Y-%m-%d')
                endDate_date = datetime.datetime.strptime(endDate,'%Y-%m-%d')
                timeList = []
                while startDate_date <= endDate_date:
                    i = datetime.datetime.strftime(startDate_date,'%Y-%m-%d')
                    timeList.append(str(i))
                    startDate_date = startDate_date + datetime.timedelta(days = 1)
            else:
               messagebox.showwarning("Please input Start Date and End Date.")
            dailyRevenue = []
            dailyVisit = []
            ifShow=[]
            for i in range(len(timeList)):
                sql = "select count(VisitorUsername) from VisitEvent where SiteName = '"+ self.manageSiteName\
                        + "' and StartDate = '"+ startDate + "' and VisitEventName = '"+ eventName+ "' and VisitEventDate = '"+ timeList[i]+"';"
                print(sql)
                self.cursor.execute(sql)
                temp = self.cursor.fetchall()
                if len(temp)>0:
                    dailyVisit.append(temp[0][0])
                    dailyRevenue.append(eventPrice*temp[0][0])
                    ifShow.append(1)
            #filting based on visit and revenue
            if minRevenue.get() and maxRevenue.get():
                if int(minRevenue.get())>=0  and int(maxRevenue.get())>int(minRevenue.get()):
                    for i in range(len(timeList)):
                        if ifShow[i] == 1:
                            if int(dailyRevenue[i])<int(minRevenue.get()) or int(dailyRevenue[i])>int(maxRevenue.get()): ifShow[i]=0
            if minVisits.get() and maxVisits.get():
                if int(minVisits.get())>=0  and int(maxVisits.get())>int(minVisits.get()):
                    for i in range(len(timeList)):
                        if ifShow[i] == 1:
                            if int(dailyVisit[i])<int(minVisits.get()) or int(dailyVisit[i])>int(maxVisits.get()): ifShow[i]=0
            # insert into the table
            j=0
            self.tv_manage_view_event.delete(*self.tv_manage_view_event.get_children())
            for i in range(len(timeList)):
                if ifShow[i]==1:
                    self.tv_manage_view_event.insert("",j, value=(str(timeList[i]),str(dailyVisit[i]),str(dailyRevenue[i])))
                    j+=1
            self.db.commit()
        # filter Button
        filterButton = Button(viewEditEventWindow, text="Filter", command=viewEditEventWindowFilterBottonClicked)
        filterButton.grid(row=11, column=1,pady=5)

        # update Button
        def  viewEditEventWindowUpdateBottonClicked():
            for stfname in initialStaff:
                sql = "DELETE FROM AssignTo WHERE SiteName = '"+self.manageSiteName+"'and EventName = '"+initialData[0][0]+"' and StaffUsername = '"+stfname+"' and StartDate ='"+str(initialData[0][2])+"';"
                self.cursor.execute(sql)
                self.db.commit()
            curItem = listbox.curselection()
            for curIndex in curItem:
                sql = "Insert INTO AssignTo (StaffUsername,EventName,StartDate,SiteName) VALUES ('"+staffList[curIndex]+"','"+initialData[0][0]+"','"+str(initialData[0][2])+"','"+self.manageSiteName+"')"
                self.cursor.execute(sql)
                self.db.commit()

            new_descp = text.get("1.0",END)
            sql = "UPDATE Event SET Description ='"+new_descp+"' WHERE SiteName = '"+self.manageSiteName+"'and EventName = '"+initialData[0][0]+"' and StartDate ='"+str(initialData[0][2])+"';"
            self.cursor.execute(sql)
            self.db.commit()
            ## update function end
        updateButton = Button(viewEditEventWindow, text="Update", command=viewEditEventWindowUpdateBottonClicked)
        updateButton.grid(row=11, column=4,pady=5)

        # back Button
        backButton = Button(viewEditEventWindow, text="Return", command=self.viewEditEventWindowBackButtonClicked)
        backButton.grid(row=14, column=3,pady=5)

    def viewEditEventWindowBackButtonClicked(self):
        # Click Return Buttion on Search Exhibit Window:
        # Destroy Search Exhibit Window
        # Display Choose Functionality Window
        self.viewEditEventWindow.destroy()
        self.manageEventWindow.deiconify()


#=========Screen 27 Manager Create Event Window============

    def createCreateEventWindow(self):
        self.createEventWindow = Toplevel()
        self.createEventWindow.title("Create Event")

    def buildCreateEventWindow(self,createEventWindow):
        self.searchEmployeeInformation()
        username = self.Username
        # Title Label
        createEventLabel = Label(createEventWindow, text="Create Event", font="Verdana 10 bold ")
        createEventLabel.grid(row=1, column=2, sticky=W + E)

        SQLCommand = "SELECT DISTINCT SiteName from Site\
			         where ManagerUsername = " + "'" + username + "' ;"
        self.cursor.execute(SQLCommand)
        SiteTuple = self.cursor.fetchall()
        SiteList = []
        for element in SiteTuple: SiteList.append(element[0])
        SiteName = StringVar()
        SiteName.set(SiteList[0])

		# name label
        nameLabel = Label(createEventWindow, text="Name", font="Verdana 10 bold")
        nameLabel.grid(row=2, column=1)
        eventName = StringVar()
        name = Entry(createEventWindow, textvariable=eventName, width=20)
        name.grid(row=2, column=2, columnspan = 3, sticky=W + E)

		# price label
        priceLabel = Label(createEventWindow, text="Price ($)", font="Verdana 10 bold")
        priceLabel.grid(row=3, column=1)
        price = StringVar()
        priceValue = Entry(createEventWindow, textvariable=price, width=20)
        priceValue.grid(row=3, column=2)

        # capacity label
        capacityLabel = Label(createEventWindow, text="Capacity", font="Verdana 10 bold")
        capacityLabel.grid(row=3, column=3)
        capacity = StringVar()
        capacityValue = Entry(createEventWindow, textvariable=capacity, width=20)
        capacityValue.grid(row=3, column=4)

        # staff label
        staffLabel = Label(createEventWindow, text="Minimum Staff Required", font="Verdana 10 bold")
        staffLabel.grid(row=4, column=1)
        staff = StringVar()
        staffValue = Entry(createEventWindow, textvariable=staff, width=20)
        staffValue.grid(row=4, column=2)

        # start date entry
        startLabel = Label(createEventWindow, text="Start Date", font="Verdana 10 bold")
        startLabel.grid(row=5, column=1)
        startDate = StringVar()
        start = Entry(createEventWindow, textvariable=startDate, width=20)
        start.grid(row=5, column=2)

        # end date entry
        endLabel = Label(createEventWindow, text="End Date", font="Verdana 10 bold")
        endLabel.grid(row=5, column=3)
        endDate = StringVar()
        end = Entry(createEventWindow, textvariable=endDate, width=20)
        end.grid(row=5, column=4)

		# Description label
        descriptionLabel = Label(createEventWindow, text="Description", font="Verdana 10 bold")
        descriptionLabel.grid(row=6, column=1)
        text = Text(createEventWindow, width=60, height=5)
        #text = Text(viewEditEventWindow, textvariable=root, width=20)
        text.grid(row=6, column=2, columnspan=3, sticky=W+E,pady=5)

        # staff assined label
        assignLabel = Label(createEventWindow, text="Assign Staff ", font="Verdana 10 bold")
        assignLabel.grid(row=7, column=1) #修改 如何根据日期filter
        # staff assined label
        self.cursor.execute("select * from Staff;")
        staffList = []
        for element in self.cursor.fetchall():staffList.append(element[0])
        listbox = Listbox(createEventWindow, width=20, height=5, selectmode=MULTIPLE)
        listbox.grid(row=7,column=2, columnspan=4,pady=5)
        for i in range(len(staffList)):
            listbox.insert(i+1,staffList[i])

        curItem = listbox.curselection()
        selectedstaff=[]
        for curIndex in curItem:
            selectedstaff.append(staffList[curIndex])

        def createButtonClicked():
            #print(str(eventName.get()), str(price.get()), str(capacity.get()), str(staff.get()),
		     #        str(startDate.get()), str(endDate.get()), str(text.get("1.0",END))))
            self.createNewEvent(eventName.get(), price.get(), capacity.get(), staff.get(),
	            	startDate.get(), endDate.get(),text.get("1.0",END) , SiteName.get(),selectedstaff)
        # create Button
        createButton = Button(createEventWindow, text="Create", command=createButtonClicked)
        createButton.grid(row=8, column=4)

        # back Button
        backButton = Button(createEventWindow, text="Return", command=self.createEventWindowBackButtonClicked)
        backButton.grid(row=8, column=1)

    def createNewEvent(self, eventName, price, capacity, staff, startDate, endDate, description, SiteName,selectedstaff):

        if eventName and startDate != "YYYY-MM-DD" and endDate != "YYYY-MM-DD" and SiteName and price and capacity and staff and capacity:
        	SQL = "INSERT INTO Event (EventName, startDate,SiteName,EndDate,EventPrice,Capacity,MinStaffRequired,Description) VALUES ("
        else:
        	messagebox.showwarning("All fields are required.")

        SQL = SQL + "'"+eventName+"'," + " '"+startDate+"',"  + "  '"+SiteName+"'," + " '"+endDate+"',";
        SQL = SQL +price+"," +capacity+"," +staff+"," + " '"+description+"');"
        print(SQL)

        ##check all the input validation
        index = 1
        if len(SiteName)<1: index=0

        sql = "select EventName, StartDate from Event where EventName = '"+eventName+"' and StartDate = '"+startDate+"' and SiteName ='"+SiteName+"';"
        print(sql)
        self.cursor.execute(sql)
        if self.cursor.fetchall(): index=0
        if float(price)<0 or int(capacity) < 0 or int(staff)<1 or datetime.datetime.strptime(startDate,'%Y-%m-%d')>datetime.datetime.strptime(endDate,'%Y-%m-%d') or len(selectedstaff)<1 or len(selectedstaff)>staff: index=0

        if index==1:
            self.cursor.execute(SQL)
            self.db.commit()
            for eachStaff in selectedstaff:
                sql = "INSERT INTO AssignTo (StaffUsername, EventName, StartDate, SiteName) VALUES ('"+eachStaff+"','"+eventName+"','"+startDate+"','"+SiteName+"');"
                self.cursor.execute(sql)
                self.db.commit()

    def createEventWindowBackButtonClicked(self):
        # Click Return Buttion on Search Exhibit Window:
        # Destroy Search Exhibit Window
        # Display Choose Functionality Window
        self.createEventWindow.destroy()
        self.manageEventWindow.deiconify()

    def createManageStaffWindow(self):
        self.manageStaffWindow = Toplevel()
        self.manageStaffWindow.title("View/Edit Event")

    def buildManageStaffWindow(self,manageStaffWindow):

        # Title Label
        createEventLabel = Label(manageStaffWindow, text="Manage Staff", font="Verdana 10 bold ")
        createEventLabel.grid(row=1, column=2, sticky=W + E)

        # site label
        siteLabel = Label(manageStaffWindow, text="Site", font="Verdana 10 bold")
        siteLabel.grid(row=2, column=2)
        SQLCommand = "SELECT DISTINCT SiteName from AssignTo"
        self.cursor.execute(SQLCommand)
        SiteTuple = self.cursor.fetchall()
        # SiteList = ["Inman Park", "yes"]
        SiteList = []
        for element in SiteTuple: SiteList.append(element[0])
        Site = StringVar()
        # Site.set("Inman Park")
        Site.set(SiteList[0])
        SiteMenu = OptionMenu(manageStaffWindow, Site, *SiteList)
        SiteMenu.config(width= 20)
        SiteMenu.grid(row=2, column=3)

		# first name label
        fnameLabel = Label(manageStaffWindow, text="First Name", font="Verdana 10 bold")
        fnameLabel.grid(row=3, column=1)
        firstName = StringVar()
        fname = Entry(manageStaffWindow, textvariable=firstName, width=20)
        fname.grid(row=3, column=2)

        # name label
        lnameLabel = Label(manageStaffWindow, text="Last Name", font="Verdana 10 bold")
        lnameLabel.grid(row=3, column=3)
        lastName = StringVar()
        lname = Entry(manageStaffWindow, textvariable=lastName, width=20)
        lname.grid(row=3, column=4)

        #Start date
        viewStartDateLabel = Label(manageStaffWindow, text="Start Date", font="Verdana 10 bold")
        viewStartDateLabel.grid(row=4, column=1)
        StartDate= StringVar(value='YYYY-MM-DD')
        showStartDate = Entry(manageStaffWindow, textvariable=StartDate, width=10)
        showStartDate.grid(row=4, column=2, sticky=W+E)

        #End date
        viewEndDateLabel = Label(manageStaffWindow, text="End Date", font="Verdana 10 bold")
        viewEndDateLabel.grid(row=4, column=3)
        EndDate= StringVar(value='YYYY-MM-DD')
        showEndDate = Entry(manageStaffWindow, textvariable=EndDate, width=10)
        showEndDate.grid(row=4, column=4, sticky=W+E)

        def manageStaffWindowFilterButtonClicked():
            print(str(Site.get()), str(firstName.get()),
                  str(lastName.get()), str(StartDate.get()), str(EndDate.get()))
            self.filterStaff(Site.get(), firstName.get(), lastName.get(), StartDate.get(), EndDate.get())

        # filter Button
        filterButton = Button(manageStaffWindow, text="Filter", command=manageStaffWindowFilterButtonClicked)
        filterButton.grid(row=8, column=4)

        # back Button
        backButton = Button(manageStaffWindow, text="Back", command=self.manageStaffWindowBackButtonClicked)
        backButton.grid(row=8, column=1)

        # search table
        self.staff_table = ttk.Treeview(self.manageStaffWindow)
        self.staff_table['columns'] = ("Staff Name", "Event Shifts")

        self.staff_table.heading("Staff Name", text='Staff Name', anchor='w')
        self.staff_table.column("Staff Name", minwidth=1)

        self.staff_table.heading("Event Shifts", text="Event Shifts", anchor='w')
        self.staff_table.column("Event Shifts", minwidth=1)

        self.staff_table['show'] = 'headings'
        self.staff_table.grid(row=7, column=2, columnspan=2)

    def filterStaff(self,Site,firstName,lastName,StartDate,EndDate):
        SQL = "SELECT Lastname, Firstname, count(EventName) as shifts\
				from AssignTo\
				join User on StaffUsername = Username"

        SQL+=" where "

        if Site:
            SQL = SQL + " SiteName = '"+Site+"'";
        if firstName:
            SQL = SQL + " AND Firstname = '"+firstName+"'";
        if lastName:
            SQL = SQL + " AND Lastname = '"+lastName+"'";
        if EndDate != "YYYY-MM-DD":
            SQL = SQL + " AND StartDate <= '"+EndDate+"'";
        if StartDate != "YYYY-MM-DD":
            SQL = SQL + " AND StartDate >= '"+StartDate+"'";
        SQL = SQL+' group by StaffUsername ;'
        # print(SQL)

        self.cursor.execute(SQL)
        result_check = self.cursor.fetchall()
        self.staff_table.delete(*self.staff_table.get_children())
        # print(result_check)
        for i, result in enumerate(result_check):
            self.staff_table.insert("",i, value=(str(result[0])+' '+str(result[1]),str(result[2])))
        self.db.commit()

    def manageStaffWindowBackButtonClicked(self):
        # Click Return Buttion on Search Exhibit Window:
        # Destroy Search Exhibit Window
        # Display Choose Functionality Window
        self.manageStaffWindow.destroy()
        self.previous.deiconify()

#=========Screen 28 Manager Staff Window============

    def createManageStaffWindow(self):
        self.manageStaffWindow = Toplevel()
        self.manageStaffWindow.title("View/Edit Event")

    def buildManageStaffWindow(self,manageStaffWindow):

        # Title Label
        createEventLabel = Label(manageStaffWindow, text="Manage Staff", font="Verdana 10 bold ")
        createEventLabel.grid(row=1, column=2, sticky=W + E)

        # site label
        siteLabel = Label(manageStaffWindow, text="Site", font="Verdana 10 bold")
        siteLabel.grid(row=2, column=2)
        SQLCommand = "SELECT DISTINCT SiteName from AssignTo"
        self.cursor.execute(SQLCommand)
        SiteTuple = self.cursor.fetchall()
        # SiteList = ["Inman Park", "yes"]
        SiteList = []
        for element in SiteTuple: SiteList.append(element[0])
        Site = StringVar()
        # Site.set("Inman Park")
        Site.set(SiteList[0])
        SiteMenu = OptionMenu(manageStaffWindow, Site, *SiteList)
        SiteMenu.config(width= 20)
        SiteMenu.grid(row=2, column=3)

		# first name label
        fnameLabel = Label(manageStaffWindow, text="First Name", font="Verdana 10 bold")
        fnameLabel.grid(row=3, column=1)
        firstName = StringVar()
        fname = Entry(manageStaffWindow, textvariable=firstName, width=20)
        fname.grid(row=3, column=2)

        # name label
        lnameLabel = Label(manageStaffWindow, text="Last Name", font="Verdana 10 bold")
        lnameLabel.grid(row=3, column=3)
        lastName = StringVar()
        lname = Entry(manageStaffWindow, textvariable=lastName, width=20)
        lname.grid(row=3, column=4)

        #Start date
        viewStartDateLabel = Label(manageStaffWindow, text="Start Date", font="Verdana 10 bold")
        viewStartDateLabel.grid(row=4, column=1)
        StartDate= StringVar(value='YYYY-MM-DD')
        showStartDate = Entry(manageStaffWindow, textvariable=StartDate, width=10)
        showStartDate.grid(row=4, column=2, sticky=W+E)

        #End date
        viewEndDateLabel = Label(manageStaffWindow, text="End Date", font="Verdana 10 bold")
        viewEndDateLabel.grid(row=4, column=3)
        EndDate= StringVar(value='YYYY-MM-DD')
        showEndDate = Entry(manageStaffWindow, textvariable=EndDate, width=10)
        showEndDate.grid(row=4, column=4, sticky=W+E)

        def manageStaffWindowFilterButtonClicked():
            print(str(Site.get()), str(firstName.get()),
                  str(lastName.get()), str(StartDate.get()), str(EndDate.get()))
            self.filterStaff(Site.get(), firstName.get(), lastName.get(), StartDate.get(), EndDate.get())

        # filter Button
        filterButton = Button(manageStaffWindow, text="Filter", command=manageStaffWindowFilterButtonClicked)
        filterButton.grid(row=8, column=4)

        # back Button
        backButton = Button(manageStaffWindow, text="Back", command=self.manageStaffWindowBackButtonClicked)
        backButton.grid(row=8, column=1)

        # search table
        self.staff_table = ttk.Treeview(self.manageStaffWindow)
        self.staff_table['columns'] = ("Staff Name", "Event Shifts")

        self.staff_table.heading("Staff Name", text='Staff Name', anchor='w')
        self.staff_table.column("Staff Name", minwidth=1)

        self.staff_table.heading("Event Shifts", text="Event Shifts", anchor='w')
        self.staff_table.column("Event Shifts", minwidth=1)

        self.staff_table['show'] = 'headings'
        self.staff_table.grid(row=7, column=2, columnspan=2)

    def filterStaff(self,Site,firstName,lastName,StartDate,EndDate):
        SQL = "SELECT Lastname, Firstname, count(EventName) as shifts\
				from AssignTo\
				join User on StaffUsername = Username"

        SQL+=" where "

        if Site:
            SQL = SQL + " SiteName = '"+Site+"'";
        if firstName:
            SQL = SQL + " AND Firstname = '"+firstName+"'";
        if lastName:
            SQL = SQL + " AND Lastname = '"+lastName+"'";
        if EndDate != "YYYY-MM-DD":
            SQL = SQL + " AND StartDate <= '"+EndDate+"'";
        if StartDate != "YYYY-MM-DD":
            SQL = SQL + " AND StartDate >= '"+StartDate+"'";
        SQL = SQL+' group by StaffUsername ;'
        # print(SQL)

        self.cursor.execute(SQL)
        result_check = self.cursor.fetchall()
        self.staff_table.delete(*self.staff_table.get_children())
        # print(result_check)
        for i, result in enumerate(result_check):
            self.staff_table.insert("",i, value=(str(result[0])+' '+str(result[1]),str(result[2])))
        self.db.commit()

    def manageStaffWindowBackButtonClicked(self):
        # Click Return Buttion on Search Exhibit Window:
        # Destroy Search Exhibit Window
        # Display Choose Functionality Window
        self.manageStaffWindow.destroy()
        self.previous.deiconify()

#=========Screen 29 Manager Site Report Window============

    def createSiteReportWindow(self):
        self.siteReportWindow = Toplevel()
        self.siteReportWindow.title("Site Report")
        self.siteReportWindow.geometry("600x600")

    def buildSiteReportWindow(self,siteReportWindow):
        # Title Label
        siteReportLabel = Label(siteReportWindow, text="Site Report", font="Verdana 13 bold ")
        siteReportLabel.grid(row=1, column=2, sticky=W + E,pady=3)

        # start date entry
        startLabel = Label(siteReportWindow, text="Start Date", font="Verdana 10 bold")
        startLabel.grid(row=2, column=1,pady=3)
        startDate = StringVar()
        start = Entry(siteReportWindow, textvariable=startDate, width=10)
        start.grid(row=2, column=2,pady=3)

        # end date entry
        endLabel = Label(siteReportWindow, text="End Date", font="Verdana 10 bold")
        endLabel.grid(row=2, column=3,pady=3)
        endDate = StringVar()
        end = Entry(siteReportWindow, textvariable=endDate, width=10)
        end.grid(row=2, column=4,pady=3)

        # event count range label
        eventRangeLabel = Label(siteReportWindow, text = "Event Count Range", font = "Verdana 10 bold")
        eventRangeLabel.grid(row=3, column = 1,pady=3)
        # minimum duration entry
        minEvent = IntVar()
        minEventEntry = Entry(siteReportWindow, textvariable=minEvent, width=10)
        minEventEntry.grid(row=3, column=2,pady=3)
        # dash in between
        dash1 = Label(siteReportWindow, text = " - ", font = "Verdana 10 bold")
        dash1.grid(row=3, column = 3,pady=3)
        # maximum duration entry
        maxEvent = IntVar()
        maxEventEntry = Entry(siteReportWindow, textvariable=maxEvent, width=10)
        maxEventEntry.grid(row=3, column=4,pady=3)

        # staff count range label
        staffRangeLabel = Label(siteReportWindow, text = "Staff Count Range", font = "Verdana 10 bold")
        staffRangeLabel.grid(row=4, column = 1,pady=3)
        # minimum duration entry
        minStaff = IntVar()
        minStaffEntry = Entry(siteReportWindow, textvariable=minStaff, width=10)
        minStaffEntry.grid(row=4, column=2,pady=3)
        # dash in between
        dash2 = Label(siteReportWindow, text = " - ", font = "Verdana 10 bold")
        dash2.grid(row=4, column = 3,pady=3)
        # maximum duration entry
        maxStaff = IntVar()
        maxStaffEntry = Entry(siteReportWindow, textvariable=maxStaff, width=10)
        maxStaffEntry.grid(row=4, column=4,pady=3)

        # total visits range label
        visitsRangeLabel = Label(siteReportWindow, text = "Total Visits Range", font = "Verdana 10 bold")
        visitsRangeLabel.grid(row=5, column = 1,pady=3)
        # minimum duration entry
        minVisits = IntVar()
        minVisitsEntry = Entry(siteReportWindow, textvariable=minVisits, width=10)
        minVisitsEntry.grid(row=5, column=2,pady=3)
        # dash in between
        dash3 = Label(siteReportWindow, text = " - ", font = "Verdana 10 bold")
        dash3.grid(row=5, column = 3,pady=3)
        # maximum duration entry
        maxVisits = IntVar()
        maxVisitsEntry = Entry(siteReportWindow, textvariable=maxVisits, width=10)
        maxVisitsEntry.grid(row=5, column=4,pady=3)

        # total revenue range label
        revenueRangeLabel = Label(siteReportWindow, text = "Total Revenue Range", font = "Verdana 10 bold")
        revenueRangeLabel.grid(row=6, column = 1,pady=3)
        # minimum duration entry
        minRevenue = IntVar()
        minRevenueEntry = Entry(siteReportWindow, textvariable=minRevenue, width=10)
        minRevenueEntry.grid(row=6, column=2,pady=3)
        # dash in between
        dash4 = Label(siteReportWindow, text = " - ", font = "Verdana 10 bold")
        dash4.grid(row=6, column = 3,pady=3)
        # maximum duration entry
        maxRevenue = IntVar()
        maxRevenueEntry = Entry(siteReportWindow, textvariable=maxRevenue, width=10)
        maxRevenueEntry.grid(row=6, column=4,pady=3)

        #select date entry
        selectDateEntryLabel = Label(siteReportWindow, text = "Date for Details", font = "Verdana 10 bold")
        selectDateEntryLabel.grid(row=8, column = 1,pady=3)
        selectDate= StringVar()
        selectDateEntry = Entry(siteReportWindow, textvariable=selectDate, width=10)
        selectDateEntry.grid(row=8, column=2,pady=3)

        def siteReportWindowFilterBottonClicked():
            self.filterSite(startDate.get(), endDate.get(), minEvent.get(),maxEvent.get(),minStaff.get(),
	            	maxStaff.get(), minVisits.get(), maxVisits.get(), minRevenue.get(), maxRevenue.get())

        # filter Button
        filterButton = Button(siteReportWindow, text="Filter", command=siteReportWindowFilterBottonClicked)
        filterButton.grid(row=7, column=4,pady=3)

        def siteReportWindowDailyDetailBottonClicked():
            self.createDailyDetailWindow()
            self.buildDailyDetailWindow(selectDate.get())

        # daily detail
        detailButton = Button(siteReportWindow, text="Daily Detail", command=siteReportWindowDailyDetailBottonClicked)
        detailButton.grid(row=9, column=4,pady=3)
        # back Button
        backButton = Button(siteReportWindow, text="Back", command=self.siteReportWindowBackButtonClicked)
        backButton.grid(row=11, column=4,pady=3)

        # search table
        self.tv_site_report = ttk.Treeview(siteReportWindow)
        self.tv_site_report['columns'] = ("Date", "Event Count", "Staff Count", "Total Visits", "Total Revenues ($)")

        self.tv_site_report.heading("Date", text='Date', anchor='w')
        self.tv_site_report.column("Date", width=100)

        self.tv_site_report.heading("Event Count", text="Event Count", anchor='w')
        self.tv_site_report.column("Event Count",  width=100)

        self.tv_site_report.heading("Staff Count", text="Staff Count")
        self.tv_site_report.column("Staff Count", width=100)

        self.tv_site_report.heading("Total Visits", text=" Total Visits")
        self.tv_site_report.column("Total Visits",  width=100)

        self.tv_site_report.heading("Total Revenues ($)", text="Total Revenues ($)")
        self.tv_site_report.column("Total Revenues ($)",  width=100)

        self.tv_site_report['show'] = 'headings'
        self.tv_site_report.grid(row=10, column=1, columnspan = 4  )

    def filterSite(self,startDate, endDate, minEvent,maxEvent,minStaff,maxStaff, minVisits, maxVisits, minRevenue, maxRevenue):
        self.searchEmployeeInformation()################################################### do it in login window
        SQL = "SELECT SiteName  from Site where ManagerUsername = '" + self.Username + "'";
        self.cursor.execute(SQL)
        temp= self.cursor.fetchall()
        self.manageSiteName = str(temp[0][0])
        if startDate and endDate :
            startDate_date = datetime.datetime.strptime(startDate,'%Y-%m-%d')
            endDate_date = datetime.datetime.strptime(endDate,'%Y-%m-%d')
            timeList = []
            while startDate_date <= endDate_date:
                i = datetime.datetime.strftime(startDate_date,'%Y-%m-%d')
                timeList.append(str(i))
                startDate_date = startDate_date + datetime.timedelta(days = 1)
        else:
           messagebox.showwarning("Please input Start Date and End Date.")
        #eventnumber and staffnumber
        eventCountList=[]
        staffCountList=[]
        ifShow = []
        for date in timeList:
            sql = "select count(*), SUM(MinStaffRequired) from Event where SiteName = '"+ self.manageSiteName\
                + "' and StartDate <= '"+ date + "' and EndDate >= '"+ date+"';"
            self.cursor.execute(sql)
            temp= self.cursor.fetchall()
            eventCountList.append(temp[0][0])
            staffCountList.append(temp[0][1])
            ifShow.append(1)
        #replace none in staff
        for i in range(len(staffCountList)):
            if staffCountList[i] is None : staffCountList[i]=0
        #total visit number
        totalVisitsList =[]
        for date in  timeList:
            sql = "select count(*) from VisitSite where SiteName = '"+ self.manageSiteName+"' and VisitSiteDate = '"+ date+"';"
            self.cursor.execute(sql)
            temp= self.cursor.fetchall()
            totalVisitsList.append(temp[0][0])
        #Revenue
        totalRevenueList=[]
        for date in timeList:
            revenue = 0
            sql = "select EventName,EventPrice,StartDate from Event where SiteName = '"+ self.manageSiteName\
                + "' and StartDate <= '"+ date + "' and EndDate >= '"+ date+"';"
            self.cursor.execute(sql)
            temp= self.cursor.fetchall()
            eventNameList = []
            eventPriceList = []
            eventStartDateList = []
            eventVisitsList = []
            for i in range(len(temp)):
                eventNameList.append(str(temp[0][0]))
                eventPriceList.append(temp[0][1])
                eventStartDateList.append(str(temp[0][2]))
            for i in range(len(eventNameList)):
                sql = "select count(*) from VisitEvent where SiteName = '"+ self.manageSiteName\
                        + "' and StartDate = '"+ eventStartDateList[i] + "' and VisitEventName = '"+ eventNameList[i]+ "' and VisitEventDate = '"+ date+"';"
                self.cursor.execute(sql)
                temp= self.cursor.fetchall()
                eventVisitsList.append(temp[0][0])
            for i in range(len(eventNameList)):
                revenue += eventPriceList[i] * eventVisitsList[i]
            totalRevenueList.append(revenue)
        #minEvent,maxEvent,minStaff,maxStaff, minVisits, maxVisits, minRevenue, maxRevenue
        if minStaff>=0  and maxStaff>minStaff:
            for i in range(len(timeList)):
                if ifShow[i] == 1:
                    if staffCountList[i]<minStaff or staffCountList[i]>maxStaff: ifShow[i]=0
        if minEvent>=0  and maxEvent>minEvent:
            for i in range(len(timeList)):
                if ifShow[i] == 1:
                    if eventCountList[i]<minEvent or eventCountList[i]>maxEvent: ifShow[i]=0
        if minVisits>=0  and maxVisits>minVisits:
            for i in range(len(timeList)):
                if ifShow[i] == 1:
                    if totalVisitsList[i]<minVisits or totalVisitsList[i]>maxVisits: ifShow[i]=0
        if minRevenue>=0  and maxRevenue>minRevenue:
            for i in range(len(timeList)):
                if ifShow[i] == 1:
                    if totalRevenueList[i]<minRevenue or totalRevenueList[i]>maxRevenue: ifShow[i]=0
        #put into tree view
        j=0
        self.tv_site_report.delete(*self.tv_site_report.get_children())
        for i in range(len(timeList)):
            if ifShow[i]==1:
                self.tv_site_report.insert("",j, value=(str(timeList[i]),str(eventCountList[i])\
                                                ,str(staffCountList[i]),str(totalVisitsList[i]),str(totalRevenueList[i])))
                j+=1
        self.db.commit()

    def siteReportWindowBackButtonClicked(self):
        # Click Return Buttion on Search Exhibit Window:
        # Destroy Search Exhibit Window
        # Display Choose Functionality Window
        self.siteReportWindow.destroy()
        self.previous.deiconify()

# ==========Screen 30 Manager Daily Detail================

    def createDailyDetailWindow(self):
        self.dailyDetailWindow = Toplevel()
        self.dailyDetailWindow.title("Exhibit Detail")
        self.siteReportWindow.geometry("600x400")

    def buildDailyDetailWindow(self,date):

        # Title Label
        dailyDetailLabel = Label(self.dailyDetailWindow, text="Daily Detail", font="Verdana 10 bold ")
        dailyDetailLabel.grid(row=1, column=2, columnspan=2, sticky=W + E)

        # search table
        self.daily_detail = ttk.Treeview(self.dailyDetailWindow)
        self.daily_detail['columns'] = ("Event", "Staff", "Visits", "Revenue")

        self.daily_detail.heading("Event", text='Event Name', anchor='w')
        self.daily_detail.column("Event", width=150)

        self.daily_detail.heading("Staff", text="Staff Names", anchor='w')
        self.daily_detail.column("Staff", width=100)

        self.daily_detail.heading("Visits", text='Visits', anchor='w')
        self.daily_detail.column("Visits", width=50)

        self.daily_detail.heading("Revenue", text="Revenue ($)", anchor='w')
        self.daily_detail.column("Revenue", width=100)

        self.daily_detail['show'] = 'headings'
        self.daily_detail.grid(row=2, column=1, columnspan=4)

        def getContent(date):
            sql = "select EventName,StartDate,EventPrice from Event where SiteName = '"+ self.manageSiteName\
                + "' and StartDate <= '"+ date + "' and EndDate >= '"+ date+"';"
            self.cursor.execute(sql)
            temp= self.cursor.fetchall()
            print(temp)
            startDateList = []
            eventNameList = []
            staffList = []
            visitsList = []
            revenueLsit = []
            eventPriceList=[]
            for i in range(len(temp)):
                eventNameList.append(temp[i][0])
                startDateList.append(str(temp[i][1]))
                eventPriceList.append(temp[i][2])
            for i in range(len(eventNameList)):
                sql = "select StaffUsername from AssignTo where SiteName = '"+ self.manageSiteName\
                    + "' and StartDate = '"+ startDateList[i] + "' and EventName = '"+ eventNameList[i]+"';"
                self.cursor.execute(sql)
                temp= self.cursor.fetchall()
                staffTemp = []
                for element in temp:
                    print(element)
                    staffTemp.append(str(element[0]))
                staffList.append(staffTemp)
            for i in range(len(eventNameList)):
                sql = "select count(*) from VisitEvent where SiteName = '"+ self.manageSiteName\
                        + "' and StartDate = '"+ startDateList[i] + "' and VisitEventName = '"+ eventNameList[i]+ "' and VisitEventDate = '"+ date+"';"
                self.cursor.execute(sql)
                temp= self.cursor.fetchall()
                visitsList.append(temp[0][0])
            for i in range(len(eventNameList)):
                revenueLsit.append(visitsList[i]*eventPriceList[i])

            self.daily_detail.delete(*self.daily_detail.get_children())
            j=0;
            for i in range(len(eventNameList)):
                self.daily_detail.insert("",j, value=(str(eventNameList[i]),str(staffList[i][0])\
                                            ,str(visitsList[i]),str(revenueLsit[i])))
                j = j+1
                if len(staffList[i])>1:
                    x=1
                    while x <len(staffList[i]):
                        self.daily_detail.insert("",j, value=("",str(staffList[i][x]),"",""))
                        x = x + 1
                        j = j+1
            self.db.commit()
        ####function  define end
        getContent(date)
        backButton = Button(self.dailyDetailWindow,text="Back", command=self.dailyDetailWindowBackButtonClicked)
        backButton.grid(row=3, column=2,pady=3)

    def dailyDetailWindowBackButtonClicked(self):
        self.dailyDetailWindow.destroy()
        self.siteReportWindow.deiconify()

#==========31 Staff View Schedule=============#
    def createStaffViewScheduleWindow(self):
        self.staffViewScheduleWindow = Toplevel()
        self.staffViewScheduleWindow.title("Staff View Schedule")
        self.staffViewScheduleWindow.geometry("900x500")

    def buildStaffViewScheduleWindow(self, staffViewScheduleWindow):
        #Label
        # Staff view schedule label
        staffViewScheduleLabel = Label(staffViewScheduleWindow, text="View Schedule",font = "Verdana 15 bold ")
        staffViewScheduleLabel.grid(row=1, column=3, sticky=W+E,pady=3)
        # event name label
        eventNameLabel = Label(staffViewScheduleWindow, text="Event Name")
        eventNameLabel.grid(row=2, column=1,sticky=W,pady=3)
        # description key word label
        descriptionKeywordLabel = Label(staffViewScheduleWindow, text="Description Keyword")
        descriptionKeywordLabel.grid(row=2, column=3, sticky=W,pady=3)
        # start date
        startDateLabel = Label(staffViewScheduleWindow, text="Start Date")
        startDateLabel .grid(row=3, column=1,sticky=W,pady=3)
        # End date
        endDateLabel = Label(staffViewScheduleWindow, text='End Date')
        endDateLabel.grid(row=3, column=3,sticky=W,pady=3)
        # View Detail
        viewDetailLabel = Label(staffViewScheduleWindow, text='EventNumber')
        viewDetailLabel.grid(row=5, column=1,sticky=W,pady=3)

        #Entry
        #Event name entry
        eventName = StringVar()
        eventNameEntry = Entry(staffViewScheduleWindow, textvariable=eventName , width=20)
        eventNameEntry.grid(row=2, column=2, sticky=W,pady=3)
        # Description keyword entry
        descriptionKeyword = StringVar()
        descriptionKeywordEntry= Entry(staffViewScheduleWindow, textvariable=descriptionKeyword  , width=20)
        descriptionKeywordEntry.grid(row=2, column=4, sticky=W,pady=3)
        # start date entry
        startDate = StringVar()
        startDateEntry = Entry(staffViewScheduleWindow, textvariable=startDate , width=20)
        startDateEntry.grid(row=3, column=2, sticky=W,pady=3)
        # end date entry
        endDate = StringVar()
        endDateEntry = Entry(staffViewScheduleWindow, textvariable=endDate , width=20)
        endDateEntry.grid(row=3, column=4, sticky=W,pady=3)
        # number of event entry
        eventNumber = StringVar()
        eventNumberEntry = Entry(staffViewScheduleWindow, textvariable=eventNumber, width=20)
        eventNumberEntry.grid(row=5, column=2, sticky=W,pady=3)

        #Button
        def filter_StaffViewScheduleWindow():
            self.staff_view_schedule_result=[];
            self.filterStaffSchedule_FilterButtonClicked(eventNameEntry.get(), descriptionKeywordEntry.get(), startDateEntry.get(), endDateEntry.get())
        def viewEvent_StaffViewScheduleWindow():
            rowNumber = eventNumber.get()
            #print(rowNumber)
            self.viewDetailStaffSchedule_ViewButtonClicked(int(rowNumber))
        ##creat window!!

        filterButton = Button(staffViewScheduleWindow,text = "Filter",command = filter_StaffViewScheduleWindow,width = 10)
        viewEventButton = Button(staffViewScheduleWindow,text = "View Event",command = viewEvent_StaffViewScheduleWindow,width = 10)
        backButton = Button(staffViewScheduleWindow,text = "Filter",command = self.staffManageProfileBackButtonClicked)
        filterButton.grid(row = 4, column=4,sticky=W,pady=3,)
        viewEventButton.grid(row = 6, column=4,sticky=W,pady=3)

        # TABLE
        self.staff_view_schedule = ttk.Treeview(staffViewScheduleWindow)
        self.staff_view_schedule['columns'] = ("Event Number","Event Name", "Site Name", "Start Date","End Date", "Staff Count",)

        self.staff_view_schedule.heading("Event Name", text='Event Name', anchor='w')
        self.staff_view_schedule.column("Event Name", width=250)

        self.staff_view_schedule.heading("Site Name", text="Site Name", anchor='w')
        self.staff_view_schedule.column("Site Name",  width=200)

        self.staff_view_schedule.heading("Start Date", text="Start Date")
        self.staff_view_schedule.column("Start Date", width=100)

        self.staff_view_schedule.heading("End Date", text="End Date")
        self.staff_view_schedule.column("End Date", width=100)

        self.staff_view_schedule.heading("Staff Count", text="Staff Count")
        self.staff_view_schedule.column("Staff Count", width=100)

        self.staff_view_schedule.heading("Event Number", text="Event Number")
        self.staff_view_schedule.column("Event Number", width=100)

        self.staff_view_schedule['show'] = 'headings'
        self.staff_view_schedule.grid(row=7, column=1, columnspan = 4,sticky=W,padx=5,pady=5)

    def filterStaffSchedule_FilterButtonClicked(self, eventName, descriptionKeyword, startDate, endDate):
        sql = "SELECT EventName, SiteName, StartDate, EndDate, MinStaffRequired, Description FROM Event"

        if eventName or startDate or endDate:
            sql+=" WHERE "
            index = 0;

        if eventName:
            if index >0: SQL+=" AND "
            sql = sql + " EventName = '"+eventName+"'";
            index+=1;
        if startDate:
            if index >0: SQL+=" AND "
            sql = sql + " StartDate >= '"+startDate+"'";
            index+=1;
        if endDate:
            if index >0: SQL+=" AND "
            sql = sql + " EndDate <= '"+EndDate+"'";
            index+=1;
        sql = sql+';'
        print(sql)

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.staff_view_schedule.delete(*self.staff_view_schedule.get_children())
        show = []
        if descriptionKeyword:
            for element in result:
                isContain = element[5].find(descriptionKeyword)
                if isContain >= 0:
                    show.append(element)
        else:
            show = result

        for i, element in enumerate(show):
            self.staff_view_schedule.insert("",i, value=(i,str(element[0]),str(element[1]),str(element[2]),str(element[3]),str(element[4]),str(element[5])))

        self.staff_view_schedule_result=show;
        self.db.commit()

    def viewDetailStaffSchedule_ViewButtonClicked(self,rowNumber):
        temp = self.staff_view_schedule_result[int(rowNumber)]
        self.createEventDetailWindow()
        #print(temp)
        self.buildEventDetailWindow(self.eventDetailWindow, temp[0], temp[2], temp[1])

    def staffManageProfileBackButtonClicked(self):
        self.registerNavigationWindow.withdraw()
        self.previous.withdraw()

# ==========Screen 32 Staff Event Detail================

    def createEventDetailWindow(self):
        self.eventDetailWindow = Toplevel()
        self.eventDetailWindow.title("Exhibit Detail")

    def buildEventDetailWindow(self, eventDetailWindow, eventName, startDate, siteName):
        self.searchEventInformation(eventName, startDate,siteName)
        # Title Label
        eventDetailLabel = Label(eventDetailWindow, text="Event Detail")
        eventDetailLabel.grid(row=1, column=2, columnspan=2, sticky=W + E)

        # Event Name Label
        EventLabel = Label(eventDetailWindow, text="Event")
        EventLabel.grid(row=2, column=1, sticky=W)
        showEventLabel = Label(eventDetailWindow, text=self.eventDetailWindow_EventName, font="underline")
        showEventLabel.grid(row=2, column=2, columnspan=2, sticky=W)
        # Site Name Label
        SiteLabel = Label(eventDetailWindow, text="Site")
        SiteLabel.grid(row=2, column=4,sticky=W)
        showSiteLabel = Label(eventDetailWindow, text=self.eventDetailWindow_SiteName, font="underline")
        showSiteLabel.grid(row=2, column=5, columnspan=2, sticky=W)
        # start date Label
        startDateLabel = Label(eventDetailWindow, text="Start Date")
        startDateLabel.grid(row=3, column=1,sticky=W)
        showstartDateLabel = Label(eventDetailWindow, text=self.eventDetailWindow_StartDate, font="underline")
        showstartDateLabel.grid(row=3, column=2)
        # end date Label
        endDateLabel = Label(eventDetailWindow, text="End Date")
        endDateLabel.grid(row=3, column=3,sticky=W)
        showendDateLabel = Label(eventDetailWindow, text=self.eventDetailWindow_EndDate, font="underline")
        showendDateLabel.grid(row=3, column=4)
        # Duration  Label
        durationLabel = Label(eventDetailWindow, text="Duration Days")
        durationLabel.grid(row=3, column=5,sticky=W)
        showdurationLabel = Label(eventDetailWindow, text=self.eventDetailWindow_Duration, font="underline")
        showdurationLabel.grid(row=3, column=6)
        # staff Label
        staffLabel = Label(eventDetailWindow, text="Staff Assigned")
        staffLabel.grid(row=4, column=1,sticky=W)
        showstaffLabel = []
        for i in range(self.eventDetailWindow__staff_count):
	        showstaffLabel = Label(eventDetailWindow, text=self.eventDetailWindow__staff_Firstname[i]+' '+self.eventDetailWindow__staff_Lastname[i], font="underline")
	        showstaffLabel.grid(row=4+i, column=2)
        # capacity Label
        capacityLabel = Label(eventDetailWindow, text="Capacity")
        capacityLabel.grid(row=4, column=3,sticky=W)
        showcapacityLabel = Label(eventDetailWindow, text=self.eventDetailWindow_Capacity, font="underline")
        showcapacityLabel.grid(row=4, column=4)
        # price  Label
        priceLabel = Label(eventDetailWindow, text="Price")
        priceLabel.grid(row=4, column=5,sticky=W)
        showpriceLabel = Label(eventDetailWindow, text=self.eventDetailWindow_EventPrice, font="underline")
        showpriceLabel.grid(row=4, column=6)
        # description  Label
        descriptionLabel = Label(eventDetailWindow, text="Description")
        descriptionLabel.grid(row=5+self.eventDetailWindow__staff_count, column=1,sticky=W)
        showdescriptionLabel = Label(eventDetailWindow, text=self.eventDetailWindow_Description, wraplength=370, anchor=W, justify=LEFT, font="underline")
        showdescriptionLabel.grid(row=5+self.eventDetailWindow__staff_count, column=2, columnspan=5, sticky=W)

        #Return Button
        BackButton = Button(eventDetailWindow, text="Back", command=self.eventDetailWindowBackButtonClicked)
        BackButton.grid(row=6+self.eventDetailWindow__staff_count, column=3,columnspan=2, pady=5,padx=5)

    def eventDetailWindowBackButtonClicked(self):
        #Go back to somewhere
        #self.createNewRegisterVisitorOnlyWindow()
        #self.buildNewRegisterVisitorOnlyWindow(self.newRegisterVisitorOnlyWindow)
        self.registerNavigationWindow.deiconify()
        self.eventDetailWindow.withdraw()

    def searchEventInformation(self, eventName, startDate_date,siteName):
        # sql = "SELECT *, EndDate - StartDate as Duration\
        #  from Event\
        #  WHERE EventName ='"+eventName+";"
         # WHERE EventName ='"+eventName+"'AND StartDate ="+startDate+";"
        startDate = datetime.datetime.strftime(startDate_date,'%Y-%m-%d')
        #print(startDate,siteName,eventName)
        sql = "SELECT *, EndDate - StartDate as Duration from Event WHERE EventName ='"+ eventName + "' AND StartDate = '"+startDate+"' And SiteName ='"+siteName+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        self.eventDetailWindow_EventName = str(temp[0][0])
        self.eventDetailWindow_StartDate = str(temp[0][2])
        self.eventDetailWindow_SiteName = str(temp[0][1])
        self.eventDetailWindow_EndDate = str(temp[0][3])
        self.eventDetailWindow_EventPrice = str(temp[0][4])
        self.eventDetailWindow_Capacity = str(temp[0][5])
        self.eventDetailWindow_Description = str(temp[0][6])
        self.eventDetailWindow_Duration = str(temp[0][8])


        sql = "SELECT Firstname, Lastname\
		         from AssignTo A\
		         join User U on StaffUsername = U.UserName\
		         where EventName ='"+self.eventDetailWindow_EventName+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        # print(temp)
        self.eventDetailWindow__staff_Firstname = []
        self.eventDetailWindow__staff_Lastname = []
        self.eventDetailWindow__staff_count = 0
        for element in temp:
        	self.eventDetailWindow__staff_count += 1
        	self.eventDetailWindow__staff_Firstname.append(element[0])
        	self.eventDetailWindow__staff_Lastname.append(element[1])

#=========33 Explore Event Window============
    def createExploreEventWindow(self):
        self.exploreEventWindow = Toplevel()
        self.exploreEventWindow.title("Explore Event")

    def buildExploreEventWindow(self,exploreEventWindow):
        self.result_exploreEvent_Visitor = []
        # Title
        viewExhibitLabel = Label(exploreEventWindow, text="Explore Event", font="Verdana 13 bold ")
        viewExhibitLabel.grid(row=1, column=1, columnspan=4, sticky=W+E,pady=5)

        #name
        nameLabel = Label(exploreEventWindow, text = "Name", font = "Verdana 10 bold")
        nameLabel.grid(row=2, column = 1,pady=5)
        nameEntry = StringVar()
        name = Entry(exploreEventWindow, textvariable=nameEntry, width=10)
        name.grid(row=2, column=2,pady=5)

        #Descrioption Keyword
        descriptionKeywordLabel = Label(exploreEventWindow, text = "Descrioption Keyword", font = "Verdana 10 bold")
        descriptionKeywordLabel.grid(row=2, column=3,pady=5)
        descriptionKeywordEntry = StringVar()
        descriptionKeyword = Entry(exploreEventWindow, textvariable=descriptionKeywordEntry, width=10)
        descriptionKeyword.grid(row=2, column=4,pady=5)

        # site name
        siteNameLabel = Label(exploreEventWindow, text = "Site Name", font = "Verdana 10 bold")
        siteNameLabel.grid(row=3, column=1,pady=5)
        # Site Name Drop Down Button
        sql = "SELECT SiteName FROM Site;"
        self.cursor.execute(sql)
        SiteTuple = self.cursor.fetchall()
        SiteList = []
        for i in SiteTuple:
            SiteList.append(i[0])
        Site = StringVar()
        Site.set("--ALL--")
        siteNameOptionMenu = OptionMenu(exploreEventWindow, Site, *SiteList)
        siteNameOptionMenu.config(width= 10)
        siteNameOptionMenu.grid(row=3, column=2, pady=5)

        # Start Date
        startDateLabel = Label(exploreEventWindow, text="Start Date", font="Verdana 10 bold ")
        startDateLabel.grid(row=4, column=1,pady=5)
        startDatetime = StringVar(value='YYYY-MM-DD')
        startDateLabel = Entry(exploreEventWindow, textvariable=startDatetime, width=10)
        startDateLabel.grid(row=4, column=2,pady=5)

        # End Date
        endDateLabel = Label(exploreEventWindow, text="End Date", font="Verdana 10 bold ")
        endDateLabel.grid(row=4, column=3,pady=5)
        endDatetime = StringVar(value='YYYY-MM-DD')
        endDateLabel = Entry(exploreEventWindow, textvariable=endDatetime, width=10)
        endDateLabel.grid(row=4, column=4,pady=5)

        #Total visit range
        totalVisitRangeLabel = Label(exploreEventWindow, text = "Total Visit Range", font = "Verdana 10 bold")
        totalVisitRangeLabel.grid(row=5, column = 1,pady=5,padx=5)
        mintotalVisitRangeEntry = StringVar()
        totalVisitRange = Entry(exploreEventWindow, textvariable=mintotalVisitRangeEntry, width=5)
        totalVisitRange.grid(row=5, column=2,pady=5,padx=5)
        totalVisitRangeLabel2 = Label(exploreEventWindow, text = "--", font = "Verdana 10 bold")
        totalVisitRangeLabel2.grid(row=5, column = 3,pady=5,padx=5)
        maxtotalVisitRangeEntry = StringVar()
        totalVisitRange2 = Entry(exploreEventWindow, textvariable=maxtotalVisitRangeEntry, width=5)
        totalVisitRange2.grid(row=5, column=4,pady=5,padx=5)

        #Ticket Price Range
        ticketPriceRangeLabel = Label(exploreEventWindow, text = "Total Price Range", font = "Verdana 10 bold")
        ticketPriceRangeLabel.grid(row=6, column =1, pady=5,padx=5)
        minticketPriceRangeEntry = StringVar()
        ticketPriceRange = Entry(exploreEventWindow, textvariable=minticketPriceRangeEntry, width=5)
        ticketPriceRange.grid(row=6, column=2,pady=5,padx=5)
        ticketPriceRangeLabel2 = Label(exploreEventWindow, text = "--", font = "Verdana 10 bold")
        ticketPriceRangeLabel2.grid(row=6, column = 3,pady=5,padx=5)
        maxticketPriceRangeEntry = StringVar()
        ticketPriceRange2 = Entry(exploreEventWindow, textvariable=maxticketPriceRangeEntry, width=5)
        ticketPriceRange2.grid(row=6, column=4, pady=5,padx=5)

        #Include Visited Checkbox
        includeVisited = IntVar()
        Checkbutton(exploreEventWindow, text="Include Visited", variable=includeVisited).grid(row=7, column=2,pady=5,padx=5)

        #Include Sold Out Checkbox
        includeSoldOutEvent = IntVar()
        Checkbutton(exploreEventWindow, text="Include Sold Out Event", variable=includeSoldOutEvent).grid(row=7, column=3,pady=5,padx=5)

        def exploreEvent_filter_Button_Clicked():
            print ("exploreEvent_filter_Button_Clicked")
            self.exploreEvent_filter_Visitor(nameEntry.get(), descriptionKeywordEntry.get(), Site.get(),
                    startDatetime.get(), endDatetime.get(), mintotalVisitRangeEntry.get(), maxtotalVisitRangeEntry.get(),
                    minticketPriceRangeEntry.get(), maxticketPriceRangeEntry.get(),
                    includeVisited.get(), includeSoldOutEvent.get())

        #filter Button
        filterButton = Button(exploreEventWindow, text="Filter", command=exploreEvent_filter_Button_Clicked, width = 12)
        filterButton.grid(row=8, column=2,pady=5,padx=5)

        #event Detail Button
        eventDetailButton = Button(exploreEventWindow, text="Event Detail", command=self.event_Detail_Button_Clicked,width = 12)
        eventDetailButton.grid(row=8, column=3,pady=5,padx=5)

        # table
        self.tv = ttk.Treeview(exploreEventWindow)
        self.tv['columns'] = ("Index","Event Name", "Site Name", "Ticket Price", "Ticket Remaining", "Total Visits", "My Visits")
        self.tv.heading("Index", text='Index', anchor='w')
        self.tv.column("Index", width=50)
        self.tv.heading("Event Name", text='Event Name▼', anchor='w')
        self.tv.column("Event Name", width=200)
        self.tv.heading("Site Name", text="Site Name▼", anchor='w')
        self.tv.column("Site Name",  width=200)
        self.tv.heading("Ticket Price", text="   Ticket Price▼")
        self.tv.column("Ticket Price", width=100)
        self.tv.heading("Ticket Remaining", text=" Ticket Remaining▼")
        self.tv.column("Ticket Remaining",  width=100)
        self.tv.heading("Total Visits", text="Total Visits▼")
        self.tv.column("Total Visits", width=100)
        self.tv.heading("My Visits", text="My Visits▼")
        self.tv.column("My Visits", width=100)
        self.tv['show'] = 'headings'
        self.tv.grid(row=9, column=1, columnspan=4,pady=5,padx=5)
        #txq
        self.tv["displaycolumns"]=("Event Name", "Site Name", "Ticket Price", "Ticket Remaining", "Total Visits", "My Visits")
        #txq
        self.seed_explore_event(includeVisited.get(), includeSoldOutEvent.get())

        self.tv.bind("<Double-1>",self.exploreEvent_onClick) #左键双击

        #Back Button
        backButton = Button(exploreEventWindow, text="Back", command=self.exploreEvent_back_Button_Clicked,width = 12)
        backButton.grid(row=10, column=2,columnspan=2, sticky=W+E, pady=5)
        #txq
    def seed_explore_event(self, includeVisited, includeSoldOutEvent):
        SQL = "select * from event"
        self.cursor.execute(SQL)
        result_ani = self.cursor.fetchall()
        self.tv.delete(*self.tv.get_children())
        eventNameList=[]
        siteNameList=[]
        descriptionList=[]
        priceList=[]
        self.startDateList=[]
        endDateList=[]
        capacityList=[]
        self.totalVisitList=[]
        self.remainingList=[]
        myVisitList=[]
        index=[]
        ifShow=[]
        for i in result_ani:
            eventNameList.append(str(i[0]))
            siteNameList.append(str(i[1]))
            priceList.append(i[4])
            self.startDateList.append(str(i[2]))
            endDateList.append(str(i[3]))
            capacityList.append(i[5])
            descriptionList.append(str(i[6]))
        for i in range(len(eventNameList)):
            index.append(i)
            ifShow.append(1)
            SQL="select count(*) from visitevent where visiteventname='"+eventNameList[i]+"' and sitename='"+siteNameList[i]+"' and startdate='"+self.startDateList[i]+"'"
            self.cursor.execute(SQL)
            result_ani = self.cursor.fetchall()
            self.totalVisitList.append(result_ani[0][0])
            self.remainingList.append(capacityList[i]-self.totalVisitList[i])
            # 加上以下四行
            sql2 = "SELECT Username from UserEmail WHERE Email ='"+self.loginEmailAddress+"';"
            self.cursor.execute(sql2)
            temp = self.cursor.fetchall()
            self.Username = str(temp[0][0])
            # 把hardcode的改成self.username
            SQL1=SQL+ " and visitorusername= '"+ self.Username+"'"
            self.cursor.execute(SQL1)
            result = self.cursor.fetchall()
            myVisitList.append(result[0][0])
        if includeVisited == 0: # not include event that i didnot visited => only include myVisit >0
            for i in range(len(eventNameList)):
                if ifShow[i] == 1:
                    if myVisitList[i] >0 : ifShow[i] = 0
        if includeSoldOutEvent == 0: # not include sold out => only include remaing >0
            for i in range(len(eventNameList)):
                if ifShow[i] == 1:
                    if self.remainingList[i] <= 0: ifShow[i] = 0

        #put into tree view
        j=0
        self.tv.delete(*self.tv.get_children())
        for i in range(len(eventNameList)):
            print (ifShow[i])
            if ifShow[i]==1:
                self.tv.insert("",j, value=(str(index[i]+1),str(eventNameList[i]),str(siteNameList[i]),str(priceList[i]),str(self.remainingList[i]),str(self.totalVisitList[i]),str(myVisitList[i])))
                j+=1

    def exploreEvent_filter_Visitor(self, eventName, descriptionKeyword, siteName, startDate, endDate,minTotalVisit, maxTotalVisit, minPrice, maxPrice, includeVisited, includeSoldOutEvent):
            SQL = "select * from event"
            self.cursor.execute(SQL)
            result_ani = self.cursor.fetchall()
            self.tv.delete(*self.tv.get_children())
            print(result_ani)
            print(len(result_ani))
            eventNameList=[]
            siteNameList=[]
            descriptionList=[]
            priceList=[]
            self.startDateList=[]
            endDateList=[]
            capacityList=[]
            self.totalVisitList=[]
            self.remainingList=[]
            myVisitList=[]
            index=[]
            ifShow=[]
            for i in result_ani:
                eventNameList.append(str(i[0]))
                siteNameList.append(str(i[1]))
                priceList.append(i[4])
                self.startDateList.append(str(i[2]))
                endDateList.append(str(i[3]))
                capacityList.append(i[5])
                descriptionList.append(str(i[6]))
            for i in range(len(eventNameList)):
                index.append(i)
                ifShow.append(1)
                SQL="select count(*) from visitevent where visiteventname='"+eventNameList[i]+"' and sitename='"+siteNameList[i]+"' and startdate='"+self.startDateList[i]+"'"
                self.cursor.execute(SQL)
                result_ani = self.cursor.fetchall()
                self.totalVisitList.append(result_ani[0][0])
                self.remainingList.append(capacityList[i]-self.totalVisitList[i])

                # txq
                # 加上以下四行
                sql2 = "SELECT Username from UserEmail WHERE Email ='"+self.loginEmailAddress+"';"
                self.cursor.execute(sql2)
                temp = self.cursor.fetchall()
                self.Username = str(temp[0][0])
                # txq
                # 把hardcode的改成self.username
                SQL1=SQL+ " and visitorusername= '"+ self.Username+"'"
                self.cursor.execute(SQL1)
                result = self.cursor.fetchall()
                myVisitList.append(result[0][0])
            # print("**************")
            # for i in range(len(eventNameList)):
            #   print(ifShow[i])
            if eventName:
                for i in range(len(eventNameList)):
                    if ifShow[i] == 1:
                        if (eventName in eventNameList[i]) == False: ifShow[i] = 0

            if descriptionKeyword:
                for i in range(len(eventNameList)):
                    if ifShow[i] == 1:
                        if (descriptionKeyword in descriptionList[i]) == False: ifShow[i] = 0

            if siteName != "--ALL--":
                for i in range(len(eventNameList)):
                    if ifShow[i] == 1:
                        if siteName != siteNameList[i]: ifShow[i] = 0

            if startDate !="YYYY-MM-DD" and startDate:
                startDate_date = datetime.datetime.strptime(startDate,'%Y-%m-%d')
                for i in range(len(eventNameList)):
                    if ifShow[i] == 1:
                        startDate_item = datetime.datetime.strptime(self.startDateList[i],'%Y-%m-%d')
                        if startDate_date > startDate_item: ifShow[i] = 0

            if endDate !="YYYY-MM-DD" and endDate:
                endDate_date = datetime.datetime.strptime(endDate,'%Y-%m-%d')
                for i in range(len(eventNameList)):
                    if ifShow[i] == 1:
                        endDate_item = datetime.datetime.strptime(endDateList[i],'%Y-%m-%d')
                        if endDate_date < endDate_item: ifShow[i] = 0
            if minTotalVisit:
                minTotalVisit_int = int(minTotalVisit)
                for i in range(len(eventNameList)):
                    if ifShow[i] == 1:
                        if minTotalVisit_int > self.totalVisitList[i]: ifShow[i] = 0
            if maxTotalVisit:
                maxTotalVisit_int = int(maxTotalVisit)
                for i in range(len(eventNameList)):
                    if ifShow[i] == 1:
                        if maxTotalVisit_int < self.totalVisitList[i]: ifShow[i] = 0
            if minPrice:
                minPrice_int = int(minPrice)
                for i in range(len(eventNameList)):
                    if ifShow[i] == 1:
                        print (type(priceList[i]))
                        priceItem_int = int(priceList[i])
                        if minPrice_int > priceList[i]: ifShow[i] = 0
            if maxPrice:
                maxPrice_int = int(maxPrice)
                for i in range(len(eventNameList)):
                    if ifShow[i] == 1:
                        priceItem_int = int(priceList[i])
                        if maxPrice_int < priceList[i]: ifShow[i] = 0
            if includeVisited == 0: # not include event that i didnot visited => only include myVisit >0
                for i in range(len(eventNameList)):
                    if ifShow[i] == 1:
                        if myVisitList[i] >0 : ifShow[i] = 0
            if includeSoldOutEvent == 0: # not include sold out => only include remaing >0
                for i in range(len(eventNameList)):
                    if ifShow[i] == 1:
                        if self.remainingList[i] <= 0: ifShow[i] = 0
            #put into tree view
            j=0
            self.tv.delete(*self.tv.get_children())
            for i in range(len(eventNameList)):
                print (ifShow[i])
                if ifShow[i]==1:
                    self.tv.insert("",j, value=(str(index[i]+1),str(eventNameList[i]),str(siteNameList[i]),str(priceList[i]),str(self.remainingList[i]),str(self.totalVisitList[i]),str(myVisitList[i])))
                    j+=1

    def event_Detail_Button_Clicked(self):
        curItem = self.tv.item(self.tv.focus())
        print (curItem)
        index=curItem['values'][0]
        eventName = curItem['values'][1]
        siteName = curItem['values'][2]
        ticketPrice = curItem['values'][3]
        ticketRemaining = curItem['values'][4]
        totalVisits = curItem['values'][5]
        myVisits = curItem['values'][6]
        self.createEventDetailWindow()
        self.buildEventDetailWindow(self.EventDetailWindow, index,eventName, siteName,
            ticketPrice, ticketRemaining, totalVisits, myVisits)

    def exploreEvent_back_Button_Clicked(self):
        print ("exploreEvent_back_Button_Clicked")
        self.exploreEventWindow.destroy()
        self.previous.deiconify()

    def exploreEvent_onClick(self,event):
        region = self.tv.identify_region(event.x, event.y)
        print (region)
        if region=="heading":
            print ("region=heading 未完待续")
        elif region=="cell":
            curItem = self.tv.item(self.tv.focus())
            print (curItem)
            eventName = curItem['values'][0]
            siteName = curItem['values'][1]
            ticketPrice = curItem['values'][2]
            ticketRemaining = curItem['values'][3]
            totalVisits = curItem['values'][4]
            myVisits = curItem['values'][5]
            self.createEventDetailWindow()
            self.buildEventDetailWindow(self.EventDetailWindow, index,eventName, siteName,ticketPrice, ticketRemaining, totalVisits, myVisits)

#=========34 Event Detail Window============
    def createEventDetailWindow(self):
        self.EventDetailWindow = Toplevel()
        self.EventDetailWindow.title("Event Detail")
        self.exploreEventWindow.withdraw()

    def buildEventDetailWindow(self, EventDetailWindow, index, eventName, siteName,ticketPrice, ticketRemaining,totalVisits,myVisits):
        # title label
        eventDetailWindow = Label(EventDetailWindow, text = "Event Detail", font = ("Verdana", 15))
        eventDetailWindow.grid(row=1, column=1, columnspan = 4,sticky=W+E, pady=3)

        index = index
        self.startDate = self.startDateList[index-1]
        eventName = str(eventName)
        self.Event_Detail_Page_EventName = eventName #log visit的时候用
        siteName = str(siteName)
        self.Event_Detail_Page_SiteName = siteName
        ticketPrice = str(ticketPrice)
        self.ticketRemaining = str(ticketRemaining)
        totalVisits = str(totalVisits)
        myVisits = str(myVisits)

        SQL="select Description, EndDate from event where sitename='"+siteName+"' and eventname='"+eventName+"' and startdate='"+ self.startDate+"'"
        self.cursor.execute(SQL)
        result_check = self.cursor.fetchall()
        print(result_check)
        print(len(result_check))
        print(result_check[0][1])

        description = str(result_check[0][0])
        self.endDate = str(result_check[0][1])

        # Event Name Label
        eventlabel = Label(EventDetailWindow, text="Event", font="Verdana 10 bold")
        eventlabel.grid(row=2, column=1, sticky=W)
        eventlabeltext = Label(EventDetailWindow, text=eventName, font="Helvetica 10 italic bold underline")
        eventlabeltext.grid(row=2, column=2, sticky=W)
        # Site Name label
        sitelabel = Label(EventDetailWindow, text="Site" , font="Verdana 10 bold")
        sitelabel.grid(row=2, column=3, sticky=W)
        sitelabeltext = Label(EventDetailWindow, text=siteName, font="Helvetica 10 italic bold underline")
        sitelabeltext.grid(row=2, column=4, sticky=W)
        # Start date label
        startdatelabel = Label(EventDetailWindow, text="Start Date" , font="Verdana 10 bold")
        startdatelabel.grid(row=3, column=1, sticky=W)
        startdatelabeltext = Label(EventDetailWindow, text=self.startDate, font="Helvetica 10 italic bold underline")
        startdatelabeltext.grid(row=3, column=2, sticky=W)
        # end date label
        enddatelabel = Label(EventDetailWindow, text="End Date" , font="Verdana 10 bold")
        enddatelabel.grid(row=3, column=3, sticky=W)
        enddatelabeltext = Label(EventDetailWindow, text=self.endDate, font="Helvetica 10 italic bold underline")
        enddatelabeltext.grid(row=3, column=4, sticky=W)
        # ticket price label
        ticketpricelabel = Label(EventDetailWindow, text="Ticket Price($)" , font="Verdana 10 bold")
        ticketpricelabel.grid(row=4, column=1, sticky=W)
        ticketpricelabeltext = Label(EventDetailWindow, text=ticketPrice, font="Helvetica 10 italic bold underline")
        ticketpricelabeltext.grid(row=4, column=2, sticky=W)
        # ticket remaining label
        ticketremaininglabel = Label(EventDetailWindow, text="Ticket Remaining" , font="Verdana 10 bold")
        ticketremaininglabel.grid(row=4, column=3, sticky=W)
        ticketremaininglabeltext = Label(EventDetailWindow, text=self.ticketRemaining, font="Helvetica 10 italic bold underline")
        ticketremaininglabeltext.grid(row=4, column=4, sticky=W)
        # Description label
        descriptionlabel = Label(EventDetailWindow, text="Description" , font="Verdana 10 bold")
        descriptionlabel.grid(row=5, column=1, sticky=W+N)
        descriptionlabeltext = Label(EventDetailWindow, text=description, font="Helvetica 10 italic bold underline", wraplength =370, anchor=W, justify=LEFT)
        descriptionlabeltext.grid(row=5, column=2, sticky=W, columnspan=3)
        # Visit Date
        visitDateLabel = Label(EventDetailWindow, text="Visit Date", font="Verdana 10 bold ")
        visitDateLabel.grid(row=6, column=1, sticky=W)
        self.visitDatetime = StringVar(value='YYYY-MM-DD')
        visitDateLabel = Entry(EventDetailWindow, textvariable=self.visitDatetime, width=10)
        visitDateLabel.grid(row=6, column=2, sticky=W, pady=5, padx=5)
        # log visit Button
        logVisitButton = Button(EventDetailWindow, text="Log Visit", command=self.logVisit_toEvent_Clicked,width =15)
        logVisitButton.grid(row=6, column=3)
        # back Button
        logBackButton = Button(EventDetailWindow, text="Back", command=self.eventDetail_back_Button_Clicked, width =15)
        logBackButton = grid(rwo=7,column = 2, clolumnspan = 2)

    def logVisit_toEvent_Clicked(self):
        print ("logVisit_toEvent_Clicked")
        # First check if remaining ticket = 0
        if int(self.ticketRemaining) <= 0:
            messagebox.showwarning("Warning", "There is no remaining ticket of this event, you cannot log visit to it.")
        # then check if date is filled
        elif not self.visitDatetime.get() or self.visitDatetime.get() == "YYYY-MM-DD":
            messagebox.showwarning("Visit Date input is empty", "Please enter a visit date before log.")
        # then check is date is between startdate and enddate
        elif self.visitDatetime.get():
            endDate_date = datetime.datetime.strptime(self.endDate,'%Y-%m-%d')
            startDate_date = datetime.datetime.strptime(self.startDate,'%Y-%m-%d')
            visitDatetime =datetime.datetime.strptime(self.visitDatetime.get(),'%Y-%m-%d')
            if startDate_date > visitDatetime or visitDatetime > endDate_date:
                messagebox.showwarning("Visit Date input is invalid", "Visit Date input is invalid.Please enter a date that is between event start date and end date.")
            else:
                # chaeck if the user has log visit to the same event on the same date
                sql = "SELECT Username from UserEmail WHERE Email ='"+self.loginEmailAddress+"';"
                self.cursor.execute(sql)
                temp = self.cursor.fetchall()
                self.Username = str(temp[0][0])

                SQL="select count(*) from visitevent where sitename='"+self.Event_Detail_Page_SiteName\
                +"' and visitorusername='"+self.Username+"' and visiteventdate='"+self.visitDatetime.get()+"' and startdate='"+\
                self.startDate+"' and VisitEventName= '"+self.Event_Detail_Page_EventName+"'"
                self.cursor.execute(SQL)
                result_ani = self.cursor.fetchall()
                print (result_ani[0][0])
                visitCount = result_ani[0][0]
                if visitCount > 0:
                    messagebox.showwarning("Dulicate Log", "Visitor cannot log to the same event on the same date.")
                else:
                    #sql = "INSERT INTO VisitEvent (VisitEventDate, sitename, startdate,visitorusername, VisitEventName) \
                    #VALUES ( '"+Date+"', '"+self.Event_Detail_Page_SiteName+"', '"+self.startDate+"', '"+self.Username+"', '"+self.Event_Detail_Page_EventName+"' );"
                    #print("Log Visit Event:",sql)
                    #self.cursor.execute(sql)
                    self.logVisitEvent(self.visitDatetime.get())

    def logVisitEvent(self,Date):
        sql = "SELECT Username from UserEmail WHERE Email ='"+self.loginEmailAddress+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        self.Username = str(temp[0][0])

        self.searchEmployeeInformation() ############################# do it in login window
        print(self.Username, self.startDate,self.Event_Detail_Page_EventName, self.Event_Detail_Page_SiteName, Date)
        sql = "INSERT INTO VisitEvent (VisitEventDate, sitename, startdate,visitorusername, VisitEventName) \
            VALUES ( '"+Date+"', '"+self.Event_Detail_Page_SiteName+"', '"+self.startDate+"', '"+self.Username+"', '"+self.Event_Detail_Page_EventName+"' );"
        print("Log Visit Event:",sql)
        self.cursor.execute(sql)
        self.db.commit()
        messagebox.showinfo("Success", "You have successfully log your visit to the event.")

    def eventDetail_back_Button_Clicked(self):
        print ("eventDetail_back_Button_Clicked")
        self.EventDetailWindow.withdraw()
        self.exploreEventWindow.deiconify()

    def exploreSite_filter_Visitor(self, siteName, openEveryday, startDate, endDate,minTotalVisit, maxTotalVisit, minEventCount, maxEventCount,includeVisited):
        SQL="select * from site"
        self.cursor.execute(SQL)
        result_ani = self.cursor.fetchall()
        self.tv.delete(*self.tv.get_children())
        print(result_ani)
        print(len(result_ani))
        siteNameList=[]
        siteAddressList=[]
        zipCodeList=[]
        openEverydayList=[]
        eventCountList=[]
        totalVisitList_Site=[]
        myVisitList=[]
        ifShow=[]
        for i in result_ani:
            siteNameList.append(str(i[0]))
            siteAddressList.append(str(i[2]))
            zipCodeList.append(i[3])
            openEverydayList.append(str(i[4]))
            ifShow.append(1)
        for i in range(len(siteNameList)):
            # index.append(i)
            # ifShow.append(1)
            SQL="select count(*) from event where sitename='"+siteNameList[i]+"'"
            self.cursor.execute(SQL)
            result_ani = self.cursor.fetchall()
            eventCountList.append(result_ani[0][0])

            SQL1="select count(*) from visitsite where sitename='"+siteNameList[i]+"'"
            self.cursor.execute(SQL1)
            result_1 = self.cursor.fetchall()
            print(result_1)
            totalVisitList_Site.append(result_1[0][0])

            # txq
            # 加上以下四行
            sql2 = "SELECT Username from UserEmail WHERE Email ='"+self.loginEmailAddress+"';"
            self.cursor.execute(sql2)
            temp = self.cursor.fetchall()
            self.Username = str(temp[0][0])

            SQL2=SQL1+ " and visitorusername= '"+ self.Username+"'"
            self.cursor.execute(SQL2)
            result = self.cursor.fetchall()
            print(result)
            myVisitList.append(result[0][0])

        if siteName != "--ALL--":
            for i in range(len(siteNameList)):
                if ifShow[i] == 1:
                    if siteName != siteNameList[i]: ifShow[i] = 0
        if openEveryday != "--ALL--":
            for i in range(len(siteNameList)):
                if ifShow[i] == 1:
                    if openEveryday != openEverydayList[i]: ifShow[i] = 0
        # start date, end date???

        if minTotalVisit:
            minTotalVisit_int = int(minTotalVisit)
            for i in range(len(siteNameList)):
                if ifShow[i] == 1:
                    if minTotalVisit_int > totalVisitList_Site[i]: ifShow[i] = 0
        if maxTotalVisit:
            maxTotalVisit_int = int(maxTotalVisit)
            for i in range(len(siteNameList)):
                if ifShow[i] == 1:
                    if maxTotalVisit_int < totalVisitList_Site[i]: ifShow[i] = 0
        if minEventCount:
            minEventCount_int = int(minEventCount)
            for i in range(len(siteNameList)):
                if ifShow[i] == 1:
                    if minEventCount_int > eventCountList[i]: ifShow[i] = 0
        if maxEventCount:
            maxEventCount_int = int(maxEventCount)
            for i in range(len(siteNameList)):
                if ifShow[i] == 1:
                    if maxEventCount_int < eventCountList[i]: ifShow[i] = 0
        print ("includeVisited")
        print (includeVisited)
        print ("includeVisited")

        if includeVisited == 0: # not include event that i didnot visited => only include myVisit >0
            for i in range(len(siteNameList)):
                if ifShow[i] == 1:
                    print(myVisitList[i])
                    if myVisitList[i] >0: ifShow[i] = 0

        #put into tree view
        j=0
        self.tv.delete(*self.tv.get_children())
        for i in range(len(siteNameList)):
            print (ifShow[i])
            if ifShow[i]==1:
                self.tv.insert("",j, value=(str(siteNameList[i]),str(eventCountList[i]),str(totalVisitList_Site[i]),str(myVisitList[i])))
                j+=1

#=========35 Explore Site Window============
    def createExploreSiteWindow(self):
        self.exploreSiteWindow = Toplevel()
        self.exploreSiteWindow.title("Explore Site")

    def buildExploreSiteWindow(self,exploreSiteWindow):
        # Title
        viewSiteLabel = Label(exploreSiteWindow, text="Explore Site", font="Verdana 13 bold ")
        viewSiteLabel.grid(row=1, column=1,columnspan=4, sticky=W + E,pady=5)
        # Site Name
        siteNameLabel = Label(exploreSiteWindow, text = "Name", font = "Verdana 10 bold")
        siteNameLabel.grid(row=2, column=1,pady=5)
        # Site Name Drop Down Button
        sql = "SELECT SiteName FROM Site;"
        self.cursor.execute(sql)
        SiteTuple = self.cursor.fetchall()
        SiteList = []
        for i in SiteTuple:
            SiteList.append(i[0])
        Site = StringVar()
        Site.set("--ALL--")
        siteNameOptionMenu = OptionMenu(exploreSiteWindow, Site, *SiteList)
        siteNameOptionMenu.config(width=10)
        siteNameOptionMenu.grid(row=2, column=2,pady=5)

        # open everyday
        openEverydayLabel = Label(exploreSiteWindow, text = "Open Everyday", font = "Verdana 10 bold")
        openEverydayLabel.grid(row=2, column=3,pady=5)
        # open everyday drop down menu
        openEveryday = StringVar()
        openEveryday.set("--ALL--")
        lst = ["Yes", "No"]
        optionbutton = OptionMenu(exploreSiteWindow, openEveryday, *lst)
        optionbutton.grid(row=2, column=4,pady=5)

        # Start Date
        startDateLabel = Label(exploreSiteWindow, text="Start Date", font="Verdana 10 bold ")
        startDateLabel.grid(row=3, column=1,pady=5)
        startDatetime = StringVar(value='YYYY-MM-DD')
        startDateLabel = Entry(exploreSiteWindow, textvariable=startDatetime, width=10)
        startDateLabel.grid(row=3, column=2,pady=5)

        # End Date
        endDateLabel = Label(exploreSiteWindow, text="End Date", font="Verdana 10 bold ")
        endDateLabel.grid(row=3, column=3,pady=5)
        endDatetime = StringVar(value='YYYY-MM-DD')
        endDateLabel = Entry(exploreSiteWindow, textvariable=endDatetime, width=10)
        endDateLabel.grid(row=3, column=4,pady=5)

        #Total visit range
        totalVisitRangeLabel = Label(exploreSiteWindow, text = "Total Visit Range", font = "Verdana 10 bold")
        totalVisitRangeLabel.grid(row=4, column = 1,pady=5)
        mintotalVisitRangeEntry = StringVar()
        totalVisitRange = Entry(exploreSiteWindow, textvariable=mintotalVisitRangeEntry, width=5)
        totalVisitRange.grid(row=4, column=2,pady=5)
        totalVisitRangeLabel2 = Label(exploreSiteWindow, text = "--", font = "Verdana 10 bold")
        totalVisitRangeLabel2.grid(row=4, column = 3,pady=5)
        maxtotalVisitRangeEntry = StringVar()
        totalVisitRange2 = Entry(exploreSiteWindow, textvariable=maxtotalVisitRangeEntry, width=5)
        totalVisitRange2.grid(row=4, column=4,pady=5)

        #Event Count Range
        eventCountRangeLabel = Label(exploreSiteWindow, text = "Event Count Range", font = "Verdana 10 bold")
        eventCountRangeLabel.grid(row=5, column = 1,pady=5)
        mineventCountRangeEntry = StringVar()
        eventCountRange = Entry(exploreSiteWindow, textvariable=mineventCountRangeEntry, width=5)
        eventCountRange.grid(row=5, column=2,pady=5)
        eventCountRangeLabel2 = Label(exploreSiteWindow, text = "--", font = "Verdana 10 bold")
        eventCountRangeLabel2.grid(row=5, column = 3,pady=5)
        maxeventCountRangeEntry = StringVar()
        eventCountRange2 = Entry(exploreSiteWindow, textvariable=maxeventCountRangeEntry, width=5)
        eventCountRange2.grid(row=5, column=4,pady=5)

        #Include Visited Checkbox
        includeVisited = IntVar(value=1)
        Checkbutton(exploreSiteWindow, text="Include Visited", variable=includeVisited).grid(row=6, column=2)

        def exploreSite_filter_Button_Clicked():
            print ("exploreSite_filter_Button_Clicked")
            self.exploreSite_filter_Visitor(Site.get(), openEveryday.get(), startDatetime.get(),
                    endDatetime.get(), mintotalVisitRangeEntry.get(), maxtotalVisitRangeEntry.get(), mineventCountRangeEntry.get(),
                    maxeventCountRangeEntry.get(), includeVisited.get())

        #filter Button
        filterButton = Button(exploreSiteWindow, text="Filter", command=exploreSite_filter_Button_Clicked, width=12)
        filterButton.grid(row=7, column=1,pady=5)

        #Site Detail Button
        siteDetailButton = Button(exploreSiteWindow, text="Site Detail", command=self.site_Detail_Button_Clicked, width=12)
        siteDetailButton.grid(row=7, column=3,pady=5)

        #transit Detail Button
        transitDetailButton = Button(exploreSiteWindow, text="Transit Detail", command=self.transit_Detail_Button_Clicked, width=12)
        transitDetailButton.grid(row=7, column=4,pady=5)

        # search table
        self.tv = ttk.Treeview(exploreSiteWindow)
        self.tv['columns'] = ("Site Name", "Event Count", "Total Visits", "My Visits")
        self.tv.heading("Site Name", text="Site Name▼", anchor='w')
        self.tv.column("Site Name",  width=250)
        self.tv.heading("Event Count", text="Event Count▼")
        self.tv.column("Event Count", width=80)
        self.tv.heading("Total Visits", text="Total Visits▼")
        self.tv.column("Total Visits", width=80)
        self.tv.heading("My Visits", text="My Visits▼")
        self.tv.column("My Visits", width=80)
        self.tv['show'] = 'headings'
        self.tv.grid(row=8, column=1, columnspan = 4,pady=5)
        self.tv.bind("<Double-1>",self.exploreSite_onClick) #左键双击

        #txq
        #加这一句 调用seed函数
        self.seed_explore_site(Site.get(), openEveryday.get(), startDatetime.get(),
                endDatetime.get(), mintotalVisitRangeEntry.get(), maxtotalVisitRangeEntry.get(), mineventCountRangeEntry.get(),
                maxeventCountRangeEntry.get(), includeVisited.get())
        #Back Button
        backButton = Button(exploreSiteWindow, text="Back", command=self.exploreSite_back_Button_Clicked, width=12)
        backButton.grid(row=9, column=2, columnspan = 2,sticky=W + E,pady=5)

    def site_Detail_Button_Clicked(self):
        print ("site_Detail_Button_Clicked")
        curItem = self.tv.item(self.tv.focus())
        print (curItem)
        # txq
        # 以下几行到这个函数结尾，改成这样， if else形式
        if not curItem['values']:
            messagebox.showwarning("Warning","Please select a row before click for detail.")
        else:
            siteName = curItem['values'][0]
            eventCount = curItem['values'][1]
            totalVisits = curItem['values'][2]
            myVisits = curItem['values'][3]
            self.createSiteDetailWindow()
            self.buildSiteDetailWindow(self.SiteDetailWindow, siteName, eventCount,totalVisits, myVisits)

    def transit_Detail_Button_Clicked(self):
        print ("transit_Detail_Button_Clicked")
        curItem = self.tv.item(self.tv.focus())
        print (curItem)
        siteName = curItem['values'][0]
        eventCount = curItem['values'][1]
        totalVisits = curItem['values'][2]
        myVisits = curItem['values'][3]
        self.createTransitDetailWindow()
        self.buildTransitDetailWindow(self.TransitDetailWindow, siteName, eventCount,totalVisits, myVisits)

    def exploreSite_back_Button_Clicked(self):
        print ("exploreSite_back_Button_Clicked")
        self.exploreSiteWindow.destroy()
        self.previous.deiconify()

    def exploreSite_onClick(self,event):
        print ("exploreSite_onClick")
        region = self.tv.identify_region(event.x, event.y)
        print (region)
        if region=="heading":
            print ("region=heading 未完待续")
        elif region=="cell":
            curItem = self.tv.item(self.tv.focus())
            print (curItem)
            siteName = curItem['values'][0]
            eventCount = curItem['values'][1]
            totalVisits = curItem['values'][2]
            myVisits = curItem['values'][3]
            self.createSiteDetailWindow()
            self.buildSiteDetailWindow(self.TransitDetailWindow, siteName, eventCount, totalVisits, myVisits)

    # txq
    # 加这一段seed site table的函数
    def seed_explore_site(self, siteName, openEveryday, startDate, endDate,minTotalVisit, maxTotalVisit, minEventCount, maxEventCount,includeVisited):
        SQL="select * from site"
        self.cursor.execute(SQL)
        result_ani = self.cursor.fetchall()
        self.tv.delete(*self.tv.get_children())
        print(result_ani)
        print(len(result_ani))
        siteNameList=[]
        siteAddressList=[]
        zipCodeList=[]
        openEverydayList=[]
        eventCountList=[]
        totalVisitList_Site=[]
        myVisitList=[]
        ifShow=[]
        for i in result_ani:
            siteNameList.append(str(i[0]))
            siteAddressList.append(str(i[2]))
            zipCodeList.append(i[3])
            openEverydayList.append(str(i[4]))
            ifShow.append(1)
        for i in range(len(siteNameList)):
            # index.append(i)
            # ifShow.append(1)
            SQL="select count(*) from event where sitename='"+siteNameList[i]+"'"
            self.cursor.execute(SQL)
            result_ani = self.cursor.fetchall()
            eventCountList.append(result_ani[0][0])

            SQL1="select count(*) from visitsite where sitename='"+siteNameList[i]+"'"
            self.cursor.execute(SQL1)
            result_1 = self.cursor.fetchall()
            print(result_1)
            totalVisitList_Site.append(result_1[0][0])

            # txq
            # 加上以下四行
            sql2 = "SELECT Username from UserEmail WHERE Email ='"+self.loginEmailAddress+"';"
            self.cursor.execute(sql2)
            temp = self.cursor.fetchall()
            self.Username = str(temp[0][0])
            # txq
            # 把hardcode的改成self.username
            SQL2=SQL1+ " and visitorusername= '"+ self.Username+"'"

            self.cursor.execute(SQL2)
            result = self.cursor.fetchall()
            print(result)
            myVisitList.append(result[0][0])
        #put into tree view
        j=0
        self.tv.delete(*self.tv.get_children())
        for i in range(len(siteNameList)):
            print (ifShow[i])
            if ifShow[i]==1:
                self.tv.insert("",j, value=(str(siteNameList[i]),str(eventCountList[i]),str(totalVisitList_Site[i]),str(myVisitList[i])))
                j+=1

#=========36 Transit Detail Window============
    def createTransitDetailWindow(self):
        self.TransitDetailWindow = Toplevel()
        self.TransitDetailWindow.title("Transit Detail")
        # self.exploreSiteWindow.withdraw()

    def buildTransitDetailWindow(self, TransitDetailWindow, siteName, eventCount,totalVisits,myVisits):
        # title label
        transitDetailWindow = Label(TransitDetailWindow, text = "Transit Detail", font = ("Verdana", 15))
        transitDetailWindow.grid(row=1, column=2, sticky=E, pady=3)

        siteName = str(siteName)
        self.Site_Detail_Page_EventName = siteName #log visit的时候用
        eventCount = str(eventCount)
        totalVisits = str(totalVisits)
        myVisits = str(myVisits)

        SQL="select * from connect where sitename='"+siteName+"'"
        self.cursor.execute(SQL)
        result_check = self.cursor.fetchall()
        routeList=[]
        transitTypeList=[]
        priceList=[]
        numberConnectedSiteList=[]
        for i in range(len(result_check)):
            routeList.append(result_check[i][1])
            transitTypeList.append(result_check[i][0])
        for i in range(len(result_check)):
            SQL="select * from transit where transitType='"+ transitTypeList[i]+"' and transitroute='"+routeList[i]+"'"
            self.cursor.execute(SQL)
            result_check = self.cursor.fetchall()
            priceList.append(result_check[0][2])
            # print(result_check[0][2])
            SQL1="select COUNT(*) from connect where transitType='"+ transitTypeList[i]+"' and transitroute='"+routeList[i]+"'"
            self.cursor.execute(SQL1)
            result_1 = self.cursor.fetchall()
            print(result_1[0][0])
            numberConnectedSiteList.append(result_1[0][0])

        # Site Name Label
        sitelabel = Label(TransitDetailWindow, text="Site", font="Verdana 10 bold")
        sitelabel.grid(row=2, column=1)
        sitelabeltext = Label(TransitDetailWindow, text=siteName, font="Helvetica 10 italic bold underline")
        sitelabeltext.grid(row=2, column=2)
        # Transport Type label
        sitelabel = Label(TransitDetailWindow, text="Transport Type" , font="Verdana 10 bold")
        sitelabel.grid(row=2, column=3)
        # Transport Type drop down
        sql = "SELECT transittype FROM transit;"
        self.cursor.execute(sql)
        transitType = self.cursor.fetchall()
        transitTypeList = []
        for i in transitType:
            transitTypeList.append(i[0])
        Type = StringVar()
        Type.set("--ALL--")
        optionMenu = OptionMenu(TransitDetailWindow, Type, *transitTypeList)
        optionMenu.config(width=10)
        optionMenu.grid(row=2, column=4,pady=5)

        # search table
        self.tv = ttk.Treeview(TransitDetailWindow)
        self.tv['columns'] = ("Route", "Transit Type", "Price", "# Connected Sites")
        self.tv.heading("Route", text='Route▼', anchor='w')
        self.tv.column("Route", width=100)
        self.tv.heading("Transit Type", text="Transit Type▼", anchor='w')
        self.tv.column("Transit Type",  width=100)
        self.tv.heading("Price", text="Price▼")
        self.tv.column("Price", width=100)
        self.tv.heading("# Connected Sites", text="# Connected Sites▼")
        self.tv.column("# Connected Sites",  width=120)
        self.tv['show'] = 'headings'
        self.tv.grid(row=3, column=1, columnspan=4,pady=5,padx=5)
        # self.tv.bind("<Double-1>",self.exploreEvent_onClick) #左键双击

        j=0
        self.tv.delete(*self.tv.get_children())
        for i in range(len(numberConnectedSiteList)):
            self.tv.insert("",j, value=(str(routeList[i]),str(transitTypeList[i]),str(priceList[i]),str(numberConnectedSiteList[i])))
            j+=1

        # back Button
        backButton = Button(TransitDetailWindow, text="Back", command=self.transitDetail_back_Button_Clicked, width =15)
        backButton.grid(row=4, column=1)

        # Transit Date
        transitDateLabel = Label(TransitDetailWindow, text="Transit Date", font="Verdana 10 bold ")
        transitDateLabel.grid(row=4, column=2, sticky=E)
        self.transitDatetime = StringVar(value='YYYY-MM-DD')
        transitDatetime = Entry(TransitDetailWindow, textvariable=self.transitDatetime, width=10)
        transitDatetime.grid(row=4, column=3, sticky=W, pady=5, padx=5)

        # log visit Button
        logVisitButton = Button(TransitDetailWindow, text="Log Transit", command=self.logTransit_toSite_Clicked,width =15)
        logVisitButton.grid(row=4, column=4)

    def logTransit_toSite_Clicked(self):
        print ("logTransit_toSite_Clicked")
        curItem = self.tv.item(self.tv.focus())
        print(curItem)
        if not curItem['values']:
            messagebox.showwarning("Transit is empty", "Please select a row of transit before log.")
        elif not self.transitDatetime.get() or self.transitDatetime.get() == "YYYY-MM-DD":
            messagebox.showwarning("Transit Date input is empty", "Please enter a date before log.")
        else:
            #txq
            #这段之后到本函数结束 改成这样
            self.LogType = curItem['values'][1]
            self.LogRoute = curItem['values'][0]
            sql = "SELECT Username from UserEmail WHERE Email ='"+self.loginEmailAddress+"';"
            self.cursor.execute(sql)
            temp = self.cursor.fetchall()
            self.Username = str(temp[0][0])
            SQL = "select count(*) from takeTransit where transitDate='"+self.transitDatetime.get()+"' and transitType='"+self.LogType+"' and transitroute='"+ self.LogRoute+"' and username='"+self.Username+"'"
            self.cursor.execute(SQL)
            result = self.cursor.fetchall()
            print(result[0])
            print(result[0][0])
            print(type(result[0][0]))

            if result[0][0] > 0:
                messagebox.showwarning("Duplicate Error", "Duplicate entry. Primary key constrain conficts.")
            else:
                # txq
                # 加上str()
                self.logTransit(str(self.transitDatetime.get()))

    def logTransit(self, Date):
        sql = "SELECT Username from UserEmail WHERE Email ='"+self.loginEmailAddress+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        self.Username = str(temp[0][0])
        print(self.Username, self.LogType, self.LogRoute, Date)
        sql = "INSERT INTO TakeTransit (Username, TransitType,TransitRoute,TransitDate) VALUES ( '"+self.Username+"', '"+self.LogType+"', '"+self.LogRoute+"', '"+Date+"' );"
        print("Log Transit:",sql)
        self.cursor.execute(sql)
        self.db.commit()

    def transitDetail_back_Button_Clicked(self):
        print ("transitDetail_back_Button_Clicked")
        self.TransitDetailWindow.destroy()
        self.exploreSiteWindow.deiconify()

#=========37 Site Detail Window============
    def createSiteDetailWindow(self):
        self.SiteDetailWindow = Toplevel()
        self.SiteDetailWindow.title("Site Detail")
        # self.exploreSiteWindow.withdraw()
    def buildSiteDetailWindow(self, SiteDetailWindow, siteName, eventCount,totalVisits,myVisits):
        # title label
        siteDetailWindow = Label(SiteDetailWindow, text = "Site Detail", font = ("Verdana", 20))
        siteDetailWindow.grid(row=1, column=3, sticky=W, pady=3)

        siteName = str(siteName)
        self.Site_Detail_Page_SiteName = siteName #log visit的时候用
        eventCount = str(eventCount)
        totalVisits = str(totalVisits)
        myVisits = str(myVisits)

        SQL = "select * from site where sitename='"+siteName+"'"
        self.cursor.execute(SQL)
        result_check = self.cursor.fetchall()

        openEveryday = str(result_check[0][4])
        address = str(result_check[0][2])
        zipcode = str(result_check[0][3])
        if address:
            address=address+", GA, "+zipcode
        else:
            address=address+"GA, "+zipcode

        # Site Name Label
        sitelabel = Label(SiteDetailWindow, text="Site", font="Verdana 10 bold")
        sitelabel.grid(row=2, column=1, sticky=W)
        sitelabeltext = Label(SiteDetailWindow, text=siteName, font="Helvetica 10 italic bold underline")
        sitelabeltext.grid(row=2, column=2, sticky=W)
        # Open everyday label
        openEverydaylabel = Label(SiteDetailWindow, text="Open Everyday" , font="Verdana 10 bold")
        openEverydaylabel.grid(row=2, column=3, sticky=W)
        openEverydaylabeltext = Label(SiteDetailWindow, text=openEveryday, font="Helvetica 10 italic bold underline")
        openEverydaylabeltext.grid(row=2, column=4, sticky=W)
        # Address label
        addresslabel = Label(SiteDetailWindow, text="Address" , font="Verdana 10 bold")
        addresslabel.grid(row=3, column=1, sticky=W)
        addresslabeltext = Label(SiteDetailWindow, text=address, font="Helvetica 10 italic bold underline", wraplength =300, anchor=W, justify=LEFT)
        addresslabeltext.grid(row=3, column=2, sticky=W)
        # Visit Date
        visitDateLabel = Label(SiteDetailWindow, text="Visit Date", font="Verdana 10 bold ")
        visitDateLabel.grid(row=4, column=2, sticky=W)
        self.visitDatetime = StringVar(value='YYYY-MM-DD')
        visitDateLabel = Entry(SiteDetailWindow, textvariable=self.visitDatetime, width=10)
        visitDateLabel.grid(row=4, column=3, sticky=W, pady=5, padx=5)
        # log visit Button
        logVisitButton = Button(SiteDetailWindow, text="Log Visit", command=self.logVisit_toSite_Clicked,width =15)
        logVisitButton.grid(row=4, column=4)
        # back Button
        logVisitButton = Button(SiteDetailWindow, text="Back", command=self.siteDetail_back_Button_Clicked, width =15)
        logVisitButton.grid(row=5, column=2, columnspan=2)

    def logVisit_toSite_Clicked(self):
        print ("logVisit_toSite_Clicked")
        print(self.visitDatetime.get())
        if not self.visitDatetime.get() or self.visitDatetime.get() == "YYYY-MM-DD":
            messagebox.showwarning("Visit Date input is empty", "Please enter a visit date before log.")
        else:
            self.logVisitSite(self.visitDatetime.get())

    def logVisitSite(self, Date):
        sql = "SELECT Username from UserEmail WHERE Email ='"+self.loginEmailAddress+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        self.Username = str(temp[0][0])

        SQL="select count(*) from visitsite where sitename='"+self.Site_Detail_Page_SiteName+"' and visitorusername='"+self.Username+"' and visitsitedate='"+Date+"'"
        self.cursor.execute(SQL)
        result_ani = self.cursor.fetchall()
        print (result_ani[0][0])
        visitCount = result_ani[0][0]
        if visitCount <= 0:
            sql = "INSERT INTO visitsite (visitsitedate, sitename, visitorusername) VALUES ( '"+Date+"', '"+self.Site_Detail_Page_SiteName+"', '"+self.Username+"' );"
            print("Log Visite Site:",sql)
            self.cursor.execute(sql)
            self.db.commit()
            messagebox.showinfo("Success", "You have successfully log your visit to the site.")
        else:
            messagebox.showwarning("Dulicate Log", "Visitor cannot log to the same site on the same date.")

    def siteDetail_back_Button_Clicked(self):
        print ("siteDetail_back_Button_Clicked")
        self.SiteDetailWindow.destroy()
        self.exploreSiteWindow.deiconify()

#=========38 Visitor Visit History Window============
    def createViewVisitHistoryWindow(self):
        self.viewVisitHistoryWindow = Toplevel()
        self.viewVisitHistoryWindow.title("Explore Site")

    def buildViewVisitHistoryWindow(self,viewVisitHistoryWindow):
        # Title
        viewSiteLabel = Label(viewVisitHistoryWindow, text="Visit History", font="Verdana 13 bold ")
        viewSiteLabel.grid(row=1, column=4, sticky=W + E)

        #Event
        eventLabel = Label(viewVisitHistoryWindow, text = "Event", font = "Verdana 10 bold")
        eventLabel.grid(row=2, column = 1, sticky=W)
        self.eventEntry = StringVar()
        event = Entry(viewVisitHistoryWindow, textvariable=self.eventEntry, width=10)
        event.grid(row=2, column=2, sticky=W + E)

        # Site Name
        siteNameLabel = Label(viewVisitHistoryWindow, text = "Site", font = "Verdana 10 bold")
        siteNameLabel.grid(row=2, column = 5, sticky=W)
        # Site Name Drop Down Button
        sql = "SELECT SiteName FROM Site;"
        self.cursor.execute(sql)
        SiteTuple = self.cursor.fetchall()
        SiteList = []
        for i in SiteTuple:
            SiteList.append(i[0])
        Site = StringVar()
        Site.set("--ALL--")
        siteNameOptionMenu = OptionMenu(viewVisitHistoryWindow, Site, *SiteList)
        siteNameOptionMenu.config(width= 10)
        siteNameOptionMenu.grid(row=2, column=6)

        # Start Date
        startDateLabel = Label(viewVisitHistoryWindow, text="Start Date", font="Verdana 10 bold ")
        startDateLabel.grid(row=3, column=1,sticky=W)
        startDatetime = StringVar(value='YYYY-MM-DD')
        startDateLabel = Entry(viewVisitHistoryWindow, textvariable=startDatetime, width=10)
        startDateLabel.grid(row=3, column=2,sticky=W,pady=5,padx=5)

        # End Date
        endDateLabel = Label(viewVisitHistoryWindow, text="End Date", font="Verdana 10 bold ")
        endDateLabel.grid(row=3, column=5,sticky=W)
        endDatetime = StringVar(value='YYYY-MM-DD')
        endDateLabel = Entry(viewVisitHistoryWindow, textvariable=endDatetime, width=10)
        endDateLabel.grid(row=3, column=6,sticky=W,pady=5,padx=5)

        #filter Button
        filterButton = Button(viewVisitHistoryWindow, text="Filter", command=self.viewVisitHistory_filter_Button_Clicked)
        filterButton.grid(row=4, column=4)

        # search table
        self.tv_visitor_visit_history = ttk.Treeview(viewVisitHistoryWindow)
        self.tv_visitor_visit_history['columns'] = ("Date", "Event", "Site", "Price")
        self.tv_visitor_visit_history.heading("Date", text="Date▼", anchor='w')
        self.tv_visitor_visit_history.column("Date",  minwidth=1)
        self.tv_visitor_visit_history.heading("Event", text="Event▼")
        self.tv_visitor_visit_history.column("Event", minwidth=1)
        self.tv_visitor_visit_history.heading("Site", text="Site▼")
        self.tv_visitor_visit_history.column("Site", minwidth=1)
        self.tv_visitor_visit_history.heading("Price", text="Price▼")
        self.tv_visitor_visit_history.column("Price", minwidth=1)
        self.tv_visitor_visit_history['show'] = 'headings'
        self.tv_visitor_visit_history.grid(row=5, column=1, columnspan = 8)
        self.tv_visitor_visit_history.bind("<Double-1>",self.viewVisitHistory_onClick) #左键双击

        #Back Button
        backButton = Button(viewVisitHistoryWindow, text="Back", command=self.viewVisitHistory_back_Button_Clicked)
        backButton.grid(row=6, column=4)

    def viewVisitHistory_filter_Button_Clicked(self):
        sql = "SELECT Username from UserEmail WHERE Email ='"+self.loginEmailAddress+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        self.Username = str(temp[0][0])
        print ("viewVisitHistory_filter_Button_Clicked")
        sql = "SELECT vs.VisitSiteDate, ve.VisitEventName, vs.SiteName, ve.StartDate\
            from VisitSite vs\
            left join VisitEvent ve\
            on vs.VisitorUsername = ve.VisitorUsername and vs.SiteName=ve.SiteName \
            and vs.VisitSiteDate=ve.VisitEventDate where vs.VisitorUsername = '"+self.Username+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        date = []
        event = []
        site = []
        startdate = []
        for element in temp:
            date.append(element[0])
            site.append(element[2])
            if element[1]:
                event.append(element[2])
                startdate.append(str(element[3]))
            else:
                event.append("")
                startdate.append("")
        price = []
        for i in range(len(date)):
            if len(event[i])>0 and len(startdata[0])>0:
                sql = "select EventName,StartDate,EventPrice from Event where EventName = '"+ event[i]\
                    + "' and StartDate = '"+ startdate[i] + "' and SiteName = '"+ site[i]+"';"
                self.cursor.execute(sql)
                temp = self.cursor.fetchall()
                price.append(temp[0][0])
            else:
                price.append(0)

        self.tv_visitor_visit_history.delete(*self.daily_detail.get_children())
        j=0;
        for i in range(len(date)):
            self.tv_visitor_visit_history.insert("",i, value=(date[i],str(event[i])\
                                            ,str(site[i]),str(price[i])))
        self.db.commit()

    def viewVisitHistory_back_Button_Clicked(self):
        print ("viewVisitHistory_back_Button_Clicked")
        self.viewVisitHistoryWindow.destroy()
        self.previous.deiconify()

    def viewVisitHistory_onClick(self,event):
        print ("viewVisitHistory_onClick")
        region = self.tv_visitor_visit_history.identify_region(event.x, event.y)
        print (region)


#=================create database & connect database=======================#
    def connect(self):
        try:
            ##change 'root' and 'password' to your own username and password
            db = pymysql.connect(host='localhost',
                       user='root',
                       password='Password',db='AtlantaBeltline')
            return db
        except:
            messagebox.showwarning('Error!','Cannot connect to database')
            return False

    def searchEmployeeInformation(self):
        sql = "SELECT Username from UserEmail WHERE Email ='"+self.loginEmailAddress+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        self.Username = str(temp[0][0])

        sql = "SELECT Firstname, Lastname from User where Username ='"+self.Username+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        self.Firstname = str(temp[0][0])
        self.Lastname = str(temp[0][1])

        sql = "SELECT * from Employee where Username ='"+self.Username+"';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()
        self.EmployeeID = str(temp[0][1])
        self.Phone = str(temp[0][2])
        self.EmployeeAddress = str(temp[0][3])
        self.EmployeeCity = str(temp[0][4])
        self.EmployeeState= str(temp[0][5])
        self.EmployeeZipcode= str(temp[0][6])

a = AtlantaBeltline()
a.db.close()
