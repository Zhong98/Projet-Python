"""
	Jeu des bâtonnets 
	
	joueur = 1  => ordinateur
	joueur = -1 => humain
"""
import math
# Constantes globales

# RECOMPENSE = valeur donnée à un état terminal dans une partie gagnée
# si la partie est perdue, la valeur est -RECOMPENSE.
# Toutes les valeurs minimax sont comprises dans [-RECOMPENSE, RECOMPENSE]
RECOMPENSE = 1	


def affiche (N):
        # Affichage du jeu
        s = ""
        for i in range(N):
                s = s + "|"
        print(s)
	
def humainJoue(N):
        # Retourne le coup joué par l'humain
        coups = coupsPossibles(N)
        print("choix possibles : ")
        print(coups)

        n = None
        while n not in coups:
                n = int(input("combien de bâtonnets ? "))

        return n


def ordiJoue(N):
        # Retourne le coup joué par l'ordinateur
        l = coupsPossibles(N)
        # Détermination du meilleur coup
        val = -RECOMPENSE-1
        #meilleurCoup=1
        for coup in l :
                #evalluation = valeurMinimax( N - coup, -1*joueur )
                evalluation = Alphabeta( N - coup, -joueur, -2,2 )
                if (evalluation >= val) :
                        val = evalluation
                        meilleurCoup = coup 
        if val==1:
                print("le joueur va perdre")
        else:
                print("le joueur va probablement gagné")
        return meilleurCoup


def coupsPossibles(N):
        coups = []
        for i in range(1,4):
                if i <= N:
                        coups.append(i)
        return coups




def valeurMinimax( N, joueur ):
        """
        Retourne la valeur minimax d'un noeud avec N batônnets
        dans lequel c'est à joueur de jouer
	
        Si le joueur précédent a perdu (N=0), 
        retourne -RECOMPENSE si humain a gagné ou RECOMPENSE si ordi a gagné
        """
        if (N==0) :
                if  (joueur==1) :
                        val = RECOMPENSE
                else :
                        val = -RECOMPENSE
        else :
                l = coupsPossibles(N)
                if (joueur==1) :
                        val = -200
                        for coup in l :
                                evalluation = valeurMinimax( N - coup, -1*joueur )
                                val=max(evalluation,val)
                else :
                        val = 200
                        for coup in l :
                                evalluation = valeurMinimax( N - coup,  -1*joueur )
                                val=min(evalluation,val)
                
        # pour connaître le nombre total de noeuds explorés:
        global nbNoeudsExplores
        nbNoeudsExplores = nbNoeudsExplores + 1

        return val


def Alphabeta(N, joueur, alpha, beta):
        if (N==0) :
                if  (joueur==1) :
                        val = RECOMPENSE
                else :
                        val = -RECOMPENSE
        else :
                l = coupsPossibles(N)
                if (joueur==1) :
                        val = -200
                        for coup in l :
                                evalluation = Alphabeta( N - coup,  -1*joueur, alpha, beta )
                                val=max(evalluation,val)
                                if val >= beta:
                                        return val
                                alpha = max(alpha,val)                                                             
                else :
                        val = 200
                        for coup in l :
                                evalluation = Alphabeta( N - coup,  -1*joueur, alpha, beta  )
                                val=min(evalluation,val)
                                if alpha >= val:
                                        return val
                                beta = min(beta,val) 

        global nbNoeudsExplores
        nbNoeudsExplores = nbNoeudsExplores + 1

        return val


######### Programme principal ##########

# Etat initial
N = 27

# Qui commence ?
joueur = int(input("Qui commence ? (1 pour ordinateur, -1 pour humain) "))

# Boucle de jeu (tant que la partie n'est pas finie)
while N > 0:
        #afficher l'état du jeu:
        affiche(N)
        if joueur == -1:
                n = humainJoue(N)
        else:
                nbNoeudsExplores = 0
                n = ordiJoue(N)
                print('ordi a pris :',n)
                print("(après une réflexion basée sur l'exploration de " + str(nbNoeudsExplores) + " noeuds)")
			
        # jouer le coup
        N = N - n
	
        # passer à l'autre joueur:
        joueur = -joueur

# affichage final:
affiche(N)
if joueur==1:
        print("PERDU (ordi a gagné) !")
else:
        print("GAGNE (ordi a perdu) !")
	

