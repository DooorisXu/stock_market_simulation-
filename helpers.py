import csv
import urllib.request

from flask import redirect, render_template, request, session, url_for
from functools import wraps

#define the function apology 
#the top and bottom will be in the url 
#the default for top/bottom is blank 

def apology(top="", bottom=""):
    """Renders message as an apology to user."""
    #define the function escape 
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        for loop, replace "-" with "--" etc.
        the replace function replaces what we put into the url (that may break the url)
        or example, ? (can break the url) is replaced by ~q (which is fine)
        therefore, our input into the url will not break the url address 
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
            #why return a dash?
        return s
    return render_template("apology.html", top=escape(top), bottom=escape(bottom))

'''
print vs return
https://www.youtube.com/watch?v=Mj0YwdiaViM
'''
#why do we need to use wraps?
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def lookup(symbol):
    """Look up quote for symbol."""

    # reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None

    # reject symbol if it contains comma
    if "," in symbol:
        return None

    # query Yahoo for quote
    # http://stackoverflow.com/a/21351911
    try:
        #.format method puts symbol into the {}
        url = "http://download.finance.yahoo.com/d/quotes.csv?f=snl1&s={}".format(symbol)
        
        webpage = urllib.request.urlopen(url)
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())
        row = next(datareader)
    except:
        return None

    # ensure stock exists
    try:
        price = float(row[2])
    except:
        return None

    # return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
    return {
        "name": row[1],
        "price": price,
        "symbol": row[0].upper()
    }

def usd(value):
    """Formats value as USD."""
    return "${:,.2f}".format(value)
