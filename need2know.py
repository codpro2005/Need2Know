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

class Reference():
    def __init__(self, value):
        self.value = value

class ScraperHelper():
    @staticmethod
    def select_on_no_exception(driver, search_select_by_xpath, select_visible_text):
        element_exists = False
        while not element_exists:
            try:
                Select(driver.find_element_by_xpath(search_select_by_xpath)).select_by_visible_text(select_visible_text)
                element_exists = True
            except:
                pass

    @staticmethod
    def wait_on_action(do_while_not_valid_action, *args):
        on_invalid_action = None
        on_invalid_action_arguments = []
        if len(args) > 0:
            for index, arg in enumerate(args):
                if index == 0:
                    on_invalid_action = arg
                else:
                    on_invalid_action_arguments.append(arg)
        is_valid = False
        has_been_invalid = False
        while not is_valid:
            is_valid, has_been_invalid = do_while_not_valid_action(has_been_invalid, on_invalid_action, *on_invalid_action_arguments)

    @staticmethod
    def wait_on_no_exception(check_no_exception_action, *args):
        def do_while_exception_action(had_failed, on_exception_action, *on_fail_action_arguments):
            has_loaded = False
            try:
                check_no_exception_action()
                has_loaded = True
            except:
                if not had_failed:
                    had_failed = True
                    if not on_exception_action is None:
                        on_exception_action(*on_fail_action_arguments)
            return has_loaded, had_failed
        ScraperHelper.wait_on_action(do_while_exception_action, *args)

    @staticmethod
    def wait_on_valid(check_if_valid_action, *args):
        def do_while_not_valid_action(has_been_invalid, on_invalid_action, *on_invalid_action_arguments):
            is_valid = False
            if check_if_valid_action():
                is_valid = True
            elif not has_been_invalid:
                has_been_invalid = True
                if not on_invalid_action is None:
                    on_invalid_action(*on_invalid_action_arguments)
            return is_valid, has_been_invalid
        ScraperHelper.wait_on_action(do_while_not_valid_action, *args)


def autoscout24(driver):
    driver.get('https://www.autoscout24.ch/')
    Select(driver.find_element_by_xpath('//*[@id="make"]')).select_by_visible_text('AUDI')
    ScraperHelper.select_on_no_exception(driver, '//*[@id="model"]', 'Q2')
    ScraperHelper.select_on_no_exception(driver, '//*[@id="yearfrom"]', 'Ab 2001')
    ScraperHelper.select_on_no_exception(driver, '//*[@id="priceto"]', 'Bis CHF 200\'000')
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/main/section/div[2]/div/div/div/section[1]/div[3]/div/div[2]/span/a').click()
    values = []
    next_page_exists = True
    while next_page_exists:
        def get_page_entries():
            return driver.find_elements_by_xpath('//*[@id="app"]/div[1]/main/section/div/div/div/div/div[2]/div[2]/div[1]/section/article')
        def check_no_exception_page_entries():
            for page_entry in get_page_entries():
                page_entry.find_element_by_xpath('./div/a/div')
        ScraperHelper.wait_on_no_exception(check_no_exception_page_entries)
        scroll_pos_ref = Reference(0)
        for page_entry in get_page_entries():
            def get_img_attribute_style():
                return page_entry.find_element_by_xpath('./div/a/div/div/div/div/div/div/div/div').get_attribute('style')
            def on_img_attribute_load_fail(scroll_pos_ref):
                scroll_pos_ref.value += 1080
                driver.execute_script('window.scrollTo(0, {});'.format(scroll_pos_ref.value))
            ScraperHelper.wait_on_no_exception(get_img_attribute_style, on_img_attribute_load_fail, scroll_pos_ref)
            def get_img_attribute_style_is_not_empty():
                return len(get_img_attribute_style()) > 0
            ScraperHelper.wait_on_valid(get_img_attribute_style_is_not_empty)
            full_info = page_entry.find_element_by_xpath('./div/a/div')
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
        def get_pages():
            return driver.find_elements_by_xpath('//*[@id="app"]/div[1]/main/section/div/div/div/div/div[2]/div[2]/nav/ul/li')
        def check_no_exception_page_attribute_class():
            for page in get_pages():
                page.get_attribute('class')
        ScraperHelper.wait_on_no_exception(check_no_exception_page_attribute_class)
        pages = get_pages()
        active_page = None
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
    # WebBot('google', google),
    WebBot('autoscout24', autoscout24)
]

iterations = 0
first_iteration = True
while True:
    for web_bot in web_bots:
        iterations += 1
        print('Iteration: ', iterations)
        new_unique_values = web_bot.get_new_unique_values()
        if not first_iteration:
            for new_unique_value in new_unique_values:
                print(new_unique_value.output)
        else:
            first_iteration = False
        print('Length: ', len(web_bot.unique_values))
    sleep(900)
