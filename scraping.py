from bs4 import BeautifulSoup
import requests
import csv
import re

url_name = ["outside", "drink", "inside", "menu", "food", "interior"]

tab_urls = {
    name: f"https://www.yelp.com/biz_photos/benemon-new-york?tab={name}"
    for name in url_name
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
    # Find the container for photo elements using CSS selector
    photo_container = doc.select("div.media-landing_gallery.photos")

    if photo_container:
        # Use .find_all() on the photo_container to get all photo-box elements
        image_elements = photo_container[0].find_all("div", class_="photo-box photo-box--interactive")

        for img in image_elements:
            # Use .select() to directly find the .photo-box-img element with the specific attribute
            srcset = img.select_one(".photo-box-img[width='226']")["srcset"]
            urls = re.findall(r"(https?://[^\s]+)\s+1\.35x", srcset)
            image_links.extend([(names, url) for url in urls])

        print(image_links)
        return image_links
    else:
        print("No image elements found for", names)
        return []

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
