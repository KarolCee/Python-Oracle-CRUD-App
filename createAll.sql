

-- sekwencja uzywana do id kierowcow
DROP SEQUENCE SEQ_ID;
CREATE SEQUENCE SEQ_ID START WITH 10 INCREMENT BY 10;

--tworzenie tabelek
DROP TABLE ULGI cascade constraints;
DROP TABLE BILETY cascade constraints;
DROP TABLE PRZEJAZDY cascade constraints;
DROP TABLE POJAZDY cascade constraints;
DROP TABLE MODELE cascade constraints;
DROP TABLE PRODUCENCI cascade constraints;
DROP TABLE KIEROWCY cascade constraints;
DROP TABLE PUNKTY_TRASY cascade constraints;
DROP TABLE PRZYSTANKI cascade constraints;
DROP TABLE DZIELNICE cascade constraints;
DROP TABLE LINIE cascade constraints;

CREATE TABLE PRODUCENCI
      ( NAZWA VARCHAR2(50) CONSTRAINT PK_PRODUCENCI PRIMARY KEY NOT NULL,
	ROK_ROZPOCZECIA DATE NOT NULL,
	KRAJ_POCHODZENIA VARCHAR2(15) NOT NULL);
    
CREATE TABLE MODELE
      ( NAZWA_MODELU VARCHAR2(50) NOT NULL,
      PRODUCENT VARCHAR2(50) CONSTRAINT FK_MODELE REFERENCES PRODUCENCI(NAZWA) NOT NULL,
	lICZBA_KONII NUMBER(4) NOT NULL,
	KOSZT_ZL number NOT NULL,
    CONSTRAINT PK_MODELE PRIMARY KEY(NAZWA_MODELU,PRODUCENT));
    
CREATE TABLE POJAZDY
      ( REJESTRACJA VARCHAR2(15) CONSTRAINT PK_POJAZDY PRIMARY KEY NOT NULL,
        NAZWA_MODELU VARCHAR2(50)  NOT NULL,
         PRODUCENT VARCHAR2(50)  NOT NULL,
        STAN_TECHNICZNY VARCHAR2(5) NOT NULL,
        CONSTRAINT CHK_STAN_TECHNICZNY CHECK(STAN_TECHNICZNY IN ('ZLY','DOBRY')),
        CONSTRAINT FK_POJAZDY FOREIGN KEY(NAZWA_MODELU,PRODUCENT) REFERENCES MODELE(NAZWA_MODELU,PRODUCENT)
        );
        
CREATE TABLE KIEROWCY
    ( ID_PRAC NUMBER constraint PK_KIEROWCY PRIMARY KEY NOT NULL,
	NAZWISKO VARCHAR2(50)  NOT NULL,
	ROK_URODZENIA DATE NOT NULL,
    IMIE VARCHAR2(50)  NOT NULL,
    NR_TEL VARCHAR2(9),
    constraint CHK_NR_TEL CHECK (regexp_like(nr_tel,'^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$') )
	);
    
CREATE TABLE ULGI (
RODZAJ VARCHAR2(50) CONSTRAINT PK_ULGI PRIMARY KEY NOT NULL,
PROCENT_ZNIZKI NUMBER NOT NULL,
constraint CHK_PROCENT_ZNIZKI CHECK (procent_znizki between 0 and 0.99));

CREATE TABLE BILETY (
MAX_MINUTY_PRZEJAZDU NUMBER CONSTRAINT PK_BILETY PRIMARY KEY NOT NULL,
CENA_ZL NUMBER(4,2) NOT NULL,
CONSTRAINT CHK_CENA_ZL CHECK(CENA_ZL>0),
CONSTRAINT CHK_MAX_MINUTY_PRZEJAZDU CHECK(MAX_MINUTY_PRZEJAZDU>0)
);

CREATE TABLE DZIELNICE (
NAZWA VARCHAR2(50) CONSTRAINT PK_DZIELNICE PRIMARY KEY NOT NULL,
LICZBA_MIESZKANCOW NUMBER NOT NULL,
CZY_BEZPIECZNA VARCHAR2(3) NOT NULL,
CONSTRAINT CHK_CZY_BEZPIECZNA CHECK(CZY_BEZPIECZNA IN ('TAK','NIE'))
);

CREATE TABLE PRZYSTANKI (
NAZWA_PRZYSTANKU VARCHAR2(50) NOT NULL,
NAZWA_DZIELNICY VARCHAR2(50) CONSTRAINT FK_PRZYSTANKI REFERENCES DZIELNICE(NAZWA) NOT NULL,
ZADASZENIE VARCHAR2(3) NOT NULL,
CONSTRAINT CHK_ZADASZENIE CHECK(ZADASZENIE IN ('TAK','NIE')),
CONSTRAINT PK_PRZYSTANKI PRIMARY KEY(NAZWA_PRZYSTANKU,NAZWA_DZIELNICY)
);

CREATE TABLE LINIE (
NAZWA VARCHAR2(2) NOT NULL CONSTRAINT PK_LINIE PRIMARY KEY,
KOLOR VARCHAR2(50) NOT NULL
);

CREATE TABLE PUNKTY_TRASY (
NAZWA_LINII VARCHAR2(50) NOT NULL CONSTRAINT FK1_PUNKTY_TRASY REFERENCES LINIE(NAZWA),
NAZWA_DZIELNICY VARCHAR2(50)  NOT NULL,
NAZWA_PRZYSTANKU VARCHAR2(50) NOT NULL,
NR_PRZYSTANKU_NA_TRASIE integer NOT NULL,
LICZBA_MINUT_OD_POPRZEDNIEGO NUMBER NOT NULL,
CONSTRAINT PK_PUNKTY_TRASY PRIMARY KEY(NAZWA_LINII,NAZWA_PRZYSTANKU,NR_PRZYSTANKU_NA_TRASIE),
CONSTRAINT FK2_PUNKTY_TRASY FOREIGN KEY(NAZWA_PRZYSTANKU,NAZWA_DZIELNICY) REFERENCES PRZYSTANKI
(NAZWA_PRZYSTANKU,NAZWA_DZIELNICY)
);

CREATE TABLE PRZEJAZDY (
NAZWA_LINII VARCHAR2(50) NOT NULL CONSTRAINT FK3_PRZEJAZDY REFERENCES LINIE(NAZWA),
GODZINA_STARTU  NUMBER(2,0) NOT NULL,
MINUTA_STARTU NUMBER(2,0) NOT NULL,
ID_KIEROWCY NUMBER CONSTRAINT FK1_PRZEJAZDY REFERENCES KIEROWCY(ID_PRAC)  NOT NULL,
REJESTRACJA_POJAZDU VARCHAR2(15) CONSTRAINT FK2_PRZEJAZDY REFERENCES POJAZDY(REJESTRACJA) NOT NULL,
CONSTRAINT PK_PRZEJAZDY PRIMARY KEY(NAZWA_LINII,GODZINA_STARTU,MINUTA_STARTU),
constraint CHK_CZASY CHECK(GODZINA_STARTU<24 AND GODZINA_STARTU>=0 AND MINUTA_STARTU>=0 AND MINUTA_STARTU<60)
);




--ograniczenia

alter table punkty_trasy add constraint CHK_LICZBA_MINUT check(liczba_minut_od_poprzedniego>=0);
alter table linie add constraint CHK_KOLOR check(kolor in('Niebieski','Czerwony','Czarny','Zielony',
'Fioletowy','Bordowy','Oliwkowy','Kremowy','Szary','Granatowy'));
alter table dzielnice add constraint CHK_LICZBA_MIESZKANCOW check(liczba_mieszkancow>0);
alter table pojazdy modify rejestracja varchar2(7);
alter table modele modify liczba_konii number;
alter table modele add constraint CHK_KOSZT_ZL check(koszt_zl>0);
alter table modele add constraint CHK_LICZBA_KONII check(liczba_konii>0);
alter table punkty_trasy add constraint CHK_NR_PRZYSTANKU check(nr_przystanku_na_trasie>=0);

ALTER TABLE punkty_trasy
ADD CONSTRAINT UQ_PUNKTY_TRASY UNIQUE(nazwa_linii,nr_przystanku_na_trasie);
alter table kierowcy add constraint CHK_ROK_URODZENIA check(extract(year from rok_urodzenia)>1930);
ALTER TABLE kierowcy
ADD CONSTRAINT UQ_NR_TEL UNIQUE (nr_tel);
alter table producenci add constraint CHK_KRAJ check (kraj_pochodzenia in 
('Polska','Węgry','Szwajcaria','Niemcy','USA','Belgia'
,'Holandia','Czechy','Hiszpania'));

--producenci
    
insert into producenci values('Mercedes-Benz',to_date('01-01-1881','DD-MM-YYYY'),'Niemcy');
insert into producenci values('Solaris',to_date('01-03-1994','DD-MM-YYYY'),'Polska');
insert into producenci values('Ikarus',to_date('15-07-1895','DD-MM-YYYY'),'Węgry');
insert into producenci values('Carrosserie Hess',to_date('01-09-1882','DD-MM-YYYY'),'Szwajcaria');
    
--modele
	
insert into modele values('Urbino 18 Hybrid','Solaris',220,15000000);
insert into modele values('Urbino 12 electric','Solaris',218,10000000);
insert into modele values('Urbino 12','Solaris',220,1500000);

insert into modele values('eCitaro','Mercedes-Benz',300,20000000);
insert into modele values('Citaro','Mercedes-Benz',350,16000000);
insert into modele values('NGT','Mercedes-Benz',230,7000000);

insert into modele values('412T','Ikarus',200,700000);
insert into modele values('V187','Ikarus',270,6000000);
insert into modele values('I280','Ikarus',195,2000000);

insert into modele values('Swisstrolley','Carrosserie Hess',270,25000000);
insert into modele values('LighTram','Carrosserie Hess',300,30000000);
insert into modele values('Eurotrolley','Carrosserie Hess',230,22000000);

--pojazdy
insert into pojazdy values('PO 21TL','eCitaro','Mercedes-Benz','DOBRY');
insert into pojazdy values('PO 42MT','Eurotrolley','Carrosserie Hess','DOBRY');
insert into pojazdy values('PO 29AX','V187','Ikarus','ZLY');
insert into pojazdy values('PO 23VA','Eurotrolley','Carrosserie Hess','DOBRY');
insert into pojazdy values('PO 45AW','Urbino 12 electric','Solaris','DOBRY');
insert into pojazdy values('PO 75CE','Urbino 18 Hybrid','Solaris','DOBRY');
insert into pojazdy values('PO 22RP','Citaro','Mercedes-Benz','DOBRY');
insert into pojazdy values('PO 29DT','NGT','Mercedes-Benz','ZLY');
    
--kierowcy

insert into kierowcy values(SEQ_ID.NEXTVAL,'Plaszczyk',to_date('01-09-1987','DD-MM-YYYY'),'Maciej','354351120');
insert into kierowcy values(SEQ_ID.NEXTVAL,'Reynolds',to_date('01-09-1965','DD-MM-YYYY'),'Andrew','153229210');
insert into kierowcy values(SEQ_ID.NEXTVAL,'Lotkowski',to_date('01-09-1989','DD-MM-YYYY'),'Edward','781121120');
insert into kierowcy values(SEQ_ID.NEXTVAL,'Kasztanowski',to_date('01-09-1990','DD-MM-YYYY'),'Marek','345548920');
insert into kierowcy values(SEQ_ID.NEXTVAL,'Nawrocki',to_date('01-09-1994','DD-MM-YYYY'),'Marcin','924532110');
insert into kierowcy values(SEQ_ID.NEXTVAL,'Socha',to_date('01-09-1957','DD-MM-YYYY'),'Andrzej','349821120');
insert into kierowcy values(SEQ_ID.NEXTVAL,'Kowalski',to_date('01-09-1977','DD-MM-YYYY'),'Jan','034576120');
insert into kierowcy values(SEQ_ID.NEXTVAL,'Kowalczyk',to_date('01-09-1976','DD-MM-YYYY'),'Beata','015321120');
insert into kierowcy values(SEQ_ID.NEXTVAL,'Kubica',to_date('01-09-1958','DD-MM-YYYY'),'Robert','789121120');
insert into kierowcy values(SEQ_ID.NEXTVAL,'Nowak',to_date('01-09-1987','DD-MM-YYYY'),'Eryk','245007020');

--ULGI

insert into ulgi values('Weteran',0.78);
insert into ulgi values('Doktorant',0.51);
insert into ulgi values('Student',0.51);
insert into ulgi values('Emeryt',0.37);

--Bilety
insert into bilety values(40,15);
insert into bilety values(30,12);
insert into bilety values(20,8);
insert into bilety values(10,5);

--DZIELNICE
insert into dzielnice values('Junikowo',8837,'TAK');
insert into dzielnice values('Ogrody',6598,'TAK');
insert into dzielnice values('Rataje',40328,'TAK');
insert into dzielnice values('Stare Winogrady',7467,'TAK');
insert into dzielnice values('Stare Miasto',30433,'NIE');
insert into dzielnice values('Winiary',15991,'TAK');
insert into dzielnice values('Wilda',29205,'TAK');
insert into dzielnice values('Stary Grunwald',3545,'NIE');

--przystanki
insert into przystanki values('Rynek Wildecki','Wilda','TAK');
insert into przystanki values('Teatralny','Wilda','TAK');
insert into przystanki values('Kwiatowy','Wilda','NIE');

insert into przystanki values('Rynek Ogrodowy','Ogrody','TAK');
insert into przystanki values('Most Ogrodowy','Ogrody','NIE');
insert into przystanki values('Zamkowy','Ogrody','NIE');

insert into przystanki values('Politechnika','Rataje','TAK');
insert into przystanki values('Serafitek','Rataje','TAK');
insert into przystanki values('Ratajczaka','Rataje','TAK');

insert into przystanki values('Adama Mickiewicza','Stare Winogrady','TAK');
insert into przystanki values('Stary Rynek','Stare Winogrady','NIE');
insert into przystanki values('Winogradowy','Stare Winogrady','TAK');

insert into przystanki values('Miastowy','Stare Miasto','TAK');
insert into przystanki values('Kazimierza Starego','Stare Miasto','NIE');
insert into przystanki values('Filmowski','Stare Miasto','TAK');

insert into przystanki values('Magiczny','Winiary','TAK');
insert into przystanki values('Winiarskiego','Winiary','NIE');
insert into przystanki values('Stephena Kinga','Winiary','TAK');

insert into przystanki values('Marcinkowskiego','Junikowo','TAK');
insert into przystanki values('Jana Sobieskiego','Junikowo','NIE');
insert into przystanki values('Piasta','Junikowo','TAK');

insert into przystanki values('Bitwy pod Grunwaldem','Stary Grunwald','TAK');
insert into przystanki values('Kazimierza Odnowiciela','Stary Grunwald','NIE');
insert into przystanki values('Lamberta','Stary Grunwald','TAK');

--linie

insert into linie values('A1','Fioletowy');
insert into linie values('R5','Niebieski');
insert into linie values('6A','Granatowy');
insert into linie values('15','Zielony');
insert into linie values('TY','Czarny');
insert into linie values('P9','Szary');

--przejazdy

insert into przejazdy values('A1',15,10,10,'PO 21TL');
insert into przejazdy values('R5',13,5,20,'PO 42MT');
insert into przejazdy values('6A',14,3,30,'PO 23VA');
insert into przejazdy values('15',11,8,40,'PO 29AX');
insert into przejazdy values('TY',20,0,60,'PO 45AW');
insert into przejazdy values('P9',17,30,70,'PO 29DT');
insert into przejazdy values('A1',19,15,80,'PO 75CE');

--punkty trasy

insert into punkty_trasy values('A1','Ogrody','Rynek Ogrodowy',0,0);
insert into punkty_trasy values('A1','Ogrody','Most Ogrodowy',1,5);
insert into punkty_trasy values('A1','Rataje','Politechnika',2,5);
insert into punkty_trasy values('A1','Winiary','Stephena Kinga',3,15);

insert into punkty_trasy values('R5','Junikowo','Marcinkowskiego',0,0);
insert into punkty_trasy values('R5','Junikowo','Jana Sobieskiego',1,6);
insert into punkty_trasy values('R5','Junikowo','Piasta',2,6);
insert into punkty_trasy values('R5','Winiary','Winiarskiego',3,20);

insert into punkty_trasy values('6A','Wilda','Rynek Wildecki',0,0);
insert into punkty_trasy values('6A','Ogrody','Zamkowy',1,10);
insert into punkty_trasy values('6A','Stare Winogrady','Adama Mickiewicza',2,15);

insert into punkty_trasy values('15','Stary Grunwald','Lamberta',0,0);
insert into punkty_trasy values('15','Rataje','Serafitek',1,5);
insert into punkty_trasy values('15','Rataje','Politechnika',2,5);
insert into punkty_trasy values('15','Stare Miasto','Filmowy',3,15);
insert into punkty_trasy values('15','Winiary','Winiarskiego',4,20);

--funkcje procedury

create or replace procedure Zmniejsz_nr
(nazwa IN varchar,
nazwa_dziel IN varchar,
nazwa_przyst IN varchar,
nr IN number) is
begin
delete from punkty_trasy where nazwa_linii=nazwa and nr_przystanku_na_trasie=nr and nazwa_dzielnicy = nazwa_dziel 
and nazwa_przystanku=nazwa_przyst;
update punkty_trasy set nr_przystanku_na_trasie = nr_przystanku_na_trasie -1 where nazwa_linii=nazwa and 
nr_przystanku_na_trasie>nr;
end Zmniejsz_nr;

/

create or replace function Wylicz_cene
(prodzaj_znizki IN varchar,
pcena_biletu IN number)
return number is cena_koncowa number;
vcena_biletu number;
vznizka number;
begin
select procent_znizki into vznizka from ulgi where rodzaj=prodzaj_znizki;
vcena_biletu := round((1-vznizka)*pcena_biletu,2);
return vcena_biletu;
end Wylicz_cene;
/
commit;
