import tkinter as tk
import os, pickle
from tkinter import messagebox, filedialog
import pandas as pd




class mainext():
	def __init__(self,parent):

		self.PATH = os.path.dirname(__file__)

		self.main = tk.Toplevel(parent)
		self.main.title('Exel data extractor')
		self.main.geometry('400x400+500+150')
		self.main.grab_set()
		self.parent = parent
		
		try:
			self.main.lift()
		except:
			pass
	    	

		self.but1 = tk.Button(self.main,
			text='Open File',font=15,bg='black',fg='white',
			command=self.button_click)
		self.but1.pack(pady=20)

		self.but1.focus()


		self.l1_var = tk.StringVar()
		self.l1_var.set('No file selected')
		l1 = tk.Label(self.main,textvariable=self.l1_var,
		 relief="solid",width=4,font=20)
		l1.pack(fill='x',padx=20)



		self.entframe= tk.Frame(self.main)
		self.entframe.pack(pady=(40,20),fill='both',padx=(30,0))

		self.ent1label = tk.Label(self.entframe,text='sheet_number:',font=40)
		self.ent1label.grid(row = 1,pady=10)
		self.ent1_var = tk.IntVar()
		self.ent1 = tk.Entry(self.entframe,textvariable=self.ent1_var,font=40)
		self.ent1.grid(row=1,column=2)

		self.ent2label = tk.Label(self.entframe,text='First Comlumn:',font=40)
		self.ent2label.grid(row = 2,pady=10)
		self.ent2_var = tk.StringVar()
		self.ent2 = tk.Entry(self.entframe,textvariable=self.ent2_var,font=40)
		self.ent2.grid(row=2,column=2)

		self.ent3label = tk.Label(self.entframe,text='Last Comlumn:',font=40)
		self.ent3label.grid(row = 3,pady=(10,0))
		self.ent3_var = tk.StringVar()
		self.ent3 = tk.Entry(self.entframe,textvariable=self.ent3_var,font=40)
		self.ent3.grid(row=3,column=2)

		self.ent4label = tk.Label(self.entframe,text='Start Rows:',font=40)
		self.ent4label.grid(row = 4,pady=(10,0))
		self.ent4_var = tk.IntVar()
		self.ent4 = tk.Entry(self.entframe,textvariable=self.ent4_var,font=40)
		self.ent4.grid(row=4,column=2)

		self.ent5label = tk.Label(self.entframe,text='End Row:',font=40)
		self.ent5label.grid(row = 5,pady=(10,0))
		self.ent5_var = tk.IntVar()
		self.ent5 = tk.Entry(self.entframe,textvariable=self.ent5_var,font=40)
		self.ent5.grid(row=5,column=2)



		self.okbut = tk.Button(self.main,text='Done',font=40,width=10,command=self.Ok)
		self.okbut.pack(side='right',padx=40,pady=10)

		self.main.mainloop()


	def button_click(self):
		self.filename = filedialog.askopenfilename(title='Select File',
			filetypes=( ("xlsx files", "*.xlsx"), )  )

		self.l1_var.set(self.filename)
		if self.l1_var.get() == '':
			self.l1_var.set('No file selected')

		
		

	# spread sheet stuff
	def exel_stuff(self,filename):
		xl_file = pd.read_excel(filename,
			usecols=f"{self.ent2_var.get()}:{self.ent3_var.get()}")

		try:
			with open(self.PATH+'/main_dict.pickle','rb') as dictx:
				xd = pickle.load(dictx)
				sn = len(xd)
		except EOFError:
			xd= {}
			sn = 0

		start_row = int(self.ent4_var.get())-1
		end_row = int(self.ent5_var.get())
		

		for n in range(start_row,end_row):

			f_list = []
			
			for m in xl_file:
				d = xl_file[m][n]
				
				if list(xl_file).index(m) == 1:
					d = str(d)
					if len(d) >= 12:
						d = d[0:11]

					f_list.append(d)

				else:
					if str(d) not in ('nan','NaT'):
						f_list.append(d)
					else:
						if list(xl_file).index(m) in (4,5,6):
							f_list.append(0)
						else:
							f_list.append('')
			
			if len(f_list) < 7:
				totssum = int(f_list[4]) + int(float(f_list[5]))
				f_list.append([totssum])

			pseudo_dict ={'name': f_list[0].title(),
							 'date':f_list[1],
							 'Description':f_list[2] , 
							 'time':f_list[3], 
							 'fee': int(f_list[4]), 
							 'paid': int(float(f_list[5])),
							 'total': int(float(f_list[6])),
							  'cb': False}

			xd[sn] = pseudo_dict

			with open(self.PATH+'\\main_dict.pickle','wb') as dumpdictx:
				pickle.dump(xd,dumpdictx)

			sn += 1

		self.parent.destroy()






	def Ok(self):

		get_list = [self.ent1_var,self.ent2_var,self.ent3_var,self.ent4_var,self.ent5_var]
		results = any([i for i in get_list if i.get() == ''])

		if self.l1_var.get() == 'No file selected' :
			messagebox.showerror("Error",'No File Selected.')

		elif results:
			messagebox.showerror("Error",'Row or Column Entry cannot be empty.')
		
		else:
			mbox = tk.messagebox.askokcancel(f"Confirm",f'Are you sure you want to add accounts from following location'
				+'This will close the program.(Restart again)',icon='warning')
			
			if mbox == True:
				self.exel_stuff(self.filename)
