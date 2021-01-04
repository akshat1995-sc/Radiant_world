import tkinter as tk
import tkinter.messagebox as box
import pandas as pd 
import numpy as np 
import yfinance as yf
from datetime import date
from yahoo_fin import stock_info as si


class SampleApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.title("Radiant World")
		self.iconbitmap("rw.ico")
		self._frame = None
		self.switch_frame(Login)

	def switch_frame(self, frame_class):
		new_frame = frame_class(self)
		if self._frame is not None:
		    self._frame.destroy()
		self._frame = new_frame
		self._frame.pack()



class Login(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		tk.Label(self, text='Username:').grid(row=0, column=0)
		self.entry1=tk.Entry(self,bd =5)
		self.entry1.grid(row=0, column=1)
		tk.Label(self, text='Password:').grid(row=1, column=0)
		self.entry2=tk.Entry(self, show="*",bd =5)
		self.entry2.grid(row=1, column=1)
		btn=tk.Button(self,text = 'Login',command = self.proceed).grid(row=3,column=1)

	def proceed(self):
		username=self.entry1.get()
		password = self.entry2.get()
		if (username == 'admin' and  password == 'admin'):
			self.master.switch_frame(Entr_summ)
		else:
			box.showinfo('info','Invalid Login')

class Entr_summ(tk.Frame):
	"""Main Navigation Window"""
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		tk.Button(self, text="Log out",
		          command=lambda: master.switch_frame(Login)).grid(row=0,column=0)
		tk.Button(self, text="Open Position",
		  command=lambda: master.switch_frame(Open)).grid(row=0,column=1)
		tk.Button(self, text="Close Position",
		  command=lambda: master.switch_frame(Close)).grid(row=0,column=2)
		tk.Button(self, text="Summary",
		  command=lambda: master.switch_frame(Summary)).grid(row=0,column=3)

class Open(tk.Frame):
	"""Make a New open entry Window"""
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		tk.Label(self, text='Ticker:').grid(row=0, column=0)
		self.e_tckr=tk.Entry(self,bd =5)
		self.e_tckr.grid(row=0, column=1)
		tk.Label(self, text='Qty:').grid(row=1, column=0)
		self.e_qty=tk.Entry(self,bd =5)
		self.e_qty.grid(row=1, column=1)
		tk.Label(self, text='Buying Price:').grid(row=2, column=0)
		self.e_bpr=tk.Entry(self,bd =5)
		self.e_bpr.grid(row=2, column=1)
		tk.Label(self, text='Bank Name:').grid(row=3, column=0)
		self.e_bnm=tk.Entry(self,bd =5)
		self.e_bnm.grid(row=3, column=1)
		tk.Label(self, text='Client ID:').grid(row=4, column=0)
		self.e_cid=tk.Entry(self,bd =5)
		self.e_cid.grid(row=4, column=1)
		tk.Label(self, text='Type:').grid(row=5, column=0)
		self.e_typ=tk.Entry(self,bd =5)
		self.e_typ.grid(row=5, column=1)
		tk.Button(self, text="Make Entry",
		  command=self.update).grid(row=6,column=0)
		tk.Button(self, text="Go Back",
		  command=lambda: master.switch_frame(Entr_summ)).grid(row=6,column=1)

	def update(self):
		"""Updating button's operation"""
		self.tckr=self.e_tckr.get().lower()
		self.qty=self.e_qty.get()
		self.op=float(self.e_bpr.get())
		self.bnm=self.e_bnm.get().upper()
		self.clid=self.e_cid.get()
		self.date=date.today()
		self.typ=self.e_typ.get()

		#The names of each column are known beforehand
		#File name declration follows below
		file_tl="HTL/TL_"+self.clid+".csv"
		file_hl="HTL/HL_"+self.clid+".csv"

		#Read the file if available otherwise head on to create new file
		try:
			df_tl=pd.read_csv(file_tl)
			df_hl=pd.read_csv(file_hl)
			col_hl=df_hl.columns
			col_tl=df_tl.columns
			templs_hl=pd.DataFrame(np.array([self.date,self.bnm.upper(),self.clid.upper(),self.typ.upper()\
				,self.tckr.upper(),self.qty,self.op,np.nan,np.nan,np.nan,np.nan]).reshape(1,-1),columns=col_hl)
			# temp_val=df_hl.Qty[(df_hl.Bank==self.bnm) & (df_hl.Ticker==self.tckr.upper())].sum()
			# df_hl["Qty"].loc[(df_hl.Bank==self.bnm) & (df_hl.Ticker==self.tckr.upper())]=float(temp_val)+float(self.qty)
			templs_tl=pd.DataFrame(np.array([self.date,self.bnm.upper(),self.clid.upper(),self.typ.upper()\
				,self.tckr.upper(),self.qty,self.op,np.nan,np.nan]).reshape(1,-1),columns=col_tl)
			df_tl=df_tl.append(templs_tl)
			df_hl=df_hl.append(templs_hl)
			try:
				df_tl.to_csv(file_tl,index=False)
				df_hl.to_csv(file_hl,index=False)
				box.showinfo('Info','Open Position Registered')
			except:
				box.showinfo('Info','Please Close All Files')

		except:
			box.showinfo('Info','New Client Entry!')
			col_hl=["Entry Date","Bank","Client ID","Type","Ticker","Qty",\
			"Open Price","P&L","AB%","Gross Amount","Brokerage"]
			col_tl=["Entry Date","Bank","Client ID",\
			"Type","Ticker","Open Qty","Open Price"\
			,"Gross Amount","Brokerage"]
			templs_tl=pd.DataFrame(np.array([self.date,self.bnm.upper(),self.clid.upper(),self.typ.upper()\
				,self.tckr.upper(),self.qty,self.op,np.nan,np.nan]).reshape(1,-1),columns=col_tl)
			templs_hl=pd.DataFrame(np.array([self.date,self.bnm.upper(),self.clid.upper(),self.typ.upper()\
				,self.tckr.upper(),self.qty,self.op,np.nan,np.nan,np.nan,np.nan]).reshape(1,-1),columns=col_hl)
			templs_tl.to_csv(file_tl,index=False)
			templs_hl.to_csv(file_hl,index=False)



class Close(tk.Frame):
	"""Make a New open entry Window"""
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		tk.Label(self, text='Ticker:').grid(row=0, column=0)
		self.e_tckr=tk.Entry(self,bd =5)
		self.e_tckr.grid(row=0, column=1)
		tk.Label(self, text='Close Qty:').grid(row=1, column=0)
		self.e_qtyc=tk.Entry(self,bd =5)
		self.e_qtyc.grid(row=1, column=1)
		tk.Label(self, text='Close Price:').grid(row=2, column=0)
		self.e_cpr=tk.Entry(self,bd =5)
		self.e_cpr.grid(row=2, column=1)
		tk.Label(self, text='Bank Name:').grid(row=3, column=0)
		self.e_bnm=tk.Entry(self,bd =5)
		self.e_bnm.grid(row=3, column=1)
		tk.Label(self, text='Client ID:').grid(row=4, column=0)
		self.e_cid=tk.Entry(self,bd =5)
		self.e_cid.grid(row=4, column=1)
		tk.Button(self, text="Close Position",
		  command=self.closep).grid(row=5,column=0)
		tk.Button(self, text="Go Back",
		  command=lambda: master.switch_frame(Entr_summ)).grid(row=5,column=1)

	def closep(self):
		"""Close position button's operation. Entry should be there in both TL and HL"""
		self.tckr=self.e_tckr.get().upper()
		self.cqty=self.e_qtyc.get()
		self.cp=float(self.e_cpr.get())
		self.bnm=self.e_bnm.get().upper()
		self.clid=self.e_cid.get()
		self.cdate=date.today()

		#The names of each column are known beforehand
		#File name declration follows below
		file_tl="HTL/TL_"+self.clid+".csv"
		file_hl="HTL/HL_"+self.clid+".csv"

		#Read the file if available otherwise head on to create new file
		try:
			df_tl=pd.read_csv(file_tl)
			df_hl=pd.read_csv(file_hl)
			col_hl=df_hl.columns
			col_tl=df_tl.columns
			total_cur=df_hl[(df_hl.Stocks==self.tckr)&(df_hl.Bank==self.bnm)]
			if self.cqty>total_cur["Qty"].sum():
				box.showinfo('Info','Closing Quantity is larger than units in holding!')
				return()
			total_cur=total_cur.sort_values(by=['Entry Date'])
			temp_cum=total_cur["Qty"].cumsum()
			temp_bool=temp_cum<self.cqty
			temp_bool=total_cur[np.r_[True,temp_bool[:-1]]]
			for itera in range(len(temp_bool[temp_bool==True])):
				lval=self.cqty-total_cur.Qty[itera]
				templs_tlc=pd.DataFrame(np.array([self.date,np.nan,self.bnm.upper(),self.clid.upper(),self.tckr.upper()\
					,self.qty,np.nan,self.op,np.nan,np.nan,np.nan]).reshape(1,-1),columns=col_tl)
			temp_val=df_hl.Qty[(df_hl.Bank==self.bnm) & (df_hl.Stocks==self.tckr.upper())]
			df_hl["Qty"].iloc[(df_hl.Bank==self.bnm) & (df_hl.Stocks==self.tckr.upper())]=temp_val-self.cqty
		except:
			box.showinfo('Info','No such client exist')
			return()
		else:
			file_tlc="HTL/TLC_"+self.clid+".csv"
			try:
				df_tlc=pd.read_csv(file_tlc)
				col_tlc=df_tlc.columns
				nf=True
			except:
				box.showinfo('Info','New Closing Position')
				col_tlc=["Entry Date","Closing Date","Bank","Client ID",\
				"Stocks","Close Qty","Open Price","Close Price"\
				,"Gross Amount","Brokerage"]
				nf=False
			else:
				templs_tlc=pd.DataFrame(np.array([self.date,np.nan,self.bnm.upper(),self.clid.upper(),self.tckr.upper()\
					,self.qty,np.nan,self.op,np.nan,np.nan,np.nan]).reshape(1,-1),columns=col_tl)
			if not nf:
				df_tlc=df_tl.append(templs_tlc)


		#In case the file is already open, request to close
			try:
				df_tlc.to_csv(file_tl,index=False)
				df_hl.to_csv(file_hl,index=False)
			except:
				box.showinfo('Info','Please Close All Files')

			box.showinfo('Info','Close Position Registered')

class Summary(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		tk.Label(self, text='Ticker:').grid(row=0, column=0)
		self.e_tckr_sum=tk.Entry(self,bd =5)
		self.e_tckr_sum.grid(row=0, column=1)
		tk.Button(self, text="View",
		  command=lambda: master.switch_frame(Login)).grid(row=1,column=0)
		tk.Button(self, text="Go Back",
		  command=lambda: master.switch_frame(Entr_summ)).grid(row=1,column=1)


# window = Tk()
# window.title('Radiant World')

# frame = Frame(window)

# Label1 = Label(window,text = 'Username:')
# Label1.pack(padx=15,pady= 5)

# entry1 = Entry(window,bd =5)
# entry1.pack(padx=15, pady=5)


# Label2 = Label(window,text = 'Password: ')
# Label2.pack(padx = 15,pady=6)

# entry2 = Entry(window, bd=5)
# entry2.pack(padx = 15,pady=7)


# btn = Button(frame, text = 'Check Login',command = dialog1)


# btn.pack(side = RIGHT , padx =5)
# frame.pack(padx=100,pady = 19)
# window.mainloop()
app = SampleApp()
app.mainloop()