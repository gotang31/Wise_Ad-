from getUrl import *
from getInfo import *
import os
from urllib.request import urlretrieve, urlopen
import re


def clean_filename(title):
    cleaned_title = re.sub(r'[\/:*?"<>|\s]', '', title)
    return cleaned_title


def extract_jpeg_urls(soup):
    # Convert the soup object to a string
    html_content = str(soup)

    # Use regular expression to find all occurrences of "origin":"//(image URL).jpeg"
    # and capture only the //(image URL).jpeg part
    matches = re.findall(r'"origin":"(//[^"]+)"', html_content)

    # Return the list of extracted .jpeg URLs
    return matches


def downloadimg(df):
    for index, row in df.iterrows():
        link = row['Link']
        # df['Name'] 값을 clean_filename 함수를 통해 정제
        name = clean_filename(row['Name'])

        text = (getres(link))
        soup = BeautifulSoup(text, 'html5lib')
        html_content = str(soup)
        jpeg_urls = extract_jpeg_urls(html_content)


        fdir = f'.//data//sweatshirt//{name}'
        if not os.path.exists(fdir):
            os.makedirs(fdir)

        for urls in jpeg_urls:
            img_url = f'https:{urls}'
            try:
                filename = urls.split('/')[-1]
                file_path = os.path.join(fdir, filename)

                urlretrieve(img_url, file_path)
                print(f"Downloaded {filename}")

            except Exception as e:
                print(f"Error downloading {filename}: {e}")