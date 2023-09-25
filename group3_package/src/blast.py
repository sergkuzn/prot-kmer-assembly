from time import sleep
import io
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import List


def blast_website(amino_acid_seqs: List[str], docker=True) -> List[str]:
    """
    Get list of proteins from amino acid sequences.
    BLAST, use the website.

    """
    # Open browser
    if docker:
        driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
                                  desired_capabilities=webdriver.DesiredCapabilities.CHROME)
    else:
        print('Use Chrome for BLAST')
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # in the background
        chrome_options.add_argument("--log-level=3")  # in the background
        driver = webdriver.Chrome(options=chrome_options)

    # Open link
    blast_url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome"
    driver.get(blast_url)

    # Paste sequences
    query = '\n'.join(amino_acid_seqs)
    text_element = driver.find_element(value='seq')
    text_element.clear()
    text_element.send_keys(query)

    # Click BLAST button
    driver.find_element(value='blastButton1').click()

    # Wait until the page with results is loaded
    print('BLAST. Sleep 40s.', end=' ')
    sleep(40)
    while True:
        result_elements = driver.find_elements(By.CLASS_NAME, 'secFlitRes')
        if len(result_elements) == 0:
            sleep(30)
            print('More 30s.')
        else:
            print('\nBLAST. Results loaded.')
            break

    # Find a link to download JSON
    download_url = None
    for el in driver.find_elements(By.CLASS_NAME, 'xgl'):
        href = el.get_attribute('href')
        if type(href) == str:
            if 'RESULTS_FILE' in href and 'JSON' in href:
                download_url = href
                break
    assert download_url is not None

    # Download JSON
    r = requests.get(download_url)
    result = json.load(io.BytesIO(r.content))

    # Parse json
    try:
        hits_array = result['BlastOutput2'][0]['report']['results']['search']['hits']
        prots = [el['description'][0]['title'] for el in hits_array]
    except:
        prots = []
    return prots
