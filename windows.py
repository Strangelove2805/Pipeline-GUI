import PySimpleGUI as sg



def make_editor(location, tag1, tag2):
    """Builds the interface for the editor window

    Text boxes for displaying and editing a table's data,
    complete with options to edit queries and modify data
    """
    hori, vert = (300, 60)

    header =  [[sg.Column(layout=[
        
               [sg.Text("Username (Import)"), sg.Input(pad=(0,0), size=(22,1), key="-INUSER-"), 
                sg.Text("", pad=(10,0)),
                sg.Text("Database (Import)"), sg.Input(pad=(0,0), size=(22,1), key="-INDB-"), 
                sg.Text("", pad=(10,0))],

               [sg.Text("Password (Import)"), sg.Input(pad=(0,0), size=(22,1), password_char='*', key="-INPW-"), 
                sg.Text("", pad=(10,0)), 
                sg.Text("Server   (Import)"), sg.Input(pad=(0,0), key="-INSRVR-", default_text="localhost:3306", size=(22,1))],

                ]), 
                
                sg.Column(layout=[[sg.Button("IMPORT DATA", button_color="#08A045"), 
                                   sg.T(" "), 
                                   sg.Text("o", key="-IMPORTTEXT-")]])],

               [sg.Text("Query", pad=(14,0)), 
                sg.Input(pad=(0,10), default_text="SELECT * FROM [table_name_here]", size=(105,1), key="-QUERY-")],

               [sg.HorizontalSeparator(pad=(0,5))],
 
                [sg.T("Search", pad=(10,15)), sg.Input(key="-CTRLF-", size=(20,1)), 
                 sg.Button("Find"), 
                 sg.T("", pad=(40,0)), sg.Input(key="-CELLSIZE-", size=(4,1), default_text="20"), 
                 sg.Button("Resize", key="-EXPAND-")]]

    boxes =   sg.Column(layout=[[sg.Input(size=(20,1), pad=(0,0), key=(tag1[col] + tag2[row]), 
                     background_color="#E1E1E1", text_color="#000000", 
                     font="Helvetica 9", enable_events=True) for col in range(8)] for row in range(25)])

    viewer = [[boxes, sg.Slider(range=(1, 0), orientation="vertical", key="-SLD1-", 
                     enable_events=True, resolution=1, default_value=0, size=(23,15))]]
            
    layout =  [[sg.Column(layout=header + viewer), 
                sg.Column(layout=[[sg.T("")],[sg.T("")]])
                ],
               [sg.Slider(range=(0, 1), orientation="horizontal", key="-SLD2-", 
                     enable_events=True, resolution=1, size=(100,15)), sg.Button("EXPORT", button_color="#D1001F", pad=(23,7))]]

    return sg.Window("Editor", layout, font="Courier 12", return_keyboard_events=True, 
                     location=(location[0], location[1]), finalize=True, resizable=True)
