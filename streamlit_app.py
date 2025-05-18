import streamlit as st
import pandas as pd
import datetime
from itertools import zip_longest

def app():
    # Inicialização do estado da sessão
    if 'dict_conta' not in st.session_state:
        st.session_state.dict_conta = {}

    # Dados completos das contas (exemplo reduzido, mantenha sua lista completa)
    CONTAS = {
        "1":"Ativo",
        "1.1":"Ativo Circulante",
        "1.1.1":"Disponibilidades",
        "1.1.1.01":"Caixa ",
        "1.1.1.01.01":"Caixa (Ativo Circulante)",
        "1.1.1.01.02":"Fundo Fixo de Caixa (Ativo Circulante)",
        "1.1.1.02":"Depósitos Bancários à Vista",
        "1.1.1.02.01":"Bancos Conta Movimento (Ativo Circulante)",
        "1.1.1.03":"Aplicações Financeiras",
        "1.1.1.03.01":"Aplicação Financeira de Liquidez Imediata (Ativo Circulante)",
        "1.1.2":"Créditos",
        "1.1.2.01":"Recebíveis de clientes",
        "1.1.2.01.01":"Contas a Receber (Ativo Circulante)",
        "1.1.2.01.02":"PECLD (Ativo Circulante)",
        "1.1.2.02":"Créditos de Colaboradores",
        "1.1.2.02.01":"Adiantamento Quinzenal (Ativo Circulante)",
        "1.1.2.02.02":"Empréstimos a colaboradores (Ativo Circulante)",
        "1.1.2.02.03":"Antecipação de Salários (Ativo Circulante)",
        "1.1.2.02.04":"Antecipação de Férias (Ativo Circulante)",
        "1.1.2.02.05":"Antecipação de 13º Salário (Ativo Circulante)",
        "1.1.2.03":"Créditos de Fornecedores",
        "1.1.2.03.01":"Adiantamentos a Fornecedores (Ativo Circulante)",
        "1.1.3":"Estoques",
        "1.1.3.01":"Estoques de Mercadorias",
        "1.1.3.01.01":"Mercadorias para Revenda (Ativo Circulante)",
        "1.1.3.01.02":"(-) Perda por Ajuste ao Valor Realizável Líquido - Estoque Mercadorias (Ativo Circulante)",
        "1.1.3.02":"Estoques de Produtos",
        "1.1.3.02.01":"Insumos (materiais diretos) (Ativo Circulante)",
        "1.1.3.02.02":"Outros Materiais (Ativo Circulante)",
        "1.1.3.02.03":"Produtos em Elaboração (Ativo Circulante)",
        "1.1.3.02.04":"Produtos Acabados (Ativo Circulante)",
        "1.1.3.02.05":"(-) Perda por Ajuste ao Valor Realizável Líquido - Estoque Produtos (Ativo Circulante)",
        "1.1.3.03":"Outros Estoques",
        "1.1.3.03.01":"Materiais para Consumo (Ativo Circulante)",
        "1.1.3.03.02":"Materiais para Reposição (Ativo Circulante)",
        "1.1.4":"Despesas Pagas Antecipadamente",
        "1.1.4.01":"Despesas do Exercício Seguinte",
        "1.1.4.01.01":"Aluguéis e Arrendamentos Pagos Antecipadamente (Ativo Circulante)",
        "1.1.4.01.02":"Prêmios de Seguros a Apropriar (Ativo Circulante)",
        "1.1.6.01.99":"Outras Despesas Antecipadas (Ativo Circulante)",
        "1.2":"Ativo Não Circulante",
        "1.2.1":"Realizável a Longo Prazo",
        "1.2.1.01":"Créditos de Longo Prazo",
        "1.2.1.01.01":"Clientes - Longo Prazo (Ativo Não Circulante)",
        "1.2.1.01.02":"PCLD Longo Prazo (Ativo Não Circulante)",
        "1.2.1.01.03":"Juros a Apropriar (Ativo Não Circulante)",
        "1.2.1.01.04":"Empréstimos de LP (Ativo Não Circulante)",
        "1.2.2":"Investimentos",
        "1.2.2.01":"Investimentos Societários",
        "1.2.2.01.01":"Participações Societárias (Ativo Não Circulante)",
        "1.2.3":"Imobilizado",
        "1.2.3.01":"Propriedades para Investimento",
        "1.2.3.01.10":"Terrenos (Ativo Não Circulante)",
        "1.2.3.01.10":"Terrenos para Investimento - Custo (Ativo Não Circulante)",
        "1.2.3.01.11":"Impairment Terrenos (Ativo Não Circulante)",
        "1.2.3.01.20":"Edifícios e Construções (Ativo Não Circulante)",
        "1.2.3.01.20":"Edifícios para Investimento - Custo (Ativo Não Circulante)",
        "1.2.3.01.21":"Impairment Edifícios e Construções (Ativo Não Circulante)",
        "1.2.3.01.21":"Edifícios para Investimento - Depreciação (Ativo Não Circulante)",
        "1.2.3.01.30":"Benfeitorias em Imóveis de Terceiros (Ativo Não Circulante)",
        "1.2.3.01.31":"Impairment Benfeitorias em Imóveis de Terceiros (Ativo Não Circulante)",
        "1.2.3.01.40":"Máquinas, Equipamentos e Instalações Industriais (Ativo Não Circulante)",
        "1.2.3.01.41":"Impairment Máquinas, Equipamentos e Instalações Industriais (Ativo Não Circulante)",
        "1.2.3.01.50":"Móveis, Utensílios e Instalações Comerciais (Ativo Não Circulante)",
        "1.2.3.01.51":"Impairment Móveis, Utensílios e Instalações Comerciais (Ativo Não Circulante)",
        "1.2.3.01.60":"Veículos (Ativo Não Circulante)",
        "1.2.3.01.61":"Impairment Veículos (Ativo Não Circulante)",
        "1.2.3.02":"Imobilizado - Depreciação Acumulada",
        "1.2.3.02.20":"Depreciação Acumulada - Edifícios e Construções (Ativo Não Circulante)",
        "1.2.3.02.30":"Depreciação Acumulada - Benfeitorias em Imóveis de Terceiros (Ativo Não Circulante)",
        "1.2.3.02.40":"Depreciação Acumulada - Máquinas, Equipamentos e Instalações Industriais (Ativo Não Circulante)",
        "1.2.3.02.50":"Depreciação Acumulada - Móveis, Utensílios e Instalações Comerciais (Ativo Não Circulante)",
        "1.2.3.02.51":"Depreciação Acumulada - Veículos (Ativo Não Circulante)",
        "1.2.4":"Intangível",
        "1.2.4.01":"Intangível - Aquisição",
        "1.2.4.01.10":"Softwares (Ativo Não Circulante)",
        "1.2.4.01.20":"Marcas (Ativo Não Circulante)",
        "1.2.4.01.30":"Patentes e Segredos Industriais (Ativo Não Circulante)",
        "1.2.4.02":"Intangível - Amortização",
        "1.2.4.02.10":"Amortização Acumulada - Softwares (Ativo Não Circulante)",
        "1.2.4.02.20":"Amortização Acumulada - Marcas (Ativo Não Circulante)",
        "1.2.4.02.30":"Amortização Acumulada - Patentes e Segredos Industriais (Ativo Não Circulante)",
        "2":"Passivo",
        "2.1":"Passivo Circulante",
        "2.1.1":"Obrigações Trabalhistas",
        "2.1.1.01":"Obrigações com Pessoal",
        "2.1.1.01.01":"Salários e Remunerações a Pagar (Passivo Circulante)",
        "2.1.1.01.02":"Participações no Resultado a Pagar (Passivo Circulante)",
        "2.1.1.01.03":"FGTS a Recolher (Passivo Circulante)",
        "2.1.1.01.04":"Férias (Passivo Circulante)",
        "2.1.1.01.05":"13º Salário (Passivo Circulante)",
        "2.1.1.01.06":"FGTS - Férias (Passivo Circulante)",
        "2.1.1.01.07":"FGTS – 13º Salário (Passivo Circulante)",
        "2.1.2":"Obrigações com Terceiros",
        "2.1.2.01":"Fornecedores",
        "2.1.2.01.01":"Fornecedores Nacionais (Passivo Circulante)",
        "2.1.2.01.02":"Fornecedores Exterior (Passivo Circulante)",
        "2.1.2.02":"Contas a Pagar",
        "2.1.2.02.01":"Aluguéis e arrendamentos a Pagar (Passivo Circulante)",
        "2.1.2.02.02":"Adiantamento de Clientes (Passivo Circulante)",
        "2.1.2.02.03":"Outras Contas a Pagar (Passivo Circulante)",
        "2.1.3":"Empréstimos e Financiamentos (CP)",
        "2.1.3.01":"Empréstimos de Terceiros",
        "2.1.3.01.01":"Duplicatas Descontadas (Passivo Circulante)",
        "2.1.3.01.02":"Empréstimos e Financiamentos (Passivo Circulante)",
        "2.1.4":"Obrigações Fiscais",
        "2.1.4.01":"Impostos a Pagar",
        "2.1.4.01.01":"Simples Nacional (Passivo Circulante)",
        "2.1.4.01.02":"Tributos Municipais (Passivo Circulante)",
        "2.1.4.03":"Parcelamentos Fiscais",
        "2.1.4.03.01":"Parcelamento Simples Nacional CP (Passivo Circulante)",
        "2.1.5":"Outras Obrigações",
        "2.1.5.01":"Obrigações com Sócios",
        "2.1.5.01.01":"Lucros a Pagar (Passivo Circulante)",
        "2.1.5.01.02":"Mútuo com Partes Relacionadas (Passivo Circulante)",
        "2.2":"Passivo Não Circulante",
        "2.2.1":"Obrigações com Terceiros LP",
        "2.2.1.01":"Fornecedores LP",
        "2.2.1.02":"Empréstimos e Financiamentos LP",
        "2.2.1.02.02":"Duplicatas Descontadas LP (Passivo Não Circulante)",
        "2.2.2":"Obrigações Fiscais (LP)",
        "2.2.2.01":"Parcelamentos Fiscais (LP)",
        "2.2.2.01.01":"Parcelamento Simples Nacional LP (Passivo Não Circulante)",
        "2.2.2.01.01":"Empréstimos de Sócios (Passivo Não Circulante)",
        "2.2.2.01.02":"Mútuos com Partes Relacionadas (Passivo Não Circulante)",
        "2.2.3":"Outras Obrigações de LP",
        "2.2.3.01":"Obrigações com Partes Relacionadas",
        "2.3":"Patrimônio Líquido",
        "2.3.1":"Capital Social Integralizado",
        "2.3.1.01":"Capital Social Subscrito ",
        "2.3.1.01.01":"Capital Social Subscrito (Patrimônio Líquido)",
        "2.8.1.02":"Capital Social a Integralizar",
        "2.8.1.02.01":"Capital Social a Integralizar (Patrimônio Líquido)",
        "2.8.2":"Reservas de Capital",
        "2.8.2.01":"Adiantamento de Capital",
        "2.8.2.01.01":"Adiantamento para Futuro Aumento de Capital (Patrimônio Líquido)",
        "2.8.3":"Reservas de Lucro",
        "2.8.3.01":"Lucros a Distribuir",
        "2.8.8":"Resultados Acumulados",
        "2.8.8.01":"Lucros Acumulados",
        "2.8.8.02":"Prejuízos Acumulados",
        "3":"Resultado",
        "3.1":"RECEITAS",
        "3.1.1":"RECEITA BRUTA",
        "3.1.1.01":"RECEITA BRUTA OPERACIONAL",
        "3.1.1.01.01":"Serviços Prestados (Resultado)",
        "3.1.1.01.02":"Mercadorias Vendidas (Resultado)",
        "3.1.1.01.03":"Produtos Vendidos (Resultado)",
        "3.1.2":"DEDUÇÕES DA RECEITA BRUTA",
        "3.1.2.01":"IMPOSTOS S/FATURAMENTO",
        "3.1.2.01.02":"ICMS (Resultado)",
        "3.1.2.01.03":"ISS (Resultado)",
        "3.1.2.01.04":"PIS/Pasep (Resultado)",
        "3.1.2.01.05":"Cofins (Resultado)",
        "3.1.2.02":"OUTRAS DEDUÇÕES DA RECEITA BRUTA",
        "3.1.2.02.01":"DESCONTOS E ABATIMENTOS (Resultado)",
        "3.1.2.02.02":"DEVOLUÇÕES (Resultado)",
        "3.1.2.02.03":"JUROS DE AVP (Resultado)",
        "3.2":"Custos",
        "3.2.1":"Custos dos bens e serviços",
        "3.2.1.01":"Custos dos bens e serviços vendidos",
        "3.2.1.01.01":"Custos dos Produtos Vendidos (Resultado)",
        "3.2.1.01.02":"Custos das Mercadorias Vendidas (Resultado)",
        "3.2.1.01.03":"Custos dos Serviços Prestados (Resultado)",
        "3.3":"Despesas Operacionais",
        "3.3.1":"Despesas com Vendas",
        "3.3.1.01":"Despesas com Pessoal",
        "3.3.1.01.01":"Salários (Resultado)",
        "3.3.1.01.02":"Gratificações (Resultado)",
        "3.3.1.01.04":"13 Salário (Resultado)",
        "3.3.1.01.05":"FGTS (Resultado)",
        "3.3.1.01.06":"Vale Refeição/Refeitório (Resultado)",
        "3.3.1.01.07":"Vale Transporte (Resultado)",
        "3.3.1.01.08":"Assistência Médica (Resultado)",
        "3.3.1.01.09":"Seguro de Vida (Resultado)",
        "3.3.1.01.10":"Treinamento (Resultado)",
        "3.3.1.02":"Outras Despesas com Vendas",
        "3.3.1.02.01":"Comissões sobre Vendas (Resultado)",
        "3.3.1.02.02":"Propaganda e publicidade (Resultado)",
        "3.3.1.02.03":"Brindes e material promocional (Resultado)",
        "3.3.2":"Despesas Administrativas",
        "3.3.2.01.11":"Pro Labore (Resultado)",
        "3.3.2.02":"Despesas Gerais",
        "3.3.2.02.01":"Aluguéis e Arrendamentos (Resultado)",
        "3.3.2.02.02":"Condomínios e Estacionamentos (Resultado)",
        "3.3.2.02.03":"Despesas com Veículos (Resultado)",
        "3.3.2.02.04":"Depreciação (Resultado)",
        "3.3.2.02.05":"Amortização (Resultado)",
        "3.3.2.02.06":"Serviços Profissionais Contratados (Resultado)",
        "3.3.2.02.07":"Energia (Resultado)",
        "3.3.2.02.08":"Água e Esgoto (Resultado)",
        "3.3.2.02.09":"Telefone e Internet (Resultado)",
        "3.3.2.02.10":"Correios e Malotes (Resultado)",
        "3.3.2.02.11":"Seguros (Resultado)",
        "3.3.2.02.12":"Multas (Resultado)",
        "3.3.2.02.13":"Bens de Pequeno Valor (Resultado)",
        "3.3.2.02.14":"Material de Escritório (Resultado)",
        "3.3.2.03":"Tributos e Contribuições",
        "3.3.2.03.01":"Taxas e Tributos Municipais (Resultado)",
        "3.3.9":"Outros Resultados Operacionais",
        "3.3.9.01":"Ganhos e Perdas de Capital",
        "3.3.9.01.01":"Receita na Venda de Investimento, Imobilizado ou Intangível (Resultado)",
        "3.3.9.01.02":"Custo do Investimento, Imobilizado ou Intangível Baixado (Resultado)",
        "3.3.9.02":"Perdas",
        "3.3.9.02.02":"Perda de recuperabilidade (Impairment) (Resultado)",
        "3.3.9.03":"Resultado de Participação em Outras Sociedades",
        "3.3.9.03.01":"Receita de Participação Societária (Resultado)",
        "3.4":"Resultado Financeiro",
        "3.4.1":"Encargos Financeiros Líquidos",
        "3.4.1.01":"Despesas Financeiras",
        "3.4.1.01.01":"Juros Passivos (Resultado)",
        "3.4.1.01.02":"Despesas Bancárias (Resultado)",
        "3.4.1.01.03":"IOF (Resultado)",
        "3.4.1.01.04":"Descontos Concedidos (Resultado)",
        "3.4.1.01.05":"Variação Cambial Passiva (Resultado)",
        "3.4.1.02":"Receitas Financeiras",
        "3.4.1.02.01":"Rendimentos de Aplicação Financeira (Resultado)",
        "3.4.1.02.02":"Juros Ativos (Resultado)",
        "3.4.1.02.03":"Descontos Obtidos (Resultado)",
        "3.4.1.02.04":"Variação Cambial Ativa (Resultado)"
    }

    # Criar mapeamento reverso
    DESCRICAO_TO_CONTA = {v: k for k, v in CONTAS.items()}

    def calcular_saldos():
        saldos = {}
        for conta, dados in st.session_state.dict_conta.items():
            total_debito = sum(valor for valor, _ in dados['débito'])
            total_credito = sum(valor for valor, _ in dados['crédito'])
            saldos[conta] = total_debito - total_credito
        return saldos

    def gerar_relatorio_patrimonio():
        saldos = calcular_saldos()
        
        ativo = 0
        passivo = 0
        patrimonio = 0
        
        for conta_desc, saldo in saldos.items():
            codigo = DESCRICAO_TO_CONTA.get(conta_desc, "")
            
            if codigo.startswith('1.'):  # Ativo
                ativo += saldo
            elif codigo.startswith('2.'):  # Passivo ou Patrimônio Líquido
                if codigo.startswith('2.3'):  # Patrimônio Líquido
                    patrimonio += saldo
                else:  # Demais códigos do passivo
                    passivo += saldo
            elif codigo.startswith('3.'):  # Resultado (não entra no balanço)
                continue

        return {
            "Ativo Total": abs(ativo),
            "Patrimônio Líquido": abs(patrimonio),
            "Passivo Total": abs(passivo),
        }

    # Interface
    st.title("Help MEI - Contabilidade")

    with st.form("my_form"):
        st.subheader("Novo Lançamento")
        
        data = st.date_input("Data")
        valor = st.number_input("Valor", min_value=0.01, step=0.01, format="%.2f")

        
        contas_filtradas = {
            descricao: codigo 
            for descricao, codigo in DESCRICAO_TO_CONTA.items()
            if len(codigo.replace(".", "")) == 7
        }

        conta_debito = st.selectbox("Débito", options=list(contas_filtradas.keys()))
        conta_credito = st.selectbox("Crédito", options=list(contas_filtradas.keys()))
        
        submitted = st.form_submit_button("Registrar")
        
        if submitted:
            if not conta_debito or not conta_credito:
                st.error("Selecione ambas as contas!")
            elif conta_debito == conta_credito:
                st.error("Contas de débito e crédito não podem ser iguais!")
            else:
                # Inicializar contas se não existirem
                for conta in [conta_debito, conta_credito]:
                    if conta not in st.session_state.dict_conta:
                        st.session_state.dict_conta[conta] = {
                            'débito': [],
                            'crédito': []
                        }
                
                # Registrar lançamento
                st.session_state.dict_conta[conta_debito]['débito'].append((valor, data))
                st.session_state.dict_conta[conta_credito]['crédito'].append((valor, data))
                st.success("Lançamento registrado!")

    # Botões de limpeza e relatório
    if st.button("Limpar Lançamentos"):
        st.session_state.dict_conta = {}
        st.success("Lançamentos removidos!")

    if st.button("Gerar Balanço"):
        relatorio = gerar_relatorio_patrimonio()
        
        
        st.subheader("Balanço Patrimonial")

        saldos = calcular_saldos()

        # Separar contas conforme estrutura contábil
        linhas_ativo = []
        linhas_passivo_pl = []

        for conta_desc, saldo in saldos.items():
            codigo = DESCRICAO_TO_CONTA.get(conta_desc, "")
            if saldo == 0 or not codigo:
                continue

            linha = {"Conta": f"{conta_desc}", "Saldo": abs(saldo)}

            if codigo.startswith("1."):
                linhas_ativo.append(linha)
            elif codigo.startswith("2."):  # Passivo e Patrimônio Líquido
                linhas_passivo_pl.append(linha)
                
        # Garantir alinhamento das tabelas
        len_max = max(len(linhas_ativo), len(linhas_passivo_pl))
        linhas_ativo += [{}] * (len_max - len(linhas_ativo))
        linhas_passivo_pl += [{}] * (len_max - len(linhas_passivo_pl))

        # Mostrar lado a lado
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Ativo")
            st.table(pd.DataFrame(linhas_ativo))

        with col2:
            st.markdown("#### Passivo + Patrimônio Líquido")
            st.table(pd.DataFrame(linhas_passivo_pl))

        # Totais
        totais = gerar_relatorio_patrimonio()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total do Ativo", f"R$ {totais['Ativo Total']:,.2f}".replace(".", ","))
        with col2:
            st.metric("Total Passivo + PL", f"R$ {(totais['Passivo Total'] + totais['Patrimônio Líquido']):,.2f}".replace(".", ","))
        
        
        if relatorio['Patrimônio Líquido'] >= 0:
            st.success("Situação líquida positiva!")
        else:
            st.error("Situação líquida negativa!")

    # Exibir lançamentos
    if st.session_state.dict_conta:
        st.subheader("Lançamentos Registrados")
        
        dados = []
        saldos = calcular_saldos()
        
        for conta, movimentos in st.session_state.dict_conta.items():
            codigo = DESCRICAO_TO_CONTA.get(conta, "N/A")
            
            for valor, data in movimentos['débito']:
                dados.append({
                    "Data": data,
                    "Conta": f"{codigo} - {conta}",
                    "Débito": valor,
                    "Crédito": None
                })
            
            for valor, data in movimentos['crédito']:
                dados.append({
                    "Data": data,
                    "Conta": f"{codigo} - {conta}",
                    "Débito": None,
                    "Crédito": valor
                })
        
        if dados:
            df = pd.DataFrame(dados)
            st.dataframe(df)
        else:
            st.info("Nenhum lançamento registrado.")

        # Exibir razonetes
        st.subheader("Razonetes")
        for conta, movimentos in st.session_state.dict_conta.items():
            codigo = DESCRICAO_TO_CONTA.get(conta, "N/A")
            saldo = saldos[conta]
            
            st.write(f"**{codigo} - {conta}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Débito**")
                for valor, data in movimentos['débito']:
                    st.write(f"R$ {valor:,.2f} - {data}")
            
            with col2:
                st.write("**Crédito**")
                for valor, data in movimentos['crédito']:
                    st.write(f"R$ {valor:,.2f} - {data}")
            
            st.write(f"**Saldo:** R$ {abs(saldo):,.2f} ({'Devedor' if saldo > 0 else 'Credor' if saldo < 0 else 'Zerado'})")
            st.divider()
    else:
        st.info("Nenhum lançamento registrado. Use o formulário acima para adicionar.")