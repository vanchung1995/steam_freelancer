import requests as rq
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import argparse
import time
from datetime import datetime

def add_item(name, csgoprice, vpprice, items):
    max_delta_time = 3 * 60
    isexist = False
    for item in items:
        if time.time() - item['timestamp'] <= max_delta_time and item['name'] == name and item[
            'csgo_price'] == csgoprice and item['vp_price'] == vpprice:
            item['timestamp'] = int(time.time())
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


def print_all_items(items):
    for item in items:
        name = item['name']
        stp = item['timestamp']
        vp_price = item['vp_price']
        csgo_price = item['csgo_price']
        print('Time: {:.20}, Name: {:.40}, csgo price: {:.10}, vp price: {:10}'.format(str(datetime.fromtimestamp(stp)),
                                                                                       name, csgo_price, vp_price))
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
        items = []
        item_withdraw_class = 'item__inner'
        item_withdraw_name_class = 'item__name'
        item_withdraw_price_class = 'item__price'
        item_withdraw_brand_class = 'text-xxxs'
        # signed_in
        show_custom_priced_btn_xpath = '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]'
        self.browser.get(self.url)
        self.browser.maximize_window()

        self.signin()

        # show_custom_priced_btn = self.browser.find_element_by_xpath(show_custom_priced_btn_xpath)
        # show_custom_priced_btn.click()
        while True:
            try:
                toggle_div = self.browser.find_elements_by_class_name('toggle')
                toggle_div[0].click()
                break
            except Exception as e:
                print(e)

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
                        name = item_brands[1].text.strip() + ' | ' + name + ' (' + item_brands[0].text.split('|')[
                            0].strip() + ')'
                    vp_prices = self.vppricetool.search(name)
                    buy_price = float(item_price.text.strip().replace(',', ''))
                    sell_price = ''
                    if len(vp_prices) > 0:
                        sell_price = float(vp_prices[0].strip().replace(',', ''))
                    add_item(name, buy_price, sell_price, items)
                except:
                    pass
                print_all_items(items)

        self.browser.close()

    def search(self, keyword):
        pass


class VPGamePrice:
    def __init__(self, chanel):
        self.base_url = 'https://www.vpgame.com/market/gift/api/mall/diamond/item'
        self.limit = '100'
        self.offset = '0'
        if chanel == 'csgo':
            self.appid = '730'
        elif chanel == 'dota2':
            self.appid = '570'
        else:
            raise Exception('Chanel must be csgo or dota2')
        self.sortby = 'price'
        self.order = 'asc'

    def get_all_data(self):
        item_price = {}
        offset = 0
        while True:
            params = {
                'limit': self.limit,
                'offset': offset,
                'appid': self.appid,
                # 'sortby': self.sortby,
                # 'order': self.order,
            }
            response = rq.get(self.base_url, params=params)
            if response.status_code != 200:
                raise Exception('Status code of get request is {}'.format(response.status_code))
            data = response.json()['data']
            if len(data) == 0:
                break
            for item in data:
                name = item['name'].strip().lower()
                price = item['price']
                item_price[name] = price
            offset += int(response.json()['limit'])
        return item_price

    def search(self, keyword, data_dict=None):
        items = []
        keyword = keyword.strip().lower()
        if data_dict is not None and type(data_dict) == dict:
            if data_dict.get(keyword) is not None:
                items.append(data_dict[keyword])
            return items
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


class ItemCompare:
    def __init__(self, item_name, name1, price1, name2, price2):
        self.item_name = item_name
        self.tradeit_name = name1
        self.vpgame_name = name2
        self.tradeit_price = price1
        self.vpgame_price = price2

    def calculateRatio(self, price1, price2):
        if (type(price1) != float and type(price1) != int) or (
                type(price2) != float and type(price2) != int) or price2 == 0:
            return None
        return round(price1 / price2, 2)

    def printInfo(self):
        print('{:.90}, {:.10} price: {:.10}, {:.10} price: {}, ratio {}/{}: {}'.format(self.item_name,
                                                                                       self.tradeit_name,
                                                                                       self.tradeit_price,
                                                                                       self.vpgame_name,
                                                                                       self.vpgame_price,
                                                                                       self.tradeit_name,
                                                                                       self.vpgame_name,
                                                                                       self.calculateRatio(
                                                                                           self.tradeit_price,
                                                                                           self.vpgame_price)))


def write_data_2_csv(data_dict, mode='w+', file_path='./tradeit_csgo_vpgame', ext=None, sep='\t'):
    # data_dict = {
    #     'item_name' : itemcompare_obj
    # }

    if ext is None:
        ext = str(datetime.fromtimestamp(time.time())).replace(' ', '_')[:19]
    with open('{}_{}.csv'.format(file_path, ext), mode) as file:
        # header = 'Name\ttradeit_csgo_price\tvpgame_price\ttradeit/vpgame\tvpgame/tradeit\texist_vpgame_price\n'
        header = 'Name\ttradeit_price\tvpgame_price\ttradeit/vpgame\tvpgame/tradeit\texist_vpgame_price\n'
        file.write(header)
        for item_name in data_dict:
            itemcompare_obj = data_dict[item_name]
            exist_vpgame = (itemcompare_obj.vpgame_price is not None)
            file.write('{}{}{}{}{}{}{}{}{}{}{}'.format(itemcompare_obj.item_name.replace(sep, ' '), sep,
                                                       itemcompare_obj.tradeit_price, sep,
                                                       itemcompare_obj.vpgame_price, sep,
                                                       itemcompare_obj.calculateRatio(
                                                           itemcompare_obj.tradeit_price,
                                                           itemcompare_obj.vpgame_price), sep,
                                                       itemcompare_obj.calculateRatio(itemcompare_obj.vpgame_price,
                                                                                      itemcompare_obj.tradeit_price),
                                                       sep,
                                                       exist_vpgame))
            file.write('\n')


class Tradeitgg:
    def __init__(self, chanel):
        self.chanel = chanel
        if chanel == 'csgo':
            self.appid = '730'
            self.url = 'https://inventory.tradeit.gg/sinv/730'
        elif chanel == 'dota2':
            self.appid = '570'
            self.url = 'https://inventory.tradeit.gg/sinv/570'
        else:
            raise Exception('chanel must be csgo or dota2')
        self.tradeit_data_dict = {}
        self.vpgamecrawler = VPGamePrice(chanel)
        self.vpgamedata_dict = {}
        self.tradeit_without_vpgame_dict = {}

    def run(self):
        scriptlang = {
            "FN": "Factory New",
            "MW": "Minimal Wear",
            "FT": "Field-Tested",
            "WW": "Well-Worn",
            "BS": "Battle-Scarred",
        }

        try:
            starttime = time.time()
            self.vpgamedata_dict = self.vpgamecrawler.get_all_data()

            tradeit_raw_data = rq.get(self.url)
            if tradeit_raw_data.status_code != 200:
                print('Error: status code = {} get data from {}'.format(rq.status_codes, self.url_csgo_data))
            tradeit_raw_data = tradeit_raw_data.json()
            for item in tradeit_raw_data:
                user_data = item[self.appid]['items']
                for fullname in user_data:
                    item_name = fullname.split('_')[1].strip()
                    if 'e' in user_data[fullname]:
                        e = user_data[fullname]['e'].strip()
                        item_name += ' (' + scriptlang[e] + ')'
                    if item_name in self.tradeit_data_dict:
                        continue
                    price = float(user_data[fullname]['p']) / 100
                    vpgameprices = self.vpgamecrawler.search(item_name, self.vpgamedata_dict)
                    if len(vpgameprices) > 0:
                        vpprice = float(vpgameprices[0].strip().replace(',', ''))
                        self.tradeit_data_dict[item_name] = ItemCompare(item_name, 'tradeit', price, 'vpgame',
                                                                        vpprice)
                    else:
                        self.tradeit_without_vpgame_dict[item_name] = ItemCompare(item_name, 'tradeit', price,
                                                                                  'vpgame',
                                                                                  None)
            write_data_2_csv(data_dict=self.tradeit_data_dict, mode='w+',
                             file_path='./tradeit_{}_vpgame'.format(self.chanel))
            write_data_2_csv(data_dict=self.tradeit_without_vpgame_dict, mode='a+',
                             file_path='./tradeit_{}_vpgame'.format(self.chanel))
            print('Time consumption get data is {}'.format(round(time.time() - starttime, 2)))

            print(len(self.tradeit_data_dict))
            print(len(self.tradeit_without_vpgame_dict))
            for i in self.tradeit_data_dict:
                item = self.tradeit_data_dict[i]
                item.printInfo()

            for i in self.tradeit_without_vpgame_dict:
                item = self.tradeit_without_vpgame_dict[i]
                item.printInfo()
        except Exception as e:
            print('Error Tradeitgg run: ', e)
            raise


class LootFarm:
    def __init__(self, chanel):
        self.app_id = None
        if chanel == 'csgo':
            self.app_id = 730
        elif chanel == 'dota2':
            self.app_id = 570
        else:
            raise Exception('chanel must be csgo or dota2')
        self.withdraw_url = 'https://loot.farm/botsInventory_{}.json'.format(self.app_id)
        self.deposit_url = 'https://loot.farm/getInv_new.php?game={}'.format(self.app_id)
        self.deposit_cookies = {
            "PHPSESSID":"ec1a09c75541254300065055c089808a",
        }

    def get_withdraw_data(self):
        response = rq.get(self.withdraw_url)
        if response.status_code != 200:
            raise Exception('Status code of get request is {}'.format(response.status_code))
        try:
            data = response.json()['result']
            return data
        except Exception as e:
            print('Error: ',e)
            return []

    def get_deposit_data(self):
        response = rq.get(self.deposit_url, cookies = self.deposit_cookies)
        if response.status_code != 200:
            raise Exception('Status code of get request is {}'.format(response.status_code))

        try:
            data = response.json()['result']
            return data
        except Exception as e:
            print('Error: ', e)
            return []


class Fiveetop:
    def __init__(self, chanel):
        self.app_id = None
        if chanel == 'csgo':
            self.app_id = 730
        elif chanel == 'dota2':
            self.app_id = 570
        else:
            raise Exception('chanel must be csgo or dota2 in itit')
        self.withdraw_url = 'https://www.5etop.com/api/ingotitems/realitemback/list.do'
        self.deposit_url = 'https://www.5etop.com/api/user/inventory/{}/list.do'.format(self.app_id)
        
        self.withdraw_params = {
            'appid': self.app_id,
            'rows': 1000,
            'api': 'null',
            'rel': 'goldingot_2_realitemsback',
            'itemWidth': 160,
        }
        self.deposit_params = {
            'rel':'inventory_items',
            'itemWidth':99,
            'data':'loading',
            'page':1,
            'total':1000,
            'pages':1,
        }
        self.cookies = {
            'DJSP_USER': '5FKPbO9h3suO6zuCb2fTW0cZ1rBs6cvpsc3Y6R4NcqU%2FI%2FBv1rzYE54THC1VxWxijSyy%2BIPvuvy%2FjCTIP8pPlwJOXFXdQn3KzU14s356cEU%3D',
            # 'DJSP_UUID': '1746bde59393fed2b798f0df',
            # '__cfduid': 'dc2adaadcb0544fdb42312fd9e23096ba1599537568',
            # 'Hm_lvt_dota21cb9c842508c929123cd97ecd5278a28': '1599537570,1599538939',
            # 'JSESSIONID': 'B0B0B4BBB19E56033EAEC373322A2FB5',
            # 'Hm_lpvt_1cb9c842508c929123cd97ecd5278a28': '1599619455'
        }

    def get_withdraw_data(self):
        response = rq.get(self.withdraw_url, params=self.withdraw_params, cookies=self.cookies)
        if response.status_code != 200:
            raise Exception('Status code of get request is {}'.format(response.status_code))

        data = response.json()['datas']['list']
        return data

    def get_deposit_data(self):
        response = rq.get(self.deposit_url, params=self.deposit_params, cookies=self.cookies)
        if response.status_code != 200:
            raise Exception('Status code of get request is {}'.format(response.status_code))

        data = response.json()['datas']['list']
        return data


def parse_arg():
    parser = argparse.ArgumentParser(description='Enter username and password')
    parser.add_argument('--username', type=str, required=True, help='username CSGoEmpire')
    parser.add_argument('--password', required=True, help='password CSGoEmpire')
    args = parser.parse_args()
    username = args.username
    password = args.password
    return username, password


if __name__ == '__main__':
    # username, password = parse_arg()
    # CSGoEmpire(username, password ).get_all_data()

    # vp = VPGamePrice()
    # print(vp.search('AWP | Dragon Lore (FACTORY NEW)'))

    # Tradeitgg('csgo').run()

    data = LootFarm('dota2').get_deposit_data()
    print(len(data))
    # print(data)

    # data = Fiveetop('dota2').get_withdraw_data()
    # data = Fiveetop('csgo').get_deposit_data()
    # data = [(d['name'], d['value']) for d in data]
    # print(data)
