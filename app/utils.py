import requests
from datetime import datetime
from app.constants import FINE_PER_DAY


def get_more_book_details(isbn):
    # return {}  # temporary

    url = (
        f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    )
    response = requests.get(url)
    data = response.json()
    print(data)

    if f"ISBN:{isbn}" in data:
        details = data[f"ISBN:{isbn}"]
        extra_data = {
            "subjects": [sub["name"] for sub in details.get("subjects", [])][:10],
            "subject_people": [
                person["name"] for person in details.get("subject_people", [])
            ][:5],
            "subject_places": [
                place["name"] for place in details.get("subject_places", [])
            ][:5],
            "links": details.get("links", []),
            "cover_img": details.get("cover", {}).get("large", ""),
            "number_of_pages": details.get("number_of_pages", ""),
            "publish_date": details.get("publish_date", ""),
            "ebooks": details.get("ebooks", []),
            "excerpts": details.get("excerpts", []),
        }

        return extra_data

    else:
        return {}


def calculate_total_fine(transactions):
    total_fine = 0
    today = datetime.now().date()  # Get today's date only
    for transaction in transactions:
        if transaction.return_date is None and transaction.due_date < today:
            days_late = (today - transaction.due_date).days
            fine = FINE_PER_DAY * days_late
            total_fine += fine
    return total_fine
