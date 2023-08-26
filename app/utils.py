import requests


def get_more_book_details(isbn):
    url = (
        f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    )
    response = requests.get(url)
    data = response.json()

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
            "ebooks": details.get("ebooks", []),
            "excerpts": details.get("excerpts", []),
        }

        return extra_data

    else:
        return {}


# isbn = (
#     "9780590353427"  # Replace with the ISBN of the book you want to fetch details for
# )
# book_details = get_book_details(isbn)
# if book_details:
#     print(book_details)
#     # print("Title:", book_details["title"])
#     # print("Author:", book_details["authors"][0]["name"])
#     # print("Publication Date:", book_details["publish_date"])
#     # Add more details as needed
# else:
#     print("Book details not found.")
