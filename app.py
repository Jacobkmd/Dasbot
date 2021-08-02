import htmlparser
import config
import datetime
from atlassian import Confluence
import yaml


confluence = Confluence(
    url=config.confluence_url,
    username=config.confluence_username,
    password=config.confluence_password)


def update_confluence_calender_page(confluence_id):

    week_number = datetime.date.today().isocalendar()[1]

    confluence_content = confluence.get_page_by_id(confluence_id, expand="body.storage") 
 
    html = confluence_content["body"]["storage"]["value"]
    title = confluence_content["title"]

    column = htmlparser.find_column_number(html, str(week_number))
    row = htmlparser.find_row_number(html, column, "B")
    teddy = htmlparser.get_cell_value(html, 0, row)

    print("Dagens bamse er: " + teddy)

    html = htmlparser.remove_highlightclass(html)
    html = htmlparser.add_highlightclass(html, column)

    confluence.update_page(confluence_id, title, html)


if __name__ == '__main__':
   
       with open("jobs.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
   
        for item in data_loaded['UpdateConfluenceCalender']:
            confluence_id = data_loaded['UpdateConfluenceCalender'][item]['Confluence_id']
            update_confluence_calender_page(confluence_id)
