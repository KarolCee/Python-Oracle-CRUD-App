from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from functools import partial
from DB import *
import re


db = Database()

def gridder(tree,labels,entries,rightbuttons,upbottons,Padx=0,Pady=0):
    if len(labels) < 5:
        tree.grid(columnspan = 5,rowspan = 5, row = 1 ,column=2,padx=Padx,pady=Pady)
    else:
        tree.grid(columnspan=5, rowspan=len(labels), row=1, column=2,padx=Padx,pady=Pady)
    for i, labelentry in enumerate(zip(labels, entries)):
        labelentry[0].grid(column=0, row=i+1,pady=Pady)
        labelentry[1].grid(column=1, row=i+1,padx=Padx,pady=Pady)
    for i, element in enumerate(rightbuttons):
        element.grid(column=7,row=i+1,padx=Padx,pady=Pady)
    for i, element in enumerate(upbottons):
        element.grid(row=0, column=i+2,padx=Padx,pady=Pady)

def change_tabs(tablica,bg_color):
    for i in tablica:
        i.configure(bg=bg_color)
def change_widgets(tablica,fg_color,bg_color,font_params):
    for i in tablica:
        i.configure(fg = fg_color, bg=bg_color,font = font_params)
def change_buttons(tablica,fg_color,bg_color,font_params,vWidth=20):
    for i in tablica:
        i.configure(fg = fg_color, bg=bg_color,font = font_params,width=vWidth)
def change_tree(tree,kolumny,Width):
    if Width<11:
        liczba_kolumn = len(kolumny)
        Width = int(950/liczba_kolumn)
    tree['columns'] = kolumny
    tree.heading("#0", text="", anchor="w")
    tree.column("#0", anchor="center", width=5, stretch=NO)
    for i in kolumny:
        tree.heading(i,text=i,anchor='center')
        tree.column(i, anchor="center",width=Width)



#TAB PRZEJAZDY
def filter_przejazdy():
    if button_filter_przejazdy['text'] == 'Zastosuj filtry':
        populate_przejazdy()
        button_filter_przejazdy['text'] = 'Resetuj filtry'
    else:
        clear(0)
        populate_przejazdy()
        button_filter_przejazdy['text'] = 'Zastosuj filtry'
def add_przejazdy():
    try:
        db.insert_przejazdy(entry_nazwa_linii_przejazdy.get(),entry_godzina_startu_przejazdy.get(),entry_minuta_startu_przejazdy.get(),
                            id_kierowcy_przejazdy.get(),rejestracja_pojazdu_przejazdy.get())

        clear_przejazdy()
        populate_przejazdy()
    except Exception as e:
        x = e.args[0]
        if 'FK3_PRZEJAZDY' in str(x):
            messagebox.showerror('Error!','Podana linia nie istnieje!')
        elif 'FK1_PRZEJAZDY' in str(x):
            messagebox.showerror('Error!','Taki pracownik nie istnieje!')
        elif 'FK2_PRZEJAZDY' in str(x):
            messagebox.showerror('Error!','Taki pojazd nie istnieje!')
        elif 'PK_PRZEJAZDY' in str(x):
            messagebox.showerror('Error!','Ta linia obsługuje już przejazd w tym czasie!')
        elif 'CHK_CZASY' in str(x):
            messagebox.showerror('Error!','Godzina powinna zawierać się w przedziale <0,24) a minuta <0,60)!')
        elif 'CHK_NR_PRZYSTANKU' in str(x):
            messagebox.showerror('Error!','Numer przystanku na trasie powinien być liczbą nieujemną!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Proszę uzupełnić wszystkie pola!')
        else:
            messagebox.showerror('Error!','Nie udało się dodać nowego przejazdu. Proszę zweryfikować poprawność podanych informacji!')
def remove_przejazdy():
    try:
        db.remove_przejazdy(entry_nazwa_linii_przejazdy.get(), entry_godzina_startu_przejazdy.get(), entry_minuta_startu_przejazdy.get())
        clear_przejazdy()
        populate_przejazdy()
    except:
        messagebox.showerror('Error!','Nie udało się usunać przejazdu. Proszę najpierw zaznaczyć rekord do usunięcia!')
def update_przejazdy():
    try:
        db.update_przejazdy(entry_nazwa_linii_przejazdy.get(),entry_godzina_startu_przejazdy.get(),entry_minuta_startu_przejazdy.get(),
                            id_kierowcy_przejazdy.get(),rejestracja_pojazdu_przejazdy.get())
        clear_przejazdy()
        populate_przejazdy()
    except Exception as e:
        x = e.args[0]
        if 'FK3_PRZEJAZDY' in str(x):
            messagebox.showerror('Error!','Podana linia nie istnieje!')
        elif 'FK1_PRZEJAZDY' in str(x):
            messagebox.showerror('Error!','Taki pracownik nie istnieje!')
        elif 'FK2_PRZEJAZDY' in str(x):
            messagebox.showerror('Error!','Taki pojazd nie istnieje!')
        elif 'CHK_CZASY' in str(x):
            messagebox.showerror('Error!','Godzina powinna zawierać się w przedziale <0,24) a minuta <0,60)!')
        elif 'CHK_NR_PRZYSTANKU' in str(x):
            messagebox.showerror('Error!','Numer przystanku na trasie powinien być liczbą nieujemną!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Proszę uzupełnić wszystkie pola!')
        else:
            messagebox.showerror('Error!','Nie udało się zmodyfikować przejazdu. Proszę najpierw zaznaczyć rekord do zmodyfikowania a następnie wybrać nowego kierowcę lub/i nowy pojazd!')
def clear_przejazdy():
    clear(0)
def select_item_przejazdy(event):
    if tree_przejazdy.selection():
        index = tree_przejazdy.selection()[0]
        selected = tree_przejazdy.item(index,'values')
        clear_przejazdy()
        for it,i in enumerate(entries_global[0]):
            if i['state'] != 'normal':
                i['state'] = 'normal'
                i.insert(END, selected[it])
                i['state'] = 'readonly'
            else:
                i.insert(END,selected[it])
def detail_przejazdy():
    try:
        nazwa_linii = entry_nazwa_linii_przejazdy.get()
        godzina = entry_godzina_startu_przejazdy.get()
        minuta = entry_minuta_startu_przejazdy.get()


        wiersz = db.fetch_polecenie(f"select * from przejazdy where nazwa_linii='{nazwa_linii}' and godzina_startu='{godzina}' and minuta_startu='{minuta}' ")
        pkty_trasy = db.fetch_polecenie(f"select * from punkty_trasy where nazwa_linii = '{nazwa_linii}' order by nr_przystanku_na_trasie")
        trasa=""
        if len(pkty_trasy)!=0:
            for i in pkty_trasy:
                trasa= trasa + '->'  + str(i[2])
            trasa = trasa[2:]

        linia = str(wiersz[0][0])
        kierowca = str(wiersz[0][3])
        pojazd = str(wiersz[0][4])
        wiersz_linie = db.fetch_polecenie(f"select * from linie where nazwa='{linia}'")
        wiersz_kierowcy= db.fetch_polecenie(f"select * from kierowcy where id_prac='{kierowca}'")
        wiersz_pojazdy = db.fetch_polecenie(f"select * from pojazdy where rejestracja='{pojazd}'")
        wiersz_kierowcy[0] = list(wiersz_kierowcy[0])
        wiersz_kierowcy[0][2] = str(wiersz_kierowcy[0][2])[0:10]

        dostaw_godzine = ""
        dostaw_minute = ""
        if len(str(godzina)) < 2:
            dostaw_godzine = "0"
        if len(str(minuta)) < 2:
            dostaw_minute = "0"
        nowa_godzina = dostaw_godzine + str(godzina) + ':' + dostaw_minute + str(minuta)

        top_przejazdy = Toplevel()
        top_przejazdy.title(f'Szczegóły przejazdu na linii {nazwa_linii}, {nowa_godzina}, {trasa}')
        # top_przejazdy.geometry('1500x600')  # widthxheight

        trees_top_przejazdy = []
        columns_top_przejazdy = []
        dane_top_przejazdy = []
        dane_top_przejazdy.append(wiersz_kierowcy)
        dane_top_przejazdy.append(wiersz_pojazdy)
        dane_top_przejazdy.append(wiersz_linie)

        tree_kierowcy_top = ttk.Treeview(top_przejazdy)  # TAB KIEROWCY
        kolumny_kierowcy_top = ('ID KIEROWCY', 'NAZWISKO KIEROWCY', 'DATA URODZENIA', 'IMIĘ KIEROWCY', 'NR TEL KIEROWCY')
        trees_top_przejazdy.append(tree_kierowcy_top)
        columns_top_przejazdy.append(kolumny_kierowcy_top)

        tree_pojazdy_top = ttk.Treeview(top_przejazdy)  # TAB POJAZDY
        kolumny_pojazdy_top = ('REJESTRACJA POJAZDY', 'MODEL POJAZDU', 'PRODUCENT POJAZDU', 'STAN TECHNICZNY POJAZDU')
        trees_top_przejazdy.append(tree_pojazdy_top)
        columns_top_przejazdy.append(kolumny_pojazdy_top)

        tree_linie_top = ttk.Treeview(top_przejazdy)  # TAB LINIE
        kolumny_linie_top = ('NAZWA LINII', 'KOLOR LINII')
        trees_top_przejazdy.append(tree_linie_top)
        columns_top_przejazdy.append(kolumny_linie_top)

        for t, c in zip(trees_top_przejazdy, columns_top_przejazdy):
            change_tree(t, c, 10)


        for index,i in enumerate(trees_top_przejazdy):
            i.grid(column=1,row=index)
            for row in i.get_children():
                i.delete(row)
            for row in dane_top_przejazdy[index]:
                i.insert("", END, values=row)
    except:
        messagebox.showerror('Error!','Proszę najpierw zaznaczyć odpowiedni przejazd!')
def populate_przejazdy():
    searchfor = str(entry_search_przejazdy.get())
    sortby = str(entry_sort_przejazdy.get())
    for row in tree_przejazdy.get_children():
        tree_przejazdy.delete(row)
    for row in db.fetch_all(searchfor,sortby,'przejazdy'):
        tree_przejazdy.insert("", END, values=row)
#TAB KIEROWCY
def filter_kierowcy():
    if button_filter_kierowcy['text'] == 'Zastosuj filtry':
        populate_kierowcy()
        button_filter_kierowcy['text'] = 'Resetuj filtry'
    else:
        clear(1)
        populate_kierowcy()
        button_filter_kierowcy['text'] = 'Zastosuj filtry'
def add_kierowcy():
    try:
        imie = str(entry_imie_kierowcy.get())
        imie = imie.replace(" ", "")
        bad_chars = re.findall('[^A-Za-zęóąśłżźćń]', imie)
        if len(bad_chars) == 0:
            imie = (imie[0].upper() + imie[1:].lower())
        else:
            messagebox.showerror('Error!', 'Proszę podać poprawne imię!')
            return

        nazwisko = str(entry_nazwisko_kierowcy.get())
        nazwisko = nazwisko.replace(" ", "")
        bad_chars = re.findall('[^A-Za-zęóąśłżźćń]', nazwisko)
        if len(bad_chars) == 0:
            nazwisko = (nazwisko[0].upper() + nazwisko[1:].lower())
        else:
            messagebox.showerror('Error!', 'Proszę podać poprawne nazwisko!')
            return

        db.insert_kierowcy(entry_id_prac_kierowcy.get(), nazwisko,
                           entry_rok_urodzenia_kierowcy.get(), imie, entry_nr_tel_kierowcy.get())
        clear_kierowcy()
        populate_kierowcy()
    except Exception as e:
        x = e.args[0]
        if 'PK_KIEROWCY' in str(x):
            messagebox.showerror('Error!', 'Podane ID jest zajęte!')
        elif 'CHK_NR_TEL' in str(x):
            messagebox.showerror('Error!', f'Numer telefonu powinien się składać z 9 cyfr!')
        elif 'CHK_ROK_URODZENIA' in str(x):
            messagebox.showerror('Error!', 'Podano zbyt dawną datę (proszę podać datę po 1930 roku)!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!', 'Wszystkie pola muszą zostać wypełnione!')
        elif 'UQ_NR_TEL' in str(x):
            messagebox.showerror('Error!', 'Podany numer telefonu jest już zajęty!')
        elif 'index' in str(x):
            messagebox.showerror('Error!', 'Proszę zweryfikować poprawność wpisane imienia oraz nazwiska')
        elif '"SYSTEM"."KIEROWCY"."NR_TEL"' in str(x):
            messagebox.showerror('Error!', 'Numer telefonu powinien się składać z 9 cyfr!')
        else:
            messagebox.showerror('Error!', f'Proszę zweryfikować poprawność wpisanych informacji (data powinna być w formacie ROK-MIESIĄC-DZIEŃ, np. 1999-01-01)')
def remove_kierowcy():
    try:
        db.remove_kierowcy(entry_id_prac_kierowcy.get())
        clear_kierowcy()
        populate_kierowcy()
        populate_przejazdy()
    except:
        messagebox.showerror('Error!','Usunięcie kierowcy nie powiodło się, proszę najpierw zaznaczyć kierowcę do usunięcia!')
def update_kierowcy():
    try:
        imie = str(entry_imie_kierowcy.get())
        imie = imie.replace(" ", "")
        bad_chars = re.findall('[^A-Za-zęóąśłżźćń]', imie)
        if len(bad_chars) == 0:
            imie = (imie[0].upper() + imie[1:].lower())
        else:
            messagebox.showerror('Error!', 'Proszę podać poprawne imię!')
            return

        nazwisko = str(entry_nazwisko_kierowcy.get())
        nazwisko = nazwisko.replace(" ", "")
        bad_chars = re.findall('[^A-Za-zęóąśłżźćń]', nazwisko)
        if len(bad_chars) == 0:
            nazwisko = (nazwisko[0].upper() + nazwisko[1:].lower())
        else:
            messagebox.showerror('Error!', 'Proszę podać poprawne nazwisko!')
            return
        db.update_kierowcy(entry_id_prac_kierowcy.get(), nazwisko,
        entry_rok_urodzenia_kierowcy.get(), imie, entry_nr_tel_kierowcy.get())
        clear_kierowcy()
        populate_kierowcy()
    except Exception as e:
        x = e.args[0]
        if 'CHK_NR_TEL' in str(x):
            messagebox.showerror('Error!', 'Numer telefonu powinien się składać z 9 cyfr!')
        elif 'CHK_ROK_URODZENIA' in str(x):
            messagebox.showerror('Error!', 'Podano zbyt dawną datę (proszę podać datę po 1930 roku)!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!', 'Wszystkie pola muszą zostać wypełnione!')
        elif 'UQ_NR_TEL' in str(x):
            messagebox.showerror('Error!', 'Podany numer telefonu jest już zajęty!')
        elif 'index' in str(x):
            messagebox.showerror('Error!', 'Proszę zweryfikować poprawność wpisane imienia oraz nazwiska')
        else:
            messagebox.showerror('Error!', f'Proszę najpierw zaznaczyć rekord do zmodyfikowania a następnie zweryfikować poprawność wpisanych informacji (data powinna być w formacie ROK-MIESIĄC-DZIEŃ, np. 1999-01-01)')

def clear_kierowcy():
    clear(1)
def select_item_kierowcy(event):
    if tree_kierowcy.selection():
        index = tree_kierowcy.selection()[0]
        selected = tree_kierowcy.item(index,'values')
        clear_kierowcy()
        for it,i in enumerate(entries_global[1]):
            if i['state'] != 'normal':
                i['state'] = 'normal'
                i.insert(END, selected[it])
                i['state'] = 'readonly'
            else:
                i.insert(END,selected[it])
def populate_kierowcy():
    searchfor = str(entry_search_kierowcy.get())
    sortby = str(entry_sort_kierowcy.get())
    for row in tree_kierowcy.get_children():
        tree_kierowcy.delete(row)
    for row in db.fetch_kierowcy(searchfor, sortby):
        row = list(row)
        row[2] = str(row[2])[0:10]
        tree_kierowcy.insert("", END, values=row)
def detail_kierowcy():
    try:
        ID = entry_id_prac_kierowcy.get()
        przejazdy = db.fetch_polecenie(f"select * from przejazdy where id_kierowcy='{ID}'")


        top_kierowcy = Toplevel()
        top_kierowcy.title(f'Przejazdy obsługiwane przez kierowcę o identyfikatorze: {ID} ')
        # top_przejazdy.geometry('1500x600')  # widthxheight


        tree_top_kierowcy = ttk.Treeview(top_kierowcy)  # TAB PRZEJAZDY
        kolumny_top_kierowcy = ('NAZWA LINII', 'GODZINA STARTU', 'MINUTA STARTU', 'ID KIEROWCY', 'REJESTRACJA POJAZDU')
        change_tree(tree_top_kierowcy, kolumny_top_kierowcy, 10)



        for row in tree_top_kierowcy.get_children():
            tree_top_kierowcy.delete(row)
        for row in przejazdy:
            tree_top_kierowcy.insert("", END, values=row)

        tree_top_kierowcy.grid(column=0,row=0)
    except:
        messagebox.showerror('Error!','Proszę najpierw zaznaczyć odpowiedniego kierowcę!')

#TAB ULGI
def filter_ulgi():
    if button_filter_ulgi['text'] == 'Zastosuj filtry':
        populate_ulgi()
        button_filter_ulgi['text'] = 'Resetuj filtry'
    else:
        clear(2)
        populate_ulgi()
        button_filter_ulgi['text'] = 'Zastosuj filtry'
def add_ulgi():
    try:
        db.insert_ulgi(entry_rodzaj_ulgi.get(), entry_procent_znizki_ulgi.get())
        clear_ulgi()
        populate_ulgi()
    except Exception as e:
        x=e.args[0]
        if 'CHK_PROCENT_ZNIZKI' in str(x):
            messagebox.showerror('Error!','Zniżka powinna się zawierać w przedziale <0,0.99>!')
        elif 'PK_ULGI' in str(x):
            messagebox.showerror('Error!','Ulga o takiej nazwie już istnieje!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Wszystkie pola muszą być uzupełnione!')
        else:
            messagebox.showerror('Error!','Wystąpił błąd podczas dodawania ulgi! (upewnij się że podana zniżka jest liczbą z zakresu <0,0.99>!')



def remove_ulgi():
    try:
        db.remove_ulgi(entry_rodzaj_ulgi.get())
        clear_ulgi()
        populate_ulgi()
    except:
        messagebox.showerror('Error!','Usunięcie ulgi nie powiodło się, proszę najpierw zaznaczyć rekord do usunięcia lub ręcznie wpisać rodzaj ulgi!')
def update_ulgi():
    try:
        db.update_ulgi(entry_rodzaj_ulgi.get(), entry_procent_znizki_ulgi.get())
        clear_ulgi()
        populate_ulgi()
    except Exception as e:
        x=e.args[0]
        if 'CHK_PROCENT_ZNIZKI' in str(x):
            messagebox.showerror('Error!','Zniżka powinna się zawierać w przedziale <0,0.99>!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Oba pola muszą być uzupełnione!')
        else:
            messagebox.showerror('Error!','Wystąpił błąd podczas modyfikowania ulgi! Proszę najpierw zaznaczyć rekord do zmodyfikowania lub ręcznie wpisać rodzaj ulgi do zmodyfikowania a następnie poprawnie uzupełnić wielkość zniżki (upewnij się że podana zniżka jest liczbą z zakresu <0,0.99>!')
def clear_ulgi():
    clear(2)
def select_item_ulgi(event):
    if tree_ulgi.selection():
        index = tree_ulgi.selection()[0]
        selected = tree_ulgi.item(index,'values')
        clear_ulgi()
        for it,i in enumerate(entries_global[2]):
            if i['state'] != 'normal':
                i['state'] = 'normal'
                i.insert(END, selected[it])
                i['state'] = 'readonly'
            else:
                i.insert(END,selected[it])
def populate_ulgi():
    searchfor = str(entry_search_ulgi.get())
    sortby = str(entry_sort_ulgi.get())
    for row in tree_ulgi.get_children():
        tree_ulgi.delete(row)
    for row in db.fetch_all(searchfor, sortby, 'ulgi'):
        tree_ulgi.insert("", END, values=row)

#BILETY
def filter_bilety():
    if button_filter_bilety['text'] == 'Zastosuj filtry':
        populate_bilety()
        button_filter_bilety['text'] = 'Resetuj filtry'
    else:
        clear(3)
        populate_bilety()
        button_filter_bilety['text'] = 'Zastosuj filtry'
def add_bilety():
    try:
        db.insert_bilety(entry_max_minuty_przejazdu_bilety.get(),entry_cena_zl_bilety.get())
        clear_bilety()
        populate_bilety()
    except Exception as e:
        x = e.args[0]
        if 'CHK_CENA_ZL' in str(x):
            messagebox.showerror('Error!','Cena powinna być liczbą dodatnią!')
        elif 'CHK_MAX_MINUTY_PRZEJAZDU' in str(x):
            messagebox.showerror('Error!','Maksymalna liczba minut przejazdu powinna być liczbą dodatnią!')
        elif 'PK_BILETY' in str(x):
            messagebox.showerror('Error!','Bilet dla takiej liczby minut jest już określony!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Oba pola muszą być wypełnione!')
        else:
            messagebox.showerror('Error!','Dodanie nowego biletu nie powiodło się. Proszę zweryfikować poprawność wypełnionych pól! (cena powinna być mniejsza niż 100 zł)')
def remove_bilety():
    try:
        db.remove_bilety(entry_max_minuty_przejazdu_bilety.get())
        clear_bilety()
        populate_bilety()
    except:
        messagebox.showerror('Error!','Usunięcie biletu nie powiodło sie, proszę najpierw zaznaczyć odpowiedni rekord lub ręcznie wpisać maksymalna liczbę minut określającą bilet do usunięcia!')
def update_bilety():
    try:
        db.update_bilety(entry_max_minuty_przejazdu_bilety.get(), entry_cena_zl_bilety.get())
        clear_bilety()
        populate_bilety()
    except Exception as e:
        x = e.args[0]
        if 'CHK_CENA_ZL' in str(x):
            messagebox.showerror('Error!', 'Cena powinna być liczbą dodatnią!')
        elif 'CHK_MAX_MINUTY_PRZEJAZDU' in str(x):
            messagebox.showerror('Error!', 'Maksymalna liczba minut przejazdu powinna być liczbą dodatnią!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!', 'Oba pola muszą być wypełnione!')
        else:
            messagebox.showerror('Error!','Modyfikacja biletu nie powiodła się. Proszę najpierw zaznaczyć odpowiedni rekord lub ręcznie wpisać maksymalna liczbę minut określającą bilet do modyfikacji, a następnie określić nową cenę! (cena powinna być mniejsza niż 100 zł)')

def clear_bilety():
    clear(3)
def select_item_bilety(event):
    if tree_bilety.selection():
        index = tree_bilety.selection()[0]
        selected = tree_bilety.item(index,'values')
        clear_bilety()
        for it,i in enumerate(entries_global[3]):
            if i['state'] != 'normal':
                i['state'] = 'normal'
                i.insert(END, selected[it])
                i['state'] = 'readonly'
            else:
                i.insert(END,selected[it])
def populate_bilety():
    searchfor = str(entry_search_bilety.get())
    sortby = str(entry_sort_bilety.get())
    for row in tree_bilety.get_children():
        tree_bilety.delete(row)
    for row in db.fetch_all(searchfor, sortby, 'bilety'):
        tree_bilety.insert("", END, values=row)

#TAB POJAZDY
def filter_pojazdy():
    if button_filter_pojazdy['text'] == 'Zastosuj filtry':
        populate_pojazdy()
        button_filter_pojazdy['text'] = 'Resetuj filtry'
    else:
        clear(4)
        populate_pojazdy()
        button_filter_pojazdy['text'] = 'Zastosuj filtry'
def add_pojazdy():
    try:
        db.insert_pojazdy(entry_rejestracja_pojazdy.get(),entry_nazwa_modelu_pojazdy.get(),entry_producent_pojazdy.get(),entry_stan_techniczny_pojazdy.get())
        clear_pojazdy()
        populate_pojazdy()
    except Exception as e:
        x = e.args[0]
        if 'PK_POJAZDY' in str(x):
            messagebox.showerror('Error!','Pojazd o podanej rejestracji już istnieje!')
        elif 'CHK_STAN_TECHNICZNY' in str(x):
            messagebox.showerror('Error!','Pole STAN TECHNICZNY powinno być uzupełnione tylko wpisem ZLY lub DOBRY!')
        elif 'FK_POJAZDY' in str(x):
            messagebox.showerror('Error!','Podany producent nie produkuje podanego modelu!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!', 'Wszystkie pola muszą zostać wypełnione!')
        elif 'FK_POJAZDY' in str(x):
            messagebox.showerror('Error!','Podany producent nie produkuje podanego modelu!')
        else:
            messagebox.showerror('Error!', 'Nie udało się dodać nowego pojazdu (sprawdź czy podana rejestracja składa się z maksymalnie 7 znaków!')
def remove_pojazdy():
    try:
        db.remove_pojazdy(entry_rejestracja_pojazdy.get())
        clear_pojazdy()
        populate_pojazdy()
        populate_przejazdy()
    except:
        messagebox.showerror('Error!','Próba usunięcia pojazdu nie powiodła się, proszę najpierw zaznaczyć rekord do usunięcia lub ręcznie wpisać rejestrację usuwanego pojazdu!')
def update_pojazdy():
    try:
        db.update_pojazdy(entry_rejestracja_pojazdy.get(), entry_nazwa_modelu_pojazdy.get(), entry_producent_pojazdy.get(),entry_stan_techniczny_pojazdy.get())
        clear_pojazdy()
        populate_pojazdy()
    except Exception as e:
        x = e.args[0]
        if 'PK_POJAZDY' in str(x):
            messagebox.showerror('Error!','Pojazd o podanej rejestracji już istnieje!')
        elif 'CHK_STAN_TECHNICZNY' in str(x):
            messagebox.showerror('Error!','Pole STAN TECHNICZNY powinno być uzupełnione tylko wpisem ZLY lub DOBRY!')
        elif 'FK_POJAZDY' in str(x):
            messagebox.showerror('Error!','Podany producent nie produkuje podanego modelu!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!', 'Wszystkie pola muszą zostać wypełnione!')
        else:
            messagebox.showerror('Error!', 'Nie udało się dodać nowego pojazdu (sprawdź czy podana rejestracja składa się z maksymalnie 7 znaków!')

def clear_pojazdy():
    clear(4)
def select_item_pojazdy(event):
    if tree_pojazdy.selection():
        index = tree_pojazdy.selection()[0]
        selected = tree_pojazdy.item(index,'values')
        clear_pojazdy()
        for it,i in enumerate(entries_global[4]):
            if i['state'] != 'normal':
                i['state'] = 'normal'
                i.insert(END, selected[it])
                i['state'] = 'readonly'
            else:
                i.insert(END,selected[it])
def populate_pojazdy():
    searchfor = str(entry_search_pojazdy.get())
    sortby = str(entry_sort_pojazdy.get())
    for row in tree_pojazdy.get_children():
        tree_pojazdy.delete(row)
    for row in db.fetch_all(searchfor, sortby, 'pojazdy'):
        tree_pojazdy.insert("", END, values=row)
def detail_pojazdy():
    try:
        rejestracja = entry_rejestracja_pojazdy.get()
        przejazdy = db.fetch_polecenie(f"select * from przejazdy where rejestracja_pojazdu='{rejestracja}'")

        top_pojazdy = Toplevel()
        top_pojazdy.title(f'Przejazdy obsługiwane przez pojazd o numerze rejestracyjnym: {rejestracja} ')
        # top_przejazdy.geometry('1500x600')  # widthxheight

        tree_top_pojazdy = ttk.Treeview(top_pojazdy)
        kolumny_top_pojazdy = ('NAZWA LINII', 'GODZINA STARTU', 'MINUTA STARTU', 'ID KIEROWCY', 'REJESTRACJA POJAZDU')
        change_tree(tree_top_pojazdy, kolumny_top_pojazdy, 10)

        for row in tree_top_pojazdy.get_children():
            tree_top_pojazdy.delete(row)
        for row in przejazdy:
            tree_top_pojazdy.insert("", END, values=row)

        tree_top_pojazdy.grid(column=0, row=0)
    except:
        messagebox.showerror('Error!','Proszę najpierw zaznaczyć odpowiedni pojazd!')
#TAB MODELE
def filter_modele():
    if button_filter_modele['text'] == 'Zastosuj filtry':
        populate_modele()
        button_filter_modele['text'] = 'Resetuj filtry'
    else:
        clear(5)
        populate_modele()
        button_filter_modele['text'] = 'Zastosuj filtry'
def add_modele():
    try:
        db.insert_modele(entry_nazwa_modelu_modele.get(),entry_producent_modele.get(),entry_liczba_konii_modele.get(),entry_koszt_zl_modele.get())
        clear_modele()
        populate_modele()
    except Exception as e:
        x=e.args[0]
        if 'CHK_KOSZT_ZL' in str(x):
            messagebox.showerror('Error!', 'Pole KOSZT powinno zawierać liczbę dodatnią!')
        elif 'CHK_LICZBA_KONII' in str(x):
            messagebox.showerror('Error!', 'Pole LICZBA KONII powinno zawierać liczbę dodatnią!')
        elif 'PK_MODELE' in str(x):
            messagebox.showerror('Error!', 'Model o podanej nazwie pochodzący od podanego producenta już istnieje!')
        elif 'FK_MODELE' in str(x):
            messagebox.showerror('Error!', 'Producent o podanej nazwie nie istnieje!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!', 'Wszystkie pola muszą zostać wypełnione!')
        else:
            messagebox.showerror('Error!', 'Wystąpił błąd podczas dodawania modelu, sprawdź czy pola LICZBA KONII oraz KOSZT zawierają wartości liczbowe!')


def remove_modele():
    try:
        db.remove_modele(entry_nazwa_modelu_modele.get(),entry_producent_modele.get())
        clear_modele()
        populate_modele()
        populate()
    except:
        messagebox.showerror('Error!','Operacja nie powiodła się, proszę najpierw zaznaczyć rekord do usunięcia lub wpisać odpowiednią nazwę producenta oraz nazwę modelu!')

def update_modele():
    try:
        db.update_modele(entry_nazwa_modelu_modele.get(),entry_producent_modele.get(),entry_liczba_konii_modele.get(),entry_koszt_zl_modele.get())
        clear_modele()
        populate_modele()
    except Exception as e:
        x=e.args[0]
        if 'CHK_KOSZT_ZL' in str(x):
            messagebox.showerror('Error!', 'Pole KOSZT powinno zawierać liczbę dodatnią!')
        elif 'CHK_LICZBA_KONII' in str(x):
            messagebox.showerror('Error!', 'Pole LICZBA KONII powinno zawierać liczbę dodatnią!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!', 'Wszystkie pola muszą zostać wypełnione!')
        else:
            messagebox.showerror('Error!','Proszę zaznaczyć odpowiedni rekord lub wpisać nazwy modyfikowanego modelu danego producenta a następnie poprawnie uzupełnić resztę informacji (sprawdź czy pola LICZBA KONII oraz KOSZT zawierają wartości liczbowe)')

def clear_modele():
    clear(5)
def select_item_modele(event):
    if tree_modele.selection():
        index = tree_modele.selection()[0]
        selected = tree_modele.item(index,'values')
        clear_modele()
        for it,i in enumerate(entries_global[5]):
            if i['state'] != 'normal':
                i['state'] = 'normal'
                i.insert(END, selected[it])
                i['state'] = 'readonly'
            else:
                i.insert(END,selected[it])
def populate_modele():
    searchfor = str(entry_search_modele.get())
    sortby = str(entry_sort_modele.get())
    for row in tree_modele.get_children():
        tree_modele.delete(row)
    for row in db.fetch_all(searchfor, sortby, 'modele'):
        tree_modele.insert("", END, values=row)

#TAB PRODUCENCI
def filter_producenci():
    if button_filter_producenci['text'] == 'Zastosuj filtry':
        populate_producenci()
        button_filter_producenci['text'] = 'Resetuj filtry'
    else:
        clear(6)
        populate_producenci()
        button_filter_producenci['text'] = 'Zastosuj filtry'
def add_producenci():
    try:
        db.insert_producenci(entry_nazwa_producenci.get(),entry_rok_rozpoczecia_producenci.get(),entry_kraj_pochodzenia_producenci.get())
        clear_producenci()
        populate_producenci()
    except Exception as e:
        x = e.args[0]
        if 'PK_PRODUCENCI' in str(x):
            messagebox.showerror('Error!', 'Producent o takiej nazwie już istnieje!')
        if 'NULL' in str(x):
            messagebox.showerror('Error!', 'Wszystkie pola powinny zostać wypełnione!')
        else:
            messagebox.showerror('Error!', f'Proszę zweryfikować poprawność wpisanych informacji (data powinna być w formacie ROK-MIESIĄC-DZIEŃ, np. 1999-01-01)')

def remove_producenci():
    try:
        db.remove_producenci(entry_nazwa_producenci.get())
        clear_producenci()
        populate_producenci()
        populate()
    except:
        messagebox.showerror('Error!', 'Operacja nie powiodła się, proszę najpierw zaznaczyć rekord do usunięcia lub wpisać odpowiednią nazwę producenta!')

def update_producenci():
    try:
        db.update_producenci(entry_nazwa_producenci.get(),entry_rok_rozpoczecia_producenci.get(),entry_kraj_pochodzenia_producenci.get())
        clear_producenci()
        populate_producenci()
    except Exception as e:
        x = e.args[0]
        if 'NULL' in str(x):
            messagebox.showerror('Error!', 'Wszystkie pola powinny zostać wypełnione!')
        else:
            messagebox.showerror('Error!',f'Proszę zaznaczyć odpowiedni rekord lub wpisać nazwę modyfikowanego producenta a następnie poprawnie uzupełnić resztę informacji (data powinna być w formacie ROK-MIESIĄC-DZIEŃ, np. 1999-01-01)')

def clear_producenci():
    clear(6)
def select_item_producenci(event):
    if tree_producenci.selection():
        index = tree_producenci.selection()[0]
        selected = tree_producenci.item(index, 'values')
        clear_producenci()
        for it, i in enumerate(entries_global[6]):
            if i['state'] != 'normal':
                i['state'] = 'normal'
                i.insert(END, selected[it])
                i['state'] = 'readonly'
            else:
                i.insert(END, selected[it])
def populate_producenci():
    searchfor = str(entry_search_producenci.get())
    sortby = str(entry_sort_producenci.get())
    for row in tree_producenci.get_children():
        tree_producenci.delete(row)
    for row in db.fetch_producenci(searchfor, sortby):
        row = list(row)
        row[1] = str(row[1])[0:10]
        tree_producenci.insert("", END, values=row)
#TAB LINIE
def filter_linie():
    if button_filter_linie['text'] == 'Zastosuj filtry':
        populate_linie()
        button_filter_linie['text'] = 'Resetuj filtry'
    else:
        clear(7)
        populate_linie()
        button_filter_linie['text'] = 'Zastosuj filtry'
def add_linie():
    try:
        db.insert_linie(entry_nazwa_linie.get(),entry_kolor_linie.get())
        clear_linie()
        populate_linie()
    except Exception as e:
        x = e.args[0]
        if 'PK_LINIE' in str(x):
            messagebox.showerror('Error!','Linia o takiej nazwie już istnieje!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Oba pola muszą zostać uzupełnione!')
        elif 'CHK_KOLOR' in str(x):
            messagebox.showerror('Error!','Nie obsługujemy takiego koloru!')
        else:
            messagebox.showerror('Error!','Nie udało się dodać nowej linii, sprawdź poprawność wpisanych danych (nazwa linia powinna się składać tylko z 2 znaków)!')
def remove_linie():
    try:
        db.remove_linie(entry_nazwa_linie.get())
        clear_linie()
        populate_linie()
        populate_przejazdy()
    except:
        messagebox.showerror('Error!','Nie udało się usunąć linii. Proszę najpierw zaznaczyć usuwany rekord lub ręcznie wpisać nazwę usuwanej linii!')
def update_linie():
    try:
        db.update_linie(entry_nazwa_linie.get(),entry_kolor_linie.get())
        clear_linie()
        populate_linie()
    except Exception as e:
        x = e.args[0]
        if 'NULL' in str(x):
            messagebox.showerror('Error!','Oba pola muszą zostać uzupełnione!')
        elif 'CHK_KOLOR' in str(x):
            messagebox.showerror('Error!','Nie obsługujemy takiego koloru!')
        else:
            messagebox.showerror('Error!','Nie udało się zmodyfikować linii. Proszę najpierw zaznaczyć modyfikowany rekord lub ręcznie wpisać nazwę modyfikowanej linii!')
def clear_linie():
    clear(7)
def select_item_linie(event):
    if tree_linie.selection():
        index = tree_linie.selection()[0]
        selected = tree_linie.item(index, 'values')
        clear_linie()
        for it, i in enumerate(entries_global[7]):
            if i['state'] != 'normal':
                i['state'] = 'normal'
                i.insert(END, selected[it])
                i['state'] = 'readonly'
            else:
                i.insert(END, selected[it])
def populate_linie():
    searchfor = str(entry_search_linie.get())
    sortby = str(entry_sort_linie.get())
    for row in tree_linie.get_children():
        tree_linie.delete(row)
    for row in db.fetch_all(searchfor, sortby, 'linie'):
        tree_linie.insert("", END, values=row)



#TAB PUNKTY TRASY
def filter_punkty_trasy():
    if button_filter_punkty_trasy['text']=='Zastosuj filtry':
        populate_punkty_trasy()
        button_filter_punkty_trasy['text'] = 'Resetuj filtry'
    else:
        clear(8)
        populate_punkty_trasy()
        button_filter_punkty_trasy['text']='Zastosuj filtry'
def add_punkty_trasy():
    try:

        r = db.fetch_polecenie(f"select * from punkty_trasy where nazwa_linii='{entry_nazwa_linii_punkty_trasy.get()}'")
        if len(r) == 0:
            entry_nr_przystanku_na_trasie_punkty_trasy['state'] = 'normal'
            entry_nr_przystanku_na_trasie_punkty_trasy.delete(0, END)
            entry_nr_przystanku_na_trasie_punkty_trasy.insert(END, '0')
            entry_nr_przystanku_na_trasie_punkty_trasy['state'] = 'readonly'



        if str(entry_nr_przystanku_na_trasie_punkty_trasy.get())=='0':
            entry_liczba_minut_od_poprzedniego_punkty_trasy.delete(0, END)
            entry_liczba_minut_od_poprzedniego_punkty_trasy.insert(END, '0')


        db.insert_punkty_trasy(entry_nazwa_linii_punkty_trasy.get(),entry_nazwa_dzielnicy_punkty_trasy.get(),entry_nazwa_przystanku_punkty_trasy.get(),
                               entry_nr_przystanku_na_trasie_punkty_trasy.get(),entry_liczba_minut_od_poprzedniego_punkty_trasy.get())
        clear_punkty_trasy()
        populate_punkty_trasy()
    except Exception as e:
        x = e.args[0]
        if 'FK1_PUNKTY_TRASY' in str(x):
            messagebox.showerror('Error!','Taka linia nie istnieje!')
        elif 'FK2_PUNKTY_TRASY' in str(x):
            messagebox.showerror('Error!','Taki przystanek nie istnieje!')
        elif 'PK_PUNKTY_TRASY' in str(x):
            messagebox.showerror('Error!','Punkt trasy o tym numerze dotyczący podanego przystanku na podanej linii już został zdefiniowany!')
        elif 'UQ_PUNKTY_TRASY' in str(x):
            messagebox.showerror('Error!','Punkt trasy o tym numerze już jest zdefiniownay na podanej linii!')
        elif 'CHK_NR_PRZYSTANKU' in str(x):
            messagebox.showerror('Error!','Numer przystanku na trasie powinien być liczbą dodatnią!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Proszę uzupełnić wszystkie pola!')
        elif 'CHK_LICZBA_MINUT' in str(x):
            messagebox.showerror('Error!','Liczba minut powinna być liczbą nieujemną!')
        else:
            messagebox.showerror('Error!','Nie udało się dodać nowego punktu trasy. Sprawdź poprawność wpisanych informacji!')
def remove_punkty_trasy():
    try:
        db.remove_punkty_trasy(entry_nazwa_linii_punkty_trasy.get(),entry_nazwa_dzielnicy_punkty_trasy.get(),entry_nazwa_przystanku_punkty_trasy.get(),
                               entry_nr_przystanku_na_trasie_punkty_trasy.get())
        clear_punkty_trasy()
        populate_punkty_trasy()
    except:
        messagebox.showerror('Error!','Usunięcie punktu trasy nie powiodło się. Proszę najpierw zaznaczyć rekord do usunięcia!')
def update_punkty_trasy():
    try:
        db.update_punkty_trasy(entry_nazwa_linii_punkty_trasy.get(),entry_nazwa_dzielnicy_punkty_trasy.get(),entry_nazwa_przystanku_punkty_trasy.get(),
                               entry_nr_przystanku_na_trasie_punkty_trasy.get(),entry_liczba_minut_od_poprzedniego_punkty_trasy.get())
        clear_punkty_trasy()
        populate_punkty_trasy()
    except Exception as e:
        x = e.args[0]
        if 'FK1_PUNKTY_TRASY' in str(x):
            messagebox.showerror('Error!','Taka linia nie istnieje!')
        elif 'FK2_PUNKTY_TRASY' in str(x):
            messagebox.showerror('Error!','Taki przystanek nie istnieje!')
        elif 'UQ_PUNKTY_TRASY' in str(x):
            messagebox.showerror('Error!','Punkt trasy o tym numerze już jest zdefiniownay na podanej linii!')
        elif 'CHK_NR_PRZYSTANKU' in str(x):
            messagebox.showerror('Error!','Numer przystanku na trasie powinien być liczbą dodatnią!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Proszę uzupełnić wszystkie pola!')
        elif 'CHK_LICZBA_MINUT' in str(x):
            messagebox.showerror('Error!','Liczba minut powinna być liczbą dodatnią!')
        else:
            messagebox.showerror('Error!','Nie udało się zmodyfikować punktu trasy. Proszę najpierw zaznaczyć odpowiedni rekord a następnie ustalić nową liczbę minut!')
def clear_punkty_trasy():
    clear(8)
def select_item_punkty_trasy(event):
    if tree_punkty_trasy.selection():
        index = tree_punkty_trasy.selection()[0]
        selected = tree_punkty_trasy.item(index, 'values')
        clear_punkty_trasy()
        for it, i in enumerate(entries_global[8]):
            if i['state'] != 'normal':
                i['state'] = 'normal'
                i.insert(END, selected[it])
                i['state'] = 'readonly'
            else:
                i.insert(END, selected[it])
def populate_punkty_trasy():
    searchfor = str(entry_search_punkty_trasy.get())
    sortby = str(entry_sort_punkty_trasy.get())
    for row in tree_punkty_trasy.get_children():
        tree_punkty_trasy.delete(row)
    for row in db.fetch_all(searchfor, sortby, 'punkty_trasy'):
        tree_punkty_trasy.insert("", END, values=row)
#TAB PRZYSTANKI
def filter_przystanki():
    if button_filter_przystanki['text'] == 'Zastosuj filtry':
        populate_przystanki()
        button_filter_przystanki['text'] = 'Resetuj filtry'
    else:
        clear(9)
        populate_przystanki()
        button_filter_przystanki['text'] = 'Zastosuj filtry'
def add_przystanki():
    try:
        db.insert_przystanki(entry_nazwa_przystanku_przystanki.get(),entry_nazwa_dzielnicy_przystanki.get(),entry_zadaszenie_przystanki.get())
        clear_przystanki()
        populate_przystanki()
    except Exception as e:
        x = e.args[0]
        if 'FK_PRZYSTANKI' in str(x):
            messagebox.showerror('Error!','Taka dzielnica nie istnieje!')
        elif 'CHK_ZADASZENIE' in str(x):
            messagebox.showerror('Error!','Pole ZADASZENIE powinno zawierać tylko tekst TAK lub NIE!')
        elif 'PK_PRZYSTANKI' in str(x):
            messagebox.showerror('Error!','Przystanek o podanej nazwie leżący na podanej dzielnicy już jest zdefiniowany!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Wszystkie pola powinny zostać uzupełnione!')
        else:
            messagebox.showerror('Error!','Wystąpił błąd przy dodawaniu nowego przystanku. Proszę zweryfikować poprawność uzupełnionych pól!')
def remove_przystanki():
    try:
        rows = db.fetch_polecenie(f"select nazwa_linii,nazwa_dzielnicy,nazwa_przystanku,nr_przystanku_na_trasie from punkty_trasy where nazwa_dzielnicy='{entry_nazwa_dzielnicy_przystanki.get()}' and nazwa_przystanku='{entry_nazwa_przystanku_przystanki.get()}' order by nazwa_linii,nr_przystanku_na_trasie")
        for i in rows:
            row = db.fetch_polecenie(f"select nazwa_linii,nazwa_dzielnicy,nazwa_przystanku,nr_przystanku_na_trasie from punkty_trasy where nazwa_dzielnicy='{entry_nazwa_dzielnicy_przystanki.get()}' and nazwa_przystanku='{entry_nazwa_przystanku_przystanki.get()}' order by nazwa_linii,nr_przystanku_na_trasie fetch first 1 row only")
            db.remove_punkty_trasy(str(row[0][0]), str(row[0][1]),str(row[0][2]),str(row[0][3]))
        db.remove_przystanki(entry_nazwa_przystanku_przystanki.get(),entry_nazwa_dzielnicy_przystanki.get())
        clear_przystanki()
        populate_przystanki()
        populate_punkty_trasy()
    except:
        messagebox.showerror('Error!','Usunięcie przystanku nie powiodło się. Proszę najpierw zaznaczyć rekord do usunięcia lub ręcznie wpisać nazwę usuwanego przystanku oraz dzielnicy na której się znajduje!')
def update_przystanki():
    try:
        db.update_przystanki(entry_nazwa_przystanku_przystanki.get(),entry_nazwa_dzielnicy_przystanki.get(),entry_zadaszenie_przystanki.get())
        clear_przystanki()
        populate_przystanki()
    except Exception as e:
        x = e.args[0]
        if 'FK_PRZYSTANKI' in str(x):
            messagebox.showerror('Error!','Taka dzielnica nie istnieje!')
        elif 'CHK_ZADASZENIE' in str(x):
            messagebox.showerror('Error!','Pole ZADASZENIE powinno zawierać tylko tekst TAK lub NIE!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Wszystkie pola powinny zostać uzupełnione!')
        else:
            messagebox.showerror('Error!','Wystąpił błąd przy modyfikowaniu przystanku. Proszę najpierw zaznaczyć rekord do zmodyfikowania lub ręcznie wpisać nazwę modyfikowanego przystanku oraz dzielnicy na której się znajduje oraz uzupełnienie pola ZADASZENIE!')
def clear_przystanki():
    clear(9)
def select_item_przystanki(event):
    if tree_przystanki.selection():
        index = tree_przystanki.selection()[0]
        selected = tree_przystanki.item(index, 'values')
        clear_przystanki()
        for it, i in enumerate(entries_global[9]):
            if i['state'] != 'normal':
                i['state'] = 'normal'
                i.insert(END, selected[it])
                i['state'] = 'readonly'
            else:
                i.insert(END, selected[it])
def populate_przystanki():
    searchfor = str(entry_search_przystanki.get())
    sortby = str(entry_sort_przystanki.get())
    for row in tree_przystanki.get_children():
        tree_przystanki.delete(row)
    for row in db.fetch_all(searchfor, sortby, 'przystanki'):
        tree_przystanki.insert("", END, values=row)
#TAB DZIELNICE
def filter_dzielnice():
    if button_filter_dzielnice['text'] == 'Zastosuj filtry':
        populate_dzielnice()
        button_filter_dzielnice['text'] = 'Resetuj filtry'
    else:
        clear(10)
        populate_dzielnice()
        button_filter_dzielnice['text'] = 'Zastosuj filtry'
def add_dzielnice():
    try:
        db.insert_dzielnice(entry_nazwa_dzielnice.get(),entry_liczba_mieszkancow_dzielnice.get(),entry_czy_bezpieczna_dzielnice.get())
        clear_dzielnice()
        populate_dzielnice()
    except Exception as e:
        x = e.args[0]
        if 'PK_DZIELNICE' in str(x):
            messagebox.showerror('Error!','Dzielnica o takiej nazwie już istnieje!')
        elif 'CHK_CZY_BEZPIECZNA' in str(x):
            messagebox.showerror('Error!','Pole CZY BEZPIECZNA powinna zawierać tylko tekst TAK lub NIE!')
        elif 'CHK_LICZBA_MIESZKANCOW' in str(x):
            messagebox.showerror('Error!','Liczba mieszkańców powinna być liczbą dodatnią!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Wszystkie pola muszą zostać uzupełnione!')
        else:
            messagebox.showerror('Error!','Dodanie nowej dzielnicy nie powiodło się zweryfikuj poprawność wszystkich podanych informacji!')

def remove_dzielnice():
    try:
        rows = db.fetch_polecenie(f"select nazwa_linii,nazwa_dzielnicy,nazwa_przystanku,nr_przystanku_na_trasie from punkty_trasy where nazwa_dzielnicy='{entry_nazwa_dzielnice.get()}' order by nazwa_linii,nr_przystanku_na_trasie")
        for i in rows:
            row = db.fetch_polecenie(f"select nazwa_linii,nazwa_dzielnicy,nazwa_przystanku,nr_przystanku_na_trasie from punkty_trasy where nazwa_dzielnicy='{entry_nazwa_dzielnice.get()}' order by nazwa_linii,nr_przystanku_na_trasie fetch first 1 row only")
            db.remove_punkty_trasy(str(row[0][0]), str(row[0][1]),str(row[0][2]),str(row[0][3]))
        db.remove_dzielnice(entry_nazwa_dzielnice.get())
        clear_dzielnice()
        populate_dzielnice()
        populate_przystanki()
        populate_punkty_trasy()
    except:
        messagebox.showerror('Error!','Usunięcie dzielnicy nie powiodło się proszę najpierw zaznaczyć rekord do usunięcia lub ręcznie wpisać nazwę usuwanej dzielnicy!')
def update_dzielnice():
    try:
        db.update_dzielnice(entry_nazwa_dzielnice.get(),entry_liczba_mieszkancow_dzielnice.get(),entry_czy_bezpieczna_dzielnice.get())
        clear_dzielnice()
        populate_dzielnice()
    except Exception as e:
        x = e.args[0]
        if 'CHK_CZY_BEZPIECZNA' in str(x):
            messagebox.showerror('Error!','Pole CZY BEZPIECZNA powinna zawierać tylko tekst TAK lub NIE!')
        elif 'NULL' in str(x):
            messagebox.showerror('Error!','Wszystkie pola muszą zostać uzupełnione!')
        elif 'CHK_LICZBA_MIESZKANCOW' in str(x):
            messagebox.showerror('Error!','Liczba mieszkańców powinna być liczbą dodatnią!')
        else:
            messagebox.showerror('Error!','Modyfikacja dzielnicy nie powiodła się proszę najpierw zaznaczyć odpowiedni rekord lub ręcznie uzupełnić nazwę dzielnicy i poprawnie uzupełnić resztę pól!')
def clear_dzielnice():
    clear(10)
def select_item_dzielnice(event):
    if tree_dzielnice.selection():
        index = tree_dzielnice.selection()[0]
        selected = tree_dzielnice.item(index, 'values')
        clear_dzielnice()
        for it, i in enumerate(entries_global[10]):
            if i['state'] != 'normal':
                i['state'] = 'normal'
                i.insert(END, selected[it])
                i['state'] = 'readonly'
            else:
                i.insert(END, selected[it])
def populate_dzielnice():
    searchfor = str(entry_search_dzielnice.get())
    sortby = str(entry_sort_dzielnice.get())
    for row in tree_dzielnice.get_children():
        tree_dzielnice.delete(row)
    for row in db.fetch_all(searchfor, sortby, 'dzielnice'):
        tree_dzielnice.insert("", END, values=row)

#osobne
def populate():
    populate_ulgi()
    populate_bilety()
    populate_dzielnice()
    populate_kierowcy()
    populate_linie()
    populate_modele()
    populate_pojazdy()
    populate_producenci()
    populate_przejazdy()
    populate_przystanki()
    populate_punkty_trasy()
def change_nazwa_linii():
    prompts = db.fetch_combo_prompt('nazwa','linie')
    prompts = [(str(s[0])).split(' ') for s in prompts]
    entry_nazwa_linii_przejazdy['values'] = prompts
    entry_nazwa_linii_punkty_trasy['values'] = prompts
def change_id_kierowcy():
    prompts = db.fetch_combo_prompt('id_prac', 'kierowcy')
    prompts = [(str(s[0])).split(' ') for s in prompts]
    entry_id_kierowcy_przejazdy['values'] = prompts
def change_nazwa_modelu():
    prompts = db.fetch_combo_prompt('nazwa_modelu','modele')
    prompts = [(str(s[0])).split(' ') for s in prompts]
    aktualny_producent = entry_producent_pojazdy.get()
    if len(aktualny_producent) == 0:
        pusty = ("")
        prompts.insert(0, pusty)
        entry_nazwa_modelu_pojazdy['values'] = prompts
    else:
        prompts = db.fetch_combo_prompt_where('nazwa_modelu', 'modele', 'producent', aktualny_producent)
        prompts = [(str(s[0])).split(' ') for s in prompts]
        pusty = ("")
        prompts.insert(0, pusty)
        entry_nazwa_modelu_pojazdy['values'] = prompts
def change_producent():
    prompts = db.fetch_combo_prompt('nazwa', 'producenci')
    prompts = [(str(s[0])).split(' ') for s in prompts]
    entry_producent_modele['values'] = prompts
    aktualny_model = entry_nazwa_modelu_pojazdy.get()
    if len(aktualny_model) == 0:
        pusty = ("")
        prompts.insert(0, pusty)
        entry_producent_pojazdy['values'] = prompts
    else:
        prompts = db.fetch_combo_prompt_where('producent', 'modele', 'nazwa_modelu', aktualny_model)
        prompts = [(str(s[0])).split(' ') for s in prompts]
        pusty = ("")
        prompts.insert(0, pusty)
        entry_producent_pojazdy['values'] = prompts
def change_rejestracja():
    prompts = db.fetch_combo_prompt('rejestracja', 'pojazdy')
    prompts = [(str(s[0])).split(' ') for s in prompts]
    entry_rejestracja_pojazdu_przejazdy['values'] = prompts
def change_nazwa_dzielnicy():
    prompts = db.fetch_combo_prompt('nazwa', 'dzielnice')
    prompts = [(str(s[0])).split(' ') for s in prompts]
    entry_nazwa_dzielnicy_przystanki['values'] = prompts
    aktualny_przystanek = entry_nazwa_przystanku_punkty_trasy.get()
    if len(aktualny_przystanek)==0:
        pusty = ("")
        prompts.insert(0, pusty)
        entry_nazwa_dzielnicy_punkty_trasy['values'] = prompts
    else:
        prompts = db.fetch_combo_prompt_where('nazwa_dzielnicy', 'przystanki', 'nazwa_przystanku', aktualny_przystanek)
        prompts = [(str(s[0])).split(' ') for s in prompts]
        pusty = ("")
        prompts.insert(0, pusty)
        entry_nazwa_dzielnicy_punkty_trasy['values'] = prompts
def change_nazwa_przystanku():
    prompts = db.fetch_combo_prompt('nazwa_przystanku', 'przystanki')
    prompts = [(str(s[0])).split(' ') for s in prompts]
    aktualna_dzielnica = entry_nazwa_dzielnicy_punkty_trasy.get()
    if len(aktualna_dzielnica)==0:
        pusty = ("")
        prompts.insert(0, pusty)
        entry_nazwa_przystanku_punkty_trasy['values'] = prompts
    else:
        prompts = db.fetch_combo_prompt_where('nazwa_przystanku','przystanki','nazwa_dzielnicy',aktualna_dzielnica)
        prompts = [(str(s[0])).split(' ') for s in prompts]
        pusty = ("")
        prompts.insert(0, pusty)
        entry_nazwa_przystanku_punkty_trasy['values'] = prompts
def change_nr_przystanku():
    if len(entry_nazwa_linii_punkty_trasy.get())!=0:
        numer = db.fetch_polecenie(f"select max(nr_przystanku_na_trasie) from punkty_trasy where nazwa_linii='{entry_nazwa_linii_punkty_trasy.get()}' fetch first 1 row only")
        if str(numer[0][0])=='None':
            entry_nr_przystanku_na_trasie_punkty_trasy['values'] = (str(0))
        else:
            entry_nr_przystanku_na_trasie_punkty_trasy['values'] = (str(int(numer[0][0])+1))
    else:
        messagebox.showerror('Error!','Proszę najpierw wybrać nazwę linii!')

def clear(parametr):
    indeks = parametr
    for i in entries_global[indeks]:
        if i['state']!='normal':
            i['state'] = 'normal'
            i.delete(0,END)
            i['state'] = 'readonly'
        else:
            i.delete(0,END)
    if upwidgets[indeks][1]['state']!='normal':
        upwidgets[indeks][1]['state']='normal'
        upwidgets[indeks][1].delete(0,END)
        upwidgets[indeks][1]['state'] = 'readonly'
    else:
        upwidgets[indeks][1].delete(0, END)

    if upwidgets[indeks][3]['state']!='normal':
        upwidgets[indeks][3]['state']='normal'
        upwidgets[indeks][3].delete(0,END)
        upwidgets[indeks][3]['state'] = 'readonly'
    else:
        upwidgets[indeks][3].delete(0, END)
def change_rodzaj_ulgi():
    prompts = db.fetch_combo_prompt('rodzaj', 'ulgi')
    prompts = [(str(s[0])).split(' ') for s in prompts]
    entry_rodzaj_ulgi_wyszukaj_trase['values']=prompts
def change_dzielnice_wyszukaj_trase():
    prompts = db.fetch_polecenie('select distinct(nazwa_dzielnicy) from przejazdy  join punkty_trasy using(nazwa_linii)')
    prompts = [(str(s[0])).split(' ') for s in prompts]
    entry_dzielnica_odjazdu_wyszukaj_trase['values'] = prompts
    entry_dzielnica_docelowa_wyszukaj_trase['values'] = prompts


#create window object
root = Tk()

#
# root.geometry('1000x500') #widthxheight
root.attributes("-fullscreen", True)
root.title('BUS FINDER')
root.bind("<Escape>", lambda event: root.destroy())

#tabs/zakladki
tabs = []
tab_control = ttk.Notebook(root)

tab_user = Frame(tab_control)
tab_control.add(tab_user,text='USER')

tab_control2 = ttk.Notebook(tab_user)


tab_wyszukaj_trase = Frame(tab_control2)
tab_control2.add(tab_wyszukaj_trase,text = "WYSZUKAJ TRASE")


tab_admin = Frame(tab_control)
tab_control.add(tab_admin,text='ADMIN')

tab_control3 = ttk.Notebook(tab_admin)

tab_przejazdy = Frame(tab_control3)
tab_control3.add(tab_przejazdy,text='PRZEJAZDY')

tab_kierowcy = Frame(tab_control3)
tab_control3.add(tab_kierowcy,text='KIEROWCY')

tab_ulgi = Frame(tab_control3)
tab_control3.add(tab_ulgi,text='ULGI')

tab_bilety = Frame(tab_control3)
tab_control3.add(tab_bilety,text='BILETY')

tab_pojazdy = Frame(tab_control3)
tab_control3.add(tab_pojazdy,text='POJAZDY')

tab_modele = Frame(tab_control3)
tab_control3.add(tab_modele,text='MODELE')

tab_producenci = Frame(tab_control3)
tab_control3.add(tab_producenci,text='PRODUCENCI')

tab_linie = Frame(tab_control3)
tab_control3.add(tab_linie,text='LINIE')

tab_punkty_trasy = Frame(tab_control3)
tab_control3.add(tab_punkty_trasy,text='PUNKTY TRASY')

tab_przystanki = Frame(tab_control3)
tab_control3.add(tab_przystanki,text='PRZYSTANKI')

tab_dzielnice = Frame(tab_control3)
tab_control3.add(tab_dzielnice,text='DZIELNICE')




tab_control.pack(expand=1,fill='both')
tab_control2.pack(expand=1,fill='both')
tab_control3.pack(expand=1,fill='both')

tabs.append(tab_przejazdy)
tabs.append(tab_kierowcy)
tabs.append(tab_ulgi)
tabs.append(tab_bilety)
tabs.append(tab_pojazdy)
tabs.append(tab_modele)
tabs.append(tab_producenci)
tabs.append(tab_linie)
tabs.append(tab_punkty_trasy)
tabs.append(tab_przystanki)
tabs.append(tab_dzielnice)
tabs.append(tab_wyszukaj_trase)



#labels/etykiety
labels_global = []
labels = []
label_nazwa_linii_przejazdy = Label(tab_przejazdy,text='NAZWA LINII:') #PRZEJAZDY
label_godzina_startu_przejazdy = Label(tab_przejazdy,text='GODZINA STARTU:')
label_minuta_startu_przejazdy = Label(tab_przejazdy,text='MINUTA STARTU:')
label_id_kierowcy_przejazdy = Label(tab_przejazdy,text='ID KIEROWCY:')
label_rejestracja_pojazdu_przejazdy = Label(tab_przejazdy,text='REJESTRACJA POJAZDU:')
label_search_przejazdy = Label(tab_przejazdy,text='SZUKAJ SŁOWA:')
label_sort_przejazdy = Label(tab_przejazdy,text='SORTUJ PO:')
labels.append(label_nazwa_linii_przejazdy)
labels.append(label_godzina_startu_przejazdy)
labels.append(label_minuta_startu_przejazdy)
labels.append(label_id_kierowcy_przejazdy)
labels.append(label_rejestracja_pojazdu_przejazdy)
labels.append(label_search_przejazdy)
labels.append(label_sort_przejazdy)
labels_global.append(labels)

labels = []
label_id_prac_kierowcy = Label(tab_kierowcy,text='ID PRAC:') #KIEROWCY
label_nazwisko_kierowcy = Label(tab_kierowcy,text='NAZWISKO:')
label_rok_urodzenia_kierowcy = Label(tab_kierowcy,text='DATA URODZENIA:')
label_imie_kierowcy = Label(tab_kierowcy,text='IMIĘ:')
label_nr_tel_kierowcy = Label(tab_kierowcy,text='NR TEL:')
label_search_kierowcy = Label(tab_kierowcy,text='SZUKAJ SŁOWA:')
label_sort_kierowcy = Label(tab_kierowcy,text='SORTUJ PO:')

labels.append(label_id_prac_kierowcy)
labels.append(label_nazwisko_kierowcy)
labels.append(label_rok_urodzenia_kierowcy)
labels.append(label_imie_kierowcy)
labels.append(label_nr_tel_kierowcy)
labels.append(label_search_kierowcy)
labels.append(label_sort_kierowcy)
labels_global.append(labels)

labels = []
label_rodzaj_ulgi = Label(tab_ulgi,text="RODZAJ:") #ULGI
label_procent_znizki_ulgi = Label(tab_ulgi,text='WIELKOŚĆ ZNIŻKI:')
label_search_ulgi = Label(tab_ulgi,text='SZUKAJ SŁOWA:')
label_sort_ulgi = Label(tab_ulgi,text='SORTUJ PO:')
labels.append(label_rodzaj_ulgi)
labels.append(label_procent_znizki_ulgi)
labels.append(label_search_ulgi)
labels.append(label_sort_ulgi)
labels_global.append(labels)

labels = []
label_max_minuty_przejazdu_bilety = Label(tab_bilety,text='MAX MINUTY PRZEJAZDY:') #BILETY
label_cena_zl_bilety = Label(tab_bilety,text='CENA ZŁ:')
label_search_bilety = Label(tab_bilety,text='SZUKAJ SŁOWA:')
label_sort_bilety = Label(tab_bilety,text='SORTUJ PO:')
labels.append(label_max_minuty_przejazdu_bilety)
labels.append(label_cena_zl_bilety)
labels.append(label_search_bilety)
labels.append(label_sort_bilety)
labels_global.append(labels)

labels = []
label_rejestracja_pojazdy = Label(tab_pojazdy,text='REJESTRACJA:') #POJAZDY
label_nazwa_modelu_pojazdy = Label(tab_pojazdy,text='NAZWA MODELU:')
label_producent_pojazdy = Label(tab_pojazdy,text='PRODUCENT:')
label_stan_techniczny_pojazdy = Label(tab_pojazdy,text='STAN TECHNICZNY:')
label_search_pojazdy = Label(tab_pojazdy,text='SZUKAJ SŁOWA:')
label_sort_pojazdy = Label(tab_pojazdy,text='SORTUJ PO:')
labels.append(label_rejestracja_pojazdy)
labels.append(label_nazwa_modelu_pojazdy)
labels.append(label_producent_pojazdy)
labels.append(label_stan_techniczny_pojazdy)
labels.append(label_search_pojazdy)
labels.append(label_sort_pojazdy)
labels_global.append(labels)

labels = []
label_nazwa_modelu_modele = Label(tab_modele,text='NAZWA MODELU:') #MODELE
label_producent_modele = Label(tab_modele,text='PRODUCENT:')
label_liczba_konii_modele = Label(tab_modele,text='LICZBA KONII:')
label_koszt_zl_modele = Label(tab_modele,text='KOSZT ZŁ:')
label_search_modele = Label(tab_modele,text='SZUKAJ SŁOWA:')
label_sort_modele = Label(tab_modele,text='SORTUJ PO:')
labels.append(label_nazwa_modelu_modele)
labels.append(label_producent_modele)
labels.append(label_liczba_konii_modele)
labels.append(label_koszt_zl_modele)
labels.append(label_search_modele)
labels.append(label_sort_modele)
labels_global.append(labels)

labels = []
label_nazwa_producenci = Label(tab_producenci,text='NAZWA:')              #PRODUCENCI
label_rok_rozpoczecia_producenci = Label(tab_producenci,text='DATA ROZPOCZĘCIA:')
label_kraj_pochodzenia_producenci = Label(tab_producenci,text='KRAJ POCHODZENIA:')
label_search_producenci = Label(tab_producenci,text='SZUKAJ SŁOWA:')
label_sort_producenci = Label(tab_producenci,text='SORTUJ PO:')
labels.append(label_nazwa_producenci)
labels.append(label_rok_rozpoczecia_producenci)
labels.append(label_kraj_pochodzenia_producenci)
labels.append(label_search_producenci)
labels.append(label_sort_producenci)
labels_global.append(labels)

labels = []
label_nazwa_linie = Label(tab_linie,text='NAZWA:') #LINIE
label_kolor_linie = Label(tab_linie,text='KOLOR:')
label_search_linie = Label(tab_linie,text='SZUKAJ SŁOWA:')
label_sort_linie = Label(tab_linie,text='SORTUJ PO:')
labels.append(label_nazwa_linie)
labels.append(label_kolor_linie)
labels.append(label_search_linie)
labels.append(label_sort_linie)
labels_global.append(labels)

labels = []
label_nazwa_linii_punkty_trasy = Label(tab_punkty_trasy,text = 'NAZWA LINII:')  #PUNKTY TRASY
label_nazwa_dzielnicy_punkty_trasy = Label(tab_punkty_trasy,text = 'NAZWA DZIELNICY:')
label_nazwa_przystanku_punkty_trasy = Label(tab_punkty_trasy,text='NAZWA PRZYSTANKU:')
label_nr_przystanku_na_trasie_punkty_trasy = Label(tab_punkty_trasy,text='NR PRZYSTANKU NA TRASIE:')
label_liczba_minut_od_poprzedniego_punkty_trasy = Label(tab_punkty_trasy,text='L. MIN. OD POPRZEDNIEGO:')
label_search_punkty_trasy = Label(tab_punkty_trasy,text='SZUKAJ SŁOWA:')
label_sort_punkty_trasy = Label(tab_punkty_trasy,text='SORTUJ PO:')

labels.append(label_nazwa_linii_punkty_trasy)
labels.append(label_nazwa_dzielnicy_punkty_trasy)
labels.append(label_nazwa_przystanku_punkty_trasy)
labels.append(label_nr_przystanku_na_trasie_punkty_trasy)
labels.append(label_liczba_minut_od_poprzedniego_punkty_trasy)
labels.append(label_search_punkty_trasy)
labels.append(label_sort_punkty_trasy)
labels_global.append(labels)

labels = []
label_nazwa_przystanku_przystanki = Label(tab_przystanki,text = 'NAZWA PRZYSTANKU:') #PRZYSTANKI
label_nazwa_dzielnicy_przystanki = Label(tab_przystanki,text ='NAZWA DZIELNICY:')
label_zadaszenie_przystanki = Label(tab_przystanki,text = 'ZADASZENIE:')
label_search_przystanki = Label(tab_przystanki,text='SZUKAJ SŁOWA:')
label_sort_przystanki = Label(tab_przystanki,text='SORTUJ PO:')
labels.append(label_nazwa_przystanku_przystanki)
labels.append(label_nazwa_dzielnicy_przystanki)
labels.append(label_zadaszenie_przystanki)
labels.append(label_search_przystanki)
labels.append(label_sort_przystanki)
labels_global.append(labels)

labels = []
label_nazwa_dzielnice = Label(tab_dzielnice,text='NAZWA:') #DZIELNICE
label_liczba_mieszkancow_dzielnice = Label(tab_dzielnice,text='LICZBA MIESZKAŃCÓW:')
label_czy_bezpieczna_dzielnice = Label(tab_dzielnice,text='CZY BEZPIECZNA:')
label_search_dzielnice = Label(tab_dzielnice,text='SZUKAJ SŁOWA:')
label_sort_dzielnice = Label(tab_dzielnice,text='SORTUJ PO:')
labels.append(label_nazwa_dzielnice)
labels.append(label_liczba_mieszkancow_dzielnice)
labels.append(label_czy_bezpieczna_dzielnice)
labels.append(label_search_dzielnice)
labels.append(label_sort_dzielnice)
labels_global.append(labels)
labels=[]

#entries/pola/comboboxy
entries_global=[]
entries=[]
#TAB PRZEJAZDY
nazwa_linii_przejazdy = StringVar()
godzina_startu_przejazdy = StringVar()
minuta_startu_przejazdy = StringVar()
id_kierowcy_przejazdy = StringVar()
rejestracja_pojazdu_przejazdy = StringVar()
search_przejazdy = StringVar()
sort_przejazdy = StringVar()
entry_nazwa_linii_przejazdy = ttk.Combobox(tab_przejazdy,textvariable=nazwa_linii_przejazdy,state="readonly",postcommand=change_nazwa_linii)
combo_nazwa_linii_przejazdy = []
entry_nazwa_linii_przejazdy['values'] = combo_nazwa_linii_przejazdy
entries.append(entry_nazwa_linii_przejazdy)
entry_godzina_startu_przejazdy = Entry(tab_przejazdy,textvariable=godzina_startu_przejazdy)
entries.append(entry_godzina_startu_przejazdy)
entry_minuta_startu_przejazdy = Entry(tab_przejazdy,textvariable=minuta_startu_przejazdy)
entries.append(entry_minuta_startu_przejazdy)
entry_id_kierowcy_przejazdy = ttk.Combobox(tab_przejazdy,textvariable=id_kierowcy_przejazdy,state="readonly",postcommand=change_id_kierowcy)
combo_id_kierowcy_przejazdy = [] #UZUPELNIJ Z DB.FETCH()
entry_id_kierowcy_przejazdy['values'] = combo_id_kierowcy_przejazdy
entries.append(entry_id_kierowcy_przejazdy)
entry_rejestracja_pojazdu_przejazdy = ttk.Combobox(tab_przejazdy,textvariable = rejestracja_pojazdu_przejazdy,state="readonly",postcommand=change_rejestracja)
combo_rejestracja_pojazdu_przejazdy = []
entry_rejestracja_pojazdu_przejazdy['values'] = combo_rejestracja_pojazdu_przejazdy
entries.append(entry_rejestracja_pojazdu_przejazdy)
entry_search_przejazdy = Entry(tab_przejazdy,textvariable=search_przejazdy)
entries.append(entry_search_przejazdy)
entry_sort_przejazdy = ttk.Combobox(tab_przejazdy,textvariable=sort_przejazdy,state="readonly")
combo_sort_przejazdy = db.fetch_sort_prompt('PRZEJAZDY')
entry_sort_przejazdy['values'] = combo_sort_przejazdy
entries.append(entry_sort_przejazdy)
entries_global.append(entries)
#TAB KIEROWCY
entries=[]
id_prac_kierowcy = StringVar()
nazwisko_kierowcy = StringVar()
rok_urodzenia_kierowcy = StringVar()
imie_kierowcy = StringVar()
nr_tel_kierowcy = StringVar()
search_kierowcy = StringVar()
sort_kierowcy = StringVar()
entry_id_prac_kierowcy = Entry(tab_kierowcy,textvariable=id_prac_kierowcy,state='readonly')
entry_nazwisko_kierowcy = Entry(tab_kierowcy,textvariable=nazwisko_kierowcy)
entry_rok_urodzenia_kierowcy = Entry(tab_kierowcy,textvariable=rok_urodzenia_kierowcy)
entry_imie_kierowcy = Entry(tab_kierowcy,textvariable=imie_kierowcy)
entry_nr_tel_kierowcy = Entry(tab_kierowcy,textvariable=nr_tel_kierowcy)
entry_search_kierowcy = Entry(tab_kierowcy,textvariable=search_kierowcy)
entry_sort_kierowcy = ttk.Combobox(tab_kierowcy,textvariable=sort_kierowcy,state="readonly")
combo_sort_kierowcy = db.fetch_sort_prompt('KIEROWCY')
entry_sort_kierowcy['values'] = combo_sort_kierowcy
entries.append(entry_id_prac_kierowcy)
entries.append(entry_nazwisko_kierowcy)
entries.append(entry_rok_urodzenia_kierowcy)
entries.append(entry_imie_kierowcy)
entries.append(entry_nr_tel_kierowcy)
entries.append(entry_search_kierowcy)
entries.append(entry_sort_kierowcy)
entries_global.append(entries)
#TAB ULGI
entries=[]
rodzaj_ulgi = StringVar()
procent_znizki_ulgi = StringVar()
sort_ulgi = StringVar()
search_ulgi = StringVar()
entry_rodzaj_ulgi = Entry(tab_ulgi,textvariable=rodzaj_ulgi)
entry_procent_znizki_ulgi = Entry(tab_ulgi,textvariable=procent_znizki_ulgi)
entry_search_ulgi = Entry(tab_ulgi,textvariable=search_ulgi)
entry_sort_ulgi = ttk.Combobox(tab_ulgi,textvariable=sort_ulgi,state="readonly")
combo_sort_ulgi = db.fetch_sort_prompt('ULGI')
entry_sort_ulgi['values'] = combo_sort_ulgi
entries.append(entry_rodzaj_ulgi)
entries.append(entry_procent_znizki_ulgi)
entries.append(entry_search_ulgi)
entries.append(entry_sort_ulgi)
entries_global.append(entries)
#TAB BILETY
entries=[]
max_minuty_przejazdu_bilety = StringVar()
cena_zl_bilety = StringVar()
sort_bilety = StringVar()
search_bilety = StringVar()
entry_max_minuty_przejazdu_bilety = Entry(tab_bilety,textvariable=max_minuty_przejazdu_bilety)
entry_cena_zl_bilety = Entry(tab_bilety,textvariable = cena_zl_bilety)
entry_search_bilety = Entry(tab_bilety,textvariable=search_bilety)
entry_sort_bilety = ttk.Combobox(tab_bilety,textvariable=sort_bilety,state="readonly")
combo_sort_bilety = db.fetch_sort_prompt('BILETY')
entry_sort_bilety['values'] = combo_sort_bilety

entries.append(entry_max_minuty_przejazdu_bilety)
entries.append(entry_cena_zl_bilety)
entries.append(entry_search_bilety)
entries.append(entry_sort_bilety)
entries_global.append(entries)
#TAB POJAZDY
entries=[]
rejestracja_pojazdy = StringVar()
nazwa_modelu_pojazdy = StringVar()
producent_pojazdy = StringVar()
stan_techniczny_pojazdy = StringVar()
search_pojazdy = StringVar()
sort_pojazdy = StringVar()
entry_rejestracja_pojazdy = Entry(tab_pojazdy,textvariable=rejestracja_pojazdy)
entry_nazwa_modelu_pojazdy = ttk.Combobox(tab_pojazdy,textvariable=nazwa_modelu_pojazdy,state="readonly",postcommand = change_nazwa_modelu)
combo_nazwa_modelu_pojazdy = [] #UZUPELNIJ Z DB.FETCH()
entry_nazwa_modelu_pojazdy['values'] = combo_nazwa_modelu_pojazdy
entry_producent_pojazdy = ttk.Combobox(tab_pojazdy,textvariable=producent_pojazdy,state="readonly",postcommand=change_producent)
combo_producent_pojazdy = [] #UZUPELNIJ Z DB.FETCH()
entry_producent_pojazdy['values'] = combo_producent_pojazdy
entry_stan_techniczny_pojazdy = ttk.Combobox(tab_pojazdy,textvariable=stan_techniczny_pojazdy,state="readonly")
combo_stan_techniczny_pojazdy = ('ZLY','DOBRY')
entry_stan_techniczny_pojazdy['values'] = combo_stan_techniczny_pojazdy
entry_search_pojazdy = Entry(tab_pojazdy,textvariable=search_pojazdy)
entry_sort_pojazdy = ttk.Combobox(tab_pojazdy,textvariable=sort_pojazdy,state="readonly")
combo_sort_pojazdy = db.fetch_sort_prompt('POJAZDY')
entry_sort_pojazdy['values'] = combo_sort_pojazdy

entries.append(entry_rejestracja_pojazdy)
entries.append(entry_nazwa_modelu_pojazdy)
entries.append(entry_producent_pojazdy)
entries.append(entry_stan_techniczny_pojazdy)
entries.append(entry_search_pojazdy)
entries.append(entry_sort_pojazdy)
entries_global.append(entries)
#TAB MODELE
entries=[]
nazwa_modelu_modele = StringVar()
producent_modele = StringVar()
liczba_konii_modele = StringVar()
koszt_zl_modele = StringVar()
search_modele = StringVar()
sort_modele = StringVar()
entry_nazwa_modelu_modele = Entry(tab_modele,textvariable=nazwa_modelu_modele)
entry_producent_modele = ttk.Combobox(tab_modele,textvariable=producent_modele,state="readonly",postcommand=change_producent)
combo_producent_modele = [] #UZUPELNIJ Z DB.FETCH()
entry_producent_modele['values'] = combo_producent_modele
entry_liczba_konii_modele = Entry(tab_modele,textvariable=liczba_konii_modele)
entry_koszt_zl_modele = Entry(tab_modele,textvariable=koszt_zl_modele)
entry_search_modele = Entry(tab_modele,textvariable=search_modele)
entry_sort_modele = ttk.Combobox(tab_modele,textvariable=sort_modele,state="readonly")
combo_sort_modele = db.fetch_sort_prompt('MODELE')
entry_sort_modele['values'] = combo_sort_modele
entries.append(entry_nazwa_modelu_modele)
entries.append(entry_producent_modele)
entries.append(entry_liczba_konii_modele)
entries.append(entry_koszt_zl_modele)
entries.append(entry_search_modele)
entries.append(entry_sort_modele)
entries_global.append(entries)

#TAB PRODUCENCI
entries=[]
nazwa_producenci = StringVar()
rok_rozpoczecia_producenci = StringVar()
kraj_pochodzenia_producenci = StringVar()
search_producenci = StringVar()
sort_producenci = StringVar()
entry_nazwa_producenci = Entry(tab_producenci,textvariable=nazwa_producenci)
entry_rok_rozpoczecia_producenci = Entry(tab_producenci,text=rok_rozpoczecia_producenci)
entry_kraj_pochodzenia_producenci = ttk.Combobox(tab_producenci,textvariable=kraj_pochodzenia_producenci,state="readonly")
entry_kraj_pochodzenia_producenci['values'] = ('Polska','Węgry','Szwajcaria','Niemcy','USA','Belgia','Holandia','Czechy','Hiszpania')
entry_search_producenci = Entry(tab_producenci,textvariable=search_producenci)
entry_sort_producenci = ttk.Combobox(tab_producenci,textvariable=sort_producenci,state="readonly")
combo_sort_producenci = db.fetch_sort_prompt('PRODUCENCI')
entry_sort_producenci['values'] = combo_sort_producenci
entries.append(entry_nazwa_producenci)
entries.append(entry_rok_rozpoczecia_producenci)
entries.append(entry_kraj_pochodzenia_producenci)
entries.append(entry_search_producenci)
entries.append(entry_sort_producenci)
entries_global.append(entries)
#TAB LINIE
entries=[]
nazwa_linie = StringVar()
kolor_linie = StringVar()
sort_linie = StringVar()
search_linie = StringVar()
entry_nazwa_linie = Entry(tab_linie,textvariable=nazwa_linie)
entry_kolor_linie = ttk.Combobox(tab_linie,textvariable=kolor_linie,state="readonly")
entry_kolor_linie['values'] = ('Niebieski','Czerwony','Czarny','Zielony','Fioletowy','Bordowy','Oliwkowy','Kremowy','Szary','Granatowy')
entry_search_linie = Entry(tab_linie,textvariable=search_linie)
entry_sort_linie = ttk.Combobox(tab_linie,textvariable=sort_linie,state="readonly")
combo_sort_linie = db.fetch_sort_prompt('LINIE')
entry_sort_linie['values'] = combo_sort_linie
entries.append(entry_nazwa_linie)
entries.append(entry_kolor_linie)
entries.append(entry_search_linie)
entries.append(entry_sort_linie)
entries_global.append(entries)
#TAB PUNKTY_TRASY
entries=[]
nazwa_linii_punkty_trasy = StringVar()
nazwa_dzielnicy_punkty_trasy = StringVar()
nazwa_przystanku_punkty_trasy = StringVar()
nr_przystanku_na_trasie_punkty_trasy = StringVar()
liczba_minut_od_poprzedniego_punkty_trasy = StringVar()
search_punkty_trasy = StringVar()
sort_punkty_trasy = StringVar()
entry_nazwa_linii_punkty_trasy = ttk.Combobox(tab_punkty_trasy,textvariable = nazwa_linii_punkty_trasy,state="readonly",postcommand=change_nazwa_linii)
combo_nazwa_linii_punkty_trasy = []
entry_nazwa_linii_punkty_trasy['values'] = combo_nazwa_linii_punkty_trasy
entry_nazwa_dzielnicy_punkty_trasy = ttk.Combobox(tab_punkty_trasy,textvariable = nazwa_dzielnicy_punkty_trasy,state="readonly",postcommand=change_nazwa_dzielnicy)
combo_nazwa_dzielnicy_punkty_trasy = []
entry_nazwa_dzielnicy_punkty_trasy['values'] = combo_nazwa_dzielnicy_punkty_trasy
entry_nazwa_przystanku_punkty_trasy = ttk.Combobox(tab_punkty_trasy,textvariable=nazwa_przystanku_punkty_trasy,state="readonly",postcommand=change_nazwa_przystanku)
combo_nazwa_przystanku_punkty_trasy = []
entry_nazwa_przystanku_punkty_trasy['values'] = combo_nazwa_przystanku_punkty_trasy
entry_nr_przystanku_na_trasie_punkty_trasy = ttk.Combobox(tab_punkty_trasy,textvariable=nr_przystanku_na_trasie_punkty_trasy,postcommand=change_nr_przystanku,state="readonly")
entry_liczba_minut_od_poprzedniego_punkty_trasy = Entry(tab_punkty_trasy,textvariable=liczba_minut_od_poprzedniego_punkty_trasy)
entry_search_punkty_trasy = Entry(tab_punkty_trasy,textvariable=search_punkty_trasy)
entry_sort_punkty_trasy = ttk.Combobox(tab_punkty_trasy,textvariable=sort_punkty_trasy,state="readonly")
combo_sort_punkty_trasy = db.fetch_sort_prompt('PUNKTY_TRASY')
entry_sort_punkty_trasy['values'] = combo_sort_punkty_trasy
entries.append(entry_nazwa_linii_punkty_trasy)
entries.append(entry_nazwa_dzielnicy_punkty_trasy)
entries.append(entry_nazwa_przystanku_punkty_trasy)
entries.append(entry_nr_przystanku_na_trasie_punkty_trasy)
entries.append(entry_liczba_minut_od_poprzedniego_punkty_trasy)
entries.append(entry_search_punkty_trasy)
entries.append(entry_sort_punkty_trasy)
entries_global.append(entries)

#TAB PRZYSTANKI
entries=[]
nazwa_przystanku_przystanki = StringVar()
nazwa_dzielnicy_przystanki = StringVar()
zadaszenie_przystanki = StringVar()
search_przystanki = StringVar()
sort_przystanki = StringVar()
entry_nazwa_przystanku_przystanki = Entry(tab_przystanki,textvariable = nazwa_przystanku_przystanki)
entry_nazwa_dzielnicy_przystanki = ttk.Combobox(tab_przystanki,textvariable = nazwa_dzielnicy_przystanki,state="readonly",postcommand=change_nazwa_dzielnicy)
combo_nazwa_dzielnicy_przystanki = [] #UZUPELNIJ Z DB.FETCH()
entry_nazwa_dzielnicy_przystanki['values'] = combo_nazwa_dzielnicy_przystanki
entry_zadaszenie_przystanki = ttk.Combobox(tab_przystanki,textvariable = zadaszenie_przystanki,state="readonly")
entry_zadaszenie_przystanki['values'] = ('TAK','NIE')
entry_search_przystanki = Entry(tab_przystanki,textvariable=search_przystanki)
entry_sort_przystanki = ttk.Combobox(tab_przystanki,textvariable=sort_przystanki,state="readonly")
combo_sort_przystanki = db.fetch_sort_prompt('PRZYSTANKI')
entry_sort_przystanki['values'] = combo_sort_przystanki

entries.append(entry_nazwa_przystanku_przystanki)
entries.append(entry_nazwa_dzielnicy_przystanki)
entries.append(entry_zadaszenie_przystanki)
entries.append(entry_search_przystanki)
entries.append(entry_sort_przystanki)
entries_global.append(entries)
#TAB DZIELNICE
entries=[]
nazwa_dzielnice = StringVar()
liczba_mieszkancow_dzielnice = StringVar()
czy_bezpieczna_dzielnice = StringVar()
search_dzielnice = StringVar()
sort_dzielnice = StringVar()
entry_nazwa_dzielnice = Entry(tab_dzielnice,textvariable=nazwa_dzielnice)
entry_liczba_mieszkancow_dzielnice = Entry(tab_dzielnice,textvariable=liczba_mieszkancow_dzielnice)
entry_czy_bezpieczna_dzielnice = ttk.Combobox(tab_dzielnice,textvariable=czy_bezpieczna_dzielnice,state="readonly")
entry_czy_bezpieczna_dzielnice['values'] = ('TAK','NIE')
entry_search_dzielnice = Entry(tab_dzielnice,textvariable=search_dzielnice)
entry_sort_dzielnice = ttk.Combobox(tab_dzielnice,textvariable=sort_dzielnice,state="readonly")
combo_sort_dzielnice = db.fetch_sort_prompt('DZIELNICE')
entry_sort_dzielnice['values'] = combo_sort_dzielnice

entries.append(entry_nazwa_dzielnice)
entries.append(entry_liczba_mieszkancow_dzielnice)
entries.append(entry_czy_bezpieczna_dzielnice)
entries.append(entry_search_dzielnice)
entries.append(entry_sort_dzielnice)
entries_global.append(entries)
entries=[]


#buttons/przyciski
#TAB PRZEJAZDY
buttons_global = []
buttons = []
button_filter_przejazdy = Button(tab_przejazdy,text='Zastosuj filtry',command=filter_przejazdy)
buttons.append(button_filter_przejazdy)
button_add_przejazdy = Button(tab_przejazdy,text='Dodaj przejazd',command=add_przejazdy)
buttons.append(button_add_przejazdy)
button_remove_przejazdy = Button(tab_przejazdy,text ='Usuń przejazd',command=remove_przejazdy)
buttons.append(button_remove_przejazdy)
button_update_przejazdy = Button(tab_przejazdy,text ='Modyfikuj przejazd',command=update_przejazdy)
buttons.append(button_update_przejazdy)
button_clear_przejazdy = Button(tab_przejazdy,text ='Wyczyść pola',command=clear_przejazdy)
buttons.append(button_clear_przejazdy)
button_details_przejazdy = Button(tab_przejazdy,text='Szczegóły przejazdu',command=detail_przejazdy)
buttons.append(button_details_przejazdy)
buttons_global.append(buttons)

buttons = []
#TAB KIEROWCY
buttons = []
button_filter_kierowcy = Button(tab_kierowcy,text='Zastosuj filtry',command=filter_kierowcy)
buttons.append(button_filter_kierowcy)
button_add_kierowcy = Button(tab_kierowcy,text='Dodaj kierowcę',command=add_kierowcy)
buttons.append(button_add_kierowcy)
button_remove_kierowcy = Button(tab_kierowcy,text ='Usuń kierowcę',command=remove_kierowcy)
buttons.append(button_remove_kierowcy)
button_update_kierowcy = Button(tab_kierowcy,text ='Modyfikuj kierowcę',command=update_kierowcy)
buttons.append(button_update_kierowcy)
button_clear_kierowcy = Button(tab_kierowcy,text ='Wyczyść pola',command=clear_kierowcy)
buttons.append(button_clear_kierowcy)
button_details_kierowcy = Button(tab_kierowcy,text='Szczegóły',command=detail_kierowcy)
buttons.append(button_details_kierowcy)
buttons_global.append(buttons)

buttons = []
#TAB ULGI
buttons = []
button_filter_ulgi = Button(tab_ulgi,text='Zastosuj filtry',command=filter_ulgi)
buttons.append(button_filter_ulgi)
button_add_ulgi = Button(tab_ulgi,text='Dodaj ulgę',command=add_ulgi)
buttons.append(button_add_ulgi)
button_remove_ulgi = Button(tab_ulgi,text ='Usuń ulgę',command=remove_ulgi)
buttons.append(button_remove_ulgi)
button_update_ulgi = Button(tab_ulgi,text ='Modyfikuj ulgę',command=update_ulgi)
buttons.append(button_update_ulgi)
button_clear_ulgi = Button(tab_ulgi,text ='Wyczyść pola',command=clear_ulgi)
buttons.append(button_clear_ulgi)
buttons_global.append(buttons)

buttons = []
#TAB BILETY
buttons = []
button_filter_bilety = Button(tab_bilety,text='Zastosuj filtry',command=filter_bilety)
buttons.append(button_filter_bilety)
button_add_bilety = Button(tab_bilety,text='Dodaj bilet',command=add_bilety)
buttons.append(button_add_bilety)
button_remove_bilety = Button(tab_bilety,text ='Usuń bilet',command=remove_bilety)
buttons.append(button_remove_bilety)
button_update_bilety = Button(tab_bilety,text ='Modyfikuj bilet',command=update_bilety)
buttons.append(button_update_bilety)
button_clear_bilety = Button(tab_bilety,text ='Wyczyść pola',command=clear_bilety)
buttons.append(button_clear_bilety)
buttons_global.append(buttons)

buttons = []
#TAB POJAZDY
buttons = []
button_filter_pojazdy = Button(tab_pojazdy,text='Zastosuj filtry',command=filter_pojazdy)
buttons.append(button_filter_pojazdy)
button_add_pojazdy = Button(tab_pojazdy,text='Dodaj pojazd',command=add_pojazdy)
buttons.append(button_add_pojazdy)
button_remove_pojazdy = Button(tab_pojazdy,text ='Usuń pojazd',command=remove_pojazdy)
buttons.append(button_remove_pojazdy)
button_update_pojazdy = Button(tab_pojazdy,text ='Modyfikuj pojazd',command=update_pojazdy)
buttons.append(button_update_pojazdy)
button_clear_pojazdy = Button(tab_pojazdy,text ='Wyczyść pola',command=clear_pojazdy)
buttons.append(button_clear_pojazdy)
button_details_pojazdy = Button(tab_pojazdy,text='Szczegóły',command=detail_pojazdy)
buttons.append(button_details_pojazdy)
buttons_global.append(buttons)

buttons = []
#TAB MODELE
buttons = []
button_filter_modele = Button(tab_modele,text='Zastosuj filtry',command=filter_modele)
buttons.append(button_filter_modele)
button_add_modele = Button(tab_modele,text='Dodaj model',command=add_modele)
buttons.append(button_add_modele)
button_remove_modele = Button(tab_modele,text ='Usuń model',command=remove_modele)
buttons.append(button_remove_modele)
button_update_modele = Button(tab_modele,text ='Modyfikuj model',command=update_modele)
buttons.append(button_update_modele)
button_clear_modele = Button(tab_modele,text ='Wyczyść pola',command=clear_modele)
buttons.append(button_clear_modele)
buttons_global.append(buttons)

buttons = []
#TAB PRODUCENCI
buttons = []
button_filter_producenci = Button(tab_producenci,text='Zastosuj filtry',command=filter_producenci)
buttons.append(button_filter_producenci)
button_add_producenci = Button(tab_producenci,text='Dodaj producenta',command=add_producenci)
buttons.append(button_add_producenci)
button_remove_producenci = Button(tab_producenci,text ='Usuń producenta',command=remove_producenci)
buttons.append(button_remove_producenci)
button_update_producenci = Button(tab_producenci,text ='Modyfikuj producenta',command=update_producenci)
buttons.append(button_update_producenci)
button_clear_producenci = Button(tab_producenci,text ='Wyczyść pola',command=clear_producenci)
buttons.append(button_clear_producenci)
buttons_global.append(buttons)

buttons = []
#TAB LINIE
buttons = []
button_filter_linie = Button(tab_linie,text='Zastosuj filtry',command=filter_linie)
buttons.append(button_filter_linie)
button_add_linie = Button(tab_linie,text='Dodaj linię',command=add_linie)
buttons.append(button_add_linie)
button_remove_linie = Button(tab_linie,text ='Usuń linię',command=remove_linie)
buttons.append(button_remove_linie)
button_update_linie = Button(tab_linie,text ='Modyfikuj linię',command=update_linie)
buttons.append(button_update_linie)
button_clear_linie = Button(tab_linie,text ='Wyczyść pola',command=clear_linie)
buttons.append(button_clear_linie)
buttons_global.append(buttons)

buttons = []
#TAB PUNKTY TRASY
buttons = []
button_filter_punkty_trasy = Button(tab_punkty_trasy,text='Zastosuj filtry',command=filter_punkty_trasy)
buttons.append(button_filter_punkty_trasy)
button_add_punkty_trasy = Button(tab_punkty_trasy,text='Dodaj punkt trasy',command=add_punkty_trasy)
buttons.append(button_add_punkty_trasy)
button_remove_punkty_trasy = Button(tab_punkty_trasy,text ='Usuń punkt trasy',command=remove_punkty_trasy)
buttons.append(button_remove_punkty_trasy)
button_update_punkty_trasy = Button(tab_punkty_trasy,text ='Modyfikuj punkt trasy',command=update_punkty_trasy)
buttons.append(button_update_punkty_trasy)
button_clear_punkty_trasy = Button(tab_punkty_trasy,text ='Wyczyść pola',command=clear_punkty_trasy)
buttons.append(button_clear_punkty_trasy)
buttons_global.append(buttons)

buttons = []
#TAB PRZYSTANKI
buttons = []
button_filter_przystanki = Button(tab_przystanki,text='Zastosuj filtry',command=filter_przystanki)
buttons.append(button_filter_przystanki)
button_add_przystanki = Button(tab_przystanki,text='Dodaj przystanek',command=add_przystanki)
buttons.append(button_add_przystanki)
button_remove_przystanki = Button(tab_przystanki,text ='Usuń przystanek',command=remove_przystanki)
buttons.append(button_remove_przystanki)
button_update_przystanki = Button(tab_przystanki,text ='Modyfikuj przystanek',command=update_przystanki)
buttons.append(button_update_przystanki)
button_clear_przystanki = Button(tab_przystanki,text ='Wyczyść pola',command=clear_przystanki)
buttons.append(button_clear_przystanki)
buttons_global.append(buttons)

buttons = []
#TAB DZIELNICE
buttons = []
button_filter_dzielnice = Button(tab_dzielnice,text='Zastosuj filtry',command=filter_dzielnice)
buttons.append(button_filter_dzielnice)
button_add_dzielnice = Button(tab_dzielnice,text='Dodaj dzielnicę',command=add_dzielnice)
buttons.append(button_add_dzielnice)
button_remove_dzielnice = Button(tab_dzielnice,text ='Usuń dzielnicę',command=remove_dzielnice)
buttons.append(button_remove_dzielnice)
button_update_dzielnice = Button(tab_dzielnice,text ='Modyfikuj dzielnicę',command=update_dzielnice)
buttons.append(button_update_dzielnice)
button_clear_dzielnice = Button(tab_dzielnice,text ='Wyczyść pola',command=clear_dzielnice)
buttons.append(button_clear_dzielnice)
buttons_global.append(buttons)

buttons = []
#tk_trees/tabelki
#TABS PRZEJAZDY
trees = []
columns = []

tree_przejazdy = ttk.Treeview(tab_przejazdy)  #TAB PRZEJAZDY
kolumny_przejazdy = ('NAZWA LINII','GODZINA STARTU','MINUTA STARTU','ID KIEROWCY','REJESTRACJA POJAZDU')
tree_przejazdy.bind('<<TreeviewSelect>>',select_item_przejazdy)
trees.append(tree_przejazdy)
columns.append(kolumny_przejazdy)

tree_kierowcy = ttk.Treeview(tab_kierowcy)  #TAB KIEROWCY
kolumny_kierowcy = ('ID PRACOWNIKA','NAZWISKO','DATA URODZENIA','IMIĘ','NR TEL')
tree_kierowcy.bind('<<TreeviewSelect>>',select_item_kierowcy)
trees.append(tree_kierowcy)
columns.append(kolumny_kierowcy)

tree_ulgi = ttk.Treeview(tab_ulgi)  #TAB ULGI
kolumny_ulgi = ('RODZAJ','WIELKOŚĆ ZNIŻKI')
tree_ulgi.bind('<<TreeviewSelect>>',select_item_ulgi)
trees.append(tree_ulgi)
columns.append(kolumny_ulgi)

tree_bilety = ttk.Treeview(tab_bilety)  #TAB BILETY
kolumny_bilety = ('MAKSYMALNA L.  MINUT PRZEJAZDU','CENA (ZŁ)')
tree_bilety.bind('<<TreeviewSelect>>',select_item_bilety)
trees.append(tree_bilety)
columns.append(kolumny_bilety)

tree_pojazdy = ttk.Treeview(tab_pojazdy)  #TAB POJAZDY
kolumny_pojazdy = ('REJESTRACJA','NAZWA MODELU','PRODUCENT','STAN TECHNICZNY')
tree_pojazdy.bind('<<TreeviewSelect>>',select_item_pojazdy)
trees.append(tree_pojazdy)
columns.append(kolumny_pojazdy)

tree_modele = ttk.Treeview(tab_modele)  #TAB MODELE
kolumny_modele = ('NAZWA MODELU','PRODUCENT','LICZBA KONII','KOSZT (ZŁ)')
tree_modele.bind('<<TreeviewSelect>>',select_item_modele)
trees.append(tree_modele)
columns.append(kolumny_modele)

tree_producenci = ttk.Treeview(tab_producenci)  #TAB PRODUCENCI
kolumny_producenci = ('NAZWA','DATA ROZPOCZĘCIA DZIAŁALNOŚCI','KRAJ POCHODZENIA')
tree_producenci.bind('<<TreeviewSelect>>',select_item_producenci)
trees.append(tree_producenci)
columns.append(kolumny_producenci)

tree_linie = ttk.Treeview(tab_linie)  #TAB LINIE
kolumny_linie = ('NAZWA','KOLOR')
tree_linie.bind('<<TreeviewSelect>>',select_item_linie)
trees.append(tree_linie)
columns.append(kolumny_linie)

tree_punkty_trasy = ttk.Treeview(tab_punkty_trasy)  #TAB PUNKTY TRASY
kolumny_punkty_trasy = ('NAZWA LINII','NAZWA DZIELNICY','NAZWA PRZYSTANKU','NR PRZYSTANKU NA TRASIE','L. MINUT OD POPRZEDNIEGO')
tree_punkty_trasy.bind('<<TreeviewSelect>>',select_item_punkty_trasy)
trees.append(tree_punkty_trasy)
columns.append(kolumny_punkty_trasy)

tree_przystanki = ttk.Treeview(tab_przystanki)  #TAB PRZYSTANKI
kolumny_przystanki = ('NAZWA PRZYSTANKU','NAZWA DZIELNICY','ZADASZENIE')
tree_przystanki.bind('<<TreeviewSelect>>',select_item_przystanki)
trees.append(tree_przystanki)
columns.append(kolumny_przystanki)

tree_dzielnice = ttk.Treeview(tab_dzielnice)  #TAB DZIELNICE
kolumny_dzielnice = ('NAZWA','LICZBA MIESZKAŃCÓW','CZY BEZPIECZNA')
tree_dzielnice.bind('<<TreeviewSelect>>',select_item_dzielnice)
trees.append(tree_dzielnice)
columns.append(kolumny_dzielnice)

#custmization
style = ttk.Style()
style.configure(".")
font_params = ("Verdana", 10, 'bold')
style.configure("Treeview.Heading", foreground='black',font = font_params)

change_tabs(tabs,'gray11')

for l,b in zip(labels_global,buttons_global):
    change_widgets(l,'white','gray11',font_params)
    change_buttons(b,'black','light blue',font_params)

for t,c in zip(trees,columns):
    change_tree(t, c, 10)

upwidgets = []
for e,l,b in zip(entries_global,labels_global,buttons_global):
    sort_entry = e.pop()
    search_entry = e.pop()
    sort_label = l.pop()
    search_label = l.pop()
    filter_button = b.pop(0)
    upwidgets.append([search_label,search_entry,sort_label,sort_entry,filter_button])

for t,l,e,b,u in zip(trees,labels_global,entries_global,buttons_global,upwidgets):
    gridder(t,l,e,b,u,3,3)


#PANEL UZYTKOWNIKA ----------------------------------------------------------------------------------------------------------------------------------------



def szukaj_trase():
    problem = 0
    problem_description = ""
    rodzaj_znizki = entry_rodzaj_ulgi_wyszukaj_trase.get()
    dzielnica_odjazdu = entry_dzielnica_odjazdu_wyszukaj_trase.get()
    dzielnica_docelowa = entry_dzielnica_docelowa_wyszukaj_trase.get()
    po_czasie = entry_odjazd_po_godzinie_wyszukaj_trase.get()
    try:
        czas = po_czasie.split(':')
        po_godzinie = int(czas[0])
        po_minucie = int(czas[1])

    except:
        problem = 1
        problem_description = problem_description + "Odjazd po godzinie powinien mieć format godzina:minuta np. 15:10\n"
        for row in tree_wyszukaj_trase.get_children():
            tree_wyszukaj_trase.delete(row)
    if len(rodzaj_znizki)==0:
        problem = 1
        problem_description = problem_description + "Proszę podać rodzaj ulgi\n"
    if dzielnica_odjazdu == dzielnica_docelowa and len(dzielnica_odjazdu)!=0:
        problem = 1
        problem_description = problem_description + "Podano te same dzielnice\n"
    if  len(dzielnica_docelowa)==0 or len(dzielnica_odjazdu)==0:
        problem=1
        problem_description = problem_description + "Proszę podać nazwy dzielnic"
    if problem == 1:
        messagebox.showerror('Uwaga!',problem_description)
        return

    try:


        rows = db.fetch_polecenie(f'''select distinct nazwa_linii from
        (select * from punkty_trasy a
        where 
        (select nr_przystanku_na_trasie from punkty_trasy
        where nazwa_linii=a.nazwa_linii and nazwa_dzielnicy='{dzielnica_docelowa}' order by nr_przystanku_na_trasie desc fetch first 1 row only)
        >(select nr_przystanku_na_trasie from punkty_trasy where nazwa_linii=a.nazwa_linii and nazwa_dzielnicy='{dzielnica_odjazdu}' order by nr_przystanku_na_trasie asc fetch first 1 row only)
        ) p1 where p1.nazwa_linii in(select nazwa_linii from przejazdy where godzina_startu>{po_godzinie}
        or (godzina_startu={po_godzinie} and minuta_startu>{po_minucie}))''')
        wyjsciowa_tablica_tablic =[]
        if len(rows) == 0:
            messagebox.showerror('Przykro nam!','Nie znaleziono połączenia')
        for i in rows:
            docelowa_linia=i[0]
            rows1 = db.fetch_polecenie(
            f'''select (select nr_przystanku_na_trasie from punkty_trasy where nazwa_linii='{docelowa_linia}' and nazwa_dzielnicy='{dzielnica_odjazdu}' order by nr_przystanku_na_trasie
            asc fetch first 1 row only) as docelowa,(select nr_przystanku_na_trasie from punkty_trasy where nazwa_linii='{docelowa_linia}' and nazwa_dzielnicy='{dzielnica_docelowa}' order by nr_przystanku_na_trasie desc
            fetch first 1 row only) as odjazdu from dual''')
            nr_odjazdu = rows1[0][0]
            nr_docelowej = rows1[0][1]
            rows1 = db.fetch_polecenie(f'''select nazwa_przystanku from punkty_trasy where nazwa_linii='{docelowa_linia}' and
            nr_przystanku_na_trasie between {nr_odjazdu} and {nr_docelowej} order by nr_przystanku_na_trasie''')
            przystanek_odjazdu = rows1[0][0]
            przystanek_docelowy = rows1[len(rows1)-1][0]
            rows1 = db.fetch_polecenie(f'''select sum(liczba_minut_od_poprzedniego) from
            punkty_trasy where nazwa_linii='{docelowa_linia}' and nr_przystanku_na_trasie>{nr_odjazdu} and nr_przystanku_na_trasie<={nr_docelowej}''')
            liczba_minut=rows1[0][0]
            rows1 = db.fetch_polecenie(f'''select godzina_startu,minuta_startu from przejazdy where nazwa_linii='{docelowa_linia}' and (godzina_startu>{po_godzinie} or
            (godzina_startu={po_godzinie} and minuta_startu>{po_minucie})) fetch first 1 row only''')
            godzina_startu = rows1[0][0]
            minuta_startu = rows1[0][1]
            rows1 = db.fetch_polecenie(f'''select sum(liczba_minut_od_poprzedniego) from punkty_trasy where nazwa_linii='{docelowa_linia}' and nr_przystanku_na_trasie<={nr_odjazdu} fetch first 1 row only''')
            l_minut = int(rows1[0][0])%60
            l_godzin = int(rows1[0][0])//60

            aktualna_minuta = minuta_startu
            aktualna_godzina = godzina_startu

            l_godzin = (l_minut + aktualna_minuta) // 60 + l_godzin
            aktualna_minuta = (l_minut + aktualna_minuta) % 60

            nowa_godzina = aktualna_godzina + l_godzin
            if nowa_godzina > 24:
                nowa_godzina = nowa_godzina - 24
            dostaw_godzine = ""
            dostaw_minute=""
            if len(str(nowa_godzina))<2:
                dostaw_godzine = "0"
            if len(str(aktualna_minuta)) < 2:
                dostaw_minute = "0"
            if nowa_godzina>23:
                return
            nowa_godzina = dostaw_godzine + str(nowa_godzina) + ':' + dostaw_minute + str(aktualna_minuta)
            rows1 = db.fetch_polecenie(f'''select case
                                when max_minuty_przejazdu-{liczba_minut}>0 then cena_zl
                                else (select max(cena_zl) from bilety)
                                end as ile
                                from bilety order by ile fetch first 1 row only''')
            cena_biletu = rows1[0][0]

            # rows1 = db.fetch_polecenie(f'''select procent_znizki from ulgi where rodzaj='{rodzaj_znizki}' ''')
            #
            # znizka = rows1[0][0]
            #
            # cena_biletu = int(cena_biletu)*(1.0-float(znizka))
            # cena_biletu = round(cena_biletu,2)
            cena_biletu = db.wylicz_cene(rodzaj_znizki,cena_biletu)


            wyjsciowa_tablica = (docelowa_linia,przystanek_odjazdu,przystanek_docelowy,nowa_godzina,str(liczba_minut) + ' minut',str(cena_biletu) + ' zł')
            wyjsciowa_tablica_tablic.append(wyjsciowa_tablica)
        for row in tree_wyszukaj_trase.get_children():
            tree_wyszukaj_trase.delete(row)
        for row in wyjsciowa_tablica_tablic:
            tree_wyszukaj_trase.insert("", END, values=row)
    except:
        for row in tree_wyszukaj_trase.get_children():
            tree_wyszukaj_trase.delete(row)


def zmien_motyw():



    if button_motyw_wyszukaj_trase['text'] == 'WŁĄCZ MOTYW NOCNY':
        label_obrazek['bg'] = 'gray11'
        photo['file'] = 'motyw_ciemny.png'
        button_motyw_wyszukaj_trase['text'] = 'WŁĄCZ MOTYW DZIENNY'
        tab_wyszukaj_trase.configure(bg='gray11')
        label_niewidzialny.configure(bg='gray11')
        change_widgets(labels_wyszukaj_trase, 'white', 'gray11', font_params)
        change_buttons(buttons_wyszukaj_trase, 'black', 'light blue', font_params)
    else:
        label_obrazek['bg'] = 'powder blue'
        photo['file'] = 'motyw_jasny.png'
        button_motyw_wyszukaj_trase['text'] = 'WŁĄCZ MOTYW NOCNY'
        tab_wyszukaj_trase.configure(bg='powder blue')
        label_niewidzialny.configure(bg='powder blue')
        change_widgets(labels_wyszukaj_trase, 'black', 'powder blue', font_params)
        change_buttons(buttons_wyszukaj_trase, 'white', 'brown4', font_params)
def select_item_wyszukaj_trase(event):
    pass
#Panel wyszukaj_trase
#labels
labels_wyszukaj_trase = []
label_pusty_wyszukaj_trase = Label(tab_wyszukaj_trase,bg='gray11',width=20)
label_dzielnica_odjazdu_wyszukaj_trase = Label(tab_wyszukaj_trase,text='DZIELNICA ODJAZDU:')
label_dzielnica_docelowa_wyszukaj_trase = Label(tab_wyszukaj_trase,text='DZIELNICA DOCELOWA:')
label_odjazd_po_godzinie_wyszukaj_trase = Label(tab_wyszukaj_trase,text='ODJAZD PO (GODZINA:MINUTA):')
label_rodzaj_ulgi_wyszukaj_trase = Label(tab_wyszukaj_trase,text = 'RODZAJ ULGI:')

labels_wyszukaj_trase.append(label_dzielnica_odjazdu_wyszukaj_trase)
labels_wyszukaj_trase.append(label_dzielnica_docelowa_wyszukaj_trase)
labels_wyszukaj_trase.append(label_odjazd_po_godzinie_wyszukaj_trase)
labels_wyszukaj_trase.append(label_rodzaj_ulgi_wyszukaj_trase)

#entries
entries_wyszukaj_trase = []
dzielnica_odjazdu_wyszukaj_trase = StringVar()
entry_dzielnica_odjazdu_wyszukaj_trase = ttk.Combobox(tab_wyszukaj_trase,textvariable = dzielnica_odjazdu_wyszukaj_trase,state='normal',postcommand=change_dzielnice_wyszukaj_trase)
combo_dzielnica_odjazdu_wyszukaj_trase = []
entry_dzielnica_odjazdu_wyszukaj_trase['values'] = combo_dzielnica_odjazdu_wyszukaj_trase
entries_wyszukaj_trase.append(entry_dzielnica_odjazdu_wyszukaj_trase)
dzielnica_docelowa_wyszukaj_trase = StringVar()
entry_dzielnica_docelowa_wyszukaj_trase = ttk.Combobox(tab_wyszukaj_trase,textvariable = dzielnica_docelowa_wyszukaj_trase,state='normal',postcommand=change_dzielnice_wyszukaj_trase)
combo_dzielnica_docelowa_wyszukaj_trase = []
entry_dzielnica_docelowa_wyszukaj_trase['values'] = combo_dzielnica_docelowa_wyszukaj_trase
entries_wyszukaj_trase.append(entry_dzielnica_docelowa_wyszukaj_trase)
odjazd_po_godzinie_wyszukaj_trase = StringVar()
entry_odjazd_po_godzinie_wyszukaj_trase = Entry(tab_wyszukaj_trase,textvariable = odjazd_po_godzinie_wyszukaj_trase)
entries_wyszukaj_trase.append(entry_odjazd_po_godzinie_wyszukaj_trase)
rodzaj_ulgi_wyszukaj_trase = StringVar()
entry_rodzaj_ulgi_wyszukaj_trase = ttk.Combobox(tab_wyszukaj_trase,textvariable = rodzaj_ulgi_wyszukaj_trase,state='readonly',postcommand=change_rodzaj_ulgi)
combo_rodzaj_ulgi_wyszukaj_trase = []
entry_rodzaj_ulgi_wyszukaj_trase['values'] = combo_rodzaj_ulgi_wyszukaj_trase
entries_wyszukaj_trase.append(entry_rodzaj_ulgi_wyszukaj_trase)
#buttons
buttons_wyszukaj_trase = []
button_szukaj_wyszukaj_trase = Button(tab_wyszukaj_trase,text='SZUKAJ PRZEJAZDU',command=szukaj_trase)
button_motyw_wyszukaj_trase = Button(tab_wyszukaj_trase,text='WŁĄCZ MOTYW DZIENNY',command=zmien_motyw)
buttons_wyszukaj_trase.append(button_szukaj_wyszukaj_trase)
buttons_wyszukaj_trase.append(button_motyw_wyszukaj_trase)
#tree
tree_wyszukaj_trase = ttk.Treeview(tab_wyszukaj_trase)  #TAB PRZEJAZDY
kolumny_wyszukaj_trase = ('NAZWA LINII','PRZYSTANEK STARTOWY','PRZYSTANEK KOŃCOWY','GODZINA ODJAZDU','CZAS PODRÓŻY','CENA (Z ULGĄ)')
tree_wyszukaj_trase.bind('<<TreeviewSelect>>',select_item_wyszukaj_trase)
change_tree(tree_wyszukaj_trase, kolumny_wyszukaj_trase, 182)
#grids
change_widgets(labels_wyszukaj_trase, 'white', 'gray11', font_params)
change_buttons(buttons_wyszukaj_trase, 'black', 'light blue', font_params)
#label-niewidzialne
label_niewidzialny = Label(tab_wyszukaj_trase,bg='gray11',width=30,height=3)
label_niewidzialny.grid(column=0,row=0)
for i,le in enumerate(zip(labels_wyszukaj_trase,entries_wyszukaj_trase)):
    le[0].grid(column=1,row=i+1,padx=5,pady=5)
    le[1].grid(column=2,row=i+1,padx=5,pady=5)

button_szukaj_wyszukaj_trase.grid(column=3,row=1,rowspan=4)
button_motyw_wyszukaj_trase.grid(column=4,row=0)
tree_wyszukaj_trase.grid(column=1,row=5,columnspan=3,padx=5,pady=5)


photo = PhotoImage(file="motyw_ciemny.png")
label_obrazek = Label(tab_wyszukaj_trase, image=photo, bg='gray11')
label_obrazek.grid(column=2,row=7)





populate()

root.mainloop()





