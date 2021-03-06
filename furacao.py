import os

from prettytable import PrettyTable

from furadeiras import furadeiras				# lista de furadeiras
from Furadeira import Furadeira					# classe Furadeira
from Furo import Furo							# classe Furo
from Peca import Peca							# classe Peca


# Arquivos de entrada
# Z:\FURACAO\0GLAMY\G20070\G20070 FURAÇÃO
# --------------------
filename = 'BASE COLUNA 15X250X640'
filename = 'TAMPO SUP COLUNA 12X248X616'
# filename = 'BASE 15X400X1046'
# filename = 'BASE COLUNA 15X250X640'
# filename = 'BASE MAIOR AÉREO 12X248X1026'
# filename = 'COSTA GAV  15X110X269'
# filename = 'DIVISÓRIA AÉREO 12X250X538'
# filename = 'DIVISÓRIA BALCÃO 12X400X645'
# filename = 'FRENTE GAV R 15mm 15X158X344'
# filename = 'LATERAL DIR AÉREO 12X250X220'
# filename = 'LATERAL DIR BALCÃO 12X400X645'
# filename = 'LATERAL DIR COLUNA 12X250X1640'
# filename = 'LATERAL ESQ AÉREO 12X250X550'
# filename = 'LATERAL ESQ BALCÃO 12X400X645'
# filename = 'LATERAL ESQ COLUNA 12X250X1640'
# filename = 'LATERAL GAV DIR R 10mm 15X110X350'
# filename = 'LATERAL GAV ESQ R 10mm 15X110X350'
# filename = 'MONTANTE BALCÃO 12X50X645'
# filename = 'PORTA  AÉREO 15X521X349'
# filename = 'PORTA COLUNA  15X315X822'
# filename = 'PORTA MAIOR BALCÃO 15X344X652'
# filename = 'PORTA MENOR BALCÃO 15X344X489'
# filename = 'TAMPO AÉREO 12X248X1626'
# filename = 'TAMPO BALCÃO 15X440X1048'
# filename = 'TAMPO INTERM ÁEREO 12X248X1026'
# filename = 'TAMPO INTERM COLUNA 12X248X616'


# Arquivo simples
# --------------------
# filename = 'TAMPO MAL 15X440X2280'											# OK - Verificada
# filename = 'BASE 15X400X1046'													# OK - Verificada
# filename = 'BASE AÉREO 12X266X1174'											# OK - Verificada
# filename = 'LATERAL DIR AÉREO 12X250X220'										# OK - Verificada

# Furo superior
# --------------------
# filename = 'BASE 12X489X1772'													# OK - Verificada
# filename = 'BASE BALCÃO 15X450X1198'											# Problema com nome de arquivo

# Furo superior e deslocamento de cabeçote
# --------------------
# filename = 'DIVISÓRIA BALCÃO 12X400X645'										# OK
# filename = 'LATERAL ESQ GAVETEIRO 15X436X724' 								# OK

# Batente de fundo
# --------------------
# filename = 'BASE 15X289X768'													# OK

# Agregado
# --------------------
# filename = 'DIVISÓRIA 12X387X1652'											# OK

# Bipartido
# --------------------
# filename = 'TAMPO SUPERIOR 12X489X574'										#

# Bipartido e furo superior
# --------------------
# filename = 'DIVISÓRIA DIR 15X440X1685'										#
# filename = 'DIVISÓRIA BALCÃO 12X450X645'										#
# filename = 'LATERAL DIR COLUNA 12X250X1640'									# Complexo
# filename = 'LATERAL DIR BALCÃO 12X400X645'

# Bipartido com menos mandris
# --------------------
# filename = 'LATERAL DIR 15X544X2175'											# Complexo

# --------------------


# Variáveis de configuração
# --------------------
modelo_furadeira = 'F500-B'
# modelo_furadeira = 'F400-T'
# --------------------


# Criar furadeira
# --------------------
def create_furadeira(modelo):
	furadeira = Furadeira(furadeiras[modelo])
	return furadeira
# --------------------

def get_path(peca_name):
	# dir = os.path.dirname(__file__) + '/Peças/' + peca_name + '/'
	dir = os.path.dirname(__file__) + '/Peças/G20070/' + peca_name + '/'
	filename = peca_name + '.bpp'
	path = dir + filename
	return path

# Criar peça
# --------------------
def create_peca(filename):
	file = open(get_path(filename), 'r', encoding='latin1')

	flag_program = False
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
		elif flag_program:
			if line != '\n':
				nome = line.rstrip('\n').replace("'", "")
				break

	peca = Peca(nome, lpx, lpy, lpz)
	file.close()
	return peca
# --------------------


# Varrer arquivo e encontrar furos
# --------------------
def find_furos(filename):
	file = open(get_path(filename), 'r', encoding='latin1')
	furos = []
	array_furos = []

	flag_program = False
	flag_nome = False

	# Varredura do arquivo
	for line in file:
		if line.find("[PROGRAM]") == 0:
			flag_program = True
		elif flag_program:
			if line != '\n':
				flag_nome = True

		if flag_nome:
			if line.find("@ BG") == 0 or line.find("@ BH") == 0:
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
				id = line[37].replace('"', '').strip()
				side = line[5].strip()
				crn = int(line[6].replace('"', '').strip())
				x = float(line[7].strip())
				y = float(line[8].strip())
				z = float(line[9].strip())
				dp = float(line[10].strip())
				diametro = float(line[11].strip())
				p = int(line[12].strip())

				broca = str(diametro)
				if (p == 1):
					broca += 'P'

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

	file.close()
	return furos
# --------------------


# Imprimir tabela de dados de furos
# --------------------
def imprimir_furos(title, furos):
	data = PrettyTable()
	data.title = title
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


# Abrir o  arquivo de furos
# --------------------
def show_pdf(filename):
	path = get_path(filename)

	if os.path.exists(path.replace('.bpp', '.pdf')):
		path = path.replace('.bpp', '.pdf')
	elif os.path.exists(path.replace('.bpp', '-IMG.pdf')):
		path = path.replace('.bpp', '-IMG.pdf')
	else:
		path = path.replace('.bpp', '-F.pdf')

	try:
		# Windows
		os.startfile(path)
	except:
		# Linux
		path = path.replace(' ', '\ ')
		os.system(f'evince {path} &')



# Testes
# --------------------
def adicionar_peca_verificada(filename, modelo_furadeira = None):
	peca = create_peca(filename)

	if modelo_furadeira == None:
		for furadeira_nome in furadeiras:
			furadeira = create_furadeira(furadeira_nome)
			furadeira.distribuir_furos(find_furos(filename), peca)

			peca.save_peca_verificada(furadeira)
	else:
		furadeira = create_furadeira(modelo_furadeira)
		furadeira.distribuir_furos(find_furos(filename), peca)

		peca.save_peca_verificada(furadeira)


# Sequencia principal do código
# --------------------
def main(filename, modelo_furadeira):
	# Peça
	peca = create_peca(filename)
	peca.imprimir_peca()

	# Furos
	furos = find_furos(filename)
	imprimir_furos(peca.nome, furos)

	# Furadeira
	furadeira = create_furadeira(modelo_furadeira)
	furadeira.distribuir_furos(furos, peca)

	furadeira.imprimir_furadeira()
	furadeira.imprimir_cabecotes()
	# furadeira.imprimir_setup()
	# furadeira.imprimir_cabecote(5)
	# print(furos)

	# show_pdf(filename)

	return furadeira


# Sequencia principal para testes
# --------------------
def main_test(filename, modelo_furadeira):
	# Peça
	peca = create_peca(filename)

	# Furos
	furos = find_furos(filename)

	# Furadeira
	furadeira = create_furadeira(modelo_furadeira)
	furadeira.distribuir_furos(furos, peca)

	return furadeira


main(filename, modelo_furadeira)
# adicionar_peca_verificada(filename)
# --------------------