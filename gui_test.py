import tkinter as tk
import tkinter.messagebox as box
import pandas as pd 
import numpy as np 
import yfinance as yf
from datetime import date
import time
from yahoo_fin import stock_info as si
import sys, os

base_pth=os.path.dirname(__file__)
if ((os.path.exists(base_pth+"/HTL"))==False):
	os.mkdir(base_pth+"/HTL")

class SampleApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.title("Radiant World")
		self.resizable(width=False, height=False)
		self.iconbitmap(base_pth+"/rw.ico")
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
		try:
			si.get_live_price(self.tckr)
		except:
			box.showinfo('Info','The Ticker is invalid, Please check yahoo finance!')
			return()
		self.qty=self.e_qty.get()
		self.op=float(self.e_bpr.get())
		self.bnm=self.e_bnm.get().upper()
		self.clid=self.e_cid.get()
		self.date=date.today()
		self.typ=self.e_typ.get()

		#The names of each column are known beforehand
		#File name declration follows below
		file_tl=base_pth+"/HTL/TL_"+self.clid+".csv"
		file_hl=base_pth+"/HTL/HL_"+self.clid+".csv"

		#Read the file if available otherwise head on to create new file
		try:
			df_tl=pd.read_csv(file_tl)
			df_hl=pd.read_csv(file_hl)
			col_hl=df_hl.columns
			col_tl=df_tl.columns
			serial=df_hl.Serial.iloc[-1]+1
			templs_hl=pd.DataFrame(np.array([serial,self.date,self.bnm.upper(),self.clid.upper(),self.typ.upper()\
				,self.tckr.upper(),self.qty,self.op,np.nan,np.nan,np.nan,np.nan]).reshape(1,-1),columns=col_hl)
			templs_tl=pd.DataFrame(np.array([serial,self.date,self.bnm.upper(),self.clid.upper(),self.typ.upper()\
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
			serial=0
			box.showinfo('Info','New Client Entry!')
			col_hl=["Serial","Entry Date","Bank","Client ID","Type","Ticker","Qty",\
			"Open Price","P&L","AB%","Gross Amount","Brokerage"]
			col_tl=["Serial","Entry Date","Bank","Client ID",\
			"Type","Ticker","Open Qty","Open Price"\
			,"Gross Amount","Brokerage"]
			templs_tl=pd.DataFrame(np.array([serial,self.date,self.bnm.upper(),self.clid.upper(),self.typ.upper()\
				,self.tckr.upper(),self.qty,self.op,np.nan,np.nan]).reshape(1,-1),columns=col_tl)
			templs_hl=pd.DataFrame(np.array([serial,self.date,self.bnm.upper(),self.clid.upper(),self.typ.upper()\
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
		self.clid=self.e_cid.get().upper()
		self.cdate=date.today()

		#The names of each column are known beforehand
		#File name declration follows below
		file_hl="HTL/HL_"+self.clid+".csv"

		#Read the file if available otherwise head on to create new file
		try:
			df_hl=pd.read_csv(file_hl)
			col_hl=df_hl.columns
			file_tlc="HTL/TLC_"+self.clid+".csv"
			total_cur=df_hl[(df_hl.Ticker==self.tckr)&(df_hl.Bank==self.bnm)]
			if total_cur.Qty.sum()==0:
				box.showinfo('Info','No Such Entry in the Holdings left!')
				return()
			if float(self.cqty)>total_cur["Qty"].sum():
				box.showinfo('Info','Closing Quantity is larger than units in holding!')
				return()
			try:
				df_tlc=pd.read_csv(file_tlc)
				col_tlc=df_tlc.columns
			except:
				box.showinfo('Info','New Closing Position')
				col_tlc=["Entry Date","Closing Date","Bank","Client ID",\
				"Stocks","Close Qty","Open Price","Close Price"\
				,"Gross Amount","Brokerage","Realized P&L"]
				df_tlc = pd.DataFrame(columns=col_tlc)
			finally:
				#Arrange all stock corresponding to the ticker date-wise
				total_cur=total_cur.sort_values(by=['Serial'])
				#Evaluate the cumulative sum vector
				temp_cum=total_cur["Qty"].cumsum()
				#Compare and evaluate the vector with boolean entries
				temp_bool=temp_cum<float(self.cqty)
				#Append additonal boolean entry to create the proper vector
				temp_bool=np.r_[True,temp_bool[:-1]]
				#Remove all the entries till the last boolean from the holdings file 
				#and update them in TLC
				temp_sum=0
				#check_val checks the number of boolean 1's. In case only single True values is
				#present, proceed to run a single time procedure
				check_val=len(temp_bool[temp_bool])-1
				if check_val==0:
					temp_left=float(self.cqty)

					#Removing the last entry from the holding files
					temp_val=df_hl.Qty[(df_hl.Bank==self.bnm) & (df_hl.Ticker==self.tckr.upper())\
						&(df_hl["Serial"]==float(total_cur["Serial"]))]
					df_hl["Qty"][(df_hl.Bank==self.bnm) & (df_hl.Ticker==self.tckr.upper())\
						&(df_hl["Serial"]==float(total_cur["Serial"]))]=temp_val-temp_left
					real_pl=(float(self.cp)-total_cur["Open Price"])/total_cur["Open Price"]
					templs_tlc=pd.DataFrame(np.array([total_cur["Entry Date"],self.cdate,self.bnm.upper(),\
							self.clid.upper(),self.tckr.upper(),temp_left,\
							total_cur["Open Price"],self.cp,np.nan,np.nan,real_pl]).reshape(1,-1),columns=col_tlc)
					df_tlc=df_tlc.append(templs_tlc)

				else:
					for itera in range(len(temp_bool[temp_bool])-1):
						df_hl=df_hl.drop(df_hl[df_hl.Serial==total_cur.Serial[itera]].index)
						real_pl=(float(self.cp)-total_cur["Open Price"][itera])/total_cur["Open Price"][itera]
						templs_tlc=pd.DataFrame(np.array([total_cur["Entry Date"][itera],self.cdate,self.bnm.upper(),\
							self.clid.upper(),self.tckr.upper(),total_cur.Qty[itera],\
							total_cur["Open Price"][itera],self.cp,np.nan,np.nan,real_pl]).reshape(1,-1),columns=col_tlc)
						temp_sum+=total_cur.Qty[itera]
						df_tlc=df_tlc.append(templs_tlc)
					temp_left=float(self.cqty)-temp_sum
					#Removing the last entry from the holding files
					temp_val=df_hl.Qty[(df_hl.Bank==self.bnm) & (df_hl.Ticker==self.tckr.upper())\
						&(df_hl["Serial"]==total_cur["Serial"][itera+1])]
					df_hl["Qty"][(df_hl.Bank==self.bnm) & (df_hl.Ticker==self.tckr.upper())\
						&(df_hl["Serial"]==total_cur["Serial"][itera+1])]=temp_val-temp_left
					real_pl=(float(self.cp)-total_cur["Open Price"][itera+1])/total_cur["Open Price"][itera+1]
					templs_tlc=pd.DataFrame(np.array([total_cur["Entry Date"][itera+1],self.cdate,self.bnm.upper(),\
							self.clid.upper(),self.tckr.upper(),temp_left,\
							total_cur["Open Price"][itera+1],self.cp,np.nan,np.nan,real_pl]).reshape(1,-1),columns=col_tlc)
					df_tlc=df_tlc.append(templs_tlc)


		#In case the file is already open, request to close
				try:
					df_tlc.to_csv(file_tlc,index=False)
					df_hl.to_csv(file_hl,index=False)
					box.showinfo('Info','Close Position Registered')
				except:
					box.showinfo('Info','Please Close All Files')
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(e,exc_type, fname, exc_tb.tb_lineno)
			box.showinfo('Info','No such client exist')
			return()
			


class Summary(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		master.title("Radiant World")
		tk.Label(self, text='Ticker:').grid(row=0, column=0)
		self.e_tckr_sum=tk.Entry(self,bd =5)
		self.e_tckr_sum.grid(row=0, column=1)
		tk.Button(self, text="View",
		  command=self.prep_sum).grid(row=1,column=0)
		tk.Button(self, text="Go Back",
		  command=lambda: master.switch_frame(Entr_summ)).grid(row=1,column=1)
	def prep_sum(self):
		global sum_tckr
		sum_tckr=self.e_tckr_sum.get().upper()
		self.master.switch_frame(Summ_win)


class Summ_win(tk.Frame):
	"""Make a New open entry Window"""
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		master.title(sum_tckr)
		self.sum_tckr=sum_tckr
		temp_sum=0
		col_nm=["Serial","Entry Date","Bank","Client ID","Type","Qty","Open Price",\
		"Current Price","% Price","Notional P/L","Average Price","Exposure","% Exposure","Total Qty"]
		df_hl_temp=pd.DataFrame(columns=col_nm)
		#Find all the holding files
		for file in os.listdir(base_pth+"/HTL"):
			if file.startswith("HL_"):
				df_temp=pd.read_csv("HTL/"+file)
				#Check if the holding is non empty
				temp_qty=df_temp.Qty[df_temp.Ticker==self.sum_tckr]
				if (temp_qty.sum()>0):
					#Record the number of non zero holdings
					temp_sum+=temp_qty.sum()
					temp_df=df_temp[df_temp.Ticker==self.sum_tckr]
					df_hl_temp=df_hl_temp.append(temp_df.drop(columns="Ticker"))
		if temp_sum==0:
			box.showinfo("Info",'No Entry Exist')
			tk.Button(self, text="Go Back",
			  command=lambda: master.switch_frame(Summary)).grid(row=1,column=1)
		else:
			for k in range(7):
				for j in range(df_hl_temp.shape[0]):
					tk.Label(self, text=col_nm[k],bg="yellow",font="bold",relief="solid").grid(row=0, column=k)
					tk.Label(self, text=df_hl_temp[col_nm[k]][j]).grid(row=j+1, column=k)
			tk.Label(self, text=col_nm[-7],bg="yellow",font="bold",relief="solid").grid(row=0, column=len(col_nm)-6)
			tk.Label(self, text=col_nm[-6],bg="yellow",font="bold",relief="solid").grid(row=0, column=len(col_nm)-5)
			tk.Label(self, text=col_nm[-5],bg="yellow",font="bold",relief="solid").grid(row=0, column=len(col_nm)-4)
			tk.Label(self, text=col_nm[-4],bg="yellow",font="bold",relief="solid").grid(row=0, column=len(col_nm)-3)
			tk.Label(self, text=col_nm[-3],bg="yellow",font="bold",relief="solid").grid(row=0, column=len(col_nm)-2)
			tk.Label(self, text=col_nm[-2],bg="yellow",font="bold",relief="solid").grid(row=0, column=len(col_nm)-1)
			tk.Label(self, text=col_nm[-1],bg="yellow",font="bold",relief="solid").grid(row=0, column=len(col_nm))
			# while(True):
			cur_val=si.get_live_price(self.sum_tckr)
			for i in range(df_hl_temp.shape[0]):
				df_hl_temp["Current Price"][i]=cur_val
				df_hl_temp["% Price"][i]=100*((-1*float(df_hl_temp["Open Price"][i])\
					+cur_val)/float(df_hl_temp["Open Price"][i]))
				df_hl_temp["Notional P/L"][i]=(-1*float(df_hl_temp["Open Price"][i])\
					+cur_val)*df_hl_temp.Qty[i]
			temp_sign=np.sign(df_hl_temp["Notional P/L"])
			temp_sign[temp_sign==-1]="red"
			temp_sign[temp_sign==1]="green"
			temp_sign[temp_sign==0]="grey"

			avg_price=df_hl_temp["Open Price"].mean()
			expo=np.dot(df_hl_temp["Current Price"],df_hl_temp["Qty"])
			per_exp=(100*((df_hl_temp["Current Price"]*df_hl_temp["Qty"])/expo)).sum()
			qty_total=df_hl_temp["Qty"].sum()

			for j in range(df_hl_temp.shape[0]):
				col=temp_sign[j]
				tk.Label(self, text=round(df_hl_temp["Notional P/L"][j],3),bg=col).grid(row=j+1, column=len(col_nm)-4)
				tk.Label(self, text=df_hl_temp["% Price"][j]).grid(row=j+1, column=len(col_nm)-5)
				tk.Label(self, text=df_hl_temp["Current Price"][j]).grid(row=j+1, column=len(col_nm)-6)
			tk.Label(self, text=avg_price).grid(row=np.int(df_hl_temp.shape[0]/2)+1, column=len(col_nm)-3)
			tk.Label(self, text=expo).grid(row=np.int(df_hl_temp.shape[0]/2)+1, column=len(col_nm)-2)
			tk.Label(self, text=per_exp).grid(row=np.int(df_hl_temp.shape[0]/2)+1, column=len(col_nm)-1)
			tk.Label(self, text=qty_total).grid(row=np.int(df_hl_temp.shape[0]/2)+1, column=len(col_nm))
			tk.Button(self, text="Go Back",
			  command=lambda: master.switch_frame(Summary)).grid(row=df_hl_temp.shape[0]+1,column=1)

app = SampleApp()
app.mainloop()