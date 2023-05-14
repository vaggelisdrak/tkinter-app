from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image 
import sqlite3
import re
import time
import webbrowser

class Loadingscreen():
    '''loading bar'''
    def __init__(self,root):
        self.root=root

        self.img = ImageTk.PhotoImage(Image.open("project bg.png"))#---background img
        self.bg = Label(self.root,image=self.img)
        self.bg.place(x=0,y=0,relwidth=1,relheight=1)

        self.fr = Frame(self.bg,bg='#FAD7B3')
        self.fr.pack(expand=True)

        self.txt = Label(self.fr,text='loading...',bg='#FFE5CC',font='none 12 bold')
        self.txt.grid(row=0,column=0,pady=10)

        self.progress_var = StringVar()
        self.loading = ttk.Progressbar(self.fr ,variable =self.progress_var, orient=HORIZONTAL, length=400, mode='determinate')
        self.loading.grid(row=1,column=0)

        self.calculation()

    def progress(self):#---animation
        for x in range(101):   
            time.sleep(0.02)
            self.txt["text"]='loading...'+str(x)+' %'
            self.progress_var.set(x)
            self.bg.update()
        if x==100:
            self.root.forget()

    def calculation(self):#---avoid errors
        try:
            self.progress()
        except:
            pass

class GUI():
    def __init__(self,root):
        self.root=root
        #------------------------------------------------------------------------------------------- main frames

        self.left = Frame(self.root,bg='#FFE5CC',relief =RAISED,bd=5)
        self.left.pack(fill='both',expand=1,side='left')

        self.right = Frame(self.root,bg='#FFE5CC',relief =RAISED,bd=5)
        self.right.pack(fill='both',expand=1,side='right')

        #-------------------------------------------------------------------------------------------- left side

        self.lefttop = Frame(self.left,bg='#461220',relief =RAISED)
        self.lefttop.pack(fill='both',expand=1)

        self.imglogo = ImageTk.PhotoImage(Image.open("download (1).jpg"))
        self.logo = Label(self.lefttop,image=self.imglogo)
        self.logo.grid(row=0,column=0)

        self.course =['1-statistics','2-fetchall','3-urls','4-authors','5-issuedates','6-titles','7-topics']
        self.l1 = Label(self.lefttop,text='Choose one and\n press enter',pady=20,padx=15,bg='#461220',fg='white',font='none 10 bold')
        self.l1.grid(row=1,column=0)

        self.select_bt = Button(self.lefttop,text='SEARCH',command=self.combo, font='none 8 bold', pady=1, bg='#fcb9b2',fg='black',borderwidth=3,width=1,
                    activebackground='#FFE5CC',cursor='hand2')
        self.select_bt.grid(row=2,column=0,padx=3,pady=5)
        self.select_bt.bind("<Enter>", self.on_enter2)
        self.select_bt.bind("<Leave>", self.on_leave2)

        self.cmb = ttk.Combobox(self.lefttop,value=self.course,width=25)
        self.cmb.grid(row=3,column=0)
        self.cmb.current(0)

        self.leftmiddle = Frame(self.left,bg='#461227',relief =RAISED)
        self.leftmiddle.pack(fill='both',expand=1)
        
        #--------------------------------------------------------------------------------------------- right side-top
        
        self.righttop =Frame(self.right,bg='#b23a48')
        self.righttop.pack(fill='x',side='top')

        self.top = Label(self.righttop,text='ΝΗΜΕΡΤΗΣ - archive of Phd theses',fg='white',bg='#FFF9F9',font='ariel 52 bold',pady=40,padx=196,relief=RAISED)
        self.top.grid(row=0,column=0)
        self.screen_change()

        #--------------------------------------------------------------------------------------------- right side-under title

        self.frame2 =Frame(self.right,bg='#b23a48')
        self.frame2.pack(fill='x')

        self.menu_img = ImageTk.PhotoImage(Image.open("menu.png"))#---menu-open img
        self.menu = Button(self.frame2,image=self.menu_img,command=self.call_bookmarks,bg='#fcb9b2',activebackground='#fcb9b2',cursor='hand2')
        self.menu.grid(row=1,column=0,padx=15)

        self.search =Entry(self.frame2,borderwidth=8,width=45)
        self.search.grid(row=1,column=1,padx=40,pady=5,rowspan=3)
        self.search.bind('<Return>',self.find)

        self.bt = Button(self.frame2,text='CLEAR',command=self.clear, fg='black', bg='#fcb9b2', padx = 5, pady = 5,font='none 10 bold',borderwidth=3)
        self.bt.grid(row=1,column=2,pady=5,padx=1,rowspan=3)
        self.bt.bind("<Enter>", self.on_enter1)
        self.bt.bind("<Leave>", self.on_leave1)

        self.link = Button(self.frame2,text='ΝΗΜΕΡΤΗΣ',command=self.clicklink, fg='black', bg='#fcb9b2', padx = 5, pady = 5,font='none 10 bold',borderwidth=3)
        self.link.grid(row=1,column=3,pady=5,padx=30,rowspan=3)
        self.link.bind("<Enter>", self.on_enter)
        self.link.bind("<Leave>", self.on_leave)

        self.l = Label(self.frame2,text='',font='none 12 bold',bg='#b23a48',fg='white',pady=10)
        self.l.grid(row=1,column=4,padx=10,pady=5)
        #----------------------------------------------------------------------------------------------- right side-center
  
        self.frame3 = LabelFrame(self.right,bg='#FFE5CC',text="graphs")
        self.frame3.pack(side='right',fill='both',expand=True,anchor=E)

        #----------------------------------------------------------------------------------------------- images and graphs

        self.fav_icon = ImageTk.PhotoImage(Image.open("bookmarkicon.png"))
        self.add_icon = ImageTk.PhotoImage(Image.open("add_icon.png"))
        self.graph_img1 = ImageTk.PhotoImage(Image.open("graph1.png"))
        self.graph_img2 = ImageTk.PhotoImage(Image.open("graph2.png"))
        self.graph_img3 = ImageTk.PhotoImage(Image.open("graph3.PNG"))
        self.graph_img4 = ImageTk.PhotoImage(Image.open("graph4.PNG"))
        self.graph_img5 = ImageTk.PhotoImage(Image.open("graph5.PNG"))

        #----------------------------------------------------------------------------------------------- default
        self.statistics()

        self.clickcount=0
        self.number=1
        self.openMENU = False
        #------------------------------------------------------------------------------------------------ default animations

        self.widthchange()
        self.colorchange()
        self.textchange()
        #------------------------------------------------------------------------------------------------- functions

    def screen_change(self):#---change the size of the title based on the screen width
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        if int(screen_width)<1400:
            self.top.configure(font='ariel 30 bold')

    def widthchange(self):#---animation for changing the width of a button
        platos=0
        while platos<23:
            platos+=1
            time.sleep(0.015)
            self.select_bt.configure(width=platos)
            self.select_bt.update()

    def colorchange(self):#---animation for changing the colors of the title
        time.sleep(0.3)
        r, g, b = 255,255,255
        while g>0 and b>0:
            g-=1
            b-=1
            time.sleep(0.02)
            self.top.configure(fg=f'#{r:02x}{g:02x}{b:02x}')
            self.top.update()
        while r>135:
            r-=1
            time.sleep(0.02)
            self.top.configure(fg=f'#{r:02x}{g:02x}{b:02x}')
            self.top.update()
        
    def textchange(self):#---animation for typing text
        text='Ιδρυματικό Αποθετήριο Πανεπιστημίου Πατρών'
        pos=1
        for letter in text:
            self.l.configure(text=text[0:pos])
            self.l.update()
            time.sleep(0.1)
            pos+=1
    
    def statistics(self):
        self.scrollbars_labels(self.frame3)

        self.graph1 = Label(self.second_frame,image=self.graph_img1)
        self.graph1.grid(row=0,column=0,padx=50,pady=20)
        self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=1, row=0, rowspan=3, sticky='ns')

        self.graph2 = Label(self.second_frame,image=self.graph_img2)
        self.graph2.grid(row=0,column=2,padx=50,pady=20)

        self.graph5 = Label(self.second_frame,image=self.graph_img5)
        self.graph5.grid(row=1,column=0,padx=50)
        self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=1, row=1, rowspan=3, sticky='ns')

        self.graph4 = Label(self.second_frame,image=self.graph_img4)
        self.graph4.grid(row=1,column=2,padx=50,pady=20)

        self.graph3 = Label(self.second_frame,image=self.graph_img3)
        self.graph3.grid(row=2,column=0,padx=50)
        self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=1, row=2, rowspan=3, sticky='ns')


    def headings(self,frame):#---headings for numbers,links,titles,titles-translated,authors,issuedates
        self.query_label=Button(frame,text='no',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=0,pady=5,padx=5)
        
        self.query_label=Button(frame,text='link',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=2,pady=5,padx=5)

        self.query_label=Button(frame,text='title',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=4,pady=5,padx=5)

        self.query_label=Button(frame,text='title-translated',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=6,pady=5,padx=5)

        self.query_label=Button(frame,text='authors',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=8,pady=5,padx=5)
    
        self.query_label=Button(frame,text='issuedates',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=10,pady=5,padx=5)

        self.query_label=Button(frame,image=self.fav_icon,bg='#FFE5CC',pady=6,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=12,pady=5,padx=5)

        #HORIZONTAL SEP LINES
        for i in range(13):
            self.sep = ttk.Separator(frame, orient=HORIZONTAL)
            self.sep.grid(column=i, row=1,sticky="ew")
        #the sticky attribute --> says "if there's more space than needed for this widget, make the edges of the widget "stick" to specific sides of its container".

    def fetch(self,event):#---select the data from the database and fetch them 
        self.recreate_widget()
        self.number = int(self.spinbox.get())
        conn = sqlite3.connect('HMTYof_with_dates.db')
        c = conn.cursor()
        c.execute('SELECT * FROM HMTYof')
        ola = c.fetchall()

        x=2
        self.scrollbars_labels(self.frame3)
        rank=1
        for o in ola:
            self.query_label1=Label(self.second_frame,text=str(rank),bg='#FFE5CC',pady=3,borderwidth=3,font='none 9 bold')
            self.query_label1.grid(row=x,column=0,pady=5,padx=5)
            self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=1, row=x-2, rowspan=3, sticky='ns')

            self.query_label1=Label(self.second_frame,text=str(o[0]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold',cursor="hand2")
            self.query_label1.grid(row=x,column=2,pady=5,padx=5)
            self.query_label1.bind("<Button-1>",self.callback)
            self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=3, row=x-2, rowspan=3, sticky='ns')

            self.query_label=Label(self.second_frame,text=str(o[1]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
            self.query_label.grid(row=x,column=4,pady=5,padx=5)
            self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=5, row=x-2, rowspan=3, sticky='ns')

            self.query_label=Label(self.second_frame,text=str(o[2]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
            self.query_label.grid(row=x,column=6,pady=5,padx=5)
            self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=7, row=x-2, rowspan=3, sticky='ns')

            self.query_label=Label(self.second_frame,text=str(o[3]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
            self.query_label.grid(row=x,column=8,pady=5,padx=5)
            self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=9, row=x-2, rowspan=3, sticky='ns')

            self.query_label=Label(self.second_frame,text=str(o[4]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
            self.query_label.grid(row=x,column=10,pady=5,padx=5)
            self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=11, row=x-2, rowspan=3, sticky='ns')
            
            self.query_label=Button(self.second_frame,image=self.add_icon,command=lambda o=o: self.save_to_bookmarks((o[0],o[1],o[2],o[3],o[4])),bg='#FFE5CC',
                            pady=3,borderwidth=3,font='none 7 bold',relief='flat',cursor='hand2')
            self.query_label.grid(row=x,column=12,pady=5,padx=5)
            self.query_label.bind("<Button-1>",self.bg_change)

            if x > self.number or x > 348 or x < 0:
                break
            x+=1
            rank+=1
        self.headings(self.second_frame)
        conn.commit()
        conn.close()
        
    def combo(self):#---select options from the combobox
        conn = sqlite3.connect('HMTYof_with_dates.db')
        c = conn.cursor()

        if self.cmb.get()=='1-statistics':
            self.recreate_widget()
            self.leftmiddle.pack_forget()
            self.statistics()

        if self.cmb.get()=='2-fetchall':
            self.recreate_widget()
            self.leftmiddle.pack_forget()
            self.leftmiddle = Frame(self.left,bg='#461227',relief =RAISED)
            self.leftmiddle.pack(fill='both',expand=1,side='top')

            self.spinbox = Spinbox(self.leftmiddle,from_=1, to=348,font='Helvetica, 15',width=14)
            self.spinbox.bind('<Return>',self.fetch)

            self.select = Label(self.leftmiddle,text='Επέλεξε τον αριθμό διατριβών\nκαι πάτησε <ENTER>', font='none 8 bold', pady=1, bg='#fcb9b2',
                            fg='black',borderwidth=3,width=23,activebackground='#FFE5CC')

            #animation
            for x in range(-300, 70):
                self.spinbox.place(x=x, y=50)
                self.select.place(x=x,y=0)
                self.select.update()
                self.leftmiddle.update()

        if self.cmb.get()=='3-urls':
            self.recreate_widget()
            self.leftmiddle.pack_forget()
            c.execute('SELECT link FROM HMTYof')
            links= c.fetchall()
            x=0
            y=1
            # Create A Main Frame
            main_frame = Frame(self.frame3)
            main_frame.pack(fill=BOTH, expand=1)

            # Create A Canvas
            my_canvas = Canvas(main_frame,bg='#FFE5CC')
            my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

            # Add A Scrollbar To The Canvas
            my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
            my_scrollbar.pack(side=RIGHT, fill=Y)

            # Configure The Canvas
            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

            # Create ANOTHER Frame INSIDE the Canvas
            second_frame = Frame(my_canvas,bg='#FFE5CC')

            # Add that New frame To a Window In The Canvas
            my_canvas.create_window((0,0), window=second_frame, anchor="ne")
            rank=1
            for link in links:
                self.query_label1=Label(second_frame,text=str(rank),bg='#FFE5CC',pady=3,borderwidth=3,font='none 11 bold')
                self.query_label1.grid(row=x,column=0,pady=5,padx=5)
                self.query_label_link=Label(second_frame,text=str(link[0]),bg='#fcb9b2',pady=3,borderwidth=3,cursor="hand2")
                self.query_label_link.grid(row=x,column=y,pady=5,padx=30)
                self.query_label_link.bind("<Button-1>",self.callback)
                x+=1
                rank+=1
            conn.commit()
            conn.close()

        if self.cmb.get()=='4-authors':
            def sort():#---alphabetic order
                self.clickcount+=1
                self.text.delete('1.0', END)
                displayed_text=''
                if self.clickcount % 2==0:
                    rank=1
                    for a in auth:
                        displayed_text += str(rank)+')  '+str(a[0]) +2*'\n'
                        rank+=1
                else:
                    for a in sorted(auth):
                        displayed_text +=str(a[0]) +2*'\n'
                self.text.insert('end', displayed_text)

            self.recreate_widget()
            self.leftmiddle.pack_forget()

            self.alpha_order=Checkbutton(self.frame3,command=sort, text="αλφαβητική σειρά", font="BahnschriftLight 13", takefocus=0, bg="#FFE5CC", fg="#E91E63", 
            activebackground="#FF9999", activeforeground="#E91E63", bd=0, highlightthickness=0, width=20, selectcolor="black", height=2)
            self.alpha_order.pack(side='top')

            c.execute('SELECT authors FROM HMTYof')
            auth= c.fetchall()
            rank=1
            displayed_text=''
            for a in auth:
                displayed_text += str(rank)+')  '+str(a[0]) +2*'\n'
                rank+=1

            self.scrollbars()
            self.text.delete('1.0', END)
            self.text.insert('end', displayed_text)

            #self.text.see('end') an thes na xekina apo kato
            conn.commit()
            conn.close()

        if self.cmb.get()=='5-issuedates':
            self.recreate_widget()
            self.leftmiddle.pack_forget()
            c.execute('SELECT day FROM HMTYof')
            days= c.fetchall()
            displayed_text=''
            rank=1
            for d in days:
                displayed_text += str(rank)+')   '+str(d[0][0:10]) +2*'\n'
                rank+=1

            self.scrollbars()
            self.text.insert('end', displayed_text)
            conn.commit()
            conn.close()

        if self.cmb.get()=='6-titles':
            self.recreate_widget()
            self.leftmiddle.pack_forget()
            c.execute('SELECT title FROM HMTYof')
            titles= c.fetchall()
            displayed_text=''
            rank=1
            for t in titles:
                displayed_text += str(rank)+')  '+str(t[0]) +2*'\n'
                rank+=1

            self.scrollbars()
            self.text.insert('end', displayed_text)
            conn.commit()
            conn.close()

        if self.cmb.get()=='7-topics':
            self.recreate_widget()
            self.leftmiddle.pack_forget()
            c.execute('SELECT abstract FROM HMTYof')
            subj= c.fetchall()
            displayed_text=''
            rank=1
            for s in subj:
                displayed_text += str(rank)+')\t'+str(s[0]) +2*'\n'
                rank+=1

            self.scrollbars()
            self.text.insert('end', displayed_text)
            conn.commit()
            conn.close()

    def find(self,event):#---search engine
        self.recreate_widget()
        self.leftmiddle.pack_forget()
        conn = sqlite3.connect('HMTYof_with_dates.db')
        c = conn.cursor()

        #name-keywords-title

        searched = self.search.get()

        c.execute('SELECT link,title,titletrans,authors,day,keywords FROM HMTYof')
        result = c.fetchall()
        label_print=[]
        for i in result:
            if i[3].lower().split(', ')[0] == str(searched.lower().strip()):#lastname
                label_print.append(i)

            elif i[3].lower().split(', ')[1] == str(searched.lower().strip()):#firstname
                label_print.append(i)

            elif i[3].lower().split(', ')[0] + i[3].lower().split(', ')[1] == str(searched.lower().strip().replace(' ','')):#name
                label_print.append(i)
            else:
                try:
                    ini_str = str(i[5])
                    # Splitting on UpperCase using re
                    res_list = []
                    res_list = re.findall('[Α-Ω][^A-Ω]*', ini_str)
                    
                    wordslist=[]
                    for o in res_list:
                        o=o.split()
                        for b in o:
                            wordslist.append(b.lower())#makes a list with all the keywords for each string of keywords

                    for c in searched.lower().strip().split():
                        if c in wordslist:#keywords
                            #print(i)
                            label_print.append(i)

                        elif c in i[1].lower():#title
                            #print(i)
                            label_print.append(i)

                        elif c in i[2].lower():#titletrans
                            #print(i)
                            label_print.append(i)
                        else:
                            pass
                except:
                    pass
   
        try:
            if not label_print:
                raise ValueError
            label_print = list(dict.fromkeys(label_print))
            x=2
            self.scrollbars_labels(self.frame3)
            rank=1
            for o in label_print:
                self.query_label1=Label(self.second_frame,text=str(rank),bg='#FFE5CC',pady=3,borderwidth=3,font='none 9 bold')
                self.query_label1.grid(row=x,column=0,pady=5,padx=5)
                self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=1, row=x-2, rowspan=3, sticky='ns')

                self.query_label1=Label(self.second_frame,text=str(o[0]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold',cursor="hand2")
                self.query_label1.grid(row=x,column=2,pady=5,padx=5)
                self.query_label1.bind("<Button-1>",self.callback)
                self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=3, row=x-2, rowspan=3, sticky='ns')

                self.query_label=Label(self.second_frame,text=str(o[1]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
                self.query_label.grid(row=x,column=4,pady=5,padx=5)
                self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=5, row=x-2, rowspan=3, sticky='ns')

                self.query_label=Label(self.second_frame,text=str(o[2]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
                self.query_label.grid(row=x,column=6,pady=5,padx=5)
                self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=7, row=x-2, rowspan=3, sticky='ns')

                self.query_label=Label(self.second_frame,text=str(o[3]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
                self.query_label.grid(row=x,column=8,pady=5,padx=5)
                self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=9, row=x-2, rowspan=3, sticky='ns')

                self.query_label=Label(self.second_frame,text=str(o[4]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
                self.query_label.grid(row=x,column=10,pady=5,padx=5)
                self.sep = ttk.Separator(self.second_frame, orient=VERTICAL).grid(column=11, row=x-2, rowspan=3, sticky='ns')

                self.query_label_btn=Button(self.second_frame,image=self.add_icon,command=lambda o=o: self.save_to_bookmarks((o[0],o[1],o[2],o[3],o[4])),bg='#FFE5CC',
                                pady=3,borderwidth=3,font='none 7 bold',relief='flat',cursor='hand2')
                self.query_label_btn.grid(row=x,column=12,pady=5,padx=5)
                self.query_label_btn.bind("<Button-1>",self.bg_change)

                if x > len(label_print):
                    break
                x+=1
                rank+=1
            self.headings(self.second_frame)
        except:
            messagebox.showerror(title='error', message='Δεν βρέθηκαν αποτελέσματα')
        conn.commit()
        conn.close()

    def clear(self):#--- clear everything
        self.search.delete(0,'end')
        self.recreate_widget()
        self.leftmiddle.pack_forget()

    def clicklink(self):#--- opens the original website in a new tab
        webbrowser.open_new("https://nemertes.library.upatras.gr/jspui/handle/10889/21?")

    def callback(self,event):
        webbrowser.open_new(event.widget.cget("text"))

    def recreate_widget(self):
        self.frame3.pack_forget()
        self.frame3 =Frame(self.right,bg='#FFE5CC')
        self.frame3.pack(side='right',fill='both',expand=True,anchor=E)

    def scrollbars(self):#---scrollbars for the Text widget
        scrol = Scrollbar(self.frame3)
        self.text = Text(self.frame3, height=10, font='Arial 13', width=173, bg='#FFE5CC')
        self.text.pack(side='left', fill='y')
        scrol.pack(side='right', fill='y')
        scrol.config(command=self.text.yview)
        self.text.config(yscrollcommand=scrol.set)

    def scrollbars_labels(self,frame):#---scollbars for labels
        # Create A Main Frame
        self.main_frame = Frame(frame)
        self.main_frame.pack(fill=BOTH, expand=1)

        # Create A Canvas
        self.my_canvas = Canvas(self.main_frame,bg='#FFE5CC')
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Create ANOTHER Frame INSIDE the Canvas
        self.second_frame = Frame(self.my_canvas,bg='#FFE5CC')

        self.third_frame = Frame(self.my_canvas)
        self.third_frame.pack(side=BOTTOM,fill=X, expand=1,anchor='se')

        # Add Scrollbars To The Canvas
        self.my_scrollbar = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)

        self.my_scrollbar1 = ttk.Scrollbar(self.third_frame, orient=HORIZONTAL, command=self.my_canvas.xview)
        self.my_scrollbar1.pack(side=BOTTOM, fill=X)

        # Configure The Canvas
        self.my_canvas.configure(xscrollcommand=self.my_scrollbar1.set,yscrollcommand=self.my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all")))

        # Add that New frame To a Window In The Canvas
        self.my_canvas.create_window((0,0), window=self.second_frame, anchor="ne")

    def on_enter(self,event):#--- if the cursor is inside the button
        self.link['background'] = '#FFCC99'

    def on_leave(self,event):#--- if the cursor is outside the button
        self.link['background'] = '#fcb9b2'

    def on_enter1(self,event):#--- if the cursor is inside the button
        self.bt['background'] = '#FFCC99'
    
    def on_leave1(self,event):#--- if the cursor is outside the button
        self.bt['background'] = '#fcb9b2'

    def on_enter2(self,event):#--- if the cursor is inside the button
        self.select_bt['fg']='white'
        self.select_bt.configure(font='none 10 bold')

    def on_leave2(self,event):#--- if the cursor is outside the button
        self.select_bt['fg']='black'
        self.select_bt.configure(font='none 8 bold')
    
    def bg_change(self,event):#--- it changes the color of the clicked widget
        event.widget.configure(bg='#fcb9b2')
    
    def call_bookmarks(self):
        b = Bookmarks(self.root)
  
    def save_to_bookmarks(self,diatrivh):#---append to the bookmarks file
        fav_diatrivh=[]
        fav_diatrivh.append(diatrivh)
        f = open('favourites.txt','a',encoding='utf-8')
        for i in fav_diatrivh:
            f.write(str(i)+'\n')
        f.close()
  
class Bookmarks():
    def __init__(self,root):
        self.root=root
        self.screen_width = int(self.root.winfo_screenwidth())
        self.screen_height = int(self.root.winfo_screenheight())
        self.openMENU = True

        self.close_img = ImageTk.PhotoImage(Image.open("close.png"))#---menu-close img
        self.remove_icon = ImageTk.PhotoImage(Image.open("delete.png"))
        self.fav_icon = ImageTk.PhotoImage(Image.open("bookmarkicon.png"))

        if self.openMENU is True:
            self.navRoot = Frame(self.root, bg="#FAD7B3", height=self.screen_height-10, width=self.screen_width,borderwidth=3)
            self.navRoot.place(x=-self.screen_width, y=0)

            navroot_label = Label(self.navRoot,bg='#b23a48',width=self.screen_width,height=3)
            navroot_label.place(x=0,y=0)

            closeBtn = Button(self.navRoot, image=self.close_img,bg='#fcb9b2',activebackground='#fcb9b2',cursor='hand2', command=self.close_menu)
            closeBtn.place(x=self.screen_width-50, y=10)

            title = Label(self.navRoot,text='Αγαπημένες Διατριβές',font='Times 17 bold',fg='black',bg="#FAD7B3")
            title.place(x=(self.screen_width/2)-100,y=70)

            myframe = LabelFrame(self.navRoot,bg='#FAD7B3',text='favourite',width=self.screen_width,height=self.screen_height)
            myframe.place(x=2,y=100)

            diatrives=[]
            f = open('favourites.txt','r',encoding='utf-8')
            for d in f:
                d = d.replace('\n','')
                d = d.replace('(','')
                d = d.replace(')','')
                diatrives.append(d.split(', '))
            f.close()
            res = list(set(tuple(sub) for sub in diatrives))#---removes duplicates from nested list

            self.canvas=Canvas(myframe,bg='#FFE5CC')
            frame=Frame(self.canvas,bg='#FFE5CC')

            myscrollbar=Scrollbar(myframe,orient="vertical",command=self.canvas.yview)
            myscrollbar.pack(side="right",fill="y")

            mysecondscrollbar = Scrollbar(myframe,orient="horizontal",command=self.canvas.xview)
            mysecondscrollbar.pack(side='bottom',fill='x')

            self.canvas.configure(yscrollcommand=myscrollbar.set,xscrollcommand=mysecondscrollbar.set)
            self.canvas.pack(side="left")

            self.canvas.create_window((0,0),window=frame,anchor='nw')
            frame.bind("<Configure>",self.myfunction)
            
            self.labels=dict()
            x=2
            rank=1
            no=0
            for i in res:
                self.labels[no]=Label(frame,text=str(rank),bg='#FFE5CC',pady=3,borderwidth=3,font='none 9 bold')
                self.labels[no].grid(row=x,column=0,pady=5,padx=5)
                self.sep = ttk.Separator(frame, orient=VERTICAL).grid(column=1, row=x-2, rowspan=3, sticky='ns')

                self.labels[no+1]=Label(frame,text=str(i[0][1:-1]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold',cursor="hand2")
                self.labels[no+1].grid(row=x,column=2,pady=5,padx=5)
                self.labels[no+1].bind("<Button-1>",self.callback)
                self.sep = ttk.Separator(frame, orient=VERTICAL).grid(column=3, row=x-2, rowspan=3, sticky='ns')

                self.labels[no+2]=Label(frame,text=str(i[1][1:-1]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
                self.labels[no+2].grid(row=x,column=4,pady=5,padx=5)
                self.sep = ttk.Separator(frame, orient=VERTICAL).grid(column=5, row=x-2, rowspan=3, sticky='ns')

                self.labels[no+3]=Label(frame,text=str(i[2][1:-1]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
                self.labels[no+3].grid(row=x,column=6,pady=5,padx=5)
                self.sep = ttk.Separator(frame, orient=VERTICAL).grid(column=7, row=x-2, rowspan=3, sticky='ns')

                self.labels[no+4]=Label(frame,text=str(i[3][1:]+' '+i[4][:-1]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
                self.labels[no+4].grid(row=x,column=8,pady=5,padx=5)
                self.sep = ttk.Separator(frame, orient=VERTICAL).grid(column=9, row=x-2, rowspan=3, sticky='ns')

                self.labels[no+5]=Label(frame,text=str(i[5][1:-1]),bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold')
                self.labels[no+5].grid(row=x,column=10,pady=5,padx=5)
                self.sep = ttk.Separator(frame, orient=VERTICAL).grid(column=11, row=x-2, rowspan=3, sticky='ns')

                self.labels[no+6]=Button(frame,image=self.remove_icon,bg='#FFE5CC',pady=3,borderwidth=3,font='none 7 bold',relief='flat',cursor='hand2')
                self.labels[no+6].grid(row=x,column=12,pady=5,padx=5)
                self.labels[no+6].bind("<Button-1>",self.remove_from_bookmarks)

                if x > len(res):
                    break
                x+=1
                rank+=1
                no+=7
                
            self.headings(frame)

            #--create animated opening
            for x in range(-int(self.screen_width/10), 0):
                if x<0:
                    self.navRoot.place(x=-x**2, y=0)
                    self.navRoot.update()
                else:
                    self.navRoot.place(x=x**2, y=0)
                    self.navRoot.update()

    def headings(self,frame):#---headings for numbers,links,titles,titles-translated,authors,issuedates
        self.query_label=Button(frame,text='no',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=0,pady=5,padx=5)
        
        self.query_label=Button(frame,text='link',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=2,pady=5,padx=5)

        self.query_label=Button(frame,text='title',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=4,pady=5,padx=5)

        self.query_label=Button(frame,text='title-translated',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=6,pady=5,padx=5)

        self.query_label=Button(frame,text='authors',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=8,pady=5,padx=5)
    
        self.query_label=Button(frame,text='issuedates',bg='#FFE5CC',pady=3,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=10,pady=5,padx=5)

        self.query_label=Button(frame,image=self.fav_icon,bg='#FFE5CC',pady=6,borderwidth=3,font='none 12 bold',relief=SUNKEN)
        self.query_label.grid(row=0,column=12,pady=5,padx=5)

        #HORIZONTAL SEP LINES
        for i in range(13):
            self.sep = ttk.Separator(frame, orient=HORIZONTAL)
            self.sep.grid(column=i, row=1,sticky="ew")
        #the sticky attribute --> says "if there's more space than needed for this widget, make the edges of the widget "stick" to specific sides of its container".

    def callback(self,event):
        webbrowser.open_new(event.widget.cget("text"))

    def myfunction(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=self.screen_width-40,height=self.screen_height-200)

    def close_menu(self):#--create animated closing
        for x in range(45):
            self.navRoot.place(x=-(x**2), y=0)
            self.navRoot.update()
        self.openMENU = False
        time.sleep(0.3)
        self.navRoot.destroy()

    def remove_from_bookmarks(self,event):
        widget = event.widget
        info = widget.grid_info()
        x = int(info['row']) #---gets the row of the pressed button
        
        pol_of_7=[]#---for this row (x) finds the index of the first label (i)
        count = 1
        num = 1
        if x>2:
            while count < x:
                num +=1
                if num % 7==0:
                    pol_of_7.append(num)
                    count += 1
            i= pol_of_7[x-3]
        else:
            i=0

        link = (self.labels[i+1].cget('text'))
        title = (self.labels[i+2].cget('text'))
        titletrans = (self.labels[i+3].cget('text'))
        surname = (self.labels[i+4].cget('text'))
        name = (self.labels[i+5].cget('text'))
        
        #delete all the widgets of the row=x
        self.labels[i].destroy()
        self.labels[i+1].destroy()
        self.labels[i+2].destroy()
        self.labels[i+3].destroy()
        self.labels[i+4].destroy()
        self.labels[i+5].destroy()
        self.labels[i+6].destroy()
        #--------------------------------------------------------------remove from file

        with open("favourites.txt", "r",encoding='utf-8') as f:
            lines = f.readlines()

        with open("favourites.txt", "w",encoding='utf-8') as f:
            for line in lines:
                #print(line.strip('\n').split(', ')[0][2:-1]) #link
                if line.strip('\n').split(', ')[0][2:-1] != str(link):#--writes to the file everything apart from the line that has been removed from the bookmarks
                    f.write(line)

#--main--

class Main():
    def __init__(self): 
        try: 
            root = Tk()
            root.title('HMTY - Phd theses')
            root.state('zoomed')#fullscreen
            #root.resizable(False,False)
            startingpage = Loadingscreen(root)
            #-----------------------------------------
            root.title('HMTY - Phd theses')
            root.state('zoomed')
            #root.geometry('1915x1050')
            web =GUI(root)
            root.mainloop()
        except:
            pass
      
if __name__ == "__main__":
    Main()