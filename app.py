import requests
from bs4 import BeautifulSoup
import json

def retrieve_and_print_secret_message(url):
    # Retrieve the HTML content of the Google Doc
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the div element containing the secret message
    secret_message_div = soup.find('div', class_='doc-content')

    table = secret_message_div.find('table')

    if table:
        print(table.prettify())
    else:
        print("Table not found.")

    data_list = []

    # Extract rows
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) == 3:
            x_coord = cols[0].get_text(strip=True)
            character = cols[1].get_text(strip=True)
            y_coord = cols[2].get_text(strip=True)
            # Append extracted data to the list as a dictionary
            data_list.append({
                'x_coordinate': x_coord,
                'character': character,
                'y_coordinate': y_coord
            })

    json_output = json.dumps(data_list, indent=4)

    sorted_data = sorted(data_list, key=lambda item: (int(item['x_coordinate']), int(item['y_coordinate'])))

    print(json.dumps(sorted_data, indent=4, ensure_ascii=False))

    # Determine the size of the grid
    width = max(int(item['x_coordinate']) for item in sorted_data) + 1
    height = max(int(item['y_coordinate']) for item in sorted_data) + 1

    # Create an empty grid initialized with spaces
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Fill the grid with the characters at the specified coordinates
    for item in sorted_data:
        x = int(item['x_coordinate'])
        y = int(item['y_coordinate'])
        grid[height - y - 1][x] = item['character']

    # Print the grid
    for row in grid:
        print(''.join(row))


# Example usage with the given Google Doc URL
retrieve_and_print_secret_message('https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub')