import tkinter as tk
from tkinter import ttk
import re

root = tk.Tk()
root.title("Immigration System")
root.geometry("400x300")

# read the SQL schemas from schemas.sql
def load_schema(file):
    with open(file, "r") as f:
        schema = f.read()

    tables = {}

    pattern = r"CREATE TABLE (\w+) \s*((.*?)\);"
    matches = re.findall(pattern, schema, re.S)

    for table, cols in matches:
        columns = []
        for col in cols.split(","):
            col_name = col.strip().split()[0]
            columns.append(col)

        tables[table] = columns

    return tables

entities = load_schema("schemas.sql")

title = tk.Label(root, text="Immigration System", font=("Arial", 18))
title.pack(pady=10)

root.mainloop()
