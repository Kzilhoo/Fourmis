
import math
import pants
import csv
import networkx as nx
import matplotlib.pyplot as plt


def moyenne(liste): 
    return sum(liste) / len(liste)

def variance(liste): 
    m=moyenne(liste)
    return moyenne([(x-m)**2 for x in liste])	
	
G=nx.Graph()
iterations = 5
nbBars = 60
noeuds = []
distances = []



#Récupération latitude / longitude
with open('open_pubs.csv', 'r') as csvfile:
    rows = csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)
    for row in rows:
        try:      
            longitude = float(row[6])
            latitude = float(row[7])
			#Ajout dans le tableau Noeuds
            noeuds.append((longitude, latitude))
        except:
            continue


# Calcul de la distance
def distance(a, b):
	#Rayon terrestre
    Rayon = 6378 
	#Conversion 
    longiRadian = (b[1] - a[1]) * math.cos( 0.5*(b[0]+a[0]) )
    latiRadian = b[0] - a[0]
    distance = Rayon * math.sqrt( longiRadian*longiRadian + latiRadian*latiRadian )
    return distance;
	
# On vient diviser la liste pour limiter les données
for i in range(iterations):
    population = noeuds[i*nbBars:(i+1)*nbBars]
    #Mise dans un set pour suppression des doublons puis mise en list pour récupération par world
    population = list(set(population))
  
    G.clear()
    monde = pants.World(population, distance)
    solver = pants.Solver()
    solution = solver.solve(monde)
    print("Distance parcourue", i, "=", solution.distance)
	#Ajout de la solution à la liste des distances
    distances.append(solution.distance)

    #Ajouts des noeuds, création et enregistrement du fichier
    G.add_edges_from([(edge.start, edge.end) for edge in solution.path])
    plt.close()
    nx.draw(G,node_color = "blue",with_labels = True)
    plt.pause(2)
    plt.title("Distance parcourue = %s" % solution.distance)
    plt.savefig("./graphiques/d_%s.png" % i, bbox_inches="tight")
    plt.show()
    
print("Distance moyenne parcourue = " + str(moyenne(distances)) + "kilomètres")
print("Distance médiane = " + str(variance(distances)))



