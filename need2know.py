from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
import re

class Value():
    def __init__(self, id, output):
        self.id = id
        self.output = output
    
    def to_string(self):
        return 'ID: {}\nOutput: {}'.format(self.id, self.output)

def reddit(driver):
    driver.get('https://www.reddit.com/hot')
    values = []
    for entry in driver.find_elements_by_xpath('//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[5]/div'):
        try:
            entry_container = entry.find_element_by_xpath('.//div/div')
            entry_content = entry_container.find_element_by_xpath('.//div[2]/div[2]/div/a/div/h3')
            print(entry_container.get_attribute('id'), entry_content.text)
            values.append(Value(entry_container.get_attribute('id'), entry_content.text))
        except:
            pass
    return values

index = 0
id = 0

def google(driver):
    global index
    global id
    driver.get('https://www.google.com')
    input_field = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    input_field.send_keys('lol')
    input_field.send_keys(Keys.RETURN)
    values = [Value(id, 'Coole ID =>  {}'.format(id))]
    index += 1
    if (index % 2 == 0):
        id += 1
    return values

def autoscout24(driver):
    driver.get('https://www.autoscout24.ch/de/?vehtyp=10')
    Select(driver.find_element_by_xpath('//*[@id="make"]')).select_by_visible_text('AUDI')
    def select_on_load(driver, search_select_by_xpath, visible_text):
        element_exists = False
        while not element_exists:
            try:
                Select(driver.find_element_by_xpath(search_select_by_xpath)).select_by_visible_text(visible_text)
                element_exists = True
            except:
                pass
    select_on_load(driver, '//*[@id="model"]', 'Q2')
    select_on_load(driver, '//*[@id="yearfrom"]', 'Ab 2001')
    select_on_load(driver, '//*[@id="priceto"]', 'Bis CHF 200\'000')
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/main/section/div[2]/div/div/div/section[1]/div[3]/div/div[2]/span/a').click()
    values = []
    next_page_exists = True
    while next_page_exists:
        page_entries_loaded = False
        def get_page_entries():
            return driver.find_elements_by_xpath('//*[@id="app"]/div[1]/main/section/div/div/div/div/div[2]/div[2]/div[1]/section/article')
        while not page_entries_loaded:
            try:
                for page_entry in get_page_entries():
                    page_entry.find_element_by_xpath('./div/a/div')
                page_entries_loaded = True
            except:
                pass
        scroll_pos = 0
        for page_entry in get_page_entries():
            def get_full_info():
                return page_entry.find_element_by_xpath('./div/a/div')
            img_attribute_style_loaded = False
            img_attribute_style_had_failed = False
            def get_img_attribute_style():
                return page_entry.find_element_by_xpath('./div/a/div/div/div/div/div/div/div/div').get_attribute('style')
            while not img_attribute_style_loaded:
                try:
                    get_img_attribute_style()
                    img_attribute_style_loaded = True
                except:
                    if not img_attribute_style_had_failed:
                        img_attribute_style_had_failed = True
                        scroll_pos += 1080
                        driver.execute_script('window.scrollTo(0, {});'.format(scroll_pos))
            value_appended = False
            while not value_appended:
                try:
                    full_info = get_full_info()
                    image_src_str = re.search(r'^background: url\("(.*)"\) center center \/ contain no-repeat;$', get_img_attribute_style()).group(1)
                    info = full_info.find_element_by_xpath('./div[2]')
                    title_str = info.find_element_by_xpath('./div/div/span').text
                    content = info.find_element_by_xpath('./div[2]')
                    price_str = content.find_element_by_xpath('./div/span').text
                    distance_driven_str = content.find_element_by_xpath('./div[2]').text
                    gear_type_str = content.find_element_by_xpath('./div[3]').text
                    force_str = content.find_element_by_xpath('./div[4]').text
                    fuel_tank_str = content.find_element_by_xpath('./div[5]').text
                    id = image_src_str + title_str + price_str + distance_driven_str + gear_type_str + force_str + fuel_tank_str
                    value = 'Image src: {}, Title: {}, Price: {}, Distance driven: {}, Gear type: {}, Force: {}, Fuel tank: {}'.format(image_src_str, title_str, price_str, distance_driven_str, gear_type_str, force_str, fuel_tank_str)
                    values.append(Value(id, value))
                    # print(len(values))
                    value_appended = True
                except:
                    pass
        pages_loaded = False
        def get_pages():
            return driver.find_elements_by_xpath('//*[@id="app"]/div[1]/main/section/div/div/div/div/div[2]/div[2]/nav/ul/li')
        while not pages_loaded:
            try:
                get_pages()
                pages_loaded = True
            except:
                pass
        pages = get_pages()
        active_page = {}
        for page in pages:
            if 'active' in page.get_attribute('class'):
                active_page = page
        next_page_index = pages.index(active_page) + 1
        if (next_page_index < len(pages)):
            pages[next_page_index].click()
        else:
            next_page_exists = False
    return values

class WebBot():
    driver = webdriver.Chrome()
    driver.maximize_window()

    def __init__(self, name, get_new_values):
        self.name = name
        self.get_new_values = get_new_values
        self.unique_values = []

    def get_new_unique_values(self):
        new_unique_values = []
        for new_value in self.get_new_values(WebBot.driver):
            new_value_is_unique = True
            for unique_value in self.unique_values:
                if new_value.id == unique_value.id:
                    new_value_is_unique = False
            if new_value_is_unique:
                self.unique_values.append(new_value)
                new_unique_values.append(new_value)
        return new_unique_values


web_bots = [
    # WebBot('reddit', reddit),
    WebBot('google', google),
    WebBot('autoscout24', autoscout24)
]

while True:
    for web_bot in web_bots:
        print(len(web_bot.unique_values))
        new_unique_values = web_bot.get_new_unique_values()
        for new_unique_value in new_unique_values:
            print(new_unique_value.output)
    sleep(10)
