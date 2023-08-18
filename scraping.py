from bs4 import BeautifulSoup
import requests
import csv
import re

url_name = ["outside", "drink", "inside", "menu", "food", "interior"]

tab_urls = {
    names: f"https://www.yelp.com/biz_photos/benemon-new-york?tab={names}"
    for names in url_name
}

def scrape_yelp_image(names):
    if names not in tab_urls:
        print("URL not found!")
        return []

    url = tab_urls[names]
    print("URL:", url)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    doc = BeautifulSoup(response.text, "html.parser")

    image_links = []
    image_elements = doc.find_all("img", class_="photo-box-img") 
    # since the photo is inside the div inside img inside srcset
    for img in image_elements:
        srcset = img.get("srcset")
        if srcset:
            urls = re.findall(r"https?://[^\s]+", srcset)
            image_links.extend([(names, url) for url in urls])  # Pairing the tab name with each URL to get the desired output 
    
    return image_links

if __name__ == '__main__':
    scraped_data = []
    
    for names in url_name:
        image_links = scrape_yelp_image(names)
        scraped_data.extend(image_links)  # Extend the list with tab-name-url pairs to get the desired output

    # Storing the data in a CSV file
    csv_filename = "yelp_images.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Tab Name", "Image Link"])  # Header row
        for tab_name, image_link in scraped_data:
            csv_writer.writerow([tab_name, image_link])  

    print("Data has been saved to", csv_filename)
