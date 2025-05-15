import streamlit as st
import pandas as pd
import datetime
from itertools import zip_longest



def app():
    # while True:
    #     data = input("Digite uma data com sómente numeros no formato dd/mm/aaaa: ")

    #     if not data.isdigit():
    #         print("Erro: Digite somente números.")
    #         continue

    #     if len(data) != 8:
    #         print("Digite uma data com 8 digitos")
    #         continue
    #     else:
    #         data_formatada = data[:2]+"/"+data[2:4]+"/"+data[4:]

    #     try:
    #         valor = float(input("Digite o valor para a conta: "))
    #     except ValueError:
    #         print("Por favor, insira um valor numérico válido.")
    #         continue

    #     while True:
    #         conta_d = input("Em qual conta você vai fazer o lançamento a débito? ").strip().lower()
    #         conta_c = input("Em qual conta você vai fazer o lançamento a crédito? ").strip().lower()

    #         if conta_d == conta_c:
    #             print("Não pode fazer esse mesmo lançamento na mesma conta")
    #             continue
    #         else:
    #             break

    #     for conta_nome in [conta_d, conta_c]:
    #         if conta_nome not in dict_conta:
    #             dict_conta[conta_nome] = {
    #                 'id_conta': descricao_to_conta.get(conta_nome, 'Conta não encontrada'),
    #                 'tipo': conta_nome,
    #                 'débito': [],
    #                 'crédito': [],
    #                 'saldo_debito': [],
    #                 'saldo_credito': []
    #             }

    #     dict_conta[conta_d]['débito'].append(valor)
    #     dict_conta[conta_d]['crédito'].append(0)

    #     dict_conta[conta_c]['crédito'].append(valor)
    #     dict_conta[conta_c]['débito'].append(0)

    #     sair = input("Deseja fazer outro lançamento? (s/n): ").lower()
    #     if sair != 's':
    #         break


    # for descricao, dados in dict_conta.items():
    #     valor_d = sum(dados['débito'])
    #     valor_c = sum(dados['crédito'])
    #     saldo_final = valor_d - valor_c

    #     if saldo_final > 0:
    #         dados['saldo_debito'].append(saldo_final)
    #         saldo_d = f"{saldo_final:.2f}"
    #         saldo_c = None
    #     elif saldo_final < 0:
    #         dados['saldo_credito'].append(abs(saldo_final))
    #         saldo_d = None
    #         saldo_c = f"{abs(saldo_final):.2f}"
    #     else:
    #         saldo_d = saldo_c = 0.00

    #     print(f"\nData: {data_formatada}")
    #     print(f"Descrição: {dados['tipo']}")
    #     print(f"Conta: {dados['id_conta']}")
    #     print("débito       | crédito")
    #     for d, c in zip_longest(dados['débito'], dados['crédito'], fillvalue=0):
    #         d_val = f"{d:.2f}" if d else None
    #         c_val = f"{c:.2f}" if c else None
    #         print(f"{d_val or '':<12} | {c_val or '':<12}")
    #     print("-" * 27)
    #     print(f"{saldo_d or '':<12} | {saldo_c or '':<12}")

    # dados_tabela = []

    # for descricao, dados in dict_conta.items():
    #     for d, c, saldo_d, saldo_c in zip_longest(dados['débito'], dados['crédito'], dados['saldo_debito'], dados['saldo_credito'], fillvalue=""):
    #         dados_tabela.append({
    #             'ID Conta': dados['id_conta'],
    #             'Conta': descricao,
    #             'Data': data_formatada,
    #             'Débito': d,
    #             'Crédito': c,
    #             'Saldo Débito': saldo_d,
    #             'Saldo Crédito': saldo_c
    #         })

    # df = pd.DataFrame(dados_tabela)
    # st.dataframe(df)

    if 'dict_conta' not in st.session_state:
        st.session_state.dict_conta = {}

    dict_conta = st.session_state.dict_conta

    conta = [
        "1.1.1.01.01", "1.1.1.01.02", "1.1.1.02.01", "1.1.1.03.01",
        "1.1.2.01.01", "1.1.2.01.02", "1.1.2.02.01", "1.1.2.02.02",
        "1.1.2.02.03", "1.1.2.02.04", "1.1.2.02.05", "1.1.2.03.01",
        "1.1.2.04.01", "1.1.2.04.02", "1.1.2.04.03", "1.1.2.04.04",
        "1.1.2.04.05", "1.1.2.05.01", "1.1.2.05.02", "1.1.2.05.03",
        "1.1.2.05.04", "1.1.2.05.05", "1.1.2.05.06", "1.1.2.05.07",
        "1.1.2.05.08", "1.1.2.05.09", "1.1.2.05.10", "1.1.2.06.01",
        "1.1.2.06.02", "1.1.2.06.03", "1.1.2.06.04", "1.1.2.06.05",
        "1.1.2.06.06", "1.1.3.01.01", "1.1.3.01.02", "1.1.3.02.01",
        "1.1.3.02.02", "1.1.3.02.03", "1.1.3.02.04", "1.1.3.02.05",
        "1.1.3.03.01", "1.1.3.03.02", "1.1.4.01.01", "1.1.4.01.02",
        "1.1.6.01.99", "1.2.1.01.01", "1.2.1.01.02", "1.2.1.01.03",
        "1.2.1.01.04", "1.2.1.01.05", "1.2.1.01.01", "1.2.1.01.02",
        "1.2.2.01.01", "1.2.2.01.02", "1.2.2.01.03", "1.2.2.01.04",
        "1.2.2.01.05", "1.2.3.01.10", "1.2.3.01.11", "1.2.3.01.20",
        "1.2.3.01.21", "1.2.3.01.30", "1.2.3.01.31", "1.2.3.01.40",
        "1.2.3.01.41", "1.2.3.01.50", "1.2.3.01.51", "1.2.3.01.60",
        "1.2.3.01.61", "1.2.3.02.20", "1.2.3.02.30"
    ]

    descricao = [
        "Caixa", "Fundo Fixo de Caixa", "Bancos Conta Movimento", "Aplicação Financeira de Liquidez Imediata",
        "Contas a Receber", "PECLD", "Adiantamento Quinzenal", "Empréstimos a colaboradores",
        "Antecipação de Salários", "Antecipação de Férias", "Antecipação de 13º Salário", "Adiantamentos a Fornecedores",
        "IRRF", "CSLL Retida na Fonte", "PIS Retido na fonte", "COFINS Retida na Fonte",
        "INSS Retido na Fonte", "IPI a Recuperar", "ICMS a Recuperar", "PIS a Recuperar - Crédito Básico",
        "PIS a Recuperar - Crédito Presumido", "COFINS a Recuperar - Crédito Básico", "COFINS a Recuperar - Crédito Presumido", "CIDE a Recuperar",
        "Outros Impostos e Contribuições a Recuperar", "Saldo Negativo - IRPJ", "Saldo Negativo - CSLL", "IRPJ Estimativa",
        "CSLL Estimativa", "COFINS a Compensar", "PIS/PASEP a Compensar", "IPI a Compensar",
        "INSS a compensar", "Mercadorias para Revenda", "(-) Perda por Ajuste ao Valor Realizável Líquido - Estoque Mercadorias", "Insumos (materiais diretos)",
        "Outros Materiais", "Produtos em Elaboração", "Produtos Acabados", "(-) Perda por Ajuste ao Valor Realizável Líquido - Estoque Produtos",
        "Materiais para Consumo", "Materiais para Reposição", "Aluguéis e Arredamentos Pagos Antecipadamente", "Prêmios de Seguros a Apropriar",
        "Outras Despesas Antecipadas", "Clientes - Longo Prazo", "PCLD Longo Prazo", "Juros a apropriar Clientes LP",
        "Empréstimos de LP", "Juros a apropriar Empréstimos LP", "IRPJ Diferido", "CSLL Diferido",
        "Investimentos em Controladas", "Ágio pago pela mais valia", "Ágio pago por Goodwill", "Investimentos em Coligadas",
        "Investimentos em Joint Ventures", "Terrenos", "Impairment Terrenos", "Edifícios e Construções",
        "Impairment Edifícios e Construções", "Benfeitorias em Imóveis de Terceiros", "Impairment Benfeitorias em Imóveis de Terceiros", "Máquinas, Equipamentos e Instalações Industriais",
        "Impairment Máquinas, Equipamentos e Instalações Industriais", "Móveis, Utensílios e Instalações Comerciais", "Impairment Móveis, Utensílios e Instalações Comerciais", "Veículos",
        "Impairment Veículos", "Depreciação Acumulada - Edifícios e Construções", "Depreciação Acumulada - Benfeitorias em Imóveis de Terceiros"
    ]

    descricao_to_conta = dict(zip(descricao, conta))

    # Formulário para novo lançamento
    with st.form("my_form"):
        st.subheader("Novo Lançamento Contábil")

        selecionar_data = st.date_input("Data do lançamento")

        valor = st.number_input("Valor do lançamento", value=0.01, min_value=0.01)

        conta_d = st.selectbox("Conta de Débito", options=descricao, index=None, placeholder="Selecione")
        conta_c = st.selectbox("Conta de Crédito", options=descricao, index=None, placeholder="Selecione")

        col1, col2 = st.columns(2)
        with col1:
            registrar = st.form_submit_button("Registrar Lançamento")
        with col2:
            limpar = st.form_submit_button("Limpar Lançamentos")

        if registrar:
            if conta_d == conta_c:
                st.error("Não é permitido usar a mesma conta para Débito e Crédito.")
            else:
                for conta_nome in [conta_d, conta_c]:
                    if conta_nome not in dict_conta:
                        dict_conta[conta_nome] = {
                            'id_conta': descricao_to_conta.get(conta_nome, 'Conta não encontrada'),
                            'tipo': conta_nome,
                            'débito': [],
                            'crédito': []
                        }

                dict_conta[conta_d]['débito'].append((valor, selecionar_data))
                dict_conta[conta_c]['crédito'].append((valor, selecionar_data))

                st.success("Lançamento registrado com sucesso!") 

        if limpar:
            st.session_state.dict_conta = {}
            st.info("Lançamentos limpos com sucesso!")

    # Tabela de lançamentos
    from itertools import zip_longest
    import pandas as pd

    dados_tabela = []

    for nome_conta, dados in dict_conta.items():
        debitos = dados['débito']
        creditos = dados['crédito']

        for (d_valor, d_data), (c_valor, c_data) in zip_longest(debitos, creditos, fillvalue=(0.0, "")):
            dados_tabela.append({
                'ID Conta': dados['id_conta'],
                'Conta': nome_conta,
                'Data': d_data or c_data,
                'Débito': d_valor if d_valor else "",
                'Crédito': c_valor if c_valor else ""
            })

    # Cálculo de saldo final por conta
    saldos = []
    for nome_conta, dados in dict_conta.items():
        total_d = sum(v for v, _ in dados['débito'])
        total_c = sum(v for v, _ in dados['crédito'])
        saldo = total_d - total_c
        saldos.append((nome_conta, saldo))

    df = pd.DataFrame(dados_tabela)
    st.subheader("Lançamentos Registrados")
    st.dataframe(df)

    st.subheader("Saldos Finais por Conta")
    for nome, saldo in saldos:
        tipo = "Devedor" if saldo > 0 else "Credor" if saldo < 0 else "Zerado"
        st.write(f"**{nome}** (Saldo {tipo}): R$ {abs(saldo):.2f}")

    st.subheader("Visualização em Razonetes")
    for nome_conta, dados in dict_conta.items():
        id_conta = dados['id_conta']
        debitos = dados['débito']
        creditos = dados['crédito']
        total_d = sum(v for v, _ in debitos)
        total_c = sum(v for v, _ in creditos)
        saldo = total_d - total_c
        tipo_saldo = "Devedor" if saldo > 0 else "Credor" if saldo < 0 else "Zerado"

        debitos_html = "<br>".join(f"{v:.2f}" for v, _ in debitos)
        creditos_html = "<br>".join(f"{v:.2f}" for v, _ in creditos)

        html_razonete = f"""
        <div class="container" style="border:1px solid #ccc; padding:10px; margin-bottom:20px;">
            <div style="text-align:center; font-weight:bold;">{nome_conta}</div>
            <div class="row" style="display:flex; text-align:center; margin-top:10px;">
                <div style="flex:1; border:1px solid #000;">D</div>
                <div style="flex:1; border:1px solid #000;">C</div>
            </div>
            <div class="row" style="display:flex; text-align:center;">
                <div style="flex:1; border:1px solid #000;">{debitos_html}</div>
                <div style="flex:1; border:1px solid #000;">{creditos_html}</div>
            </div>
            <div style="text-align:right; margin-top:5px;">
                <b>Saldo ({tipo_saldo}):</b> R$ {abs(saldo):.2f}
            </div>
        </div>
        """
        st.markdown(html_razonete, unsafe_allow_html=True)
