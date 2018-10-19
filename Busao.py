from pyknow import *

print("Bem vindo ao programa. (use: 's' ou 'n' para responder as perguntas.)\n")
distancia = input("A distância é grande demais?")
dinheiro = input("Você tem uma quantia boa de dinheiro contigo?")
prazo = input("Você tem prazo pra chegar lá?")
disposicao = input("Você está bem dispostx a andar?")
pico = input("É horário de pico?")
obstaculo = input("Há obstáculos que influenciam as rotas dos ônibus?")
print("\n")


# Declaração da classe Ônibus:
class Bus(Fact):
    pass


# Definição das regras:
class PegoOnibus(KnowledgeEngine):

    # Regra referente às condições de escolha do método de locomoção:
    @Rule(AND(Bus(Distancia='s'), OR(Bus(Prazo='s'), Bus(Tempo=True), Bus(Disposicao='n')), Bus(Dinheiro='n')))
    def pega_onibus(self):
        print("Pega um ônibus.")

    @Rule(AND(Bus(Distancia='s'), Bus(Disposicao='n'),  Bus(Tempo=False), Bus(Prazo='s'), Bus(Dinheiro='s')))
    def pega_uber(self):
        print("Pega um uber.")

    @Rule(OR(AND(Bus(Disposicao='s'), Bus(Distancia='n'), Bus(Prazo='s'), Bus(Tempo=False)),
             OR(Bus(Disposicao='s'), Bus(Prazo='n')), OR(Bus(Dinheiro='n'))))
    def vai_andando(self):
        print("Vai andando mesmo.")

    # Regra referente às condições favoráveis de viagem:
    @Rule(AND(Bus(Obstaculo='n'), Bus(Pico='n')))
    def tempo_de_viagem(self):
        # print("O ônibus não deve demorar.")
        engine.declare(Bus(Tempo=True))

    @Rule(OR(Bus(Obstaculo='s'), Bus(Pico='s')))
    def tempo_de_viagem(self):
        # print("O ônibus deve demorar.")
        engine.declare(Bus(Tempo=False))


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
