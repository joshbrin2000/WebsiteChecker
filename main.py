import urllib.request
import urllib.error
import re

prefix = {"https://www", "http://www"}
postfix = {"com", "net", "ca"}


def webCheck(address):
    print(address)
    try:
        result = urllib.request.urlopen(address).status
    except ValueError as e:
        raise ValueError("Not a valid website URL") from e
    except urllib.error.URLError as e:
        raise ValueError("Connection Timeout - Website is down!") from e
    return result


def urlCheck(address):
    urlTest = address.split(".")
    # print(f"{urlTest[0]} and {urlTest[-1]}")
    x = re.search("http://...\.*.*", url)
    y = re.search("https://...\.*.*", url)
    if ((urlTest[0] in prefix and len(urlTest) >= 3) or x or y) and urlTest[-1] in postfix:
        return False
    else:
        return True


def main():
    global url
    loop = True
    while loop:
        url = input("Enter website: ")
        loop = urlCheck(url)
    result = webCheck(url)
    match result:
        case 200:
            print("The server is online!")
        case _:
            print("Unknown response")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
