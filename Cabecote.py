class Cabecote:
	def __init__(self, nro, nro_brocas, distancia_pinos, posicao):
		self.nro = nro
		self.distancia_pinos = distancia_pinos
		self.posicao = posicao
		self.x = 0
		self.deslocamento_x = 0
		self.used = False

		self.brocas = {}
		for i in range(1, nro_brocas + 1):
			self.brocas[i] = 'x'

	def setBroca(self, furo, eixo_y = 'normal', var = 'y'):
		if eixo_y == 'invertido':
			nro_broca = len(self.brocas) + 1 - (getattr(furo, var) // self.distancia_pinos)
			deslocamento = getattr(furo, var) % self.distancia_pinos
		elif eixo_y == 'normal':
			nro_broca = getattr(furo, var) // self.distancia_pinos
			deslocamento = getattr(furo, var) % self.distancia_pinos

		self.brocas[nro_broca] = furo.broca

		if deslocamento != 0:
			self.deslocamento_x = deslocamento

	def setX(self, x):
		self.x = x

	def use(self):
		self.used = True