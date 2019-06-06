from bs4 import BeautifulSoup
import requests
import re
import operator

urls = ["http://tutoring.csc.calpoly.edu/",
        "https://csc.calpoly.edu/clubs/",
        "https://engineering.calpoly.edu/student-clubs-organizations"
        ]


def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def CS_get_club_info(url):
    soup = get_soup(url)

    def get_clubs_and_contact_info(div):
        info = {}
        club_contact = div.find_all('td')
        for idx in range(0, len(club_contact), 2):
            info[club_contact[idx].text] = club_contact[idx + 1].text
        return info

    for div in soup.find_all('div', attrs={'class': 'accordion'}):
        csse = div.find('h2',
                        attrs={'id':
                                   'Computer_Science_and_Software_Engineering'})
        if csse:
            return get_clubs_and_contact_info(div)


def extract_from_acm(clubs):
    club = list(clubs.keys())[-1]
    url = "https://" + clubs[club]['Website']
    soup = get_soup(url)
    about = soup.find('div', {"id": "mainLeftFull"}).p.text
    clubs[club]["About"] = about
    clubs[club]['Contact'] = "N/A"
    clubs[club]['Department'] = "CSSE"
    return clubs


def extract_info_from_wish(soup):
    wish = {}
    wish['Location'] = "N/A"
    wish['Department'] = "CSSE"
    wish['About'] = soup.find('h2').find_next().text.strip()
    wish['Contact'] = soup.find('div', class_='text-right').a.text.strip()
    return wish


def extract_officers_from_wish():
    url = "https://web.calpoly.edu/~wish/pages/officers.html"
    soup = get_soup(url)
    officers = {}
    for x in soup.find_all('h3'):
        t = x.text.strip().split('\n')
        officers[t[-1]] = t[0]
    advisors = soup.find_all('h2')[-1]
    advisors_email = []
    for advisor in advisors.parent.find_next_siblings():
        s = advisor.text.strip().split(' ')
        advisors_email.append((s[0] + " " + s[1], s[-1]))
    return officers, advisors_email


def get_schedules(soup, days):
    date, tutors = [], []
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) == 7:
            for td in tds:
                if td.text.isdigit():
                    date.append(td.text)
                else:
                    tutors.append(td.text)
    time_day = []
    for i, d in enumerate(date):
        tutor = tutors[i]
        if tutor:
            tutor = tutors[i].split(':')
            time = tutor[0].split('T')[0]
            people = tutor[-1].strip()
            time_day.append((days[date.index(d) % 7], time, people))
    return time_day


def extract_from_google_calendar(soup):
    url = soup.find('iframe')['src']
    url = re.sub('&amp;', '&', url)
    r = requests.get(url)
    soup_calendar = BeautifulSoup(r.text, 'html.parser')
    url = soup_calendar.find('noscript').find('a')['href']
    url = re.sub('&amp;', '&', url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    days = [day.text for day in soup.find_all('th', class_='column-label')]
    events = get_schedules(soup, days)
    days = list(map(operator.itemgetter(0), events))
    time_location = list(map(operator.itemgetter(2), events))
    temp = []
    for time in time_location:
        temp.append(('m '.join(time.split('m'))))
    return days, temp


def extract_from_wish(clubs):
    try:
        club = list(clubs.keys())[-1]
        url = "https://" + clubs[club]['Website']
        soup = get_soup(url)
        wish_info = extract_info_from_wish(soup)
        for k, v in wish_info.items():
            clubs[club][k] = v
        clubs[club]['Officers'], advisors = \
            extract_officers_from_wish()
        clubs[club]['Advisors'] = {}
        clubs[club]['Advisors']['Name'] = []
        clubs[club]['Advisors']['Email'] = []
        for advisor in advisors:
            clubs[club]['Advisors']['Name'].append(advisor[0])
            clubs[club]['Advisors']['Email'].append(advisor[1])
        clubs[club]['Schedule'] = []
        url = "https://web.calpoly.edu/~wish/pages/calendar.html"
        soup = get_soup(url)
        days, temp = extract_from_google_calendar(soup)
        for idx, day in enumerate(days):
            clubs[club]['Schedule'].append(day + " " + temp[idx])
        return clubs
    except:
        return clubs


def extract_from_CPGD(clubs):
    club = list(clubs.keys())[-1]

    def get_officers(soup):
        officers = {}
        cpgd = soup.find('div', {'id': 'TextList1'}).div.text.strip()
        for officer in cpgd.split('\n'):
            officer = officer.replace('(', '').replace(')', '')
            titles = officer.split(' ')
            officers[titles[-1]] = titles[0] + " " + titles[1]
        return officers

    url = "http://www." + clubs[club]['Website']
    soup = get_soup(url)
    cpgd = soup.find('div', {'id': 'HTML1'}).div.text.strip()
    about = ''.join(cpgd.split('.')[:2])
    clubs[club]['About'] = about
    clubs[club]['Location'] = ''.join(cpgd.split('.')[2:]).strip()
    clubs[club]['Department'] = "CSSE"
    clubs[club]['Officers'] = get_officers(soup)
    email = re.search(r'(\w+)\s*?@\s*?(\w+).org',
                      soup.find('div', {'id': "HTML2"}).div.text.strip()).group()
    clubs[club]['Contact'] = email
    return clubs


def extract_projects_from_cplug(soup):
    projects = []
    for x in soup.find_all('h1'):
        projects.append(x.text.strip())
    return projects


def extract_from_CPLUG(clubs):
    club = list(clubs.keys())[-1]
    url = "http://www." + clubs[club]['Website']
    soup = get_soup(url)
    clubs[club]['About'] = soup.find('div', class_='content').p.text
    h3 = soup.find_all('h3')[-1]
    email = h3.find_next_sibling().text.strip()
    email = re.search(r'(\w+)@(\w+).(\w+)', email).group()
    clubs[club]['Contact'] = email
    clubs[club]['Location'] = "N/A"
    clubs[club]['Department'] = "CSSE"
    url = "http://cplug.org/projects.html"
    soup = get_soup(url)
    clubs[club]['Projects'] = extract_projects_from_cplug(soup)
    return clubs


def get_schedule_whitehat():
    url  = "https://thewhitehat.club/calendar"
    soup = get_soup(url)
    days, temp = extract_from_google_calendar(soup)
    schedule = []
    try:
        assert (len(days) == len(temp))
    except AssertionError:
        return
    for idx, day in enumerate(days):
        schedule.append(day + " " + temp[idx])
    return schedule


def get_officers_whitehat():
    url = "https://thewhitehat.club/officers"
    soup = get_soup(url)
    officer_list = {}
    temp_dict = {}
    for officer in soup.find_all('div', class_='officer-item'):
        item = officer.text.strip().split("\n")
        temp_dict[item[0]] = item[-1]
    officer_list['Officers'] = temp_dict
    lab = soup.find('div', attrs={'id': 'footer-left'})
    officer_list['Meeting'] = lab.a.text
    return officer_list


def extract_info_from_whitehat(soup):
    try:
        about = soup.find_all('div', class_='about-section')[-1]
        whitehat = {'About': about.text.strip()}
        email = soup.find('div', attrs={'id': 'footer-right'})
        whitehat['Contact'] = email.a['href'].split(':')[-1]
        whitehat['Department'] = "CSSE"
        whitehat['Schedule'] = get_schedule_whitehat()
        for k, v in get_officers_whitehat().items():
            whitehat[k] = v
        return whitehat
    except:
        pass


def extract_from_whitehat(clubs):
    url = "https://thewhitehat.club/about"
    soup = get_soup(url)
    whitehat = extract_info_from_whitehat(soup)
    club = list(clubs.keys())[-1]
    clubs[club]['Website'] = club
    if not whitehat:
        return clubs
    clubs[club].update(whitehat)
    return clubs


def extract_from_CPADC(clubs):
    club = list(clubs.keys())[-1]
    url = "https://www." + clubs[club]['Website']
    soup = get_soup(url)
    clubs[club]['Location'] = "N/A"
    for div in soup.find_all('div', class_='text-center'):
        if div.find('i', class_='sr-contact'):
            clubs[club]['Contact'] = div.text.strip()
    people = soup.find_all('div', class_='service-box')[4:]
    clubs[club]["Officers"] = {}
    for officer in people:
        officer = officer.text.strip().split('\n')
        clubs[club]['Officers'][officer[-1]] = officer[0]
    about = soup.find_all('div', class_='service-box')[:4]
    cpadc = ""
    for ab in about:
        cpadc += ab.text.strip()
    clubs[club]["About"] = cpadc
    clubs[club]['Department'] = "CSSE"
    return clubs


def extract_from_robotics(clubs):

    def get_contact_and_officers(url):
        soup = get_soup(url)
        club_officers = soup.find_all('div', class_='sqs-block-content')[-5]
        officers = {}
        officers['Officers'] = {}
        for officer in club_officers:
            tite_officer = officer.text.split('-')
            if len(tite_officer) >= 2:
                officers['Officers'][tite_officer[0].strip()] = tite_officer[1].strip()
            if '@' in officer.text:
                officers['Contact'] = officer.text.strip()
        return officers

    def get_meetings():
        url = "https://www.calpolyrobotics.com/membership"
        soup = get_soup(url)
        return soup.find('div', {'id': 'block-a6630fefb74bf392d66b'}).text.split('.')[0]

    club = list(clubs.keys())[-1]
    url = "https://www." + clubs[club]['Website']
    soup = get_soup(url)
    about = soup.find('div',class_='sqs-block-content').p.text.strip()
    clubs[club]['About'] = about
    clubs[club]['Department'] = "CSSE"
    projects = list(soup.find('div',class_='subnav').stripped_strings)[:-1]
    clubs[club]['Projects'] = projects
    clubs[club]['Location'] = soup.find('footer').text.strip().split('-',1)[-1].strip()
    clubs[club]['Meeting'] = get_meetings()
    url = "https://www.calpolyrobotics.com/contact"
    officers = get_contact_and_officers(url)
    clubs[club].update(officers)
    return clubs


def extract_from_SLOHacks(clubs):
    club = list(clubs.keys())[-1]
    url = "https://www." + clubs[club]['Website']
    soup = get_soup(url)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
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
    workshop['Location'] = "CalPoly, San Luis Obispo"
    workshop['About'] = soup.find('div', class_="src-components----History-module---historyText---2jWN3").text
    workshop['Department'] = "CSSE"
    clubs[club].update(workshop)
    return workshop


def get_csc_clubs():
    clubs_contact = CS_get_club_info(urls[2])
    clubs = {}
    functions = {}
    extract_clubs = [extract_from_acm, extract_from_wish, extract_from_CPGD,
                     extract_from_CPLUG, extract_from_whitehat,
                     extract_from_CPADC, extract_from_robotics,
                     extract_from_SLOHacks
                     ]
    idx = 0
    try:
        for k, v in clubs_contact.items():
            clubs[k] = {}
            functions[k] = extract_clubs[idx]
            idx += 1
            clubs[k]['Website'] = v
            function = functions.get(k)
            if function:
                p = function(clubs)
        return clubs
    except:
        pass


def extract_tutoring_info(p):
    line = p.split('\n')
    keys = [None, 'Building and Room', 'Days', 'Time', 'Unavailable', None]
    tutoring_center_info = {}
    for idx, l in enumerate(line):
        l = l.strip()
        if l:
            tutoring_center_info[keys[idx]] = l.split('.')[0]
    return tutoring_center_info


def extract_tutoring_center(soup):
    hours = soup.find('iframe')['src']
    tutoring_center = dict()
    tutoring_center['Hours'] = hours
    div = soup.find('div', {'id': 'contentHeader'})
    center = extract_tutoring_info(div.find('p').text)
    tutoring_center.update(center)
    return center


def getTutorNames():
    url = "http://tutoring.csc.calpoly.edu/tutors/"
    soup = get_soup(url)
    tutors = soup.find("h1", {"id": "head-tutor"}).text
    tutors = [tutors.split(': ')[-1].split(' ')[0]]
    for row in soup.find_all("div", class_="articleEntry"):
        if row.find('h2'):
            tutors.append(row.find('h2').text)
    tutor_first_name = []
    for tutor in tutors:
        tutor_first_name.append(tutor.split(' ')[0])
    return tutor_first_name


def insert_into_tutorSchedule(time_day_people):
    tutors = list(map(operator.itemgetter(2), time_day_people))
    tutors = ', '.join(tutors).split(', ')
    more_tutors = getTutorNames()
    tutors.extend(more_tutors)
    tutors = set(tutors)
    map_tutors = {}
    for idx, tutor in enumerate(tutors):
        map_tutors[idx + 1] = tutor
    return map_tutors


def extract_csc_tutoring_hours(url):
    soup = get_soup(url)
    url = soup.find('iframe')['src']
    url = re.sub('&amp;', '&', url)
    soup = get_soup(url)
    url = soup.find('noscript').find('a')['href']
    url = re.sub('&amp;', '&', url)
    soup = get_soup(url)
    days = [day.text for day in soup.find_all('th', class_='column-label')]
    time_day = get_schedules(soup, days)
    print(time_day)
    return insert_into_tutorSchedule(time_day), time_day


def tutoring_csc():
    url = "http://tutoring.csc.calpoly.edu/schedule/"
    return extract_csc_tutoring_hours(url)


def get_csc_tutor_info(url):
    soup = get_soup(url)
    div = soup.find('div', {'id': 'contentHeader'})
    text = re.sub('\s+', ' ', div.p.text)
    classes = re.findall('(\d+)', text)
    tutoring_info = {}
    about = div.p.text.strip()
    about = re.sub('\s+', ' ', about)
    tutoring_info[div.h1.text] = about
    for h2 in soup.find_all('h2'):
        if h2.find_next_sibling():
            info = h2.find_next_sibling().text.strip()
            info = re.sub('\s+', ' ', info)
            tutoring_info[h2.text] = info
    return classes, tutoring_info