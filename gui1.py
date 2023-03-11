import adventurelib as adv
import PySimpleGUI as sg

layout = [
	[sg.Text("Butterbrotquest Version 1.0")],
	[sg.Multiline("bla bla bla", size=(20,5),key="multi"), ],
	[sg.Text("Your command >>>"), sg.Input(size=(10,1), key="command")],
	[sg.Button("OK"), sg.Button("Quit")],
		]
		
window = sg.Window("my game", layout)

while True:
	event, values = window.read()
	if event in (sg.WIN_CLOSED, "Quit"):
		break
	if event == "OK":
		adv._handle_command(values["command"])
print("bye")	
