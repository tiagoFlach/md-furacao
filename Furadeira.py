from prettytable import PrettyTable
from collections import defaultdict
from typing import OrderedDict

from Cabecote import Cabecote

class Furadeira:
	def __init__(self, array):
		self.marca = array['marca']
		self.nome = array['nome']
		self.nro_cabecotes = array['nro_cabecotes']
		self.nro_mandris = array['nro_mandris']
		self.distancia_mandris = array['distancia_mandris']
		self.distancia_min_cabecotes = array['distancia_min_cabecotes']
		self.posicao_cabecotes = array['posicao_cabecotes']
		# self.batente_fundo = array['batente_fundo']
		self.batente_fundo = 0
		self.eixo_y = array['eixo_y']
		self.bipartido = array['bipartido']

		# ----------
		self.posicoes = list(self.posicao_cabecotes.keys())
		self.deslocamento_y = 0

		self.criar_cabecotes()
		# self.__calcular_posicao_cabecotes()
		# self.__calcular_posicao_brocas()

	# Define o batente de fundo com base nas peças laterais
	def defineBatenteFundo(self, furos):
		side = '0 : 1'

		furos = [item for sublist in furos for item in sublist]
		furos = list(
				furo for furo in furos
				if furo.side == side)

		if len(furos) > 0:
			furo = min(furos)
			diferenca = furo % self.distancia_mandris

			if diferenca != 0:
				self.batente_fundo = diferenca



	# Cria os cabeçotes com base nas definições da furadeira
	def criar_cabecotes(self):
		cabecotes = []

		for nro in range(1, self.nro_cabecotes + 1):
			for posicao in self.posicao_cabecotes:
				if nro in self.posicao_cabecotes[posicao]:
					cabecote = Cabecote(nro,
						self.nro_mandris,
						self.distancia_mandris,
						self.distancia_min_cabecotes,
						posicao,
						self.bipartido)
					cabecotes.append(cabecote)
					break

		self.cabecotes = cabecotes

	# Distribuir furos para os cabeçotes
	def distribuir_furos(self, furos):
		
		self.defineBatenteFundo(furos)

		# Agrupar por side
		groups = defaultdict(list)
		for array in furos:
			for furo in array:
				groups[furo.side].append(array)
				break
		furos = dict(groups.items())

		# Agrupa furos por alinhamento
		# for side in furos:
		# 	if side in ['0 : 0', '0 : 5']:
		# 		groups = defaultdict(list)
		# 		for array in furos[side]:
		# 			x_array = list(set(list(furo.x for furo in array)))
		# 			y_array = list(set(list(furo.y for furo in array)))

		# 			if len(x_array) == 1:
		# 				# Alinhado no eixo X
		# 				groups['alinhado_x'].append(array)
		# 				# groups[side].append(array)
		# 			elif len(y_array) == 1:
		# 				# Alinhado no eixo Y
		# 				groups['alinhado_y'].append(array)
		# 			else:
		# 				# Não alinhado
		# 				groups['nao_alinhado'].append(array)
		# 		furos[side] = dict(groups.items())

		# Distribuir furos
		for side in furos:

			# Define a posição
			if side == '0 : 0':
				posicao = 'inferior'
				atributo = 'x'
			elif side == '0 : 1':
				posicao = 'esquerda'
				atributo = 'y'
			elif side == '0 : 2':
				posicao = ''
				atributo = ''
			elif side == '0 : 3':
				posicao = 'direita'
				atributo = 'y'
			elif side == '0 : 4':
				posicao = ''
				atributo = ''
			elif side == '0 : 5':
				posicao = 'superior'
				atributo = 'x'


			# Inferior
			# Superior
			# --------------------
			if side in ['0 : 0', '0 : 5']:

				# Agrupar furos por alinhamento
				groups = defaultdict(list)
				for array in furos[side]:
					x_array = list(set(list(furo.x for furo in array)))
					y_array = list(set(list(furo.y for furo in array)))

					if len(x_array) == 1:
						# Alinhado no eixo X
						groups['alinhado_x'].append(array)

					elif len(y_array) == 1:
						# Alinhado no eixo Y
						groups['alinhado_y'].append(array)

					else:
						# Não alinhado
						groups['nao_alinhado'].append(array)

				furos[side] = dict(groups.items())
				
				# Furos alinhados nos eixos X e Y
				# -------------------------------------------------
				for alinhamento in ['alinhado_x', 'alinhado_y']:
					if alinhamento in furos[side]:
						# Agrupar por x
						groups = defaultdict(list)
						for array in furos[side][alinhamento]:
							for furo in array:
								middle = self.defineMiddleX(array)
								groups[middle].append(furo)

						groups = dict(groups.items())

						# Ordenar
						groups = dict(OrderedDict(sorted(groups.items())))
						furos[side][alinhamento] = groups

				# print(furos)
				# exit()


				# Selecionar o cabeçotes
				# -------------------------------------------------
				for alinhamento in furos[side]:
					for x in furos[side][alinhamento]:
						for cabecote in self.cabecotes:
							if cabecote.posicao == posicao and cabecote.used == False:
								break

						cabecote.use()
						cabecote.setX(x)

						if alinhamento == 'alinhado_y':
							cabecote.setUsedBipartido()

						# Aplica os furos
						for furo in furos[side][alinhamento][x]:
							cabecote.setMandril(furo, self.eixo_y)

		self.ordenar_cabecotes()


	# Ordena os cabeçotes que serão utilizados conforme a posição no eixo x
	def ordenar_cabecotes(self):
		for posicao in self.posicoes:
			cabecotes = list(
				cabecote for cabecote in self.cabecotes 
				if cabecote.posicao == posicao and cabecote.used)

			# Ordena os cabeçotes conforme X
			cabecotes.sort(key=lambda cabecote: cabecote.x)

			if (len(cabecotes) > 0):
				cabecotes_nro = list(cabecote.nro for cabecote in cabecotes)
				cabecotes_nro.sort()

				for i, cabecote in enumerate(cabecotes):
					if cabecote.nro != cabecotes_nro[i]:
						cabecote.setNro(cabecotes_nro[i])

		self.cabecotes.sort(key=lambda cabecote: cabecote.nro)


	# Define o ponto X que os furos deverão ser aplicados
	def defineMiddleX(self, furos):
		ponto_x = []
		for furo in furos:
			ponto_x.append(furo.x)

		ponto_x = list(set(ponto_x))

		# Encontrar ponto médio em x para furação
		# if len(ponto_x) == 2:
			# Se a quantidade de furos na horizontal for 2 
			# (separados pela distancia de da broca), ao invés de girar o cabeçote
			# pode ser adicionado o agregado (ÚLTIMO RECURSO)

			# Adicionar agregado
			# middle = min(ponto_x)
		# 	continue
		# else:
		middle = min(ponto_x) + (len(ponto_x) // 2) * self.distancia_mandris

		return middle


	# Imprimir tabela de cabeçotes
	def imprimir_cabecotes(self):

		table = PrettyTable()
		table.title = 'Cabeçotes'
		table.field_names = list(cabecote.nro for cabecote in self.cabecotes)

		# Brocas
		for mandril in range(1, self.nro_mandris + 1):
			
			row = list()
			for cabecote in self.cabecotes:
				if cabecote.used_bipartido:
					if mandril in cabecote.mandris_rotacao:

						array = []
						for rotacionado in list(cabecote.mandris)[
								int(((mandril // (self.nro_mandris / 2)) * (self.nro_mandris / 2))) 
								: 
								int((mandril // (self.nro_mandris / 2)) * (self.nro_mandris / 2) + (self.nro_mandris / 2))
							]:
							
							array.append(cabecote.mandris[rotacionado])

						line = ' '.join(array)
						row.append(line)

						# row.append(fila_dividida)
					else:
						row.append(' ')
				else:
					row.append(cabecote.mandris[mandril])


			# table.add_row(list(cabecote.mandris[mandril] for cabecote in self.cabecotes))
			table.add_row(row)

		# Distancia x
		line = '-----'
		table.add_row(list(line for cabecote in self.cabecotes))
		# Limites
		row = []
		for cabecote in self.cabecotes:
			if cabecote.used_bipartido:
				string = str(cabecote.limite['start']) + ' ← ' + str(cabecote.x) + ' → ' + str(cabecote.limite['end'])
				row.append(string)
			else:
				row.append(cabecote.x)
		table.add_row(row)
		# Deslocamento Y
		table.add_row(list(cabecote.deslocamento_y for cabecote in self.cabecotes))
		# Limites totais
		row = []
		for cabecote in self.cabecotes:
			if cabecote.used:
				string = str(cabecote.limite['start']) + ' ↔ ' + str(cabecote.limite['end'])
			else:
				string = ' '
			row.append(string)
		# table.add_row(row)
		table.add_row(list(cabecote.posicao[0:3] for cabecote in self.cabecotes))

		# Índice 1
		indice = ''
		table._field_names.insert(0, indice)
		table._align[indice] = 'r'
		table._valign[indice] = 't'
		for i, _ in enumerate(table._rows):
			if i < self.nro_mandris:
				if self.eixo_y == 'invertido':
					table._rows[i].insert(0, (len(table._rows) - 3 - i) * self.distancia_mandris)
				else:
					table._rows[i].insert(0, (i+1) * self.distancia_mandris)
			elif i == self.nro_mandris:
				table._rows[i].insert(0, line)
			elif i == self.nro_mandris + 1:
				table._rows[i].insert(0, 'pos_x')
			elif i == self.nro_mandris + 2:
				table._rows[i].insert(0, 'des_y')
			else:
				table._rows[i].insert(0, '')

		# Índice 2
		table._field_names.insert(0, indice)
		for i, _ in enumerate(table._rows):
			if i < self.nro_mandris:
				table._rows[i].insert(0, (i+1))
			elif i == self.nro_mandris:
				table._rows[i].insert(0, line)
			else:
				table._rows[i].insert(0, '')

		print(table)

	# Imprimir tabela de cabeçote específico
	def imprimir_cabecote(self, nro):
		cabecote = self.cabecotes[nro - 1]
		cabecote.imprimir_cabecote()

	def imprimir_furadeira(self):
		table = PrettyTable()
		table.title = self.marca + ' ' + self.nome
		table.field_names = list(['Atributo', 'Valor'])
		for var in vars(self):
			if var != 'cabecotes':
				table.add_row([var, vars(self)[var]])
		print(table)