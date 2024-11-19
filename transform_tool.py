"""Displays editor windows (code re-used from another project)"""

# Requires 3.12 > Python >= 3.8

import PySimpleGUI as sg
import windows
import pandas as pd
import spark_read as sp



def refresh_editor(editor_data, offset1, offset2):
    """Resets the elements shown in the CSV editor window

    The editor is made up of input text boxes. These must be refreshed
    constantly when scrolling through a file to maintain the impression that
    the file is being looked through much like in Excel

    Input Parameters:
    -----------------
    editor_data     Type:   List
                    Use:    The data file being looked at in the editor

    offset1         Type:   Int
                    Use:    The column number that will correlate to the top-left
                            element in the editor table
                    Case:   1, 2, 3, 4...

    offset2         Type:   Int
                    Use:    The row number that will correlate to the top-left
                            element in the editor table
                    Case:   1, 2, 3, 4...
    """
    global tag1     # A, B, C, D...
    global tag2     # 1, 2, 3, 4...  put together to make the text box tags A1, A2, A3...


    cols = 8

    for i in range(cols):
        for j in range(25):

            try:
                window[tag1[i] + tag2[j]].update(str(editor_data[offset1 + j][offset2 + i])) 
            except:
                window[tag1[i] + tag2[j]].update("")        # If the coordinate does not exist in the data, leave the cell blank




if __name__ == "__main__":


    # Information for the editor window
    tag1 = ["A", "B", "C", "D", "E", "F", "G", "H"]
    tag2 = [str(num) for num in range(25)]
    taglist = [letter + number for letter in tag1 for number in tag2]
    editor_data = []
    column_names = []

    sg.theme("DarkTeal9")
    sg.set_options(element_padding=(0,0))

    location = (160,50)
    window1 = windows.make_editor(location, tag1, tag2)
    window1.bind("<Enter>", "UNDER CURSOR")
    window1.bind("<Leave>", "CURSOR NOT IN WINDOW")

    in_editor = False       # Scroll wheel function causes issues so we need to check the editor is being used before it's considered


    while True:                                                                                 # Primary loop where events take place
        window, event, values = sg.read_all_windows()

        if event == sg.WIN_CLOSED:                     # Windows can be closed in the top-right or through any button labelled "Exit"
        
                window1.close()
                break


        elif event in ["-SLD1-","-SLD2-"]:                                                  # EVENT: CSV editor sliders are being scrolled

            try:
                refresh_editor(editor_data, int(values["-SLD1-"]), int(values["-SLD2-"]))
            except:
                pass


        elif event == "UNDER CURSOR":                   # EVENT: Ensuring the cursor is on the Editor for the scroll events below
            in_editor = True


        elif event == "CURSOR NOT IN WINDOW":           # EVENT: The cursor has left the editor window so the below events should be ignored
            in_editor = False


        elif in_editor == True and event == "MouseWheel:Up":                                                      # EVENT: Mouse wheel (rolled up) is being used in the CSV editor
            try:
                window["-SLD1-"].update(values["-SLD1-"] - 3)
                refresh_editor(editor_data, int(values["-SLD1-"]), int(values["-SLD2-"]))
            except:
                pass


        elif in_editor == True and event == "MouseWheel:Down":                                                    # EVENT: Mouse wheel (rolled down) is being used in the CSV editor
            try:
                window["-SLD1-"].update(values["-SLD1-"] + 3)
                refresh_editor(editor_data, int(values["-SLD1-"]), int(values["-SLD2-"]))
            except:
                pass


        elif event == "IMPORT DATA":                                           # A file has been selected for the CSV editor


            try:

                df = sp.mysql_query(values["-INUSER-"],
                                    values["-INPW-"],
                                    values["-INSRVR-"],
                                    values["-INDB-"],
                                    values["-QUERY-"])

                column_names = [item for item in df.columns]
                dtype_info = df.dtypes

                # Create a list of tuples containing column names and their data types
                dtype_list = [(col, str(dtype)) for col, dtype in dtype_info.items()]

                column_names = [item[0] + " Type(" + item[1] + ")" for item in dtype_list]

                data = df.values.tolist()

                editor_data = [[str(item) for item in row] for row in data]
                editor_data.insert(0, column_names)


                longest = len(max(editor_data, key=len))
                length = len(editor_data)

                refresh_editor(editor_data, 0, 0)

                window["-SLD1-"].update(range=(0, length))      # Update the size of the scrollbars to fit the data
                window["-SLD2-"].update(range=(0, longest))

                window["-IMPORTTEXT-"].update("Success!")
                window["-IMPORTTEXT-"].update(text_color=("lime green"))

            except:

                window["-IMPORTTEXT-"].update("Import error!")
                window["-IMPORTTEXT-"].update(text_color=("red"))
                pass


        elif event == "EXPORT":                                           # A file has been selected for the CSV editor

            print("")

            try:

                columns = []
                
                for column in editor_data[0]:
                    dtype_flag = column.rfind("(")

                    if dtype_flag != -1:
                        columns.append(column[:dtype_flag-5])
                    else:
                        columns.append(column)

                for i in range(len(editor_data)):
                    if len(editor_data[i]) > len(columns):
                        delta = len(editor_data[i]) - len(columns)
                        editor_data[i] = editor_data[i][:-delta]



                df = pd.DataFrame(editor_data[1:], columns=columns)

                print(df)

            except Exception as e:

                print(e)

                pass


        elif event == "Find":   # The CTRL-F equivalent finder function has been used


            found = False
            try:
                for i in range(int(values["-SLD1-"]), len(editor_data)):    # Search all elements after the one currently at the top-right

                    if found == True:
                        break

                    for j in range(len(editor_data[i])):

                        if i == int(values["-SLD1-"]) and j <= int(values["-SLD2-"]):   # Make sure the search can start from the middle of a row
                            continue

                        elif values["-CTRLF-"] in editor_data[i][j]:
                            window["-SLD1-"].update(value=i)
                            window["-SLD2-"].update(value=j)
                            refresh_editor(editor_data, i, j)
                            found = True
                            break

            except:
                pass




        elif event == "-EXPAND-":                                               # EVENT: Change the horizontal size of cells in the CSV editor
            try:
                if int(values["-CELLSIZE-"]) <= 300:
                    [[window[y + str(x)].set_size((values["-CELLSIZE-"],None)) for x in range(25)] for y in tag1]
            except:
                pass


        elif event in taglist:                                                  # EVENT: A box in the CSV editor is being edited
            # In order to prevent an index error, we need to add columns and rows to the existing dataset to account
            # for adding data into cells that are beyond its size

            # If the selected box is beyond the length of the dataset
            if (int(values["-SLD1-"]) + int(event[1:])) > len(editor_data) - 1:

                for i in range(len(editor_data) -1,
                            (int(values["-SLD1-"]) + int(event[1:]))):

                    editor_data.append([""])    # Add a new empty list for each new row required

            # Same as above but for columns. If new data is added too far to the right, it will cause an index error
            if (int(values["-SLD2-"]) + int(tag1.index(event[0]))) > len(editor_data[int(values["-SLD1-"]) + int(event[1:])]) - 1:

                for i in range(len(editor_data[int(values["-SLD1-"]) + int(event[1:])]) -1,
                            (int(values["-SLD2-"]) + int(tag1.index(event[0])))):

                    editor_data[int(values["-SLD1-"]) + int(event[1:])].append("")

            # Replace the current element in the data with the edited cell in the editor table
            editor_data[int(values["-SLD1-"]) + int(event[1:])][int(values["-SLD2-"]) + int(tag1.index(event[0]))] = values[event]



