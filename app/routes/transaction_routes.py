from app import app, db
from flask import Flask, render_template, request, redirect, flash, url_for
from app.model.Transaction import Transaction

import requests


# def get_book_summary(isbn):
#     base_url = "https://www.googleapis.com/books/v1/volumes"
#     params = {"q": f"isbn:{isbn}"}

#     response = requests.get(base_url, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#         if "items" in data and len(data["items"]) > 0:
#             book_info = data["items"][0]["volumeInfo"]
#             title = book_info.get("title", "Title not available")
#             summary = book_info.get("description", "Summary not available")
#             return title, summary
#         else:
#             return "Book not found", ""
#     else:
#         return "Error fetching data", ""


# isbn = "3570211029"
# title, summary = get_book_summary(isbn)
# print(f"Title: {title}")
# print(f"Summary: {summary}")
