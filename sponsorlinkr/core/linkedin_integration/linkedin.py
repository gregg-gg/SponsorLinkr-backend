import os
import re

from django.conf import settings
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sponsorlinkr.core.models import POC, Company


def get_company_details(company_list, job_title="marketing"):
    # Replace with your LinkedIn credentials
    username = settings.SELENIUM_USERNAME
    password = settings.SELENIUM_PASSWORD

    # Set up the Chrome WebDriver (make sure chromedriver is installed and its location is in the system PATH)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()

    # Open LinkedIn login page
    driver.get("https://www.linkedin.com/login")

    # Wait for the login page to load
    # Add necessary waits or conditions here if needed

    # Enter username and password
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    # Wait for the home page to load
    # Add necessary waits or conditions here if needed
    for company_name in company_list:
        print(company_name)
        # Replace with the name of the company you want to search
        driver.get(
            f"https://www.linkedin.com/search/results/companies/?keywords={company_name}&origin=SWITCH_SEARCH_VERTICAL"
        )

        try:
            # # Find the search box by XPath
            # search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search' and @role='combobox' and @class='search-global-typeahead__input']")

            # wait = WebDriverWait(driver, 10)
            # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search' and @role='combobox' and @class='search-global-typeahead__input']")))
            # search_box.click()

            # # Clear any existing text in the search box
            # search_box.clear()

            # # Enter the company name in the search box
            # search_box.send_keys(company_name)

            # # Press Enter to perform the search
            # search_box.send_keys(Keys.RETURN)
            # Wait for the search results page to load
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.reusable-search__result-container")))

            try:
                # # Find the first search result
                first_result = driver.find_element(By.CSS_SELECTOR, "span.entity-result__title-text")

                # # Click on the first search result
                # first_result.click()
                first_link = first_result.find_element(By.CSS_SELECTOR, "a.app-aware-link").get_attribute("href")

                driver.get(first_link)

                # Wait for the company page to load
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.org-top-card")))

                # Get the LinkedIn link of the company
                company_linkedin_url = first_link
                print(company_linkedin_url)

                # Get the LinkedIn ID of the company
                company_id = driver.find_element(
                    By.CSS_SELECTOR, "a.ember-view.org-top-card-summary-info-list__info-item"
                ).get_attribute("href")
                print(company_id)
                try:
                    len(re.findall(r"%5B%22[1-9]+%22%5D", company_id))
                    company_param = re.findall(r"%5B%22(\d+)%22%5D", company_id)[0]
                    company_id = company_param
                    company_id.lstrip("%5B%22").rstrip("%22%5D")
                except IndexError:
                    continue

                # Print the company LinkedIn URL

                # Getting org logo
                org_logo = driver.find_element(
                    By.CSS_SELECTOR, "img.org-top-card-primary-content__logo"
                ).get_attribute("src")

                # Getting org name
                org_name = driver.find_element(By.CSS_SELECTOR, "h1.org-top-card-summary__title").text

                company = Company.objects.create(
                    name=company_name,
                    linkedin_url=company_linkedin_url,
                    linkedin_id=company_id,
                    linkedin_logo_url=org_logo,
                )

                position = "marketing"
                people_search_url = f"https://www.linkedin.com/search/results/people/?currentCompany={company_param}&keywords={position}&origin=FACETED_SEARCH"

                driver.get(people_search_url)
                wait = WebDriverWait(driver, 20)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.reusable-search__result-container")))

                profile_parents = driver.find_elements(By.CSS_SELECTOR, "span.entity-result__title-text")
                image_parents = driver.find_elements(By.CSS_SELECTOR, "div.entity-result__universal-image")
                print(len(profile_parents))
                print(len(image_parents))

                for profile_parent, image_parent in zip(profile_parents, image_parents):
                    profile_link = profile_parent.find_element(By.CSS_SELECTOR, "a.app-aware-link")
                    image_tag = image_parent.find_element(By.CSS_SELECTOR, "img.presence-entity__image")
                    # Extract the src attribute
                    pic_url = image_tag.get_attribute("src")
                    print(profile_link.text)
                    print(profile_link.get_attribute("href"))
                    print()
                    POC.objects.create(
                        company=company,
                        name=profile_link.text,
                        linkedin_profile_url=profile_link.get_attribute("href"),
                        job_title=position,
                        linkedin_profile_pic_url=pic_url,
                    )

            except NoSuchElementException:
                print("No search results found for the company.")

        except NoSuchElementException:
            print("Search box not found.")

        except TimeoutException:
            print("Timeout occurred while waiting for search results.")

    # Close the browser
    driver.quit()
