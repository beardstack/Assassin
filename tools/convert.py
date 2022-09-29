# Assassin - Database Convert

# This tool converts OpenStreetMap data from the Overpass API to databases that can are compatible with Assassin. The converted databases might not be as detailed as databases specifically designed for Assassin, but they should still function correctly.
# To use this tool, simply run it from the command line using `python3 convert.py`. You will then be prompted to enter the file path to a JSON file containing information from the Overpass API. Then you'll be prompted to enter an output file path for the finished database after conversion. You'll then be prompted to enter a name and description for the new Assassin database. If these are left blank, defaults will be used.




# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE.md)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





import os # Required to interact with certain operating system functions
import json # Required to process JSON data
import time # Required to add delays and handle dates/times

import utils # Import the utils.py scripts.
style = utils.style # Load the style from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
save_to_file = utils.save_to_file # Load the file saving function from the utils script.
add_to_file = utils.add_to_file # Load the file appending function from the utils script.
display_notice = utils.display_notice  # Load the function used to display notices, warnings, and errors.


input_file = input("Input File: ")
output_file = input("Output File: ")


if (os.path.exists(input_file)): # Check to see if the input file path exists.
    input_database = json.load(open(input_file)) # Load the database from the file.
else:
    display_notice("The input file specified does not exist.", 3)
    exit()


output_database = { } # Create a blank JSON database to convert the data to.



output_database["name"] = input("Database Name: ") # Prompt the user to enter the name of the converted database.
if (output_database["name"] == ""): # If the user leaves the database name blank, set it to a default.
    output_database["name"] = "Converted Database"

output_database["description"] = input("Database Description: ") # Prompt the user to enter a description for the converted database.
if (output_database["description"] == ""): # If the user leaves the database description blank, set it to a default.
    output_database["description"] = "This is an Assassin database converted from data from OpenStreetMap via the Overpass API"

output_database["author"] = "OpenStreetMap Contributors"
output_database["created"] = str(round(time.time()))
output_database["modified"] = str(round(time.time()))
output_database["elements"] = {'brand': 'str', 'name': 'str', 'road': 'str', 'description': 'str', 'direction': 'int', 'operator': 'str'}
output_database["entries"] = []

for entry in input_database["elements"]:
    new_entry_data = {} # Set the new entry data to a placeholder.

    new_entry_data["latitude"] = entry["lat"]
    new_entry_data["longitude"] = entry["lon"]

    if "brand" in entry["tags"].keys():
        new_entry_data["brand"] = str(entry["tags"]["brand"])
    else:
        new_entry_data["brand"] = ""

    if "name" in entry["tags"].keys():
        new_entry_data["name"] = str(entry["tags"]["name"])
    else:
        new_entry_data["name"] = ""

    if "addr:street" in entry["tags"].keys():
        new_entry_data["road"] = str(entry["tags"]["addr:street"])
    else:
        new_entry_data["road"] = ""

    if "description" in entry["tags"].keys():
        new_entry_data["description"] = str(entry["tags"]["description"])
    else:
        new_entry_data["description"] = ""

    if "direction" in entry["tags"].keys():
        new_entry_data["direction"] = int(entry["tags"]["direction"])
    elif "camera:direction" in entry["tags"].keys():
        new_entry_data["direction"] = int(entry["tags"]["camera:direction"])
    else:
        new_entry_data["direction"] = ""

    if "operator" in entry["tags"].keys():
        new_entry_data["operator"] = str(entry["tags"]["operator"])
    else:
        new_entry_data["operator"] = ""

    output_database["entries"].append(new_entry_data) # Add the new entry to the rest of the database.


save_to_file(output_file, json.dumps(output_database, indent=4)) # Save the converted database to the file path specified by the user.