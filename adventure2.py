import adventuresimplelib as adv
import PySimpleGUI as sg

class Game:
	current_room = None
	player_inventory = adv.Bag()

bedroom = adv.Room("""This is the bedroom, there is a burning candle on the wall. There is also a comfortable bed.""")

livingroom = adv.Room("""This is the livingroom. There is a sofa""")

computerroom = adv.Room("""This is a room with computers, the computer room.""")

kitchen = adv.Room("""This is the kitchen.""")

garden = adv.Room(""" This is the garden, there are pretty and aromatic flowers here that you have planted. """)

bedroom.inventory = adv.Bag()
livingroom.inventory = adv.Bag()
kitchen.inventory = adv.Bag()
computerroom.inventory = adv.Bag()
garden.inventory = adv.Bag()

bedroom.west = livingroom
livingroom.north = computerroom
livingroom.west = garden
computerroom.east = kitchen

computerroom.locked = {"east":True}
bedroom.locked = dict()
kitchen.locked = dict()
livingroom.locked = {"west":True}

Game.current_room = bedroom

def use_garden_key():
	if Game.current_room == livingroom:
		print("You have unlocked the door to the garden.")
		livingroom.locked["west"] = False
		return True
	else:
		print("You have failed to unlock the door to the garden. Try another room.")


def use_kitchen_key():
	"""returns boolean destroy is True when item was used successfull, otherwise False"""
	# only works in the computerrrom
	if Game.current_room == computerroom:
		print("You have unlocked the door to the kitchen.")
		computerroom.locked["east"] = False
		return True
	else:
		print("You have failed to unlock the kitchen door. Try another room.")
		return False

		
kitchen_key = adv.Item("There is an old rusty brass key on the floor. Try to find out what this is for.", "Brass key")
kitchen_key.use_item = use_kitchen_key

bedroom.inventory.add(kitchen_key)

garden_key = adv.Item("On the kitchen counter there is a iron key. What could this be for?", "Iron key")
garden_key.use_item = use_garden_key

kitchen.inventory.add(garden_key)

fresh_baguettes = adv.Item("There is a bag of freshly baked baguettes on the kitchen counter.", "Baguettes")

kitchen.inventory.add(fresh_baguettes)


@adv.when("use ITEM")
def use(item):
	# do we have item?
	print("took the item:", item)
	obj = Game.player_inventory.take(item)
	if not obj:
		print("You don't have", item)
		#destroy = False
	else:
		print("Use the item:", item)
		destroy = obj.use_item()
		# destroy item after use?
		if not destroy:
			Game.player_inventory.add(obj)
		

@adv.when("inventory")
@adv.when("show inventory")
@adv.when("show my items")
def show():
	print("You carry these items with you:")
	for item in Game.player_inventory:
		print(item)
	if len(Game.player_inventory) == 0:
		print("You have nothing in your inventory.")
		

@adv.when("take ITEM")
def get(item):
	obj = Game.current_room.inventory.take(item)
	if not obj:
		print("In this room there is no ", item, "to take")
	else:
		print("You took the", item)
		Game.player_inventory.add(obj)


@adv.when("look")
def look():
	adv.say(Game.current_room)
	print("Items in this room:")
	for item in Game.current_room.inventory:
		print(item)
	if len(Game.current_room.inventory) == 0:
		print("There are no items in this room")
	
	print("exits:")
	print(Game.current_room.exits())


@adv.when("go DIRECTION")
@adv.when("DIRECTION")
def go(direction):
	next_room = Game.current_room.exit(direction)
	if next_room:
		# locked ?
		if direction in Game.current_room.locked:			
			if Game.current_room.locked[direction]:
				print("The door is closed. You can't go in.")
				return
		Game.current_room = next_room
		print("You entered another room")
		look()
	else:
		print("It isn't possible to go into this direction.")


layout = [
		[sg.Image(background_color="white", key="image1")],
		[sg.Multiline("blabla", size=(20,10),key="multi1")],
		[sg.Text(">>>"),sg.Input(key="command", size=(10,1)), sg.Button("OK"),],
		[sg.Button("Quit")],
	]

window = sg.Window("Butterbrotquest",layout)

while True:
	event,values = window.read(timeout=100)
	if event in (sg.WIN_CLOSED, "Quit"):
		break
	if event == "OK":
		window["multi1"].update(">>>"+values["command"]+"\n")
		adv._handle_command(values["command"])

window.close()
#if __name__ == "__main__":
	#look()
	#print("Type help to see a list of all commands")
	#adv.start()
