#facts.py
from experta import Fact, Field

class Conduta(Fact):
    """Representa a conduta sendo avaliada, incluindo sua descrição e fatores."""
    descricao = Field(str, mandatory=True)
    contexto_formal_informal = Field(str, default=None) # 'Formal', 'Informal'
    contexto_publico_privado = Field(str, default=None) # 'Público', 'Privado'
    historico_envolvidos = Field(str, default=None)    # 'Primário', 'Reincidente', 'Frequente'
    frequencia_conduta = Field(str, default=None)      # 'Isolado', 'Ocasional', 'Repetitivo e/ou Insistente'
    impacto_vitima = Field(str, default=None)          # 'Não-significativo', 'Impacto negativo considerável', 'Impacto Negativo Intenso'
    sinais_nao_verbais = Field(str, default=None)      # 'Neutro', 'Agravado'
    intencao_percebida = Field(str, default=None)      # 'Acidental', 'Negligente', 'Intencional'
    relacao_hierarquica = Field(str, default=None)     # 'Mesmo nível hierárquico ou não relevante', 'Superior - subordinado direto', 'Superior - subordinado indireto'


class Gravidade(Fact):
    """Representa o nível de gravidade inferido da conduta."""
    nivel = Field(int, mandatory=True)
    explicacao = Field(str, mandatory=True)
    tipo_avaliacao = Field(str, default="base") # "base" ou "agravado"

class Agravante(Fact):
    """Representa um fator agravante que foi identificado."""
    tipo = Field(str, mandatory=True) # Ex: 'contexto_formal_publico', 'historico_reincidente'
    explicacao = Field(str, mandatory=True)
    incremento_nivel = Field(int, default=0) # Quanto esse agravante aumenta o nível de gravidade

class AvaliacaoFinal(Fact):
    """Fato final que contém o resultado consolidado da avaliação."""
    nivel_final_gravidade = Field(int, mandatory=True)
    explicacoes_finais = Field(list, mandatory=True)
    concluida = Field(bool, default=True)

class Recomendacao(Fact):
    """Fato que contém as recomendações de ação para a vítima."""
    recomendacoes_texto = Field(list, mandatory=True)






















    