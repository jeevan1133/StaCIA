create table if not exists club(
  cid integer auto_increment,
  cname varchar(200),
  department varchar(200),
  primary key (cid)) engine=InnoDB;

create table if not exists positions(
  pid integer auto_increment,
  title varchar(200) not null,
  primary key (pid)) engine=innodb;

create table if not exists clubSchedule(
  schid integer auto_increment,
  cid integer not null,
  dayOfTheWeek varchar(200),
  time varchar(200),
  location varchar(200),
  primary key (schid),
  foreign key (cid)
    references club(cid)
    on delete cascade) engine=InnoDB;

create table if not exists clubOfficers(
  cofid integer auto_increment,
  cid integer not null,
  pid integer not null,
  name varchar(200) not null,
  term varchar(200) not null,
  primary key (cofid),
  foreign key (cid)
    references club(cid)
    on delete cascade,
  foreign key (pid)
    references positions(pid)
    on delete cascade) engine=InnoDB;

create table if not exists clubExtraDump(
  extraid integer auto_increment,
  cid integer not null,
  keywords varchar(200) not null,
  data varchar(200) not null,
  primary key (extraid),
  foreign key (cid)
    references club(cid)
    on delete cascade) engine=InnoDB;

create table if not exists clubInfo(
  cid integer,
  clubDescription varchar(3000),
  website varchar(3000),
  generalEmail varchar(200),
  generalPhone varchar(200),
  primary key (cid),
  foreign key (cid)
    references club(cid)
    on delete cascade) engine=InnoDB;

create table if not exists clubPresidentContact(
  cid integer,
  email varchar(200),
  phone varchar(200),
  primary key (cid),
  foreign key (cid)
    references club(cid)
    on delete cascade) engine=InnoDB;

create table if not exists clubAdvisorContact(
  cid integer,
  name varchar(200) not null,
  email varchar(200),
  phone varchar(200),
  primary key (cid),
  foreign key (cid)
    references club(cid)
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
