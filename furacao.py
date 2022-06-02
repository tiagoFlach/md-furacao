# import pandas as pd
import os

from prettytable import PrettyTable

from furadeiras import furadeiras				# lista de furadeiras
from setups import setups, pecas_verificadas	# dicionario para teste de validação		
from Furadeira import Furadeira					# classe Furadeira
from Furo import Furo							# classe Furo
from Peca import Peca							# classe Peca		


# Arquivo
# --------------------
# filename = 'DIVISÓRIA 12X387X1652.bpp'
# filename = 'TAMPO MAL 15X440X2280.bpp'
# --------------------
# filename = 'BASE 12X489X1772/BASE 12X489X1772.bpp'
filename = 'BASE 15X400X1046/BASE 15X400X1046.bpp'							# OK
# filename = 'BASE AÉREO 12X266X1174/BASE AÉREO 12X266X1174.bpp'				# OK
# filename = 'BASE BALCÃO 15X450X1198/BASE BALCÃO 15X450X1198.bpp'
# filename = 'DIVISÓRIA BALCÃO 12X400X645/DIVISÓRIA BALCÃO 12X400X645.bpp'		# Revisar - Furo superior
# filename = 'DIVISÓRIA BALCÃO 12X450X645/DIVISÓRIA BALCÃO 12X450X645.bpp'
# filename = 'DIVISÓRIA DIR 15X440X1685/DIVISÓRIA DIR 15X440X1685.bpp'
# filename = 'LATERAL DIR 15X544X2175/LATERAL DIR 15X544X2175.bpp'				# Complexo
# filename = 'LATERAL ESQ GAVETEIRO 15X436X724/LATERAL ESQ GAVETEIRO 15X436X724.bpp'
# filename = 'TAMPO SUPERIOR 12X489X574/TAMPO SUPERIOR 12X489X574.bpp'
dir = os.path.dirname(__file__) + '/Peças/'
file = open(dir + filename, 'r', encoding='latin1')
# --------------------


# Variáveis de configuração
# --------------------
furadeira = 'F500-B'
# --------------------


# Cria furadeira
# --------------------
furadeira = Furadeira(furadeiras[furadeira])
# furadeira.imprimir_cabecotes()
# --------------------


# Varrer arquivo e encontrar furos
# --------------------
furos = []
array_furos = []
count = 0

# Varredura do arquivo
for line in file:
	if line.find("PAN=LPX") == 0:
		lpx = float(line.split('|')[1])
		lpx = round(lpx, 1)
	if line.find("PAN=LPY") == 0:
		lpy = float(line.split('|')[1])
		lpy = round(lpy, 1)
	if line.find("PAN=LPZ") == 0:
		lpz = float(line.split('|')[1])
		lpz = round(lpz, 1)

	if line.find("[PROGRAM]") == 0:
		flag_program = True
	elif 'flag_program' in locals() and flag_program:
		if line != '\n':
			nome = line.rstrip('\n').replace("'", "")
			flag_program = False

	if 'nome' in locals():
		if line.find("@ BG") == 0:
			# line[ 0]: '@ BG'
			# line[ 1]: '""'
			# line[ 2]: '""'
			# line[ 3]: '37127068'
			# line[ 4]: '""'
			# line[ 5]: side
			# line[ 6]: crn
			# line[ 7]: x
			# line[ 8]: y
			# line[ 9]: z
			# line[10]: dp
			# line[11]: diametro
			# line[12]: p
			# line[13]: cabeçote
			# line[37]: "id"

			line = line.split(',')

			# Dados
			id = line[37].strip().replace('"', '')
			side = line[5].strip()
			crn = int(line[6].strip().replace('"', ''))
			x = float(line[7].strip())
			y = float(line[8].strip())
			z = float(line[9].strip())
			dp = float(line[10].strip())
			diametro = float(line[11].strip())
			p = int(line[12].strip())

			broca = str(diametro)
			if (p == 1):
				broca += 'T'

			# Cria o Furo
			furo = Furo(
				id,
				side,
				crn,
				x,
				y,
				z,
				dp,
				diametro,
				p,
				broca
			)

			array_furos.append(furo)
		elif line == '\n' and len(array_furos) > 0:
			furos.append(array_furos)
			array_furos = []
# --------------------


# Imprimir tabela de dados da peça
# --------------------
peca = Peca(nome, lpx, lpy, lpz)
peca.imprimir_peca()


# Imprimir tabela de dados de furos
# --------------------
data = PrettyTable()
data.title = nome
data.field_names = ["Id", "Side", "CRN", "X", "Y", "Z", "DP", "Diametro", "P", "Broca"]
for array in furos:
	for i in array:
		data.add_row(list(i.__dict__.values()))
indice = ''
data._field_names.insert(0, indice)
data._align[indice] = 'c'
data._valign[indice] = 't'
for i, _ in enumerate(data._rows):
	data._rows[i].insert(0, i+1)
print(data)
# --------------------


# Obtém o dicionário para realização de testes
# --------------------
def getTestDict():
	with open("TestDict.txt", 'w', encoding = 'utf-8') as file:
		file.write(furadeira.toDict())
# --------------------


# Realiza testes em peças já aprovadas
# --------------------
def tests():

	data = PrettyTable()
	data.title = 'Testes'
	data.field_names = ["Peca", "Furadeira", "Resultado"]

	for peca in pecas_verificadas:
		for furadeira_nome in furadeiras:
			if furadeira_nome in list(setups[peca]) and setups[peca][furadeira_nome] == furadeira.toDict():
				resultado = 'Aprovado'
			else:
				resultado = 'Erro'

			data.add_row([peca, furadeira_nome, resultado])

	print(data)
# --------------------









# furadeira.imprimir_furadeira()
furadeira.distribuir_furos(furos, peca)
# furadeira.imprimir_setup()
furadeira.imprimir_cabecotes()
# furadeira.imprimir_cabecote(5)
# print(furos)

# getTestDict()
tests()




exit()