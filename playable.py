import pygame
import sys
import random

# --- ERALDI SKOORI KLASS ---
class Timer:
    def __init__(self):
        self.algusaeg = pygame.time.get_ticks()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.sekundid = 0

    def uuenda(self):
        self.sekundid = (pygame.time.get_ticks() - self.algusaeg) // 1000

    def joonista(self, aken):
        tekst = self.font.render(f"Aeg: {self.sekundid}s", True, (255, 255, 255))
        aken.blit(tekst, (20, 60))

    def reset(self):
        self.algusaeg = pygame.time.get_ticks()
        self.sekundid = 0

class Score:
    def __init__(self):
        self.points = 0
        self.high_score = 0
        self.font = pygame.font.SysFont("Arial", 24, bold=True)

    def lisa_punkte(self, kogus):
        self.points += kogus
        if self.points > self.high_score:
            self.high_score = self.points

    def joonista(self, aken):
        skoor_pind = self.font.render(f"Score: {int(self.points)}", True, (255, 255, 255))
        aken.blit(skoor_pind, (20, 20))

        high_score_pind = self.font.render(f"High Score: {int(self.high_score)}", True, (255, 255, 255))
        aken.blit(high_score_pind, (455, 20))

    def reset(self):
        self.points = 0

class Car:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 90)
        self.kiirus = 7
        self.PUNANE = (191, 12, 12)
        self.MUST = (30, 30, 30)
        self.KLAAS = (173, 216, 230)

    def liiguta(self):
        klahvid = pygame.key.get_pressed()
        if klahvid[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.kiirus
        if klahvid[pygame.K_RIGHT] and self.rect.right < 640:
            self.rect.x += self.kiirus

    def joonista(self, aken, varv=(191, 12, 12)):
        pygame.draw.rect(aken, varv, self.rect, border_radius=8)
        pygame.draw.rect(aken, (30, 30, 30), self.rect, 2, border_radius=8)
        ratta_laius, ratta_korgus = 10, 18
        rattad = [
            (self.rect.x - 2, self.rect.y + 10),
            (self.rect.right - ratta_laius + 2, self.rect.y + 10),
            (self.rect.x - 2, self.rect.bottom - 25),
            (self.rect.right - ratta_laius + 2, self.rect.bottom - 25)
        ]
        for r in rattad:
            pygame.draw.rect(aken, (30, 30, 30), (r[0], r[1], ratta_laius, ratta_korgus), border_radius=3)
        klaasi_varv = (173, 216, 230)
        pygame.draw.rect(aken, klaasi_varv, (self.rect.x + 8, self.rect.y + 20, 34, 15), border_radius=2)
        pygame.draw.rect(aken, klaasi_varv, (self.rect.x + 8, self.rect.bottom - 30, 34, 10), border_radius=2)

class McTrip:
    def __init__(self):
        pygame.init()
        # Algatame helisüsteemi
        pygame.mixer.init()

        self.LAAIUS, self.KORGUS = 640, 960
        self.aken = pygame.display.set_mode((self.LAAIUS, self.KORGUS))
        pygame.display.set_caption("McTrip")
        self.kell = pygame.time.Clock()

        

        self.VALGE = (255, 255, 255)
        self.MUST = (0, 0, 0)
        self.HALL = (80, 80, 80)
        self.VARVID = [(0, 0, 255), (0, 200, 0), (255, 165, 0), (128, 0, 128), (0, 255, 255)]

        self.mang_kaib = False
        self.mang_labi = False
        self.dialoog_kaib = False 
        
        self.nupp_rect = pygame.Rect(230, 440, 180, 80)
        self.reset_nupp_rect = pygame.Rect(200, 500, 240, 80)
        
        self.triibu_vahe = 150
        self.triibud = [[315, i * self.triibu_vahe] for i in range(10)]
        self.auto = Car(300, 800)
        
        self.skoor = Score()
        self.vastased = []
        self.toidud = [] 
        self.vastaste_kiirus = 10 
        self.teksti_timer = 180
        self.taimer = Timer()

        # DIALOOGI ANDMED (Uuendatud)
        self.dialoogi_tekstid = [
            "Kurat, kõht on nii tühi...",
            "Ma tahaks bigmac einet...",
            "Ja tahaks suurt kokat ka...",
            "Lähme ruttu mäkki!",
            "Vajuta 'Enter', et sõitma hakata!"
        ]
        self.praegune_lause = 0
        self.dialoog_font = pygame.font.SysFont("Calibri", 26, bold=True)
        
        # --- UUED MUUTUJAD TRÜKKIMISE EFEKTI JAOKS ---
        self.trykitud_tekst = ""            # Tekst, mis on hetkel ekraanil
        self.taislause = ""                 # Kogu lause, mis peab ilmuma
        self.tahe_indeks = 0                # Mitu tähte on trükitud
        self.trykkimise_kiirus = 2          # Mitu frame'i oodata enne uut tähte
        self.trykkimise_counter = 0         # Taimer tähtede jaoks
        self.tekst_ilmub = False           # Kas trükkimine käib hetkel?
        self.meheke_offset_y = 0            # Meheke liigutamiseks y-teljel
        self.meheke_liigub_yles = False    # Kas meheke on "hüppe" faasis
        
        # PILTIDE LAADIMINE
        try:
            self.logo_pilt = pygame.image.load("McTrip.png").convert_alpha()
            logo_laius = 450
            logo_korgus = int(self.logo_pilt.get_height() * (logo_laius / self.logo_pilt.get_width()))
            self.logo_pilt = pygame.transform.scale(self.logo_pilt, (logo_laius, logo_korgus))
            self.logo_rect = self.logo_pilt.get_rect(center=(self.LAAIUS // 2, 255))
        except:
            self.logo_pilt = None

        # TOIDU PILTIDE LAADIMINE
        try:
            self.pildid = {
                "friikad": pygame.transform.scale(pygame.image.load("friikad.png").convert_alpha(), (70, 70)),
                "burger": pygame.transform.scale(pygame.image.load("Burger.png").convert_alpha(), (80, 50)),
                "mcsoft": pygame.transform.scale(pygame.image.load("McSoft2.png").convert_alpha(), (50, 80))
            }
        except:
            # Kui pilte pole, loome värvilised kastid
            self.pildid = {
                "friikad": pygame.Surface((40, 40)),
                "burger": pygame.Surface((50, 30)),
                "mcsoft": pygame.Surface((30, 50))
            }
            self.pildid["friikad"].fill((255, 255, 0))
            self.pildid["burger"].fill((139, 69, 19))
            self.pildid["mcsoft"].fill((0, 191, 255))

        # Dialoogi pildid (Uuendatud suu lahti pildiga)
        try:
            self.meheke_pilt = pygame.image.load("Meheke_uus.png").convert_alpha()
            self.meheke_pilt = pygame.transform.scale(self.meheke_pilt, (140, 160)) 
            
            # --- UUS PILLT: Suu lahti ---
            self.meheke_suu_lahti = pygame.image.load("Raakimine.png").convert_alpha()
            self.meheke_suu_lahti = pygame.transform.scale(self.meheke_suu_lahti, (140, 160))
            
            self.kast_pilt = pygame.image.load("Dialoog kast_uus.png").convert_alpha()
            self.kast_pilt = pygame.transform.scale(self.kast_pilt, (640, 160))
        except:
            self.meheke_pilt = None
            self.meheke_suu_lahti = None
            self.kast_pilt = None

        # --- HELI LAADIMINE ---
        try:
            self.raakimissound = pygame.mixer.Sound("Mehe_raakimine.wav")
            self.raakimissound.set_volume(0.03)
        except:
            self.raakimissound = None

        # === UUS: TAUSTAMUUSIKA LISAMINE ===
        try:
            # Asenda "taustamuusika.mp3" oma faili nimega
            pygame.mixer.music.load("track.wav") 
            
            # Määrame helitugevuse (0.0 kuni 1.0)
            pygame.mixer.music.set_volume(0.5) 
            
            # Paneme muusika mängima. Lõpmatu korduse jaoks määrame loops=-1
            pygame.mixer.music.play(loops=-1) 
        except pygame.error as e:
            print(f"Muusika laadimine ebaõnnestus: {e}")

        # === UUS: SÖÖKIDE JA AVARII HELID ===
        try:
            self.heli_friikad = pygame.mixer.Sound("YUM!.mp3")
            self.heli_burger = pygame.mixer.Sound("YUM!.mp3")
            self.heli_mcsoft = pygame.mixer.Sound("YUM!.mp3")
            self.heli_crash = pygame.mixer.Sound("DEATH.mp3")
            
            # Keera crashi heli natuke kõvemaks, et oleks matsu kuulda
            self.heli_crash.set_volume(0.2)
            self.heli_mcsoft.set_volume(0.2)
            self.heli_burger.set_volume(0.2)
            self.heli_friikad.set_volume(0.2)
        except:
            self.heli_friikad = None
            self.heli_burger = None
            self.heli_mcsoft = None
            self.heli_crash = None

        # --- LÕPU CUTSCENE'I ANDMED (LISA SIIA) ---
        self.cutscene_kaib = False
        self.cutscene_indeks = 0
        self.cutscene_tekstid = [
            "Lõpuks ometi olen kohale jõudnud",
            "Ma olen nii ära nälginud",
            "Oi kui hea big mac",
            "Nüüd koju, et sittuda see kõik välja"
        ]

        # Uued muutujad fade'i jaoks
        self.fade_alpha = 255  # 255 tähendab täiesti musta, 0 tähendab läbipaistvat
        self.fade_pind = pygame.Surface((self.LAAIUS, self.KORGUS))
        self.fade_pind.fill(self.MUST)
        self.fading_in = False

        # Laadime pildid (ootab faile lopustseen1.png, lopustseen2.png jne)
        self.cutscene_pildid = []
        for i in range(1, len(self.cutscene_tekstid) + 1):
            try:
                pilt = pygame.image.load(f"lopustseen{i}.png").convert()
                pilt = pygame.transform.scale(pilt, (self.LAAIUS, self.KORGUS))
                self.cutscene_pildid.append(pilt)
            except:
                # Kui pilte kaustas pole, luuakse ajutised rohekad taustad testimiseks
                asendus_pind = pygame.Surface((self.LAAIUS, self.KORGUS))
                asendus_pind.fill((20, 40 + (i * 30), 20))
                self.cutscene_pildid.append(asendus_pind)

        self.valitud_raskus = None  # Alguses pole midagi valitud
        self.sihtskoor = 200
        
        # Raskusastme nupud (nihutatud veidi ülespoole, et PLAY mahuks alla)
        self.nupp_easy = pygame.Rect(200, 500, 230, 60)
        self.nupp_medium = pygame.Rect(200, 580, 235, 60)
        self.nupp_hard = pygame.Rect(200, 660, 230, 60)
        
        # PLAY nupp
        self.nupp_play = pygame.Rect(220, 760, 200, 80)

    # --- UUS FUNKTSIOON: Teksti trükkimise algatamine ja mehe hüpe ---
    def algata_teksti_trykkimine(self):
        # Vaatame, kumba teksti parajasti trükkida on vaja
        if self.dialoog_kaib and self.praegune_lause < len(self.dialoogi_tekstid):
            self.taislause = self.dialoogi_tekstid[self.praegune_lause]
        elif self.cutscene_kaib and self.cutscene_indeks < len(self.cutscene_tekstid):
            self.taislause = self.cutscene_tekstid[self.cutscene_indeks]
        else:
            # Kui tekstid saavad otsa
            if self.dialoog_kaib:
                self.dialoog_kaib = False
                self.mang_kaib = True
                self.taimer.reset()
            elif self.cutscene_kaib:
                self.cutscene_kaib = False
                self.mang_labi = True
            return

        self.tahe_indeks = 0
        self.trykitud_tekst = ""
        self.tekst_ilmub = True
        self.meheke_offset_y = -20
        self.meheke_huppe_taimer = 10 
        
        if self.raakimissound:
            self.raakimissound.play(loops=-1)

    def reset_mang(self):
        self.cutscene_kaib = False
        self.cutscene_indeks = 0
        self.mang_kaib = False
        self.mang_labi = False
        self.dialoog_kaib = False
        self.valitud_raskus = None  # LISA SEE RIDA
        
        self.vastased = []
        self.toidud = []
        self.auto.rect.x = 300
        
        self.praegune_lause = 0
        self.teksti_timer = 180
        self.vastaste_kiirus = 10 
        self.skoor.reset()
        self.taimer.reset()

        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play(loops=-1)
        
        
        # EEMALDATUD: self.algata_teksti_trykkimine() rida pole siin enam vaja!

    def joonista_auto_mudel(self, aken, rect, varv):
        pygame.draw.rect(aken, varv, rect, border_radius=8)
        pygame.draw.rect(aken, (30, 30, 30), rect, 2, border_radius=8)
        ratta_v = (30, 30, 30)
        pygame.draw.rect(aken, ratta_v, (rect.x - 2, rect.y + 10, 10, 18), border_radius=3)
        pygame.draw.rect(aken, ratta_v, (rect.right - 8, rect.y + 10, 10, 18), border_radius=3)
        pygame.draw.rect(aken, ratta_v, (rect.x - 2, rect.bottom - 25, 10, 18), border_radius=3)
        pygame.draw.rect(aken, ratta_v, (rect.right - 8, rect.bottom - 25, 10, 18), border_radius=3)
        klaas = (173, 216, 230)
        pygame.draw.rect(aken, klaas, (rect.x + 8, rect.y + 20, 34, 15), border_radius=2)
        pygame.draw.rect(aken, klaas, (rect.x + 8, rect.bottom - 30, 34, 10), border_radius=2)

    def tekita_vastane(self):
        if random.random() < 0.04:
            read = [25, 100, 200, 300, 400, 500, 560]
            mitu = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
            valitud_read = random.sample(read, mitu)
            for rida in valitud_read:
                y_pos = random.randint(-400, -100)
                uus_rect = pygame.Rect(rida, y_pos, 50, 90)
                lubatud = True
                for v_andmed in self.vastased:
                    if uus_rect.colliderect(v_andmed[0].inflate(70, 200)):
                        lubatud = False
                        break
                if lubatud:
                    self.vastased.append([uus_rect, random.choice(self.VARVID)])

        # TOIDU TEKITAMINE TÕENÄOSUSTEGA
        if random.random() < 0.025: # Sagedus, kui tihti üldse midagi tekib
            toit_x = random.randint(50, self.LAAIUS - 80)
            
            # Määrame tüübi ja tõenäosused: friikad 70%, burger 20%, mcsoft 10%
            tyybid = ["friikad", "burger", "mcsoft"]
            kaalud = [70, 20, 10]
            valitud_tyyp = random.choices(tyybid, weights=kaalud)[0]
            
            uus_toit = {
                "rect": pygame.Rect(toit_x, -80, 80, 80),
                "tyyp": valitud_tyyp
            }
            self.toidud.append(uus_toit)

    def uuenda_tausta(self):
        for triip in self.triibud:
            triip[1] += 7 
            if triip[1] > self.KORGUS:
                koige_ylem_y = min(t[1] for t in self.triibud)
                triip[1] = koige_ylem_y - self.triibu_vahe

    def joonista(self):
        self.aken.fill(self.HALL) 
        for triip in self.triibud:
            pygame.draw.rect(self.aken, self.VALGE, (triip[0], triip[1], 10, 40))

        if not self.mang_kaib and not self.mang_labi and not self.dialoog_kaib and not self.cutscene_kaib:
            if self.logo_pilt:
                self.aken.blit(self.logo_pilt, self.logo_rect)
        
        if not self.mang_kaib and not self.mang_labi and not self.dialoog_kaib and not self.cutscene_kaib:
            if self.logo_pilt:
                self.aken.blit(self.logo_pilt, self.logo_rect)
            
            # --- JOONISTAME RASKUSASTME NUPUD ---
        if not self.mang_kaib and not self.mang_labi and not self.dialoog_kaib and not self.cutscene_kaib:
            if self.logo_pilt:
                self.aken.blit(self.logo_pilt, self.logo_rect)
            
            font_nupp = pygame.font.SysFont("Calibri", 30, bold=True)
            raskused = [
                (self.nupp_easy, "KERGE (200)", (0, 200, 0), "easy"),
                (self.nupp_medium, "KESKMINE (300)", (200, 200, 0), "medium"),
                (self.nupp_hard, "RASKE (400)", (200, 0, 0), "difficult")
            ]

            for rect, tekst, varv, nimi in raskused:
                # Kui see nupp on valitud, teeme piirjoone paksemaks (8), muidu tavaline (4)
                paksus = 8 if self.valitud_raskus == nimi else 4
                pygame.draw.rect(self.aken, (255, 255, 255), rect, border_radius=10)
                pygame.draw.rect(self.aken, varv, rect, paksus, border_radius=10)
                t_pind = font_nupp.render(tekst, True, (0, 0, 0))
                self.aken.blit(t_pind, (rect.x + 35, rect.y + 15))

            # --- JOONISTAME PLAY NUPU ---
            # Kui raskus on valitud, on PLAY nupp erekollane, muidu hallikas
            play_varv = (255, 215, 0) if self.valitud_raskus else (150, 150, 150)
            pygame.draw.rect(self.aken, play_varv, self.nupp_play, border_radius=15)
            pygame.draw.rect(self.aken, (0, 0, 0), self.nupp_play, 5, border_radius=15)
            play_tekst = font_nupp.render("START GAME", True, (0, 0, 0))
            self.aken.blit(play_tekst, (self.nupp_play.x + 25, self.nupp_play.y + 25))
        # --- DIALOOGI JOONISTAMISE LOGIKA (UUENDATUD) ---
        elif self.dialoog_kaib:
            self.auto.joonista(self.aken, (191, 12, 12))
            
            # Valib pildi selle järgi, kas tekst jookseb (suu lahti) või mitte
            pilt_mida_kasutada = self.meheke_suu_lahti if self.tekst_ilmub else self.meheke_pilt

            # Meheke hüppe loogika tagasitõmbumine (kui vajutati enterit)
            if self.meheke_offset_y < 0:
                self.meheke_offset_y += 2
                if self.meheke_offset_y > 0:
                    self.meheke_offset_y = 0

            # Joonistame pildid ekraanile
            if pilt_mida_kasutada:
                self.aken.blit(pilt_mida_kasutada, (-5, 725 + self.meheke_offset_y))
            
            if self.kast_pilt:
                self.aken.blit(self.kast_pilt, (0, 800))
            
            # Joonistame teksti
            if self.dialoog_font:
                lause = self.dialoog_font.render(self.trykitud_tekst, True, self.MUST)
                self.aken.blit(lause, (100, 875))
            
            # ENTER vihje ilmub alles siis, kui mees on rääkimise lõpetanud
            if not self.tekst_ilmub:
                vihje = self.dialoog_font.render("[ ENTER ]", True, (100, 100, 100))
                self.aken.blit(vihje, (500, 900))
        
        # --- LÕPU CUTSCENE JOONISTAMINE ---
        elif self.cutscene_kaib:
            # 1. Kuvame täisekraani taustapildi
            if self.cutscene_pildid and self.cutscene_indeks < len(self.cutscene_pildid):
                self.aken.blit(self.cutscene_pildid[self.cutscene_indeks], (0, 0))
            
            # 2. Joonistame musta kile pildi peale, kui hajumine käib
            if self.fade_alpha > 0:
                self.fade_pind.set_alpha(self.fade_alpha)
                self.aken.blit(self.fade_pind, (0, 0))
            
            # 3. Dialoogikast ja tekst tulevad NÄHTAVALE alles siis, kui fade on läbi
            if not self.fading_in:
                if self.kast_pilt:
                    self.aken.blit(self.kast_pilt, (0, 800))
                else:
                    pygame.draw.rect(self.aken, self.VALGE, (0, 800, 640, 160))
                
                if self.dialoog_font:
                    lause = self.dialoog_font.render(self.trykitud_tekst, True, self.MUST)
                    self.aken.blit(lause, (100, 875))
                
                # ENTER vihje ilmub, kui lause on trükitud
                if not self.tekst_ilmub:
                    vihje = self.dialoog_font.render("[ ENTER ]", True, (100, 100, 100))
                    self.aken.blit(vihje, (500, 900))

        elif self.mang_labi:
            font = pygame.font.SysFont("Calibri", 40)
            fail_tekst = font.render(f"Final Score: {int(self.skoor.points)}", True, self.VALGE)
            fail_text = font.render(f"Final Time: {int(self.taimer.sekundid)}", True, self.VALGE)
            self.aken.blit(fail_tekst, (220, 350))
            self.aken.blit(fail_text, (220, 410))
            pygame.draw.rect(self.aken, self.VALGE, self.reset_nupp_rect)
            pygame.draw.rect(self.aken, self.MUST, self.reset_nupp_rect, 5)
            btn_font = pygame.font.SysFont("Calibri", 50)
            btn_tekst = btn_font.render("Try Again", True, self.MUST)
            self.aken.blit(btn_tekst, (self.reset_nupp_rect.x + 25, self.reset_nupp_rect.y + 15))

        elif self.mang_kaib:
            self.auto.joonista(self.aken, (191, 12, 12)) 
            for v_andmed in self.vastased:
                self.joonista_auto_mudel(self.aken, v_andmed[0], v_andmed[1])
            
            # TOIDU JOONISTAMINE (Friikad, Burger, McSoft)
            for toit in self.toidud:
                if toit["tyyp"] in self.pildid:
                    self.aken.blit(self.pildid[toit["tyyp"]], toit["rect"])

            self.skoor.joonista(self.aken)
            self.taimer.joonista(self.aken)

            if self.teksti_timer > 0:
                font = pygame.font.SysFont("Calibri", 32)
                tekst_pind = font.render("Welcome to McTrip", True, self.VALGE)
                labipaistvus = max(0, min(255, self.teksti_timer * 1.5))
                tekst_pind.set_alpha(labipaistvus)
                self.aken.blit(tekst_pind, (210, 200))

        pygame.display.flip()
    
    def run(self):
        while True:
            for sündmus in pygame.event.get():
                if sündmus.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 1. KLAHVIVAJUTUSED (Klaviatuuril pole ".pos" omadust!)
                if sündmus.type == pygame.KEYDOWN:
                    if sündmus.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if sündmus.key == pygame.K_RETURN:
                        if self.dialoog_kaib:
                            if self.tekst_ilmub:
                                self.trykitud_tekst = self.taislause
                                self.tahe_indeks = len(self.taislause)
                                self.tekst_ilmub = False
                                if self.raakimissound: self.raakimissound.stop()
                            else:
                                self.praegune_lause += 1
                                self.algata_teksti_trykkimine()

                        elif self.cutscene_kaib:
                            if self.tekst_ilmub:
                                self.trykitud_tekst = self.taislause
                                self.tahe_indeks = len(self.taislause)
                                self.tekst_ilmub = False
                                if self.raakimissound: self.raakimissound.stop()
                            else:
                                self.cutscene_indeks += 1
                                self.algata_teksti_trykkimine()

                # 2. HIIREVAJUTUSED (Siin on ".pos" olemas!)
                elif sündmus.type == pygame.MOUSEBUTTONDOWN:
                    # Menüü nupud
                    if not self.mang_kaib and not self.mang_labi and not self.dialoog_kaib and not self.cutscene_kaib:
                        if self.nupp_easy.collidepoint(sündmus.pos):
                            self.sihtskoor = 200
                            self.valitud_raskus = "easy"
                        elif self.nupp_medium.collidepoint(sündmus.pos):
                            self.sihtskoor = 300
                            self.valitud_raskus = "medium"
                        elif self.nupp_hard.collidepoint(sündmus.pos):
                            self.sihtskoor = 400
                            self.valitud_raskus = "hard"
                        elif self.nupp_play.collidepoint(sündmus.pos):
                            if self.valitud_raskus is not None:
                                self.dialoog_kaib = True
                                self.algata_teksti_trykkimine()

                    # Try Again nupp
                    elif self.mang_labi:
                        if self.reset_nupp_rect.collidepoint(sündmus.pos):
                            self.reset_mang()
            
            self.uuenda_tausta()

            # --- TEKSTI TRÜKKIMISE JA SUU LOGIKA (MÕLEMA OLEKU JAOKS) ---
            if (self.dialoog_kaib or self.cutscene_kaib) and self.tekst_ilmub:
                self.trykkimise_counter += 1
                if self.trykkimise_counter >= self.trykkimise_kiirus:
                    self.trykkimise_counter = 0
                    if self.tahe_indeks < len(self.taislause):
                        self.trykitud_tekst += self.taislause[self.tahe_indeks]
                        self.tahe_indeks += 1
                    else:
                        self.tekst_ilmub = False
                        if self.raakimissound:
                            self.raakimissound.stop()

            # Meheke hüppe loogika tagasitõmbumine
            if self.meheke_offset_y < 0:
                self.meheke_offset_y += 2
                if self.meheke_offset_y > 0:
                    self.meheke_offset_y = 0
            
            if self.mang_kaib:
                self.skoor.lisa_punkte(2 / 60)
                self.taimer.uuenda()
                
                # --- KONTROLLIME, KAS SIHTSKOOR ON KÄES ---
                if self.skoor.points >= self.sihtskoor:
                    self.mang_kaib = False
                    self.cutscene_kaib = True
                    self.fading_in = True
                    self.fade_alpha = 255
                    self.cutscene_indeks = 0
                    self.vastased = []  # Puhastame ekraani autodest
                    self.toidud = []    # Puhastame ekraani toidust
                    pygame.mixer.music.fadeout(2000)
                        
                tase = self.skoor.points // 40
                self.vastaste_kiirus = 9 + tase * 2
                self.auto.kiirus = 7 + tase
                
                self.auto.liiguta()
                self.tekita_vastane()

                for v_andmed in self.vastased[:]:
                    rect = v_andmed[0]
                    rect.y += self.vastaste_kiirus
                    if rect.y > self.KORGUS:
                        self.vastased.remove(v_andmed)
                        
                    # --- Auto kokkupõrge ---
                    if self.auto.rect.colliderect(rect):
                        if self.heli_crash:
                            self.heli_crash.play() # Mängime matsu heli
                        
                        pygame.mixer.music.stop() # Paneme taustamuusika kinni
                        
                        self.mang_kaib = False
                        self.mang_labi = True

                # Toidu liikumine ja kokkupõrge
                for toit in self.toidud[:]:
                    toit["rect"].y += self.vastaste_kiirus
                    
                    if toit["rect"].y > self.KORGUS:
                        self.toidud.remove(toit)
                    
                    # --- Toidu söömine ---
                    if self.auto.rect.colliderect(toit["rect"]):
                        if toit["tyyp"] == "friikad":
                            self.skoor.lisa_punkte(5)
                            if self.heli_friikad: self.heli_friikad.play()
                            
                        elif toit["tyyp"] == "burger":
                            self.skoor.lisa_punkte(10)
                            if self.heli_burger: self.heli_burger.play()
                            
                        elif toit["tyyp"] == "mcsoft":
                            self.skoor.lisa_punkte(15)
                            if self.heli_mcsoft: self.heli_mcsoft.play()
                            
                        self.toidud.remove(toit)
            
                if self.teksti_timer > 0:
                    self.teksti_timer -= 1

            # --- FADE IN LOOGIKA ---
            if self.cutscene_kaib and self.fading_in:
                self.fade_alpha -= 3  # Muuda seda numbrit, et muuta hajumise kiirust
                if self.fade_alpha <= 0:
                    self.fade_alpha = 0
                    self.fading_in = False
                    self.algata_teksti_trykkimine() # Käivitame teksti alles siis, kui pilt on täiesti nähtav

            self.joonista()
            self.kell.tick(60)

if __name__ == "__main__":
    mang = McTrip()
    mang.run()