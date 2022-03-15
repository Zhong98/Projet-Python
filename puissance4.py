#!/usr/bin/python
# -*- coding: latin-1 -*-

#	Puissance 4
#	
#	joueur -1 : humain
#	joueur 1 : ordinateur
import random
		
RECOMPENSE = 100	# valeur absolue de la récompense (doit être > evaluation max)


def afficheJeu(etat):
	# affiche le jeu
	print("")
	for i in range(6):
		s = ' |'
		for j in range(7):
			if etat[i][j] == 1:
				s = s + ' X |'
			else:
				if etat[i][j] == -1:
					s = s + ' O |'
				else:
					s = s + '   |'
				
		print(s)
	
	print('-------------------------------')

	s = ' |'
	for j in range(7): 
		s = s + ' ' + str(j) + ' |'
	print(s + '\n')
	
def testFin( etat, joueur ):
	# Test si l'état est un état terminal
	# On peut utiliser la fonction d'évaluation 
	# pour savoir si le dernier coup était gagnant
	# et sinon tester le match nul
	
	ev = evaljoueur ( etat, -joueur ) 
	if ev == RECOMPENSE:
		return True	# le joueur a gagné => partie finie
	
	# test match nul
	n = 0
	for i in range(6):
		for j in range(7):
			if etat[i][j] == 0:
				return False
	# tout scanné sans trouver de trou => partie finie
	return True
	
def coupsPossibles(etat):
	"""
	Retourne la liste des coups possibles (indices de colonnes)
	"""
	coups = []
	for j in range(7):
		if etat[0][j] == 0:
			coups.append(j)
	return coups
	
def evaljoueur ( etat, joueur ):
	# Evalue la position d'un joueur (~ son score indépendamment de l'autre joueur)
	# retourne une valeur positive
	#  = RECOMPENSE si le joueur a gagné 
	#  = 0 si match nul
	#  sinon, on doit avoir 0 <= valeur < RECOMPENSE

	value = 0
	n = 0
	# eval le nb max d'alignes
	for i in range(6):
		for j in range(7):
			if etat[i][j] == joueur:
				# compte nb de jetons total
				n = n + 1
			
				# compte nb alignes
				k=1
				while k <= 4 and i+k < 6 and etat[i+k][j] == joueur:
					k = k + 1
				
				if k == 2:
					value = value + 1
				elif k==3:	
					value = value + 3
				elif k==4:
					value = value + RECOMPENSE

				
				k=1
				while k <= 4 and j+k < 7 and etat[i][j+k] == joueur:  
					k = k + 1
				
				if k == 2:
					value = value + 1
				elif k==3:	
					value = value + 3
				elif k==4:
					value = value + RECOMPENSE

				k=1
				while k <= 4 and i+k < 6 and j+k < 7 and etat[i+k][j+k] == joueur:
					k = k + 1
				if k == 2:
					value = value + 1
				elif k==3:	
					value = value + 3
				elif k==4:
					value = value + RECOMPENSE

				k=1
				while k <= 4 and i+k < 6 and j-k >= 0 and etat[i+k][j-k] == joueur: 
					k = k + 1
				
				if k == 2:
					value = value + 1
				elif k==3:	
					value = value + 3
				elif k==4:
					value = value + RECOMPENSE
			elif etat[i][j] != 0:
				n = n + 1
				
	# Il faut retourner RECOMPENSE si le joueur a gagné et 0 si match nul
	
	if value >= RECOMPENSE:
		# 4 jetons alignés => c'est gagné ! 
		value = RECOMPENSE 
	else:
		# pour avoir value = 0 en cas de match nul
		if n == 6*7:
			value = 0
	
	return value


def evaluation ( etat ): 
	# Fonction d'évaluation pour un jeu à somme nulle
	#	= evaljoueur(ordi) - evaljoueur(humain)
	# sauf si un des deux joueurs a gagné
	# dans ce cas, il faut retourner
	#	+RECOMPENSE si l'ordinateur a gagné
	#  -RECOMPENSE si l'ordinateur a perdu

	evalHumain = evaljoueur(etat, -1)
	evalOrdi = evaljoueur(etat, 1)
	
	if evalHumain == RECOMPENSE:
		return -RECOMPENSE 
	elif evalOrdi == RECOMPENSE:
		return RECOMPENSE
	else:
		return evalOrdi - evalHumain 
	

def jouerCoup( etat, coup , joueur ): 
	# Modifier l'état en jouant un coup 
	# et retourne True/False si le coup est/n'est pas possible

	if etat[0][coup] != 0:
		return False
	
	h = 0
	while h < 6 and etat[h][coup] == 0:
		h = h + 1 
	
	etat[h-1][coup] = joueur
	return True

def copieEtat(etat):
	"""
	 copie un état du jeu (pour pouvoir réfléchir en jouant des coups
	 sans modifier l'état réel de la partie)
	"""
	copie = [[0 for j in range(7)] for i in range(6)] 
	for i in range(6):
		for j in range(7):
			copie[i][j] = etat[i][j]
	return copie
	
    
def ordiJoue(etat, profondeur_max):	
	
	coups = coupsPossibles(etat)
	meilleurCoup = 0
	valeur = -RECOMPENSE - 1 
	alpha = -RECOMPENSE - 1
	for coup in coups: 
		etatvirtuel = copieEtat(etat) 
		jouerCoup(etatvirtuel, coup , joueur) 
		minimax = valeurAlpha(etatvirtuel, -1, 1, profondeur_max, alpha, RECOMPENSE+1) 
		if minimax > valeur: 
			valeur = minimax
			meilleurCoup = coup
		if valeur > alpha:
			alpha = valeur
	if minimax==RECOMPENSE:
		print("l ordinateur va  gagner")
	if(minimax==-RECOMPENSE):
		print("l ordinateur va perdre")
	if(minimax>=evaluation(etatvirtuel)):
		print("l ordinateur va surement gagner")
	if(minimax<=evaluation(etatvirtuel)):
		print("l ordinateur va surement perdre")
	if(minimax==evaluation(etatvirtuel)):
		print("l ordinateur vise le nul")
	return meilleurCoup



def valeurMinimax( etat, joueur, profondeur, profondeur_max ):
	"""
	Retourne la valeur minimax d'un noeud avec un certain état
	dans lequel c'est à joueur de jouer
	"""
		
	
	global nbNoeudsExplores 
	nbNoeudsExplores = nbNoeudsExplores + 1

	coups = coupsPossibles(etat) 

	if len(coups) == 0 or profondeur >= profondeur_max:
		valeur = evaluation(etat)
		return valeur
	if joueur == 1:
		valeur = -RECOMPENSE - 1
		for coup in coups:
			etatvirtuel = copieEtat(etat) 
			jouerCoup(etatvirtuel, coup , joueur) 
			minimax = valeurMinimax(etatvirtuel, -1, profondeur + 1, profondeur_max) 
			if minimax > valeur: 
				valeur = minimax
	else :
		valeur = RECOMPENSE + 1 
		for coup in coups: 
			etatvirtuel = copieEtat(etat) 
			jouerCoup(etatvirtuel, coup , joueur) 
			minimax = valeurMinimax(etatvirtuel, 1, profondeur + 1, profondeur_max) 
			if minimax < valeur: 
				valeur = minimax
	
	return valeur

def valeurAlpha( etat, joueur, profondeur, profondeur_max, alpha, beta):
	"""
	Retourne la valeur minimax d'un noeud avec un certain état
	dans lequel c'est à joueur de jouer
	"""
		
	# pour connaître le nombre total de noeuds explorés:
	global nbNoeudsExplores 
	nbNoeudsExplores = nbNoeudsExplores + 1

	coups = coupsPossibles(etat) 

	if len(coups) == 0 or profondeur >= profondeur_max:
		valeur = evaluation(etat)
		return valeur
	if joueur == 1:
		valeur = -RECOMPENSE - 1 
		for coup in coups:
			etatvirtuel = copieEtat(etat) 
			jouerCoup(etatvirtuel, coup , joueur) 
			minimax = valeurAlpha(etatvirtuel, -1, profondeur + 1, profondeur_max, alpha, beta)
			if minimax > valeur: 
				valeur = minimax
			if valeur >= beta: 
				return valeur 
			if valeur > alpha:
				alpha = valeur
	else :
		valeur = RECOMPENSE + 1
		for coup in coups: 
			etatvirtuel = copieEtat(etat) 
			jouerCoup(etatvirtuel, coup , joueur) 
			minimax = valeurAlpha(etatvirtuel, 1, profondeur + 1, profondeur_max, alpha, beta) 
			if minimax < valeur: 
				valeur = minimax
			if valeur <= alpha:
				return valeur 
			if valeur < beta:
				beta = valeur 
	
	return valeur


########## Programme principal ###############

# Etat initial : matrice de 0
etat = [[0 for j in range(7)] for i in range(6)]
 
# Choisir qui commence : 
joueur = int(input('Qui commence (-1 : humain, 1 : ordinateur) ? '))

# Boucle de jeu
while not testFin( etat, joueur ):
	
	afficheJeu(etat)
	
	if joueur == -1:
		# tour de l'humain
		ok = False
		while not ok: 
			coup = int(input(' quelle colonne ? '))
			ok = jouerCoup(etat, coup, joueur)
						
	else: 
		# tour de l'Ordinateur
		
		nbNoeudsExplores = 0

		coup = ordiJoue( etat, 7)
		print("(apres une reflexion basee sur l\'exploration de " + str(nbNoeudsExplores) + " noeuds)")
		jouerCoup(etat,coup, joueur )
	
	
	# passer à l'autre joueur:
	joueur = -joueur


afficheJeu(etat)

r = evaluation( etat )
if r > 0:
	print( '** Ordinateur a gagné  **')
elif r == 0:
	print(' Match nul ! ')
else:
	print( '** BRAVO, ordinateur a perdu **')

