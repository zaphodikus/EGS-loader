# read and understand the structure
import os
import ecf_parser
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

path_vanilla = "C:/Users/conradb/PycharmProjects/egs_parser/TESTDATA/Config_Example.ecf"
path_english = "C:/ssd/Steam/SteamApps/common/Empyrion - Galactic Survival/Content/Extras/Localization.csv"

# load all the item internal and English Strings
default_language = 'Deutsch'# 'English'
language_csv = {}
with open(path_english, 'r', encoding="utf-8") as f:
    props = f.readline().rstrip().split(',')
    for line in f.readlines():
        line = line.rstrip()
        entry = dict(zip(props, line.split(',')))
        language_csv[line.split(',')[0]]= entry

def get_language_string(name:str, language = default_language):
    try:
        return language_csv[name][language]
    except KeyError:
        return "[{}]".format(name) # make it clear that this item never shows up in item menu


class HelloECF:
    def __init__(self, master, languages):
        row = 0
        self.label_path_vanilla = ttk.Label(master, text = "File: {}".format(path_vanilla))
        self.label_path_vanilla.grid(row=row, column=0, pady=(7,7),columnspan=3)
        self.browse_button = ttk.Button(master, text="...", command = self.browse_file)
        self.browse_button.grid(row=row, column=4)
        row += 1
        text = ttk.Label(master, text = "Language").grid(row=row, column=0, pady=(7,7))
        self.language = StringVar()
        self.cb_language = ttk.Combobox(master, textvariable= self.language, state="readonly")
        self.cb_language.grid(row=row , column=1)
        self.cb_language.config(values=languages)
        self.language.set('English') # a default
        self.cb_language.bind("<<ComboboxSelected>>", self.item_box_updated)  # language drop-list 2 cause tree rebuild
        row +=1
        # filter box can be used to reduce what we see in the combo box
        text = ttk.Label(master, text="Filter").grid(row=row, column=0)
        self.edit_filter = ttk.Entry(master)
        vcmd = (self.edit_filter.register(self.filter_callback), "%d", "%P")
        self.edit_filter.config(validate = "key", validatecommand = vcmd)
        self.edit_filter.grid(row=row, column=1, pady=(7,7))

        self.item_name_legend = ttk.Label(master, text="Item Name")
        self.item_name_legend.grid(row=row, column=2)
        self.item_name = StringVar()
        self.cb_itemname = ttk.Combobox(master, textvariable = self.item_name, state="readonly")
        self.cb_itemname.grid(row=row, column = 3)
        #entity_names = [entity.Name for entity in entities]
        #self.cb_itemname.config(values = entity_names)
        self.cb_itemname.bind("<<ComboboxSelected>>", self.item_box_updated)
        #self.fill_item_listbox(None)

        row +=1
        self.item = "noone"
        self.text = ttk.Label(master, text = self.item)
        self.text.grid(row=row, column=0)
        self.button = ttk.Button(master, text="Press me", command = self.Pressed)
        self.button.grid(row=row, column=1)
        row +=1
        # tree control for entity

        self.entity_tree = ttk.Treeview(master)
        self.entity_tree.grid(row=row, column=0, columnspan=4, pady=(7,7))
        self.entity_tree.config(columns=("value", "default"))
        self.entity_tree.column("#0", width=250, anchor="e")
        self.entity_tree.column("value", width=250, anchor="w")
        self.entity_tree.column("default", width=250, anchor="w")

        self.entity_tree.heading("#0", text="<element>")
        self.entity_tree.heading("value", text="Value")
        self.entity_tree.heading("default", text="Default")
        self.reload_entities(path_vanilla)
        self.images = {}
        self.ent_types = []
        for entry in self.entities:
            val = self.entities[entry]
            if not val.Type in self.ent_types:
                self.ent_types.append(val.Type)
        wd = os.getcwd()
        for name in self.ent_types:
            filepath = (wd + "\\ecf_compare\\img_{}.gif".format(name)).replace("\\", '/')
            self.images[name] = PhotoImage(file=filepath)

        # load the defaults file too
        gen = ecf_parser.entries_from_ecf_file(path_vanilla)
        # ignore containers and lootz etc
        entities_list = [entry for entry in gen if entry.Type in ['Template', 'Entity', 'Item', 'Block']]
        self.default_entities = dict(zip([entity.Name for entity in entities_list] ,entities_list))

        self.row = row #should really use a frame here
        self.fill_item_listbox(filter="")
        self.item_box_updated(None)

    def reload_entities(self, filename):
        # (re)load the .ECF file
        self.label_path_vanilla["text"] = "Loading... {}".format(filename)
        gen = ecf_parser.entries_from_ecf_file(filename)
        # ignore containers and lootz etc
        entities_list = [entry for entry in gen if entry.Type in ['Template', 'Entity', 'Item', 'Block']]
        self.entities = dict(zip([entity.Name for entity in entities_list] ,entities_list))
        self.label_path_vanilla["text"] = "File {}".format(filename)

    def browse_file(self):
        dir = self.label_path_vanilla["text"].split(' ')[1:][0]
        initial = os.path.normpath(os.path.split(dir)[0])
        filename = filedialog.askopenfilename(initialdir = initial, title = "Select A File", \
                filetype = (("Config files","*.ecf"),("all files","*.*")) )
        # load the file
        self.reload_entities(filename)
        self.fill_item_listbox("")
        self.item_box_updated(None)

    def item_box_updated(self, event):
        # combo box updated.
        ent = self.entities[self.item_name.get()]
        for i in self.entity_tree.get_children():
            self.entity_tree.delete(i)
        # populate
        self.entity_tree.heading("#0", text=ent.Name)
        rowsadded = self.populate_tree(ent)
        print("rows={}".format(rowsadded))


    def populate_tree(self, ent, row_index=0, parent_name= ""):
        class listObject(list):
            def __init__(self, list):
                self.__setattr__(list['Name'], list['Value'])

        row =0
        rowsadded = 0
        unique_id = parent_name # parent node in tree
        for property in vars(ent):
            value = getattr(ent, property)
            if value and "Properties" != property:
                unique_id = parent_name + str(row) + property
                args = {'parent':parent_name, 'index': str(row), 'iid': unique_id, 'text': property, 'open': True}
                # add icon to 1st entry
                if not (row) and parent_name == "":
                    args['image'] = self.images[ent.Type]
                print(args)
                self.entity_tree.insert( **args)
                print("= {}".format(getattr(ent, property)))
                value = getattr(ent, property)
                if property == 'Name':
                    value += " ({})".format(get_language_string(value, self.language.get()))

                self.entity_tree.set(unique_id, "value", value)
                self.entity_tree.set(unique_id, "default", "?")
                row += 1
            else:
                if "Properties" == property:
                    for subproperty in getattr(ent, property):
                        print("{} ->".format( unique_id))
                        if isinstance(subproperty, ecf_parser.Entry):
                            rowsadded += self.populate_tree(subproperty, row , parent_name=unique_id)
                        else:
                            if isinstance(subproperty, dict):
                                rowsadded += self.populate_tree(listObject(subproperty), row, parent_name=unique_id)
        return row + rowsadded


    def fill_item_listbox(self, filter):
        """
        populate the list of items user can choose from, based on a filter
        :param filter:
        :return:
        """
        entity_names = [entity for entity in self.entities if not filter or filter.lower() in entity.lower()]
        self.cb_itemname.config(values = entity_names)
        try:
            self.item_name.set(entity_names[0])
        except IndexError:
            pass
        self.item_name_legend.configure(text="Item ({})".format(len(entity_names)))

    def filter_callback(self, action, final):
        # Validation hook for the filter input-box. simply returns true, but refreshes the items combobox
        self.fill_item_listbox(filter=final)
        self.text.config(text=final)
        return(True)

    def Pressed(self):
        self.text.config(text = "pressed")


root = Tk()
languages = props[1:]
app = HelloECF(root, languages)

root.mainloop()