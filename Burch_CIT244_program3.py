# Courtney Burch CIT244 Program 3
# Speeding Ticket Database Progrma

import wx
import sqlite3 as db

class MyDialog(wx.Dialog):
	def __init__(self):
		wx.Dialog.__init__(self, None, title="Dialog Window")
        #form label
		lbl = wx.StaticText(self, label='Ticket Record Entry', pos=(120, 10))

        #input boxes for data
		self.tid = wx.TextCtrl(self, -1, '', pos=(115,40))
		wx.StaticText(self, -1, 'Ticket ID:', pos=(20, 40))

		self.stop_date = wx.TextCtrl(self, -1, '', pos=(115,80))
		wx.StaticText(self, -1, 'Date:', pos=(20, 80))

		self.stop_time = wx.TextCtrl(self, -1, '', pos=(115,120))
		wx.StaticText(self, -1, 'Time:', pos=(20, 120))

		self.actual_speed = wx.TextCtrl(self, -1, '', pos=(115,160))
		wx.StaticText(self, -1, 'Actual Speed:', pos=(20, 160))

		self.posted_speed = wx.TextCtrl(self, -1, '', pos=(115,200))
		wx.StaticText(self, -1, 'Posted Speed', pos=(20, 200))

		self.miles_over = wx.TextCtrl(self, -1, '', pos=(115,240))
		wx.StaticText(self, -1, 'MPH Over:', pos=(20, 240))

		self.age = wx.TextCtrl(self, -1, '', pos=(115,280))
		wx.StaticText(self, -1, 'Age:', pos=(20, 280))
		
		self.violator_sex = wx.TextCtrl(self, -1, '', pos=(115,320))
		wx.StaticText(self, -1, 'Sex:', pos=(20, 320))

		ok_btn = wx.Button(self, id=wx.ID_OK, pos=(115, 350)) 

class DataList(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(620, 270))
        panel = wx.Panel(self, -1) 

        #panel to display database records
        self.table_name = wx.StaticText(panel, -1, 'Tickets', pos=(50, 5))
        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT, pos=(20, 30), size=(600, -1))
        
        self.list.InsertColumn(0, 'tid', width=55)
        self.list.InsertColumn(1, 'stop_date', width=75)
        self.list.InsertColumn(2, 'stop_time', width=75)
        self.list.InsertColumn(3, 'actual_speed', width=90)
        self.list.InsertColumn(4, 'posted_speed', width=90)
        self.list.InsertColumn(5, 'miles_over', width=75)
        self.list.InsertColumn(6, 'age', width=55)
        self.list.InsertColumn(7, 'violator_sex', width=900)

        #buttons to display, insert data, cancel
        display = wx.Button(panel, -1, 'Display', size=(-1, 30), pos=(40, 190))
        insert = wx.Button(panel, -1, 'Insert New Ticket', size=(-1, 30), pos=(160, 190))
        cancel = wx.Button(panel, -1, 'Cancel', size=(-1, 30), pos=(300, 190))

        #bind buttons to functions
        display.Bind(wx.EVT_BUTTON, self.OnDisplay )  
        insert.Bind(wx.EVT_BUTTON, self.OnAdd )
        cancel.Bind(wx.EVT_BUTTON, self.OnCancel)

        self.Centre()

    def getAllData(self):   # function to display the whole table
        #If list control contains data, delete it
        self.list.DeleteAllItems()    
        con = db.connect('speeding_tickets.db')  # connect to db
        cur = con.cursor() #create a cursor
 
        cur.execute('SELECT * FROM tickets') #select all records from tickets table
        results = cur.fetchall()
        for row in results:
            self.list.Append(row)  # add record to list control

        cur.close() #close the cursor
        con.close() #close the connection

    def OnDisplay(self, event):

    	try:
        	self.getAllData()    #display the entire table

    	except lite.Error as error:
        	dlg = wx.MessageDialog(self, str(error), 'An error has occured')
        	dlg.ShowModal()       # display error message

    def OnAdd(self, event):
        dlg = MyDialog()      # create an instance of MyDialog
        btnID = dlg.ShowModal()
        if btnID == wx.ID_OK:
            # get data from input controls on dialog box
            tid = dlg.tid.GetValue()
            stop_date = dlg.stop_date.GetValue()  
            stop_time = dlg.stop_time.GetValue()
            actual_speed = dlg.actual_speed.GetValue()
            posted_speed = dlg.posted_speed.GetValue()
            miles_over = dlg.miles_over.GetValue()
            age = dlg.age.GetValue()
            violator_sex = dlg.violator_sex.GetValue()

        # check that all inputs have values
        if tid != "" and stop_date != "" and stop_time != "" and actual_speed != "" and posted_speed != "" and miles_over != "" and age != "" and violator_sex != "":   

            try:
                con = db.connect('speeding_tickets.db')  # connect to db
                cur = con.cursor() #open a cursor
                #insert data into table
                sql = "INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                #execute querty
                cur.execute(sql, (tid, stop_date, stop_time, actual_speed, posted_speed, miles_over, age, violator_sex))
                con.commit()          

                self.getAllData()     # display all data

            except db.Error as error:
                dlg = wx.MessageDialog(self, str(error), 'An error occured')
                dlg.ShowModal()        # display error message

        dlg.Destroy()

    def OnCancel(self, event):
        self.Close()  # exit program

app = wx.App()
dl = DataList(None, -1, 'Insert Into List Control')
dl.Show()
app.MainLoop()
