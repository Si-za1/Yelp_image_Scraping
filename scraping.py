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
        print("Url not found!")
        return []

    url = tab_urls[names]
    print("url is", url)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    print(response)
    doc = BeautifulSoup(response.text, "html.parser")

    image_links = []
    image_elements = doc.find_all("img", class_="photo-box-img") 
    # since the photo is inside the div inside img inside srcset
    for img in image_elements:
        srcset = img.get("srcset")
        if srcset:
            urls = re.findall(r"https?://[^\s]+", srcset)
            image_links.append(urls[0])
    
    return image_links

if __name__ == '__main__':
    scraped_data = {}
    
    for names in url_name:
        image_links = scrape_yelp_image(names)
        scraped_data[names] = image_links

if __name__ == '__main__':
    scraped_data = {}
    
    for names in url_name:
        image_links = scrape_yelp_image(names)
        scraped_data[names] = image_links

    # Storing the data in a CSV file
    csv_filename = "yelp_images.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Tab Name", "Image Links"])
        for names, links in scraped_data.items():
            csv_writer.writerow([names, "\n".join(links)])

    print("Data has been saved to", csv_filename)

    
if __name__ == '__main__':
   
   for names in url_name:
        movies = scrape_yelp_image(names)
        print(f"URL in {names} links:")
        
        print("\n")