import htmlparser
import tools
import config
import datetime
from atlassian import Confluence
import yaml
import os

confluence = Confluence(
    url=config.confluence_url,
    username=config.confluence_username,
    password=config.confluence_password)


def update_confluence_calender_page(confluence_id, unit):

    if unit == "w":
        unit = datetime.date.today().isocalendar()[1]
    else:
        unit = datetime.datetime.today().day

    confluence_content = confluence.get_page_by_id(confluence_id, expand="body.storage") 
 
    html = confluence_content["body"]["storage"]["value"]
    title = confluence_content["title"]

    column = htmlparser.find_column_number(html, str(unit))
    row = htmlparser.find_row_number(html, column, "B")
    teddy = htmlparser.get_cell_value(html, 0, row)

    print("Dagens bamse er den " + str(datetime.datetime.today()) + " er " + teddy)

    html = htmlparser.remove_highlightclass(html)
    html = htmlparser.add_highlightclass(html, column)

    confluence.update_page(confluence_id, title, html)

    return teddy


if __name__ == '__main__':
    
    dispatchers = []
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    with open(os.path.join(__location__, 'jobs.yaml'), 'r') as stream:
        jobs = yaml.safe_load(stream)

        for job in jobs['SearchDomain']:
            domain = jobs['SearchDomain'][job]['Domain']
            
            html = htmlparser.get_html_from_browser('https://www.webhuset.no/bestillingsskjema/domenesok?coupon-2=&fqdn='+ domain, 3)
            status = htmlparser.get_text_from_tagname(html, 'div', 'col-xs-12 result-text').strip()
            print(status)

            if status.find("ledig") != -1:
                email = jobs['SearchDomain'][job]['Email']
                tools.send_email(email, domain + " er ledig!", "")

                
        for job in jobs['UpdateConfluenceCalender']:
            confluence_id = jobs['UpdateConfluenceCalender'][job]['Confluence_id']
            unit = jobs['UpdateConfluenceCalender'][job]['Unit']

            name = update_confluence_calender_page(confluence_id, unit)

            #dispatchers.append(dispatcher.Dispatcher(job, name))
