import time
from selenium import webdriver
import scraper.constants as const
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup


class PropertyCrawler(webdriver.Chrome):
    def __init__(self):
        super(PropertyCrawler, self).__init__()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        time.sleep(5)
        self.quit()

    def page(self):
        time.sleep(3)
        self.get(const.BASE_URI)

    def changeLocation(self, state=None):
        input_ = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[4]/form/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div/div/input'))
        )
        input_.click()
        input_.send_keys(state)
        button_ = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[4]/form/div[1]/div[1]/div[2]/div/div/div[1]/div[3]/button/span'))
        )
        button_.click()

    def getData(self, city_):

        data_ = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[5]/div[3]/div[2]'))
        )
        data_ = self.find_element(By.XPATH, '/html/body/div[1]/div/div/div[5]/div[3]/div[2]')
        sections = data_.find_elements(By.CLASS_NAME, 'projectTuple__descCont ')

        property_info = []

        for section in sections:
            outer_html = section.get_attribute('outerHTML')
            data = BeautifulSoup(outer_html, 'lxml')

            name_tag = data.find('a', class_=['projectTuple__projectName',  'projectTuple__pdWrap20', 'ellipsis'])

            name = name_tag.text
            locality = data.find('h2', class_=['projectTuple__subHeadingWrap', 'body_med', 'ellipsis']).text
            city = city_
            link = name_tag['href']
            cost = []
            type_ = []
            area = []

            for d in (data.find('div', class_='carousel__slidingBox').find_all_next('div', class_=['configurationCards__cardContainer', 'configurationCards__srpCardStyle'])):
                cost_ = d.find_next('div', class_='configurationCards__cardPriceHeadingWrapper').find_next('span', class_=['list_header_semiBold', 'configurationCards__cardPriceHeading']).text
                typ = d.find_next('span', class_=['list_header_semiBold', 'configurationCards__configBandLabel']).text
                area_ = d.find_next('span', class_=['caption_subdued_medium', 'configurationCards__cardAreaSubHeadingOne']).text
                cost.append(cost_)
                type_.append(typ)
                area.append(area_)

            property_info.append({
                'Property name': name,
                'City': city,
                'Locality': locality,
                'Cost': cost,
                'Type': type_,
                'Area': area,
                'Link': link
            })
        return property_info

    def checkData(self, city_):
        cond = True
        z=0

        data = []

        while cond == True:
            time.sleep(4)
            action = ActionChains(self)
            if z == 0:
                for i in range(120):
                    time.sleep(0.2)
                    action.scroll_by_amount(0, 500).perform()
            else:
                for i in range(30):
                    time.sleep(0.2)
                    action.scroll_by_amount(0, 500).perform()

            data_ = self.getData(city_=city_)
            print(data_)
            data.extend(data_)

            page_div = self.find_element(By.CLASS_NAME, 'Pagination__srpPagination')
            page = page_div.find_element(By.CLASS_NAME, 'caption_strong_large')
            page = page.text
            at_page = page.split(' ')[1]
            total_page = page.split(' ')[3]

            if at_page == total_page:
                cond = False

            a_tag = self.find_element(By.XPATH, '/html/body/div[1]/div/div/div[5]/div[3]/div[3]/div[4]/a')
            a_tag_text = a_tag.text.strip()
            if a_tag_text == 'Next Page >':
                a_tag.click()

            z+=1

        return data



