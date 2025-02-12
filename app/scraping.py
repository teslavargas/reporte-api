# app/scraping.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def scrape_full(episode: int) -> dict:
    url = f"https://reporteminoritario.com/?episode={episode}"
    driver = init_driver()
    driver.get(url)
    driver.implicitly_wait(10)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    main_elem = soup.find("main") or soup
    sections = {}

    section_tags = main_elem.find_all("section")
    for sec in section_tags:
        heading_tag = sec.find(["h2", "h3", "h4"])
        if heading_tag:
            heading = heading_tag.get_text(strip=True)
            content = sec.get_text(separator="\n", strip=True)
            sections[heading] = content

    return sections
