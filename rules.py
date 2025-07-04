from experta import KnowledgeEngine, Rule, AS, W, P, L, NOT, MATCH, TEST
from facts import Conduta, Gravidade, Agravante, AvaliacaoFinal, Recomendacao

class SistemaAvaliacaoConduta(KnowledgeEngine):
    def reset(self):
        super().reset()
        self._applied_rules = set()
        # Mapeamento de níveis para suas explicações padrão
        self._nivel_explanations = {
            1: "A conduta se enquadra no Nível 1 (Em Geral, Não Ofensivo)...",
            2: "A conduta se enquadra no Nível 2 (Constrangedor e Levemente Ofensivo)...",
            3: "A conduta se enquadra no Nível 3 (Ofensivo)...",
            4: "A conduta se enquadra no Nível 4 (Bastante Ofensivo)...",
            5: "A conduta se enquadra no Nível 5 (Agressivo e Não Fisicamente Violento)...",
            6: "A conduta se enquadra no Nível 6 (Agressivo e Fisicamente Violento), representando a forma mais extrema de conduta inapropriada...",
        }

    def _log_rule_applied(self, rule_name):
        self._applied_rules.add(rule_name)

    # --- Regras para os Níveis de Gravidade (Base) ---
    # (Mantenha estas regras como estão, elas vão declarar o nível BASE inicial)

    @Rule(AS.conduta_fact << Conduta(descricao=MATCH.descricao),
          TEST(lambda descricao: "agressão física" in descricao.lower() or
                                 "violência física" in descricao.lower() or
                                 "ameaça grave" in descricao.lower() or
                                 "coerção física" in descricao.lower()),
          NOT(Gravidade()), salience=600)
    def nivel_6(self, conduta_fact):
        print(f"DEBUG: Regra 'nivel_6' verificando: '{conduta_fact['descricao']}'")
        self.declare(Gravidade(
            nivel=6,
            explicacao=self._nivel_explanations[6], # Usa a explicação do dicionário
            tipo_avaliacao="base"
        ))
        self._log_rule_applied("nivel_6")
        print(f"DEBUG: Nivel 6 DISPARADO para: '{conduta_fact['descricao']}'")


    @Rule(AS.conduta_fact << Conduta(descricao=MATCH.descricao),
          TEST(lambda descricao: "agressivo não físico" in descricao.lower() or
                                 "ambiente hostil" in descricao.lower() or
                                 "avanços sexuais" in descricao.lower() or
                                 "comentários racistas" in descricao.lower() or
                                 "material pornográfico" in descricao.lower()),
          NOT(Gravidade()), salience=500)
    def nivel_5(self, conduta_fact):
        print(f"DEBUG: Regra 'nivel_5' verificando: '{conduta_fact['descricao']}'")
        self.declare(Gravidade(
            nivel=5,
            explicacao=self._nivel_explanations[5], # Usa a explicação do dicionário
            tipo_avaliacao="base"
        ))
        self._log_rule_applied("nivel_5")
        print(f"DEBUG: Nivel 5 DISPARADO para: '{conduta_fact['descricao']}'")

    @Rule(AS.conduta_fact << Conduta(descricao=MATCH.descricao),
          TEST(lambda descricao: "bastante ofensivo" in descricao.lower() or
                                 "explicitamente humilhante" in descricao.lower() or
                                 "toques não solicitados" in descricao.lower() or
                                 "danos emocionais" in descricao.lower() or
                                 "insultos diretos" in descricao.lower() or
                                 "humilhação maliciosa" in descricao.lower()),
          NOT(Gravidade()), salience=400)
    def nivel_4(self, conduta_fact):
        print(f"DEBUG: Regra 'nivel_4' verificando: '{conduta_fact['descricao']}'")
        self.declare(Gravidade(
            nivel=4,
            explicacao=self._nivel_explanations[4], # Usa a explicação do dicionário
            tipo_avaliacao="base"
        ))
        self._log_rule_applied("nivel_4")
        print(f"DEBUG: Nivel 4 DISPARADO para: '{conduta_fact['descricao']}'")

    @Rule(AS.conduta_fact << Conduta(descricao=MATCH.descricao),
          TEST(lambda descricao: "ofensivo" in descricao.lower() or
                                 "reforçam estereótipos" in descricao.lower() or
                                 "piadas sexuais" in descricao.lower() or
                                 "apelidos pejorativos" in descricao.lower() or
                                 "reproduz privilégio" in descricao.lower()),
          NOT(Gravidade()), salience=300)
    def nivel_3(self, conduta_fact):
        print(f"DEBUG: Regra 'nivel_3' verificando: '{conduta_fact['descricao']}'")
        self.declare(Gravidade(
            nivel=3,
            explicacao=self._nivel_explanations[3], # Usa a explicação do dicionário
            tipo_avaliacao="base"
        ))
        self._log_rule_applied("nivel_3")
        print(f"DEBUG: Nivel 3 DISPARADO para: '{conduta_fact['descricao']}'")


    @Rule(AS.conduta_fact << Conduta(descricao=MATCH.descricao),
          TEST(lambda descricao: "constrangedor" in descricao.lower() or
                                 "levemente ofensivo" in descricao.lower() or
                                 "causa desconforto" in descricao.lower() or
                                 "estereótipos sutis" in descricao.lower() or
                                 "comentários desrespeitosos" in descricao.lower() or
                                 "perguntas habilidades gênero" in descricao.lower() or
                                 "comentários aparência etnia" in descricao.lower()),
          NOT(Gravidade()), salience=200)
    def nivel_2(self, conduta_fact):
        print(f"DEBUG: Regra 'nivel_2' verificando: '{conduta_fact['descricao']}'")
        self.declare(Gravidade(
            nivel=2,
            explicacao=self._nivel_explanations[2], # Usa a explicação do dicionário
            tipo_avaliacao="base"
        ))
        self._log_rule_applied("nivel_2")
        print(f"DEBUG: Nivel 2 DISPARADO para: '{conduta_fact['descricao']}'")


    @Rule(AS.conduta_fact << Conduta(descricao=MATCH.descricao),
          TEST(lambda descricao: "não ofensivo" in descricao.lower() or
                                 "socialmente aceitável" in descricao.lower() or
                                 "comentários neutros" in descricao.lower() or
                                 "elogios simples" in descricao.lower() or
                                 "discussões neutras" in descricao.lower()),
          NOT(Gravidade()), salience=100)
    def nivel_1(self, conduta_fact):
        print(f"DEBUG: Regra 'nivel_1' verificando: '{conduta_fact['descricao']}'")
        self.declare(Gravidade(
            nivel=1,
            explicacao=self._nivel_explanations[1], # Usa a explicação do dicionário
            tipo_avaliacao="base"
        ))
        self._log_rule_applied("nivel_1")
        print(f"DEBUG: Nivel 1 DISPARADO para: '{conduta_fact['descricao']}'")

    # --- Regras para Fatores Adicionais (Agravantes) ---
    # (Mantenha estas regras como estão, elas declaram fatos Agravante)
    @Rule(AS.conduta_fact << Conduta(contexto_formal_informal='Formal', contexto_publico_privado='Público'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_contexto_formal_publico(self, conduta_fact):
        self.declare(Agravante(
            tipo='contexto_formal_publico',
            explicacao="O contexto da conduta (Formal/Público) é um agravante.", # Adicionei ponto final para consistência
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_contexto_formal_publico")

    @Rule(AS.conduta_fact << Conduta(descricao=MATCH.descricao, contexto_publico_privado='Privado'),
          TEST(lambda descricao: "conotação sexual" in descricao.lower()),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_contexto_conotacao_sexual_privado(self, conduta_fact):
        self.declare(Agravante(
            tipo='contexto_conotacao_sexual_privado',
            explicacao="O contexto da conduta (conotação sexual/Privado) é um agravante.",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_contexto_conotacao_sexual_privado")

    @Rule(AS.conduta_fact << Conduta(historico_envolvidos='Reincidente'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_historico_reincidente(self, conduta_fact):
        self.declare(Agravante(
            tipo='historico_reincidente',
            explicacao="O histórico do envolvido é um agravante porque há histórico de condutas similares.",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_historico_reincidente")

    @Rule(AS.conduta_fact << Conduta(historico_envolvidos='Frequente'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_historico_frequente(self, conduta_fact):
        self.declare(Agravante(
            tipo='historico_frequente',
            explicacao="O histórico do envolvido é um agravante porque há múltiplas reincidências.",
            incremento_nivel=2
        ))
        self._log_rule_applied("fator_historico_frequente")

    @Rule(AS.conduta_fact << Conduta(frequencia_conduta='Ocasional'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_frequencia_ocasional(self, conduta_fact):
        self.declare(Agravante(
            tipo='frequencia_ocasional',
            explicacao="A frequência da conduta é um agravante, pois ocorre esporadicamente.",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_frequencia_ocasional")

    @Rule(AS.conduta_fact << Conduta(frequencia_conduta='Repetitivo e/ou Insistente'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_frequencia_repetitivo_insistente(self, conduta_fact):
        self.declare(Agravante(
            tipo='frequencia_repetitivo_insistente',
            explicacao="A frequência da conduta é um agravante, pois acontece frequentemente.",
            incremento_nivel=2
        ))
        self._log_rule_applied("fator_frequencia_repetitivo_insistente")

    @Rule(AS.conduta_fact << Conduta(impacto_vitima='Impacto negativo considerável'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_impacto_negativo_consideravel(self, conduta_fact):
        self.declare(Agravante(
            tipo='impacto_negativo_consideravel',
            explicacao="O impacto na vítima é um agravante, pois gerou consequências de curto prazo.",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_impacto_negativo_consideravel")

    @Rule(AS.conduta_fact << Conduta(impacto_vitima='Impacto Negativo Intenso'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_impacto_negativo_intenso(self, conduta_fact):
        self.declare(Agravante(
            tipo='impacto_negativo_intenso',
            explicacao="O impacto na vítima é um agravante, pois gerou consequências de médio e longo prazo.",
            incremento_nivel=2
        ))
        self._log_rule_applied("fator_impacto_negativo_intenso")

    @Rule(AS.conduta_fact << Conduta(sinais_nao_verbais='Agravado'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_sinais_agravado(self, conduta_fact):
        self.declare(Agravante(
            tipo='sinais_agravado',
            explicacao="Os sinais não-verbais são um agravante, pois intensificam a negatividade da conduta.",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_sinais_agravado")

    @Rule(AS.conduta_fact << Conduta(intencao_percebida='Negligente'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_intencao_negligente(self, conduta_fact):
        self.declare(Agravante(
            tipo='intencao_negligente',
            explicacao="A intenção percebida é um agravante, pois demonstra falta de consideração.",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_intencao_negligente")

    @Rule(AS.conduta_fact << Conduta(intencao_percebida='Intencional'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_intencao_intencional(self, conduta_fact):
        self.declare(Agravante(
            tipo='intencao_intencional',
            explicacao="A intenção percebida é um agravante, pois houve objetivo claro de causar dano.",
            incremento_nivel=2
        ))
        self._log_rule_applied("fator_intencao_intencional")

    @Rule(AS.conduta_fact << Conduta(relacao_hierarquica='Superior - subordinado direto'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_hierarquia_superior_subordinado_direto(self, conduta_fact):
        self.declare(Agravante(
            tipo='hierarquia_superior_subordinado_direto',
            explicacao="A relação hierárquica é um agravante, pois o agressor é superior direto da vítima.",
            incremento_nivel=2
        ))
        self._log_rule_applied("fator_hierarquia_superior_subordinado_direto")

    @Rule(AS.conduta_fact << Conduta(relacao_hierarquica='Superior - subordinado indireto'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_hierarquia_superior_subordinado_indireto(self, conduta_fact):
        self.declare(Agravante(
            tipo='hierarquia_superior_subordinado_indireto',
            explicacao="A relação hierárquica é um agravante, pois o agressor tem posição superior mesmo sem relação direta.",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_hierarquia_superior_subordinado_indireto")










    # --- Regras para Fatores Adicionais (Agravantes) ---

    @Rule(AS.conduta_fact << Conduta(contexto_formal_informal='Formal', contexto_publico_privado='Público'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_contexto_formal_publico(self, conduta_fact):
        self.declare(Agravante(
            tipo='contexto_formal_publico',
            explicacao="O contexto da conduta (Formal/Público) é um agravante...",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_contexto_formal_publico")


    @Rule(AS.conduta_fact << Conduta(descricao=MATCH.descricao, contexto_publico_privado='Privado'),
          TEST(lambda descricao: "conotação sexual" in descricao.lower()),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_contexto_conotacao_sexual_privado(self, conduta_fact):
        self.declare(Agravante(
            tipo='contexto_conotacao_sexual_privado',
            explicacao="O contexto da conduta (conotação sexual/Privado) é um agravante...",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_contexto_conotacao_sexual_privado")


    @Rule(AS.conduta_fact << Conduta(historico_envolvidos='Reincidente'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_historico_reincidente(self, conduta_fact):
        self.declare(Agravante(
            tipo='historico_reincidente',
            explicacao="O histórico do envolvido é um agravante porque há histórico de condutas similares...",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_historico_reincidente")


    @Rule(AS.conduta_fact << Conduta(historico_envolvidos='Frequente'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_historico_frequente(self, conduta_fact):
        self.declare(Agravante(
            tipo='historico_frequente',
            explicacao="O histórico do envolvido é um agravante porque há múltiplas reincidências...",
            incremento_nivel=2
        ))
        self._log_rule_applied("fator_historico_frequente")


    @Rule(AS.conduta_fact << Conduta(frequencia_conduta='Ocasional'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_frequencia_ocasional(self, conduta_fact):
        self.declare(Agravante(
            tipo='frequencia_ocasional',
            explicacao="A frequência da conduta é um agravante, pois ocorre esporadicamente...",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_frequencia_ocasional")


    @Rule(AS.conduta_fact << Conduta(frequencia_conduta='Repetitivo e/ou Insistente'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_frequencia_repetitivo_insistente(self, conduta_fact):
        self.declare(Agravante(
            tipo='frequencia_repetitivo_insistente',
            explicacao="A frequência da conduta é um agravante, pois acontece frequentemente...",
            incremento_nivel=2
        ))
        self._log_rule_applied("fator_frequencia_repetitivo_insistente")


    @Rule(AS.conduta_fact << Conduta(impacto_vitima='Impacto negativo considerável'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_impacto_negativo_consideravel(self, conduta_fact):
        self.declare(Agravante(
            tipo='impacto_negativo_consideravel',
            explicacao="O impacto na vítima é um agravante, pois gerou consequências de curto prazo...",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_impacto_negativo_consideravel")


    @Rule(AS.conduta_fact << Conduta(impacto_vitima='Impacto Negativo Intenso'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_impacto_negativo_intenso(self, conduta_fact):
        self.declare(Agravante(
            tipo='impacto_negativo_intenso',
            explicacao="O impacto na vítima é um agravante, pois gerou consequências de médio e longo prazo...",
            incremento_nivel=2
        ))
        self._log_rule_applied("fator_impacto_negativo_intenso")


    @Rule(AS.conduta_fact << Conduta(sinais_nao_verbais='Agravado'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_sinais_agravado(self, conduta_fact):
        self.declare(Agravante(
            tipo='sinais_agravado',
            explicacao="Os sinais não-verbais são um agravante, pois intensificam a negatividade da conduta...",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_sinais_agravado")


    @Rule(AS.conduta_fact << Conduta(intencao_percebida='Negligente'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_intencao_negligente(self, conduta_fact):
        self.declare(Agravante(
            tipo='intencao_negligente',
            explicacao="A intenção percebida é um agravante, pois demonstra falta de consideração...",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_intencao_negligente")


    @Rule(AS.conduta_fact << Conduta(intencao_percebida='Intencional'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_intencao_intencional(self, conduta_fact):
        self.declare(Agravante(
            tipo='intencao_intencional',
            explicacao="A intenção percebida é um agravante, pois houve objetivo claro de causar dano...",
            incremento_nivel=2
        ))
        self._log_rule_applied("fator_intencao_intencional")


    @Rule(AS.conduta_fact << Conduta(relacao_hierarquica='Superior - subordinado direto'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_hierarquia_superior_subordinado_direto(self, conduta_fact):
        self.declare(Agravante(
            tipo='hierarquia_superior_subordinado_direto',
            explicacao="A relação hierárquica é um agravante, pois o agressor é superior direto da vítima...",
            incremento_nivel=2
        ))
        self._log_rule_applied("fator_hierarquia_superior_subordinado_direto")


    @Rule(AS.conduta_fact << Conduta(relacao_hierarquica='Superior - subordinado indireto'),
          Gravidade(nivel=~L(6)), salience=50)
    def fator_hierarquia_superior_subordinado_indireto(self, conduta_fact):
        self.declare(Agravante(
            tipo='hierarquia_superior_subordinado_indireto',
            explicacao="A relação hierárquica é um agravante, pois o agressor tem posição superior mesmo sem relação direta...",
            incremento_nivel=1
        ))
        self._log_rule_applied("fator_hierarquia_superior_subordinado_indireto")















    # --- Regra de Agravamento Genérica: Elevação de Nível por Múltiplos Agravantes ---
    # --- Regra de Agravamento Genérica: Elevação de Nível por Múltiplos Agravantes ---
    @Rule(
        AS.gravidade_fact << Gravidade(nivel=MATCH.current_level & P(lambda x: x < 6), tipo_avaliacao="base"),
        AS.agravante_1 << Agravante(tipo=~L('multiplos_agravantes_elevacao')),
        AS.agravante_2 << Agravante(tipo=~L('multiplos_agravantes_elevacao')),
        AS.agravante_3 << Agravante(tipo=~L('multiplos_agravantes_elevacao')),
        AS.agravante_4 << Agravante(tipo=~L('multiplos_agravantes_elevacao')),
        TEST(lambda agravante_1, agravante_2, agravante_3, agravante_4:
             len({agravante_1['tipo'], agravante_2['tipo'], agravante_3['tipo'], agravante_4['tipo']}) >= 4),
        NOT(Gravidade(tipo_avaliacao="agravado")), # Impede que a regra dispare se um nível agravado já foi declarado
        salience=1000
    )
    def elevar_nivel_por_multiplos_agravantes(self, gravidade_fact, current_level, agravante_1, agravante_2, agravante_3, agravante_4):
        print(f"DEBUG: Regra 'elevar_nivel_por_multiplos_agravantes' verificando. Nível base: {current_level}")

        # PEGA A EXPLICAÇÃO ORIGINAL DO FATO DE GRAVIDADE BASE
        original_explicacao_base = gravidade_fact['explicacao']

        if gravidade_fact in self.facts.values():
            self.retract(gravidade_fact)
            print(f"DEBUG: Gravidade base (Nível: {gravidade_fact['nivel']}) retraída com sucesso.")
        else:
            print(f"DEBUG: Tentativa de retrair gravidade_fact (Nível: {gravidade_fact['nivel']}) falhou, fato já inexistente ou diferente.")
            return # Se o fato não existe, a regra não deve continuar

        new_level = min(6, current_level + 1)
        
        # OBTÉM A EXPLICAÇÃO PADRÃO PARA O NOVO NÍVEL ELEVADO
        # Adicionamos um fallback caso new_level não esteja no dicionário (embora não deva acontecer aqui)
        new_level_standard_explanation = self._nivel_explanations.get(new_level, f"O nível foi elevado para {new_level}.")

        # CRIA A NOVA EXPLICAÇÃO COMBINANDO A ORIGINAL COM A DA ELEVAÇÃO
        # E TAMBÉM COM A EXPLICAÇÃO PADRÃO DO NOVO NÍVEL
        nova_explicacao = (
            f"{original_explicacao_base} Foi ajustada para: **{new_level_standard_explanation}** "
            f"Isso ocorreu devido à presença de quatro ou mais fatores agravantes."
        )
        
        # OU, uma alternativa mais limpa:
        # nova_explicacao = (
        #     f"A conduta, originalmente classificada como Nível {current_level}, "
        #     f"agora se enquadra no {new_level_standard_explanation}. "
        #     f"Esta elevação de nível é resultado da presença de quatro ou mais fatores agravantes."
        # )


        self.declare(Gravidade(
            nivel=new_level,
            explicacao=nova_explicacao, # Usa a explicação combinada
            tipo_avaliacao="agravado"
        ))
        # Este agravante 'multiplos_agravantes_elevacao' é usado para logar a regra e sua explicação,
        # mas sua 'explicacao' não precisa ser incluída na 'explicacoes_finais' da AvaliacaoFinal
        # porque a informação já está na 'nova_explicacao' da Gravidade final.
        self.declare(Agravante(
            tipo='multiplos_agravantes_elevacao',
            explicacao="O nível de gravidade foi elevado em 1 ponto devido à identificação de quatro ou mais fatores agravantes.",
            incremento_nivel=1
        ))
        self._log_rule_applied("elevar_nivel_por_multiplos_agravantes")
        print(f"DEBUG: Nível elevado para {new_level} e registrado.")


    # --- Regra Final para Consolidar Resultados ---
    @Rule(
        AS.gravidade_final << Gravidade(nivel=MATCH.final_level, explicacao=MATCH.base_explicacao),
        NOT(AvaliacaoFinal()),
        salience=10
    )
    def consolidar_avaliacao(self, gravidade_final, final_level, base_explicacao):
        print(f"DEBUG: Regra 'consolidar_avaliacao' disparada.")
        print(f"DEBUG: Fato Gravidade final casado: {gravidade_final}")
        print(f"DEBUG: Nível final capturado: {final_level}")
        print(f"DEBUG: Explicação base capturada: {base_explicacao}")

        agravantes = [f for f in self.facts.values() if isinstance(f, Agravante)]
        
        # A lista de explicações finais deve começar com a explicação do fato de gravidade final
        # Esta base_explicacao JÁ DEVE CONTER a explicação combinada se a regra de elevação disparou.
        explicacoes_finais = [base_explicacao]
        tipos_incluidos = set()

        # Adiciona as explicações dos agravantes individuais
        for agravante in agravantes:
            # Garante que não adicionamos a explicação do agravante 'multiplos_agravantes_elevacao'
            # pois sua explicação já foi incorporada à 'base_explicacao' se ela disparou.
            if agravante['tipo'] not in tipos_incluidos and agravante['tipo'] != 'multiplos_agravantes_elevacao':
                explicacoes_finais.append(agravante['explicacao'])
                tipos_incluidos.add(agravante['tipo'])
        
        self.declare(AvaliacaoFinal(
            nivel_final_gravidade=final_level, # Usa o final_level já capturado
            explicacoes_finais=explicacoes_finais,
            concluida=True
        ))
        self._log_rule_applied("consolidar_avaliacao")
        print(f"DEBUG: Avaliação final consolidada com nível {final_level} e explicações: {explicacoes_finais}")















    # --- Regra caso nenhuma gravidade seja identificada ---
    @Rule(
        Conduta(),
        NOT(Gravidade()),
        NOT(AvaliacaoFinal()),
        salience=0
    )
    def nenhuma_gravidade_encontrada(self):
        self.declare(AvaliacaoFinal(
            nivel_final_gravidade=0,
            explicacoes_finais=["Não foi possível determinar um nível de gravidade para a conduta com as informações fornecidas."],
            concluida=True
        ))
        self._log_rule_applied("nenhuma_gravidade_encontrada")














    # --- Regras de Recomendação ---
    @Rule(
        AS.avaliacao_final << AvaliacaoFinal(nivel_final_gravidade=6),
        NOT(Recomendacao()),
        salience=-1
    )
    def recomendar_nivel_6(self, avaliacao_final):
        recomendacoes = [
            "A vítima deve procurar a delegacia.",
            "A vítima deve procurar a ouvidoria da UFAPE.",
            "Denuncie na PLATAFORMA FALA.BR disponível no endereço: https://falabr.cgu.gov.br"
        ]
        self.declare(Recomendacao(recomendacoes_texto=recomendacoes))
        self._log_rule_applied("recomendar_nivel_6")


    @Rule(
        AS.avaliacao_final << AvaliacaoFinal(nivel_final_gravidade=5),
        NOT(Recomendacao()),
        salience=-1
    )
    def recomendar_nivel_5(self, avaliacao_final):
        recomendacoes = [
            "A vítima deve procurar a ouvidoria da UFAPE.",
            "Denuncie na PLATAFORMA FALA.BR disponível no endereço: https://falabr.cgu.gov.br.",
            "Caso ache necessário, a vítima pode procurar a delegacia."
        ]
        self.declare(Recomendacao(recomendacoes_texto=recomendacoes))
        self._log_rule_applied("recomendar_nivel_5")


    @Rule(
        AS.avaliacao_final << AvaliacaoFinal(nivel_final_gravidade=P(lambda n: n in [3, 4])),
        NOT(Recomendacao()),
        salience=-1
    )
    def recomendar_nivel_3_4(self, avaliacao_final):
        recomendacoes = [
            "A vítima deve procurar a ouvidoria da UFAPE.",
            "Denuncie na PLATAFORMA FALA.BR disponível no endereço: https://falabr.cgu.gov.br."
        ]
        self.declare(Recomendacao(recomendacoes_texto=recomendacoes))
        self._log_rule_applied("recomendar_nivel_3_4")


    @Rule(
        AS.avaliacao_final << AvaliacaoFinal(nivel_final_gravidade=2),
        NOT(Recomendacao()),
        salience=-1
    )
    def recomendar_nivel_2(self, avaliacao_final):
        recomendacoes = [
            "A vítima deve procurar a ouvidoria da UFAPE, se achar necessário."
        ]
        self.declare(Recomendacao(recomendacoes_texto=recomendacoes))
        self._log_rule_applied("recomendar_nivel_2")


    @Rule(
        AS.avaliacao_final << AvaliacaoFinal(nivel_final_gravidade=P(lambda n: n in [0, 1])),
        NOT(Recomendacao()),
        salience=-2
    )
    def recomendar_nivel_1_ou_nao_determinado(self, avaliacao_final):
        recomendacoes = [
            "Para este nível de gravidade, não há uma recomendação formal de denúncia ou busca de autoridade neste momento. Recomenda-se manter o ambiente de trabalho respeitoso."
        ]
        self.declare(Recomendacao(recomendacoes_texto=recomendacoes))
        self._log_rule_applied("recomendar_nivel_1_ou_nao_determinado")