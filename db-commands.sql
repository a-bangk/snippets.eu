show tables;

describe note;
describe user;

CREATE TABLE user (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(320) UNIQUE,
    password_hash VARCHAR(255),
    is_active TINYINT(1) DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME,
    PRIMARY KEY (id)
);

select * from users;
ALTER TABLE user MODIFY COLUMN id int unsigned;
drop table user;
describe user;

alter table note add column user_id int;

select * from author;
v
v
select * from author;
select * from author;

select * from source_type st ;

select st.entry as type,s.id,s.title as title, GROUP_CONCAT(concat(IFNULL(a.title,"")," ",IFNULL(a.forename,""),IFNULL(a.middlename,"")," ",IFNULL(a.surname,""), " ",IFNULL(a.postnominal,"")) SEPARATOR " & ") as author,a.id as a_id, s.url as url from source s left join associate_source_author aa on s.id = aa.source_id left join author a on aa.author_id = a.id left join source_type st on s.source_type_id = st.id group by s.id order by s.id desc;

select * from source s ;

SELECT 
COL.COLUMN_NAME, 
COL.DATA_TYPE, 
COL.CHARACTER_MAXIMUM_LENGTH, 
COL.IS_NULLABLE 
FROM INFORMATION_SCHEMA.COLUMNS COL 
WHERE COL.TABLE_NAME = 'source';

describe author ;

ALTER TABLE source MODIFY year varchar(64);
select * from source;

ALTER TABLE author drop birthyear; 

ALTER TABLE author
ADD full_name varchar(512); 

alter table author 
add update_datetime datetime;


describe author;

describe note;

select * from author;
select * from note order by id desc;
UPDATE author SET full_name =concat(forename,' ',surname) where id in (1,2,3,29,30,54,55,56);
insert into author(full_name,birthyear, deathyear, comment) VALUES ("Adam Kjems",1988,Null,"It is me");

select a.full_name as author,a.id as a_id, s.url as url from source s 
	left join associate_source_author aa on s.id = aa.source_id 
	left join author a on aa.author_id = a.id 
	where s.id=92;

update author set middlename=concat('',middlename); 
select full_name as author from author;
delete from source where id=55;

select * from associate_source_author asa ;

INSERT INTO author(full_name) values ("test");

ALTER DATABASE [personal_snippetsdb]
SET offline WITH ROLLBACK IMMEDIATE 
GO
ALTER DATABASE [personal_snippetsdb] SET online;
show process list;


alter table author add comment varchar(1024);

KILL SOFT 1239;
show processlist;


SELECT id,full_name as fullname, IFNULL(birthyear,"") as birthyear,IFNULL(deathyear,"") as deathyear, comment from author order by id desc;
insert into source(title,entry_datetime,source_type_id,url,year) VALUES ("asdf", now(),"1", "",NULL);

select * from note;

select * from notetag n ;
delete from notetag where id=163;
select * from associate_notetag_note ann where notetag_id = 155;
delete from author where id>80;
select * from note n ;

select * from source s ;

update source set title ="Essential Ideas for Parents" where id=13 ;
update note set content = "Cheese",update_datetime=now() where id = 390;
select * from note where id = 390;


update note set update_datetime=now() where id = id;

select * from note;

SELECT * from associate_source_note;

describe author;
update author set full_name = "Bobby",birthyear = "1987" where id = 86;

select * from author order by id desc;

select content from note;

with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR ", ") as tags from associate_notetag_note ann join notetag nt on nt.id = ann.notetag_id group by ann.note_id ), s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources, s.url from associate_source_note asn join source s on s.id = asn.source_id group by asn.note_id ) select n.id,n.content, n.entry_datetime,nt.tags,s.sources,s.url from note n left join nt on nt.note_id = n.id left join s on s.note_id = n.id where n.id=173;

with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR ", ") as tags 
	from associate_notetag_note ann
	join notetag nt on nt.id = ann.notetag_id group by ann.note_id ),
b as ( select asn.note_id, GROUP_CONCAT(b.title SEPARATOR ", ") as sources ,b.url
	from associate_source_note asn  
	join source b on b.id = asn.source_id  group by asn.note_id ) 
select n.id,n.content, n.entry_datetime,nt.tags,b.sources, b.url
	from note n left join nt on nt.note_id = n.id 
	left join b on b.note_id = n.id
order by n.id desc;

SELECT * from source;

s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources 
	from associate_source_note asn  
	join source s on s.id = asn.source_id  group by asn.note_id ) ;

select * from 	associate_source_note where note_id=380;
select * from associate_notetag_note ann where note_id=380;
select exists(select * from associate_source_author where source_id=401 and author_id=92);

SELECT * FROM author;

select a.full_name as author,a.id as a_id, s.url as url from source s left join associate_source_author aa on s.id = aa.source_id left join author a on aa.author_id = a.id where s.id=94;


select * from author;
select * from source;
select * from associate_source_author asa where source_id = 94;
describe author;

describe associate_source_author;
select * from associate_source_author asa ;
select * from author where id in (74,75,76);
select * from author where id = 74;

select a.fullname, s.title

with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR ", ") as tags from associate_notetag_note ann 
join notetag nt on nt.id = ann.notetag_id group by ann.note_id ), 
s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources, 
s.url from associate_source_note asn 
join source s on s.id = asn.source_id group by asn.note_id ) 
select n.id,n.content, n.entry_datetime,nt.tags,s.sources,s.url from note n 
left join nt on nt.note_id = n.id 
left join s on s.note_id = n.id where n.id=401;

select * from author a;
select a.full_name from author a;
select id from author where full_name='Finn Kjems';
select id from author where full_name="Carl Marx";

insert into author(full_name,birthyear, deathyear, comment) VALUES ("Adam Kjems",1988,Null,"It is me");


IF NOT EXISTS(SELECT id FROM author WHERE full_name='Finn Kjems');
INSERT INTO author(full_name) VALUES ("Finn Kjems") where not EXISTS (select * from author where full_name ="Finn Kjems");


INSERT INTO author (full_name)
SELECT * FROM (SELECT 'Bobby' AS full_name) AS tmp
WHERE NOT EXISTS (
    SELECT full_name FROM author WHERE full_name = 'Bobby'
) LIMIT 1
select scope_identity();

select * from note where id =417;
delete from note where id=417;

INSERT IGNORE INTO associate_notetag_note(note_id,notetag_id) VALUES(426,126);
select * from associate_notetag_note ann  where note_id=426;

select * from notetag n where id = 223;

select * from notetag where tag like " %";


select concat('KILL SOFT ',id,';') from information_schema.processlist;
KILL 4470;

KILL SOFT 4473;
KILL SOFT 4472;
KILL SOFT 4467;
KILL SOFT 4460;
KILL SOFT 4436;
KILL SOFT 4434;

show processlist;
kill soft 9276;
kill soft 9277;
kill soft 9278;
kill soft 9296;
kill soft 9297;
describe notetag;
select * from associate_source_author asa ;
delete from author where id=114;
delete from associate_source_author where author_id = 114;

INSERT IGNORE INTO associate_source_author(source_id,author_id)  VALUES(500,74);
delete from associate_source_author where source_id =500;

select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR "; ") as tags from associate_notetag_note ann  join notetag nt on nt.id = ann.notetag_id  group by ann.note_id;
select asa.source_id, GROUP_CONCAT(a.full_name separator ", ") as authors from associate_source_author asa join author a on a.id=asa.author_id group by asa.source_id;




select * from associate_source_author asa ;
delete from associate_source_author where source_id>300;

select * from associate_notetag_note ann ;

select * from source where id=128 or id=131;

select st.entry as type,s.id,s.title as title,s.year  as year, GROUP_CONCAT(a.full_name SEPARATOR " & ") as author, s.url as url from source s left join associate_source_author aa on s.id = aa.source_id left join author a on aa.author_id = a.id left join source_type st on s.source_type_id = st.id where s.id=94;

select st.entry as type,s.id,s.title as title, GROUP_CONCAT(a.full_name SEPARATOR " & ") as author,a.id as a_id, s.url as url from source s left join associate_source_author aa on s.id = aa.source_id left join author a on aa.author_id = a.id left join source_type st on s.source_type_id = st.id group by s.id order by s.id desc;

select * from notetag n ;
select * from associate_notetag_note ann where notetag_id =221;

select * from notetag where id in(
SELECT n.id
FROM notetag n
left JOIN associate_notetag_note ann 
ON n.id = ann.notetag_id
where ann.note_id is Null
);

select * from associate_notetag_note ann;

select * from notetag where tag like '%es%';

select * from notetag n group by tag  ;

update associate_notetag_note set notetag_id=243;
delete from associate_notetag_note where notetag_id =243;
delete from notetag where id=243;

select * from author;
delete from author where id = 124;

select * from associate_source_author asa where author_id = 124;

UPDATE notetag SET  tag=replace(tag, ' ', '');


select * from notetag;
select * from associate_notetag_note ann where notetag_id = 216;
update associate_notetag_note set notetag_id = 193 where notetag_id =216;
delete from notetag where id=216;


with nt as ( 
	select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR "; ") as tags 
	from associate_notetag_note ann  
	join notetag nt on nt.id = ann.notetag_id  
	group by ann.note_id 
	), 
s as ( 
	select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources,s.url  
	from associate_source_note asn  
	join source s on s.id = asn.source_id  
	group by asn.note_id 
	)
select n.id,n.content, n.entry_datetime, n.update_datetime ,nt.tags,s.sources,s.url
from note n 
left join nt on nt.note_id = n.id 
left join s on s.note_id = n.id 
order by n.update_datetime desc, n.entry_datetime desc;

 ORDER BY COALESCE(n.update_datetime, n.entry_datetime);

ORDER BY CASE 
    WHEN n.update_datetime IS NOT NULL THEN n.update_datetime
    ELSE n.entry_datetime;

select * from notetag n
left join associate_notetag_note ann 
on ann.notetag_id = n.id 
where tag like '%time%' ;
 

update associate_notetag_note set notetag_id =28 where notetag_id =255;

UPDATE note
SET update_datetime = entry_datetime
WHERE update_datetime IS NULL;


select * from note order by id DESC;
delete from notetag where id=255;

select * from author order by id desc;

INSERT INTO note(content,entry_datetime,update_datetime) VALUES (?, now(), now());

insert into source(title,entry_datetime,source_type_id,url,year) VALUES ("hellow", now(),1, NULL, NULL);

select * from source order by id DESC ;

describe source;
ALTER TABLE source
ADD published varchar(64);
update source set published=year;

select id from source s where title ="kajfæakjfæ" and url="dkajfædj";


update source set title = "cheese",update_datetime=now(),url="nothign.html", source_type_id=2, year="3000" where id = 171;

show process list;


UPDATE notetag SET update_datetime  = entry_datetime WHERE update_datetime is NULL;

UPDATE source SET entry_datetime=now() WHERE id=1 or 13;

update author set update_datetime=entry_datetime where update_datetime is NULL;

select * from address a ;

drop table address;

select * from note  ;
alter table note 
drop column url_source;

select * from notetag n ;
delete from notetag where id=268 or id=305 or id=306 or id=308;
delete from associate_notetag_note where notetag_id =268;

select * from author;
select * from associate_notetag_note ann ;
select * from associate_source_author asa ;
select * from associate_source_note asn order by note_id desc ;

select * from note where id=566;
select * from source order by id desc;

with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR ", ") as tags from associate_notetag_note ann join notetag nt on nt.id = ann.notetag_id group by ann.note_id ), s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources, s.url from associate_source_note asn join source s on s.id = asn.source_id group by asn.note_id ) select n.id,n.content, n.entry_datetime,nt.tags,s.sources,s.url from note n left join nt on nt.note_id = n.id left join s on s.note_id = n.id where n.id=566;

CREATE TABLE users
( id      int       NOT NULL AUTO_INCREMENT,
username    varchar(50)  NOT NULL ,
password char(82)  NULL ,
cust_email   varchar(255) NULL ,
category varchar(20) NULL,
PRIMARY KEY (id)
) ;

select * from notetag;

describe
-- ------- Complete used SQL ------------------

-- Delete all unused Tags
DELETE FROM notetag WHERE id IN(
	SELECT n.id
	FROM notetag n
	LEFT JOIN associate_notetag_note ann 
	ON n.id = ann.notetag_id
	WHERE ann.note_id IS NULL
);


-- Author table link with source table
with a as(select asa.source_id, GROUP_CONCAT(a.full_name separator ", ") as authors from associate_source_author asa join author a on a.id=asa.author_id group by asa.source_id)
select a.authors, s.title, s.id as source_id from source s
left join a on a.source_id =s.id;


-- Author with note_id, source title
with atable as (
	with a as(select asa.source_id, GROUP_CONCAT(a.full_name separator ", ") as authors from associate_source_author asa join author a on a.id=asa.author_id group by asa.source_id)
	select a.authors, s.title as title, s.id as source_id from source s
	left join a on a.source_id =s.id
	)
select atable.authors from associate_source_note asn 
left join atable on atable.source_id=asn.source_id
-- ;
where asn.note_id=548;

-- Author with note content, use two association tables in a row. Author-to-source, source-to-note
with asnatable as (
	with atable as (
		with a as(select asa.source_id, GROUP_CONCAT(a.full_name separator ", ") as authors from associate_source_author asa join author a on a.id=asa.author_id group by asa.source_id)
		select a.authors, s.id as source_id from source s
		left join a on a.source_id =s.id
		)
	select atable.authors, asn.note_id as asnnote_id from associate_source_note asn 
	left join atable on atable.source_id=asn.source_id
)
select asnatable.authors, n.content from note n
left join asnatable on asnatable.asnnote_id=n.id;

-- Note with source-to-note, and tag-to-note association tables
with nt as ( 
	select ann.note_id, GROUP_CONCAT(nt.tag order by tag asc SEPARATOR "; ") as tags 
	from associate_notetag_note ann  
	join notetag nt on nt.id = ann.notetag_id  
	group by ann.note_id
	), 
s as ( 
	select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources,s.url  
	from associate_source_note asn  
	join source s on s.id = asn.source_id  
	group by asn.note_id 
	)
select n.id,n.content, n.entry_datetime, n.update_datetime ,nt.tags,s.sources,s.url
from note n 
left join nt on nt.note_id = n.id 
left join s on s.note_id = n.id 
order by n.update_datetime desc;

