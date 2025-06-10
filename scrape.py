from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import numpy as np
import pandas as pd
import time
import datetime
import os
#Fixed constants
list_of_attributes_heating={"autonomous_heating":"autonomi_thermansi","central_heating":"kentriki_thermansi","individual_heating":"atomiki_thermansi","no_heating":"xwris_thermansi"}
list_of_attributes_kind_of_heating={
"petrol_heating":"thermansi_petrelaio","natural_gas_heating":"thermansi_fisiko_aerio","LPG_heating":"thermansi_igraerio","electrical_heating":"thermansi_revma",
"thermal_storage_heating":"thermansi_thermosisswreftis","wood_headting":"thermansi_sompa","pellet_heating":"thermansi_pellet","heat_pump_heating":"thermansi_antlia_thermansis"
}
list_of_attributes={"with_AC":"me_klimatismo","with_storage_room":"me_apothiki","with_elavator":"me_anelkistira","with_solar_heater":"me_iliako_thermosifona","with_fireplace":"me_tzaki",
"Furnished":"epiplwmeno","with_parking":"me_garage","with_garden":"me_kipo","with_pool":"me_pisina","with_balcony":"me_mpalkoni","last_floor":"retire"}
list_of_years={i:f"etos_kataskevis_apo-{i}/etos_kataskevis_eos-{i}" for i in range(1952,2025)}

filters=list_of_attributes_heating|list_of_attributes_kind_of_heating|list_of_attributes|list_of_years
#Creating a dictionary with the urls for each filter.
html_files_years_filters={}
for attribute in filters:
    
    url_solo=f"https://www.spitogatos.gr/pwliseis-katoikies/anazitisi-xarti/{filters[attribute]}?gad_source=1&gclid=Cj0KCQjw4MSzBhC8ARIsAPFOuyWdbWoq9MkzYB_9GZ1t8uEdSNmoSlUXErPyIku-g_dip54sBWRoNC0aArmUEALw_wcB&latitudeLow=40.535981&latitudeHigh=40.733210&longitudeLow=22.799034&longitudeHigh=23.120041&zoom=14" 
    
    
    html_files_years_filters[attribute]=url_solo


def single_page_scraper(sel_webdriver,df_base):
    """""
    Extracts house attributes from a webpage using a Selenium WebDriver and returns a list of attribute lists.
        Args:
        sel_webdriver (WebDriver): Selenium WebDriver instance.
        df_base (DataFrame): Base DataFrame to append data to.

    Returns:
        DataFrame: Updated DataFrame with extracted attributes.
    Notes:
        - If any attribute cannot be found for a house, its value is set to np.nan.
        - Prints the index of the last entry processed on the current page.
        - Relies on specific HTML structure and class names present in the target website.
    
    """
  
    # Define ignored exceptions globally to avoid redefining them in every function call
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException, TimeoutException)
    #this is a list of webdriver elements one  for each house. Note that we wait until all elements have been located.
    entries=WebDriverWait(sel_webdriver, 10,ignored_exceptions=ignored_exceptions)\
                        .until(expected_conditions.visibility_of_all_elements_located((By.XPATH, "//article[@class='ordered-element']")))
    # for each house now we want to find the floor, number of rooms etc. Again we wait until all elements have been located. 
    # The exact locations for each attribute can be found by inspecting the html code of the website.
    houses_attributes=[]
    i=1
    for house in entries:
        try:
            floor=house.find_element(By.XPATH, ".//ul[@class='tile__info']/li[1]/span/span").text
            rooms=house.find_element(By.XPATH, ".//ul[@class='tile__info']/li[2]/span/span").text
            bathrooms=house.find_element(By.XPATH, ".//ul[@class='tile__info']/li[3]/span/span").text
            
            price=house.find_element(By.XPATH, ".//div[@class='tile__price']/p").text
            
            description_and_area=house.find_element(By.XPATH, ".//div[@class='content__top']/h3[1]").text
            
            location=house.find_element(By.XPATH, ".//div[@class='content__top']/h3[2]").text
            submission_date=house.find_element(By.XPATH, ".//p[@class='tile__updated']/time").text
            description=description_and_area.split(",")[0]
            area=description_and_area.split(",")[1]
            
        #Each of these attributes is a WebDriver element from which we want to extract the html content.
        #Also if the scraper did not find any of these attributes we want their value as np.nan. 
    
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException): 
            description=np.nan
            area=np.nan
            floor=np.nan
            rooms=np.nan
            bathrooms=np.nan
            price=np.nan
            location=np.nan
            submission_date=np.nan
        #Finallly we append to our empty dataframe the extracted attributes.   
        attributes=[location,price,area,description,floor,rooms,bathrooms,submission_date]
        houses_attributes.append(attributes)
        if i==len(entries):
            print(f"Reached entry number: \033[91m{i}\033[0m on current page")
        i=i+1
        
    return(houses_attributes)


def get_driver(sel_webdriver,year=None,attribute=None):
    """
    Takes the driver instance to the correct website.

    Args:
        sel_webdriver (WebDriver): Selenium WebDriver instance.
        year: Year for which to fetch data.
    """
    if year !=None:
        sel_webdriver.get(html_files_years1952_2024[year])
    if attribute != None:
        sel_webdriver.get(html_files_years_filters[attribute])

def click(sel_webdriver):
    """
    Clicks the next page of the pagination to load the next batch of entries.
    Args:
        sel_webdriver (WebDriver): Selenium WebDriver instance.
    """
    page1=sel_webdriver.find_elements(By.XPATH,"//ul[@class='pagination b-pagination']/li[@class='page-item page-arrow']")
    while True:
        try:
            page1[-1].click()
            return
        except WebDriverException as e:
            input(f"Error clicking next page. Check if the page is loaded correctly and hit enter.")

def many_page_scrape(sel_webdriver,df,attribute=None,):
    """
        Scrapes house data across multiple pages and appends it to the provided DataFrame.
            sel_webdriver (WebDriver): Selenium WebDriver instance used for navigating and scraping web pages.
            df (pd.DataFrame): DataFrame to which the scraped data will be appended.
            attribute (str, optional): Attribute used for scraping all houses with that specific attribute. Defaults to None.
            pd.DataFrame: Updated DataFrame containing the accumulated scraped data.
        Notes:
            - The function determines the total number of pages to scrape and iterates through each page, scraping data and appending it to the DataFrame.
            - Every 50 pages (if `attribute` is provided), the function saves the current batch of data to a CSV file, resets the DataFrame, and continues scraping.
            - After the last page, any remaining data is saved to a separate CSV file if `attribute` is provided.
            - Duplicate entries are dropped before saving to CSV.
    """
    
    #1. We find the number of pages in the html file of the webpage
    page_num,current_page=find_pages(sel_webdriver)
    print(f"the number of total pages to scrape is:{page_num}")
    #2. We call the single_page_scraper function on the driver we loaded on the first step. We append the data (including the year) to our initial dataframe.
    df1=pd.DataFrame(single_page_scraper(sel_webdriver,df),columns=["Location", "Price","Total_area","House_type","Floor","Rooms","Bathrooms","submission_date"])

    df=pd.concat([df,df1],ignore_index=True)
    #3. If there is more than one page of houses built on that specific year we load the next page with the click function.
    if  page_num>1:
        
        
        
        for page in range(current_page,page_num):
            print(f"We scraped page {page} of {page_num}")
            click(sel_webdriver)
            current_url=sel_webdriver.current_url
            time.sleep(3)
        #4. We repeat step 3 until all pages for that year have been scraped.    
            df1=pd.DataFrame(single_page_scraper(sel_webdriver,df),columns=["Location", "Price","Total_area","House_type","Floor","Rooms","Bathrooms","submission_date"])

            
            df=pd.concat([df,df1],ignore_index=True)
            if page%50==0 and attribute!=None:
                path=f"/home/tsantaris/OneDrive/Data science and AI stuff/Project spitogatos/Houses_data_{datetime.date.today()}/Houses_data_{attribute}/Houses_data_page{page-50}_to{page}.csv"
                df.drop_duplicates(inplace=True)
                df.reset_index(drop=True, inplace=True)
                if attribute in list_of_years.keys():
                    df["Year"]=attribute
                df.to_csv(path)
                df=df.iloc[0:0]
                print(f"Saved data from page {page-50} to {page} to {path} for attribute {attribute}")


            if page==page_num-1 and attribute!=None:
                path=f"/home/tsantaris/OneDrive/Data science and AI stuff/Project spitogatos/Houses_data_{datetime.date.today()}/Houses_data_{attribute}/Houses_data_lastbatch.csv"
                df.drop_duplicates(inplace=True)
                df.reset_index(drop=True, inplace=True)
                df.to_csv(path)
                print(f"Saved data from page {page//50*50} to {page_num}")

    return(df)

def find_pages(sel_webdriver):
    """
    Finds the total number of pages in the current webpage and the current page.
    Args:
        sel_webdriver (WebDriver): Selenium WebDriver instance.
    """
    try:
        pages=sel_webdriver.find_elements(By.XPATH,"//a[@class='page-link']")
        current_page=sel_webdriver.find_element(By.XPATH,"//li[@class='page-item active']")
        if len(pages)>0:
            page_num=int(pages[-2].text)
            current_page=int(current_page.text)
        else:
            page_num=1
            current_page=1
    except:
        page_num=1
        current_page=1
    return page_num, current_page