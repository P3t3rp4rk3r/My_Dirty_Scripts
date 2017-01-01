#!/usr/bin/python3
__author__ = "Santhosh Baswa"

# standard libraries
import sys
import tkinter
import webbrowser

# BW libraries
from rssdb import rssDB
from rss import RSS

# for exception symbols
import sqlite3
import urllib
import xml.parsers.expat

TITLE = 'RSS Sandbox' 

class hyperlinkManager:
    ''' manager for hyperlinks in tk text widgets '''
    def __init__(self, text):
        self.text = text
        self.text.tag_bind('hyper', '<Enter>', self._enter)
        self.text.tag_bind('hyper', '<Leave>', self._leave)
        self.text.tag_bind('hyper', '<Button-1>', self._click)
        self.links = {}

    def add(self, url):
        ''' 
            add an action to the manager.
            return tags to use in text wiget
        '''
        tag = 'hyper-{}'.format(len(self.links))
        self.links[tag] = url
        return 'hyper', tag

    def _enter(self, event):
        self.text.config(cursor='hand2')    # set the cursor ('hand2' is standard, 'trek' is fun)

    def _leave(self, event):
        self.text.config(cursor='')         # cursor back to standard

    def _click(self, event):
        for tag in self.text.tag_names(tkinter.CURRENT):
            if tag[:6] == 'hyper-':
                webbrowser.open(self.links[tag])
                break

class mainWindow(tkinter.Frame):
    def __init__(self, master = None, **kwargs):
        tkinter.Frame.__init__(self, master)
        self._db = rssDB()
        self.master.title( TITLE )
        self.createWidgets()
        self.grid()

    def createWidgets(self):
        # default font
        self.defaultFont = ('Helvetica', '16', 'roman')

        # URL text box
        self.labelURL = tkinter.Label(text = 'URL')
        self.varURL = tkinter.StringVar()
        self.entryURL = tkinter.Entry(textvariable = self.varURL, width = 40)
        self.buttonURLGo = tkinter.Button (text = 'Go', command = self.go)
        self.buttonAdd = tkinter.Button (text = 'Add', command = self.addFeed)

        # Listbox for feeds
        self.listBox = tkinter.Listbox()
        self.buttonListGo = tkinter.Button (text = 'Go', command = self.listGo)
        self.buttonListDel = tkinter.Button (text = 'Del', command = self.listDel)
        self.listBox.grid(row = 2, column = 0, rowspan = 4, columnspan = 2, padx = 10, pady = 3)

        # scrollbar for listBox - must have same grid options as listBox
        self.textScroll = tkinter.Scrollbar(self.master)
        self.textScroll.grid(row = 2, column = 0, columnspan = 2, rowspan = 4, pady = 3, sticky='nse')
        self.textScroll.config(command=self.listBox.yview)
        self.listBox.config(yscrollcommand=self.textScroll.set)

        # fill the listbox from the database
        self.fillListBox()

        # set up the rest of the grid
        self.labelURL.grid(row = 0, column = 0, sticky = 'e')
        self.entryURL.grid(row = 0, column = 1, pady = 3) 
        self.buttonURLGo.grid(row = 0, padx = 2, column = 2)
        self.buttonAdd.grid(row = 0, padx = 2, column = 3)
        self.buttonListDel.grid(row = 4, column = 2, padx = 2, sticky = 'sw')
        self.buttonListGo.grid(row = 4, column = 3, padx = 2, sticky = 'sw')

    def fillListBox(self):
        self._db_index = [];
        self.listBox.config(listvariable = tkinter.StringVar(), width = 40)
        for r in self._db.list():
            self.listBox.insert(tkinter.END, r['title'])
            self._db_index.append(str(r['id']))
        
    def go(self, url = None):
        if url is None: url = self.varURL.get()

        contentWindow = tkinter.Toplevel()
        textContainer = tkinter.Text(contentWindow, wrap = 'word', height = 25, width = 100)
        contentClose = tkinter.Button(contentWindow, text = 'Close', command = contentWindow.destroy)

        textContainer.tag_add('default', '0.0')
        textContainer.tag_config('default', font = self.defaultFont)
        textContainer.tag_config('hyper', foreground='blue', underline = 1, font = self.defaultFont)

        contentWindow.title('RSS Feed')
        contentWindow.grid()
        textContainer.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)
        contentClose.grid(row = 1, column = 1, pady = 5)

        # scrollbar for textContainer - must have same grid options as parent
        textScroll = tkinter.Scrollbar(contentWindow)
        textScroll.grid(row = 0, column = 0, columnspan = 2, sticky='nse')
        textScroll.config(command=textContainer.yview)
        textContainer.config(yscrollcommand=textScroll.set)

        hyperlink = hyperlinkManager(textContainer)

        try: 
            feedString = ''
            feed = RSS(url)
            contentWindow.title(feed.feedTitle)
            separator = '--------------------\n'
            for r in feed.records():
                textContainer.insert(tkinter.INSERT, separator, 'default')
                if ['title'] and r['link']:
                    textContainer.insert(tkinter.INSERT, r['title'] + '\n', hyperlink.add(r['link'])) 
                else:
                    if r['title']: textContainer.insert(tkinter.INSERT, r['title'] + '\n', 'default')
                    if r['link']: textContainer.insert(tkinter.INSERT, r['title'] + '\n', hyperlink.add(r['link']))
                if r['description']: textContainer.insert(tkinter.INSERT, r['description'] + '\n', 'default')

        except urllib.error.HTTPError as e: self.errorBox(e, contentWindow.destroy)
        except urllib.error.URLError as e: self.errorBox(e, contentWindow.destroy)
        except ValueError as e:
            if url: self.errorBox(e, contentWindow.destroy)
            else: contentWindow.destroy()
        except xml.parsers.expat.ExpatError as e: self.errorBox(e, contentWindow.destroy)

    def listGo(self):
        try: recno = self.listBox.curselection()[0]
        except: self.errorBox('No feed selected')
        else: 
            rec = self._db.getById(self._db_index[int(recno)])
            self.varURL.set('')
            self.go(rec['url'])

    def listDel(self):
        recno = self.listBox.curselection()[0]
        itemText = self.listBox.get(recno)
        self._db.delById(self._db_index[int(recno)])
        self.fillListBox()
        self.messageBox('Deleted from list: {}.'.format(itemText))

    def addFeed(self):
        url = self.varURL.get()
        try:
            feed = RSS(url)
            rec = {
                'title': feed.feedTitle.strip(),
                'url': url.strip(),
                'description': feed.feedDescription.strip()
            }
            try:
                self._db.insert(rec)
            except sqlite3.IntegrityError:  # duplicate key - update instead
                self._db.update(rec)
                self.messageBox('Udpated in list: {}.'.format(rec['title']))
            else:
                self.fillListBox()
                self.messageBox('Added to list: {}.'.format(rec['title']))
        except urllib.error.HTTPError as e: self.errorBox(e)
        except urllib.error.URLError as e: self.errorBox(e)
        except ValueError as e: self.errorBox(e)
        except xml.parsers.expat.ExpatError as e: self.errorBox(e)

        self.varURL.set('')     # clear the URL box

    def errorBox(self, message, callback = None):
        self.messageBox(message, title = 'Error')
        if callback is not None: callback()
    
    def messageBox(self, message, **kwargs):
        mTitle = kwargs['title'] if 'title' in kwargs else 'Message'
        messageWindow = tkinter.Toplevel()
        textContainer = tkinter.Message(messageWindow, width = 500, text = message)
        messageClose = tkinter.Button(messageWindow, text = 'Close', command = messageWindow.destroy)
        messageWindow.title(TITLE + ' - ' + mTitle)
        messageWindow.grid()
        textContainer.grid(sticky = 'ew')
        messageClose.grid()

if __name__=='__main__':
    app = mainWindow()
    app.mainloop()

