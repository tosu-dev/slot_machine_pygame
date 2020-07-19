# Continuer à faire des petits ajouts par ci par là !

import pygame
import random as rand
import pickle
import time
import classes
import os
os.system('cls')


# ___JEU___

# MACHINE
machine = classes.Machine()


# JETONS
# s'il n'existe pas de fichier pour enregistrer le nombre de jetons
if os.path.exists('jetons') == False:

    # on le créer avec les nombre de jetons par défaut
    with open('jetons', 'wb') as jetons_file:
        user_jetons = pickle.Pickler(jetons_file)
        user_jetons.dump(machine.default_all_jetons)
        jetons_file.close()

# s'il existe
else: 

    # on vérifie s'il y a des jetons
    with open('jetons', 'rb') as jetons_file:
        user_jetons = pickle.Unpickler(jetons_file)
        jetons = user_jetons.load()

        # s'il n'y en a plus
        if jetons <= 0:

            # on en remet par défaut
            with open('jetons', 'wb') as jetons_file_bis:
                user_jetons_bis = pickle.Pickler(jetons_file_bis)
                user_jetons_bis.dump(machine.default_all_jetons)
                jetons_file_bis.close()

        jetons_file.close()

# on récup les jetons
machine.get_jetons()

# BIENVENUE
print('\nBienvenue sur la machine à sous de tosu!')
print(f'\t- Vous avez {machine.all_jetons} jetons')
print(f'\t- Un lancer (barre espace) coûte {machine.prix_lancer} jetons')
print('\t- L\'apparition des fruits sont aléatoire mais avec des pourcentages différents')
print('\t- Les jetons gagnés sont plus ou moins élevé selon le fruit gagné')
print('Bonne chance l\'ami ! \n')

# FENETRE
pygame.init() # init
pygame.display.set_caption('Machine à sous')
screen = pygame.display.set_mode((800, 400)) 
screen.fill((255, 255, 255)) # bg blanc

#PYGAME
space_pressed = 0 # nombre de fois appuyé sur espace
running = True
while running:

    # image machine a sous
    screen.blit(machine.image, (0,0))
    pygame.display.flip()

    for event in pygame.event.get():

        # quitter le jeu
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("A la prochaine !")

            # enregistre les jetons dans un fichier
            with open('jetons', 'wb') as jetons_file:
                user_jetons = pickle.Pickler(jetons_file)
                user_jetons.dump(machine.all_jetons)
                jetons_file.close()


        # s'il appuis sur une touche...
        elif event.type == pygame.KEYDOWN:

            # si c'est sur espace, on lance la roulette
            if event.key == pygame.K_SPACE:
                space_pressed += 1 # +1



                machine.son_lancement.play() # on joue le son de la tirette
                time.sleep(0.5)
                machine_slots = machine.lancement() # on lance la machine

                # afficher les 3 fruits sur la ma chine a sous
                for i in range(len(machine.slots)):
                    time.sleep(0.5)
                    machine.son_slots[i].play()
                    time.sleep(0.25)
                    screen.blit(machine.dict_fruits[machine.slots[i]], machine.slots_list[i])
                    pygame.display.flip()

                # on vérifie s'il a gagné ou non
                verification = machine.verification(machine_slots)

                print(f'{space_pressed})\n>>> {machine_slots}')

                # si oui
                if verification: 
                    machine.son_jackpot.play()
                    print(f'\t- Vous avez gagné {machine.jetons} jetons !')
                    time.sleep(2.5)
                    print(f'\t- Vous avez {machine.all_jetons} jetons !\n')

                # si non
                else:
                    machine.son_perdu.play()
                    print('\t- Vous n\'avez rien gagné, dommage !')
                    time.sleep(1)
                    print(f'\t- Vous avez {machine.all_jetons} jetons !\n')

                    # s'il n'a plus de jetons, c'est la fin
                    if machine.all_jetons <= 0:
                        machine.son_end.play()
                        print("Vous n'avez plus un seul jetons, c'est la fin de la partie !")
                        time.sleep(1.5)
                        running = False
                        pygame.quit()
  
                