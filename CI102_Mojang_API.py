from mojang import Client

#Placeholder, it is my minecraft account, user input will be needed.
client = Client("evanpalubinski@gmail.com", "Binski55")
#Getting the NameInformation class object
name_change_info = client.get_name_change_info()

#Extract the creation date from the name_change_info dictionary
creation_date = name_change_info.created_at.strftime("%Y-%m-%d")

print(f"The Minecraft account was created on {creation_date}")