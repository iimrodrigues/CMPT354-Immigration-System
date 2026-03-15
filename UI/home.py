import tkinter as tk
from tkinter import ttk
import re
import os

root = tk.Tk()
root.title("Immigration System")
root.geometry("1080x720")

# read the SQL schemas from schemas.sql
def load_schema(file):
    with open(file, "r") as f:
        schema = f.read()

    tables = {}

    pattern = r"CREATE TABLE (\w+)\s*\((.*?)\)\);"
    matches = re.findall(pattern, schema, re.S | re.I)

    for table, cols_block in matches:
        cols = []
        for col in cols_block.split(","):
            col_name = col.strip().split()[0]
            if col_name.upper() not in ["PRIMARY", "FOREIGN", "CONSTRAINT"]:
                cols.append(col_name)

        tables[table] = cols

    return tables

base_dir = os.path.dirname(__file__)
schema_file = os.path.abspath(os.path.join(base_dir, "..", "Database", "schema.sql"))

if not os.path.exists(schema_file):
    raise FileNotFoundError(f"Cannot find schema at {schema_file}")

entities = load_schema(schema_file)

#
#GUI
#
title = tk.Label(root, text="Immigration System", font=("Arial", 18))
title.pack(pady=10)

#dropdown menu for the entities to be inserted
selected_entity = tk.StringVar()

dropdown = ttk.Combobox(
    root,
    textvariable=selected_entity,
    values=list(entities.keys())
)
dropdown.pack(pady=10)

dropdown.set("Select Entity to Insert")

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

entries = {}

def update_form(event=None):

    for widget in form_frame.winfo_children():
        widget.destroy()

    entries.clear()

    entity = selected_entity.get()

    if entity in entities:

        for attr in entities[entity]:

            row = tk.Frame(form_frame)
            row.pack(fill="x", pady=3)

            label = tk.Label(row, text=attr, width=15, anchor="w")
            label.pack(side=tk.LEFT)

            entry = tk.Entry(row)
            entry.pack(side=tk.RIGHT, expand=True, fill="x")

            entries[attr] = entry

##does not connect to database for now
##simply prints out the data to be inserted
def submit():

    entity = selected_entity.get()

    data = {k: v.get() for k, v in entries.items()}

    print("Table:", entity)
    print("Data:", data)

submit_btn = tk.Button(root, text="Insert", command=submit)
submit_btn.pack(pady=10)

dropdown.bind("<<ComboboxSelected>>", update_form)

root.mainloop()
