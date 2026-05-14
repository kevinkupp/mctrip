import pygame
import sys

class Car:
    def __init__(self, x, y):
        # Suurendame veidi mõõtmeid (50x90), et detailid mahuksid ära
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

    def joonista(self, aken):
        # 1. Rattad (4 musta ristkülikut nurkades)
        pygame.draw.rect(aken, self.MUST, (self.rect.x - 5, self.rect.y + 10, 10, 20)) # Vasak esimene
        pygame.draw.rect(aken, self.MUST, (self.rect.x + 45, self.rect.y + 10, 10, 20)) # Parem esimene
        pygame.draw.rect(aken, self.MUST, (self.rect.x - 5, self.rect.y + 60, 10, 20)) # Vasak tagumine
        pygame.draw.rect(aken, self.MUST, (self.rect.x + 45, self.rect.y + 60, 10, 20)) # Parem tagumine

        # 2. Auto kere
        pygame.draw.rect(aken, self.PUNANE, self.rect)
        pygame.draw.rect(aken, self.MUST, self.rect, 2) # Must piirjoon ümber kere

        # 3. Kabiin/Klaas (helesinine osa auto peal)
        kabiin_rect = pygame.Rect(self.rect.x + 8, self.rect.y + 25, 34, 35)
        pygame.draw.rect(aken, self.KLAAS, kabiin_rect)
        pygame.draw.rect(aken, self.MUST, kabiin_rect, 2) # Piirjoon kabiini ümber

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

        self.mang_kaib = False
        self.nupp_rect = pygame.Rect(230, 440, 180, 80)
        
        self.triibu_vahe = 150
        self.triibud = [[315, i * self.triibu_vahe] for i in range(10)]
        self.teksti_timer = 180

        # Loo auto objekt
        self.auto = Car(300, 800)

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

        if not self.mang_kaib:
            pygame.draw.rect(self.aken, self.VALGE, self.nupp_rect)
            pygame.draw.rect(self.aken, self.MUST, self.nupp_rect, 5)
            
            font = pygame.font.SysFont("Calibri", 60)
            tekst = font.render("PLAY", True, self.MUST)
            self.aken.blit(tekst, (self.nupp_rect.x + 30, self.nupp_rect.y + 10))
        else:
            # Kui mäng käib, joonistame auto
            self.auto.joonista(self.aken)

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
                    if not self.mang_kaib and self.nupp_rect.collidepoint(sündmus.pos):
                        self.mang_kaib = True
            
            self.uuenda_tausta()
            
            if self.mang_kaib:
                self.auto.liiguta()
                if self.teksti_timer > 0:
                    self.teksti_timer -= 1

            self.joonista()
            self.kell.tick(60)

if __name__ == "__main__":
    mang = McTrip()
    mang.run()