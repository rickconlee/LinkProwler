import unittest
import scrape

###################
# TEST CASE VARS
###################

# We need a site to target so we can properly test the selenium function. 
target_site = 'https://www.goombaas.com/'


###################
# TEST CASES
###################

# Check and make sure selenium is working correctly. 

class TestSelenium(unittest.TestCase):

    def test_selenium_function(self):
        key = 'html'
        container = scrape.grab_page_selenium(target=target_site)
        message = 'didnt get shit.'
        self.assertIn(key, container, message)


class TestTypes(unittest.TestCase):

    def test_selenium_return_type(self):
        result = scrape.grab_page_selenium(target=target_site)
        self.assertIsInstance(result, str)

    def test_website_links_type(self):
        result = scrape.get_all_website_links(url=target_site)
        self.assertIsInstance(result, set)