from bs4 import BeautifulSoup
import requests
from bs4 import element
import functools
from database import *
import re
import operator

urls = ["http://tutoring.csc.calpoly.edu/",
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
        "https://thewhitehat.club/about",
        "https://thewhitehat.club/officers",
        "https://www.slohacks.com/",
        "https://web.calpoly.edu/~wish/pages/calendar.html",
        "http://www.cpgd.org/"
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
        info[club_contact[idx].text] = club_contact[idx + 1].text
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


clubs, csse = CS_get_club_info(soup)

list_of_all_clubs = list(clubs.keys())


@debug
def extract_contact_from_wish(soup):
    contact = soup.find('div', class_='text-right')
    wish = {}
    wish_about = ''
    for about in soup.find('div', class_="col-sm-8").find('p').text.split('\n'):
        wish_about += about.strip()
    wish['About'] = wish_about
    wish["Contact"] = contact.find('a').text.strip()
    wish['Events'] = "https://web.calpoly.edu/~wish/pages/calendar.html"
    wish['Website'] = urls[11]
    wish['Department'] = "CSSE"
    return wish


r = requests.get(urls[11])
soup = BeautifulSoup(r.text, 'html.parser')


wish_club = extract_contact_from_wish(soup)
club = {}
club["WISH"] = wish_club


def insert_into_clubs(clubs, csse):
    for club, link in clubs.items():
        stmt = "INSERT INTO club (cname, department) VALUES ( \"%s\", \"%s\")"
        stmt = stmt % (club, "CSSE")
        # insert_into(stmt)


# insert_into_clubs(clubs, csse)

@debug
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
            title = "General Contact"
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


@debug
def statistics_deparment_info(soup):
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
    links = {}
    for idx, club in enumerate(club_links):
        links[stat_clubs[idx]] = {}
        links[stat_clubs[idx]]['About'] = club_info[stat_clubs[idx]]
        links[stat_clubs[idx]]['Contact'] = club
        links[stat_clubs[idx]]['Website'] = "N/A"
        links[stat_clubs[idx]]['Department'] = "STAT"
    return links, data_science, stat_club


r = requests.get(urls[4])
soup = BeautifulSoup(r.text, 'html.parser')


links, datascience, stat = statistics_deparment_info(soup)
for c, val in links.items():
    club[c] = val
# for club, link in links:
# list_of_all_clubs.appenda(list(links.keys()))
# print(links)
# print(datascience)
# print(stat)
# datascience_president = datascience["President"]
# datascience_advisor = datascience["Advisor"]
# stat_president = stat["President"]
# stat_advisor = stat["Advisor"]
# presidents = [datascience_president, stat_president]
# advisors = [datascience_advisor, stat_advisor]


def insert_presidents_or_advisors(presidents, table):
    for president in presidents:
        if "Advisor" in table:
            stmt = "INSERT INTO {} ( name, email, phone) \
                            VALUES ( \"{}\", \"{}\", \"{}\");".format( \
                table, president["Name"], president["Email"], president["Phone"])
        else:
            stmt = "INSERT INTO {} ( email, phone) \
                            VALUES ( \"{}\", \"{}\");".format( \
                table, president["Email"], president["Phone"])
        insert_into(stmt)


def insert_stat_clubs(clubs):
    for club in clubs:
        stmt = "INSERT INTO club (cname, department) VALUES (\"{}\", \"{}\")"
        stmt = stmt.format(club, "STAT")
        insert_into(stmt)
    pass


# insert_stat_clubs(links.keys())
# insert_presidents_or_advisors(presidents, "clubPresidentContact")
# insert_presidents_or_advisors(advisors, "clubAdvisorContact")


def _get_upcoming_events(info):
    return info.string, None


def _get_program(info):
    program = ''
    advanced = info.find_next_sibling()
    stat_form = []
    for content in info.contents:
        if isinstance(content, element.Tag):
            program += " visit " + content['href']
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


@debug
def extract_statistics_deparment_info(soup):
    main_content = soup.find('div', class_='field-items')
    stat_info = main_content.find_next('p')
    stat_club = {}
    stat_club['about'] = stat_info.text
    titles = {
        "Upcoming Events": _get_upcoming_events,
        "Stat Buddy Program": _get_program,
        "2018-2019 STAT Club Officers": _get_officers
    }

    for title in main_content.find_all('h2'):
        function = titles.get(title.string.strip())
        if "2017-2018" in title.string:
            stat_club["2017-2018 STAT Club Officers"], _ = _get_officers(title.find_next_sibling())
        if function:
            info, link = function(title.find_next_sibling())
            stat_club[title.string] = info
            if link:
                stat_club['signup_for_mentor'] = link[1]
                stat_club['signup_for_classes'] = link[0]
    advisors = main_content.find('h3').find_next()
    stat_club["Advisors"] = advisors.text
    return stat_club


r = requests.get(urls[3])
soup = BeautifulSoup(r.text, 'html.parser')


# extract_statistics_deparment_info(soup)

@debug
def extract_stat_tutoring(soup):
    stat_tutoring = {}
    main_content = soup.find_all('div', class_='field-item')
    for x in main_content:
        if x:
            info = []
            for x in soup.find('div', class_='field-item').find_all('div', class_='clear'):
                info.append(re.sub('\xa0', ' ', x.text))
            stat_tutoring[info[0]] = info[1]
            stat_tutoring[info[2]] = info[3].split('.')[0]
    tutors = soup.find('div', class_='field-item').find('a')['href']
    stat_tutoring['tutors'] = tutors
    tutor_hours = soup.find('div', class_='field-item').find('img')['src']
    stat_tutoring['tutor_hours'] = tutor_hours
    return stat_tutoring


def add_to_tutorExtraDump(stat_info, tid):
    for k, v in stat_info.items():
        stmt = "INSERT INTO tutorExtraDump (tid, keywords, data) VALUES \
                ( \"{}\", \"{}\", \"{}\")".format(tid, k, v)
        insert_into(stmt)


r = requests.get(urls[5])
soup = BeautifulSoup(r.text, 'html.parser')


# stat = extract_stat_tutoring(soup)

# add_to_tutorExtraDump(stat, 2)


def add_department():
    departments = ["CSSE", "STAT"]
    for i, d in enumerate(departments):
        stmt = "INSERT INTO department ( name ) VALUES ( \"{}\");"
        stmt = stmt.format(d)
        insert_into(stmt)


# add_department()
# add_to_tutorExtraDump(stat, 2)


def extract_tutoring_info(p):
    line = p.split('\n')
    keys = [None, 'Building and Room', 'Days', 'Time', 'Unavailable', None]
    tutoring_center_info = {}
    for idx, l in enumerate(line):
        l = l.strip()
        if l:
            tutoring_center_info[keys[idx]] = l.split('.')[0]
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
csc_tutor_info = extract_tutoring_center(soup)


# add_to_tutorExtraDump(csc_tutor_info, 1)

@debug
def extract_info_from_acm(soup):
    url = "https://cpe.calpoly.edu/clubs/association-computing-and-machinery"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.find('div', {'id': 'mainLeftFull'}).text.strip()
    acm = {}
    acm["About"] = text
    acm['Website'] = url
    acm['Contact'] = "N/A"
    acm['Department'] = "CSSE"
    return acm


r = requests.get(urls[9])
soup = BeautifulSoup(r.text, 'html.parser')
acm = extract_info_from_acm(soup)
club["ACM"] = acm


def insert_into_club_schedule(time_day):
    pass


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


def get_wish_schedule(soup):
    url = soup.find('iframe')['src']
    url = re.sub('&amp;', '&', url)
    r = requests.get(url)
    soup_calendar = BeautifulSoup(r.text, 'html.parser')
    url = soup_calendar.find('noscript').find('a')['href']
    url = re.sub('&amp;', '&', url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    days = [day.text for day in soup.find_all('th', class_='column-label')]
    time_day = get_schedules(soup, days)
    insert_into_club_schedule(time_day)


@debug
def extract_info_from_wish(soup):
    people = {}
    for x in soup.find_all('h3'):
        t = x.text.strip().split('\n')
        people[t[-1]] = t[0]
    advisors = soup.find_all('h2')[-1]
    advisors_email = []
    for advisor in advisors.parent.find_next_siblings():
        s = advisor.text.strip().split(' ')
        advisors_email.append((s[0] + " " + s[1], s[-1]))
    wish = {}
    wish['People'] = people
    wish['Adivsors'] = advisors_email
    wish['Location'] = "N/A"
    wish['Department'] = "CSSE"
    # wish['Schedule'] = get_wish_schedule(soup)
    return wish


r = requests.get(urls[10])
soup = BeautifulSoup(r.text, 'html.parser')
wish = extract_info_from_wish(soup)
print(wish)


def get_cplug_about(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    about = soup.find('div', class_='content').p.text
    return about


@debug
def extract_projects_from_cplug(soup):
    projects = dict()
    url = "http://cplug.org/"
    projects['CPLUG projects'] = []
    for x in soup.find_all('h1'):
        projects['CPLUG projects'].append(x.text.strip())
    projects['Contact'] = "cplug@calpoly.edu"
    projects['Location'] = "N/A"
    projects['Website'] = url
    projects['About'] = get_cplug_about(url)
    projects['Department'] = "CSSE"
    return projects


r = requests.get(urls[12])
soup = BeautifulSoup(r.text, 'html.parser')
cplug = extract_projects_from_cplug(soup)

club["CPLUG"] = cplug


def getGameDesignDescript():
    url = "http://www.cpgd.org/"
    myRequest = requests.get(url)
    soup = BeautifulSoup(myRequest.text, "html.parser")
    i = 0
    for Row in soup.find_all("div", {"class": "widget-content"}):
        if (i == 1):
            return Row.text
        i += 1


def getCPGDOfficers():
    url = "http://www.cpgd.org/"
    myRequest = requests.get(url)
    soup = BeautifulSoup(myRequest.text, "html.parser")
    officers_list = {}
    officers = soup.find('div', {'id': 'TextList1'}).ul.text
    for officer in officers.strip().split('\n'):
        officer = officer.strip().replace('(', '')
        officer = officer.replace(')', '')
        title = officer.split(' ')
        officers_list[title[-1]] = title[0] + " " + title[1]
    return officers


def extract_from_cpgd():
    cpgd = {}
    cpgd_desc = getGameDesignDescript()
    cpgd["About"] = cpgd_desc.split('.')[0]
    cpgd["Meeting"] = cpgd_desc.split('.')[-2]
    cpgd["Officers"] = re.sub('\s+', ' ', getCPGDOfficers())
    cpgd["Website"] = "http://www.cpgd.org/"
    cpgd['Contact'] = "officers @ cpgd.org"
    cpgd['Department'] = "CSSE"
    return cpgd


cpgd = extract_from_cpgd()
club["CPGD"] = cpgd


@debug
def extract_about_from_whitehat(soup):
    about = soup.find_all('div', class_='about-section')[-1]
    whitehat = dict()
    whitehat['About'] = about.text
    whitehat['Website'] = urls[13]
    email = soup.find('div', attrs={'id': 'footer-right'})
    whitehat['Contact'] = email.a['href'].split(':')[-1]
    whitehat['Department'] = "CSSE"
    return whitehat


r = requests.get(urls[13])
soup = BeautifulSoup(r.text, 'html.parser')
club_whitehat = extract_about_from_whitehat(soup)
club["White Hat"] = club_whitehat


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
    return officer_list


r = requests.get(urls[14])
soup = BeautifulSoup(r.text, 'html.parser')
whitehat = extract_officers_from_whitehat(soup)
club_whitehat.update(whitehat)




@debug
def extract_slo_hacks(soup):
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
    workshop['Location'] = "N/A"
    return workshop


r = requests.get(urls[15])
soup = BeautifulSoup(r.text, 'html.parser')


# extract_slo_hacks(soup)


def insert_into_tutors(tutors):
    for k, tutor in tutors.items():
        stmt = "INSERT INTO tutor ( department, name, cost) VALUES \
                    (\"{}\", \"{}\", {});".format("CSSE", tutor, 0.00)
        print(stmt)
        insert_into(stmt)


def insert_into_schedule(time_day_people, map_tutors):
    tutors = list(map(operator.itemgetter(2), time_day_people))
    for idx, tutor_group in enumerate(tutors):
        for i, tutor in enumerate(tutor_group.split(', ')):
            tid = list(map_tutors.keys())[list(map_tutors.values()).index(tutor)]
            stmt = "INSERT INTO tutorSchedule ( tid, dayOfTheWeek, time, location) \
                    VALUES ( \"{}\", \"{}\", \"{}\", \"{}\")"
            stmt = stmt.format(tid, time_day_people[idx][0], time_day_people[idx][1], "Building 14, Room 302")
            print(stmt)
            insert_into(stmt)


def getTutorNames():
    url = urls[7]
    myRequest = requests.get(url)
    soup = BeautifulSoup(myRequest.text, "html.parser")
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
    insert_into_tutors(map_tutors)
    insert_into_schedule(time_day_people, map_tutors)


# @debug
def extract_csc_tutoring_hours(soup):
    url = soup.find('iframe')['src']
    url = re.sub('&amp;', '&', url)
    r = requests.get(url)
    soup_calendar = BeautifulSoup(r.text, 'html.parser')
    url = soup_calendar.find('noscript').find('a')['href']
    url = re.sub('&amp;', '&', url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    days = [day.text for day in soup.find_all('th', class_='column-label')]
    time_day = get_schedules(soup, days)
    insert_into_tutorSchedule(time_day)


url = urls[8]
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')


# extract_csc_tutoring_hours(soup)


def get_csc_tutor_info(soup):
    div = soup.find('div', {'id': 'contentHeader'})
    text = re.sub('\s+', ' ', div.p.text)
    classes = re.findall('(\d+)', text)
    for class_ in classes:
        stmt = "INSERT INTO tutorClasses ( name ) VALUES \
                ( \"{}\")".format(class_)
        insert_into(stmt)
    tutoring_info = {}
    about = div.p.text.strip()
    about = re.sub('\s+', ' ', about)
    tutoring_info[div.h1.text] = about
    for h2 in soup.find_all('h2'):
        if h2.find_next_sibling():
            info = h2.find_next_sibling().text.strip()
            info = re.sub('\s+', ' ', info)
            tutoring_info[h2.text] = info
    add_to_tutorExtraDump(tutoring_info, 1)


url = urls[0]
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')


# get_csc_tutor_info(soup)


def getRoboticsDescript():
    url = "http://calpolyrobotics.com"
    myRequest = requests.get(url)
    i = 0
    soup = BeautifulSoup(myRequest.text, "html.parser")
    for Row in soup.find_all("p", {"style": "white-space:pre-wrap;"}):
        return Row.text


def getRoboticsOfficers():
    url = "http://calpolyrobotics.com/contact"
    myRequest = requests.get(url)
    i = 0
    soup = BeautifulSoup(myRequest.text, "html.parser")
    retDict = {}
    for Row in soup.find_all("p", {"class": "text-align-center"}):
        if (i == 0):
            pres = Row.text.split(' - ')
            retDict[pres[0]] = pres[1]
        if (i == 1):
            currDict = {}
            pos = Row.text.split(' - ')
            currDict[pos[0]] = pos[1]
            retDict.update(currDict)
            return retDict
        i += 1


def getRoboticsLocation():
    url = "http://calpolyrobotics.com/contact"
    myRequest = requests.get(url)
    i = 0
    soup = BeautifulSoup(myRequest.text, "html.parser")
    for Row in soup.find_all("div", {"class": "footer-inner"}):
        return Row.text


def getRoboticsInfoFull():
    fullDict = {}
    subDict = {}
    subDict["About"] = getRoboticsDescript()
    subDict["Location"] = getRoboticsLocation()
    subDict.update(getRoboticsOfficers())
    fullDict["Cal Poly Robotics Club"] = subDict
    subDict['Website'] = "calpolyrobotics.com"
    subDict['Contact'] = "calpolyroboticsclub@gmail.com"
    subDict['Department'] = "CSSE"
    return subDict


robotics_club = getRoboticsInfoFull()

club["Cal Poly Robotics Club"] = robotics_club


def insert_into_clubInfo(club, value):
    about = value['About']
    website = value['Website']
    department = value["Department"]
    email = value["Contact"]
    stmt = "INSERT INTO club (cname, clubDescription, website, department, generalEmail) \
            VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\");"
    stmt= stmt.format(club, about, website, department, email)
    insert_into(stmt)


for c, val in club.items():
    insert_into_clubInfo(c, val)
    print(c, val)
