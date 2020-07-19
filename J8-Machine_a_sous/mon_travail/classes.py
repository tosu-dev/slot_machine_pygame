import pygame
import random as rand
import pickle

class Machine(pygame.sprite.Sprite):

    pygame.init()

    def __init__(self):
        '''
        '''

        super().__init__()

        # jetons
        self.jetons = 0 # a la fin du lancement
        self.default_all_jetons = 50 # jetons donné au début du jeu
        self.all_jetons = 0 # nombre de jetons du joueur (enregister dans la ficher 'jetons')
        self.prix_lancer = 5 # le prix du lancer

        # fruits + images
        self.dict_fruits = {'orange': pygame.image.load('mon_travail/assets/orange.png'),
                            'cerise': pygame.image.load('mon_travail/assets/cerise.png'), 
                            'ananas': pygame.image.load('mon_travail/assets/ananas.png'), 
                            'pasteque': pygame.image.load('mon_travail/assets/pasteque.png'), 
                            'pomme_dore': pygame.image.load('mon_travail/assets/pomme_dore.png')}
        
        # slots
        self.slots = [None,
                    None, 
                    None] # slots qui va conternir les fruits
        self.slots_line = 257 # la ligne en pixel des slots
        self.slots_list = [(227, self.slots_line), 
                        (329, self.slots_line), 
                        (429, self.slots_line)] # les coord des slots

        # image de la machine a sous
        self.image = pygame.image.load('mon_travail/assets/slot.png')
        self.rect = self.image.get_rect()

        # sons
        self.son_lancement = pygame.mixer.Sound('mon_travail/sounds/lancement.wav')
        self.son_slots = [pygame.mixer.Sound('mon_travail/sounds/pop0.wav'),
                        pygame.mixer.Sound('mon_travail/sounds/pop1.wav'),
                        pygame.mixer.Sound('mon_travail/sounds/pop2.wav')]
        self.son_jackpot = pygame.mixer.Sound('mon_travail/sounds/jackpot.ogg')
        self.son_perdu = pygame.mixer.Sound('mon_travail/sounds/lose.ogg')
        self.son_end = pygame.mixer.Sound('mon_travail/sounds/game_over.ogg')


    def get_jetons(self):
        '''
        Charge le fichier contenant le nombre de jetons dans la variable 'all_jetons'
        '''

        with open('jetons', 'rb') as jetons_file:
            user_jetons = pickle.Unpickler(jetons_file)
            self.all_jetons = user_jetons.load()
            jetons_file.close()

    def fruit_aleatoire(self):
        '''
        Tire au hasard un fruit parmis la liste de fruit de la machine
        '''
        pourcent = rand.randint(1,100) # nombre aléatoire entre 1 et 100

        if 1 <= pourcent <= 40: # 40%
            fruit = 'orange'

        elif 41 <= pourcent <= 65: # 25%
            fruit = 'cerise'

        elif 66 <= pourcent <= 85: # 20%
            fruit = 'ananas'

        elif 86 <= pourcent <= 95: # 10%
            fruit = 'pasteque'

        else: # 5%
            fruit = 'pomme_dore'

        return fruit

    def lancement(self):
        '''
        Lance la roulette et mets dans les slots de la machine
        3 fruis au hasard
        '''
        self.jetons = 0 # remet a 0 le nombre de jeton gagné
        self.all_jetons -= self.prix_lancer # le cout du lancement vaut 5 jetons

        for i in range(3):
            self.slots[i] = self.fruit_aleatoire()

        return self.slots

    def verification(self, liste_machine):
        '''
        vérifie s'il y a dans la liste en paramètre, 3 fois le même fruit ou non
        et renvoie True ou False selon oui ou non
        '''

        if (fruit := liste_machine[0]) == liste_machine[1] == liste_machine[2]: # s'il gagne
            
            # on regarde quel est le fruit
            if fruit == 'orange':
                self.jetons = 5

            elif fruit == 'cerise':
                self.jetons = 15

            elif fruit == 'ananas':
                self.jetons = 50

            elif fruit == 'pasteque':
                self.jetons = 150

            else: # pomme dore
                self.jetons = 1_000

            # on ajoute au nombre de jetons totaux, le nombre de jetons gagné (+ ce qu'il a dépensé)
            self.all_jetons += self.jetons + self.prix_lancer

            return True

        return False
