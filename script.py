from tkinter import *
import tkinter as tk
import tkinter.filedialog
import copy
import numpy as np
import time
from scipy.stats.mstats_basic import scoreatpercentile

# typographie et taille du texte
LARGE_FONT= ("Britannic Bold", 44)
TITLE=("Kunstler Script",130)
TEXT=("Britannic Bold",26)
TEXT_Fin=("Britannic Bold",16)
BUTTON=("Britannic Bold",20)
SUB_BUTTON=("Britannic Bold",15)
ENTER=("Britannic Bold",10)

global score 
global nb_naissance 

score = 0
nb_naissance=0

text_aide="Le jeu de la vie a été créé en 1970, et contrairement à ce que laisse entendre son nom il ne s’agit \n pas d’un jeu mais d’un automate cellulaire, c’est-à-dire une grille contenant des cellules, \n dont vous choisissez le placement et qui évoluent au cours du temps. \n Dans notre cas les cellules vivantes sont en noir et les mortes en blanc. \n Le passage d’un instant t à t+1 est appelé génération, et l’état de chaque cellule à un instant t \n dépend de son état à l’instant t-1 et de ses voisines immédiates. \n\n Les règles par défaut sont simples (mais vous pouvez les modifier !) :\n - Mort par isolement : de 0 à 1 cellule(s) voisine(s) vivante(s) \n - Mort par étouffement : de 4 à 8 cellules voisines \n - Survie : 2 cellules voisines vivantes \n - Naissance d’une nouvelle cellule : 3 voisines vivantes\n\n Et maintenant que vous savez tout, c'est à vous de jouer !"
text_regles="\n Vous allez choisir si la cellule meurt, survie ou naît en fonction du nombre de ses voisins. \n Pour cela veuillez mettre M, S ou N  pour mort, survie et naissance."


class Jeu_de_la_vie(tk.Tk):
    def __init__(self, *args,**kwargs):
        tk.Tk.__init__(self, *args,**kwargs)
        container=tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames={}
        
        for F in (StartPage,PageOne,PageTwo,PageThree,PageFour,PageQuit):
            frame=F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,column=0, sticky="nsew")
        self.show_frame(StartPage)
    
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.configure(bg='pale turquoise') #couleur de fond de la fenetre
        frame.tkraise()


class StartPage (tk.Frame): # ecran d'accueil
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Bienvenue sur le jeu de la vie", font=TITLE)
        label.config(fg='violet red') #couleur du texte
        label.config(background='pale turquoise') #couleur de fond du texte
        label.pack(pady = 40) # abaisser le titre
        
        # conteneur des boutons
        fen_boutons = tk.Frame(self, width=1000, height=600,)
        fen_boutons.configure(bg='pale turquoise') #couleur de fond de la fenetre 
        
        button1=tk.Button(fen_boutons,text="Démarrer",font=BUTTON ,command=lambda:controller.show_frame(PageOne))
        button1.config(background='orchid2') #couleur de fond 
        button1.place(relx=0,rely=1,anchor=tk.SW)
        
        button2=tk.Button(fen_boutons,text="Règles",font=BUTTON ,command=lambda:controller.show_frame(PageTwo))
        button2.config(background='orchid2') #couleur de fond 
        button2.place(relx=0.5,rely=1,anchor=tk.S)
        
        button3=tk.Button(fen_boutons,text="Quitter",font=BUTTON ,command=lambda:controller.show_frame(PageQuit))
        button3.config(background='orchid2') #couleur de fond du texte
        button3.place(relx=1,rely=1,anchor=tk.SE)
        
        fen_boutons.pack(pady=50)


class PageOne (tk.Frame): # page qui donne l'occasion de modifier les règles avant de commencer à jouer
    
    def __init__(self,parent,controller,):
        
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Souhaitez-vous : ", font=LARGE_FONT)
        label.config(background='pale turquoise') # couleur de fond du texte
        label.pack(pady = 40) # abaisser le titre
        
        # conteneur des boutons
        fen_boutons = tk.Frame(self, width=1000, height=600,)
        fen_boutons.configure(bg='pale turquoise') #couleur de fond de la fenetre 
        
        
        button1=tk.Button(fen_boutons,text="Jouer",font=BUTTON ,command=lambda:controller.show_frame(PageThree))
        button1.config(background='orchid2') #couleur de fond du texte
        button1.place(relx=0,rely=1,anchor=tk.SW)
        
        button2=tk.Button(fen_boutons,text="Modifier les règles",font=BUTTON ,command=lambda:controller.show_frame(PageFour))
        button2.config(bg='orchid2')
        button2.place(relx=0.5,rely=1,anchor=tk.S)
        
        button3=tk.Button(fen_boutons,text="Retour",font=BUTTON ,command=lambda:controller.show_frame(StartPage))
        button3.config(bg='orchid2')
        button3.place(relx=1,rely=1,anchor=tk.SE)
        
        fen_boutons.pack(pady=50)


class PageTwo (tk.Frame): # page affichant l'histoire et les règles régissant le jeu de la vie
    
    def __init__(self,parent,controller):
        
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Règles du jeu de la vie",font=LARGE_FONT)
        label.config(background='pale turquoise') # couleur de fond du texte
        label.pack(pady=40)
        label=tk.Label(self,text=text_aide,font=BUTTON,justify=LEFT) # affichage des règles du jeu de la vie
        label.config(background='pale turquoise') # couleur de fond du texte
        label.pack(pady=10,padx=10)
        
        # conteneur des boutons
        fen_boutons = tk.Frame(self, width=1000, height=600,)
        fen_boutons.configure(bg='pale turquoise') #couleur de fond de la fenetre 
        
        button1=tk.Button(fen_boutons,text="Retour",font=BUTTON ,command=lambda:controller.show_frame(StartPage))
        button1.config(bg='orchid2')
        button1.place(relx=0,rely=1,anchor=tk.SW)
        
        button2=tk.Button(fen_boutons,text="Jouer",font=BUTTON ,command=lambda:controller.show_frame(PageOne))
        button2.config(bg='orchid2')
        button2.place(relx=0.5,rely=1,anchor=tk.S)
        
        button3=tk.Button(fen_boutons,text="Quitter",font=BUTTON ,command=lambda:controller.show_frame(PageQuit))
        button3.config(bg='orchid2')
        button3.place(relx=1,rely=1,anchor=tk.SE)

        fen_boutons.pack(pady=50)


class PageThree (tk.Frame):
    
    def __init__(self,parent,controller):
        
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="JEU !",font=LARGE_FONT)
        label.config(background='pale turquoise') #couleur de fond du texte
        label.grid(row=0, sticky=N)
        
        #declaration des frames
        self.config(bg='pale turquoise')
        fen_jeu=tk.Frame(self)
        fen_jeu.configure(bg='pale turquoise') #couleur de fond de la fenetre
        
        fen_boutons = tk.Frame(self, width=1000, height=50,)
        fen_boutons.configure(bg='pale turquoise') #couleur de fond de la fenetre 
        fen_jeu_grille=tk.Frame(fen_jeu)
        fen_jeu_grille.configure(bg='pale turquoise') #couleur de fond de la fenetre 
        
        fen_jeu_button=tk.Frame(fen_jeu)
        fen_jeu_button.configure(bg='pale turquoise') #couleur de fond de la fenetre

        # les 2 couleurs à  utiliser
        couleurs = {0: "pale turquoise", 1: "black"}
        # dimensions du canevas
        can_width = can_height = 500
        # taille du tableau
        tab_row = tab_column = 50
        # taille d'une "case"
        size = can_width/tab_row
        # le tableau Ã  afficher
        global tableau 
        tableau = np.zeros((tab_row, tab_column))
        # création canevas
        can = Canvas(fen_jeu_grille, width=can_width, height=can_height)
        can.config(background='pale turquoise') #couleur de fond du canevas
        can.grid(row=1, column=0)
        
        
        def forme1():
        
            effacer()
            
            #clignotant
            
            tableau[24][25]=1    
            tableau[25][25]=1    
            tableau[26][25]=1
            
            afficher(tableau)
        
        def forme2():

            effacer()
            
            #block
            tableau[26][25]=1
            tableau[26][26]=1
            tableau[25][25]=1
            tableau[25][26]=1
        
            afficher(tableau)
            
        def forme3():

            effacer()
            
            #planeur
            tableau[5][6]=1
            tableau[6][7]=1
            tableau[7][5]=1
            tableau[7][6]=1
            tableau[7][7]=1
        
            afficher(tableau)
        
        def forme4():

            effacer()
        
            #vaisseau
            tableau[26][26]=1
            tableau[27][27]=1
            tableau[23][28]=1
            tableau[27][28]=1
            tableau[24][29]=1
            tableau[25][29]=1
            tableau[26][29]=1
            tableau[27][29]=1
        
            afficher(tableau)
        
        def effacer():
            
             for i in range(tab_column):
                
                 for j in range(tab_row):
                            
                    tableau[i][j]=0
                    
             afficher(tableau)
                 
            
        def afficher(tableau):
        
            """
            Fonction d'affichage du tableau ; 1 élément = 1 case
            La couleur de la "case" dépend de l'état de l'élement correspondant, 0 ou 1
            """
            can.delete(ALL) # ça c'est le graal au niveau des performances
            
            for i in range(tab_column):
        
                 for j in range(tab_row):
        
                      can.create_rectangle(i * size,j * size,i * size + size*0.7,j * size + size*0.7,fill = couleurs[tableau[i][j]])

        def modifierTableau(event):
        
            """
            Fonction appelée lors d'un clic gauche sur le canevas 
            Déterminer la correspondance entre la position horizontale
            de la souris et l'élément correspondant du tableau :
            evt.x est la position en x de la souris """
        
            pos_x = int(event.x / size)
            pos_y = int(event.y / size)

            # inverse la valeur de l'emplacement cliqué
        
            if tableau[pos_x][pos_y] == 0:
                tableau[pos_x][pos_y] = 1
            else:
                tableau[pos_x][pos_y] = 0
            # ré-afficher le tableau
            afficher(tableau)
            
        #calculs
        global rule
        rule = "MMSNMMMM" # règles par défaut

        def nb_neighbours(grid, tab_column, tab_row, xcell, ycell) : 				# fonction qui renvoie le nombre de voisines (cellules vivantes) d'une cellule donnée de coordonnées (xcell, ycell)
            neighbours=0

            for col in range(max(0, ycell-1), min(ycell+2, tab_column)) :
                for row in range(max(0, xcell-1), min(xcell+2, tab_row)) :
                    neighbours += grid[row][col]
            return neighbours - grid[xcell][ycell]
            

        def evolution(tableau, rule): # mise à  jour de la grille : modification de l'état des cellules
        
            global score
            global nb_naissance
        
            grid = copy.deepcopy(tableau)
            score = score +1 
        
            for col in range(0,tab_column):
                for row in range(0,tab_row): # on regarde chaque cellule du damier
                    neighbours = int(nb_neighbours(grid, tab_column, tab_row, row, col))
                    
                    if rule[neighbours] == 'N' :
                        nb_naissance=nb_naissance+1
                        tableau[row][col] = 1 # naissance

                    elif rule[neighbours] == 'M' :
                        tableau[row][col] = 0 # mort ou conservation
            return tableau
        
        def start(): # démarre l'évolution du jeu de la vie

            global run 
            run = 1
            fen_jeu_grille.after(1000, automatic)

        
        def stop() : # arrêt
        
            global run 
            run =  0

        def automatic() : # passage automatique d'une génération Ã  la suivante
        
            global rule
            global run
            global nb_naissance
        
            if run :
                global tableau
                tableau = evolution(tableau, rule)
                afficher(tableau)   
                fen_jeu_grille.after(1000, automatic)

        def next_step() : # passage à  la génération suivante au clic sur le bouton

            global tableau
            global nb_naissance
            tableau = evolution(tableau, rule)
        
            afficher(tableau) 
            
            
        def fin_jeu():
            global run 
            run =  0
            m=Tk()
            
            
            m.geometry('600x500')
            label=tk.Label(m,text="Résumé de la partie ",font=LARGE_FONT)
            label.config(fg='black') #couleur du texte
            label.grid(row=0,column=0)
            
            label=tk.Label(m,text="nombre de génération totale : ",font=TEXT_Fin)
            label.config(fg='green') #couleur du texte
            label.grid(row=1,column=0)
            
            label=tk.Label(m,text=score,font=TEXT_Fin)
            label.config(fg='green') #couleur du texte
            label.grid(row=1,column=1)
            
            label=tk.Label(m,text="nombre de naissance total : ",font=TEXT_Fin)
            label.config(fg='blue') #couleur du texte
            label.grid(row=2, column=0)
            
            label=tk.Label(m,text=nb_naissance)
            label.config(fg='blue',font=TEXT_Fin) #couleur du texte
            label.grid(row=2, column=1)
            
            b1 = Button(m, text ='Fermer',font=BUTTON, command = m.destroy)
            b1.config(background='pale turquoise') #couleur de fond du bouton
            b1.grid(row=3, column=0, pady=50)
               
        #-----------------------------------------------------
        # programme
        
        afficher(tableau)
        run = 0 
        
        # binding de la fonction modifierTableau sur le canevas
        
        can.bind("<Button-1>", modifierTableau)

        b2 = Button(fen_jeu_button, text ='Start',font=SUB_BUTTON, command = start)
        b2.config(background='orchid2') #couleur de fond du bouton
        b2.grid(row=1, column=2)
        
        b3 = Button(fen_jeu_button, text ='Stop',font=SUB_BUTTON, command = stop)
        b3.config(background='orchid2') #couleur de fond du bouton
        b3.grid(row=1, column=3)
        
        b4 = Button(fen_jeu_button, text ='Next step',font=SUB_BUTTON, command = next_step)
        b4.config(background='orchid2') #couleur de fond du bouton
        b4.grid(row=1, column=4)
        
        b5 = Button(fen_jeu_button, text ='Effacer tableau',font=SUB_BUTTON, command = effacer)
        b5.config(background='orchid2') #couleur de fond du bouton
        b5.grid(row=1, column=5)
        
        b6 = Button(fen_jeu_button, text ='fin de jeu',font=SUB_BUTTON, command = fin_jeu)
        b6.config(background='orchid2') #couleur de fond du bouton
        b6.grid(row=1, column=6)
        
        # barre de menu
        
        Monmenu = Menubutton(fen_jeu_grille, text='Figures predefinies') # Définit le menu
        Monmenu.grid(row=0, column=0)
        
        deroule = Menu(Monmenu, tearoff=0, activebackground='blue') # Définit la partie déroulante du menu
        deroule.add_command(label="Clignotant", command=forme1) # On ajoute des éléments 
        deroule.add_command(label="Cube", command=forme2) # au menu déroulant
        deroule.add_command(label="Planneur", command=forme3)
        deroule.add_command(label="Vaisseau", command=forme4)
        
        Monmenu.config(menu=deroule) # On joint le menu déroulant à  Monmenu

        fen_jeu.grid(row=1)

        fen_jeu_grille.grid(row=0)
        fen_jeu_button.grid(row=1)
        
        # conteneur des boutons
        
        button1=tk.Button(fen_boutons,text="Retour",font=BUTTON,command=lambda:controller.show_frame(StartPage))
        button1.config(background='orchid2') #couleur de fond du bouton
        button1.place(relx=0,rely=1,anchor=tk.SW)
        
        button3=tk.Button(fen_boutons,text="Quitter",font=BUTTON ,command=lambda:controller.show_frame(PageQuit))
        button3.config(background='orchid2') #couleur de fond du bouton
        button3.place(relx=1,rely=1,anchor=tk.SE)
        fen_boutons.grid(row=2, sticky=S)
        
        
class PageFour (tk.Frame): # page permettant de modifier les règles du jeu
    
    def __init__(self,parent,controller):
        
        tk.Frame.__init__(self,parent,)
        label=tk.Label(self,text="Règles du jeu",font=LARGE_FONT)
        label.config(background='pale turquoise') # couleur de fond du texte
        label.pack(pady=40)
        
        # explications
        label=tk.Label(self,text=text_regles,font=BUTTON,justify=LEFT) # affichage du texte expliquant comment choisir les règles
        label.config(background='pale turquoise') # couleur de fond du texte
        label.pack(pady = 90)

        # conteneur des saisies
        fen_saisie=tk.Frame(self)
        fen_saisie.configure(bg='pale turquoise') #couleur de fond de la fenetre
        
        global t
        t=0
        def confirmer():

            for i in range(9):
                choix[i] = str(e[i].get())
                if (choix[i] not in ['M','S', 'N']) :
                    e[i].delete(0, len(choix[i]))
                    global t
                    t=t+1
                    
            if t !=0 :
                button4.configure(bg='red')
            elif t==0 :
                button4.configure(bg='green')
            	    
            global rule
            rule = ''.join(choix)
            
            t=0
            
        e = [i for i in range(9)] 
        choix = [i for i in range(9)]
         
        for i in range(9):
            label=tk.Label(fen_saisie,text=format(i,"^5d"),font=BUTTON)
            label.config(background='pale turquoise') #couleur de fond du texte
            label.grid(row=0,column=i,padx=5,pady=5)
            
            #ENTRY fenetre de saisi
            e[i]=tk.Entry(fen_saisie,width=5)
            e[i].grid(row=1,column=i,padx=5,pady=5)
            
        fen_saisie.pack(pady=50)
        
        # conteneur des boutons
        fen_boutons = tk.Frame(self, width=1000, height=600,)
        fen_boutons.configure(bg='pale turquoise') #couleur de fond de la fenetre 
        
        button1=tk.Button(fen_boutons,text="Retour",font=BUTTON,command=lambda:controller.show_frame(PageOne))
        button1.config(background='orchid2') #couleur de fond du bouton
        button1.place(relx=0,rely=1,anchor=tk.SW)
        
        button2=tk.Button(fen_boutons,text="Jouer",font=BUTTON ,command=lambda:controller.show_frame(PageThree))
        button2.config(background='orchid2') #couleur de fond du bouton
        button2.place(relx=0.5,rely=1,anchor=tk.S)
        
        button3=tk.Button(fen_boutons,text="Quitter",font=BUTTON ,command=lambda:controller.show_frame(PageQuit))
        button3.config(background='orchid2') #couleur de fond du bouton
        button3.place(relx=1,rely=1,anchor=tk.SE)
        
        button4=tk.Button(fen_saisie, text='Valider',font=ENTER, command=confirmer)
        button4.config(background='VioletRed2') #couleur de fond du bouton
        button4.grid(row=2,column=4,padx=0,pady=0)

        fen_boutons.pack(pady=50)
        

class PageQuit (tk.Frame): # page qui demande confirmation avant de quitter
    
    def __init__(self,parent,controller):
        
        tk.Frame.__init__(self,parent,)
        label=tk.Label(self,text="Souhaitez vous quitter ?",font=LARGE_FONT)
        label.config(background='pale turquoise') #couleur de fond du texte
        label.pack(pady = 50)
        
        
        # conteneur des boutons
        fen_boutons = tk.Frame(self, width=1000, height=600,)
        fen_boutons.configure(bg='pale turquoise') #couleur de fond de la fenetre 
        
        button1=tk.Button(fen_boutons,text="Oui",font=BUTTON ,command=self.quit)
        button1.config(background='orchid2') #couleur de fond du bouton
        button1.place(relx=0,rely=1,anchor=tk.SW)
        
        button2=tk.Button(fen_boutons,text="Non",font=BUTTON ,command=lambda:controller.show_frame(StartPage))
        button2.config(background='orchid2') #couleur de fond du bouton
        button2.place(relx=1,rely=1,anchor=tk.SE)

        fen_boutons.pack(pady=50)
        
        
def main():
    app=Jeu_de_la_vie()
    app.attributes('-fullscreen', True) # mode plein ecran
    app.mainloop()

  
if __name__ == '__main__':

    main()

# pour les couleurs http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
