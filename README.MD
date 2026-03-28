# Url-Short

simple url shortener i built with flask and sqlite. paste a long url, get a short one. tracks how many times each link gets clicked.

## how it works

generates a random 6 character code, stores it in sqlite with the original url, redirects anyone who visits the short link to the original. click count goes up every time someone uses the link.

## stack

- python + flask
- sqlite for storing urls
- html css js frontend

## setup
```
git clone https://github.com/X-4bys5/url-short.git
cd url-short
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
run:
python app.py

go to http://localhost:5000

## known issues
```
- no expiry on links, they stay forever
- short codes are random so technically you could get a collision, theres a check for that but its still random
- no user accounts so anyone can delete any link
```