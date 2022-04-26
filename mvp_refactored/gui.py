import PySimpleGUI as sg
import mapper_utils

cal_title = 'Select'
cal_msg = 'Select an image to check how many calories it contains.'
layout = [[sg.Combo(sorted(sg.user_settings_get_entry('-filenames-', [])), default_value=sg.user_settings_get_entry('-last filename-', ''), size=(50, 1), key='-FILENAME-'), sg.FileBrowse(), sg.B('Check Calories')],
          [sg.Text(cal_msg)],
          [sg.Button('Exit')]]

window = sg.Window('CalCheck', layout)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Check Calories':
        sg.user_settings_set_entry('-last filename-', values['-FILENAME-'])
        fc_img = sg.user_settings_get_entry('-last filename-')
        print(fc_img)
        match, calories, labels = mapper_utils.identify_image(fc_img)
        if match and calories:
            cal_title = 'Match found!'
            cal_msg = f'We found a match! This looks like a {match}. Estimated calorie count: {calories}'
        else:
            cal_title = 'Oh no'
            cal_msg = 'Sorry, we could not identify this image.'
        sg.popup(cal_title, cal_msg)

window.close()