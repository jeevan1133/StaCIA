drop table clubOfficers;
drop table clubExtraDump;
drop table clubPresidentContact;
drop table clubAdvisorContact;
drop table clubSchedule;
drop table club;
drop table tutorSchedule;
drop table tutorExtraDump;
drop table department;
drop table tutor;
drop table tutorClasses;
drop table questions;

create table if not exists club(
  cname varchar(200),
  clubDescription varchar(3000),
  website varchar(3000),
  department varchar(200),
  generalPhone varchar(200),
  generalEmail varchar(200),
  primary key (cname)) engine=InnoDB;

create table if not exists clubSchedule(
  schid integer auto_increment,
  cname varchar(200) not null,
  dayOfTheWeek varchar(200),
  time varchar(200),
  event varchar(200),
  location varchar(200),
  primary key (schid),
  foreign key (cname)
    references club(cname)
    on delete cascade) engine=InnoDB;

create table if not exists clubOfficers(
  cofid integer auto_increment,
  cname varchar(200) not null,
  title varchar(200) not null,
  name varchar(200) not null,
  term varchar(200) not null,
  primary key (cofid),
  foreign key (cname)
    references club(cname)
    on delete cascade) engine=InnoDB;

create table if not exists clubExtraDump(
  extraid integer auto_increment,
  cname varchar(200) not null,
  keywords varchar(200) not null,
  data varchar(5000) not null,
  primary key (extraid),
  foreign key (cname)
    references club(cname)
    on delete cascade) engine=InnoDB;

create table if not exists clubPresidentContact(
  cname varchar(200),
  email varchar(200),
  phone varchar(200),
  primary key (cname),
  foreign key (cname)
    references club(cname)
    on delete cascade) engine=InnoDB;

create table if not exists clubAdvisorContact(
  cname varchar(200),
  advisorName varchar(200) not null,
  advisorEmail varchar(200),
  advisorPhone varchar(200),
  primary key (cname),
  foreign key (cname)
    references club(cname)
    on delete cascade) engine=InnoDB;

create table if not exists tutor(
  tid integer auto_increment,
  department varchar(200),
  name varchar(200),
  email varchar(200),
  cost float not null,
  primary key (tid)) engine=InnoDB;

create table if not exists department(
  tid integer auto_increment,
  name varchar(200) not null,
  primary key (tid)) engine=InnoDB;

create table if not exists tutorSchedule(
  schid integer auto_increment,
  tid integer not null,
  dayOfTheWeek varchar(200),
  time varchar(200),
  location varchar(200),
  primary key (schid),
  foreign key (tid)
    references tutor(tid)
    on delete cascade) engine=InnoDB;

create table if not exists tutorExtraDump(
  extraid integer auto_increment,
  department varchar(200),
  keywords varchar(200),
  data varchar(5000),
  primary key (extraid)) engine=InnoDB;


create table if not exists tutorClasses(
  classid integer auto_increment,
  name varchar(200),
  department varchar(200) default "CSSE",
  primary key (classid)) engine=InnoDB;

create table if not exists questions (
  questions varchar(2000),
  answers varchar(5000),
  statement varchar(5000)) engine=InnoDB;
