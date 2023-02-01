import customtkinter as ctk
from note import Note,Book
import os,json
  
class NoteApp:
    def __init__(self,width,height):
        # SETUP
        self.unit = width/10-1
        self.yunit = height/10-1
        self.root = ctk.CTk()
        self.root.geometry(f"{width+10}x{height}")
        self.root.resizable(False,False)
        self.root.title("DamPad V1.0")
        self.root.protocol("WM_DELETE_WINDOW",self.savequit)
        self.buttonstartrel = 15
        self.buttonincreaserel = 35
        self.secondWindowOpen = False
        self.secondWindow:ctk.CTkToplevel = None
        self.noteEditTextBox:ctk.CTkTextbox = None
        self.bookEditTextBox:ctk.CTkTextbox = None
        self.bookPageDisplayer:ctk.CTkLabel = None
        self.runtimePages = []
        self.currentPage = 0
        
        # DATA
        self.notes_data:list[Note] = list()
        self.books_data:list[Book] = list()
        self.notes_buttons:list[ctk.CTkButton] = list()
        self.notesstrvar:list[ctk.StringVar] = list()
        self.notes_checkboxes:list[ctk.CTkCheckBox] = list()
        self.books_buttons:list[ctk.CTkButton] = list()
        self.books_checkboxes:list[ctk.CTkCheckBox] = list()
        self.booksstrvar:list[ctk.StringVar] = list()
        
        # SETTING UP FRAMES
        # category
        self.categoryFrame = ctk.CTkFrame(self.root,self.unit*3,self.yunit*10)
        self.categoryFrame.grid(row = 0,column=0,padx=5,pady=5)
        # notes
        self.notesOuterFrame = ctk.CTkFrame(self.root,self.unit*7-5,self.yunit*10)
        self.notesCanvas = ctk.CTkCanvas(self.notesOuterFrame,width=self.unit*7-20,height=self.yunit*7-10,background="gray17",bd=0, highlightthickness=0, relief='ridge')#,self.unit*7-5,self.yunit*10)
        self.notesFrame = ctk.CTkFrame(self.notesCanvas,self.unit*7-10,self.yunit*1000)
        self.notesCanvas.create_window((0, 0), window=self.notesFrame, anchor="nw")
        self.notesCanvas.place(in_=self.notesOuterFrame,anchor=ctk.CENTER,relx=0.5,rely=0.675)
        # books
        self.booksOuterFrame = ctk.CTkFrame(self.root,self.unit*7-5,self.yunit*10)
        self.booksCanvas = ctk.CTkCanvas(self.booksOuterFrame,width=self.unit*7-20,height=self.yunit*7-10,background="gray17",bd=0, highlightthickness=0, relief='ridge')
        self.booksFrame = ctk.CTkFrame(self.booksCanvas,self.unit*7-10,self.yunit*1000)
        self.booksCanvas.create_window((0,0),window=self.booksFrame,anchor="nw")
        self.booksCanvas.place(in_=self.booksOuterFrame,anchor=ctk.CENTER,relx=0.5,rely=0.675)
        # finish
        self.category_frames = {
            "notes":self.notesOuterFrame,
            "books":self.booksOuterFrame
        }
        
        # SETTING CATEGORIES
        #self.notesCategoryBtn = ctk.CTkButton(self.categoryFrame,text="My Notes",command=lambda: self.select_category("notes"))
        self.notesCategoryBtn = ctk.CTkButton(self.categoryFrame,corner_radius=0, width=self.unit*3,height=40, text="Notes",
                                                      fg_color="#2FA572", text_color=("gray10", "gray90"),
                                                        command=lambda: self.select_category("notes"))
        #self.booksCategoryBtn = ctk.CTkButton(self.categoryFrame,text="My Books",command=lambda: self.select_category("books"))
        self.booksCategoryBtn = ctk.CTkButton(self.categoryFrame,corner_radius=0, width=self.unit*3,height=40, text="Books",
                                                      fg_color="#2FA572", text_color=("gray10", "gray90"),
                                                        command=lambda: self.select_category("books"))
        categoryTitle = ctk.CTkLabel(self.categoryFrame,text="DamPad",font=("Segoe UI",30))
        savequitBtn = ctk.CTkButton(self.categoryFrame,text="Save & Quit",command=self.savequit)
        saveBtn = ctk.CTkButton(self.categoryFrame,text="Save",command=self.save)
        self.notesCategoryBtn.place(in_=self.categoryFrame,anchor=ctk.CENTER,relx = 0.5,rely=0.2)
        self.booksCategoryBtn.place(in_=self.categoryFrame,anchor=ctk.CENTER,relx = 0.5, rely = 0.26)
        savequitBtn.place(in_=self.categoryFrame,anchor=ctk.CENTER,relx = 0.5, rely = 0.9)
        saveBtn.place(in_=self.categoryFrame,anchor=ctk.CENTER,relx = 0.5, rely = 0.84)
        categoryTitle.place(in_=self.categoryFrame,anchor=ctk.CENTER,relx = 0.5, rely = 0.08)
        
        # SETTING "MY NOTES"
        self.scrollbarNotes = ctk.CTkScrollbar(self.root,orientation="vertical",height=self.yunit*10+10)
        self.scrollbarNotes.grid(row=0,column=2)
        self.scrollbarNotes.configure(command=self.notesCanvas.yview)
        self.notesCanvas.configure(yscrollcommand=self.scrollbarNotes.set)
        notesTitle = ctk.CTkLabel(self.notesOuterFrame,text="My Notes",font=("Segoe UI",30))
        notesTitle.place(in_=self.notesOuterFrame,anchor=ctk.CENTER,relx = 0.5, y = 25)
        # add
        self.addNoteEntry = ctk.CTkEntry(self.notesOuterFrame)
        self.addNewNoteBtn = ctk.CTkButton(self.notesOuterFrame,text="Create New Note",command=self.new_note)
        self.addNewNoteBtn.place(in_=self.notesOuterFrame,anchor=ctk.CENTER,relx = 0.625,y=70)
        self.addNoteEntry.place(in_=self.notesOuterFrame,anchor=ctk.CENTER,relx = 0.375,y=70)
        # rename
        self.renameNoteEntry = ctk.CTkEntry(self.notesOuterFrame)
        self.renameNewNoteBtn = ctk.CTkButton(self.notesOuterFrame,text="Rename Selected Note",command=self.rename_note)
        self.renameNewNoteBtn.place(in_=self.notesOuterFrame,anchor=ctk.CENTER,relx = 0.625,y=105)
        self.renameNoteEntry.place(in_=self.notesOuterFrame,anchor=ctk.CENTER,relx = 0.375,y=105)
        # delete
        self.deleteNewNoteBtn = ctk.CTkButton(self.notesOuterFrame,295,text="Delete Selected Notes",command=self.delete_notes)
        self.deleteNewNoteBtn.place(in_=self.notesOuterFrame,anchor=ctk.CENTER,relx = 0.5,y=140)
        # other
        separator1 = ctk.CTkProgressBar(self.notesOuterFrame,self.unit*6,2,progress_color="gray17")
        separator1.place(in_=self.notesOuterFrame,anchor=ctk.CENTER,relx = 0.5,y=175)
        separator1.set(0)
        
        # SETTING "MY BOOKS"
        self.scrollbarBooks = ctk.CTkScrollbar(self.root,orientation="vertical",height=self.yunit*10+10)
        self.scrollbarBooks.grid(row=0,column=2)
        self.scrollbarBooks.configure(command=self.booksCanvas.yview)
        self.booksCanvas.configure(yscrollcommand=self.scrollbarBooks.set)
        booksTitle = ctk.CTkLabel(self.booksOuterFrame,text="My Books",font=("Segoe UI",30))
        booksTitle.place(in_=self.booksOuterFrame,anchor=ctk.CENTER,relx = 0.5, y = 25)
        # add
        self.addBookEntry = ctk.CTkEntry(self.booksOuterFrame)
        self.addNewBookBtn = ctk.CTkButton(self.booksOuterFrame,text="Create New Book",command=self.new_book)
        self.addNewBookBtn.place(in_=self.booksOuterFrame,anchor=ctk.CENTER,relx = 0.625,y=70)
        self.addBookEntry.place(in_=self.booksOuterFrame,anchor=ctk.CENTER,relx = 0.375,y=70)
        # rename
        self.renameBookEntry = ctk.CTkEntry(self.booksOuterFrame)
        self.renameNewBookBtn = ctk.CTkButton(self.booksOuterFrame,text="Rename Selected Book",command=self.rename_book)
        self.renameNewBookBtn.place(in_=self.booksOuterFrame,anchor=ctk.CENTER,relx = 0.625,y=105)
        self.renameBookEntry.place(in_=self.booksOuterFrame,anchor=ctk.CENTER,relx = 0.375,y=105)
        # delete
        self.deleteNewBookBtn = ctk.CTkButton(self.booksOuterFrame,295,text="Delete Selected Books",command=self.delete_books)
        self.deleteNewBookBtn.place(in_=self.booksOuterFrame,anchor=ctk.CENTER,relx = 0.5,y=140)
        # other
        separator2 = ctk.CTkProgressBar(self.booksOuterFrame,self.unit*6,2,progress_color="gray17")
        separator2.place(in_=self.booksOuterFrame,anchor=ctk.CENTER,relx = 0.5,y=175)
        separator2.set(0)
        
        self.select_category("notes")
        self.load()
        
    def new_note(self,content=""):
        txt = self.addNoteEntry.get()
        if txt.strip() == "":
            name = "New Note"
            startname = name
        else:
            if len(txt) > 15:
                txt = txt[:15]
            name = txt
            startname = name
        num = 0
        for n in self.notes_data:
            if n.name == name:
                num += 1
                name = f"{startname} ({num})"
        new = Note(name,content)
        self.notes_data.append(new)
        strvar = ctk.StringVar()
        strvar.set(new.name)
        self.notesstrvar.append(strvar)
        button = ctk.CTkButton(self.notesFrame,text=new.name,textvariable=strvar,command=lambda:self.open_note(strvar.get()))
        button.place(in_=self.notesFrame,anchor=ctk.CENTER,relx = 0.5, y = self.buttonstartrel+self.buttonincreaserel*len(self.notes_buttons))
        checkbox = ctk.CTkCheckBox(self.notesFrame,24,text="")
        checkbox.place(in_=self.notesFrame,anchor=ctk.CENTER,relx = 0.35, y = self.buttonstartrel+self.buttonincreaserel*len(self.notes_buttons))
        self.notes_buttons.append(button)
        self.notes_checkboxes.append(checkbox)
        self.notesCanvas.configure(scrollregion=(0,0,500,len(self.notes_buttons)*35+10))
            
    def rename_note(self):
        txt = self.renameNoteEntry.get()
        if txt.strip() == "":
            name = "New Note"
            startname = name
        else:
            if len(txt) > 15:
                txt = txt[:15]
            name = txt
            startname = name
        num = 0
        for n in self.notes_data:
            if n.name == name:
                num += 1
                name = f"{startname} ({num})"
        for i,c in enumerate(self.notes_checkboxes):
            if c.get() == 1:
                self.notes_data[i].rename(name)
                self.notesstrvar[i].set(name)
                break
            
    def delete_notes(self):
        index = -1
        for i,c in enumerate(self.notes_checkboxes):
            if c.get() == 1:
                index = i
                break
        if index != -1:
            self.notes_data.pop(index)
            self.notes_buttons.pop(index).destroy()
            self.notes_checkboxes.pop(index).destroy()
            self.notesstrvar.pop(index)
            for b in self.notes_buttons:
                b.grid_forget()
            for c in self.notes_checkboxes:
                c.grid_forget()
            for i in range(len(self.notes_data)):
                self.notes_buttons[i].place(in_=self.notesFrame,anchor=ctk.CENTER,relx = 0.5, y = self.buttonstartrel+self.buttonincreaserel*i)
                self.notes_checkboxes[i].place(in_=self.notesFrame,anchor=ctk.CENTER,relx = 0.35, y = self.buttonstartrel+self.buttonincreaserel*i)
            self.delete_notes()
        self.notesCanvas.configure(scrollregion=(0,0,500,len(self.notes_buttons)*35+10))
    
    def create_second_window_for_note(self,name):
        self.secondWindow = ctk.CTkToplevel()
        w = 500
        h = 500
        self.secondWindow.geometry(f"{w}x{h}")
        self.secondWindow.resizable(False,False)
        self.secondWindow.protocol("WM_DELETE_WINDOW",self.onsecondwindowclose)
        self.noteEditTextBox = ctk.CTkTextbox(self.secondWindow,w-10,w-30-15)
        self.noteEditTextBox.pack(pady=5)
        savebutton = ctk.CTkButton(self.secondWindow,w-10,text="Save",command=lambda:self.save_note(name))
        savebutton.pack()
        
    def onsecondwindowclose(self):
        self.secondWindow.destroy()
        self.secondWindow = None
    
    def open_note(self,name):
        for n in self.notes_data:
            if n.name == name:
                if self.secondWindow == None:
                    self.create_second_window_for_note(name)
                self.secondWindow.title(f"Note Editor: {name}")
                self.noteEditTextBox.delete("1.0",ctk.END)
                self.noteEditTextBox.insert("1.0",n.content)
                self.secondWindow.focus()
                return
            
    def save_note(self,name):
        for n in self.notes_data:
            if n.name == name:
                if self.secondWindowOpen != None:
                    n.content = self.noteEditTextBox.get("1.0",ctk.END)
                    
    def new_book(self):
        txt = self.addBookEntry.get()
        if txt.strip() == "":
            name = "New Book"
            startname = name
        else:
            if len(txt) > 15:
                txt = txt[:15]
            name = txt
            startname = name
        num = 0
        for n in self.books_data:
            if n.name == name:
                num += 1
                name = f"{startname} ({num})"
        new = Book(name)
        self.books_data.append(new)
        strvar = ctk.StringVar()
        strvar.set(new.name)
        self.booksstrvar.append(strvar)
        button = ctk.CTkButton(self.booksFrame,text=new.name,textvariable=strvar,command=lambda:self.open_book(strvar.get()))
        button.place(in_=self.booksFrame,anchor=ctk.CENTER,relx = 0.5, y = self.buttonstartrel+self.buttonincreaserel*len(self.books_buttons))
        checkbox = ctk.CTkCheckBox(self.booksFrame,24,text="")
        checkbox.place(in_=self.booksFrame,anchor=ctk.CENTER,relx = 0.35, y = self.buttonstartrel+self.buttonincreaserel*len(self.books_buttons))
        self.books_buttons.append(button)
        self.books_checkboxes.append(checkbox)
        self.booksCanvas.configure(scrollregion=(0,0,500,len(self.books_buttons)*35+10))
        return new
        
    def rename_book(self):
        txt = self.renameBookEntry.get()
        if txt.strip() == "":
            name = "New Book"
            startname = name
        else:
            if len(txt) > 15:
                txt = txt[:15]
            name = txt
            startname = name
        num = 0
        for n in self.books_data:
            if n.name == name:
                num += 1
                name = f"{startname} ({num})"
        for i,c in enumerate(self.books_checkboxes):
            if c.get() == 1:
                self.books_data[i].rename(name)
                self.booksstrvar[i].set(name)
                break
    
    def delete_books(self):
        index = -1
        for i,c in enumerate(self.books_checkboxes):
            if c.get() == 1:
                index = i
                break
        if index != -1:
            self.books_data.pop(index)
            self.books_buttons.pop(index).destroy()
            self.books_checkboxes.pop(index).destroy()
            self.booksstrvar.pop(index)
            for b in self.books_buttons:
                b.grid_forget()
            for c in self.books_checkboxes:
                c.grid_forget()
            for i in range(len(self.books_data)):
                self.books_buttons[i].place(in_=self.booksFrame,anchor=ctk.CENTER,relx = 0.5, y = self.buttonstartrel+self.buttonincreaserel*i)
                self.books_checkboxes[i].place(in_=self.booksFrame,anchor=ctk.CENTER,relx = 0.35, y = self.buttonstartrel+self.buttonincreaserel*i)
            self.delete_books()
        self.booksCanvas.configure(scrollregion=(0,0,500,len(self.books_buttons)*35+10))
    
    def create_second_window_for_book(self,name):
        self.secondWindow = ctk.CTkToplevel()
        w = 500
        h = 500
        self.secondWindow.geometry(f"{w}x{h}")
        self.secondWindow.resizable(False,False)
        self.secondWindow.protocol("WM_DELETE_WINDOW",self.onsecondwindowclose)
        
        self.bookEditTextBox = ctk.CTkTextbox(self.secondWindow,w-10,w-60-15)
        self.bookEditTextBox.place(relx=0.5,rely=0.01,anchor=ctk.N)
        savebutton = ctk.CTkButton(self.secondWindow,w-10,text="Save",command=lambda:self.save_book(name))
        savebutton.place(anchor=ctk.S,relx=0.5,rely=1-0.01)
        prevbutton = ctk.CTkButton(self.secondWindow,100,text="Previous Page",command=self.previous_page)
        prevbutton.place(anchor=ctk.SW,relx=0.01,rely=0.933-0.01)
        nextbutton = ctk.CTkButton(self.secondWindow,100,text="Next Page",command=self.next_page)
        nextbutton.place(anchor=ctk.SE,relx=1-0.01,rely=0.933-0.01)
        self.bookPageDisplayer = ctk.CTkLabel(self.secondWindow,text="Current Page: 1")
        self.bookPageDisplayer.place(anchor=ctk.S,relx=0.5,rely=0.933-0.01)
        
    def next_page(self):
        if self.currentPage < len(self.runtimePages)-1:
            self.runtimePages[self.currentPage] = self.bookEditTextBox.get("1.0","end").rstrip()
            self.currentPage += 1
            self.bookEditTextBox.delete("1.0","end")
            self.bookEditTextBox.insert("1.0",self.runtimePages[self.currentPage].rstrip())
            self.bookPageDisplayer.configure(text=f"Current Page: {self.currentPage+1}")
        else:
            self.runtimePages[self.currentPage] = self.bookEditTextBox.get("1.0","end").rstrip()
            self.currentPage += 1
            self.runtimePages.append("")
            self.bookEditTextBox.delete("1.0","end")
            self.bookPageDisplayer.configure(text=f"Current Page: {self.currentPage+1}")
    
    def previous_page(self):
        if self.currentPage > 0:
            self.runtimePages[self.currentPage] = self.bookEditTextBox.get("1.0","end").rstrip()
            self.currentPage -= 1
            self.bookEditTextBox.delete("1.0","end")
            self.bookEditTextBox.insert("1.0",self.runtimePages[self.currentPage].rstrip())
            self.bookPageDisplayer.configure(text=f"Current Page: {self.currentPage+1}")
    
    def open_book(self,name):
        for n in self.books_data:
            if n.name == name:
                if self.secondWindow == None:
                    self.create_second_window_for_book(name)
                self.secondWindow.title(f"Book Editor: {name}")
                self.runtimePages.clear()
                self.currentPage = 0 
                self.bookEditTextBox.delete("1.0","end")
                for p in n.pages:
                    self.runtimePages.append(p.content)
                self.bookEditTextBox.insert("1.0",self.runtimePages[0])
                self.secondWindow.focus()
                return
    
    def save_book(self,name):
        self.runtimePages[self.currentPage] = self.bookEditTextBox.get("1.0","end").rstrip()
        for b in self.books_data:
            if b.name == name:
                del b.pages
                b.pages = list()
                for p in self.runtimePages:
                    b.add(p)
                    
    def savequit(self):
        self.save()
        self.root.destroy()
        quit()
        
    def save(self):
        names = {"notes":[],"books":[]}
        for name in os.listdir("data/notes"):
            if "." in name:
                if name.split(".")[1] == "txt":
                    os.remove("data/notes/"+name)
        for fn in os.listdir("data/books"):
            for ffn in os.listdir("data/books/"+fn):
                os.remove("data/books/"+fn+"/"+ffn)
            os.rmdir("data/books/"+fn)
        for n in self.notes_data:
            n.save("data/notes")
            names["notes"].append(n.name)
        for b in self.books_data:
            b.save("data/books")
            names["books"].append(b.name)
        with open("data/names.json","w") as file:
            n = json.dumps(names)
            file.write(n)
    
    def load(self):
        with open("data/names.json","r") as file:
            names = json.loads(file.read())
        for name in names["notes"]:
            self.addNoteEntry.delete("0",ctk.END)
            self.addNoteEntry.insert("0",name)
            try: 
                with open("data/notes/"+name+".txt","r") as file:
                    self.new_note(file.read())
            except:
                print(f"Error while loading note '{name}'")
        self.addNoteEntry.delete("0",ctk.END)
        for n in names["books"]:
            self.addBookEntry.delete("0","end")
            self.addBookEntry.insert("0",n)
            b = self.new_book()
            b.pages.clear()
            try:
                for fname in os.listdir("data/books/"+n):
                    with open("data/books/"+n+"/"+fname,"r") as f:
                        b.add(f.read())
            except Exception as e:
                print(f"Error while loading pages of book '{n}':")
                print(e)
        self.addBookEntry.delete("0","end")
        
    def select_category(self,name):
        selected = self.category_frames[name]
        for k,v in self.category_frames.items():
            if k != name:
                v.grid_forget()
        selected.grid(row = 0 ,column=1,pady=5)
        if name == "notes":
            self.notesCategoryBtn.configure(fg_color="#2FA572")
            self.booksCategoryBtn.configure(fg_color="transparent")
            self.scrollbarBooks.grid_forget()
            self.scrollbarNotes.grid(row=0,column=2)
        else:
            self.notesCategoryBtn.configure(fg_color="transparent")
            self.booksCategoryBtn.configure(fg_color="#2FA572")
            self.scrollbarNotes.grid_forget()
            self.scrollbarBooks.grid(row=0,column=2)
        
    def start(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    with open("settings.json","r") as file:
        data = json.loads(file.read())
        ctk.set_appearance_mode(data["appearence-mode"])
        ctk.set_default_color_theme(data["color-theme"])
    noteApp = NoteApp(900,600)
    noteApp.start()