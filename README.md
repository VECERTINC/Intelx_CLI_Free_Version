# Intelx CLI Free Version

This script is functional for “academic and free” users. They can be used with just an “API” key that you can manage in your Intelx account on the intelx.io website.

The filters we use are the basic “non-pro” ones, since it is a very expensive service.

Now I present to you one of the scripts that we are using and that you can already use.

![1_I1GwaDj4Tj0pPJ9CfGM39A (1)](https://github.com/user-attachments/assets/4295f97a-709b-41d4-aa99-ebfa993c9c7e)

Quick and easy query: we manage 90 results per search, as this is the limit for common users.

Searches are the same by email, IP address, web URL address; results will be returned instantly. You can now also preview and download the full file in .txt and perhaps .pdf format.

![rocks](https://github.com/user-attachments/assets/cecfcd34-0bc7-4a62-9406-329ca1274f47)

selecting and downloading file.txt

We will moderate the script later. For now we have code display issues in our github repository and rely on few sources, but soon a project management system from the Vecert team will be available on our website as well.

To install the script we must first install the requirements. You can use pip or save this in requirements.txt and run pip install -r requirements.txt

requests==2.31.0
colorama==0.4.6
tqdm==4.68.0

Now you can check out “python intelx.py” and then it will ask you to add your API key. This will be stored in a text file called API.txt to save the session.

![keys](https://github.com/user-attachments/assets/8730b9bd-d126-42f5-b2ec-9d40746eed64)

And here’s how the terminal would look like.



And that’s it, it’s ready to go.


Notes:

1 — If you have problems connecting to the API, I would advise changing your IP. Intelx often blocks certain IP addresses.

2 — You can’t preview everything from the terminal; you would have to use the automated download that our script allows you to use.

