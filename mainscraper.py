from selenium import webdriver
import time

categorys = [
'https://planetadveri.kiev.ua/kvartirnye-dveri',
'https://planetadveri.kiev.ua/vnutrennie-dveri',
'https://planetadveri.kiev.ua/tehnicheskie-dveri',
'https://planetadveri.kiev.ua/polutornye-dveri'
]

category = -1

while category not in range(0, 4):
    choose = input("Какую категорию будем парсить?\n1 - Квартирные двери.\n2 - Внутренние двери.\n3 - Технические двери.\n4 - Полуторные двери.\nНапомню, что вводить нужно только цифру от 1 до 4:\n")
    if not (choose.isdigit()):
        print("Вводим только цифры\n")
    elif int(float(choose))-1 not in range(0, 4):
        choose = print("Так не пойдёт, нужно вводить число от 1 до 4, давай еще раз.\n")
    else:
        category = int(float(choose))-1
        break

# print("End.")s
# exit()




class scrapper():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # options.headless = True

        self.browser = webdriver.Chrome(
            'chromedriver',
            options=options
        )


    def scrapbycategory(self, category):
        self.browser.get(category)

        time.sleep(2)

        allhrefs = []

        pagecount = self.browser.find_elements_by_css_selector('div.pager:nth-of-type(2) span')
        if len(pagecount) > 0:
            numpages = int(pagecount[0].text[-2:])
            for page in range(numpages):
                j = page * 24
                self.browser.get(category+f'?filter=%7B%22n%22%3A%22{j}%22%7D')
                time.sleep(0.5)
                cartpages = self.browser.find_elements_by_css_selector('.itemsList .B > a')
                for page in cartpages:
                    href = page.get_attribute('href')
                    allhrefs.append(href)

        else:
            cartpages = self.browser.find_elements_by_css_selector('.itemsList .B > a')
            for page in cartpages:
                href = page.get_attribute('href')
                allhrefs.append(href)
        
        for href in allhrefs:
            self.browser.get(href)
            time.sleep(0.5)
            name = self.browser.find_element_by_css_selector('h1')
            price = self.browser.find_element_by_css_selector('.itemInfo big')
            params = self.browser.find_elements_by_css_selector('dt')

            print(name.text)
            print(price.text.replace(' ', ''))
            for param in params:
                print(param.text)
            print(href)
            print('')

        time.sleep(2)


    def finalize(self):
        self.browser.close()
        self.browser.quit()

my_scrapper = scrapper()
my_scrapper.scrapbycategory(categorys[category])
my_scrapper.finalize()