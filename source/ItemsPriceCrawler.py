import requests as rq
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import argparse

item_withdraw_class = 'item--instant-withdraw'
item_withdraw_class = 'item__inner'
item_withdraw_name_class = 'item__name'
item_withdraw_price_class = 'item__price'
item_withdraw_brand_class = 'text-xxxs'

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

        show_custom_priced_btn = self.browser.find_element_by_xpath(show_custom_priced_btn_xpath)
        show_custom_priced_btn.click()
        sleep(10)

        while True:
            withdraw_items = self.browser.find_elements_by_class_name(item_withdraw_class)
            for withdraw_item in withdraw_items:
                item_name = withdraw_item.find_element_by_class_name(item_withdraw_name_class)
                item_price = withdraw_item.find_element_by_class_name(item_withdraw_price_class)
                item_brands = withdraw_item.find_elements_by_class_name(item_withdraw_brand_class)
                print(item_name.text, item_price.text, [item_brand.text for item_brand in item_brands])
            print('-----------------')
            sleep(1)

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
            if item['name'] == keyword:
                items.append(item['price'])
        return items

# parser = argparse.ArgumentParser(description='Enter username and password')
# parser.add_argument('--username', type=str, required=True, help='username CSGoEmpire')
# parser.add_argument('--password', required=True, help='password CSGoEmpire')
# args = parser.parse_args()

if __name__ == '__main__':
    print(len(VPGamePrice().search('M4A4 | Hellfire (Field-Tested)')))
    print(VPGamePrice().search('M4A4 | Hellfire (Field-Tested)'))
    # username = args.username
    # password = args.password
    # webdriver.remote
    # CSGoEmpire(username, password).get_all_data()
