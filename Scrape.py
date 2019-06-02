from bs4 import BeautifulSoup
import requests
from bs4 import element
import functools


urls = ["https://tutoring.csc.calpoly.edu/",
        "https://csc.calpoly.edu/clubs/",
        "https://engineering.calpoly.edu/student-clubs-organizations",
        "https://statistics.calpoly.edu/content/statclub",
        "http://www.cosam.calpoly.edu/content/student_orgs",
        "https://statistics.calpoly.edu/content/tutoring ",
        "https://csc.calpoly.edu/current/free-tutoring/",
        "http://tutoring.csc.calpoly.edu/tutors/",
        "http://tutoring.csc.calpoly.edu/schedule/",
        "https://cpe.calpoly.edu/clubs/association-computing-and-machinery",
        "https://web.calpoly.edu/~wish/pages/officers.html",
        "https://web.calpoly.edu/~wish/index.html",
        "http://cplug.org/projects.html",
        "https://thewhitehat.club//about",
        "https://thewhitehat.club/officers",
        "https://www.slohacks.com/"
        ]



def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        print(f"Calling {func.__name__}")
        value = func(*args, **kwargs)
        print(value)
        return value
    return wrapper_debug


def get_clubs_and_contact_info(div):
    info = {}
    club_contact = div.find_all('td')
    for idx in range(0, len(club_contact), 2):
        info[club_contact[idx].string] = club_contact[idx+1].string
    return info


r = requests.get(urls[2])

soup = BeautifulSoup(r.text, 'html.parser')

@debug
def CS_get_club_info(soup):
    for div in soup.find_all('div', attrs={'class': 'accordion'}):
        csse = div.find('h2', attrs={'id':
                    'Computer_Science_and_Software_Engineering'})
        if csse:
            csse = csse.text
            return get_clubs_and_contact_info(div), csse


CS_get_club_info(soup)

@debug
def stat_get_club_info(h):
    club = h.find_all('td')
    club_info = {}
    counter = 0
    text = ""
    extract = ["Contact", "President", "Advisor"]
    curr = 0
    for info in club:
        counter += 1
        text += " " + info.string
        if counter % 3 == 0:
            club_info[extract[curr]] = text
            text = ""
            curr += 1
    return club_info


def get_data_science_info(h):
    return stat_get_club_info(h.findNext('table'))


def get_stat_club_info(h):
    return stat_get_club_info(h.findNext('table').findNext('table'))


@debug
def statistics_deparment_info(soup):
    h = soup.find('h2', attrs={'id': 'Statistics_Department'})
    club_links = []
    stat_clubs = []
    for tag in h.fetchNextSiblings():
        if 'Club' in str(tag.string):
            stat_clubs.append(tag.string)
            club_links.append(tag.find('a')['href'])
    data_science = get_data_science_info(h)
    stat_club = get_stat_club_info(h)
    links = {}
    for idx, club in enumerate(club_links):
        links[stat_clubs[idx]] = club
    links['Data Science'] = data_science
    links['Stat Club'] = stat_club

    return links


r = requests.get(urls[4])
soup = BeautifulSoup(r.text, 'html.parser')
statistics_deparment_info(soup)


def _get_upcoming_events(info):
    return info.string, None


def _get_program(info):
    program = ''
    link = ''
    for content in info.contents:
        if isinstance(content, element.Tag):
            program += content.string
            link = content['href']
        else:
            program += content
    return program, link


def _get_officers(info):
    return info.text, None


@debug
def extract_statistics_deparment_info(soup):
    main_content = soup.find('div', class_='field-items')
    stat_info = main_content.find_next('p')
    stat_club = {}
    stat_club['about'] = stat_info.text
    titles = {
        "Upcoming Events": _get_upcoming_events,
        "Stat Buddy Program": _get_program,
        "2018-2019 STAT Club Officers": _get_officers,
        "2017-2018 STAT Club Officers": _get_officers
    }

    for title in main_content.find_all('h2'):
        function = titles.get(title.string)
        if function:
            stat_club[title.string], link = function(title.find_next_sibling())
            if link:
                stat_club['signup_for_mentor'] = link
    advisors = main_content.find('h3').find_next()
    stat_club["Advisors"] = advisors.text
    return stat_club


r = requests.get(urls[3])
soup = BeautifulSoup(r.text, 'html.parser')
extract_statistics_deparment_info(soup)

@debug
def extract_stat_tutoring(soup):
    csse_tutoring = {}
    title = soup.find('h1', class_="page-title")
    csse_tutoring['title'] = title.text
    main_content = soup.find_all('div',class_='field-item')
    for x in main_content:
        if x:
            csse_tutoring['info'] = x.text.strip()

    tutors = soup.find('div', class_='field-item').find('a')['href']
    csse_tutoring['tutors'] = tutors
    tutor_hours = soup.find('div', class_='field-item').find('img')['src']
    csse_tutoring['tutor_hours'] = tutor_hours
    return csse_tutoring


r = requests.get(urls[5])
soup = BeautifulSoup(r.text, 'html.parser')
extract_stat_tutoring(soup)


def extract_tutoring_info(p):
    line = p.split('\n')
    keys = [None, 'Building and Room', 'Days', 'Time', 'Unavailable', None]
    tutoring_center_info = {}
    for idx, l in enumerate(line):
        l = l.strip()
        if l:
            tutoring_center_info[keys[idx]] = l
    return tutoring_center_info


@debug
def extract_tutoring_center(soup):
    hours = soup.find('iframe')['src']
    tutoring_center = dict()
    tutoring_center['Hours'] = hours
    div = soup.find('div', {'id': 'contentHeader'})
    center = extract_tutoring_info(div.find('p').text)
    tutoring_center.update(center)
    return center


r = requests.get(urls[8])
soup = BeautifulSoup(r.text, 'html.parser')
extract_tutoring_center(soup)

@debug
def extract_info_from_acm(soup):
    #TODO
    pass


r = requests.get(urls[9])
soup = BeautifulSoup(r.text, 'html.parser')
extract_info_from_acm(soup)

@debug
def extract_info_from_wish(soup):
    people = {}
    for x in soup.find_all('h3'):
        t = x.text.strip().split('\n')
        people[t[-1]] = t[0]
    advisors = soup.find_all('h2')[-1]
    advisors_email = {}
    for advisor in advisors.find_next_siblings():
        s = advisor.text.strip().split(' ')
        advisors_email = {s[0] + " " + s[1], s[-1]}
    wish = {}
    wish['People'] = people
    wish['Adivsors'] = advisors_email
    wish['Location'] = "N/A"
    return wish


r = requests.get(urls[10])
soup = BeautifulSoup(r.text, 'html.parser')
extract_info_from_wish(soup)

@debug
def extract_contact_from_wish(soup):
    contact = soup.find('div',class_='text-right')
    wish = {}
    wish_about = ''
    for about in soup.find('div', class_="col-sm-8").find('p').text.split('\n'):
        wish_about += about.strip()
    wish['About'] = wish_about
    wish["WISH Contact"] = contact.find('a').text.strip()
    return wish




r = requests.get(urls[11])
soup = BeautifulSoup(r.text, 'html.parser')
extract_contact_from_wish(soup)

@debug
def extract_projects_from_cplug(soup):
    projects = dict()
    projects['CPLUG projects'] = []
    for x in soup.find_all('h1'):
        projects['CPLUG projects'].append(x.text.strip())
    projects['Contact'] = "cplug@calpoly.edu"
    projects['Location'] = "N/A"
    return projects


r = requests.get(urls[12])
soup = BeautifulSoup(r.text, 'html.parser')
extract_projects_from_cplug(soup)

@debug
def extract_about_from_whitehat(soup):
    about = soup.find_all('div', class_='about-section')[-1]
    whitehat = {}

    whitehat['about'] = about.text
    return whitehat


r = requests.get(urls[13])
soup = BeautifulSoup(r.text, 'html.parser')
extract_about_from_whitehat(soup)

@debug
def extract_officers_from_whitehat(soup):
    officer_list = {}
    temp_dict = {}
    for officer in soup.find_all('div', class_='officer-item'):
        item = officer.text.strip().split("\n")
        temp_dict[item[0]] = item[-1]
    officer_list['Officers'] = temp_dict
    lab = soup.find('div', attrs={'id': 'footer-left'})
    officer_list['Meeting'] = lab.a.text
    email = soup.find('div', attrs={'id': 'footer-right'})
    officer_list['Contact'] = email.a['href'].split(':')[-1]
    return officer_list


r = requests.get(urls[14])
soup = BeautifulSoup(r.text, 'html.parser')
extract_officers_from_whitehat(soup)

@debug
def extract_slo_hacks(soup):
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    workshop = {}
    temp_dict = {}
    schedule = {}
    for day in days:
        div = soup.find('h2', text=day)
        if div:
            for sibling in div.find_next_siblings():
                event = sibling.text
                events = event.split(',')
                temp_dict[events[0]] = events[-1]
            schedule[day] = temp_dict
    workshop['Schedule'] = schedule
    workshop['Contact'] = "team@slohacks.com"
    workshop['Location'] = "N/A"
    return workshop


r = requests.get(urls[15])
soup = BeautifulSoup(r.text, 'html.parser')
extract_slo_hacks(soup)

