from pyknow import *

distancia = None;   dinheiro = None;    prazo = None;
disposicao = None;  obstaculo = None;   pico = None;

print("Bem vindo ao Sistema Especialista pra você saber se deve pegar um ônibus.\n")

while (distancia not in ['s', 'n']):
    distancia = input("A distância até o destino é longa demais pra se caminhar? (S/N) ").lower()

while (dinheiro not in [0, 1, 2]):
    dinheiro = int(input("De 0 a 2, o quanto você tem dinheiro? "))

while (prazo not in ['s', 'n']):
    prazo = input("Você tem um prazo pra chegar até seu destino? (S/N) ").lower()

while (disposicao not in ['s', 'n']):
    disposicao = input("Você está com motivação suficiente pra caminhar até lá? (S/N) ").lower()

while (pico not in ['s', 'n']):
    pico = input("É horário de pico? (S/N) ").lower()

while (obstaculo not in ['s', 'n']):
    obstaculo = input("Há obstáculos que influenciam as rotas dos ônibus? (S/N) ").lower()

print("\n")

onibus = 0
uber = 0
caminhar = 0

# Declaração da classe Ônibus:
class Bus(Fact):
    pass


# Definição das regras:
class PegoOnibus(KnowledgeEngine):

    # Regra referente às condições de escolha do método de locomoção:
    @Rule(
        AND(
            Bus(Distancia='s'),
            OR(
                AND(
                    Bus(Prazo='s'),
                    Bus(Tempo=True)
                ),
                Bus(Disposicao='n')
            ),
            Bus(Dinheiro=1)
        )
    )
    def pega_onibus(self):
        global onibus
        onibus += 1

    @Rule(
        AND(
            Bus(Distancia='s'),
            Bus(Disposicao='n'),
            Bus(Tempo=False),
            Bus(Prazo='s'),
            Bus(Dinheiro=2)
        )
    )
    def pega_uber(self):
        global uber
        uber += 1

    @Rule(
        OR(
            AND(
                Bus(Disposicao='s'),
                Bus(Distancia='n'),
                Bus(Prazo='s'),
                Bus(Tempo=False)
            ),
            OR(
                Bus(Disposicao='s'),
                Bus(Prazo='n')
            ),
            Bus(Dinheiro=0)
        )
    )
    def vai_andando(self):
        global caminhar
        caminhar += 1

    # Regra referente às condições favoráveis de viagem:
    @Rule(
        AND(
            Bus(Obstaculo='n'),
            Bus(Pico='n')
        )
    )
    def tempo_de_viagem(self):
        engine.declare(Bus(Tempo=True))

    @Rule(
        OR(
            Bus(Obstaculo='s'),
            Bus(Pico='s')
        )
    )
    def tempo_de_viagem(self):
        engine.declare(Bus(Tempo=False))


def resultado(onibus, uber, caminhar):
    if ((onibus > uber) and (onibus > caminhar)):
        return ("Vá de ônibus.")
    elif ((uber > onibus) and (uber > caminhar)):
        return ("Vá de Uber.")
    elif ((caminhar > onibus) and (caminhar > uber)):
        return ("Vá andando.")
    elif ((onibus > uber) and (onibus == caminhar)):
        return ("Vá de ônibus ou andando.")
    elif ((onibus > caminhar) and (onibus == uber)):
        return ("Vá de ônibus ou Uber.")
    elif ((uber > onibus) and (uber == caminhar)):
        return ("Vá de Uber ou andando.")
    else:
        return ("Tanto faz.")

# Define o motor de inferência com a classe PegoOnibus:
engine = PegoOnibus()

# Anula as variáveis do motor, caso já iniciado:
engine.reset()

# Declara as condições das variáveis-base:
engine.declare(Bus(Distancia=distancia))
engine.declare(Bus(Prazo=prazo))
engine.declare(Bus(Disposicao=disposicao))
engine.declare(Bus(Obstaculo=obstaculo))
engine.declare(Bus(Pico=pico))
engine.declare(Bus(Dinheiro=dinheiro))

# Inicia o motor de inferência:
engine.run()

print (resultado(onibus, uber, caminhar))
