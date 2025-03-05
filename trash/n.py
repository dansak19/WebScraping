import requests

code = "158576702"

url = f"https://www.ceneo.pl/{code}#tab=reviews"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/",
}

response = requests.get(url, headers=headers)

html = response.text  # Get the HTML content

# Save it to a file and check manually
# with open("output.html", "w", encoding="utf-8") as f:
#     f.write(html)

# print("HTML saved! Open output.html and search for your div.")

url = "https://www.ceneo.pl/158576702/opinie-8"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/",
}

response = requests.get(url, headers=headers)

html = response.text  # Get the HTML content

# Save it to a file and check manually
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML saved! Open output.html and search for your div.")