import requests
from bs4 import BeautifulSoup
from random import seed
from random import randint

def generate(difficulty):

    if difficulty == 'easy':
        thresh = 40
    elif difficulty == 'normal':
        thresh = 60
    else:
        thresh = 75

    URL = 'https://www.sudokuweb.org/'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    board = [[None for _ in range(9)] for _ in range(9)]
    row = [[None for _ in range(9)] for _ in range(9)]

    row[0] = soup.find(id='line').text.strip()
    row[0] = ''.join(row[0].split())

    # Generate the complete sudoku numbers
    for i in range(1, 9):
        row[i] = soup.find(id='line'+str(i)).text.strip()
        row[i] = ''.join(row[i].split())

    # Make sudoku board
    for i in range(9):
        for j in range(9):
            if randint(0, 100) < thresh:
                board[i][j] = 0
            else:
                board[i][j] = int(row[i][j])
    return board

