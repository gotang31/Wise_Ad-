create table userinfo
    (
        userid int,
        username varchar(10),
        age smallint,
        gender varchar(10),
        address varchar(40),
        primary key (userid)
    );

create table iteminfo
    (
        itemid SERIAL,
        itemname varchar(120),
        category int,
        price int,
        rating numeric(2,1),
        reviews int,
        youreco_reviews int,
        imagefile varchar(30),
        primary key (itemid)
    );

create table transactioninfo
    (
        id SERIAL primary key,
        userid int,
        itemid int,
        rating smallint,
        foreign key (userid) references userinfo (userid),
        foreign key (itemid) references iteminfo (itemid)
    );