import requests_html
import bs4
from markdown_generator import MarkdownGenerator

HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

SIX_FLAGS_PARKS = {}

SIX_FLAGS_WEBSITE = "https://www.sixflags.com"
SIX_FLAGS_SEASON_PASS_PAGE = "/store/season-passes"

requests = requests_html.HTMLSession()
six_flags_code = requests.get(SIX_FLAGS_WEBSITE, headers=HEADERS).content
six_flags_parser = bs4.BeautifulSoup(six_flags_code, 'html.parser')
parks = six_flags_parser.find_all(class_='choose-your-park')[0]
park_list = parks.find_all('li')

for park in park_list:
    state = park.get('title') # Get the name of the state
    if state:
        STATE_PARKS_DICT = {}
        state_parks = park.find_all('a')
        for state_park in state_parks:
            state_park_name = state_park['title']
            if not 'Hurricane' in state_park_name and not 'Water' in state_park_name: # Tell all the water parks to go drown themselves.
                state_park_href = state_park['href']
                if not 'http' in state_park_href:
                    state_park_website = SIX_FLAGS_WEBSITE + state_park['href']
                elif "La Ronde" in state_park_name: # The href we get is for a French version, however, there is a English version, so we use that.
                    state_park_website = SIX_FLAGS_WEBSITE + '/larondeen'
                else:
                    state_park_website = state_park_href
                STATE_PARKS_DICT[state_park_name] = {}
                STATE_PARKS_DICT[state_park_name]['website'] = state_park_website
        if STATE_PARKS_DICT.keys(): # Get rid of states that do not have non-water parks.
            SIX_FLAGS_PARKS[state] = STATE_PARKS_DICT

for state in SIX_FLAGS_PARKS:
    state_parks = SIX_FLAGS_PARKS[state]
    for park in state_parks:
        website = state_parks[park]['website']
        season_pass_page = website + SIX_FLAGS_SEASON_PASS_PAGE
        requests = requests_html.HTMLSession()
        season_pass_code = requests.get(season_pass_page, headers=HEADERS)
        season_pass_code.html.render() # The prices are changed by JavaScript on the website, so we need to use this function.
        season_pass_code = season_pass_code.html.html
        season_pass_parser = bs4.BeautifulSoup(season_pass_code, 'html.parser')
        season_pass_blocks = season_pass_parser.find_all(class_='view-content')
        for season_pass_block in season_pass_blocks:
            season_pass_content = season_pass_block.find_all('div', class_='product')
            for season_pass_section in season_pass_content:
                season_pass_left = season_pass_section.find('div', class_='productLeftSide')
                season_pass_right = season_pass_section.find('div', class_='productRightSide')
                season_pass_name = season_pass_left.find('h3').string
                if season_pass_name == None:
                    season_pass_name = 'Unknown'
                state_parks[park][season_pass_name] = {}
                season_pass_buttons = season_pass_right.find_all('div', class_='buyButtonWrapper')

                for season_pass_button in season_pass_buttons:
                    season_pass_price_desc = season_pass_button.find('div', class_='buyButtonPriceDesc').string
                    if season_pass_price_desc == None:
                        season_pass_price_desc = ''
                    season_pass_dollars = season_pass_button.find('span', class_='buyButtonPrice').string
                    season_pass_unit = season_pass_button.find('span', class_='buyButtonPriceUnit').string
                    season_pass_price = season_pass_dollars + season_pass_unit
                    state_parks[park][season_pass_name][season_pass_price_desc] = season_pass_price

generator = MarkdownGenerator()
generator.handle_list(SIX_FLAGS_PARKS)
generator.merge_templates('README.md')