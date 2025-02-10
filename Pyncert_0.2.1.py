# Código para hallar las incertidumbres en una medida por el método
# de las Derivadas Parciales desarrollado por Martín Lozano Rivas y
# Nilo Muñiz Martínez. UniOvi 2025.

# Versión Beta 0.2.1

# Módulos
from sympy import symbols, diff, sin, cos, pi, exp, tan, log, sqrt, sympify
import os 
import platform as pf

# Funciones
def valores_incertidumbres(num, es_incertidumbre = False):
	comprobador = True
	while comprobador:
		try:
			if es_incertidumbre == False:
				n = input('Valor del elemento %d: ' % num)
			else:
				n = input('Incertidumbre del elemento %d: ' % num)
			n = float(n)
		except:
			n = sympify(n, locals={'pi': pi, 'sen': sin, 'sin': sin, 'cos': cos, 'tg': tan, 'tan': tan, 'exp': exp, 'sqrt': sqrt, 'raiz': sqrt, 'raíz': sqrt, 'log': log})
			if n.is_number == False:
				if es_incertidumbre == False:
					print('Introduce un valor válido (número decimal o expresión matemática).')
				else:
					print('Introduce un valor válido (número decimal o expresión matemática mayor o igual a 0).')
			else:
				comprobador = False
		else:
			if es_incertidumbre == True:
				if n < 0:
					print('El valor de la incertidumbre debe ser mayor o igual a 0.')
				else:
					comprobador = False
			else:
				comprobador = False
	return n		

def nombrar_variables(num, exist):
	reservado = ['pi','oo','sqrt','nan','zeta','gamma']
	while True:
		var = input('Nombre de la variable %d: ' % num)
		while var in reservado:
			print('El nombre establecido para la variable está reservado para otra función. Elige otro nombre.')
			var = input('Nombre de la variable %d: ' % num)
		if var.lower() == 'i':
			var = 'Ibueno'
			nombre_visual = 'I'
		else:
			nombre_visual = var
		varaux = symbols(var)
		if varaux in exist:
			print('Ese nombre ya está escogido para otra variable. Elige otro.')
			continue
		try:
			var = float(var)
		except:
			var = str(var)
			return var, nombre_visual
		else:
			print('El nombre de la variable no puede ser un número.')

# Número de Variables
comprobador = True
while comprobador:
	try:
		nvar = int(input('Número de variables: '))
	except:
		print('Introduce un valor válido (número entero mayor a 0).')
	else:
		if nvar <= 0:
			print('Introduce un valor válido (número entero mayor a 0).')
		else:
			comprobador = False
print('')

# Declaración de variables:
variables = [0 for _ in range(0,nvar)]
variables_visuales = []
for i in range(0,nvar):
	tupla_variables = nombrar_variables(i+1, variables)  
	variables[i] = symbols(tupla_variables[0])
	variables_visuales.append(tupla_variables[1])
print('')

# Posibilidad de calcular el valor de la incertidumbre
comprobador = True
while comprobador:
    calcular = str(input('Además de las derivadas, ¿quieres calcular el valor de la incertidumbre? (Sí/No) '))
    calcular = calcular.lower()
    calcular = calcular.replace('í', 'i')
    if calcular not in ['si','no']:
        print('Introduce únicamente Sí o No (no importan mayúsculas ni acentos).')
    else:
        comprobador = False
		
# Valores:
if calcular == 'si':
    valores = []
    for i in range(0,nvar):
        valor = valores_incertidumbres(i+1)
        valores.append(valor)
	
# Incertidumbres:
if calcular == 'si':
    incertidumbres = []
    for i in range(0,nvar):
        incertidumbre = valores_incertidumbres(i+1, es_incertidumbre = True)
        incertidumbres.append(incertidumbre)	
print('')

# Función cuya incertidumbre se quiere conocer:
funcion = input('Función cuya incertidumbre se quiere conocer: ')
funcion = funcion.replace('I', 'Ibueno')
funcion = sympify(funcion)

# Derivadas parciales simbólicas:
DPS = []
DPSprint = []
for i in variables:
	D = diff(funcion, i)
	DPS.append(D)
	D = str(D)
	D = D.replace('Ibueno', 'I')
	DPSprint.append(D)
print('')
print('Las derivadas parciales de la función son:')
for i in range(0,nvar):
	print('- Respecto a %s:' % variables_visuales[i],DPSprint[i])	

# Fórmula de la incertidumbre:
variablesauxiliar = [str(i) for i in variables_visuales]
FORMULA = ['(%s)*Δ%s' % (DPSprint[i],variablesauxiliar[j]) for i in range(0,nvar) for j in range(0,nvar) if i == j]
print('La fórmula de la incertidumbre final es:',' + '.join(FORMULA))

# Derivadas parciales definidas:
if calcular == 'si':
    DPD = []
    for i in range(0,nvar):
        Dd = DPS[i].subs({a:valores[i] for a in variables})
        DPD.append(Dd)

# Cálculo de la incertidumbre:
if calcular == 'si':
    I = 0
    for i in range(0,nvar):
        Inc = abs(DPD[i])*incertidumbres[i]	
        I += Inc
    print('')
    print('La incertidumbre total es: ',I)

#Impresión del resultado en el portapapeles
sistema = pf.system()
try:
    if sistema == "Windows":
        os.system(f'echo {str(I)} | clip')
    elif sistema == "Darwin":  # macintosh
        os.system(f'echo {str(I)} | pbcopy')
    elif sistema == "Linux":
        os.system(f'echo {str(I)} | xclip -selection clipboard')
except:
	if sistema == "Windows":
		print('Tu sistema no es compatible con la copia al portapapeles.')
	elif sistema == "Darwin":  # macintosh
		print('Tu sistema no es compatible con la copia al portapapeles.')
	elif sistema == "Linux":
		print('El sistema no ha podido acceder al portapapeles.', '\n', 'Asegúrese de tener el módulo "xclip" instalado en el dispositivo')
else:
	print('El resultado ha sido copiado al portapapeles.')

# Finalización del programa en CMD
print('')
input('Presiona la tecla Enter para salir del programa.')