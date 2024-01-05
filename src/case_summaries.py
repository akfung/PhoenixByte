import requests
import random
from bs4 import BeautifulSoup

class CaseSummaries:
    def __init__(self):
        self._case_summaries = None

    @property
    def case_summaries(self):
        if self._case_summaries == None:
            r = requests.get('https://en.wikipedia.org/wiki/List_of_pending_United_States_Supreme_Court_cases')
            soup = BeautifulSoup(r.content, 'html.parser')
            self._case_summaries = soup.find_all(True, {'class': ['wikitable', 'sortable', 'jquery-tablesorter']})[0].find_all('tr')[1:]
        return self._case_summaries

    def random_summary(self) -> str:
        # function to get a random case summary from wikipedia pending list
        row:str = random.choice(self.case_summaries)
        summary = row.find_all('td')[2]
        summary = summary.get_text()
        return summary
    