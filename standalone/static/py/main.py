from io import StringIO
import asyncio
import io
import json
import pickle


from argonodes.models import Model
from argonodes.nodes import Tree
from panel.io.pyodide import show
from pyodide import create_proxy, to_js
import js
import pandas as pd
import panel as pn


MODEL = Model()
TABLE = pn.widgets.Tabulator(pagination="remote", page_size=10, layout="fit_data_table", sizing_mode="stretch_width")


def init_model():
    global MODEL
    MODEL = Model()
    update_table_model()


def table_color_cells(val):
    if val == "None":
        color = "orange"
    elif val == "N/A":
        color = "red"
    else:
        color = "black"
    return "color: %s" % color


def update_table_model():
    global TABLE
    headers, listes = MODEL.to_list()

    temp = []
    for filename, liste in listes.items():
        for l in liste:
            temp.append([f"{filename or ''}:{l[0]}"] + l[1:])

    df = pd.DataFrame(temp, columns=headers)
    df.set_index("path", inplace=True)
    TABLE.value = df
    TABLE.style.applymap(table_color_cells)


async def process_file(event):
    global MODEL
    fileList = event.target.files.to_py()

    for f in fileList:  # JavaScript File
        # Get raw data
        data = await f.text()

        # Add a Tree to the model
        tree = Tree(json.loads(data), filename=f.name)
        MODEL.add_tree(tree)

        # Update table
        update_table_model()

        # Add a Tree to the list
        js.addTree(f.name)

        # Add method to remove
        remove_event = create_proxy(remove_file)
        e = js.document.getElementById(f.name)
        e.addEventListener("click", remove_event, False)


async def remove_file(event):
    global MODEL
    filename = event.target.parentElement.id

    # Remove from table
    try:
        del MODEL.traversal[filename]
    except KeyError:
        pass

    # Update table
    update_table_model()

    # Remove from the Trees list
    js.removeTree(filename)


async def new_model(event):
    global MODEL
    if js.confirm("Are you sure you want to create a new Model?\nAll your unsaved modifications will be lost."):
        for filename in MODEL.traversal:
            js.removeTree(filename)
        init_model()
        js.showAlert("primary", "New Model created.")
    else:
        return


async def change_name(event):
    global MODEL
    MODEL.name = event.target.value if event.target.value != "" else "Argonodes Model"


async def load_model(event):
    if js.confirm("Are you sure you want to load a Model?\nAll your unsaved modifications will be lost."):
        init_model()

        global MODEL
        fileList = event.target.files.to_py()
        for file in fileList:  # JavaScript File
            data = await file.text()
            # pyfile = io.BytesIO(data.encode())  # TODO Not working...

            # if file.mime == "text/csv" or file.name.endswith(".csv"):
            MODEL.import_from_csv(data)
            # elif file.mime == "application/python-pickle" or file.name.endswith(".pickle"):
            #     MODEL.import_from_pickle(pyfile)
            # else:
            #     raise AttributeError

            js.showAlert("primary", f"Model {0} loaded.")
    else:
        return


async def save_model(event):
    if event.target.id == "saveCSV":
        name = f"{MODEL.name}.csv"
        js.downloadFile(TABLE.value.to_csv(), name, "text/csv")
    elif event.target.id == "savePickle":
        buf = io.BytesIO()
        pickle.dump(MODEL.traversal, buf)
        name = f"{MODEL.name}.pickle"
        js.downloadFile(buf, name, "application/python-pickle")
    else:
        raise AttributeError
    js.showAlert("primary", f"Model saved under {name}.")


async def main():
    # New tree
    file_event = create_proxy(process_file)
    e = js.document.getElementById("newtree")
    e.addEventListener("change", file_event, False)

    # Model name change
    name_event = create_proxy(change_name)
    e = js.document.getElementById("modelname")
    e.addEventListener("change", name_event, False)

    # New Model
    new_event = create_proxy(new_model)
    e = js.document.getElementById("new")
    e.addEventListener("click", new_event, False)

    # Save Model
    save_event = create_proxy(save_model)
    e = js.document.getElementById("saveCSV")
    e.addEventListener("click", save_event, False)
    e = js.document.getElementById("savePickle")
    e.addEventListener("click", save_event, False)

    # Load Model
    new_event = create_proxy(load_model)
    e = js.document.getElementById("loadFile")
    e.addEventListener("change", new_event, False)

    # Init a new Model
    init_model()

    # Create table
    TABLE.value = pd.DataFrame(
        columns=["path", "foundType", "descriptiveType", "unique", "default", "description", "choices", "regex"]
    )

    await show(TABLE, "table")
    js.document.getElementById("loading").innerHTML = "Model Preview"


main()
