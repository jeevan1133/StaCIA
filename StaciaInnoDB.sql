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
  data varchar(200) not null,
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
  name varchar(200) not null,
  email varchar(200),
  phone varchar(200),
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

create table if not exists tutorClasses(
  classid integer auto_increment,
  tid integer not null,
  name varchar(200) not null,
  primary key (classid),
  foreign key (tid)
    references tutor(tid)
    on delete cascade) engine=InnoDB;

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
  tid integer not null,
  keywords varchar(200),
  data varchar(200),
  primary key (extraid),
  foreign key (tid)
    references tutor(tid)
    on delete cascade) engine=InnoDB;
