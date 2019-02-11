# Platypus

![image](https://i.imgur.com/lfGuoQE.png)

Project Platypus is a tool that will allow you to input a city name and receive a variety of geolocated OSINT exported as a CSV.  Platypus will use MapQuest API, allowing you to pull construction, traffic, and other road advisories.  It will also, in the future, incorporate some web scraping to collect protest locations where available.  The purpose of this tool is for travel security. Use it to streamline your OSINT collection for travel reports, personal or professional.

# How-to

Create a file called `key.txt` and place there your API key, Platypus will automatically read from that file.

Run `python3 platypus.py`, specify the file which read the entries from and then specify the file which save the results to.

# Example

An input must be formatted as `City,State`. For example `New York,NY` or `Dallas,TX`.
