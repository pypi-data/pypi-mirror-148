from ast import excepthandler
import json
import os
import shutil
from glob import glob

Download_Folder: str = "YAY SEE!"
Destination_Folder: str = "C:/Users/verys/Downloads/TestDestination/"

Tax_Return_Check_String: str = "signal"
Client_Contact_Check_String: str = "Minecraft"

# Get settings from basic cache file json format
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
_config_location = os.path.join(__location__, "settings.json")
action = input(
    "PRESS ENTER to continue\nPress 'r' to reset the settings file\nClose this windows to exit\n")
if action == "r":
  try:
    os.remove(_config_location)
    print("Great! Removed settings file, will now create a new one ...")
  except Exception as err:
    print(f"No settings file found, {err=}")
try:
  with open(_config_location, "x"):
    print("First time detected: Creating settings file :)")
except:
  print("Settings file detected :)")
with open(_config_location, "r") as config:
  settings = config.read()
  if settings == "":
    settings = "{}"
  settings = json.loads(settings)
  print("Reading config file ...")
  try:
    #print(f"{settings['Download_Folder']=}")
    #print(f"{type(settings['Download_Folder'])=}")
    if "Download_Folder" not in settings:
      settings["Download_Folder"] = input(
          "No download folder detected (copy paste below pls): ") + "/*"
      settings["Download_Folder"]
    Download_Folder = settings["Download_Folder"]
  except:
    ...
  try:
    if "Destination_Folder" not in settings:
      settings["Destination_Folder"] = input(
          "No destination folder detected (copy paste below pls): ")
    Destination_Folder = settings["Destination_Folder"]
  except:
    ...
  try:
    if "Tax_Return_Check_String" not in settings:
      settings["Tax_Return_Check_String"] = input(
          "No tax return check string detected (copy paste below pls): ")
    Tax_Return_Check_String = settings["Tax_Return_Check_String"]
  except:
    ...
  try:
    if "Client_Contact_Check_String" not in settings:
      settings["Client_Contact_Check_String"] = input(
          "No client contact check string detected (copy paste below pls): ")
    Client_Contact_Check_String = settings["Client_Contact_Check_String"]
  except:
    ...
settings = f'{{\n"Download_Folder":"{Download_Folder!r}",\n"Destination_Folder":"{Destination_Folder!r}",\n"Tax_Return_Check_String":"{Tax_Return_Check_String!r}",\n"Client_Contact_Check_String":"{Client_Contact_Check_String!r}"\n}}'
try:
  with open(_config_location, "w") as config:
    config.write(settings)
    print("Successfully updated settings :)")
except:
  print("Unable to update settings :(")

Ignore_Next_Tax_Return_Check: bool = False
Ignore_Next_Client_Contact_Check: bool = False

try:
  Files = glob(Download_Folder)
except Exception as err:
  print("Attempting to open download folder, maybe incorrect path given?")
  raise err
#print(f"Your download files: \n{Files}")
Files.sort(key=os.path.getctime)
try:
  Files.reverse()
except Exception as err:
  print("Attempting to reverse download files, maybe path contains no files?")
  raise err
if not os.path.isdir(Destination_Folder):
  print("Creating destination folder (given one does not exist) ...")
  try:
      os.mkdir(Destination_Folder)
  except OSError as err:
      print("Creation of the directory {Destination_Folder} failed")
      raise Exception(
          "Cannot find / create directory given to copy to\nTry to reset the settings file by chosing 'r' next run")
print("Destination Folder is valid (or created :)")
for file in Files:
  if Tax_Return_Check_String in file and not Ignore_Next_Tax_Return_Check:
    input(
        f"Moving this file: \n  {file}\n to folder \n  {Destination_Folder}\nClose this window to exit")
    try:
      shutil.move(file, Destination_Folder)
    except Exception as err:
      print(
          f"Unable to move file {file} to {Destination_Folder} for some reason (maybe destination not possible to save files in?)")
      raise err
    Ignore_Next_Tax_Return_Check = True
  if Client_Contact_Check_String in file and not Ignore_Next_Client_Contact_Check:
    input(
        f"Moving this file: \n  {file}\n to folder \n  {Destination_Folder}\nClose this window to exit")
    try:
      shutil.move(file, Destination_Folder)
    except Exception as err:
      print(
          f"Unable to move file {file} to {Destination_Folder} for some reason (maybe destination not possible to save files in?)")
      raise err
    Ignore_Next_Client_Contact_Check = True
if not Ignore_Next_Client_Contact_Check:
  print("OOPs, no Client Contact file found!")
if not Ignore_Next_Tax_Return_Check:
  print("OOPs, no Tax Return file found!")
