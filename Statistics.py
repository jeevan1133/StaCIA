from database import *
from bs4 import element
import re
from CSC import get_soup

urls = [ "https://statistics.calpoly.edu/content/statclub",
        "http://www.cosam.calpoly.edu/content/student_orgs",
        "https://statistics.calpoly.edu/content/tutoring "
        ]


def _get_upcoming_events(info):
    return info.string, None


def _get_program(info):
    program = ''
    advanced = info.find_next_sibling()
    stat_form = []
    for content in info.contents:
        if isinstance(content, element.Tag):
            program += "visit " + content['href']
            stat_form.append(content['href'])
        else:
            program += content
    stat_form.append(advanced.a['href'])
    return program, stat_form


def _get_officers(info):
    officers = {}
    for item in info.text.split('\n'):
        if item:
            people = item.split(':')
            officers[people[0]] = people[1]
    return officers, None


def extract_statistics_deparment_info(url):
    soup = get_soup(url)
    main_content = soup.find('div', class_='field-items')
    stat_club = {}
    titles = {
        "Upcoming Events": _get_upcoming_events,
        "Stat Buddy Program": _get_program,
        "2018-2019 STAT Club Officers": _get_officers
    }

    for title in main_content.find_all('h2'):
        function = titles.get(title.string.strip())
        if "2017-2018" in title.string:
            stat_club["2017-2018"], _ = _get_officers(title.find_next_sibling())
        if function:
            info, link = function(title.find_next_sibling())
            key = title.string
            if "2018-2019" in key:
                key = "2018-2019"
            elif "Upcoming Events" in key:
                key = "Events"
            stat_club[key] = info

            if link:
                stat_club['signup_for_mentor'] = link[1][:-1]
                stat_club['signup_for_classes'] = link[0][:-1]
    advisers = main_content.find('h3').find_next()
    stat_club["Advisors"] = advisers.text
    stat_club["Website"] = url
    return stat_club


def stat_get_club_info(h):
    club = h.find_all('td')
    club_info = {}
    counter = 0
    text = ""
    temp_dict = {}
    for info in club:
        counter += 1
        text += " " + info.string
        if counter % 3 == 0:
            title_person = text.split(':')
            title = "Contact"
            if len(title_person) >= 2:
                title = title_person[0].strip()
                text = title_person[1].lstrip().split(' ')
                temp_dict["Name"] = text[0] + " " + text[1]
                temp_dict["Email"] = text[2]
                temp_dict["Phone"] = text[3]
                club_info[title] = temp_dict
                temp_dict = {}
            else:
                club_info[title] = text.strip().split(" ")[-1]
            text = ""
    return club_info


def get_data_science_info(h):
    return stat_get_club_info(h.findNext('table'))


def get_stat_club_info(h):
    return stat_get_club_info(h.findNext('table').findNext('table'))


def statistics_deparment_info(url):
    soup = get_soup(url)
    h = soup.find('h2', attrs={'id': 'Statistics_Department'})
    club_links = []
    stat_clubs = []
    club_info = {}
    for tag in h.fetchNextSiblings():
        if 'Club' in str(tag.string):
            stat_clubs.append(tag.string)
            p = tag.find_next_sibling()
            club_info[tag.string] = p.text
            club_links.append(tag.find('a')['href'])
    data_science = get_data_science_info(h)
    stat_club = get_stat_club_info(h)
    clubs = {}
    contacts = {'Data Science Club': data_science['Contact'],
                'STAT Club': stat_club['Contact']}

    for idx, club in enumerate(club_links):
        clubs[stat_clubs[idx]] = {}
        clubs[stat_clubs[idx]]['About'] = club_info[stat_clubs[idx]]
        clubs[stat_clubs[idx]]['Contact'] = contacts[stat_clubs[idx]]
        clubs[stat_clubs[idx]]['Website'] = club
        clubs[stat_clubs[idx]]['Department'] = "STAT"
        clubs[stat_clubs[idx]]['Location'] = None
    clubs_president = [data_science, stat_club]
    for idx, c in enumerate(stat_clubs):
        clubs[c]['Officers'] = {}
        clubs[c]['Officers']['President'] = {}
        clubs[c]['Officers']['President'] = clubs_president[idx]['President']
        clubs[c]['Advisors'] = clubs_president[idx]['Advisor']
    return clubs


def extract_stat_tutoring(url):
    soup = get_soup(url)
    stat_tutoring = {}
    main_content = soup.find_all('div', class_='field-item')
    for main_ in main_content:
        if main_:
            info = []
            for x in soup.find('div', class_='field-item').find_all('div', class_='clear'):
                info.append(re.sub('\xa0', ' ', x.text))
            stat_tutoring[info[0]] = info[1]
            stat_tutoring[info[2]] = info[3].split('.')[0]
    tutors = soup.find('div', class_='field-item').find('a')['href']
    stat_tutoring['Tutors'] = tutors
    tutor_hours = soup.find('div', class_='field-item').find('img')['src']
    stat_tutoring['Tutor Hours'] = tutor_hours
    return stat_tutoring

