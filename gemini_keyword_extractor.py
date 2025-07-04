import google.generativeai as genai

def extract_keywords_with_gemini(text_input: str, gemini_model: genai.GenerativeModel) -> list[str]:

    # Verifica se a entrada está vazia ou se o modelo Gemini não foi fornecido/inicializado.
    if not text_input.strip() or gemini_model is None:
        print("A descrição da conduta está vazia ou o modelo Gemini não está disponível.")
        return []

    # CONJUNTO DE PALAVRAS-CHAVE DAS SUAS REGRAS
    # Este conjunto DEVE ser idêntico ao que você usa nas suas regras (rules.py)

    allowed_keywords = [
        # Nível 1
        "não ofensivo", "socialmente aceitável", "comentários neutros", 
        "elogios simples", "discussões neutras",

        # Nível 2
        "constrangedor", "levemente ofensivo", "causa desconforto", 
        "estereótipos sutis", "comentários desrespeitosos",
        "perguntas habilidades gênero", "comentários aparência etnia",

        # Nível 3
        "ofensivo", "reforçam estereótipos", "piadas sexuais", 
        "apelidos pejorativos", "reproduz privilégio",

        # Nível 4
        "bastante ofensivo", "explicitamente humilhante", 
        "toques não solicitados", "danos emocionais", 
        "insultos diretos", "humilhação maliciosa",

        # Nível 5
        "agressivo não físico", "ambiente hostil", 
        "avanços sexuais", "comentários racistas", 
        "material pornográfico",

        # Nível 6
        "agressão física", "violência física", 
        "ameaça grave", "coerção física",

        # Fatores adicionais (alguns destes também podem aparecer nas descrições)
        "formal", "informal", "público", "privado", 
        "conotação sexual", "reincidente", "frequente", 
        "ocasional", "isolado", "impacto negativo considerável", 
        "impacto negativo intenso", "não-significativo", "agravado", 
        "neutro", "negligente", "acidental", "intencional", 
        "superior - subordinado direto", "superior - subordinado indireto", 
        "mesmo nível hierárquico"
    ]


    try:
        # O prompt instrui o modelo a focar nessas palavras-chave específicas.
        # Adicionei uma menção para retornar a correspondência exata dos termos da lista.
        prompt = (
            f"Analise a seguinte descrição de conduta em português. "
            f"Retorne APENAS as palavras-chave exatas que correspondem ou são sinônimos muito próximos "
            f"dos termos na seguinte lista. Priorize os termos exatos da lista. "
            f"Se um termo da lista não for claramente aplicável ou inferível, não o inclua.\n"
            f"Lista de termos prioritários: {', '.join(allowed_keywords)}\n\n"
            f"Descrição: \"{text_input}\"\n\n"
            f"Palavras-chave extraídas (separadas por vírgula e em minúsculas):"
        )

        response = gemini_model.generate_content(prompt)
        keywords_raw = response.text.strip()

        # Limpa e formata a resposta.
        # Filtra para garantir que apenas as palavras-chave da lista permitida sejam consideradas.
        # Convertemos tudo para minúsculas para a comparação.
        keywords_list = [
            kw.strip().lower() for kw in keywords_raw.split(',')
            if kw.strip().lower() in [term.lower() for term in allowed_keywords]
        ]
        
        # Opcional: Adicionar palavras-chave diretamente da descrição original
        # que também estejam em allowed_keywords, caso o Gemini perca algo.
        # Isso pode ser útil para garantir cobertura máxima.
        for term in allowed_keywords:
            if term.lower() in text_input.lower() and term.lower() not in keywords_list:
                keywords_list.append(term.lower())

        return list(set(keywords_list)) # Remove duplicatas
                                        # (se a ordem importar, use uma lista normal e um set para verificar duplicatas)

    except Exception as e:
        # A manipulação de erros para a API deve ser robusta no app.py.
        # Aqui, apenas imprimimos para depuração e retornamos vazio.
        print(f"Ocorreu um erro ao chamar a API da Gemini no extrator: {e}")
        return []