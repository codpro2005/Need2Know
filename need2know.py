from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep

class RefVal():
    def __init__(self, id, result):
        self.id = id
        self.result = result
    
    def to_string(self):
        return 'ID: {}\nResult: {}'.format(self.id, self.result)

def reddit(driver):
    driver.get('https://www.reddit.com/hot')
    ref_vals = []
    for entry in driver.find_elements_by_xpath('//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[5]/div'):
        try:
            entry_container = entry.find_element_by_xpath('.//div/div')
            entry_content = entry_container.find_element_by_xpath('.//div[2]/div[2]/div/a/div/h3')
            print(entry_container.get_attribute('id'), entry_content.text)
            ref_vals.append(RefVal(entry_container.get_attribute('id'), entry_content.text))
        except:
            pass
    return ref_vals

index = 0
id = 0

def google(driver):
    global index
    global id
    driver.get('https://www.google.com')
    input_field = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    input_field.send_keys('lol')
    input_field.send_keys(Keys.RETURN)
    test_ref_vals = [RefVal(id, 'Haha')]
    index += 1
    if (index % 2 == 0):
        id += 1
    return test_ref_vals

def autoscout24(driver):
    driver.get('https://www.autoscout24.ch/de/?vehtyp=10')
    Select(driver.find_element_by_xpath('//*[@id="make"]')).select_by_visible_text('AUDI')
    select_on_load(driver, '//*[@id="model"]', 'Q2')
    select_on_load(driver, '//*[@id="yearfrom"]', 'Ab 2001')
    select_on_load(driver, '//*[@id="priceto"]', 'Bis CHF 200\'000')
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/main/section/div[2]/div/div/div/section[1]/div[3]/div/div[2]/span/a').click()
    ref_vals = []
    next_page_exits = True
    while next_page_exits:
        pageEntries = []
        while len(pageEntries) == 0:
            pageEntries = driver.find_elements_by_xpath('//*[@id="app"]/div[1]/main/section/div/div/div/div/div[2]/div[2]/div[1]/section/article')
        for pageEntry in pageEntries:
            try:
                info = pageEntry.find_element_by_xpath('.//div/a/div/div[2]')
                title_str = info.find_element_by_xpath('.//div/div/span').text
                content = info.find_element_by_xpath('.//div[2]')
                price_str = content.find_element_by_xpath('.//div/span').text
                driven_distance_str = content.find_element_by_xpath('.//div[2]').text
                gear_type_str = content.find_element_by_xpath('.//div[3]').text
                print('Gear type:' + gear_type_str)
                force_str = content.find_element_by_xpath('.//div[4]').text
                print('PS: ' + force_str)
                fuel_tank_type_str = content.find_element_by_xpath('.//div[5]').text
                print('Fuel tank: ' + fuel_tank_type_str)
                all_info_str = 'Title: {}, Price: {}, Distance driven: {}, Gear type: {}, Force: {}, Fuel tank: {}'.format(title_str, price_str, driven_distance_str, gear_type_str, force_str, fuel_tank_type_str)
                ref_vals.append(RefVal(all_info_str, title_str))
                print('success')
            except:
                pass
        pages = driver.find_elements_by_xpath('//*[@id="app"]/div[1]/main/section/div/div/div/div/div[2]/div[2]/nav/ul/li')
        activePage = {}
        for page in pages:
            if 'active' in page.get_attribute('class'):
                activePage = page
        nextPageIndex = pages.index(activePage) + 1
        if (nextPageIndex < len(pages)):
            pages[nextPageIndex].click()
        else:
            next_page_exits = False
    return ref_vals

def select_on_load(driver, search_select_by_xpath, visible_text):
    element_exists = False
    while not element_exists:
        try:
            Select(driver.find_element_by_xpath(search_select_by_xpath)).select_by_visible_text(visible_text)
            element_exists = True
        except:
            pass

class WebBot():
    driver = webdriver.Chrome()

    def __init__(self, name, action):
        self.name = name
        self.action = action
        self.ref_vals = []

    def get_new_unique_ref_vals(self):
        new_unique_ref_vals = []
        for new_ref_val in self.action(WebBot.driver):
            new_ref_val_exists = False
            for ref_val in self.ref_vals:
                if (new_ref_val.id == ref_val.id):
                    new_ref_val_exists = True
            if not new_ref_val_exists:
                self.ref_vals.append(new_ref_val)
                new_unique_ref_vals.append(new_ref_val)
        return new_unique_ref_vals


web_bots = [
    # WebBot('reddit', reddit),
    # WebBot('google', google),
    WebBot('autoscout24', autoscout24)
]

while True:
    for web_bot in web_bots:
        print(len(web_bot.ref_vals))
        new_unique_ref_vals = web_bot.get_new_unique_ref_vals()
        for new_unique_ref_val in new_unique_ref_vals:
            print(new_unique_ref_val.to_string())
    sleep(10)
