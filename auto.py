import pygame
import random

BREITE = 1280
HOEHE = 480
FPS = 25
HOECHSTGESCHWINDIGKEIT = 100
LEBEN = 3
PUNKTE = 0
MAIN = True
TITEL = True
GAME = False

pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Reinhardtsgrimma Racer")
clock = pygame.time.Clock()

pygame.mixer.music.load('audio/musik.ogg')

print("\n\n\n\n\n*** Nutze die Cursor-Tasten (rechts und links), SPACE, und Escape zum Beenden.\n\nHintergrundgrafik von opengameart.org, Auto-Sprite von pixeljoint.com.png.\n\nMusik von Chris Hülsbeck.")

def hiscorecheck(punkte):
    import urllib.request, json
    with urllib.request.urlopen("https://chartophylakeion.de/racerhigh.json") as url:
        scores = json.loads(url.read().decode())
    if punkte > scores[9][1]:
        return True
    return False
def hiscoreeintrag(score):
    hintergrundfarbe = SCREEN.get_at((0,0))[:3]
    textfarbe = (bool(hintergrundfarbe[0]) ^ bool(255), bool(hintergrundfarbe[1]) ^ bool(255), bool(hintergrundfarbe[2]) ^ bool(255))
    input = True
    font = pygame.font.SysFont(None, int(HOEHE/10))
    anzeige = font.render("Highscore-Eintrag! Gib deinen Namen ein!", True, textfarbe)
    SCREEN.blit(anzeige, (BREITE/2-(anzeige.get_rect().size[0]/2),HOEHE-2*(HOEHE/10)))
    font = pygame.font.SysFont(None, int(2*HOEHE/10))
    text = ""
    while input:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text =  text[:-1]
                elif event.unicode.isalnum():
                    text += event.unicode
        hintergrundfarbe = SCREEN.get_at((0,0))[:3]
        text_surface = font.render(text, True, hintergrundfarbe)
        pygame.draw.rect(SCREEN,hintergrundfarbe,(BREITE/2-150,HOEHE-(HOEHE/8),300,2*HOEHE/10+16))
        pygame.draw.rect(SCREEN,textfarbe,(BREITE/2-(text_surface.get_rect().size[0]/2),HOEHE-(HOEHE/8),text_surface.get_rect().size[0],100))
        SCREEN.blit(text_surface, (BREITE/2-(text_surface.get_rect().size[0]/2),HOEHE-(HOEHE/8)))
        pygame.display.flip()
        if len(text) == 3:
            input = False
    import requests
    url = 'https://chartophylakeion.de/racerhigh-server.php?name=' + text + '&score=' + str(score)
    json = { text:score }
    x = requests.post(url, json = json)
    return text
def hiscoredisplay():
    hintergrund.update(0)
    hintergrundfarbe = SCREEN.get_at((0,0))[:3]
    textfarbe = (bool(hintergrundfarbe[0]) ^ bool(255), bool(hintergrundfarbe[1]) ^ bool(255), bool(hintergrundfarbe[2]) ^ bool(255))
    SCREEN.fill(hintergrundfarbe)
    hintergrund.update(0)
    import urllib.request, json
    with urllib.request.urlopen("https://chartophylakeion.de/racerhigh.json") as url:
        hiscores = json.loads(url.read().decode())
    font = pygame.font.SysFont(None, int(HOEHE/12))

    i = 0
    for eintrag in hiscores:
        text_surface = font.render(str(i+1) + ". " + eintrag[0], True, textfarbe)
        SCREEN.blit(text_surface, (BREITE/2-BREITE/10,HOEHE/10+i*HOEHE/12))
        text_surface = font.render(str(eintrag[1]), True, textfarbe)
        SCREEN.blit(text_surface, (BREITE/2+BREITE/10,HOEHE/10+i*HOEHE/12))
        i += 1
    pygame.display.flip()
class Hintergrund():
    def __init__(self):
        self.hintergrund1 = pygame.image.load('auto-h1.png') # das ist der obere Teil des Hintergrunds (Wolken)
        self.hintergrund2 = pygame.image.load('auto-h2.png') # das der untere (Häuser)
        self.hintergrund1_breite = self.hintergrund1.get_size()[0]
        self.hintergrund2_breite = self.hintergrund2.get_size()[0]
        self.hintergrund1_verschiebung, self.hintergrund2_verschiebung = 0,0
    def update(self,speed):
        self.hintergrundfarbe = SCREEN.get_at((0,0))[:3] # hole nur die ersten 3 Werte des Farbarrays (=RGB-Wert), der Alpha-Kanal (vierter Wert) fliegt raus
        SCREEN.fill(self.hintergrundfarbe) # mit der Farbe des Pixels bei (0,0) fülle ich den ganzen Bildschirm
        self.speed = speed

        horizontal = -self.hintergrund1_breite
        while horizontal < BREITE + self.hintergrund1_breite:
            SCREEN.blit(self.hintergrund1, (self.hintergrund1_verschiebung + horizontal,0))
            horizontal += self.hintergrund1_breite
        horizontal = -self.hintergrund2_breite
        while horizontal < BREITE + self.hintergrund2_breite:
            SCREEN.blit(self.hintergrund2, (self.hintergrund2_verschiebung + horizontal,100))
            horizontal += self.hintergrund2_breite
        self.hintergrund1_verschiebung += (0.1 + self.speed)
        self.hintergrund2_verschiebung += self.speed * 4
        if abs(self.hintergrund1_verschiebung) > self.hintergrund1_breite:
            self.hintergrund1_verschiebung = 0
        if abs(self.hintergrund2_verschiebung) > self.hintergrund2_breite:
            self.hintergrund2_verschiebung = 0

class Karre(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('auto.png')
        self.rect = self.image.get_rect()
        self.autogroesse = self.image.get_size()
        self.positionx = (BREITE / 2) - (self.autogroesse[0] / 2)
        self.positiony = HOEHE * 0.9 - self.autogroesse[1]
        self.abhaudurchlauf = 1 # Hilfsvariable = Faktor für Geschwindigkeitserhöhung, wenn das Auto nach Überschreitung der Höchstgeschwindigkeit rechts oder links rausfährt
        self.restjump = 0
        self.jumpziel = 0
    def update(self, speed):
        ''' Ein Update für das Auto-Sprite brauche ich eigentlich nur für den Fall, dass sich die Richtung ändert oder es links oder recht aus dem Bild rausfährt.
        Die Geschwindigkeit brauche ich nur für den Fall, dass es links oder rechts rausfahren soll.'''
        self.speed = speed
        if self.speed < -HOECHSTGESCHWINDIGKEIT/20 or self.speed > HOECHSTGESCHWINDIGKEIT/20:
            self.positionx = self.positionx - (self.abhaudurchlauf * self.speed)
            self.abhaudurchlauf += 0.05
        elif int(self.positionx) < int((BREITE / 2) - (self.autogroesse[0] / 2)) or int(self.positionx) > int((BREITE / 2) - (self.autogroesse[0] / 2)):
            xdifferenz = int(self.positionx - ((BREITE / 2) - (self.autogroesse[0] / 2)))
            self.positionx -= xdifferenz/5 # Das passiert, wenn die Höchstgeschwindigkeit nicht (mehr) erreicht/überschritten wurde, aber das Auto nicht an seiner ursprünglichen X-Position ist.

        if self.restjump > 0:
            jumpetappe = self.autogroesse[1] / 6 + ((self.positiony - self.jumpziel) / 20)
            self.positiony -= jumpetappe
            self.restjump -= jumpetappe
        elif self.positiony < HOEHE * 0.9 - self.autogroesse[1]:
            self.fallstrecke = abs(self.positiony - self.jumpziel)
            self.positiony = self.positiony + (self.autogroesse[1] / 6 + self.fallstrecke / 20)
        if self.positiony > HOEHE * 0.9 - self.autogroesse[1]:
            self.positiony = HOEHE * 0.9 - self.autogroesse[1]

        self.rect.topleft = ( self.positionx, self.positiony )

    def sprung(self):
        if self.positiony > HOEHE * 0.9 - (2 * self.autogroesse[1]):
            self.restjump = 2.5 * self.autogroesse[1] # sprunghöhe = 2,5 mal Autohöhe
            self.jumpziel = self.positiony - self.restjump
            pygame.mixer.Sound.play(pygame.mixer.Sound('audio/jump.ogg'))
        else:
            self.restjump = 0
            self.jumpziel = 0

class Monster(pygame.sprite.Sprite):
    def __init__(self,monster,auto):
        pygame.sprite.Sprite.__init__(self)
        self.images = monster
        self.index = 0
        self.image = self.images[self.index]
        self.flipped = 0

        self.rect = self.image.get_rect()

        self.monsterspeed = 4
        self.uebersprungen = False

        if hintergrund.speed < 0:
            self.ix = BREITE
            self.flipped = 0
        elif hintergrund.speed > 0:
            self.ix = -self.image.get_rect().size[0]
            self.flipped = 1

        self.ypsilon = HOEHE * 0.9 - auto.autogroesse[1] + auto.autogroesse[1]
        self.rect.bottomleft = self.ix, self.ypsilon
    def update(self,auto):
        self.index += 0.5
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)]

        xdisplacement = 4 * auto.speed
        if self.flipped == 1:
            xdisplacement += self.monsterspeed
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            xdisplacement -= self.monsterspeed

        self.ix += xdisplacement

        xcheck = int (self.ix / 10) * 10
        if int(auto.positionx) > xcheck and int(auto.positionx) < xcheck + 10 and not self.uebersprungen:
            global PUNKTE
            PUNKTE += int(abs(auto.speed * 20))
            self.uebersprungen = True
            print ("Übersprungen!!!!" + str(PUNKTE))

        self.rect.bottomleft = self.ix, self.ypsilon

class Powerup(pygame.sprite.Sprite):
    def __init__(self,auto):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("etc/powr1.png"), pygame.image.load("etc/powr2.png"), pygame.image.load("etc/powr3.png"), pygame.image.load("etc/powr4.png"), pygame.image.load("etc/powr5.png")]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        if hintergrund.speed < 0:
            self.ix = BREITE
            self.flipped = 0
        else:
            self.ix = -self.image.get_rect().size[0]
            self.flipped = 1
        self.ypsilon = HOEHE * 0.9 - auto.autogroesse[1] + auto.autogroesse[1]
        self.rect.bottomleft = self.ix, self.ypsilon
    def update(self):
        self.index += 0.5
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)]
        if self.flipped == 1:
            self.image = pygame.transform.flip(self.image, True, False)

        xdisplacement = hintergrund.speed * 4

        self.ix += xdisplacement

        if self.ix < -self.image.get_rect().size[0] or self.ix > BREITE + self.image.get_rect().size[0]:
            self.kill()

        self.rect.bottomleft = self.ix, self.ypsilon

def titel():
    idle = 0
    global TITEL, GAME
    while TITEL:
        idle += clock.tick(FPS)
        if idle < 3000:
            SCREEN.fill(hintergrundfarbe)
            hintergrund.update(0)
            SCREEN.blit(logo, (logopositionx,logopositiony))
            pygame.display.flip()
        elif idle < 6000:
            hiscoredisplay()
        else:
            idle = 0

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.fadeout(3000)
                    pygame.time.wait(3000)
                    pygame.quit()
                    exit()
                idle = 0
                TITEL = False
                GAME = True
def game():
    running = True
    global TITEL, GAME, LEBEN, PUNKTE
    maxmonster = 5 # wie viele verschiedene Monster aktuell da sind
    maxframes = 10 # wie viele Frames maximal pro Monster da sind
    maxextras = 1 # extras = andere Objekte, wie Powerup
    maxextraf = 5 # max. Frames in den Extras
    monster = [[0 for x in range(maxframes)] for y in range(maxmonster)]
    extras = [[0 for x in range(maxextraf)] for y in range(maxextras)]
    monster[0] = [pygame.image.load("monster/chum/chum1.png"), pygame.image.load("monster/chum/chum2.png"), pygame.image.load("monster/chum/chum3.png"), pygame.image.load("monster/chum/chum4.png"), pygame.image.load("monster/chum/chum5.png"), pygame.image.load("monster/chum/chum6.png")]
    monster[1] = [pygame.image.load("monster/runn/runn1.png"), pygame.image.load("monster/runn/runn2.png"), pygame.image.load("monster/runn/runn3.png"), pygame.image.load("monster/runn/runn4.png"), pygame.image.load("monster/runn/runn5.png"), pygame.image.load("monster/runn/runn6.png"), pygame.image.load("monster/runn/runn7.png"), pygame.image.load("monster/runn/runn8.png")]
    monster[2] = [pygame.image.load("monster/radf/radf1.png"), pygame.image.load("monster/radf/radf2.png"), pygame.image.load("monster/radf/radf3.png"), pygame.image.load("monster/radf/radf4.png"), pygame.image.load("monster/radf/radf5.png"), pygame.image.load("monster/radf/radf6.png"), pygame.image.load("monster/radf/radf7.png"), pygame.image.load("monster/radf/radf8.png")]
    monster[3] = [pygame.image.load("monster/kick/kick1.png"), pygame.image.load("monster/kick/kick2.png"), pygame.image.load("monster/kick/kick3.png"), pygame.image.load("monster/kick/kick4.png"), pygame.image.load("monster/kick/kick5.png"), pygame.image.load("monster/kick/kick6.png"), pygame.image.load("monster/kick/kick7.png"), pygame.image.load("monster/kick/kick8.png")]
    monster[4] = [pygame.image.load("monster/runn/runn1.png"), pygame.image.load("monster/runn/runn2.png"), pygame.image.load("monster/runn/runn3.png"), pygame.image.load("monster/runn/runn4.png"), pygame.image.load("monster/runn/runn5.png"), pygame.image.load("monster/runn/runn6.png"), pygame.image.load("monster/runn/runn7.png"), pygame.image.load("monster/runn/runn8.png")]

    all_sprites = pygame.sprite.Group()
    monsti_sprites = pygame.sprite.Group()
    extras_sprites = pygame.sprite.Group()
    speed = 0 # zu Beginn bewegt sich der Hintergrund nicht
    auto = Karre() # initialisiere das Auto
    all_sprites.add(auto) # nimm das Auto in die Sprite-Gruppe auf
    flipped = 0 # Indikator, ob das Auto-Sprite rechts oder links (flipped = 1) herum fährt

    monstercooldown = 0
    while running:
        if monstercooldown > 0:
            monstercooldown = int(monstercooldown-1)
        clock.tick(FPS)
        hintergrund.update(speed) # hiermit wird pro Frame ein Update (Scrollen) des Hintergrunds aufgerufen, die Geschwindigkeit wird übergeben

        if speed > 0 and flipped == 0: # Wenn Geschwindigkeit > 0 ist (Hintergrund bewegt sich nach rechts!) und das Auto noch nicht geflippt wurde:
            auto.image = pygame.transform.flip(auto.image, True, False) # Spiegele das Auto-Sprite horizontal!
            flipped = 1 # und setze flipped auf 1, damit es nicht wieder gespiegelt wird
        elif speed < 0: # Wenn Geschwindigkeit < 0 (Hintergrund bewegt sich nach links!),
            auto.image = pygame.image.load('auto.png') # nimm das normale Auto-Sprite
            flipped = 0 # und merke dir, dass es nicht geflippt ist
        zufall = random.random()
        if zufall < 0.1 and speed != 0 and monstercooldown == 0:
            monsti = Monster(monster[int(len(monster)*random.random())],auto)
            monsti_sprites.add(monsti)
            monstercooldown = int(30 - (PUNKTE / 300)) + int(-12 + 24 * random.random()) - int(abs(speed*2))
            if monstercooldown <=0:
                monstercooldown = 1
        elif zufall > 0.992 and speed != 0:
            powerup = Powerup(auto)
            extras_sprites.add(powerup)

        all_sprites.update(speed)
        all_sprites.draw(SCREEN)
        monsti_sprites.update(auto)
        monsti_sprites.draw(SCREEN)
        extras_sprites.update()
        extras_sprites.draw(SCREEN)

        if auto.positionx < -auto.autogroesse[0] or auto.positionx > BREITE + auto.autogroesse[0]: # Falls das Auto rechts oder links aus dem Bildschirm raus ist:
            pygame.mixer.Sound.play(pygame.mixer.Sound('audio/away.ogg'))
            hintergrundfarbe = SCREEN.get_at((0,0))[:3]
            textfarbe = (bool(hintergrundfarbe[0]) ^ bool(255), bool(hintergrundfarbe[1]) ^ bool(255), bool(hintergrundfarbe[2]) ^ bool(255))
            font = pygame.font.SysFont(None,64)
            anzeige1 = font.render("Viel Spaß in Norwegen!", True, textfarbe)
            font = pygame.font.SysFont(None,32)
            anzeige2 = font.render("In Reinhardtsgrimma hast Du " + str(int(PUNKTE)) + " Punkte erzielt.", True, textfarbe)
            y = HOEHE / 2 - ((anzeige1.get_rect().size[1] + anzeige2.get_rect().size[1]) / 2)
            SCREEN.blit(anzeige1, (BREITE/2 - anzeige1.get_rect().size[0]/2, y))
            SCREEN.blit(anzeige2, (BREITE/2 - anzeige2.get_rect().size[0]/2, y + anzeige1.get_rect().size[1]))
            pygame.display.flip()
            if hiscorecheck(PUNKTE):
                hiscoreeintrag(PUNKTE)
            pygame.time.wait(3000)
            running = False

        hintergrundfarbe = SCREEN.get_at((0,0))[:3]
        textfarbe = (bool(hintergrundfarbe[0]) ^ bool(255), bool(hintergrundfarbe[1]) ^ bool(255), bool(hintergrundfarbe[2]) ^ bool(255))

        treffer = pygame.sprite.spritecollide(auto,monsti_sprites,True)
        if treffer:
            pygame.mixer.Sound.play(pygame.mixer.Sound('audio/bumm.ogg'))
            LEBEN -= 1
            if LEBEN == 0:
                all_sprites.update(speed)
                monsti_sprites.update(auto)
                monsti_sprites.draw(SCREEN)
                pygame.mixer.Sound.play(pygame.mixer.Sound('audio/ende.ogg'))
                font = pygame.font.SysFont(None,64)
                anzeige1 = font.render("Du bist Schrott!", True, textfarbe)
                font = pygame.font.SysFont(None,32)
                anzeige2 = font.render("Aber immerhin hast Du " + str(int(PUNKTE)) + " Punkte erzielt.", True, textfarbe)
                y = HOEHE / 2 - ((anzeige1.get_rect().size[1] + anzeige2.get_rect().size[1]) / 2)
                SCREEN.blit(anzeige1, (BREITE/2 - anzeige1.get_rect().size[0]/2, y))
                SCREEN.blit(anzeige2, (BREITE/2 - anzeige2.get_rect().size[0]/2, y + anzeige1.get_rect().size[1]))
                pygame.display.flip()
                if hiscorecheck(PUNKTE):
                    hiscorename = hiscoreeintrag(PUNKTE)
                pygame.time.wait(3000)
                running = False
            PUNKTE += abs(auto.speed * 20)

        bonus = pygame.sprite.spritecollide(auto,extras_sprites,True)
        if bonus:
            pygame.mixer.Sound.play(pygame.mixer.Sound('audio/powerup.ogg'))
            LEBEN += 1

        font = pygame.font.SysFont(None,64)
        speedanzeige = font.render(str(int(abs(speed * 20))) + " km/h", True, textfarbe)
        SCREEN.blit(speedanzeige, (BREITE/100,HOEHE/20)) # platziere die Geschwindigkeitsanzeige

        font = pygame.font.SysFont(None,64)
        lebenanzeige = font.render("Blech: " + str(LEBEN), True, textfarbe)
        SCREEN.blit(lebenanzeige, (BREITE/100, HOEHE - HOEHE/10))

        font = pygame.font.SysFont(None,128)
        punkteanzeige = font.render(str(int(PUNKTE)), True, textfarbe)
        punktexpos = BREITE - punkteanzeige.get_rect().size[0] - BREITE/40
        SCREEN.blit(punkteanzeige, (punktexpos, HOEHE/20))

        pygame.display.flip()

        PUNKTE += abs(speed/50)
        ereignisse = pygame.event.get()
        for ereignis in ereignisse:
            if ereignis.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ereignis.type == pygame.KEYDOWN:
                if ereignis.key == pygame.K_LEFT:
                    speed += 0.25
                elif ereignis.key == pygame.K_RIGHT:
                    speed -= 0.25
                elif ereignis.key == pygame.K_ESCAPE:
                    font = pygame.font.SysFont(None,64)
                    anzeige1 = font.render("Mach's gut!", True, textfarbe)
                    font = pygame.font.SysFont(None,32)
                    anzeige2 = font.render("Du hast " + str(int(PUNKTE)) + " Punkte erzielt.", True, textfarbe)

                    y = HOEHE / 2 - ((anzeige1.get_rect().size[1] + anzeige2.get_rect().size[1]) / 2)

                    SCREEN.blit(anzeige1, (BREITE/2 - anzeige1.get_rect().size[0]/2, y))
                    SCREEN.blit(anzeige2, (BREITE/2 - anzeige2.get_rect().size[0]/2, y + anzeige1.get_rect().size[1]))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    running = False
                elif ereignis.key == pygame.K_SPACE and auto.positiony >= HOEHE * 0.9 - (2 * auto.autogroesse[1]):
                    auto.sprung()
    
    all_sprites.empty()
    monsti_sprites.empty()
    extras_sprites.empty()
    GAME = False
    TITEL = True

pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(.6)

while MAIN:
    if TITEL:
        hintergrund = Hintergrund()
        hintergrund.update(0)
        hintergrundfarbe = SCREEN.get_at((0,0))[:3]
        logo = pygame.image.load('logo.png')
        logogroesse = list(logo.get_size())

        if logogroesse[0] > BREITE:
            logogroesse[1] = int(logogroesse[1]/(logogroesse[0]/BREITE))
            logogroesse[0] = BREITE
        if logogroesse[1] > HOEHE:
            logogroesse[0] = int(logogroesse[0]/(logogroesse[1]/HOEHE))
            logogroesse[1] = HOEHE
        logo = pygame.transform.scale(logo, (logogroesse[0],logogroesse[1]))
        logopositionx = (BREITE / 2) - (logogroesse[0] / 2)
        logopositiony = HOEHE * 0.9 - logogroesse[1]
        titel()

    if GAME:
        LEBEN = 3
        PUNKTE = 0
        game()
