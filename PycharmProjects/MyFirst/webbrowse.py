import webbrowser

def validator(func):
    def wrapper(url):
        if url.startswith("http"):
            return func(url)
        else:
            print("Invalid URL")
    return wrapper

@validator
def open_url(url):
    webbrowser.open(url)


open_url("https://www.google.com")