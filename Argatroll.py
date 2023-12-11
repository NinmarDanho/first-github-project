import felhantering
import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox
from datetime import datetime


class Spel:

    """ Denna Klass skapar hela spelet."""

    def __init__(self):
        self.bradet = []
        self.antal_forsok = 5
        self.antal_troll = 0
        self.start_tid = 0
        self.spel_tid = 0
        self.root = tk.Tk()
        self.root.title("Arga troll")

        self.spel_frame = tk.Frame()
        self.bradet_frame = tk.Frame()

        self.antal_forsok_output = tk.Label()
        self.spelare_frame = tk.Frame()

    def start_frame(self):
        """ Här skapas det ett Start Frame där flera labels läggs till t.ex storlek_label
        som visas i början av spelet, weight=1 är för att fördela den tomma arean på de olika raderna och kolonnerna """

        start_frame = tk.Frame(self.root, width=500, height=500)
        start_frame.grid_propagate(False)
        start_frame.grid(row=0, column=0)
        start_frame.grid_rowconfigure(0, weight=1)
        start_frame.grid_rowconfigure(3, weight=1)
        start_frame.grid_columnconfigure(0, weight=1)

        storlek_label = tk.Label(start_frame, text="Hej! och välkommen till Arga troll spelet:\n Spelet går ut på att ställa trollen på giltiga positioner\ndär trollen inte får vara i samma rad kolonn eller diagonal.\n Du har fem försök på dig att lösa brädet.\n\nVar vänlig och välj brädets storlek:")
        storlek_label.grid(row=0, column=0, sticky="s", pady=10)

        storlek_inmatning = tk.Entry(start_frame)
        storlek_inmatning.grid(row=1, column=0)

        start_knapp = tk.Button(start_frame, text="Börja spelet", command=lambda: self.borja_spelet(storlek_inmatning.get()))
        start_knapp.grid(row=3, column=0, sticky="n", pady=10)

        start_frame.tkraise()

        self.root.mainloop()

    def borja_spelet(self, storlek):
        """Denna metod körs när spelaren trycker på "börja spelet" knappen. Den kontrollerar
        inmatningen på brädets storlek och om inmatningen är giltig då tar den strttiden
        och skapar brädet annars får användaren ett felmeddelande."""
        if felhantering.storlek_validera(storlek) == True:
            self.start_tid = datetime.now()
            self.antal_troll = int(storlek)
            self.visa_spel_framet()
            self.skapa_bradet(storlek)
        else:
            tk.messagebox.showwarning(title="Felinmatning", message="brädets storlek ska vara ett tal som är minst lika med 4, var vänlig och försök igen!")

    def visa_spel_framet(self):
        """Här skapas det ett "spel_frame" som innhåller "brädet_frame", "info_fram" och "vinn_frame" dvs här ska
        spelaren kunna placera trollen (i brädet_frame) samt se antalet försök som är kvar (i info_frame) och ifall
        spelaren vinner så ska den även få ett gratiis medelande i "vinn_frame" som placeras över "info_frame" """
        self.spel_frame = tk.Frame(self.root, width=500)
        self.spel_frame.grid(row=0, column=0)

        self.bradet_frame = tk.Frame(self.spel_frame)
        self.bradet_frame.grid(row=0, column=0)

        info_frame = tk.Frame(self.spel_frame, width=500, height=100)
        info_frame.grid(row=1, column=0)
        info_frame.grid_propagate(False)

        for grid_cell in range(0, 2):  # hantera tomm area
            info_frame.grid_rowconfigure(grid_cell, weight=1)
            info_frame.grid_columnconfigure(grid_cell, weight=1)

        antal_forsok_label = tk.Label(info_frame, text="Antal försök kvar")
        antal_forsok_label.grid(row=0, column=0, sticky="s")

        self.antal_forsok_output = tk.Label(info_frame, text=self.antal_forsok)
        self.antal_forsok_output.grid(row=1, column=0, sticky="n")

        avsluta_spelet_knapp = tk.Button(info_frame, text="Avsluta spelet", command=self.avslut_spelet)
        avsluta_spelet_knapp.grid(row=0, column=1, rowspan=2)

        self.spel_frame.tkraise()

    def skapa_bradet(self, storlek):
        """Denna metod skapar brädet baserat på användarens val av storlek."""
        for rad in range(int(storlek)):
            bradet_rad = []
            for kol in range(int(storlek)):
                bradet_cell = Cell(False, self.bradet_frame)
                bradet_cell.label.grid(row=rad, column=kol)
                bradet_cell.label.bind('<Button-1>', lambda event, rad=rad, kol=kol: self.byt_bild(rad, kol))
                bradet_rad.append(bradet_cell)
            self.bradet.append(bradet_rad)

    def byt_bild(self, rad, kol):
        """Denna metod körs när användaren trycker på en ruta i brädet. Den byter bild från gräs till troll när
        troll positionen är giltig. Om troll positionen däremot inte är giltig så minskas antalet försök kvar med 1 och
        till slut när användaren har använt alla sina försök så dycker "Game over" meddelandet upp. Dessutom
        om rutan redan har en troll så byts bilden från troll till gräs med hjälp av Denna metod."""
        if self.bradet[rad][kol].har_troll == False:
            if self.validera_troll_position(rad, kol) == True:
                self.bradet[rad][kol].har_troll = True
                self.bradet[rad][kol].visa_troll()
                self.antal_troll -= 1
                if self.antal_troll == 0:  # Spelaren har vunnit
                    slut_tid = datetime.now()
                    self.spel_tid = (slut_tid - self.start_tid).seconds
                    self.avbinda_alla_celler()
                    self.visa_vinn_frame()
            else:
                self.antal_forsok -= 1
                self.antal_forsok_output.configure(text=self.antal_forsok)
                if self.antal_forsok == 0:  # spelaren har förlurat
                    tk.messagebox.showwarning(title="Game over", message="Du har tyvärr använt alla dina försök, tryck på \"ok\" knappen för att se lösningen.")
                    rad = self.forsta_tom_rad()
                    for bradet_rad in range(rad + 1, len(self.bradet)):
                        self.tabort_alla_troll_fran_raden(bradet_rad)
                    self.los_bradet(rad)
                    self.avbinda_alla_celler()
        else:  # ångra troll position
            self.bradet[rad][kol].har_troll = False
            self.bradet[rad][kol].visa_gras()
            self.antal_troll += 1

    def validera_troll_position(self, rad, kol):
        """Denna funktion kontrollerar troll positionen och returnerar True ifall trollpositionen är giltig och False annars.
        Troll positionen är giltig om det inte finns en troll på samma rad, kolonn eller diagonal."""
        index_raknare = 0
        while index_raknare < len(self.bradet):
            if self.bradet[rad][index_raknare].har_troll == True:  # kontrollerar rad
                return False
            if self.bradet[index_raknare][kol].har_troll == True:  # kontrollerar kolonn
                return False
            if rad - index_raknare in range(len(self.bradet)) and kol - index_raknare in range(len(self.bradet)):  # kontrollera diagonaler
                if self.bradet[rad - index_raknare][kol - index_raknare].har_troll == True:  # kontrollerar vänster-topp
                    return False
            if rad - index_raknare in range(len(self.bradet)) and kol + index_raknare in range(len(self.bradet)):
                if self.bradet[rad - index_raknare][kol + index_raknare].har_troll == True:  # kontrollerar höger-topp
                    return False
            if rad + index_raknare in range(len(self.bradet)) and kol + index_raknare in range(len(self.bradet)):
                if self.bradet[rad + index_raknare][kol + index_raknare].har_troll == True:  # kontrolerar höger-botten
                    return False
            if rad + index_raknare in range(len(self.bradet)) and kol - index_raknare in range(len(self.bradet)):
                if self.bradet[rad + index_raknare][kol - index_raknare].har_troll == True:  # kontrollerar vänster-botten
                    return False
            index_raknare += 1
        return True

    def visa_vinn_frame(self):
        vinn_frame = tk.Frame(self.spel_frame, width=500, height=100)
        vinn_frame.grid(row=1, column=0)
        vinn_frame.pack_propagate(False)

        grattis_label = tk.Label(vinn_frame, text="Grattis, du har vunnit!!", font=("Arial", 15), fg="green")
        grattis_label.pack()

        namn_inmatning_label = tk.Label(vinn_frame, text="Var vänlig och skriv in ditt namn:")
        namn_inmatning_label.pack()
        namn_inmatning = tk.Entry(vinn_frame)
        namn_inmatning.pack()

        spara_knapp = tk.Button(vinn_frame, text="Spara", command=lambda: self.spara_spelare(namn_inmatning.get()))
        spara_knapp.pack()

        vinn_frame.tkraise()

    def forsta_tom_rad(self):
        """Denna metod hittar den första tomma raden och returnerar dess index för att "lösa_brädet" funktionen ska
        "veta" vart den ska börja"""
        for rad in range(len(self.bradet)):
            is_rad_har_troll = False
            for kol in range(len(self.bradet)):
                if self.bradet[rad][kol].har_troll == True:
                    is_rad_har_troll = True
                    break
            if is_rad_har_troll == False:
                return rad
    
    def los_bradet(self, rad):
        sist_kontrollerad_kolonn = [-1] * len(self.bradet)

        while rad < len(self.bradet):  # looper på rader
            kolonn = sist_kontrollerad_kolonn[rad] + 1
            accepterad_position = False

            while kolonn < len(self.bradet):  # looper på kolonner
                sist_kontrollerad_kolonn[rad] = kolonn

                if self.validera_troll_position(rad, kolonn):
                    accepterad_position = True
                    self.bradet[rad][kolonn].har_troll = True
                    self.bradet[rad][kolonn].visa_troll()
                    break
                else:
                    accepterad_position = False
                    kolonn += 1

            if accepterad_position:
                rad += 1
            else:
                sist_kontrollerad_kolonn[rad] = -1
                rad -= 1
                self.tabort_alla_troll_fran_raden(rad)


    def tabort_alla_troll_fran_raden(self, rad):
        """
        Denna metod sätter variablen "har_troll" till False för alla celler i given rad.
        """
        for rad_cell in self.bradet[rad]:
            rad_cell.har_troll = False
            rad_cell.visa_gras()

    def avbinda_alla_celler(self):
        """
        Denna metod gör så att man inte kan klicka på och ändra troll positionen efter att man har förlorat
        """
        for rad in range(len(self.bradet)):
            for kol in range(len(self.bradet)):
                self.bradet[rad][kol].label.unbind('<Button-1>')

    def spara_spelare(self, spelare_namn):
        """
        Denna metod hämtar alla spelare från den befintliga High_score.txt filen, därefter lägger den till
        den nya spelaren och sorterar spelarna efter tid och brädets storlek och sparar den igen på High_score.txt filen.
        Till slut så visar den High_score framet
        """
        if felhantering.validera_namn_inmatning(spelare_namn) == False:
            tk.messagebox.showwarning(title="Fel namn format", message="Namnfältet kan ej vara tomt!")
        else:
            spelare = Spelare(spelare_namn, len(self.bradet), self.spel_tid)
            high_score_fil = open('Highscore.txt', 'r')  # filens rader sparas i variabeln high-score
            rader_fran_fil = high_score_fil.readlines()
            high_score_fil.close()

            spelare_lista = self.skapa_spelare_fran_filen(rader_fran_fil)
            spelare_lista.append(spelare)
            spelare_lista.sort(key=lambda x: (int(x.storlek), int(x.speltid)))

            self.visa_highscore_frame()

            high_score_fil = open('Highscore.txt', 'w')

            rad = 0

            for spelare_i_lista in spelare_lista:
                high_score_fil.write(str(spelare_i_lista.namn))
                high_score_fil.write("\n")
                high_score_fil.write(str(spelare_i_lista.storlek))
                high_score_fil.write("\n")
                high_score_fil.write(str(spelare_i_lista.speltid))
                high_score_fil.write("\n")

                spelare_namn_label = tk.Label(self.spelare_frame, text=spelare_i_lista.namn)
                spelare_namn_label.grid(row=rad, column=0)

                spel_storlek = str(spelare_i_lista.storlek) + "X" + str(spelare_i_lista.storlek)
                spelare_storlek_label = tk.Label(self.spelare_frame, text=spel_storlek)
                spelare_storlek_label.grid(row=rad, column=1)

                spel_tid = self.formatera_tid(spelare_i_lista.speltid)
                spelare_tid_label = tk.Label(self.spelare_frame, text=spel_tid)
                spelare_tid_label.grid(row=rad, column=2)

                rad += 1

            high_score_fil.close()

    def skapa_spelare_fran_filen(self, rader_fran_fil):
        """
        Denna metod skapar spelare från den befintliga listan av spelare (tid, storlek, namn) och returnerar
        en lista av spelare "spelarna"
        """
        spelarna = []

        for fil_rad in range(len(rader_fran_fil) // 3):
            namn = rader_fran_fil[fil_rad * 3].strip()
            storlek = rader_fran_fil[fil_rad * 3 + 1].strip()
            speltid = rader_fran_fil[fil_rad * 3 + 2].strip()
            spelare = Spelare(namn, storlek, speltid)
            spelarna.append(spelare)

        return spelarna

    def visa_highscore_frame(self):
        """
        Här skapas det ett "Highscore Frame" som inneåller labels och en canvas där spelarna organsieras
        efter tid och brädets storlek och för att kunna se alla spelarna så skapas det scrollbarhet funktionen
        """
        self.spel_frame.grid_forget()

        highscore_frame = tk.Frame(self.root, width=500, height=500)
        highscore_frame.grid(row=0, column=0)
        highscore_frame.grid_propagate(False)

        highscore_label = tk.Label(highscore_frame, text="Highscore", font=("Arial", 20))
        highscore_label.grid(row=0, column=0, columnspan=3)

        namn_label = tk.Label(highscore_frame, text="Namn", font=("Arial", 15))
        namn_label.grid(row=1, column=0)

        storlek_label = tk.Label(highscore_frame, text="Storlek", font=("Arial", 15))
        storlek_label.grid(row=1, column=1)

        tid_label = tk.Label(highscore_frame, text="Tid", font=("Arial", 15))
        tid_label.grid(row=1, column=2)

        spelare_canvas = tk.Canvas(highscore_frame)
        spelare_canvas.grid(row=2, column=0, columnspan=3, sticky="news")

        self.spelare_frame = tk.Frame(spelare_canvas)

        for grid_kol in range(0, 3):
            highscore_frame.grid_columnconfigure(grid_kol, weight=1)
            self.spelare_frame.grid_columnconfigure(grid_kol, minsize=166)

        spelare_canvas.create_window(0, 0, window=self.spelare_frame, anchor='nw')

        spelare_rullningslist = tk.Scrollbar(highscore_frame, orient=tk.VERTICAL, command=spelare_canvas.yview)
        spelare_canvas.config(yscrollcommand=spelare_rullningslist.set)  # annars sparas ej scrolläget
        spelare_rullningslist.grid(row=2, column=3, sticky="ns")

        self.spelare_frame.bind("<Configure>", lambda event: uppdatera_rullningslist(event))  # scrollbars funktion

        def uppdatera_rullningslist(event):
            """
            En funktion för att uppdatera scrollläget
            """
            spelare_canvas.configure(scrollregion=spelare_canvas.bbox("all"))

        borja_om_knapp = tk.Button(highscore_frame, text="Börja om spelet", command=self.avslut_spelet)
        borja_om_knapp.grid(row=3, column=0, columnspan=3, pady=10)

        highscore_frame.tkraise()

    def formatera_tid(self, spel_tid):
        """
        Denna metod konverterar tiden från sekunder till en användarvänlig tidräkning.
        """
        spel_tid = int(spel_tid)
        timmar = spel_tid // 3600
        minuter = (spel_tid // 60) - (timmar * 60)
        sekunder = spel_tid - (minuter * 60) - (timmar * 3600)

        return f'{timmar} : {minuter} : {sekunder}'

    def avslut_spelet(self):
        """
        Denna metod körs när användaren trycker på "avsluta spelet" knappen och går tillbaka till start_frame.
        """
        # ställ_om_spelet()
        self.bradet = []
        self.antal_forsok = 5
        self.spel_frame.grid_forget()
        self.start_frame()

class Cell:
    """
    Denna class skapar en cell som placeras i brädet.
    varje cell har ett attribut "har_troll" fär att representera om cellen har en troll eller ej,
    och ett attribut av typen Label för att visa troll eller gräs-bilden.
    varje objekt av typen Cell ska ha två metoder "visa_gräs" och "visa_troll" för att visa gräs-bilden om attributet
    "har_troll" är False och visa troll-bilden om attributet "har_troll" är True.
    """

    def __init__(self, har_troll, frame):
        self.har_troll = har_troll
        self.gras_bild = ImageTk.PhotoImage(file='ECO-GRASS-SOFT-TOUCH-150x150.jpg')
        self.troll_bild = ImageTk.PhotoImage(file='223_medium.jpg')
        self.label = tk.Label(frame)
        self.visa_gras()

    def visa_gras(self):
        self.label.configure(image=self.gras_bild)

    def visa_troll(self):
        self.label.configure(image=self.troll_bild)

class Spelare:
    """Denna class skapar en spelare där brädets storlek, tiden och namn sätts ihop till en spelare """
    def __init__(self, namn, storlek, speltid):
        self.namn = namn
        self.storlek = storlek
        self.speltid = speltid

def main():
    """ denna if sats funkar endast första gången koden körs för att skapa en fil
    och spara den ifall den inte redan finns """
    if not felhantering.fil_kontrollering():
        ny_fil = open('Highscore.txt', 'w')
        ny_fil.close()
    ny_spel = Spel()
    ny_spel.start_frame()

if __name__ == "__main__":
    main()




   

