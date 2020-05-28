import io

class MarkdownGenerator:
    def __init__(self):
        self.markdown_file = io.StringIO()

    def return_value(self):
        return self.markdown_file.getvalue()

    def merge_templates(self, filename):
        with open('header.md', 'r') as header_file:
            header_text = ''.join(header_file.readlines()[2:]) # Get rid of the header warning.
        with open(filename, 'w') as readme_file:
            readme_file.write(header_text + self.return_value())

    def insert_line_link(self, text, link):
        self.insert_line(f"**[{text}]({link})**")

    def insert_line(self, text):
        self.markdown_file.write(text + "\n")

    def insert_newline(self):
        self.markdown_file.write("\n")

    def insert_state_header(self, state_name):
        self.insert_line("#### " + state_name)

    def capitalize_state(self, state):
        lower_state = state.lower()
        state_split = lower_state.split(' ')
        state_cap = [name.capitalize() for name in state_split]
        return ' '.join(state_cap)

    def insert_season_pass_table(self, season_pass_list):
        self.insert_line("| Season Pass | Price |")
        self.insert_line("| ------------| ----- |")
        for season_pass in season_pass_list:
            if season_pass != "website": # Ignore website dicts.
                season_pass_price = []
                for price in season_pass_list[season_pass]:
                    season_pass_price.append(f"{price} {season_pass_list[season_pass][price]}")
                season_pass_price = ' \| '.join(season_pass_price)
                self.insert_line(f"| {season_pass} | {season_pass_price} |")
        self.insert_newline()


    def handle_list(self, park_list):
        self.insert_line("# Full Table") # Add header.
        for state in park_list:
            if 'SAUDI ARABIA' in state:  # Saudi Arabia is not open, and we do not really care about it that much, just ignore it,
                continue
            self.insert_state_header(self.capitalize_state(state))
            for park in park_list[state]:
                self.insert_line_link(park, park_list[state][park]['website'])
                if 'Mexico' in park: # Add translation disclaimer for Mexico.
                    self.insert_newline()
                    self.insert_line("Please note that the bottom table was pulled directly from the above website untranslated.")
                self.insert_season_pass_table(park_list[state][park])