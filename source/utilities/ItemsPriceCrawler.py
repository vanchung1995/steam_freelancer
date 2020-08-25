import requests as rq
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import argparse


class CSGoEmpire:
    def __init__(self, username, password):
        self.url = 'https://csgoempire.com/withdraw#730'
        driver_path = '/home/nghiacv/code/python/steam_freelancer/libs/chromedriver'
        chrome_options = webdriver.ChromeOptions()
        cookie = [
            {
                "domain": ".csgoempire.com",
                "expirationDate": 1600828222.708344,
                "hostOnly": False,
                "httpOnly": True,
                "name": "__cfduid",
                "path": "/",
                "sameSite": "lax",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "d9e7a5203918b6804c21d811b9eddce131598236222",
                "id": 1
            },
            {
                "domain": ".csgoempire.com",
                "expirationDate": 1661424332,
                "hostOnly": False,
                "httpOnly": False,
                "name": "_ga",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "GA1.2.1782676415.1598236225",
                "id": 2
            },
            {
                "domain": ".csgoempire.com",
                "expirationDate": 1598352392,
                "hostOnly": False,
                "httpOnly": False,
                "name": "_gat",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "1",
                "id": 3
            },
            {
                "domain": ".csgoempire.com",
                "expirationDate": 1598438732,
                "hostOnly": False,
                "httpOnly": False,
                "name": "_gid",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "GA1.2.1898183453.1598236225",
                "id": 4
            },
            {
                "domain": ".csgoempire.com",
                "expirationDate": 1598354134,
                "hostOnly": False,
                "httpOnly": False,
                "name": "_hjAbsoluteSessionInProgress",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "0",
                "id": 5
            },
            {
                "domain": ".csgoempire.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "_hjid",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "25542009-5bdb-48cd-a68f-b7914b251629",
                "id": 6
            },
            {
                "domain": ".csgoempire.com",
                "expirationDate": 1598841279,
                "hostOnly": False,
                "httpOnly": False,
                "name": "intercom-session-okm1s2ii",
                "path": "/",
                "sameSite": "lax",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "UkhaNG92YWp1R3F1Nk5xbWhDSVpXYWZyUWF3NFlCMitydzcvdm5xZGY3UG1YS2NLWHpqMWhHUWZLSkpiaTQ1YS0tTzNNenVnZEJwRnRibXBtb3BHL0Evdz09--9a9870366ccd81e2150c13238c89ef53d65fb536",
                "id": 7
            },
            {
                "domain": "csgoempire.com",
                "hostOnly": True,
                "httpOnly": False,
                "name": "data",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "cc70b666773877443a8107e7500d0988",
                "id": 8
            },
            {
                "domain": "csgoempire.com",
                "expirationDate": 1629886194.925921,
                "hostOnly": True,
                "httpOnly": True,
                "name": "do_not_share_this_with_anyone_not_even_staff",
                "path": "/",
                "sameSite": "lax",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "6310085_qFhSfliDk9m9FACkSgSubQVCXeAEMOeZtt4GjCJMaoet4YMMvEsL4WiddUXW",
                "id": 9
            },
            {
                "domain": "csgoempire.com",
                "hostOnly": True,
                "httpOnly": True,
                "name": "PHPSESSID",
                "path": "/",
                "sameSite": "lax",
                "secure": True,
                "session": True,
                "storeId": "0",
                "value": "6egocdr4blg43rd4ogln13mqef",
                "id": 10
            }
        ]
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--profile-directory=Default')
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-plugins-discovery");
        chrome_options.add_argument("--start-maximized")
        self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
        self.username = username
        self.password = password

    def signin(self):
        signin_btn_xpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[3]/div[2]/div[3]/a'
        signin_btn = self.browser.find_element_by_xpath(signin_btn_xpath)
        signin_btn.click()
        # sleep(2)

        username_input_id = "steamAccountName"
        password_input_id = "steamPassword"
        login_btn_id = 'imageLogin'

        username_input = self.browser.find_element_by_id(username_input_id)
        password_input = self.browser.find_element_by_id(password_input_id)
        login_btn = self.browser.find_element_by_id(login_btn_id)

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_btn.send_keys(Keys.ENTER)
        # sleep(2)

    def get_all_data(self):
        show_custom_priced_btn_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]'
        self.browser.get(self.url)
        # self.browser.maximize_window()
        # self.browser.refresh()
        # sleep(10)
        self.signin()
        # sleep(10)
        show_custom_priced_btn = self.browser.find_element_by_xpath(show_custom_priced_btn_xpath)
        show_custom_priced_btn.click()
        sleep(10)
        self.browser.close()

    def search(self, keyword):
        pass


class VPGame:
    def __init__(self):
        self.base_url = 'https://www.vpgame.com/market/gift/api/mall/diamond/item'
        self.limit = '100'
        self.offset = '0'
        self.appid = '730'
        self.sortby = 'price'
        self.order = 'asc'

    def search(self, keyword):
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
        return response.json()


parser = argparse.ArgumentParser(description='Enter username and password')
parser.add_argument('--username', type=str, required=True, help='username CSGoEmpire')
parser.add_argument('--password', required=True, help='password CSGoEmpire')
args = parser.parse_args()

if __name__ == '__main__':
    # print(VPGame().search('AWP | Gungnir (Factory New)'))
    username = args.username
    password = args.password
    webdriver.remote
    CSGoEmpire(username, password).get_all_data()
