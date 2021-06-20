from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from MongoServer import *
from bson.json_util import dumps
from EntryListener import *
import datetime

class MongoGUI:
    def __init__(self):
        self.mongoServer = None
        self.connect()

        self.root = Tk()
        self.root.title("Mongo Praktikum 3")

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.createEntryWidget(row=1, label='7b)', entryListener=EntryListener(self.sb))
        self.createEntryWidget(row=2, label='7c)', entryListener=EntryListener(self.sc))
        self.createEntryWidget(row=3, label='8b1)', entryListener=EntryListener(self.ebo))
        self.createButtonWidget(row=4, label='8b2)', callback=self.ebt)
        self.createButtonWidget(row=5, label='8b3)', callback=self.ebth)
        self.createButtonWidget(row=6, label='8b4)', callback=self.ebf)
        self.createButtonWidget(row=7, label='8b5)', callback=self.ebfi)
        self.createButtonWidget(row=8, label='8b6)', callback=self.ebs)
        self.createButtonWidget(row=9, label='8c)', callback=self.ec)
        self.createButtonWidget(row=10, label='8d)', callback=self.ed)
        self.createButtonWidget(row=11, label='8dr)', callback=self.edr)
        self.createButtonWidget(row=12, label='8e1)', callback=self.eeo)
        self.createButtonWidget(row=13, label='8e2)', callback=self.eet)
        self.createButtonWidget(row=14, label='8e3)', callback=self.eeth)
        self.createButtonWidget(row=15, label='8e4)', callback=self.eef)

        # Miscellaneous function section
        ttk.Button(self.mainframe, text="COUNT", command=self.count).grid(column=3, row=1, sticky=(W, E))
        ttk.Button(self.mainframe, text="SHOW ALL", command=self.showall).grid(column=3, row=2, sticky=(W, E))

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def createEntryWidget(self, row=0, label='Label', entryListener=None):
        ttk.Label(self.mainframe, text=label).grid(column=1, row=row, sticky=(W, E))
        entryVar = StringVar()
        entryListener.setEntry(entryVar)
        entry = ttk.Entry(self.mainframe, width=20, textvariable=entryVar)
        entry.grid(column=2, row=row, sticky=(W, E))
        entry.bind('<Return>', entryListener.method)

    def createButtonWidget(self, row=0, label='Label', callback=None):
        ttk.Label(self.mainframe, text=label).grid(column=1, row=row, sticky=(W, E))
        ttk.Button(self.mainframe, text="Ausführen", command=callback).grid(column=2, row=row, sticky=(W, E))

    # Method task 7b
    def sb(self, entryVar):
        entry = entryVar.get()
        startTime = datetime.datetime.now()
        results = self.mongoServer.find({"_id":entry})
        endTime = datetime.datetime.now()
        for result in results:
            self.writeToConsole('[7b)] Ort:{}, Staat:{}'.format(result['city'],result['state']))
        print('Query took {}'.format(endTime-startTime))
    
    # Method task 7c
    def sc(self, entryVar):
        entry = entryVar.get()
        startTime = datetime.datetime.now()
        results = self.mongoServer.find({"city":entry})
        endTime = datetime.datetime.now()
        for result in results:
            self.writeToConsole('[7c)] PLZ:{}'.format(result['_id']))
        print('Query took {}'.format(endTime-startTime))

    # Method task 8b1
    def ebo(self, entryVar):
        entry = entryVar.get()
        results = self.mongoServer.find({"name":entry}, {"_id":0})
        self.writeList('8b1)', results)

    # Method task 8b2
    def ebt(self):
        results = self.mongoServer.find({"$and": [{"farben": {"$all":["schwarz"]}},
                                                  {"nike":"j"}]}, {"name":1, "_id":0})
        self.writeList('8b2)', results)

    # Method task 8b3
    def ebth(self):
        results = self.mongoServer.find({"$and": [{"farben": {"$all":["weiss","gruen"]}},
                                                  {"nike":"j"}]}, {"name":1, "_id":0})
        self.writeList('8b3)', results)

    # Method task 8b4
    def ebf(self):
        results = self.mongoServer.find({"$and": [{"farben": {"$in":["weiss","gruen"]}},
                                                  {"nike":"j"}]}, {"name":1, "_id":0})
        self.writeList('8b4)', results)

    # Method task 8b5
    def ebfi(self):
        result = self.mongoServer.minByKeyOne("Tabellenplatz")
        self.writeToConsole('[8b5)] {}'.format(result))

    # Method task 8b6
    def ebs(self):
        results = self.mongoServer.find({"Tabellenplatz": {"$lt": 16}}, {"_id":0})
        self.writeList('8b6)', results)

    # Method task 8c
    def ec(self):
        results = self.mongoServer.find({"Tabellenplatz": {"$gte": 16}}, {"_id":0})
        self.writeList('8c)', results)

    # Method task 8d
    def ed(self):
        self.mongoServer.update({"name":"Augsburg"}, {"Tabellenplatz":1})

    # Method task 8dr
    def edr(self):
        self.mongoServer.update({"Tabellenplatz":1}, 
            {'name': 'Augsburg', 'farben': ['rot', 'weiss'], 'Tabellenplatz': 12, 'nike': 'j'})

    # Method task 8e1
    def eeo(self):
        self.mongoServer.update({"name":"Leverkusen"}, {"$set":{"Tabellenplatz":2}})

    # Method task 8e2
    def eet(self):
        self.mongoServer.update({"name":"Werder"}, {"$inc":{"Tabellenplatz":-1}})

    # Method task 8e3
    def eeth(self):
        self.mongoServer.update({"name":"HSV"}, {"$set":{"abgestiegen":True}})

    # Method task 8e4
    def eef(self):
        self.mongoServer.update({"farben": {"$in":["weiss"]}}, {"$set":{"Waschtemperatur":90}}, multi=True)

    def writeList(self, prefix, results):
        for result in results:
            self.writeToConsole('[{}] {}'.format(prefix, result))

    def count(self):
        count = self.mongoServer.count()
        self.writeToConsole('[COUNT] {}'.format(count))

    def showall(self):
        results = self.mongoServer.find(projection={"_id":0})
        self.writeList('ALL', results)
        separateline = ''
        for x in range(0,120):
            separateline+='-'
        self.writeToConsole(separateline)

    def writeToConsole(self, output):
        print(output)

    def connect(self):
        HOST = 'localhost'
        self.mongoServer = MongoServer(HOST)