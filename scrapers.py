import requests
import json
import re
from datetime import date
from slack_webhook import Slack
from slack_sdk import WebClient
import mysql.connector
import urllib
from getpass import getpass
from mysql.connector import connect, Error
import json
from datetime import datetime
from argparse import ArgumentParser
from os.path import join, dirname, realpath
import time
import shutil
import base64
import os
import sys
import ast
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time

chromedriver_path = "/usr/bin/chromedriver"  # Adjust this path to your chromedriver location
# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
socks5_proxy = "socks5://127.0.0.1:9050"  # Update with your proxy details
chrome_options.add_argument(f"--proxy-server={socks5_proxy}")

# Initialize the Chrome driver
driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
screenshot_directory = "./screenshots/"

def scrape_qilin(victim_name, short_location):
    short_location = "http://" + short_location
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Find all divs with class 'col-md-10 mb-2'
    divs = soup.find_all('div', class_='col-md-10 mb-2')

    # Iterate through each div
    for div in divs:
        # Find the <a> tag with the class 'item_box-title mb-2 mt-1'
        a_tag = div.find('a', class_='item_box-title mb-2 mt-1')
        if a_tag:
            # Check if the text matches the victim_name
            if a_tag.get_text(strip=True) == victim_name:
                # Print the href attribute
                print(a_tag['href'])

                victim_site = a_tag['href']
                #
                screenshot_url = short_location + str(victim_site)
                screenshot_filename = f'{victim_name}.png'
                screenshot_path = os.path.join(screenshot_directory, screenshot_filename)
                print(f"the full url to the site is {screenshot_url}")
                driver.get(screenshot_url)
                time.sleep(5)
                # Get the page dimensions
                page_height = driver.execute_script("return document.body.scrollHeight")
                page_width = driver.execute_script("return document.body.scrollWidth")

                # Set the window size to the full page dimensions
                driver.set_window_size(page_width, page_height)

                # Take the screenshot and save it
                driver.get_screenshot_as_file(screenshot_path)

                print(f"Screenshot saved to {screenshot_path}")

                # Close the browser
                driver.quit()
def scrape_cicada3301(victim_name, short_location):
    short_location = "http://" + short_location
    print(f"Scraping {short_location}")
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Find all div elements with the specified class
    divs = soup.find_all('div', class_='w-full sm:w-1/2 md:w-1/2 lg:w-1/3 xl:w-1/3 px-6 mb-12')
    victim_site = ""
    for div in divs:
        # Find the h2 element within the div
        h2 = div.find('h2', class_='font-bold text-yellow-500 mb-4 break-words uppercase')
        if h2 and h2.get_text(strip=True) == victim_name:
            # Find the a tag within the div
            a = div.find('a',
                         class_='inline-flex items-center justify-center bg-gray-900 text-white py-2 px-4 border border-gray-600 hover:border-gray-400 rounded shadow hover:shadow-md transform hover:scale-105 transition ease-in-out duration-300 text-sm font-medium absolute bottom-0 right-0 mb-3 mr-6')
            if a:
                # Print the href attribute
                print(a.get('href'))
                victim_site = a.get('href')

                screenshot_url = short_location + str(victim_site)
                screenshot_filename = f'{victim_name}.png'
                screenshot_path = os.path.join(screenshot_directory, screenshot_filename)
                print(f"the full url to the site is {screenshot_url}")
                driver.get(screenshot_url)
                time.sleep(5)
                # Get the page dimensions
                page_height = driver.execute_script("return document.body.scrollHeight")
                page_width = driver.execute_script("return document.body.scrollWidth")

                # Set the window size to the full page dimensions
                driver.set_window_size(page_width, page_height)

                # Take the screenshot and save it
                driver.get_screenshot_as_file(screenshot_path)

                print(f"Screenshot saved to {screenshot_path}")

                # Close the browser
                driver.quit()

def scrape_spacebears(victim_name, short_location):
    short_location = "http://" + short_location
    print(short_location)
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find all div elements with class "name"
    divs = soup.find_all('div', class_='name')

    # Iterate through each div
    for div in divs:
        # Find the 'a' tag inside the div
        a_tag = div.find('a')

        # Check if the text matches the victim_name
        if a_tag and a_tag.text.strip() == victim_name:
            # Print the href attribute
            print(a_tag['href'])

            screenshot_url = a_tag['href']
            print(f"the full url to the site is {screenshot_url}")
            # print(screenshot_url)
            driver.get(screenshot_url)
            time.sleep(4)

            # Get the dimensions of the page
            total_height = driver.execute_script("return document.body.scrollHeight")
            total_width = driver.execute_script("return document.body.scrollWidth")
            viewport_height = driver.execute_script("return window.innerHeight")
            viewport_width = driver.execute_script("return window.innerWidth")

            # Set the window size to the total page width and viewport height
            driver.set_window_size(total_width, viewport_height)

            # Scroll and take screenshots
            screenshot_path = f"./screenshots/{victim_name}.png"
            screenshots = []

            for y in range(0, total_height, viewport_height):
                for x in range(0, total_width, viewport_width):
                    driver.execute_script(f"window.scrollTo({x}, {y});")
                    time.sleep(0.2)  # Adjust time if needed
                    screenshot = driver.get_screenshot_as_file(f"screenshot_{x}_{y}.png")
                    screenshots.append((x, y, f"screenshot_{x}_{y}.png"))

            # Create a blank image with the total width and height of the page
            stitched_image = Image.new('RGB', (total_width, total_height))

            # Paste all the screenshots together
            for x, y, path in screenshots:
                screenshot_image = Image.open(path)
                stitched_image.paste(screenshot_image, (x, y))

            # Save the final image
            stitched_image.save(screenshot_path)

            # Clean up temporary screenshots
            for _, _, path in screenshots:
                os.remove(path)

            # Close the browser
            driver.quit()

def scrape_hunters(victim_name, short_location):
    ###NOT WORKING YET
    print(short_location)
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Iterate through each <div class="card">
    for card in soup.find_all('div', class_='card'):
        # Find the <div class="title"> element
        title_div = card.find('div', class_='title')
        if title_div:
            # Find the <a> tag within the <div class="title">
            a_tag = title_div.find('a')
            if a_tag and title_div.get_text(strip=True) == victim_name:
                # Print the href attribute
                victim_site = a_tag['href']
                victim_site = victim_site.strip()
                print(a_tag['href'])

                screenshot_url = short_location + "/" + victim_site
                print(f"the full url to the site is {screenshot_url}")
                print(screenshot_url)
                driver.get(screenshot_url)
                time.sleep(4)

                # Get the dimensions of the page
                total_height = driver.execute_script("return document.body.scrollHeight")
                total_width = driver.execute_script("return document.body.scrollWidth")
                viewport_height = driver.execute_script("return window.innerHeight")
                viewport_width = driver.execute_script("return window.innerWidth")

                # Set the window size to the total page width and viewport height
                driver.set_window_size(total_width, viewport_height)

                # Scroll and take screenshots
                screenshot_path = f"./screenshots/{victim_name}.png"
                screenshots = []

                for y in range(0, total_height, viewport_height):
                    for x in range(0, total_width, viewport_width):
                        driver.execute_script(f"window.scrollTo({x}, {y});")
                        time.sleep(0.2)  # Adjust time if needed
                        screenshot = driver.get_screenshot_as_file(f"screenshot_{x}_{y}.png")
                        screenshots.append((x, y, f"screenshot_{x}_{y}.png"))

                # Create a blank image with the total width and height of the page
                stitched_image = Image.new('RGB', (total_width, total_height))

                # Paste all the screenshots together
                for x, y, path in screenshots:
                    screenshot_image = Image.open(path)
                    stitched_image.paste(screenshot_image, (x, y))

                # Save the final image
                stitched_image.save(screenshot_path)

                # Clean up temporary screenshots
                for _, _, path in screenshots:
                    os.remove(path)

                # Close the browser
                driver.quit()
def scrape_eldorado(victim_name, short_location):
    short_location = "http://" + short_location
    print(short_location)
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    # Find all <article> elements with the specified class
    articles = soup.find_all('article', class_='p-6 dark:text-white lg:flex')

    for article in articles:
        # Find the <h1> element inside the article
        h1 = article.find('h1', class_='text-xl mb-2 text-decoration-underline')
        if h1 and h1.text.strip() == victim_name:
            # Find the <a> tag inside the article
            a_tag = article.find('a', href=True)
            if a_tag:
                print(a_tag['href'])
                screenshot_url = a_tag['href']
                # # screenshot_url = short_location + "/" +  victim_site
                print(f"the full url to the site is {screenshot_url}")
                # print(screenshot_url)
                driver.get(screenshot_url)
                time.sleep(4)

                # Get the dimensions of the page
                total_height = driver.execute_script("return document.body.scrollHeight")
                total_width = driver.execute_script("return document.body.scrollWidth")
                viewport_height = driver.execute_script("return window.innerHeight")
                viewport_width = driver.execute_script("return window.innerWidth")

                # Set the window size to the total page width and viewport height
                driver.set_window_size(total_width, viewport_height)

                # Scroll and take screenshots
                screenshot_path = f"./screenshots/{victim_name}.png"
                screenshots = []

                for y in range(0, total_height, viewport_height):
                    for x in range(0, total_width, viewport_width):
                        driver.execute_script(f"window.scrollTo({x}, {y});")
                        time.sleep(0.2)  # Adjust time if needed
                        screenshot = driver.get_screenshot_as_file(f"screenshot_{x}_{y}.png")
                        screenshots.append((x, y, f"screenshot_{x}_{y}.png"))

                # Create a blank image with the total width and height of the page
                stitched_image = Image.new('RGB', (total_width, total_height))

                # Paste all the screenshots together
                for x, y, path in screenshots:
                    screenshot_image = Image.open(path)
                    stitched_image.paste(screenshot_image, (x, y))

                # Save the final image
                stitched_image.save(screenshot_path)

                # Clean up temporary screenshots
                for _, _, path in screenshots:
                    os.remove(path)

                # Close the browser
                driver.quit()

def scrape_handala(victim_name, short_location):
    short_location = "https://" + short_location
    # print(short_location)
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find all <h2> elements with class "wp-block-post-title"
    h2_elements = soup.find_all('h2', class_='wp-block-post-title')

    for h2 in h2_elements:
        a_tag = h2.find('a')
        if a_tag and a_tag.text.strip() == victim_name:
            print(a_tag['href'])
            screenshot_url = a_tag['href']
            # screenshot_url = short_location + "/" +  victim_site
            print(f"the full url to the site is {screenshot_url}")
            # print(screenshot_url)
            driver.get(screenshot_url)
            time.sleep(4)

            # Get the dimensions of the page
            total_height = driver.execute_script("return document.body.scrollHeight")
            total_width = driver.execute_script("return document.body.scrollWidth")
            viewport_height = driver.execute_script("return window.innerHeight")
            viewport_width = driver.execute_script("return window.innerWidth")

            # Set the window size to the total page width and viewport height
            driver.set_window_size(total_width, viewport_height)

            # Scroll and take screenshots
            screenshot_path = f"./screenshots/{victim_name}.png"
            screenshots = []

            for y in range(0, total_height, viewport_height):
                for x in range(0, total_width, viewport_width):
                    driver.execute_script(f"window.scrollTo({x}, {y});")
                    time.sleep(0.2)  # Adjust time if needed
                    screenshot = driver.get_screenshot_as_file(f"screenshot_{x}_{y}.png")
                    screenshots.append((x, y, f"screenshot_{x}_{y}.png"))

            # Create a blank image with the total width and height of the page
            stitched_image = Image.new('RGB', (total_width, total_height))

            # Paste all the screenshots together
            for x, y, path in screenshots:
                screenshot_image = Image.open(path)
                stitched_image.paste(screenshot_image, (x, y))

            # Save the final image
            stitched_image.save(screenshot_path)

            # Clean up temporary screenshots
            for _, _, path in screenshots:
                os.remove(path)

            # Close the browser
            driver.quit()

def scrape_darkvault(victim_name, short_location):
    short_location = "http://" + short_location
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    # Find all div elements with class "post-block"
    post_blocks = soup.find_all('div', class_='post-block')

    # Iterate through each post-block div
    for post_block in post_blocks:
        # Find the post-title div within the post-block
        post_title = post_block.find('div', class_='post-title')

        # Check if post_title exists and its text matches the victim_name
        if post_title and victim_name.lower() == post_title.text.strip().lower():
            # Print the matching post title
            print("Matching post title:", post_title.text.strip())

            # Extract the link from the onclick attribute of the post-block div
            onclick_value = post_block.get('onclick', '')
            victim_site = onclick_value.split("'")[1] if "'" in onclick_value else "Link not found"
            print("Link:", victim_site)
            print("---")

            screenshot_url = short_location + victim_site
            driver.get(screenshot_url)
            time.sleep(2)

            # Get the dimensions of the page
            total_height = driver.execute_script("return document.body.scrollHeight")
            total_width = driver.execute_script("return document.body.scrollWidth")
            viewport_height = driver.execute_script("return window.innerHeight")
            viewport_width = driver.execute_script("return window.innerWidth")

            # Set the window size to the total page width and viewport height
            driver.set_window_size(total_width, viewport_height)

            # Scroll and take screenshots
            screenshot_path = f"./screenshots/{victim_name}.png"
            screenshots = []

            for y in range(0, total_height, viewport_height):
                for x in range(0, total_width, viewport_width):
                    driver.execute_script(f"window.scrollTo({x}, {y});")
                    time.sleep(0.2)  # Adjust time if needed
                    screenshot = driver.get_screenshot_as_file(f"screenshot_{x}_{y}.png")
                    screenshots.append((x, y, f"screenshot_{x}_{y}.png"))

            # Create a blank image with the total width and height of the page
            stitched_image = Image.new('RGB', (total_width, total_height))

            # Paste all the screenshots together
            for x, y, path in screenshots:
                screenshot_image = Image.open(path)
                stitched_image.paste(screenshot_image, (x, y))

            # Save the final image
            stitched_image.save(screenshot_path)

            # Clean up temporary screenshots
            for _, _, path in screenshots:
                os.remove(path)

            # Close the browser
            driver.quit()
def scrape_danon(victim_name, short_location):
    short_location = "http://" + short_location
    print(short_location)
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)
    html = driver.page_source

    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    # Find all <h6> elements with class "card-title"
    # Find all <div class="col-md-5 mt-3">
    div_elements = soup.find_all('div', class_='col-md-5 mt-3')

    # Iterate through each div element
    for div in div_elements:
        # Find the h6 element with class "card-title"
        h6_element = div.find('h6', class_='card-title')

        # Check if the text matches the target text
        if h6_element and h6_element.text.strip() == victim_name:
            # Find the a element within the corresponding counter-container div
            counter_container = div.find('div', class_='counter-container')
            if counter_container:
                a_element = counter_container.find('a')
                if a_element and a_element.has_attr('href'):
                    victim_site = a_element['href']
                    # print(a_element['href'])
                    # Open the page
                    screenshot_url = short_location + victim_site
                    driver.get(screenshot_url)
                    time.sleep(2)

                    # Get the dimensions of the page
                    total_height = driver.execute_script("return document.body.scrollHeight")
                    total_width = driver.execute_script("return document.body.scrollWidth")
                    viewport_height = driver.execute_script("return window.innerHeight")
                    viewport_width = driver.execute_script("return window.innerWidth")

                    # Set the window size to the total page width and viewport height
                    driver.set_window_size(total_width, viewport_height)

                    # Scroll and take screenshots
                    screenshot_path = f"./screenshots/{victim_name}.png"
                    screenshots = []

                    for y in range(0, total_height, viewport_height):
                        for x in range(0, total_width, viewport_width):
                            driver.execute_script(f"window.scrollTo({x}, {y});")
                            time.sleep(0.2)  # Adjust time if needed
                            screenshot = driver.get_screenshot_as_file(f"screenshot_{x}_{y}.png")
                            screenshots.append((x, y, f"screenshot_{x}_{y}.png"))

                    # Create a blank image with the total width and height of the page
                    stitched_image = Image.new('RGB', (total_width, total_height))

                    # Paste all the screenshots together
                    for x, y, path in screenshots:
                        screenshot_image = Image.open(path)
                        stitched_image.paste(screenshot_image, (x, y))

                    # Save the final image
                    stitched_image.save(screenshot_path)

                    # Clean up temporary screenshots
                    for _, _, path in screenshots:
                        os.remove(path)

                    # Close the browser
                    driver.quit()

def scrape_play(victim_name, short_location):
    victim_found = 0
    short_location = "http://" + short_location
    print(short_location)
    driver.get(short_location)
    html = driver.page_source
    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Find all <th> elements with an onclick attribute
    th_elements = soup.find_all('th', onclick=True)

    # Iterate through each <th> element
    for th in th_elements:
        # Extract the text directly inside <th> and exclude nested elements
        text = ''.join(th.find_all(text=True, recursive=False)).strip()

        # Extract the viewtopic ID using regex
        onclick_value = th['onclick']
        match = re.search(r"viewtopic\('([^']+)'\)", onclick_value)
        viewtopic_id = match.group(1) if match else 'Not found'

        # Check if the text matches the victim_name variable
        if victim_name == text and "viewtopic('" in onclick_value:
            # Print or process the matching text and viewtopic ID
            print(f"Match Found: {text}")
            print(f"Viewtopic ID: {viewtopic_id}")
            # victim_found = 1
            screenshot_filename = f'{victim_name}.png'
            screenshot_path = os.path.join(screenshot_directory, screenshot_filename)
            #
            # # Ensure the screenshots directory exists
            os.makedirs(screenshot_directory, exist_ok=True)
            #
            # # Take a screenshot and save it to the specified path
            screenshot_url = short_location + "/topic.php?id=" + viewtopic_id
            print(f"SCreenshotting url: {screenshot_url}")
            time.sleep(2)
            # # Get the full page height and width
            page_height = driver.execute_script("return document.body.scrollHeight")
            page_width = driver.execute_script("return document.body.scrollWidth")
            driver.set_window_size(page_width, page_height)
            #
            # # Set the window size to full page height
            driver.get(screenshot_url)
            driver.get_screenshot_as_file(screenshot_path)
            #
            print(f"Screenshot saved to {screenshot_path}")

def scrape_cactus(victim_name, short_location):
    short_location = "https://" + str(short_location)
    short_location = extract_url(short_location)
    short_location = short_location.replace('[', '')
    short_location = short_location.replace(']', '')
    short_location = short_location.replace('\'', '')


    print(short_location)
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
    # Find all divs with the class "card-title text-center"
    titles = soup.find_all("a", class_="before:absolute before:inset-0")
    print(f"Looking for victim {victim_name}")
    for title in titles:
        print(title.get_text(strip=True))
    # print(titles)
    # # Iterate through all titles to find the one that matches the desired text
    # for title in titles:
    #     print(title)
    #     if victim_name in title.get_text():
    #         # Find the parent 'a' tag to get the href attribute
    #         a_tag = title.find_parent("a")
    #         if a_tag and a_tag.has_attr('href'):
    #                 print(a_tag['href'])

    # screenshot_filename = f'{victim_name}.png'
    # screenshot_path = os.path.join(screenshot_directory, screenshot_filename)
    #
    # # Ensure the screenshots directory exists
    # os.makedirs(screenshot_directory, exist_ok=True)
    #
    # # Take a screenshot and save it to the specified path
    # screenshot_url = short_location + "/" + a_tag['href']
    # time.sleep(2)
    # # Get the full page height and width
    # page_height = driver.execute_script("return document.body.scrollHeight")
    # page_width = driver.execute_script("return document.body.scrollWidth")
    # driver.set_window_size(page_width, page_height)
    #
    # # Set the window size to full page height
    # driver.get(screenshot_url)
    # driver.get_screenshot_as_file(screenshot_path)
    #
    # print(f"Screenshot saved to {screenshot_path}")
def scrape_bianlian(victim_name, short_location):
    short_location = "http://" + short_location
    print(f"Short Location {short_location}")
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Find the <main class="list"> element
    main_list = soup.find('main', class_='list')
    # Iterate through each <section class="list-item">
    for section in main_list.find_all('section', class_='list-item'):
        # Find the <h1 class="title"> element
        h1_title = section.find('h1', class_='title')
        if h1_title and h1_title.get_text(strip=True) == victim_name:
            # Find the <a> tag within the <h1 class="title">
            a_tag = h1_title.find('a')
            if a_tag:
                # Print the href attribute
                # print(a_tag['href'])
                victim_site = a_tag['href']

            screenshot_url = short_location + victim_site
            print(f"Screenshot URL {screenshot_url}")

            driver.get(screenshot_url)
            time.sleep(2)

            # Get the dimensions of the page
            total_height = driver.execute_script("return document.body.scrollHeight")
            total_width = driver.execute_script("return document.body.scrollWidth")
            viewport_height = driver.execute_script("return window.innerHeight")
            viewport_width = driver.execute_script("return window.innerWidth")

            # Set the window size to the total page width and viewport height
            driver.set_window_size(total_width, viewport_height)

            # Scroll and take screenshots
            screenshot_path = f"./screenshots/{victim_name}.png"
            screenshots = []

            for y in range(0, total_height, viewport_height):
                for x in range(0, total_width, viewport_width):
                    driver.execute_script(f"window.scrollTo({x}, {y});")
                    time.sleep(0.2)  # Adjust time if needed
                    screenshot = driver.get_screenshot_as_file(f"screenshot_{x}_{y}.png")
                    screenshots.append((x, y, f"screenshot_{x}_{y}.png"))

            # Create a blank image with the total width and height of the page
            stitched_image = Image.new('RGB', (total_width, total_height))

            # Paste all the screenshots together
            for x, y, path in screenshots:
                screenshot_image = Image.open(path)
                stitched_image.paste(screenshot_image, (x, y))

            # Save the final image
            stitched_image.save(screenshot_path)

            # Clean up temporary screenshots
            for _, _, path in screenshots:
                os.remove(path)

            # Close the browser
            driver.quit()

def scrape_blacksuit(victim_name, short_location):
    victim_name_short = victim_name.replace('https://', '')
    victim_name_short = victim_name_short.replace('http://','')
    print("$$$$$$$$$$$$$$$$$$$$$$")
    print(f"Updated Victim Name: {victim_name_short}")
    short_location = "http://" + short_location
    print(f"Short Location {short_location}")
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Find all div elements with class "title"
    divs = soup.find_all('div', class_='title')

    # Iterate through each div
    for div in divs:
        # Find the 'a' tag inside the div
        a_tag = div.find('a')
        print(f"victim name {victim_name}")
        print(f"post name {a_tag}")
        # Check if the text matches the victim_name
        if a_tag and victim_name_short in a_tag.text.strip():
            # Print the href attribute
            print(a_tag['href'])
            victim_site = a_tag['href']
            print("Match found on site!")
            screenshot_url = short_location + "/" + victim_site

            print(f"the full url to the site is {screenshot_url}")
            print(screenshot_url)
            driver.get(screenshot_url)
            time.sleep(4)

            # Get the dimensions of the page
            total_height = driver.execute_script("return document.body.scrollHeight")
            total_width = driver.execute_script("return document.body.scrollWidth")
            viewport_height = driver.execute_script("return window.innerHeight")
            viewport_width = driver.execute_script("return window.innerWidth")

            # Set the window size to the total page width and viewport height
            driver.set_window_size(total_width, viewport_height)

            # Scroll and take screenshots
            screenshot_path = f"./screenshots/{victim_name_short}.png"
            print(f"saving file to {screenshot_path}")
            screenshots = []

            for y in range(0, total_height, viewport_height):
                for x in range(0, total_width, viewport_width):
                    driver.execute_script(f"window.scrollTo({x}, {y});")
                    time.sleep(0.2)  # Adjust time if needed
                    screenshot = driver.get_screenshot_as_file(f"screenshot_{x}_{y}.png")
                    screenshots.append((x, y, f"screenshot_{x}_{y}.png"))

            # Create a blank image with the total width and height of the page
            stitched_image = Image.new('RGB', (total_width, total_height))

            # Paste all the screenshots together
            for x, y, path in screenshots:
                screenshot_image = Image.open(path)
                stitched_image.paste(screenshot_image, (x, y))

            # Save the final image
            stitched_image.save(screenshot_path)

            # Clean up temporary screenshots
            for _, _, path in screenshots:
                os.remove(path)

            # Close the browser


def scrape_akira(victim_name, short_location):
    short_location = "https://" + short_location
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    screenshot_filename = f'{victim_name}.png'
    screenshot_path = os.path.join(screenshot_directory, screenshot_filename)

    # Ensure the screenshots directory exists
    os.makedirs(screenshot_directory, exist_ok=True)

    # Take a screenshot and save it to the specified path
    screenshot_url = short_location + "/" + a_tag['href']
    time.sleep(2)
    # Get the full page height and width
    page_height = driver.execute_script("return document.body.scrollHeight")
    page_width = driver.execute_script("return document.body.scrollWidth")
    driver.set_window_size(page_width, page_height)

    # Set the window size to full page height
    driver.get(screenshot_url)
    driver.get_screenshot_as_file(screenshot_path)

    print(f"Screenshot saved to {screenshot_path}")

def scrape_ransomhub(victim_name, short_location):
    short_location = "http://" + short_location
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(short_location)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    # Find all divs with the class "card-title text-center"
    titles = soup.find_all("div", class_="card-title text-center")

    # Iterate through all titles to find the one that matches the desired text
    for title in titles:
        # print(a_tag['href'])
        if victim_name in title.get_text():
            # Find the parent 'a' tag to get the href attribute
            a_tag = title.find_parent("a")
            if a_tag and a_tag.has_attr('href'):
                print(a_tag['href'])

    screenshot_filename = f'{victim_name}.png'
    screenshot_path = os.path.join(screenshot_directory, screenshot_filename)

    # Ensure the screenshots directory exists
    os.makedirs(screenshot_directory, exist_ok=True)

    # Take a screenshot and save it to the specified path
    screenshot_url = short_location + "/" + a_tag['href']
    time.sleep(2)
    # Get the full page height and width
    page_height = driver.execute_script("return document.body.scrollHeight")
    page_width = driver.execute_script("return document.body.scrollWidth")
    driver.set_window_size(page_width, page_height)

    # Set the window size to full page height
    driver.get(screenshot_url)
    driver.get_screenshot_as_file(screenshot_path)

    print(f"Screenshot saved to {screenshot_path}")
