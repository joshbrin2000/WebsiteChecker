#!/usr/bin/env python3

"""Website Checker: takes user input, checks if valid url, then returns status code of 
   website server
"""

import urllib.request
import urllib.error
import tkinter as tk
from PIL import Image, ImageTk
import sql_features
from datetime import datetime

result_var = None
imagePanel = None
checkmark = None
xmark = None
history_var = None

prefix = {"https://www", "http://www", "https://", "http://"}
postfix = {"com", "net", "ca", "edu"}

def webCheck(address):
    """_summary_

    Args:
        address (str): website address in URL format

    Raises:
        ValueError: if address does not adhere to basic URL format
        ValueError: if website is down

    Returns:
        int: status code of website
    """
    try:
        result = urllib.request.urlopen(address).status
    except ValueError as e:
        raise ValueError("Not a valid website URL") from e
    except urllib.error.URLError as e:
        raise ValueError("Connection Timeout - Website is down!") from e
    return result


def urlCheck(address):
    """Checks if input is in url format

    Args:
        address (str): string of web address
    """
    inputUrl = address.get()
    urlTest = inputUrl.split(".")
    endCheck = urlTest[-1].split("/")

    if urlTest[0] in prefix and len(urlTest) >= 3 and endCheck[0] in postfix:
        result = webCheck(inputUrl)
        evaluation(result, inputUrl)
    else:
        result_var.set("Entry is not valid")
        imagePanel.configure(image=xmark)
        imagePanel.image = xmark
    num_lines = min(sum(1 for _ in open('output.txt', 'r')), 5)
    sqlReading()


def evaluation(code, inputUrl):
    """checks status code and displays relavant message and checkmark/
       xmark

    Args:
        code (int): server status code
        inputUrl (str): url string submitted by user
    """
    match code:
        case 200:
            result_var.set("The website is online!")
            imagePanel.configure(image=checkmark)
            imagePanel.image = checkmark
        case 203:
            result_var.set("The website is online! NAI - content accessed from third-party")
            imagePanel.configure(image=checkmark)
            imagePanel.image = checkmark
        case 300:
            result_var.set("URL too unspecific")
            imagePanel.configure(image=checkmark)
            imagePanel.image = checkmark
        case 400:
            result_var.set("Bad request - URL may have poor syntax")
            imagePanel.configure(image=checkmark)
            imagePanel.image = checkmark
        case 401:
            result_var.set("Unauthorized Access")
            imagePanel.configure(image=checkmark)
            imagePanel.image = checkmark
        case 403:
            result_var.set("Forbidden - No Access Allowed")
            imagePanel.configure(image=checkmark)
            imagePanel.image = checkmark
        case 404:
            result_var.set("Website was not found")
            imagePanel.configure(image=xmark)
            imagePanel.image = xmark
        case _:
            result_var.set("Unknown response")
            imagePanel.configure(image=xmark)
            imagePanel.image = xmark
    sqlWriting(inputUrl)


def sqlWriting(urlString):
    sql_features.insertTable(urlString, result_var.get())


def sqlReading():
    history_var.set('')
    result = sql_features.selectNTable(5)
    for i in result:
        history_var.set(history_var.get() + f'{i[1]}    {i[2]}    {i[3].strftime("%Y-%m-%d %H:%M:%S")}\n')


def fileWriting(urlString):
    """writes url string to .txt file for history

    Args:
        urlString (str): url address
    """
    with open("output.txt", 'a') as file:
        file.writelines(f'{urlString}:      {result_var.get()}\n')


def lastNLines(fileName, n):
    """sets history variable to up to last n entries in file

    Args:
        fileName (str): string of file name
        n (int): number of lines to display
    """
    history_var.set('')
    with open(fileName, 'r') as f:
        for i in (f.readlines()[-n:]):
            history_var.set(history_var.get() + i + '\n')


def finishUp(root):
    sql_features.closeSQL()
    root.destroy()


def main():
    """sets up TKinter layout
    """
    global result_var, imagePanel, checkmark, xmark, history_var

    sql_features.databaseInit()
    sql_features.tableInit()
    
    window = tk.Tk()
    window.title('Website Checker')

    url_var = tk.StringVar()
    result_var = tk.StringVar()
    history_var = tk.StringVar()
    
    sqlReading()

    ico = Image.open('resources/img/website-icon.png')
    photo = ImageTk.PhotoImage(ico)
    window.wm_iconphoto(False, photo)

    checkmark = ImageTk.PhotoImage(Image.open('resources/img/checkmark.png'))
    xmark = ImageTk.PhotoImage(Image.open('resources/img/x-mark.png'))

    screen_width = window.winfo_screenwidth()
    screen_length = window.winfo_screenheight()
    centerX = int(screen_width / 2 - 300)
    centerY = int(screen_length / 2 - 300)
    window.geometry(f'600x600+{centerX}+{centerY}')
    window.resizable(False, False)
    window['background'] = '#9a9aa7'

    frameMain = tk.Frame(window, padx=10, pady=10)
    frameMain.pack()
    frameMain['background'] = '#9a9aa7'

    tk.Label(frameMain, bg='#9a9aa7', text="Enter the website you want to check:",
             font=('Times New Roman', 20)).grid(row=0, column=0, pady=(25, 10))
    tk.Entry(frameMain, width=25, textvariable=url_var).grid(row=1, column=0, padx=10, pady=(0, 5))
    tk.Button(frameMain, width=15, height=2, text="Submit", font=('Times New Roman', 10),
              command=lambda: urlCheck(url_var)).grid(row=2, column=0)

    frame1 = tk.Frame(window, padx=10, pady=10)
    frame1.pack(padx=10)
    frame1['background'] = '#9a9aa7'

    tk.Label(frame1, bg='#9a9aa7', textvariable=result_var).grid(row=0, column=0, padx=30)
    imagePanel = tk.Label(frame1, bg='#9a9aa7')
    imagePanel.grid(row=0, column=1)

    frame2 = tk.Frame(window, padx=10, pady=10)
    frame2.pack(padx=10)
    frame2['background'] = '#9a9aa7'

    tk.Label(frame2, bg='#9a9aa7', text="History", font=('Times New Roman', 20))\
        .grid(row=0, column=0)
    tk.Label(frame2, bg='#9a9aa7', textvariable=history_var).grid(row=1, column=0)

    window.bind('<Return>', lambda event: urlCheck(url_var))
    
    window.protocol("WM_DELETE_WINDOW", lambda arg=window: finishUp(arg))
    window.mainloop()


if __name__ == '__main__':
    main()
