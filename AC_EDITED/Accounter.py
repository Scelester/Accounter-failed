#!/usr/bin/python
"""
The Accounter 1.O devloped by Nabin Paudel and SleepySama.
Contact me on : ninedust.org@gmail.com

Short_cut keys for search bar:
		..e    :  check for math errors in accounts
		..an   :	 show total number of account.
		..n    :  show total number of acounts with Account name.
		..madd :  open export from excel dialog box.

Other shortCuts:
		ctrl+ s        : to enter or exit search bar
		ctrl+a    : to add new accounts
		ctrl + x  : destroy new account creation frame

"""



import tkinter as tk
from collections import OrderedDict
from tkinter import ttk , font, messagebox
import os,pickle
import got_data



#app start
PATH = os.path.dirname(__file__)












"""                  //////////////////////////////////////////////////////////////////////////           """


# Setting up the root and window to display
root = tk.Tk()
WIDTH=root.winfo_screenwidth();HEIGHT=root.winfo_screenheight()
root.update_idletasks()
root.geometry(f'{WIDTH}x{HEIGHT}+0+20')
root.title('Accounter')
root.resizable(True, True)
root.focus_set()
# photo = tk.PhotoImage(file = PATH + '\\icon.png')
# root.iconbitmap(PATH + '/icon.ico')





"""                  ///////////////////////////////////////////////////////////////////////           """


APP_MAINFRAME = tk.Frame(root)
APP_MAINFRAME.grid()



# subsection works after button click
def change_section(name,dictx):
	global SUBSECTION
	APP_MAINFRAME.grid_forget()
	Main_Canvas.delete('all')
	SUBSECTION = tk.Frame(root,width=root.winfo_screenwidth(),height=root.winfo_screenheight())
	SUBSECTION.grid(sticky='nsew')
	SUBSECTION.columnconfigure(0,weight=1);SUBSECTION.rowconfigure(0,weight=1)
	top_label = tk.Label(SUBSECTION, relief="groove",text=name,
		font=('Helvetica',25),bg='black',fg='white',width=30)
	top_label.grid(row=0,column=0,sticky='nw',pady=0,ipady=5)
	Gobackbutton = tk.Button(SUBSECTION,text= 'Go back',
		bg= 'black',fg= 'white',width=15,command=lambda:change_section_to_main())
	Gobackbutton.place(x=640,y=660)
	subtt = tabeltitle(SUBSECTION,xpad=(3,2),ypad=(0,0))
	subtt.all_wd = False
	subtt.create_subwidgets(namelist,tablewidthdict)
	
	# creating canvas for subwindow
	subcanvframe = tk.Frame(SUBSECTION)
	subcanvframe.grid(sticky='w',row=4,pady=(0,70))
	
	sub_main_canvas = tk.Canvas(subcanvframe,width = (WIDTH-150),height = 540)
	sub_main_canvas.pack(side='left' , fill= 'both', expand= 1,ipady=2)


	sscroll = ttk.Scrollbar(subcanvframe,orient='vertical',command=sub_main_canvas.yview)
	sscroll.pack(side='right',fill='y')

	# Adding stuff to the table in sub main table
	SUBMAINDICT = {}
	temp_list = list(maindict.keys())
	for n in temp_list:
		if dictx[n]['name'].lower() == name.lower():
			SUBMAINDICT[n] = dictx[n]

	if SUBMAINDICT:
		sub_main_table = main_table(sub_main_canvas,SUBMAINDICT,sscroll)
		sub_main_table.all_wd = False
		sub_main_table.update_table_list()
		sub_main_table.scroll_setting(sub_main_canvas)	
	
	sub_temp_list = list(SUBMAINDICT.keys())
	per_Ac_tots = int()
	per_Ac_fee =  int()
	per_Ac_paid = int()
	for n in sub_temp_list:
		per_Ac_tots += SUBMAINDICT[n]['total']
		per_Ac_fee += SUBMAINDICT[n]['fee']
		per_Ac_paid += SUBMAINDICT[n]['paid']

	cc = tk.Frame(SUBSECTION,)
	cc.grid(row=0,column=0,padx=(2,1),sticky='e')

	paid_lable = tk.Label(cc,text=f"Total Paid= {per_Ac_paid}",
		font=('Helvetica',13),relief='groove',borderwidth=5,width=17)
	paid_lable.grid(row= 0, column=0,padx=10,ipady=5)

	Fee_lable = tk.Label(cc,text=f"Total Fee= {per_Ac_fee}",
		font=('Helvetica',13),relief='groove',borderwidth=5,width=17)
	Fee_lable.grid(row= 0, column=1,padx=10,ipady=5)

	Tots_lable = tk.Label(cc,text=f"Total Rem= {per_Ac_tots}",
		font=('Helvetica',13),bg='black',relief='groove',borderwidth=5,width=17)
	Tots_lable.grid(row= 0, column=2,padx=10,ipady=5)




#revert back to main page
def change_section_to_main():
	SUBSECTION.destroy()
	APP_MAINFRAME.grid()
	maindict = load_dict()
	main_window_refresh(md = maindict)
	





"""               ******///////////////////////////////////////////////////////////////////////****           """


maindict = {}
# Logic and workarounds
def load_dict():
	global maindict
	try:
		with open(PATH+'/main_dict.pickle','rb') as dictx:
			maindict = pickle.load(dictx)
			return maindict
	except EOFError:
		pass

def store_in_pickle(m):
	with open(PATH+'/main_dict.pickle','wb') as dumpdictx:
		pickle.dump(m,dumpdictx)



load_dict()






"""                 ///////////////////////////////////////////////////////////////////////           """
def ult_rem_tots():
	c = int()
	for n in maindict:
		c += maindict[n]['total']

	return c



"""                /////////////////////////////////////////////////////////////////////////              """
def check_for_errors():
	for n in maindict:
		error_message = "Math Error in serial number {}"
		checking = (maindict[n]['fee']-maindict[n]['paid'])
		if checking != maindict[n]['total']:
			messagebox.showerror("Error check",error_message.format(n+1))
			break
	else:
		messagebox.showinfo("Error check",'No Math Errors')
"""                /////////////////////////////////////////////////////////////////////////              """
def all_name_count():
	pseudo_names=[]
	for n in maindict:
		if maindict[n]['name'] not in pseudo_names:
			pseudo_names.append(maindict[n]['name'])
	messagebox.showinfo("Total names",'Total_Account: '+str(len(pseudo_names)))

"""                ////////////////////////////////////////////////////////////////////////              """
class all_name_list():
	def __init__(self,):
		self.new_win = tk.Tk()
		self.new_win.title('All Accounts name')
		self.list_of_name = tk.Text(self.new_win,font=('Helvetica',10))
		self.list_of_name.pack(fill='both',expand=1)
		nameset = set(maindict[name]['name'] for name in range(len(list(maindict))))
		for n,i in enumerate(nameset):
			self.list_of_name.insert(f'{n+1}.0',str(n+1)+'. '+str(i.title())+'\n')





"""                ////////////////////////////////////////////////////////////////////////              """

# Change the number here to change the size of the title bars.

tablewidthdict= OrderedDict( {'sn':5,
							 'name':25,
							 'date':16,
							 'Description':14,
							 'time':15,
							 'fee':10,
							 'paid':10,
							 'total':11,
							 'checkboxwidth':4,
							 'buttonwidth':5,
							} )

# Change the title bar here to name 

namelist = ['SN','Name','date','Description','time','Fee','Paid','Total Rem.','✓','Goto']













# tittle bar 
class Logics():
	def __init__(self):
		self.Loss = 0
		
		
	def top_frame_update(self):
		self.topgreenlinewidth = (WIDTH/4 - self.Loss) - round((WIDTH/(WIDTH/8))*8,-1)
		self.topredlinewidth = (WIDTH/4 + self.Loss)   - round((WIDTH/(WIDTH/8))*8,-1)

		self.main_bar_container = tk.Frame(APP_MAINFRAME,highlightbackground='black',bg="red"
			,highlightthickness=2)
		
		APP_MAINFRAME.grid_columnconfigure(0,weight=1)

		self.main_bar_container.grid(row=0,column=0,sticky='we')

		topframeleft = tk.Frame(self.main_bar_container,bg='lightgreen')     #adding the frame with green background yo
		topframeleft.grid(row=0,column=0,ipadx=logic.topgreenlinewidth,	# displaying the frame
						ipady=0 ,sticky='we'
					)
		topframeleft.columnconfigure(0,weight=1)                  # columnconfiguration for sticky situation lol
		top_paid = tk.Label(topframeleft,   # creating label for greeny
			bg='lightgreen',font=('Arial Black',15))
		top_paid.config(width=8)                        # setting the fixed width to our label in the greeny
		top_paid.grid(ipady=0,sticky='w')				# displaying the label 



		# doing the same thing as above just opposite you will understand once you see me.
		topframeright = tk.Frame(self.main_bar_container,bg='red')    
		topframeright.grid(row=0,column=1, 
							ipadx=logic.topredlinewidth,					# ""
							ipady=0,sticky='we'																						
					)
		topframeright.columnconfigure(0,weight=1)
		top_rem_to_pay = tk.Label(topframeright,      # ""
			bg='red',font=('Arial Black',15))
		top_rem_to_pay.config(width=8)
		top_rem_to_pay.grid(ipady=0,sticky='e')			
		root.update_idletasks()


logic = Logics()
logic.top_frame_update()













"""////////////////////////////////////////////////////////////////////////////////              """
# Table class
class tabeltitle(tk.Frame):
	def __init__(self,parent,ypad=(10,0),xpad=(1,4),**kwargs,):
		super().__init__(parent,**kwargs,
			width=1320,height=40,bd=0,)
		self.grid(row=2,column=0,pady=(10,0),sticky='nw')
		self.all_wd = True
		self.xpad = xpad

	def inside_text_widgets(self,txt,w,c):
		sn = tk.Label(self,text=txt,font=('TkDefaultFont',13),
			bg='black',fg='white',width=w,height=2)
		sn.grid(pady=0,padx=self.xpad,row=0,column=c)

		
	def create_subwidgets(self,namelist,tablewidthdict):
		for n in range(len(namelist)):
			if namelist[n] not in ('✓','Goto'):
				self.inside_text_widgets(namelist[n],tablewidthdict[list(tablewidthdict)[n]],n)
			if self.all_wd == True:
				self.inside_text_widgets(namelist[n],tablewidthdict[list(tablewidthdict)[n]],n)


obj_tabletitle = tabeltitle(APP_MAINFRAME)
obj_tabletitle.create_subwidgets(namelist,tablewidthdict)












"""                       //////////////////////////////////////////////////////////////////////              """
#creating parent frame for Canvas
Parent_of_main_table = tk.Frame(APP_MAINFRAME,bg='grey',height = 565,width = (WIDTH-80) )
Parent_of_main_table.grid(sticky='w',row=3,column=0)

#creating canves in parent_of_main_table 
Main_Canvas = tk.Canvas(Parent_of_main_table,width = (WIDTH-15),height = 553,)
Main_Canvas.pack(side='left' , fill= 'both', expand= 1,ipady=2)
scroll_bar = ttk.Scrollbar(Parent_of_main_table,orient='vertical',command=Main_Canvas.yview)


class main_table(tk.Frame):
	def __init__(self,parent,maindict,scrbr,**kwargs,):
		
		super().__init__(parent,width=1300,**kwargs,)
		
		parent.create_window((0,0),window=self,anchor='nw')

		if len(maindict) >= 20:
			self.maindict = maindict[:20]
		else:
			self.maindict = maindict

		self.namelist = []

		self.temp_list = list(self.maindict.keys())
		
		self.all_wd = True	

		self.scroll_bar = scrbr

		self.cb_list= []

		self.cb_snlist = []

		self.env_tes_red = 1
		self.env_tes_green = 1


	def scroll_setting(self,parent):
		if len(self.temp_list) <= 15:
			self.scroll_bar.pack_forget()
		elif len(self.temp_list) >= 16:
			self.scroll_bar.pack(side='right',fill='y')

			parent.configure(yscrollcommand= self.scroll_bar.set)
			parent.bind_all('<Configure>',lambda e:parent.configure(scrollregion=parent.bbox('all')))
		    
			parent.bind_all("<MouseWheel>",lambda event:parent.yview_scroll(-1*(int(event.delta/120)), "units"))


	def update_table_list(self):
		
		for m in maindict.values():
			self.namelist.append( m['name'])



		for list_n in self.temp_list:
			background_ = self.background_selector(list_n,namelist)

			self.f = tk.Frame(self)
			self.f.grid()

			c = 0
			for dict_m in self.maindict[list_n]:
				txt = self.maindict[list_n][dict_m]
				c += 1
				p_width_list = list(tablewidthdict.values())[:9]
				w = p_width_list[c]
				if c ==1:
					w += 3
				if c == 2:
					w += 2
				if c == 3:
					w += 1
				if c == 4 or c==5:
					w+= 1
				if  c== 6 or c==7:
					w+= 1
				self.add_from_the_dlist(txt,w,c+1,list_n,dict_m,background_)
			

			self.adding_rem(background_,list_n)

	

	def adding_rem(self,background_,list_n):
		self.jv = tk.Label(self.f,text=list_n+1,font=('Helvetica',13),bg=background_,width=tablewidthdict['sn'])
		self.jv.grid(pady=1,padx=3,row=list_n,column=0,ipady=4)

		if self.all_wd == True:
			last_button = tk.Button(self.f,text="⇲GO",bg=background_,font=('Helvetica',9),
				width=tablewidthdict['buttonwidth']+1,cursor='',
				command=lambda : change_section(self.maindict[list_n]['name'].title(),maindict))
			last_button.grid(pady=1,padx=(3,0),row=list_n,column=10)


	
	
	def add_from_the_dlist(self,txt,w,c,list_n,dict_m,background_):
		if dict_m != 'cb':
			
			self.jkv = tk.Label(self.f,text=txt,font=('Helvetica',13),bg=background_,width=w)
			self.jkv.grid(pady=1,padx=(2,3),row=list_n,column=c)

		elif dict_m == 'cb' and self.all_wd== True:
			
			def change_state():
				for n in list(self.maindict):
					cb_var_to_check = self.cb_list[list(self.maindict).index(n)].get()
					if cb_var_to_check == 1 and n not in self.cb_snlist:
						self.cb_snlist.append(n)
					if cb_var_to_check == 0 and n in self.cb_snlist:
						self.cb_snlist.remove(n)


			self.cb_list.append(tk.IntVar())
			cb = tk.Checkbutton(self.f,width=w-2,bg=background_,
				variable=self.cb_list[list(self.maindict).index(list_n)],command=change_state)
			cb.grid(pady=1,padx=0,row=list_n,column=c)




	def background_selector(self,list_n,namelist):
		total = int()
		temp_list = list(maindict.keys())

		total = maindict[list_n]['total']
				
		if total >= 15000:
			return '#FF3131'
		else:
			return '#21bc1c'


	


if maindict:
	obj_main_table = main_table(Main_Canvas,maindict,scroll_bar)
	obj_main_table.update_table_list()
	obj_main_table.scroll_setting(Main_Canvas)











"""////////////////////////////////////////////////////////////////////////////////              """
class bottom_frame(tk.Frame):
	def __init__(self,parent,**kwargs):
		super().__init__(parent,width=WIDTH,height=40,**kwargs)
		APP_MAINFRAME.columnconfigure(0,weight=1)
		self.grid(pady=(5,0),sticky='w')
		self.grid_propagate(0)
		self.columnconfigure(0,weight=1)
		self.search_var = tk.StringVar()
		self.search_var.set('Search Here...')

		self.inside_search_bar = False
		
		self.search_bar = tk.Entry(self,textvariable=self.search_var,bg='white',font=('Helvetica',15),
			width=50 ,relief='solid',fg='black')
		self.search_bar.grid(sticky='w',padx=(5,5),ipady=2,column=0)
		self.search_bar.grid_propagate(0)

		self.search_bar.bind("<Button-1>",self.search_click)
							
		self.search_bar.bind("<Return>",self.search_type)

			

		self.b = tk.Button(self,text='Add +',font=('Helvetica',13),width=7,bg='black',fg='white',
			command=self.add_Ac)
		self.b.grid(row=0,column=2,sticky='w')

		self.c = tk.Button(self,text='Edit',font=('Helvetica',13),width=7,bg='black',fg='white',
			command=self.edit_Ac)
		self.c.grid(row=0,column=3,ipady=1,padx=(30))

		self.d= tk.Button(self,text='Delete',font=('Helvetica',13),width=7,bg='black',fg='white',
			command=self.delete_Ac)
		self.d.grid(row=0,column=4,padx=(0,200))

		self.ult_tots_initilize()

		self.new_dict = {}
		self.prev_dic = {}

		self.num_row = tk.StringVar()
		self.num_row.set('Total Rows:'+str(len(maindict)))
		self.Label = tk.Label(self,textvariable=self.num_row,font=('Helvetica',9))
		self.Label.grid(row=0,column=5,padx=(10,10))


		self.obj_main_add = None

	def ult_tots_initilize(self,):
		fame_ = tk.Frame(self,highlightbackground='grey',highlightthickness=2,
			relief='raised',height=30,width=150)
		fame_.grid_propagate(0)
		fame_.grid(row=0,column=6,padx=(20,20))
		self.ult_rem_var = tk.StringVar()
		self.ult_rem_var.set('Rs '+str(ult_rem_tots()))
		self.ult_rem = tk.Label(fame_,width=14,font=('Helvetica',13),textvariable=self.ult_rem_var)
		self.ult_rem.grid(row=0,column=0)
		fame_.rowconfigure(0,weight=1);fame_.columnconfigure(0,weight=1)
		pseudo_frame = tk.Frame(fame_,bg='white')
		pseudo_frame.grid(sticky='nsew',row=0,column=0)
		fame_.bind("<Enter>",lambda e: pseudo_frame.grid_forget())
		fame_.bind("<Leave>",lambda e: pseudo_frame.grid(sticky='nsew',row=0,column=0))

	def search_click(self,*args):
		self.search_var.set('')
		self.x_button = tk.Button(self,text='X',font=('Helvetica',8),bg='lightblue',width=2,fg='red',
			command=self.reverse)
		self.x_button.grid(column=1,row=0,padx=(0,30))
		self.inside_search_bar = True
	
	def search_type(self,event):
		global maindict
		if self.search_var.get() in ("Search Here...",'..','.','/'):
			pass
		if  '/' in self.search_var.get():
			pass
		elif self.search_var.get() == '..e':
			check_for_errors()
		elif self.search_var.get() == '..n':
			all_name_count()
		elif self.search_var.get() == '..an':
			all_name_list()
		elif self.search_var.get() == '..madd':
			self.reverse()
			got_data.mainext(root)


		elif '.' not in self.search_var.get():
			self.new_dict = {}
			try:
				for dict_n in obj_main_table.maindict:
					if self.search_var.get() in obj_main_table.maindict[dict_n]['name'].lower():
						self.new_dict[dict_n] = obj_main_table.maindict[dict_n]
				self.refresh_table(self.new_dict)
				
			except:
				pass
	
	def refresh_table(self,new_dict):
		global obj_main_table
		Main_Canvas.delete('all')
		self.num_row.set('Total Rows:'+str(len(self.new_dict)))
		if new_dict:
			obj_main_table = main_table(Main_Canvas,self.new_dict,scroll_bar)
			obj_main_table.update_table_list()
			obj_main_table.scroll_setting(Main_Canvas)



	def reverse(self):
		global obj_main_table
		self.x_button.destroy()
		self.search_var.set('Search Here...')
		root.focus()
		Main_Canvas.delete('all')
		obj_main_table = main_table(Main_Canvas,maindict,scroll_bar)
		obj_main_table.update_table_list()
		obj_main_table.scroll_setting(Main_Canvas)
		self.num_row.set('Total Rows:'+str(len(maindict)))


	def add_Ac(self):
		if not isinstance(self.obj_main_add, Add_frame):
			self.obj_main_add = Add_frame(Main_Canvas)
			self.obj_main_add.name.focus()
			try:
				self.reverse()
			except:
				pass
		else:
			messagebox.showerror("??",'you have not saved the new account')
		
			


	def edit_Ac(self):
		if  len(obj_main_table.cb_snlist) >= 1:
			c = obj_main_table.cb_snlist[0]
			obj_main_edit = Add_frame(Main_Canvas,edit_frame=True,ch_sn=c)
			obj_main_edit.name.focus()
			try:
				self.reverse()
			except:
				pass

	def delete_Ac(self):
		try:
			self.reverse()
		except:
			pass
		global maindict
		a = 0
		b = 0
		c = 0
		dn_dict = {}
		new_dumpdictx_list = []
		
		try:
			with open(PATH+'/dump_dict.pickle','rb') as ddictList:
				prev_dumpdict_list = pickle.load(ddictList)

			new_dumpdictx_list = prev_dumpdict_list

		except:
			pass

				

		for n in list(maindict.keys()):
			if n in obj_main_table.cb_snlist:		
				
				new_dumpdictx_list.append(maindict[n])

				c += 1

			else:
				dn_dict[b] = maindict[a]
				b += 1

			a += 1

		mbox = tk.messagebox.askokcancel(f"Confirm Delete",f'Are you sure you want to delete {c} accounts',icon='warning')

		if mbox == True:

			with open(PATH+'/dump_dict.pickle','wb') as ddictList2:
				pickle.dump(new_dumpdictx_list,ddictList2)


			store_in_pickle(dn_dict)

			maindict = load_dict()

			Main_Canvas.delete('all')

			main_window_refresh(md = maindict )

			self.ult_tots_initilize()


obj_bottom_frame = bottom_frame(APP_MAINFRAME)



# class edit_frame():
class Add_frame(tk.Frame):
	def __init__(self,parent,edit_frame= False,ch_sn=None,**kwargs):
		super().__init__(parent,width=100,height=20,**kwargs)

		self.place(x=2,y=0)
		self.ch_sn = ch_sn
		
		self.edit_frame = edit_frame
		self.maindict = load_dict()
		if self.maindict == None:
			self.maindict = {}

		root.bind("<Control-x>",lambda a :self.xdestroy())

		self.columnconfigure(0,weight=1)
		xmain_label = tk.Label(self,text="ADD+ Account",font=('Helvetica',14),bg='white',fg='black')
		xmain_label.grid(row=0,column=0,sticky='we')

		tk.Button(self,text='x',font=('Helvetica',10),bg='red',fg='white',height=0,width=3,
			command=self.xdestroy).grid(row=0,column=0,sticky='e',padx=(0,0))

		self.b_frame= tk.Frame(self)
		self.b_frame.grid(row=1,column=0)

		sn_txt_var = tk.IntVar()
		try:
			sn_txt_var.set((list(self.maindict.keys()))[-1]+2)
		except:
			sn_txt_var.set(1)

		self.sn = tk.Label(self.b_frame,textvar=sn_txt_var,width=tablewidthdict['sn']-2,bg='grey',font=('Helvetica',13))
		self.sn.grid(padx=5,pady=4,row=1,column=1,sticky='w')


		self.name_var = tk.StringVar()
		self.name = tk.Entry(self.b_frame,text = 'name',textvariable=self.name_var,
			bg='dark grey',highlightbackground='black',highlightthickness='2',fg='black',
			font=('Helvetica',13),width=tablewidthdict['name'])
		self.name.grid(padx=(0,5),pady=4,row=1,column=2,sticky='w')

		date_frame = tk.Frame(self.b_frame,highlightbackground='black',
			highlightthickness='2',)
		date_frame.grid(padx=15,pady=4,row=1,column=3,sticky='w',)
		self.dyy_var = tk.StringVar()
		self.dyy = tk.Entry(date_frame,width=4,bg='dark grey',font=('Helvetica',13),textvariable=self.dyy_var,fg='black')
		self.dyy.grid(row=0,column=0,padx=(0,2))
		self.dyy.bind("<KeyRelease>",lambda e: self.we_next(4,self.dyy_var,e))

		self.dmm_var = tk.StringVar()
		self.dmm = tk.Entry(date_frame,width=3,bg='dark grey',font=('Helvetica',13),textvariable=self.dmm_var,fg='black')
		self.dmm.grid(row=0,column=1)
		self.dmm.bind("<KeyRelease>",lambda e: self.we_next(2,self.dmm_var,e))

		self.ddd_var = tk.StringVar()
		self.ddd = tk.Entry(date_frame,width=3,bg='dark grey',font=('Helvetica',13),textvariable=self.ddd_var,fg='black',)
		self.ddd.grid(row=0,column=2)
		self.ddd.bind("<KeyRelease>",lambda e: self.we_next(2,self.ddd_var,e))


		self.bvar = tk.StringVar()
		self.bvar.set('Description')
		options = ['usual option','usual option2','usual option3','usually option4']
		bibaranlb = ttk.Combobox(self.b_frame,font=('Helvetica',13),width=15,value=options,textvariable=self.bvar,)
		# bibaranlb.option_add("*Font",('Helvetica',13))
		bibaranlb.grid(row=1,column=4,padx=10)

		pariman_frame = tk.LabelFrame(self.b_frame,highlightbackground='black',
			highlightthickness='2',)
		pariman_frame.grid(padx=10,pady=4,row=1,column=5,sticky='w',)
		self.phr_var = tk.StringVar()
		self.phr = tk.Entry(pariman_frame,width=4,bg='dark grey',font=('Helvetica',13),textvariable=self.phr_var,fg='black',)
		self.phr.grid(row=0,column=0,padx=(0,2))
		self.phr.bind("<KeyRelease>",lambda e: self.we_next(2,self.phr_var,e))

		tk.Label(pariman_frame,text='H',font=('Helvetica',10)).grid(row=0,column=1)
		
		self.phm_var = tk.StringVar()
		self.phm = tk.Entry(pariman_frame,width=3,bg='dark grey',font=('Helvetica',13),textvariable=self.phm_var,fg='black')
		self.phm.grid(row=0,column=2)
		self.phm.bind("<KeyRelease>",lambda e: self.we_next(2,self.phm_var,e))

		tk.Label(pariman_frame,text='M',font=('Helvetica',10)).grid(row=0,column=3)


		self.fee_entry_var = tk.IntVar()
		fee_entry = tk.Entry(self.b_frame,textvariable=self.fee_entry_var,fg='black',
			bg='dark grey',font=('Helvetica',13),width=12)
		fee_entry.grid(padx=(14,0),pady=4,row=1,column=7)

		self.paid_entry_var = tk.IntVar()
		paid_entry = tk.Entry(self.b_frame,textvariable=self.paid_entry_var,bg='dark grey',fg='black',
			font=('Helvetica',13),width=12)
		paid_entry.grid(padx=(20,12),pady=4,row=1,column=8)

		if self.edit_frame == False:
			save_button = tk.Button(self.b_frame,text='Save',width=11,)
			save_button.grid(row=1,column=9)

			Next_button = tk.Button(self.b_frame,text='Save & Next',width=13,command=self._Next)
			Next_button.grid(row=1,padx=(10,4),column=10)

			save_button.config(command=lambda: self._Save())
			Next_button.config(command=lambda: self._Next())
		else:
			save_button = tk.Button(self.b_frame,text='_Save_ ',width=22,command=self._Save)
			save_button.grid(row=1,column=9)

			xmain_label.config(text='Edit- Window')
			sn_txt_var.set(str(self.ch_sn+1))
			self.name_var.set(self.maindict[self.ch_sn]['name'])
			
			self.dyy_var.set(self.maindict[self.ch_sn]['date'][0:4])
			self.dmm_var.set(self.maindict[self.ch_sn]['date'][5:7])
			self.ddd_var.set(self.maindict[self.ch_sn]['date'][8:10])
			self.bvar.set(self.maindict[self.ch_sn]['Discription'])
			self.phr_var.set(self.maindict[self.ch_sn]['time'][0:3])
			self.phm_var.set(self.maindict[self.ch_sn]['time'][4:6])
			self.fee_entry_var.set(self.maindict[self.ch_sn]['fee'])
			self.paid_entry_var.set(self.maindict[self.ch_sn]['paid'])



	def we_next(self,num,xwidide,event):
		if len(xwidide.get()) >= num:
			# root.event_generate('<Tab>')
			xwidide.set(xwidide.get()[0:num])

	def xdestroy(self):
		self.destroy()
		obj_bottom_frame.obj_main_add = False

	def _Save(self): 
		

		if len(self.dyy_var.get()) != 4 or len(self.dmm_var.get())!=2 or len(self.ddd_var.get())!=2:
			self.dyy_var.set('----')
			self.dmm_var.set('--')
			self.ddd_var.set('--')

		if self.bvar.get() == '':
			self.bvar.set('--------')

		if len(self.name_var.get()) >= 3:
			date_frame_var = f"{self.dyy_var.get()}-{self.dmm_var.get()}-{self.ddd_var.get()}"
			pariman_frame_var = "{}h {}m".format(self.phr_var.get(),self.phm_var.get())
			if len(pariman_frame_var) == 3:
				pariman_frame_var = '-------'
			
			# try:
			pseudo_dict ={
							'name': self.name_var.get().title(),
							'date': date_frame_var,
							'Description':self.bvar.get() , 
							'time':pariman_frame_var, 
							'fee': self.fee_entry_var.get(), 
							'paid': self.paid_entry_var.get() , 
							'total': (self.fee_entry_var.get()- (self.paid_entry_var.get()) ),
							'cb': False}
			
			if self.edit_frame == False:
				try:
					n = list(self.maindict.keys())[-1]+1
				except:
					n = 0
			else:
				n = self.ch_sn

			
			self.maindict[n] = pseudo_dict

			store_in_pickle(self.maindict)



			#creating canves in parent_of_main_table 
			Main_Canvas.delete('all')
			main_window_refresh(md = self.maindict)

			# except:
			# 	messagebox.showerror("Add Error",'Enter a proper Account')
		
		else:
			messagebox.showerror("Add Error",'Enter a proper Account')

		self.xdestroy()
		obj_bottom_frame.ult_tots_initilize()

	def _Next(self):
		self._Save()
		self_instance = type(self)(Main_Canvas)
		self_instance.name.focus()





"""////////////////////////////////////////////////////////////////////////////////              """

def main_window_refresh(mc=Main_Canvas,md=maindict,sb=scroll_bar):
	global obj_main_table
	obj_main_table = main_table(mc,md,sb)
	obj_main_table.update_table_list()
	obj_main_table.scroll_setting(Main_Canvas)


main_window_refresh()

"""////////////////////////////////////////////////////////////////////////////////              """
def bind_search_bar(e):
	if root.focus_get() != obj_bottom_frame.search_bar:
		obj_bottom_frame.search_click()
		obj_bottom_frame.search_bar.focus()

	else:
		obj_bottom_frame.reverse()


root.bind("<Control-s>",bind_search_bar)
root.bind("<Control-a>",lambda e:obj_bottom_frame.add_Ac() )

tk.Label(root,text='© Scelester & NineDust',font=('Helvetica',10)).place(x=5,y=(root.winfo_height()-20))








# main loop for
if __name__ == '__main__':
	root.mainloop()