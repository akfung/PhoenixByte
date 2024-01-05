from bs4 import BeautifulSoup
import re
import requests
import json
import math

'''Script for scraping and formatting Supreme Court case summaries and court opinions from Justia since 2013'''

def remove_tags(text: str) -> str:
    '''helper method'''
    text = re.sub(r'\t|\r', '', text)
    text = re.sub(r'\n', ' ', text)
    text.encode('ascii', 'ignore').decode()
    return text

def clean_soup(url, verbose=False):
    '''Get docket no, court opinion, and justice opinions for a given case url'''

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html')
    case_details = dict()

    docket_no = soup.find_all(True, {'class':['flex-col', 'reset-width-below-tablet', 'item']})[0].find_all('span')[0].get_text()

    # get summary. if none, return empty
    case_summaries = soup.find_all('div', id='summary')
    if len(case_summaries) == 0:
        return docket_no, {'summary': 'Dismissed'}
    case_summary = case_summaries[0].get_text()
    case_details['summary'] = remove_tags(case_summary)
    
    # look for per curiam opinion
    per_curiam = soup.find_all(True,  {'data-gtm-label':['Opinions Tab - Per Curiam']})
    if len(per_curiam)>0:
        opinion = soup.find_all('div',  {'id':re.compile(r'tab-opinion-\d+')})[0]
        opinion = remove_tags(opinion.get_text())
        court_opinion_text = re.findall(r'(?<=Per Curiam.)[\w\W]+', opinion)[0].strip()
        case_details['court_opinion'] = court_opinion_text
    else:
    
        for opinion in soup.find_all('div', {'id': re.compile(r'tab-opinion-')})[1:]:

            opinion = remove_tags(opinion.get_text())

            justice_name = re.findall(r'(?<=Justice\s)\w+', opinion)[0]
            if verbose:
                print(justice_name)

            # get court opinion text
            court_opinion_text = re.findall(r'(?<=delivered the opinion of the Court.)[\w\W]+', opinion)

            if len(court_opinion_text) >0:
                justice_opinion = court_opinion_text[0].strip()
                case_details['court_opinion'] = justice_opinion
                case_details[justice_name] = justice_opinion
                if verbose:
                    print(justice_opinion)

            else:
                justice_opinion =  re.findall(r'((?<=dissenting.)[\w\W]+|(?<=concurring.)[\w\W]+)', opinion)[0].strip()
                if verbose:
                    print(justice_opinion)
                case_details[justice_name] = justice_opinion
    return docket_no, case_details

if __name__=="__main__":
    # Scrape case_urls from justia

    years = [f'https://supreme.justia.com/cases/federal/us/year/{i}.html' for i in range(2013, 2024)]
    case_urls = []

    for year_url in years:
        r = requests.get(year_url)
        soup = BeautifulSoup(r.content, 'html')
        for i in soup.find_all(True,  {'class':['color-green', 'text-soft-wrap']} ):
            case_urls.append('https://supreme.justia.com' + i.a['href'])

    # scrape cases, track errors
    case_data = dict()
    failed_urls = []
    i = 1
    for url in case_urls:
        print(f'Scraping case {i}')
        try:
            docket_no, opinions = clean_soup(url)
            assert opinions
            case_data[docket_no] = opinions
        except Exception as e:
            print(f'Failed on url {url}')
            failed_urls.append([url, str(e)])
        
        i+=1

    # Serialize case_data as json
    json_object = json.dumps(case_data, indent=4)
    
    # Writing to case_data.json
    with open("case_data.json", "w") as outfile:
        outfile.write(json_object)

    # Create chunked dataset for hugging face dataloaders

    data = []
    current = 1
    max_char = 4000
    for k,v in case_data.items():
        print(current)
        current +=1
        if v['summary'] != 'Dismissed':
            summary = re.findall(r'(?<=Justia Summary\s\s\s)[\w\W]+', v['summary'])[0]
        else:
            continue

        if v.get('court_opinion')==None:

            continue

        # remove notes from opinion
        if re.search(r'[\w\W]+(?=Notes 1 \xa0)', v['court_opinion']):
            court_opinion = re.findall(r'[\w\W]+(?=Notes 1 \xa0)', v['court_opinion'])[0]

        if len(court_opinion) + len(summary) > max_char:

            # chunk the opinions
            max_len = max_char - len(summary)

            chunk_size = int(max_len/ (math.ceil(max_len/ len(court_opinion))))
            chunk_suffix = 1
            for i in range(0, len(court_opinion), chunk_size):
                chunk = court_opinion[i:i+chunk_size]
                data.append({
                    'docket_no': k + str(chunk_suffix),
                    'summary': summary,
                    'opinion': chunk
                })

                chunk_suffix +=1
        
        else:
            data.append({
                'docket_no': k,
                'summary': summary,
                'opinion': v.get('court_opinion', '')
            })

    dataloader_formatted = dict(
        version='1.0',
        data=data
    )

    json_object = json.dumps(dataloader_formatted, indent=4)
    with open("chunked_case_data.json", "w") as outfile:
        outfile.write(json_object)
