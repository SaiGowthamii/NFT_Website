#drop database test;
#create database test;
use test;

create table user(
	uid int auto_increment primary key,
	username varchar(50) unique,
    password varchar(255),
    user_type int default 0
);


create table trader(
	t_id int primary key,
    eth_addr varchar(50) not null unique,
    trader_level varchar(12),
	fname varchar(50),
	lname varchar(50),
    email_id varchar(50) not null unique,
    cell_no varchar(15),
    phone_no varchar(15),
    street_addr varchar(100),
    city varchar(50),
    state varchar(50),
    zip_code int,
    wallet_balance float,
    foreign key(t_id) references user(uid)
	);

#drop table nft;
create table nft(
		nft_name varchar(50),
        token_id varchar(100),
        contract_addr varchar(100),
        owner_id int,
        current_price float,
        primary key(token_id,contract_addr),
        foreign key(owner_id) references trader(t_id)
);

create table transaction(
		trans_id int auto_increment primary key,
        trans_time datetime default current_timestamp,
        trans_type varchar(15)
);

#drop table nft_transaction;

create table nft_transaction(
		trans_id int primary key,
        initiator_id int not null,
        receiver_id int not null,
        contract_addr varchar(50),
        token_id varchar(100),
        total_amount float,
        commission_in_eth float,
        commission_in_usd float,
        commission_type varchar(10),
        nft_trans_type varchar(10),
        trans_status varchar(15),
        foreign key(trans_id) references transaction(trans_id),
        foreign key(initiator_id) references trader(t_id),
        foreign key(token_id,contract_addr) references nft(token_id,contract_addr)
);

create table wallet_transaction(
	trans_id int primary key,
        initiator_id int not null,
        wallet_trans_type varchar(10),
        amount_in_usd float,
        amount_in_eth float,
        payment_addr varchar(50),
        foreign key(trans_id) references transaction(trans_id),
        foreign key(initiator_id) references trader(t_id)
);

create table cancelledLogs(
	log_id int auto_increment primary key,
        trans_id int not null,
        log_info varchar(100),
        log_trans_time datetime default current_timestamp,
        foreign key(trans_id) references nft_transaction(trans_id)
);

create table manager(
	t_id int primary key,
    fname varchar(50),
	lname varchar(50),
    manager_level int default 1
);


insert into user(username,password,user_type) values ('s',"abc",0),('r',"abc",0),('g',"abc",0),('a',"abc",0);

insert into trader(t_id,eth_addr,trader_level,fname,lname,email_id,cell_no, phone_no,street_addr,city,state,zip_code,wallet_balance) values
					(1,'0xb65913648136498291','silver','Suhaas','Kalisetty','s@gnmail.com','9999999999','9999999999','EOR','Richardson','Texas','75080',99.89),
                    (2,'0xb24756384738465386','silver','Roshan','Rayudu','r@gnmail.com','9999999999','9999999999','EOR','Richardson','Texas','75080',67.73),
                    (3,'0xb72485642654985628','gold','Gowthami','Pavani','g@gnmail.com','9999999999','9999999999','Northside','Austin','Texas','75085',82.92),
                    (4,'0xb48527658483748593','gold','Abhi','A','a@gnmail.com','9999999999','9999999999','Axis','Manhattan','Newyork State','75090',71.45);
                    

insert into nft(nft_name,token_id,contract_addr,owner_id,current_price) values ('CryptoPunks #1','2437486768674343252466','0xb02846592465482545',1,62.35),
						('CryptoPunks #2','4867238447837246645988','0xb974975645485426385',2,47.90),
                        ('CryptoPunks #3','8624576247354854754735','0xb852679862586958565',3,87.28),
                        ('CryptoPunks #4','6374562347563745463756','0xb324758639574824994',3,56.29),
                        ('CryptoPunks #5','7645725463756437564542','0xb746325842395777445',2,29.74),
                        ('CryptoPunks #6','1034843257636857593255','0xb824356948273567745',4,91.35),
                        ('CryptoPunks #7','5347215338954236858743','0xb018264985155757997',3,51.35),
                        ('CryptoPunks #8','6974658254972452190004','0xb832745427549854790',4,49.13),
                        ('CryptoPunks #9','4762459864759245725943','0xb943205792458945834',1,78.84),
                        ('CryptoPunks #10','6312453654124589125921','0xb742836596862537672',2,69.63);
