from bs4 import BeautifulSoup
import requests
import csv
import os
from urllib.parse import urlparse
import datetime

#Purpose: Scraping title, author, references, and images from webpages on the archive.
#Functions div, title, and image    
#=====================================================================================================================================================
# == For Author  == 
def text_scrape_div(link, writer):
    html_txt = requests.get(link).text
    soup = BeautifulSoup(html_txt, "html.parser")
    div_info = soup.find_all("div", class_ = "field-item even")
    
    for element in div_info:
        element_text = element.text.strip()
        if element_text:
            writer.writerow([element_text])
#=====================================================================================================================================================
# == For Paragraphs <p> == 
def text_scrape_p(link, writer):
    html_txt = requests.get(link).text
    soup = BeautifulSoup(html_txt, "html.parser")
    p_info = soup.find_all("p")
    
    for paragraph in p_info:
        paragraph_text = paragraph.text.strip()
        if paragraph_text:
            writer.writerow([paragraph_text])
#=====================================================================================================================================================
# == For Lists == 
def text_scrape_li(link, writer):
    html_txt = requests.get(link).text
    soup = BeautifulSoup(html_txt, "html.parser")
    list_items = soup.find_all("li")
    
    for item in list_items:
        item_text = item.text.strip()
        if item_text:
            writer.writerow([item_text])
#=====================================================================================================================================================
# == Grabs entire HTML of that page ==
def text_scrape_full(link, writer):
    html_txt = requests.get(link).text
    soup = BeautifulSoup(html_txt, "html.parser")
    
    for element in soup.find_all():
        element_text = element.text.strip()
        if element_text:
            writer.writerow([element_text])
#=====================================================================================================================================================
#Just need the first header
def text_scrape_title(link, writer):
    html_txt = requests.get(link).text
    soup = BeautifulSoup(html_txt, "html.parser")
    
    for element in soup.find("h1"):
        element_text = element.text.strip()
        if element_text:
            writer.writerow([element_text])
#=====================================================================================================================================================
def append_link_if_missing(image_link):
    base_link = "https://centropr-archive.hunter.cuny.edu"
    if not image_link.startswith(base_link):
        image_link = base_link + image_link
    return image_link

#====================================================================================================
#For timestamping image filenames so they don't overwrite over other images because of the same name
def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)
#====================================================================================================

def imagedown(link, path):
    try:
        os.makedirs(os.path.join(os.getcwd(), path))  # Use makedirs to create nested directories
    except FileExistsError:  # Catch specific exception
        pass

    os.chdir(os.path.join(os.getcwd(), path))

    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    images = soup.find_all("img")

    for image in images:
        name = image["alt"]
        link = image["src"]
        newlink = append_link_if_missing(link)
        print(newlink)

        filename = name + ".png"
        filename = make_unique_filename(filename)  # Ensure unique filename
        with open(timeStamped(filename), "wb") as f:
            im = requests.get(newlink)
            f.write(im.content)

def make_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    return filename

#=====================================================================================================================================================
# == MAIN ==    
#Usage: 4 for title header, then 1 for full text. Then Images. Other functions may be used as necessary.                                 

#Writer is file 
while True:
    select = int(input("Type a number for the class type to search:\n"
                   "1 for Title & Full Text : \n"
                   "2 for lists (ordered & unordered): \n"
                   "3 For Paragraphs <p> \n"
                   "4 For Images:\n "))
    link = input("\nInput website link: ")
    file_path = input("Enter file path: ")
    try:
        with open(file_path, "a+", newline='', encoding='ANSI') as csvfile:
            path = csv.writer(csvfile)
            if select == 1:
                text_scrape_title(link, path)   
                text_scrape_div(link, path)
            elif select == 2:
                text_scrape_li(link, path)
            elif select == 3:
                text_scrape_p(link, path)
            elif select == 4:
                imagedown(link, file_path)
                print("Image files successfully downloaded")
            else:
                print("Invalid option selected.")
            print("Data has been scraped and written to CSV successfully!")
    except Exception as e:
        if select == 4:
            print("An error has occurred with the image downloader:", e)
        else:
            print("An error occurred:", e)
    continue_option = input("Do you want to continue (yes/no)? ").lower()
    if continue_option != ('yes' or "y"):
        break
#=====================================================================================================================================================