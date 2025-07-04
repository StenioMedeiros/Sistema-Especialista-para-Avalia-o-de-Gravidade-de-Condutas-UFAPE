import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv # Importa para carregar variáveis de ambiente do .env

# Importa a função de extração de palavras-chave do novo módulo
from gemini_keyword_extractor import extract_keywords_with_gemini
from inference_engine import InferenceEngine # Importa o novo wrapper do motor

st.set_page_config(layout="wide")

# =========================================================================
# Área para configurar sua chave de API do Gemini
#
# Opção 1 (Recomendado): Usar variável de ambiente via .env
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Obtém a chave da variável de ambiente

# Configura a API do Gemini se a chave estiver disponível
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception as e:
        st.error(f"Erro ao configurar a API do Gemini: {e}. Verifique sua chave de API.")
        GOOGLE_API_KEY = None # Invalida se a configuração falhar
else:
    st.error("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada no arquivo .env ou no ambiente.")
    st.warning("Funcionalidades de IA (extração de palavras-chave) estarão desabilitadas.")
    # st.stop() # Descomente esta linha se quiser parar o aplicativo se a chave não estiver configurada

# Inicializa o modelo Gemini Pro FORA da função para evitar recarregamento
# Apenas inicializa se a chave da API foi configurada com sucesso
gemini_model = None
if GOOGLE_API_KEY:
    try:
        # Usando 'gemini-1.5-pro' como um modelo comumente disponível e robusto.
        # Verifique a disponibilidade deste modelo em sua conta Google AI Studio.
        # Se não estiver disponível, tente 'gemini-pro'.
        gemini_model = genai.GenerativeModel('gemini-1.5-flash') 
    except Exception as e:
        st.error(f"Erro ao inicializar o modelo Gemini: {e}. Verifique se sua chave de API está correta e a conexão.")
        gemini_model = None # Garante que seja None em caso de falha

# =========================================================================

def main():
    st.title("**Sistema Especialista para Avaliação de Gravidade de Condutas UFAPE** ")
    st.write("Este sistema avalia a gravidade de condutas no ambiente universitário, com foco em assédio e discriminação, baseado na Matriz de Avaliação da Gravidade de Condutas da UFAPE.")

    st.header("Informações da Conduta")

    descricao_conduta_original = st.text_area("Descreva a conduta:", height=150, help="Descreva detalhadamente o comportamento ou fala a ser avaliado. Inclua palavras-chave que possam indicar o nível de ofensa.")

    # Variável para armazenar as palavras-chave extraídas pelo Gemini
    extracted_keywords_from_gemini = [] 

    # Se uma descrição foi fornecida, tente extrair palavras-chave com o Gemini
    if descricao_conduta_original:
        if gemini_model: # Verifica se o modelo Gemini foi inicializado com sucesso
            with st.spinner("Analisando descrição com IA..."):
                # Chama a função de extração de palavras-chave, passando a descrição original e o modelo Gemini
                extracted_keywords_from_gemini = extract_keywords_with_gemini(descricao_conduta_original, gemini_model)
            
            if extracted_keywords_from_gemini:
                st.info(f"**Palavras-chave detectadas pela IA:** {', '.join(extracted_keywords_from_gemini)}")
            else:
                st.info("Nenhuma palavra-chave relevante detectada pela IA para a descrição fornecida.")
        else:
            st.warning("Modelo Gemini não disponível para extração de palavras-chave. Verifique a configuração da chave de API.")

    st.subheader("**Fatores Adicionais para Avaliação** ")

    st.markdown("---")
    st.markdown("**Fator 1: Contexto em que ocorreu a conduta** ")
    contexto_formal_informal = st.radio(
        "A conduta ocorreu em um ambiente formal ou informal?",
        ('Formal', 'Informal', 'Não se aplica'),
        index=2
    )
    contexto_publico_privado = st.radio(
        "A conduta foi um ato público ou privado?",
        ('Público', 'Privado', 'Não se aplica'),
        index=2
    )
    st.markdown("---")

    st.markdown("**Fator 2: Histórico dos envolvidos**")
    historico_envolvidos = st.radio(
        "Existe histórico de condutas inapropriadas envolvendo a mesma pessoa?",
        ('Primário', 'Reincidente', 'Frequente', 'Não se aplica'),
        index=3,
        help="Primário: Sem histórico anterior. Reincidente: Histórico de condutas similares. Frequente: Múltiplas reincidências que indicam um padrão comportamental."
    )
    st.markdown("---")

    st.markdown("**Fator 3: Frequência das Condutas** ")
    frequencia_conduta = st.radio(
        "Qual a frequência da conduta?",
        ('Isolado', 'Ocasional', 'Repetitivo e/ou Insistente', 'Não se aplica'),
        index=3,
        help="Isolado: Incidente único. Ocasional: Ocorre esporadicamente, mais de uma vez. Repetitivo e/ou Insistente: Acontece frequentemente."
    )
    st.markdown("---")

    st.markdown("**Fator 4: Impacto na Vítima**")
    impacto_vitima = st.radio(
        "Qual o impacto percebido na vítima?",
        ('Impacto não-significativo', 'Impacto negativo considerável', 'Impacto Negativo Intenso', 'Não se aplica'),
        index=3,
        help="Não-significativo: Não teve maiores repercussões. Negativo considerável: Consequências de curto prazo e não muito graves. Negativo Intenso: Consequências de médio e longo prazo, sofrimento físico, emocional ou psicológico."
    )
    st.markdown("---")

    st.markdown("**Fator 5: Sinais Não-Verbais**")
    sinais_nao_verbais = st.radio(
        "Houve sinais não-verbais que intensificaram a conduta?",
        ('Neutro', 'Agravado', 'Não se aplica'),
        index=2,
        help="Neutro: Sem sinais significativos. Agravado: Sinais não-verbais que intensificam a negatividade da conduta."
    )
    st.markdown("---")

    st.markdown("**Fator 6: Intenção Percebida** ")
    intencao_percebida = st.radio(
        "Qual a intenção percebida da conduta?",
        ('Acidental', 'Negligente', 'Intencional', 'Não se aplica'),
        index=3,
        help="Acidental: Sem intenção clara de causar dano. Negligente: Falta de consideração pelas consequências. Intencional: Evidente objetivo de causar dano ou desconforto. "
    )
    st.markdown("---")

    st.markdown("**Fator 7: Relação Hierárquica**")
    relacao_hierarquica = st.radio(
        "Qual a relação hierárquica entre os envolvidos?",
        ('Mesmo nível hierárquico ou nível hierárquico não relevante', 'Superior - subordinado direto', 'Superior - subordinado indireto', 'Não se aplica'),
        index=3,
        help="Superior - subordinado direto: Agressor é superior direto da vítima. Superior - subordinado indireto: Agressor tem posição superior, mas não é o superior direto."
    )
    st.markdown("---")


    if st.button("Avaliar Conduta"):
        if not descricao_conduta_original.strip():
            st.warning("Por favor, descreva a conduta antes de avaliar.")
            return

        # AQUI ESTÁ A MUDANÇA: A descrição para o motor de inferência AGORA É APENAS as palavras-chave do Gemini.
        # Convertemos para minúsculas para garantir a correspondência com as regras.
        descricao_para_engine = ' '.join(extracted_keywords_from_gemini).lower()
        
        st.write(f"Descrição da conduta usada para avaliação (apenas palavras-chave da IA): \"{descricao_para_engine}\"")


        engine = InferenceEngine()

        # Adicionar fatos do formulário, usando a descrição AGORA SUBSTITUÍDA pelas palavras-chave
        engine.add_fact('descricao', descricao_para_engine)
        engine.add_fact('contexto_formal_informal', contexto_formal_informal if contexto_formal_informal != 'Não se aplica' else None)
        engine.add_fact('contexto_publico_privado', contexto_publico_privado if contexto_publico_privado != 'Não se aplica' else None)
        engine.add_fact('historico_envolvidos', historico_envolvidos if historico_envolvidos != 'Não se aplica' else None)
        engine.add_fact('frequencia_conduta', frequencia_conduta if frequencia_conduta != 'Não se aplica' else None)
        engine.add_fact('impacto_vitima', impacto_vitima if impacto_vitima != 'Não se aplica' else None)
        engine.add_fact('sinais_nao_verbais', sinais_nao_verbais if sinais_nao_verbais != 'Não se aplica' else None)
        engine.add_fact('intencao_percebida', intencao_percebida if intencao_percebida != 'Não se aplica' else None)
        engine.add_fact('relacao_hierarquica', relacao_hierarquica if relacao_hierarquica != 'Não se aplica' else None)


        nivel_final, explicacoes, recomendacoes, applied_rules = engine.run()

        st.subheader("Resultado da Avaliação:")
        if nivel_final is not None:
            st.markdown(f"**Nível de Gravidade da Conduta: NÍVEL {nivel_final}**")
        else:
            st.warning("Não foi possível determinar o nível de gravidade da conduta com as informações fornecidas.")

        st.subheader("Explicações Detalhadas:")
        if explicacoes:
            for exp in explicacoes:
                st.info(exp)
        else:
            st.info("Nenhuma explicação detalhada gerada para esta conduta.")

        st.subheader("Recomendações para a Vítima:")
        if recomendacoes:
            for rec in recomendacoes:
                st.success(rec)
        else:
            st.info("Nenhuma recomendação específica gerada para esta conduta neste momento.")

        st.subheader("Regras Aplicadas:")
        if applied_rules:
            for rule_name in applied_rules:
                st.code(rule_name)
        else:
            st.info("Nenhuma regra foi aplicada para esta conduta.")


        st.markdown("""
            ---
            **Observação Importante:** Este sistema é uma ferramenta de apoio baseada na Matriz de Avaliação da Gravidade de Condutas da UFAPE.
            Ele oferece uma classificação inicial e explicações fundamentadas nas regras definidas.
            Para casos reais, a avaliação final e as ações cabíveis devem sempre ser conduzidas por profissionais especializados e seguir os procedimentos oficiais da instituição.
            A UFAPE busca garantir ambientes seguros e inclusivos, construídos por meio de escolhas e atitudes diárias.
        """)

if __name__ == '__main__':
    main()