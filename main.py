import urllib.request
import urllib.error
import re
import tkinter as tk
from PIL import Image, ImageTk

global url, result_var, imagePanel, checkmark, xmark

prefix = {"https://www", "http://www"}
postfix = {"com", "net", "ca"}


def webCheck(address):
    try:
        result = urllib.request.urlopen(address).status
    except ValueError as e:
        raise ValueError("Not a valid website URL") from e
    except urllib.error.URLError as e:
        raise ValueError("Connection Timeout - Website is down!") from e
    return result


def urlCheck(address):
    global xmark, imagePanel
    inputUrl = address.get()
    urlTest = inputUrl.split(".")
    x = re.search("http://...\.*.*", inputUrl)
    y = re.search("https://...\.*.*", inputUrl)
    z = re.search("https://...\.*.*/*", inputUrl)
    if ((urlTest[0] in prefix and len(urlTest) >= 3) or x or y) and urlTest[-1] in postfix:
        # print(inputUrl)
        result = webCheck(inputUrl)
        evaluation(result)
    else:
        result_var.set("Entry is not valid")
        imagePanel.configure(image=xmark)
        imagePanel.image = xmark
        # print("not valid")


def evaluation(code):
    global checkmark, xmark, imagePanel
    match code:
        case 200:
            result_var.set("The website is online!")
            imagePanel.configure(image=checkmark)
            imagePanel.image = checkmark
            # print("The website is online!")
        case 404:
            result_var.set("Website was not found")
            imagePanel.configure(image=xmark)
            imagePanel.image = xmark
            # print("Website was not found")
        case _:
            result_var.set("Unknown response")
            imagePanel.configure(image=xmark)
            imagePanel.image = xmark
            # print("Unknown response")


def main():
    global url, result_var, imagePanel, checkmark, xmark

    window = tk.Tk()
    window.title('Website Checker')

    ico = Image.open('website-icon.png')
    photo = ImageTk.PhotoImage(ico)
    window.wm_iconphoto(False, photo)

    checkmark = ImageTk.PhotoImage(Image.open('checkmark.png'))
    xmark = ImageTk.PhotoImage(Image.open('x-mark.png'))

    screen_width = window.winfo_screenwidth()
    screen_length = window.winfo_screenheight()
    centerX = int(screen_width/2 - 450)
    centerY = int(screen_length/2 - 250)
    window.geometry(f'900x500+{centerX}+{centerY}')
    window.resizable(False, False)
    window['background'] = '#9a9aa7'

    url_var = tk.StringVar()
    frame = tk.Frame(window, padx=10, pady=10)
    frame.pack(pady=20)
    frame['background'] = '#9a9aa7'

    tk.Label(frame, bg='#9a9aa7', text="Enter the website you want to check:").grid(row=0, column=0)
    tk.Entry(frame, textvariable=url_var).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(frame, width=15, text="Submit", command=lambda: urlCheck(url_var)).grid(row=2, column=0)

    result_var = tk.StringVar()
    result_var.set("")
    tk.Label(frame, bg='#9a9aa7', textvariable=result_var).grid(row=3, column=0, pady=50)
    imagePanel = tk.Label(frame, bg='#9a9aa7')
    imagePanel.grid(row=3, column=1, pady=50)

    window.bind('<Return>', lambda event: urlCheck(url_var))
    window.mainloop()


if __name__ == '__main__':
    main()
