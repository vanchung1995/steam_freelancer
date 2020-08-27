import requests as rq
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import argparse
import time
from datetime import datetime

item_withdraw_class = 'item--instant-withdraw'
item_withdraw_class = 'item__inner'
item_withdraw_name_class = 'item__name'
item_withdraw_price_class = 'item__price'
item_withdraw_brand_class = 'text-xxxs'

items = []
max_delta_time = 3 * 60

def add_item(name, csgoprice, vpprice):
    isexist = False
    for item in items:
        if time.time() - item['timestamp'] <= max_delta_time and item['name'] == name and item['csgo_price'] == csgoprice and item['vp_price'] == vpprice:
            isexist = True
        if time.time() - item['timestamp'] > max_delta_time:
            items.remove(item)
    if not isexist:
        item = {}
        item['name'] = name
        item['csgo_price'] = csgoprice
        item['vp_price'] = vpprice
        item['timestamp'] = int(time.time())
        items.append(item)

def print_all_items(items = items):
    for item in items:
        name = item['name']
        stp = item['timestamp']
        vp_price = item['vp_price']
        csgo_price = item['csgo_price']
        print('Time: {:.20}, Name: {:.20}, csgo price: {:.10}, vp price: {:10}'.format(str(datetime.fromtimestamp(stp)),name,csgo_price, vp_price))
    print('--------------------')

class CSGoEmpire:
    def __init__(self, username, password):
        self.url = 'https://csgoempire.com/withdraw#730'
        driver_path = '/home/nghiacv/code/python/steam_freelancer/libs/chromedriver'
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--user-data-dir=chrome-data")
        # chrome_options.add_argument("user-data-dir=chrome-data")
        self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
        self.username = username
        self.password = password
        self.vppricetool = VPGamePrice()

    def signin(self):
        signin_btn_xpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[3]/div[2]/div[3]/a'
        signin_btn = self.browser.find_element_by_xpath(signin_btn_xpath)
        signin_btn.click()

        username_input_id = "steamAccountName"
        password_input_id = "steamPassword"
        login_btn_id = 'imageLogin'

        username_input = self.browser.find_element_by_id(username_input_id)
        password_input = self.browser.find_element_by_id(password_input_id)
        login_btn = self.browser.find_element_by_id(login_btn_id)

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_btn.send_keys(Keys.ENTER)

    def get_all_data(self):
        # signed_in
        show_custom_priced_btn_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]'
        self.browser.get(self.url)
        self.browser.maximize_window()

        self.signin()
        sleep(10)

        # show_custom_priced_btn = self.browser.find_element_by_xpath(show_custom_priced_btn_xpath)
        # show_custom_priced_btn.click()
        try:
            toggle_div = self.browser.find_elements_by_class_name('toggle')
            toggle_div[0].click()
        except Exception as e:
            print(e)
        sleep(10)

        while True:
            withdraw_items = self.browser.find_elements_by_class_name(item_withdraw_class)
            for withdraw_item in withdraw_items:
                try:
                    item_name = withdraw_item.find_element_by_class_name(item_withdraw_name_class)
                    item_price = withdraw_item.find_element_by_class_name(item_withdraw_price_class)
                    item_brands = withdraw_item.find_elements_by_class_name(item_withdraw_brand_class)

                    name = item_name.text.strip()
                    if len(item_brands) == 1:
                        name = item_brands[0].text.strip() + ' | ' + name
                    elif len(item_brands) >= 2:
                        name = item_brands[1].text.strip() + ' | ' + name + ' (' + item_brands[0].text.split('|')[0].strip() + ')'
                    vp_prices = self.vppricetool.search(name)
                    buy_price = float(item_price.text.strip().replace(',',''))
                    sell_price = ''
                    if len(vp_prices) > 0:
                        sell_price = float(vp_prices[0].strip().replace(',',''))
                    add_item(name,buy_price,sell_price)
                except:
                    pass
                print_all_items()

        self.browser.close()

    def search(self, keyword):
        pass


class VPGamePrice:
    def __init__(self):
        self.base_url = 'https://www.vpgame.com/market/gift/api/mall/diamond/item'
        self.limit = '100'
        self.offset = '0'
        self.appid = '730'
        self.sortby = 'price'
        self.order = 'asc'

    def search(self, keyword):
        items = []
        params = {
            'limit': self.limit,
            'offset': self.offset,
            'appid': self.appid,
            'sortby': self.sortby,
            'order': self.order,
            'keyword': keyword
        }
        response = rq.get(self.base_url, params=params)
        if response.status_code != 200:
            raise Exception('Status code of get request is {}'.format(response.status_code))
        data = response.json()['data']
        for item in data:
            if item['name'].lower().strip() == keyword.lower().strip():
                items.append(item['price'])
        return items

parser = argparse.ArgumentParser(description='Enter username and password')
parser.add_argument('--username', type=str, required=True, help='username CSGoEmpire')
parser.add_argument('--password', required=True, help='password CSGoEmpire')
args = parser.parse_args()

if __name__ == '__main__':
    vp = VPGamePrice()
    # print(VPGamePrice().search('M4A4 | Hellfire (Field-Tested)'))
    # print(VPGamePrice().search('StatTrak™ AK-47 | Asiimov (BATTLE-SCARRED)'))
    # print(vp.search('AWP | Dragon Lore (FACTORY NEW)'))
    username = args.username
    password = args.password
    CSGoEmpire(username, password).get_all_data()
