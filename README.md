
# presetmails
Python package for quickly sending different emails via the commandline using a template

## Description

This small project I've been working on allows the user to set a template in a textfile containing an email-preset.
This preset can contain variables denoted by curly brackets {}, which can then be set to different values each time the program is executed.
The email is then sent with the users mailing account.

*Do keep in mind that this project is currently in alpha-alpha.*

## Getting Started

### Dependencies

* Python3 (Should work with Python2 aswell, untested)
* Windows 10 (Should work for Windows<10 or Unix systems aswell, untested)

Libraries:
* colorama==0.4.6 
* termcolor==2.2.0
* keyring==23.13.1
* cryptography==39.0.0

### Installing

**Download as zip or run:**
```
git clone https://github.com/NotIPlayForFun/presetmails.git
```
**Then install required libraries:**
Run:
```
pip install -r requirements.txt
``` 
in the presetmails folder to install required libraries.

## Executing program

Navigate into the presetmails folder using the command line.

**Use --help for list of commands:**
```
Python main.py --help
```
**Use  --readme option for detailed description:**
```
Python main.py --readme
```
This will give you detailed instructions on how the program works.

### Getting started:

**1. First, setup your email account using the --setup option.**
```
Python main.py --setup
```
Here, you can set all the information the program needs to send your emails.
* **smtp server:** Your mail providers smtp server, you can find this on google
* **port:** The servers port; preferably tls
* **mail address:** The mail address you want to send the emails with
* **Login options:**
	* **Toggle password storage:** Wether you want the program to store your password
	* **username:** The mailing accounts username, likely the same as email-address
	* **password:** Store the mailing accounts password if password storage is turned on

**2. Then, write a preset in MAIL_PRESET.txt (create it in the presetmails folder if it's not there already).**

***Example preset:***
```
SUBJECT=This is an example Subject ---> optional subject header, you can use variables here too
Hello {person1}, --->variable named person1

I am writing to you because of {reason}.

Also, did you hear about {thing}?

See you soon,
{person2}
```
**3. Run the program.**
```
python3 main.py
```

<sub>Optionally, you can specify some or all of the variables, recipients and subject
ahead of time when calling the program on the command line using the optional arguments.
This is honestly kind of a useless feature right now, just run it program normally.
For more information, check the --readme</sub>

## Help

God help you if something breaks.
There are some useful error messages, so it should usually be clear why things aren't working.
**If there's a bug, do feel free to open an issue :)**
## Authors

Contributors names and contact info

Jerrik S.
mail: jerrik@jerrik.de

## Version History

* Aint no version tracking in these lawless lands

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
