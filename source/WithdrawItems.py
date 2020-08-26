import requests as rq
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import argparse
from ItemsPriceCrawler import VPGamePrice

# item_withdraw_class = 'item--instant-withdraw'
item_withdraw_class = 'item__inner'
item_withdraw_name_class = 'item__name'
item_withdraw_price_class = 'item__price'
item_withdraw_brand_class = 'text-xxxs'
withdraw_button_text = 'Withdraw 1 Item'

username_input_id = "steamAccountName"
password_input_id = "steamPassword"
login_btn_id = 'imageLogin'
authencode_input_id = 'twofactorcode_entry'
famcode_input_id = 'steam_parental_password_box'

signin_btn_xpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[3]/div[2]/div[3]/a'
re_signin_btn_id = 'imageLogin'
show_custom_priced_btn_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]'
driver_path = '/home/nghiacv/code/python/steam_freelancer/libs/chromedriver'

def canby(buy,sell):
    buy_sell_ratio = 0.97
    return buy < sell * 0.97

class CSGoEmpire:
    def __init__(self, username, password, famcode, authcode):
        self.username = username
        self.password = password
        self.famcode = famcode
        self.authcode = authcode

        self.url = 'https://csgoempire.com/withdraw#730'
        self.vppricetool = VPGamePrice()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--user-data-dir=chrome-data")
        self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)

    def signin(self):
        signin_btn = self.browser.find_element_by_xpath(signin_btn_xpath)
        signin_btn.click()

        username_input = self.browser.find_element_by_id(username_input_id)
        password_input = self.browser.find_element_by_id(password_input_id)
        login_btn = self.browser.find_element_by_id(login_btn_id)
        sleep(1)

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_btn.send_keys(Keys.ENTER)
        sleep(2)

        authen_input = self.browser.find_element_by_id(authencode_input_id)
        authen_input.send_keys(self.authcode)
        authen_input.send_keys(Keys.ENTER)
        sleep(2)

        famcode_input = self.browser.find_element_by_id(famcode_input_id)
        famcode_input.send_keys(self.famcode)
        famcode_input.send_keys(Keys.ENTER)

    def resignin(self):
        self.browser.find_element_by_xpath(signin_btn_xpath).click()
        sleep(1)
        signin_btn = self.browser.find_element_by_id(re_signin_btn_id)
        signin_btn.click()

    def run(self):
        self.browser.get(self.url)
        self.browser.maximize_window()
        try:
            self.signin()
        except Exception as e:
            print('Error when trying to sign in, ',e)
        sleep(3)

        self.browser.refresh()
        self.browser.get(self.url)
        try:
            self.resignin()
        except Exception as e:
            print('Error when trying to sign in, ',e)
        sleep(1)
        # self.browser.refresh()
        self.browser.maximize_window()
        # self.browser.refresh()
        sleep(10)
        while True:
            try:
                toggle_div = self.browser.find_elements_by_class_name('toggle')
                toggle_div[0].click()
                break
            except Exception as e:
                print(e)
        sleep(10)

        while True:
            try:
                withdraw_items = self.browser.find_elements_by_class_name(item_withdraw_class)
                for withdraw_item in withdraw_items:
                    item_name = withdraw_item.find_element_by_class_name(item_withdraw_name_class)
                    item_price = withdraw_item.find_element_by_class_name(item_withdraw_price_class)
                    item_brands = withdraw_item.find_elements_by_class_name(item_withdraw_brand_class)

                    buy_price = float(item_price.text.strip().replace(',',''))

                    name = item_name.text.strip()
                    if len(item_brands) == 1:
                        name = item_brands[0].text.strip() + ' | ' + name
                    elif len(item_brands) == 2:
                        name = item_brands[1].text.strip() + ' | ' + name + ' (' + item_brands[0].text.split('|')[0].strip() + ')'
                    vp_prices = self.vppricetool.search(name)
                    if len(vp_prices) == 0:
                        print("Name: {},\t vpprice: {},\t\t csgo price: {}".format(name, None, buy_price))
                        continue

                    sell_price = float(vp_prices[0].strip().replace(',',''))
                    should_buy = canby(buy_price, sell_price)
                    print("Name: {},\t vpprice: {},\t csgo price: {},\t should buy: {} ".format(name, sell_price, buy_price, should_buy))
                    if should_buy:
                        withdraw_item.click()
                        btns = self.browser.find_elements_by_tag_name('button')
                        for btn in btns:
                            if btn.text.lower().strip() == withdraw_button_text.lower().strip():
                                btn.click()

                print('-----------------')
            except Exception as e:
                print('Error: ', e)
            sleep(1)

        self.browser.close()

parser = argparse.ArgumentParser(description='Enter username and password for trade account')
parser.add_argument('--username', type=str, required=True, help='username CSGoEmpire') #navi_tm
parser.add_argument('--password', type=str,required=True, help='password CSGoEmpire') #super_I250
parser.add_argument('--famcode', required=True, help='family code CSGoEmpire') # 7485
parser.add_argument('--authcode', type=str,action='store', required=True, help='authencode CSGoEmpire')
args = parser.parse_args()


if __name__ == '__main__':
    username = args.username
    password = args.password
    authcode = args.authcode
    famcode = args.famcode
    csgo = CSGoEmpire(username, password, famcode, authcode)
    csgo.run()
