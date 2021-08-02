from bs4 import BeautifulSoup

def remove_highlightclass(html):
    return html.replace(' data-highlight-colour="#e3fcef"', '').strip()


def add_highlightclass(html, column):
    find_string = "<th"
    last_position = 0
    position = 0
    new_html = ''
    
    while True:
        for x in range(column + 1):
            position = html.find(find_string, position) + len(find_string)
        
        new_html = new_html + html[last_position:position] + ' data-highlight-colour="#e3fcef"'

        last_position = position 
        position = html.find("<tr>", position)
        find_string = "<td"
            
        if position == -1:
            break

    return new_html + html[last_position:]


def find_column_number(html, value):
    soup = BeautifulSoup(html, "html.parser")
    column_counter = 0
    
    columns = soup.find_all("th")

    for column in columns:
        if column.text == value:
            return column_counter
        else:
            column_counter += 1


def find_row_number(html, column, value):
    soup = BeautifulSoup(html, "html.parser")
    row_counter = 0
    
    rows = soup.find_all("tr")[1:]

    for row in rows:     
        if row.find_all('td')[column].text == value:
            return row_counter
        else:
            row_counter += 1


def get_cell_value(html, column, row):
    soup = BeautifulSoup(html, "html.parser")

    return soup.find_all("tr")[1:][row].find_all("td")[column].text