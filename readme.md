# Path of Exile trade monitor

This is a proof of concept, not a fully featured trade monitor. It will take the name of an item and then continuously search stashes retrieved from the path of exile API for matching items. When it finds an item, it will print a useable trade message based on its price. It stores cur_change_id from the API in a text file to keep its place between program runs.

For testing, try entering "Tabula Rasa" (without quotes) when prompted for an item name