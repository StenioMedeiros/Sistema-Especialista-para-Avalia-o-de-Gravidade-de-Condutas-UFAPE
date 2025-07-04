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
        applied_rules = set() # Para armazenar nomes de regras aplicadas únicas

        for fact in self.engine.facts.values():
            if isinstance(fact, AvaliacaoFinal):
                final_evaluation = fact
            elif isinstance(fact, Recomendacao):
                recomendacoes_finais = fact
            elif isinstance(fact, Gravidade):
                explanations.append(f"Gravidade Base: Nível {fact['nivel']} - {fact['explicacao']}")
            elif isinstance(fact, Agravante):
                explanations.append(f"Agravante: {fact['explicacao']}")

        # Coleta os nomes das regras que foram disparadas
        # Isso exige modificar as regras ligeiramente para registrar seus nomes
        # Para simplicidade aqui, vamos apenas rastrear os tipos de fatos declarados,
        # mas uma solução mais robusta envolveria modificar as regras em rules.py
        # para adicionar explicitamente seus nomes a uma lista durante a execução.

        # Por enquanto, podemos inferir regras aplicadas com base nas explicações.
        # Isso é uma simplificação; uma lista verdadeiramente precisa exigiria integração direta com o Experta
        # ou registro explícito dentro do corpo de cada regra.

        # Exemplo de como você *poderia* rastrear regras se modificasse rules.py:
        # Em cada regra: self.engine.applied_rules.add("nome_da_regra")
        # Então, inicialize self.applied_rules = set() em __init__ de SistemaAvaliacaoConduta

        # Para esta configuração, tentaremos inferir a partir das explicações.
        for exp in explanations:
            if "Nível 6" in exp and "Agressivo e Fisicamente Violento" in exp:
                applied_rules.add("nivel_6")
            elif "Nível 5" in exp and "Agressivo e Não Fisicamente Violento" in exp:
                applied_rules.add("nivel_5")
            elif "Nível 4" in exp and "Bastante Ofensivo" in exp:
                applied_rules.add("nivel_4")
            elif "Nível 3" in exp and "Ofensivo" in exp:
                applied_rules.add("nivel_3")
            elif "Nível 2" in exp and "Constrangedor e Levemente Ofensivo" in exp:
                applied_rules.add("nivel_2")
            elif "Nível 1" in exp and "Não Ofensivo" in exp:
                applied_rules.add("nivel_1")
            elif "múltiplos fatores agravantes" in exp or "quatro ou mais fatores agravantes" in exp:
                applied_rules.add("elevar_nivel_por_multiplos_agravantes")
            elif "contexto da conduta (Formal/Público)" in exp:
                applied_rules.add("fator_contexto_formal_publico")
            elif "contexto da conduta (conotação sexual/Privado)" in exp:
                applied_rules.add("fator_contexto_conotacao_sexual_privado")
            elif "histórico do envolvido é um agravante porque há histórico de condutas similares" in exp:
                applied_rules.add("fator_historico_reincidente")
            elif "histórico do envolvido é um agravante porque há múltiplas reincidências" in exp:
                applied_rules.add("fator_historico_frequente")
            elif "frequência da conduta é um agravante, pois ocorre esporadicamente" in exp:
                applied_rules.add("fator_frequencia_ocasional")
            elif "frequência da conduta é um agravante, pois acontece frequentemente" in exp:
                applied_rules.add("fator_frequencia_repetitivo_insistente")
            elif "impacto na vítima é um agravante, pois gerou consequências de curto prazo" in exp:
                applied_rules.add("fator_impacto_negativo_consideravel")
            elif "impacto na vítima é um agravante, pois gerou consequências de médio e longo prazo" in exp:
                applied_rules.add("fator_impacto_negativo_intenso")
            elif "sinais não-verbais são um agravante, pois intensificam a negatividade da conduta" in exp:
                applied_rules.add("fator_sinais_agravado")
            elif "intenção percebida é um agravante, pois demonstra falta de consideração" in exp:
                applied_rules.add("fator_intencao_negligente")
            elif "intenção percebida é um agravante, pois houve objetivo claro de causar dano" in exp:
                applied_rules.add("fator_intencao_intencional")
            elif "relação hierárquica é um agravante, pois o agressor é superior direto da vítima" in exp:
                applied_rules.add("fator_hierarquia_superior_subordinado_direto")
            elif "relação hierárquica é um agravante, pois o agressor tem posição superior mesmo sem relação direta" in exp:
                applied_rules.add("fator_hierarquia_superior_subordinado_indireto")


        result = {
            'nivel_gravidade': None,
            'recomendacoes': [],
            'explicacoes': explanations,
            'applied_rules': list(applied_rules)
        }

        if final_evaluation:
            result['nivel_gravidade'] = final_evaluation['nivel_final_gravidade']
            result['explicacoes'] = final_evaluation['explicacoes_finais']

        if recomendacoes_finais:
            result['recomendacoes'] = recomendacoes_finais['recomendacoes_texto']

        return result['nivel_gravidade'], result['explicacoes'], result['recomendacoes'], result['applied_rules']