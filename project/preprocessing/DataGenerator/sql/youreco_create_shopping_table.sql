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
        imagefile varchar(150),
        link varchar(250),
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

create table inferenceinfo
    (
        id SERIAL primary key,
        url varchar(100),
        start_time int,
        end_time int,
        category int,
        sim_itemlist int[],
        video_subject int
    );