import pygame
import sys
import random

# --- ERALDI SKOORI KLASS ---
class Score:
    def __init__(self):
        self.points = 0
        self.font = pygame.font.SysFont("Arial", 32, bold=True)

    def lisa_punkte(self, kogus):
        self.points += kogus

    def joonista(self, aken):
        # Tekitame tekstist pildi (render)
        skoor_pind = self.font.render(f"Score: {int(self.points)}", True, (255, 255, 255))
        # Joonistame selle ekraanile (blit) - asukoht 20, 20 on ekraanil nähtav
        aken.blit(skoor_pind, (20, 20))

    def reset(self):
        self.points = 0

class Car:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 90)
        self.kiirus = 7

    def liiguta(self):
        klahvid = pygame.key.get_pressed()
        if klahvid[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.kiirus
        if klahvid[pygame.K_RIGHT] and self.rect.right < 640:
            self.rect.x += self.kiirus

    def joonista(self, aken):
        pygame.draw.rect(aken, (255, 0, 0), self.rect)
        pygame.draw.rect(aken, (0, 0, 0), self.rect, 2)

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
        
        # LOOME SKOORI OBJEKTI
        self.skoor = Score()
        
        self.vastased = []
        self.teksti_timer = 180

    def reset_mang(self):
        self.vastased = []
        self.auto.rect.x = 300
        self.mang_kaib = True
        self.mang_labi = False
        self.teksti_timer = 180
        self.skoor.reset() # Nullime skoori uue mängu alguses

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
            # Algusmenüü
            pygame.draw.rect(self.aken, self.VALGE, self.nupp_rect)
            pygame.draw.rect(self.aken, self.MUST, self.nupp_rect, 5)
            font = pygame.font.SysFont("Calibri", 60)
            tekst = font.render("PLAY", True, self.MUST)
            self.aken.blit(tekst, (self.nupp_rect.x + 30, self.nupp_rect.y + 10))

        elif self.mang_labi:
            # Kaotuse ekraan
            font = pygame.font.SysFont("Calibri", 40)
            fail_tekst = font.render(f"Final Score: {int(self.skoor.points)}", True, self.VALGE)
            self.aken.blit(fail_tekst, (220, 350))
            
            pygame.draw.rect(self.aken, self.VALGE, self.reset_nupp_rect)
            pygame.draw.rect(self.aken, self.MUST, self.reset_nupp_rect, 5)
            btn_font = pygame.font.SysFont("Calibri", 50)
            btn_tekst = btn_font.render("Try Again", True, self.MUST)
            self.aken.blit(btn_tekst, (self.reset_nupp_rect.x + 25, self.reset_nupp_rect.y + 15))

        elif self.mang_kaib:
            self.auto.joonista(self.aken)
            for v_andmed in self.vastased:
                rect, varv = v_andmed
                pygame.draw.rect(self.aken, varv, rect)
                pygame.draw.rect(self.aken, self.MUST, rect, 2)

            # SKOORI JOONISTAMINE
            self.skoor.joonista(self.aken)

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
                # SKOORI LISAMINE: 2 punkti sekundis (60 FPS juures)
                self.skoor.lisa_punkte(2 / 60)
                
                self.auto.liiguta()
                self.tekita_vastane()

                for v_andmed in self.vastased[:]:
                    rect = v_andmed[0]
                    rect.y += 10
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