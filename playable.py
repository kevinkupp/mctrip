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
        # Arvutame möödunud aja sekundites
        self.sekundid = (pygame.time.get_ticks() - self.algusaeg) // 1000

    def joonista(self, aken):
        tekst = self.font.render(f"Aeg: {self.sekundid}s", True, (255, 255, 255))
        # Joonistame skoorist veidi allapoole
        aken.blit(tekst, (20, 60))

    def reset(self):
        self.algusaeg = pygame.time.get_ticks()
        self.sekundid = 0

class Score:
    def __init__(self):
        self.points = 0
        self.font = pygame.font.SysFont("Arial", 32, bold=True)

    def lisa_punkte(self, kogus):
        self.points += kogus

    def joonista(self, aken):
        skoor_pind = self.font.render(f"Score: {int(self.points)}", True, (255, 255, 255))
        aken.blit(skoor_pind, (20, 20))

    def reset(self):
        self.points = 0

class Car:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 90)
        self.kiirus = 7
        self.PUNANE = (191, 12, 12)
        self.MUST = (30, 30, 30)
        self.KLAAS = (173, 216, 230) # Helesinine

    def liiguta(self):
        klahvid = pygame.key.get_pressed()
        if klahvid[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.kiirus
        if klahvid[pygame.K_RIGHT] and self.rect.right < 640:
            self.rect.x += self.kiirus

    def joonista(self, aken, varv=(191, 12, 12)):
        # 1. Kere (põhivärv)
        pygame.draw.rect(aken, varv, self.rect, border_radius=8)
        # Kere piirjoon
        pygame.draw.rect(aken, (30, 30, 30), self.rect, 2, border_radius=8)

        # 2. Rattad (4 musta ristkülikut nurkades)
        ratta_laius = 10
        ratta_korgus = 18
        # Vasak ees, Parem ees, Vasak taga, Parem taga
        rattad = [
            (self.rect.x - 2, self.rect.y + 10),
            (self.rect.right - ratta_laius + 2, self.rect.y + 10),
            (self.rect.x - 2, self.rect.bottom - 25),
            (self.rect.right - ratta_laius + 2, self.rect.bottom - 25)
        ]
        for r in rattad:
            pygame.draw.rect(aken, (30, 30, 30), (r[0], r[1], ratta_laius, ratta_korgus), border_radius=3)

        # 3. Klaasid (Helesinine)
        klaasi_varv = (173, 216, 230)
        # Esiklaas
        pygame.draw.rect(aken, klaasi_varv, (self.rect.x + 8, self.rect.y + 20, 34, 15), border_radius=2)
        # Tagaklaas
        pygame.draw.rect(aken, klaasi_varv, (self.rect.x + 8, self.rect.bottom - 30, 34, 10), border_radius=2)

class McTrip:
    def __init__(self):
        pygame.init()
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
        
        self.nupp_rect = pygame.Rect(230, 440, 180, 80)
        self.reset_nupp_rect = pygame.Rect(200, 500, 240, 80)
        
        self.triibu_vahe = 150
        self.triibud = [[315, i * self.triibu_vahe] for i in range(10)]
        self.auto = Car(300, 800)
        
        self.skoor = Score()
        self.vastased = []
        self.vastaste_kiirus = 10 
        self.teksti_timer = 180
        self.taimer = Timer()

    def reset_mang(self):
        self.vastased = []
        self.auto.rect.x = 300
        self.mang_kaib = True
        self.mang_labi = False
        self.teksti_timer = 180
        self.vastaste_kiirus = 10 
        self.skoor.reset()
        self.taimer.reset()
    
    def joonista_auto_mudel(self, aken, rect, varv):
        # Kere
        pygame.draw.rect(aken, varv, rect, border_radius=8)
        pygame.draw.rect(aken, (30, 30, 30), rect, 2, border_radius=8)
        
        # Rattad
        ratta_v = (30, 30, 30)
        pygame.draw.rect(aken, ratta_v, (rect.x - 2, rect.y + 10, 10, 18), border_radius=3)
        pygame.draw.rect(aken, ratta_v, (rect.right - 8, rect.y + 10, 10, 18), border_radius=3)
        pygame.draw.rect(aken, ratta_v, (rect.x - 2, rect.bottom - 25, 10, 18), border_radius=3)
        pygame.draw.rect(aken, ratta_v, (rect.right - 8, rect.bottom - 25, 10, 18), border_radius=3)

        # Klaasid
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
                    v_rect = v_andmed[0]
                    if uus_rect.colliderect(v_rect.inflate(70, 200)):
                        lubatud = False
                        break
                
                if lubatud:
                    suvaline_varv = random.choice(self.VARVID)
                    self.vastased.append([uus_rect, suvaline_varv])

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

        if not self.mang_kaib and not self.mang_labi:
            pygame.draw.rect(self.aken, self.VALGE, self.nupp_rect)
            pygame.draw.rect(self.aken, self.MUST, self.nupp_rect, 5)
            font = pygame.font.SysFont("Calibri", 60)
            tekst = font.render("PLAY", True, self.MUST)
            self.aken.blit(tekst, (self.nupp_rect.x + 30, self.nupp_rect.y + 10))

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
                rect, varv = v_andmed
                self.joonista_auto_mudel(self.aken, rect, varv)

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
                
                if sündmus.type == pygame.MOUSEBUTTONDOWN:
                    if not self.mang_kaib and not self.mang_labi:
                        if self.nupp_rect.collidepoint(sündmus.pos):
                            self.mang_kaib = True
                    elif self.mang_labi:
                        if self.reset_nupp_rect.collidepoint(sündmus.pos):
                            self.reset_mang()
            
            self.uuenda_tausta()
                 
            if self.mang_kaib:
                # Skoori lisamine
                self.skoor.lisa_punkte(2 / 60)
                self.taimer.uuenda()
                
                # KONTROLL: Kas skoor on 10 täis?
                if self.skoor.points >= 300:
                    pygame.quit()
                    sys.exit()
                        
                # Taseme ja kiiruse arvutamine
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
                        
                    if self.auto.rect.colliderect(rect):
                        self.mang_kaib = False
                        self.mang_labi = True
            
                if self.teksti_timer > 0:
                    self.teksti_timer -= 1

            self.joonista()
            self.kell.tick(60)

if __name__ == "__main__":
    mang = McTrip()
    mang.run()