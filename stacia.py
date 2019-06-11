import os
import functools
import time
import atexit
from CSC import *
from Statistics import *
from database import *
from machineLearn import *

DEBUG = False

def debug(debug=False):
    """Print the function signature and return value"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if debug:
                print(f"Calling {func.__name__.upper()}")
                value = func(*args, **kwargs)
                return value
            else:
               return func(*args, **kwargs)

        return wrapper

    return decorator


@debug(debug=DEBUG)
def insert_info_into_clubs(club, about, contact, website, depart):
    stmt = "INSERT INTO club ( cname, clubDescription, website, department, generalEmail) \
            VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\");"
    stmt = stmt.format(club, about, website, depart, contact)
    insert_into(stmt)
    return stmt


@debug(debug=DEBUG)
def insert_into_president(club, email, phone):
    stmt = "INSERT INTO clubPresidentContact (cname, email, phone) \
            VALUES (\"{}\", \"{}\", \"{}\");"
    stmt = stmt.format(club, email, phone)
    insert_into(stmt)
    return stmt


@debug(debug=DEBUG)
def insert_advisors(club, val):
    try:
        advisor = val['Officers']['Advisor']
    except KeyError:
        try:
            advisor = val['Advisors']
            if isinstance(advisor, str):
                advisors = '\t'.join(advisor.split('\n'))
                email = phone = None
                stmt = "INSERT INTO clubAdvisorContact (cname, advisorName, advisorEmail, advisorPhone) \
                            VALUES  (\"{}\", \"{}\", \"{}\", \"{}\");"
                stmt = stmt.format(club, advisor, email, phone)
                insert_into(stmt)
                return stmt
        except:
            return
    try:
        advisorName = advisor['Name']
    except KeyError:
        advisorName = None
    try:
        advisorEmail = advisor['Email']
    except KeyError:
        advisorEmail = None
    try:
        advisorPhone = advisor['Phone']
    except KeyError:
        advisorPhone = None

    def get_sql_stmt(club, adv, email, phone):
        stmt = "INSERT INTO clubAdvisorContact (cname, advisorName, advisorEmail, advisorPhone) \
                               VALUES  (\"{}\", \"{}\", \"{}\", \"{}\");"
        stmt = stmt.format(club, adv, email, phone)
        return stmt

    if isinstance(advisorName, list):
        advisorName = '\t'.join(advisorName)
        advisorEmail = '\t'.join(advisorEmail)
        stmt = get_sql_stmt(club, advisorName, advisorEmail, advisorPhone)
    else:
        stmt = get_sql_stmt(club, advisorName, advisorEmail, advisorPhone)
    insert_into(stmt)
    return stmt


def get_officers_from_val(club, val):
    try:
        officers = val['Officers']
    except:
        return
    stmts = []
    for title, officer in officers.items():
        term = None
        name = officer
        if isinstance(officer, dict):
            name = officers[title]['Name']
        stmt = "INSERT INTO clubOfficers (cname, title, name, term) \
                VALUES (\"{}\", \"{}\", \"{}\", \"{}\");"
        stmt = stmt.format(club, title, name, term)
        insert_into(stmt)
        stmts.append(stmt)
    return stmts


@debug(debug=DEBUG)
def insert_club_officers(club, val):
    terms = []
    for k, v in val.items():
        if "20" in k:
            terms.append(k)
    if terms:
        for term in terms:
            officers = val[term]
            for title, officer in officers.items():
                stmt = "INSERT INTO clubOfficers (cname, title, name, term) \
                VALUES (\"{}\", \"{}\", \"{}\", \"{}\");"
                stmt = stmt.format(club, title, officer, term)
                insert_into(stmt)
        return terms
    return get_officers_from_val(club, val)


def slo_hacks_schedule(club, schedules):
    stmts = []
    for day, events in schedules.items():
        for event, place in events.items():
            event_ = re.split(r'(\d+)', event, 1)
            time_ = ''.join(event_[-2:])
            event = ''.join(event_[:-2])
            stmt = "INSERT INTO clubSchedule (cname, dayOfTheWeek, time, event, location) \
                    VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\");"
            stmt = stmt.format(club, day, time_, event, place)
            insert_into(stmt)
            stmts.append(stmt)
    return stmts


@debug(debug=DEBUG)
def insert_into_club_schedule(club, val):
    try:
        schedules = val['Schedule']
    except KeyError:
        return
    if isinstance(schedules, dict):
        return slo_hacks_schedule(club, schedules)

    stmts = []
    for schedule in schedules:
        day, time, location = schedule.split(' ', 2)
        stmt = "INSERT INTO clubSchedule (cname, dayOfTheWeek, time, event) \
                VALUES (\"{}\", \"{}\", \"{}\", \"{}\");"
        stmt = stmt.format(club, day, time, location)
        insert_into(stmt)
        stmts.append(stmt)
    return stmts


@debug(debug=DEBUG)
def add_to_extra_dump(stat_clubs):
    stmts = []
    for club, extra in stat_clubs.items():
        try:
            for keyword, data in extra.items():
                stmt = "INSERT INTO clubExtraDump (cname, keywords, data) \
                    VALUES (\"{}\", \"{}\", \"{}\");"
                stmt = stmt.format(club, keyword, data)
                insert_into(stmt)
                stmts.append(stmt)
        except Exception:
            stmt = "INSERT INTO clubExtraDump (cname, keywords, data) \
                               VALUES (\"{}\", \"{}\", \"{}\");"
            stmt = stmt.format("STAT Club", club, extra)
            insert_into(stmt)
    return stmts


def insert_into_clubs():
    url = "https://statistics.calpoly.edu/content/statclub"
    stat_club_info = extract_statistics_department_info(url)
    url = "http://www.cosam.calpoly.edu/content/student_orgs"
    stat_clubs = statistics_deparment_info(url)
    csc_clubs = get_csc_clubs()
    if csc_clubs:
        stat_clubs.update(csc_clubs)
    else:
        pass
    terms = [name for name in stat_club_info.keys() if name.startswith("20")]
    for idx, term in enumerate(terms):
        stat_clubs["STAT Club"][term] = {}
        stat_clubs["STAT Club"][term].update(stat_club_info[term])
    stat_advisor_contact = {"Advisors": stat_club_info['Advisors']}
    del stat_club_info['Advisors']
    stat_clubs['STAT Club'].update(stat_club_info)
    for club, val in stat_clubs.items():
        about = val['About']
        contact = val['Contact']
        website = val['Website']
        depart = val['Department']
        _ = stat_clubs[club].pop('About', None)
        _ = stat_clubs[club].pop('Contact', None)
        _ = stat_clubs[club].pop('Website', None)
        _ = stat_clubs[club].pop('Department', None)
        insert_info_into_clubs(club, about, contact, website, depart)
        try:
            email = val['Officers']['President']['Email']
            phone = val['Officers']['President']['Phone']
            insert_into_president(club, email, phone)
        except Exception:
            pass
        insert_advisors(club, val)
        stat_clubs[club].pop('Advisors', None)
        terms = insert_club_officers(club, val)
        if terms:
           for term in terms:
               stat_clubs[club].pop(term, None)
        stat_clubs[club].pop('Officers', None)
        insert_into_club_schedule(club, val)
        stat_clubs[club].pop('Schedule', None)

    stat_club_info.pop("Advisors", None)
    add_to_extra_dump(stat_advisor_contact)
    return add_to_extra_dump(stat_clubs)


def add_to_tutor_extra_dump(stat_tutoring, cname="STAT"):
    stmts = []
    for k, v in stat_tutoring.items():
        stmt = "INSERT INTO tutorExtraDump (department, keywords, data) \
                        VALUES (\"{}\", \"{}\", \"{}\");"
        stmt = stmt.format(cname, k, v)
        stmts.append(stmt)
        insert_into(stmt)
    return stmts


def extract_tutoring_info(p):
    line = p.split('\n')
    keys = [None, 'Building and Room', 'Days', 'Time', 'Unavailable', None]
    tutoring_center_info = {}
    for idx, l in enumerate(line):
        l = l.strip()
        if l:
            tutoring_center_info[keys[idx]] = l.split('.')[0]
    return tutoring_center_info


@debug(debug=DEBUG)
def extract_tutoring_center(url):
    soup = get_soup(url)
    tutoring_center = dict()
    div = soup.find('div', {'id': 'contentHeader'})
    center = extract_tutoring_info(div.find('p').text)
    tutoring_center.update(center)
    return center


@debug(debug=DEBUG)
def add_tutors(tutors):
    stmts = []
    for k, tutor in tutors.items():
        stmt = "INSERT INTO tutor (tid, department, name, cost) \
                VALUES (\"{}\", \"{}\", \"{}\", \"{}\")"
        stmt = stmt.format(k, "CSSE", tutor, 0.0)
        insert_into(stmt)
        stmts.append(stmt)
    return stmts


@debug(debug=DEBUG)
def insert_into_tutorSchedule(time_day_people, map_tutors):
    tutors = list(map(operator.itemgetter(2), time_day_people))
    stmts = []
    for idx, tutor_group in enumerate(tutors):
        for i, tutor in enumerate(tutor_group.split(', ')):
            tid = list(map_tutors.keys())[list(map_tutors.values()).index(tutor)]
            stmt = "INSERT INTO tutorSchedule ( tid, dayOfTheWeek, time, location) \
                    VALUES ( \"{}\", \"{}\", \"{}\", \"{}\")"
            stmt = stmt.format(tid, time_day_people[idx][0], time_day_people[idx][1], "Building 14, Room 302")
            stmts.append(stmt)
            insert_into(stmt)
    return stmts


@debug(debug=DEBUG)
def add_tutors_and_schedules():
    tutors, time_day = tutoring_csc()
    add_tutors(tutors)
    return insert_into_tutorSchedule(time_day, tutors)


@debug(debug=DEBUG)
def add_to_tutorClasses(classes):
    stmts = []
    for class_ in classes:
        stmt = "INSERT INTO tutorClasses ( name ) VALUES \
                    ( \"{}\")".format(class_)
        insert_into(stmt)
        stmts.append(stmt)
    return stmts


def insert_into_questions_table(file_name):
    f = open(file_name, 'r', encoding='utf-8')
    variables = []
    for idx, line in enumerate(f):
        questions = line.split('|')
        qstn = questions[1].strip()
        answer = questions[2].strip()
        stmt = questions[3].strip()
        sql_stmt = 'INSERT INTO questions (questions, answers, statement) \
                    VALUES ( "{}", "{}", "{}")'
        sql = sql_stmt.format(qstn, answer, stmt)
        variables.append(re.findall(r'\[(.*?)\]', questions[1]))
        insert_into(sql, line_num=idx+1)
    f.close()
    return


def get_tuples_format(ans, res):
    result = list(res.values())
    placeholders = re.findall(r'\{(.*?)\}', ans)
    return {i: j for i, j in zip(placeholders, result)}


def get_answer_from_query(query, args, orig_args=None):
    result = None
    record = get_sql_statement_from_query(query)
    if not record:
        print("I can't understand the question")
        return
    sql_stmt = record['statement']
    answer_format = record['answers']
    answers = answer_format.split('\t')
    try:
       for idx, stmt in enumerate(sql_stmt.split('\t')):
           stmt = stmt.format(**args)
           print(stmt)
           result = check_if_answer_exists(stmt)
           if result:
              return answers[idx].format(**get_tuples_format(answers[0], result[0]))
       if not result:
           return answers[-1]
    except Exception:
       return "Can't find in the database"

def get_club_names():
    sql = "SELECT `cname`, `department` from club;"
    result = check_if_answer_exists(sql)
    club_names = {}
    for record in result:
        club_names[record['cname']] = record['department']

    return club_names


def get_variable_mapping(variables_to_substitute_for, varibales_dict, query):
    present = False
    args = {k: None for k in variables_to_substitute_for}
    for variable in variables_to_substitute_for:
        present = False
        if variable.capitalize() == "Professor" or variable.capitalize() == "CSSE":
            present = True
        for term in varibales_dict.get(variable):
            found = re.search(term, query, re.IGNORECASE)
            if found:
                present = True
                args[variable] = term
                break
    return present, args


def mapped_dict():
    list_of_classes = [v for x in check_if_answer_exists("SELECT `name` FROM tutorClasses") for k,v in x.items()]
    club_officers = list(set([v for x in check_if_answer_exists("SELECT `title` FROM clubOfficers") for k,v in x.items()]))
    tutors =[v for x in check_if_answer_exists("SELECT `name` FROM tutor") for k,v in x.items()]
    days = list(set([v for x in check_if_answer_exists("SELECT `dayOfTheWeek` FROM tutorSchedule") for k,v in x.items()]))
    club_names = get_club_names()
    list_of_clubs = list(club_names.keys())
    list_of_clubs.extend(["ACM", "CPGD", "CPLUG", "WISH", "CPAD", "CPRC", "CPADC"])

    variables = {'CSCClassName': list_of_classes,
                 'CSSE': ["CSSE"],
                 'CSSESTAT': ["CSSE","STAT"],
                 'CSSESTATClassName': ["CSSE", "STAT"],
                 'CSSESTATClub': list_of_clubs,
                 'Day': days,
                 'Linux':["Linux","Windows","Unix"],
                 'OfficerRole': club_officers,
                 'Professor': [],
                 'STATCLASSName': ["STAT"],
                 'StatYear': ['2017', '2018'],
                 'Tutorname': tutors,
                 'programming language': ['Java', 'C', 'Python']
               }
    return variables


def main():
    #atexit.register(_close_connection())
    test = True
    if test:
       d, u, p = read_info('/home/jbasnet466/Project3/credentials.txt')
       os.system("mysql --user={} --password={} {} < makeTables.sql".format(u,p,d))
       print("Trashed table")
       insert_into_clubs()
       url = "https://statistics.calpoly.edu/content/tutoring"
       stat_tutoring = extract_stat_tutoring(url)
       add_to_tutor_extra_dump(stat_tutoring)

       url = "http://tutoring.csc.calpoly.edu/schedule/"
       add_to_tutor_extra_dump(extract_tutoring_center(url), cname="CSSE")
       add_tutors_and_schedules()

       url = "http://tutoring.csc.calpoly.edu/"
       classes, extra_dump = get_csc_tutor_info(url)
       add_to_tutorClasses(classes)
       add_to_tutor_extra_dump(extra_dump, "CSSE")
      
       question_answer = "/home/jbasnet466/Project3/Questions.txt"
       insert_into_questions_table(question_answer)

    variables = mapped_dict()
    clf = classTrain(variables)
    while True:
       query = input("Please input string: ")
       if query == "quit":
          break
       question = clf.classify(run(query))
       print(question)
       variables_to_substitute_for = re.findall(r'\[(.*?)\]', question)
       cond, args = get_variable_mapping(variables_to_substitute_for, variables, query)
       print(args)
       print(get_answer_from_query(question, args))


if __name__ == "__main__":
    main()
    
