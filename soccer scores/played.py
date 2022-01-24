import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from time import sleep
from datetime import datetime
from selenium import webdriver
import random
import sqlite3
import os

c_path = os.path.dirname(__file__)
os.chdir(c_path)
# print(c_path)

data_base = str(datetime.today().date())
conn = sqlite3.connect(f'results\\backup\\back-up-{data_base}.db')
cr = conn.cursor()
df_config = pd.read_excel('config.xlsx')
df_config.active = df_config.active.astype(int)
all_links_leagues = df_config['link'][df_config['active'] == 1]
driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()

for c, link in enumerate(all_links_leagues):
    os.system('cls')
    print(f'scraping : {link} {c+1}/{len(all_links_leagues)}', end='\n\n')
    c = 0
    driver.get(link)
    sleep(3*random.random())
    try:
        more = driver.find_element_by_link_text('Mostra più incontri')
        more.click()
        sleep(3)
    except:
        pass
    sleep(3*random.random())
    try:
        more = driver.find_element_by_link_text('Mostra più incontri')
        more.click()
        sleep(3)
    except:
        pass
    try:
        more = driver.find_element_by_link_text('Mostra più incontri')
        more.click()
        sleep(3)
    except:
        pass
    try:
        more = driver.find_element_by_link_text('Mostra più incontri')
        more.click()
        sleep(3)
    except:
        pass

    soup_home = BeautifulSoup(driver.page_source, 'lxml')
    all_raw_tags_1 = []
    all_raw_tags_1 = soup_home.find_all('div', class_='event__match')
    all_raw_tags_2 = [x['id'].replace('g_1_', '') for x in all_raw_tags_1]
    all_matches_links = [
        f'https://www.diretta.it/partita/{x}/#informazioni-partita/informazioni-partita' for x in all_raw_tags_2]

    soups = []
    for c, match_link in enumerate(all_matches_links):
        print(f'match: {c+1}/{len(all_matches_links)}')
        sleep(random.random())
        driver.get(match_link)
        sleep(random.random()*1.2)
        soups.append(BeautifulSoup(driver.page_source, 'lxml'))
        c += 1
        if c == 3:
            break

    countries = []
    leagues = []
    dates = []
    times = []
    homes = []
    aways = []
    fts = []
    hts = []
    first_values = []
    first_dirs = []
    x_values = []
    x_dirs = []
    second_values = []
    second_dirs = []

    for c, soup in enumerate(soups):

        try:
            try:
                three_ods_raw = soup.find_all('div', class_='cellWrapper')

                try:
                    first_value = three_ods_raw[0]['title']
                    first_value = re.findall('\d+.\d+', first_value)[-1]
                    first_dir = three_ods_raw[0]['title']
                    first_dir = re.findall(r'\[\w\]', first_dir)[0]
                    first_dir = first_dir.replace('[', '')
                    first_dir = first_dir.replace(']', '')
                    first_dir = first_dir.replace('u', 'UP')
                    first_dir = first_dir.replace('d', 'DOWN')
                except IndexError:
                    first_value = three_ods_raw[0].text
                    first_value = re.findall(
                        '\d+.\d+', first_value)[-1]
                    first_dir = '-'

                try:
                    x_value = three_ods_raw[1]['title']
                    x_value = re.findall('\d+.\d+', x_value)[-1]

                    x_dir = three_ods_raw[1]['title']
                    x_dir = re.findall(r'\[\w\]', x_dir)[0]
                    x_dir = x_dir.replace('[', '')
                    x_dir = x_dir.replace(']', '')
                    x_dir = x_dir.replace('u', 'UP')
                    x_dir = x_dir.replace('d', 'DOWN')
                except IndexError:
                    x_value = three_ods_raw[1].text
                    x_value = re.findall(
                        '\d+.\d+', x_value)[-1]
                    x_dir = '-'

                try:
                    second_value = three_ods_raw[2]['title']
                    second_value = re.findall('\d+.\d+', second_value)[-1]
                    second_dir = three_ods_raw[2]['title']
                    second_dir = re.findall(r'\[\w\]', second_dir)[0]
                    second_dir = second_dir.replace('[', '')
                    second_dir = second_dir.replace(']', '')
                    second_dir = second_dir.replace('u', 'UP')
                    second_dir = second_dir.replace('d', 'DOWN')
                except IndexError:
                    second_value = three_ods_raw[2].text
                    second_value = re.findall(
                        '\d+.\d+', second_value)[-1]
                    second_dir = '-'

            except:
                first_value = '-'
                first_dir = '-'
                x_dir = '-'
                x_value = '-'
                second_dir = '-'
                second_value = '-'

    #         first_value = three_ods_raw[0]['title'][7:]
    #         first_dir = three_ods_raw[0]['title'][5]
    #         if first_value == '1.04':
    #             print(c)

    #         x_value = three_ods_raw[1]['title'][7:]
    #         x_dir = three_ods_raw[1]['title'][5]

    #         second_value = three_ods_raw[2]['title'][7:]
    #         second_dir = three_ods_raw[2]['title'][5]

            country_league = soup.find(
                'span', class_='tournamentHeader__country').text
            country = country_league.split(':')[0].strip()
            league = country_league.split(':')[1].strip()
            countries.append(country)
            leagues.append(league)

            date_time = soup.find(
                'div', class_='duelParticipant__startTime').text
            date_ = date_time.split()[0]
            time_ = date_time.split()[1]
            dates.append(date_)
            times.append(time_)

            home = soup.find(
                'div', class_='duelParticipant__home').text.strip()
            homes.append(home)
            away = soup.find(
                'div', class_='duelParticipant__away').text.strip()
            aways.append(away)

            full_time = soup.find(
                'div', class_='duelParticipant__score').text.strip('Finale')
            full_time = full_time.strip('\xa0')
            try:
                full_time = re.findall('\d+-\d+', full_time)[0]
            except:
                full_time = '-'
            # print(full_time)
            if full_time == '-':
                half_time = '-'
            else:
                try:
                    half_time = soup.find(
                        'div', class_='smv__incidentsHeader section__title').text.replace(' ', '')
                    half_time = re.findall('\d+-\d+', half_time)[-1]
                    # print(half_time)
                except:
                    half_time = '-'
                    # half-time-error
                    print(c, 'half_time error')

            first_values.append(first_value)
            first_dirs.append(first_dir)

            x_values.append(x_value)
            x_dirs.append(x_dir)

            second_values.append(second_value)
            second_dirs.append(second_dir)

            fts.append(full_time)
            hts.append(half_time)
        except:
            print(c, 'full-error')
    df = pd.DataFrame({
        'country': countries,
        'league': leagues,
        'date': dates,
        'time': times,
        'home': homes,
        'away': aways,
        'FT': fts,
        'HT': hts,
        '_1_dir': first_dirs,
        '_1': first_values,
        'x_dir': x_dirs,
        'x': x_values,
        '_2_dir': second_dirs,
        '_2': second_values
    })
    rr = link.split('/')
    country_name = rr[-4].capitalize()
    league_name = rr[-3].capitalize()
    excel_name = f'{country_name}-{league_name}'
    tablename = f'{rr[-4]}_{rr[-3]}'
    tablename_sql = tablename.replace('-', '_')
    tablename_sql = tablename_sql.replace(':', '_')
    df.to_excel(f'results\\played\\{tablename_sql}.xlsx',
                index=False, sheet_name=f'{excel_name}')
    cr.execute(
        f'create table if not exists back_up (country text, league text, date text, time text, home text,away text, FT text, HT text, _1_dir text, _1 text, x_dir, x, _2_dir text, _2 );')
    df.to_sql(f'back_up', conn, if_exists='append',
              index=False, index_label=False)
driver.close()
conn.commit()
cr.close()
conn.close()
input('\nDone.....\nPress Enter to close')
