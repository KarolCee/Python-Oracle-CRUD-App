import cx_Oracle
from tkinter import messagebox


def search(array,text):
    found = []
    szukany = text.upper()
    for row in array:
        for column in row:
            if szukany in (str(column)).upper():
                found.append(row)
                break
    return found
class Database:
    def __init__(self):
        username = str(input("Proszę podać nazwę użytkownika: "))
        haslo = str(input("Proszę podać hasło: "))
        user_haslo = username + "/" + haslo
        try:
            self.conn = cx_Oracle.connect(f'{user_haslo}@localhost')
            print('Udalo się zalogować')
        except Exception as e:
            print(f'Nie udało się zalogować: {e}')
        self.cur = self.conn.cursor()
    def fetch_producenci(self,szukany,filtr):
        if len(filtr) == 0:
            self.cur.execute("select nazwa,rok_rozpoczecia,kraj_pochodzenia from producenci")
            rows = self.cur.fetchall()
        else:

            polecenie = f"select nazwa,rok_rozpoczecia,kraj_pochodzenia from producenci order by {filtr} "
            self.cur.execute(polecenie)
            rows = self.cur.fetchall()
        rows = search(rows,szukany)
        return rows
    def fetch_kierowcy(self,szukany,filtr):
        if len(filtr) == 0:
            self.cur.execute("select id_prac,nazwisko,rok_urodzenia,imie,nr_tel from kierowcy order by id_prac")
            rows = self.cur.fetchall()
        else:

            polecenie = f"select id_prac,nazwisko,rok_urodzenia,imie,nr_tel from kierowcy order by {filtr} "
            self.cur.execute(polecenie)
            rows = self.cur.fetchall()
        rows = search(rows,szukany)
        return rows
    def fetch_all(self,szukany,filtr,tabela):

        if len(filtr) == 0:
            if tabela=='punkty_trasy':
                polecenie = f"select * from {tabela} order by 1,4"
                self.cur.execute(polecenie)
                rows = self.cur.fetchall()
            elif tabela == 'przejazdy':
                polecenie = f"select * from {tabela} order by 2,3,1"
                self.cur.execute(polecenie)
                rows = self.cur.fetchall()
            else:
                polecenie = f"select * from {tabela}"
                self.cur.execute(polecenie)
                rows = self.cur.fetchall()
        else:

            polecenie = f"select * from {tabela} order by {filtr} "
            self.cur.execute(polecenie)
            rows = self.cur.fetchall()
        rows = search(rows,szukany)
        return rows
    def fetch_combo_prompt(self,whatprompt,fromwhere):
        polecenie = f'select {whatprompt} from {fromwhere}'
        self.cur.execute(polecenie)
        rows = self.cur.fetchall()
        return rows
    def fetch_combo_prompt_where(self,whatprompt,fromwhere,what,where):
        polecenie = f"select {whatprompt} from {fromwhere} where {what}='{where}' "
        self.cur.execute(polecenie)
        rows = self.cur.fetchall()
        return rows
    def fetch_sort_prompt(self,tablename):
        polecenie = f"select column_name from all_tab_cols where table_name = '{tablename}'"
        self.cur.execute(polecenie)
        rows = self.cur.fetchall()
        return rows
    def fetch_polecenie(self,polecenie):
        self.cur.execute(polecenie)
        rows = self.cur.fetchall()
        return rows
    def fetch_void(self,polecenie):
        self.cur.execute(polecenie)

    #TE SA ZLE

    #PRZEJAZDY
    def insert_przejazdy(self,nazwa_linii,godzina_startu,minuta_startu,id_kierowcy,rejestracja_pojazdu):
        self.cur.execute("insert into przejazdy values(:1,:2,:3,:4,:5)",
                         (nazwa_linii,godzina_startu,minuta_startu,id_kierowcy,rejestracja_pojazdu))
        self.conn.commit()

    def remove_przejazdy(self,nazwa_linii,godzina_startu,minuta_startu):
        self.cur.execute("delete from przejazdy where nazwa_linii=:1 and godzina_startu=:2 and minuta_startu=:3",(nazwa_linii,godzina_startu,minuta_startu))
        self.conn.commit()
    def update_przejazdy(self,nazwa_linii,godzina_startu,minuta_startu,id_kierowcy,rejestracja_pojazdu):
        self.cur.execute("""update przejazdy set id_kierowcy=:1, rejestracja_pojazdu=:2
         where nazwa_linii = :3 and godzina_startu=:4 and minuta_startu=:5 """,(id_kierowcy,rejestracja_pojazdu,nazwa_linii,godzina_startu,minuta_startu))
        self.conn.commit()

    #KIEROWCY
    def insert_kierowcy(self,id_prac,nazwisko,rok_urodzenia,imie,nr_tel):
        try:
            maximum = self.cur.execute("select max(id_prac) from kierowcy")
            wiersz = self.cur.fetchall()
            id_prac = wiersz[0][0]
            self.cur.execute("""insert into kierowcy values(:1,:2,to_date(:3,'YYYY-MM-DD'),:4,:5) """,
                             (id_prac + 10, nazwisko, rok_urodzenia, imie, nr_tel))
            self.conn.commit()
        except:

            self.cur.execute("select seq_id.nextval from dual")
            wiersz = self.cur.fetchall()
            id_prac = wiersz[0][0]

            self.cur.execute("""insert into kierowcy values(:1,:2,to_date(:3,'YYYY-MM-DD'),:4,:5) """, (id_prac,nazwisko,rok_urodzenia,imie,nr_tel))
            self.conn.commit()

    def remove_kierowcy(self,id_prac):
        self.cur.execute("delete from kierowcy where id_prac=:1",(id_prac,))
        self.conn.commit()

    def update_kierowcy(self,id_prac,nazwisko,rok_urodzenia,imie,nr_tel):
        self.cur.execute("""update kierowcy set nazwisko=:1,rok_urodzenia=to_date(:2,'YYYY-MM-DD'),imie=:3,nr_tel=:4
        where id_prac=:5 """,(nazwisko,rok_urodzenia,imie,nr_tel,id_prac))
        self.conn.commit()
    #ULGI
    def insert_ulgi(self,rodzaj,procent_znizki):
        self.cur.execute("insert into ulgi values(:1,:2)",
                         (rodzaj,procent_znizki))
        self.conn.commit()

    def remove_ulgi(self,rodzaj):
        self.cur.execute("delete from ulgi where rodzaj=:1",(rodzaj,))
        self.conn.commit()

    def update_ulgi(self,rodzaj,procent_znizki):
        self.cur.execute("""update ulgi set procent_znizki = :1 where rodzaj =:2""",(procent_znizki,rodzaj))
        self.conn.commit()
    #BILETY
    def insert_bilety(self,max_minuty_przejazdu,cena_zl):
        self.cur.execute("insert into bilety values(:1,:2)",
                         (max_minuty_przejazdu,cena_zl))
        self.conn.commit()

    def remove_bilety(self,max_minuty_przejazdu):
        self.cur.execute("delete from bilety where max_minuty_przejazdu=:1",(max_minuty_przejazdu,))
        self.conn.commit()

    def update_bilety(self,max_minuty_przejazdu,cena_zl):
        self.cur.execute("""update bilety set cena_zl=:1 where max_minuty_przejazdu=:2""",(cena_zl,max_minuty_przejazdu))
        self.conn.commit()
    #POJAZDY
    def insert_pojazdy(self,rejestracja,nazwa_modelu,producent,stan_techniczny):
        self.cur.execute("insert into pojazdy values(:1,:2,:3,:4)",
                         (rejestracja,nazwa_modelu,producent,stan_techniczny))
        self.conn.commit()

    def remove_pojazdy(self,rejestracja):
        self.cur.execute("delete from pojazdy where rejestracja=:1",(rejestracja,))
        self.conn.commit()

    def update_pojazdy(self,rejestracja,nazwa_modelu,producent,stan_techniczny):
        self.cur.execute("""update pojazdy set nazwa_modelu=:1,producent=:2,stan_techniczny=:3 where rejestracja=:4""",
        (nazwa_modelu,producent,stan_techniczny,rejestracja))
        self.conn.commit()
    #MODELE
    def insert_modele(self,nazwa_modelu,producent,liczba_konii,koszt_zl):
        self.cur.execute("insert into modele values(:1,:2,:3,:4)",
                         (nazwa_modelu,producent,liczba_konii,koszt_zl))
        self.conn.commit()

    def remove_modele(self,nazwa_modelu,producent):
        self.cur.execute("delete from modele where nazwa_modelu=:1 and producent=:2",(nazwa_modelu,producent))
        self.conn.commit()

    def update_modele(self,nazwa_modelu,producent,liczba_konii,koszt_zl):
        self.cur.execute("""update modele set liczba_konii=:1,koszt_zl=:2 where nazwa_modelu=:3 and producent=:4""",
        (liczba_konii,koszt_zl,nazwa_modelu,producent))
        self.conn.commit()
    #PRODUCENCI
    def insert_producenci(self,nazwa,rok_rozpoczecia,kraj_pochodzenia):
        self.cur.execute("insert into producenci values(:1,to_date(:2,'YYYY-MM-DD'),:3)",
                         (nazwa,rok_rozpoczecia,kraj_pochodzenia))
        self.conn.commit()

    def remove_producenci(self,nazwa):
        self.cur.execute("delete from producenci where nazwa=:1",(nazwa,))
        self.conn.commit()

    def update_producenci(self,nazwa,rok_rozpoczecia,kraj_pochodzenia):
        self.cur.execute("""update producenci set rok_rozpoczecia=to_date(:1,'YYYY-MM-DD'),kraj_pochodzenia=:2 where nazwa=:3""",
        (rok_rozpoczecia,kraj_pochodzenia,nazwa))
        self.conn.commit()
    #LINIE
    def insert_linie(self,nazwa,kolor):
        self.cur.execute("insert into linie values(:1,:2)",
                         (nazwa,kolor))
        self.conn.commit()

    def remove_linie(self,nazwa):
        self.cur.execute("delete from linie where nazwa=:1",(nazwa,))
        self.conn.commit()

    def update_linie(self,nazwa,kolor):
        self.cur.execute("""update linie set kolor = :1 where nazwa =:2""",(kolor,nazwa))
        self.conn.commit()
    #PUNKTY_TRASY
    def insert_punkty_trasy(self,nazwa_linii,nazwa_dzielnicy,nazwa_przystanku,nr_przystanku_na_trasie,liczba_minut_od_poprzedniego):
        self.cur.execute("insert into punkty_trasy values(:1,:2,:3,:4,:5)",
                         (nazwa_linii,nazwa_dzielnicy,nazwa_przystanku,nr_przystanku_na_trasie,liczba_minut_od_poprzedniego))
        self.conn.commit()

    def remove_punkty_trasy(self,nazwa_linii,nazwa_dzielnicy,nazwa_przystanku,nr_przystanku_na_trasie):
        self.cur.callproc('Zmniejsz_nr' ,[nazwa_linii,nazwa_dzielnicy,nazwa_przystanku,nr_przystanku_na_trasie])
        # self.cur.execute("delete from punkty_trasy where nazwa_linii=:1 and nazwa_dzielnicy=:2 and nazwa_przystanku=:3 and nr_przystanku_na_trasie=:4",
        #                  (nazwa_linii,nazwa_dzielnicy,nazwa_przystanku,nr_przystanku_na_trasie))
        self.conn.commit()

    def update_punkty_trasy(self,nazwa_linii,nazwa_dzielnicy,nazwa_przystanku,nr_przystanku_na_trasie,liczba_minut_od_poprzedniego):
        self.cur.execute("""update punkty_trasy set liczba_minut_od_poprzedniego=:1
        where nazwa_linii=:2 and nazwa_dzielnicy=:3 and nazwa_przystanku=:4 and nr_przystanku_na_trasie=:5""",
        (liczba_minut_od_poprzedniego,nazwa_linii,nazwa_dzielnicy,nazwa_przystanku,nr_przystanku_na_trasie))
        self.conn.commit()
    #PRZYTANKI
    def insert_przystanki(self,nazwa_przystanku,nazwa_dzielnicy,zadaszenie):
        self.cur.execute("insert into przystanki values(:1,:2,:3)",
                         (nazwa_przystanku,nazwa_dzielnicy,zadaszenie))
        self.conn.commit()

    def remove_przystanki(self,nazwa_przystanku,nazwa_dzielnicy):
        self.cur.execute("delete from przystanki where nazwa_przystanku=:1 and nazwa_dzielnicy=:2 ",(nazwa_przystanku,nazwa_dzielnicy))
        self.conn.commit()

    def update_przystanki(self,nazwa_przystanku,nazwa_dzielnicy,zadaszenie):
        self.cur.execute("""update przystanki set zadaszenie=:1 where nazwa_przystanku=:2 and nazwa_dzielnicy=:3 """,
        (zadaszenie,nazwa_przystanku,nazwa_dzielnicy))
        self.conn.commit()
    #DZIELNICE
    def insert_dzielnice(self,nazwa,liczba_mieszkancow,czy_bezpieczna):
        self.cur.execute("insert into dzielnice values(:1,:2,:3)",
                         (nazwa,liczba_mieszkancow,czy_bezpieczna))
        self.conn.commit()

    def remove_dzielnice(self,nazwa):
        self.cur.execute("delete from dzielnice where nazwa=:1",(nazwa,))
        self.conn.commit()

    def update_dzielnice(self,nazwa,liczba_mieszkancow,czy_bezpieczna):
        self.cur.execute("""update dzielnice set liczba_mieszkancow=:1,czy_bezpieczna=:2 where nazwa = :3 """,
        (liczba_mieszkancow,czy_bezpieczna,nazwa))
        self.conn.commit()
    def wylicz_cene(self,rodzaj_znizki,cena_wyjsciowa):
        return self.cur.callfunc('Wylicz_cene',float,[str(rodzaj_znizki),float(cena_wyjsciowa)])


    def __del__(self):
        self.cur.close()
        self.conn.close()





















