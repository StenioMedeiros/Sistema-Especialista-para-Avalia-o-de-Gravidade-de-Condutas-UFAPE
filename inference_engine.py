from experta import Fact
from rules import SistemaAvaliacaoConduta
from facts import Conduta, Gravidade, Agravante, AvaliacaoFinal, Recomendacao

class InferenceEngine:
    def __init__(self):
        self.engine = SistemaAvaliacaoConduta()
        self.engine.reset()
        self.facts_to_declare = {}

    def add_fact(self, key, value):
        if value is not None:
            self.facts_to_declare[key] = value

    def run(self):
        self.engine.declare(Conduta(**self.facts_to_declare))
        self.engine.run()

        final_evaluation = None
        recomendacoes_finais = None
        explanations = []
        applied_rules = set() # Este conjunto será preenchido pelo motor

        for fact in self.engine.facts.values():
            if isinstance(fact, AvaliacaoFinal):
                final_evaluation = fact
            elif isinstance(fact, Recomendacao):
                recomendacoes_finais = fact
            elif isinstance(fact, Gravidade):
                explanations.append(f"Gravidade Base: Nível {fact['nivel']} - {fact['explicacao']}")
            elif isinstance(fact, Agravante):
                explanations.append(f"Agravante: {fact['explicacao']}")
        
        # Agora, simplesmente pegamos as regras aplicadas diretamente do motor
        applied_rules = self.engine._applied_rules

        result = {
            'nivel_gravidade': None,
            'recomendacoes': [],
            'explicacoes': explanations,
            'applied_rules': list(applied_rules) # Convertendo para lista para facilitar o uso no Streamlit
        }

        if final_evaluation:
            result['nivel_gravidade'] = final_evaluation['nivel_final_gravidade']
            result['explicacoes'] = final_evaluation['explicacoes_finais']

        if recomendacoes_finais:
            result['recomendacoes'] = recomendacoes_finais['recomendacoes_texto']

        return result['nivel_gravidade'], result['explicacoes'], result['recomendacoes'], result['applied_rules']