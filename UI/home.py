import tkinter as tk
from tkinter import ttk
import re
import os

root = tk.Tk()
root.title("Immigration System")
root.geometry("400x300")

# read the SQL schemas from schemas.sql
def load_schema(file):
    with open(file, "r") as f:
        schema = f.read()

    tables = {}

    pattern = r"CREATE TABLE (\w+)\s*\((.*?)\);"
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

title = tk.Label(root, text="Immigration System", font=("Arial", 18))
title.pack(pady=10)

root.mainloop()
