#coding: utf-8

import argparse
import random
import math
import copy
import ConfigParser


"""
Objetivo: 

"""

def get_args(): 
   parser = argparse.ArgumentParser(description='Seed e Numero de Iteracoes (niter)')
   parser.add_argument( '-s', '--seed', type=int, help='Seed', required=True)
   parser.add_argument( '-n', '--niter', type=int, help='Niter', required=True)
   args = parser.parse_args()
   seed = args.seed
   niter = args.niter
   return seed, niter

seed, Niter = get_args()

random.seed(seed)


#atributos do AG
"""  
tamanho #numero de genes do individuo
num #numero de individuos na populacao
lambdaa  #numero de individuos selecionados para cruzar
ring  #numero de individuos selecionados para o torneio
prob_cruzamento  #probabilidade de cruzamento
ngenes  #numero de genes do cruzamento 
prob_mutacao  #probabilidade de mutacao do individuo
cadeia  #cadeia de genes de colaboracao para a aplicacao do bonus
bonnus  #base da bonificacao (1,2,3,4)*bonus
fitn  #base do fitness (20,10,1,0)*fitness para FitEgo DC,CC,DD,CD ou FitGrupo CC,CD,DC,DD
nteste  #numero de individuos teste para o calculo do fitness
kgeracoes #numero de geracoes sem modificacao no fitness - criterio de parada
prob_mutacao_gene #probabilidade de mutacao de cada gene
"""

#Lê arquivo de configuracao

config = ConfigParser.ConfigParser()

config.read("config.ini")

tamanho = config.getint("myvars", "tamanho")
num = config.getint("myvars", "num")
lambdaa = config.getint("myvars", "lambdaa")
ring = config.getint("myvars", "ring")
prob_cruzamento = config.getfloat("myvars", "prob_cruzamento")
ngenes = config.getint("myvars", "ngenes")
prob_mutacao = config.getfloat("myvars", "prob_mutacao")
cadeia = config.getint("myvars", "cadeia")
bonnus = config.getint("myvars", "bonnus")
fitn = config.getint("myvars", "fitn")
nteste = config.getint("myvars", "nteste")
kgeracoes = config.getint("myvars", "kgeracoes")
prob_mutacao_gene = config.getfloat("myvars","prob_mutacao_gene")



# A funcao individuo cria um individuo formado por numeros inteiros aleatorios [0,9]
  
def individuo(min, max):
   
    return[random.randint(min, max) for i in range(tamanho)]

# A funcao Populacao cria novos individuos
  
def Populacao():
    
    return [individuo(0,9) for i in range(num)] 


# A funcao melhorIndividuo seleciona o melhor individuo dentre os individuos da população final
# neste caso, o critério de parada é o número de iterações. Portanto, a população 
# final é a população Niter*

def melhorIndividuo(populacao):

	vetor=[0 for i in range(len(populacao))]
    	
	i=0

	lista=[]

	while i < (len(populacao)):
    
    		vetor = [ (Totalfitness[i], populacao[i])] # Guarda em vetor* na forma [(score, [individuo])]  
   	
		lista.append(vetor)  
		
		i = i + 1	
	
	lista.sort()

	melhor=lista[(len(populacao)-1)]

	return melhor


def melhorFit(populacao):

	vetor=[0 for i in range(len(populacao))]
    	
	i=0

	lista=[]

	while i < (len(populacao)):
    
    		vetor = Totalfitness[i] # Guarda em vetor* na forma [(score, [individuo])] 
   	
		lista.append(vetor)  
		
		i = i + 1	
	
	lista.sort()

	melhor=lista[(len(populacao)-1)]

	return melhor




def calculaFitnessEgo(populacao):

	fitego=[0 for i in range(len(populacao))]

	i=0

	while i < (len(populacao)): #para cada individuo da populacao
			
		individuo_alvo=populacao[i]

		index_alvo=i

		index_teste = [0 for p in range(nteste)]

		individuo_teste = [0 for p in range(nteste)]

		k=0 
		while k < nteste: #seleciona os individuos teste

			index_teste=random.randint(0, (len(populacao)-1))

			while index_alvo == index_teste:
        			index_teste=random.randint(0, (len(populacao)-1))

			individuo_teste[k]=populacao[index_teste]

			k=k+1


		fitness = 0
		w=0
		while w < nteste: 

			ind_teste = individuo_teste[w]
			
			j=0
			while j < tamanho:
		
				if individuo_alvo[j] > 4 and ind_teste[j] < 5: # D C
					fitness += fitn*20 
				elif individuo_alvo[j] < 5 and ind_teste[j] < 5: # C C
					fitness += fitn*10 
				elif individuo_alvo[j] > 4 and ind_teste[j] > 4: # D D
					fitness += fitn*1 		
 				else:  # C D
					fitness += 0
					
				j=j+1 #fim for gene		

			w=w+1 #fim for nteste
		

			fitego[i] = copy.deepcopy(fitness)	

	
		i=i+1 #fim for populacao

	return fitego   
    
    	
	
def calculaFitnessGrupo(populacao):

	fitgrupo=[0 for i in range(len(populacao))]

	i=0

	while i < (len(populacao)): #para cada individuo da populacao
			
		individuo_alvo=populacao[i]

		index_alvo=i

		index_teste = [0 for p in range(nteste)]

		individuo_teste = [0 for p in range(nteste)]

		k=0 
		while k < nteste: #seleciona os individuos teste

			index_teste=random.randint(0, (len(populacao)-1))

			while index_alvo == index_teste:
        			index_teste=random.randint(0, (len(populacao)-1))

			individuo_teste[k]=populacao[index_teste]

			k=k+1

		fitness = 0
		w=0
		while w < nteste: 

			ind_teste = individuo_teste[w]
			
			j=0
			while j < tamanho:
		
				if individuo_alvo[j] < 5 and ind_teste[j] < 5: # C C
					fitness += fitn*20
				elif individuo_alvo[j] < 5 and ind_teste[j] > 4: # C D
					fitness += fitn*10
				elif individuo_alvo[j] > 4 and ind_teste[j] < 5: # D C
					fitness += fitn*1		
 				else:  # D D
					fitness += 0
					
				j=j+1 #fim for gene		

			w=w+1 #fim for nteste
		

			fitgrupo[i] = copy.deepcopy(fitness)	

	
		i=i+1 #fim for populacao

	return fitgrupo   
	

def calculaBonus(populacao):

	vetorbonus=[0 for i in range(len(populacao))]

	j=0
	while j < (len(populacao)):

		bonus = 0		
		contador = 0
		somavalor = 0

		individuo_alvo=populacao[j]
		

		for i in range(len(individuo_alvo)):
			if individuo_alvo[i] < 5:
				somavalor += individuo_alvo[i]
				contador += 1

				if contador == cadeia:

					media=float(somavalor/cadeia)

					somavalor=0
					contador=0
			
					if media >= 0 and media < 1:
						bonus += 4*bonnus
					elif media >= 1 and media < 2:
						bonus += 3*bonnus
					elif media >= 2 and media < 3:
						bonus += 2*bonnus
					else:
						bonus += bonnus
			else:
				contador = 0
			

		vetorbonus[j]=copy.deepcopy(bonus)	
	
		j=j+1 #fim for populacao

	return vetorbonus


def fitnessTotal(populacao):

	fitnessTotal = [0 for i in range(len(populacao))]

	j=0

	while j < len(populacao):

		fitnessTotal[j] = bonus[j] + grupo[j]
		
		j=j+1

	return fitnessTotal



def seleciona(populacao):

	populacao = populacao
	fitpopulacao = Totalfitness
	
	selecaopais = [0 for i in range(lambdaa)]

        pai=[]
	
	j=0
	while j < lambdaa:

		index = [i for i in range(len(populacao))] 

		indexIndividuo = random.sample(index,ring)

		maiorfitness=0	

		k=0
		while k < ring:
			
			if fitpopulacao[indexIndividuo[k]] > maiorfitness:
  			
				maiorfitness=fitpopulacao[indexIndividuo[k]]

				pai=populacao[indexIndividuo[k]]

			k=k+1
	
			selecaopais[j]=copy.deepcopy(pai)

		j=j+1


	return selecaopais


def cruzamento(selecao_pais):

	pais = selecao_pais


	filhos = [0 for i in range(len(pais))] 	
	
	t=lambdaa/2

	j=0
	while j < t:

		pai1=pais[j]
		pai2=pais[j+t]

	
		f1=pai1
		f2=pai2

		if random.random() <= prob_cruzamento:		
		
			index = [i for i in range(tamanho)]



			indexgene = random.sample(index,ngenes) #n genes para cruzar	

			k=0 #troca dos genes
			while k < ngenes:

				genepai1=pai1[indexgene[k]] #valor no gene x1
				genepai2=pai2[indexgene[k]]
			
        			diferenca = genepai1 - genepai2
        			n = math.fabs(diferenca) #modulo da diferenca

       				if n == 0: # se n é zero os genes sao iguais
  					novogene1 = genepai1
       				else:
					if n % 2 == 0: # se n é par, o novo gene é a mediana
 						if genepai1 > genepai2:
		        				novogene1=genepai2+n/2
                				else:
							novogene1=genepai1+n/2

           				else:  #se n é impar, o novo gene é um valor aleatorio entre os pontos medianos
						if genepai2 > genepai1:
							if random.random() <= 0.5:
								novogene1=genepai1+(n-1)/2
							else:
								novogene1=genepai2-(n-1)/2
						else:
							if random.random() <= 0.5:
								novogene1=genepai2+(n-1)/2
							else:
								novogene1=genepai1-(n-1)/2	
				novogene1 = int(novogene1)
		
		
				f1[indexgene[k]]=novogene1
				f2[indexgene[k]]=novogene1
		
				k=k+1 #fim for gene
	
 			filhos[j] = copy.deepcopy(f1)
			filhos[j+t] = copy.deepcopy(f2)

		else:
			filhos[j] = copy.deepcopy(f1)
			filhos[j+t] = copy.deepcopy(f2)

		j=j+1
		
	return filhos


def mutacao(novosfilhos):
  
	filhos = novosfilhos 
	
	j=0
	while j < lambdaa:

		filho1=filhos[j]

		f1=filho1

		if random.random() <= prob_mutacao: #probabilidade de mutacao do individuo

			for i in range(tamanho):

				if random.random() <= prob_mutacao_gene: #probabilidade de mutacao do gene

					index=i #escolha do gene para mutacao
			
					antigovalor=filho1[index]
			
					prob = random.random()					

	
					if prob <= 0.6: 

						valor = 1

						if random.random() <= 0.5: #adiciona valor
							novovalor = antigovalor + valor
						else:
							novovalor = antigovalor - valor

					elif prob > 0.6 and prob <= 0.9:

						valor = 2

						if random.random() <= 0.5: 
							novovalor = antigovalor + valor
						else:
							novovalor = antigovalor - valor

					else:
						valor = 3

						if random.random() <= 0.5: 
							novovalor = antigovalor + valor
						else:
							novovalor = antigovalor - valor
				

            				if novovalor > 9: #trunca
						novovalor=9

					if novovalor < 0: 
						novovalor=0

					f1[index]=copy.deepcopy(novovalor) #atribui novo valor ao gene
									

		filhos[j]=copy.deepcopy(f1) 
					
		j=j+1
				
		
	return filhos


def selecionapopulacao(novapopulacao):


	index = [i for i in range(len(novapopulacao))]


	indexgene = random.sample(index,len(populacao)) #seleciona aleatoriamente a prox populacao


	j=0
	while j < len(populacao):

		k=0
		while k < len(populacao):
			populacao[k]=novapopulacao[indexgene[j]]

			k=k+1
			j=j+1

	
	return populacao
	

#------------- main --------------

populacao = Populacao() # Inicializa uma população

#print("População Inicial:\n%s"%(populacao)) 


best = 0
	
valor = [0 for i in range(Niter)]

#print "vetor valor ", valor

contador=0

# Evolui a populacao

#f = open('file.txt', 'wb')

totalgeracao = []

for i in range(Niter):

		
	bonus = calculaBonus(populacao)	
	grupo = calculaFitnessGrupo(populacao)	
	#egoista = calculaFitnessEgo(populacao)
	Totalfitness = fitnessTotal(populacao)

	melhor = melhorIndividuo(populacao)

	melhorfitn = melhorFit(populacao)

	#print  i+1,melhorfitn
	
	#f.write("%i %5.2f\n" % (i+1, melhorfitn))

	
	valor[i]=melhorfitn

	#guarda o melhor individuo entre todas as geracoes

	if melhorfitn > best:
		best = melhorfitn
		bestindiv = melhor
		it = i

	

	selecao_pais = seleciona(populacao)

	#print "pais selecionados : ", selecao_pais

	novosfilhos = cruzamento(selecao_pais)

	#print "filhos cruzamento : ", novosfilhos

	filhosmutacao = mutacao(novosfilhos)

	#print "filhos mutacao : ", filhosmutacao

	novapopulacao = populacao + filhosmutacao

	#print "nova populacao : \n", novapopulacao

	populacao = selecionapopulacao(novapopulacao)

	#print "proxima populacao : \n",populacao


	#verifica criterio de parada
	
	if i > 2:

		if valor[i] == valor[i-1]:
	
			contador += 1
			

			if contador == kgeracoes:

				totalgeracao = i			
			
				break
						
 
		else:
			contador = 0
			totalgeracao = i

#print("\nPopulação Final:\n%s"%(populacao)) 

print bestindiv, it
#print totalgeracao

#f.close()





