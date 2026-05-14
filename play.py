import pygame
import sys
class Play(pygame, sys):
    # Algseadistus
    pygame.init()
    LAAIUS, KORGUS = 640, 960
    aken = pygame.display.set_mode((LAAIUS, KORGUS))
    pygame.display.set_caption("McTrip")

    # Värvid
    VALGE = (255, 255, 255)
    MUST = (0, 0, 0)
    KOLLANE = (255, 204, 0)

    # Nupu seaded
    nupp_rect = pygame.Rect(230, 240, 175, 87)
    mang_kaib = False

    # Mängu põhitsükkel
    while True:
        for sündmus in pygame.event.get():
            if sündmus.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Kontrollime hiirevajutust
            if sündmus.type == pygame.MOUSEBUTTONDOWN:
                if nupp_rect.collidepoint(sündmus.pos):
                    mang_kaib = True

        # Joonistamine
        aken.fill(VALGE) # Nüüd värvib kogu akna valgeks

        if not mang_kaib:
            # Joonistame nupu
            pygame.draw.rect(aken, VALGE, nupp_rect)
            pygame.draw.rect(aken, MUST, nupp_rect, 5) # Outline
            
            font = pygame.font.SysFont("Calibri", 75)
            tekst = font.render("PLAY", True, MUST)
            # Paneme teksti nupu sisse (veidi nihutatult)
            aken.blit(tekst, (nupp_rect.x + 15, nupp_rect.y + 5))
        else:
            # Siia tuleb mängu sisu
            font = pygame.font.SysFont("Calibri", 32)
            soit_tekst = font.render("Welcome to McTrip", True, MUST) # Muutsin MUSTAKS, et valgel taustal näha oleks
            aken.blit(soit_tekst, (50, 200))

        pygame.display.flip()