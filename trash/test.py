from bs4 import BeautifulSoup
import requests
import re
import time
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/",
}

code = "74463012"

url = f"https://www.ceneo.pl/{code}#tab=reviews"

page = requests.get(url, headers=headers)
print(page)

soup = BeautifulSoup(page.text, features="html.parser")
# print(soup)
print(soup.title.get_text())
name = soup.find("h1", class_ = "product-top__product-info__name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor").text
print(name)
# comment_section = soup.find("div", class_ = "js_product-reviews js_reviews-hook js_product-reviews-container")
# print(comment_section)
# comments = comment_section.find_all("div", class_="user-post user-post__card js_product-review")
# print(len(comments))

comments = []

for comment in comments:
    op_id = re.findall("\\d+", str(comment.find("div", class_="js_product-review-form-hook")))
    if len(op_id):
        op_id = op_id[0]
    else: op_id = None
    print(op_id)
    print()
    
    author_name = comment.find("span", class_ = "user-post__author-name")
    if author_name:
        author_name = author_name.text.strip()
    else: author_name = None
    
    print(author_name)
    print()
    
    recomendation = comment.find("em", class_ = "recommended").text
    # <em class="recommended">Polecam</em>
    
    print(recomendation)
    print()
    # <span class="user-post__score-count">4,5/5</span>
    
    score = comment.find("span", class_ = "user-post__score-count")
    if score:
        score = float(score.text[:-2].replace(",", "."))
    print(score)
    print()
    
    content = comment.find("div", class_ = "user-post__text").text+"\n"
    # <div class="user-post__text">
    
    print(content.strip())
    print()
    # <div class="review-feature">
    # <div class="review-feature__section">
    # <div class="review-feature__item review-feature__item--positive" data-new-icon="check">
    adv  = comment.find_all("div", class_ = "review-feature__item review-feature__item--positive")
    j = []
    for i in adv:
        j.append(i.text)
    adv = j
    
    # review-feature__item review-feature__item--negative
    
    print(adv)
    print()
    
    disadv  = comment.find_all("div", class_ = "review-feature__item review-feature__item--negative")
    disadv = [i.text for i in disadv]

    
    print(disadv)
    print()
    
    
    # <button class="vote-yes js_product-review-vote js_vote-yes"
    # <button class="vote-no js_product-review-vote js_vote-no"
    
    likes = comment.find("button", class_ = "vote-yes js_product-review-vote js_vote-yes")
    likes = re.findall("\\d+", re.findall("data-total-vote=\"\\d+\"", str(likes))[0])[0]
    
    print(likes)
    
    dislikes = comment.find("button", class_ = "vote-no js_product-review-vote js_vote-no")
    dislikes = re.findall("\\d+", re.findall("data-total-vote=\"\\d+\"", str(dislikes))[0])[0]
    
    print(dislikes)
    
    time = comment.find_all("time")
    
    time_publish = re.findall("\".+ .+\"", str(time[0]))[0][1:-1]
    print(time_publish)
    if len(time) == 2:
        time_purchase = re.findall("\".+ .+\"", str(time[1]))[0][1:-1]
        print(time_purchase)
        
    print()
    
# reviews_number = int(soup.find("a", class_ = "product-review__link link link--accent js_reviews-link js_clickHash js_seoUrl").find("span").text)
# print(reviews_number)

# print(soup)