"""
Aplicativo de Organização de Estudos Universitários
Desenvolvido com Streamlit para interface web interativa.

Funcionalidades:
- Cadastrar matérias
- Registrar tempo de estudo
- Editar e excluir matérias
- Visualizar gráfico de distribuição do tempo de estudo
- Persistência de dados em arquivo JSON
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from study_organizer import StudyOrganizer

# Configuração da página
st.set_page_config(
    page_title="Organizador de Estudos",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa o organizador de estudos
@st.cache_resource
def get_organizer():
    return StudyOrganizer()

organizer = get_organizer()

# Título principal
st.title("📚 Organizador de Estudos Universitários")
st.markdown("---")

# Sidebar para adicionar matéria
st.sidebar.header("➕ Adicionar Nova Matéria")
with st.sidebar.form("add_subject_form", clear_on_submit=True):
    new_subject_name = st.text_input("Nome da Matéria", placeholder="Ex: Cálculo I")
    add_subject_button = st.form_submit_button("Adicionar Matéria", use_container_width=True)
    
    if add_subject_button and new_subject_name.strip():
        if organizer.add_subject(new_subject_name.strip()):
            st.sidebar.success(f"✅ Matéria \'{new_subject_name}\' adicionada!")
            st.rerun()
        else:
            st.sidebar.warning(f"⚠️ Matéria \'{new_subject_name}\' já existe.")
    elif add_subject_button and not new_subject_name.strip():
        st.sidebar.error("❌ Por favor, digite o nome da matéria.")

# Obter matérias atuais
subjects = organizer.get_all_subjects()

# Seção principal: Lista de matérias
st.header("📋 Minhas Matérias e Tempo de Estudo")

if not subjects:
    st.info("🎯 Nenhuma matéria cadastrada ainda. Adicione uma matéria na barra lateral para começar!")
else:
    # Criar DataFrame para melhor visualização
    df_subjects = pd.DataFrame([
        {"Matéria": name, "Tempo de Estudo (min)": data["study_time"], "Tempo de Estudo (h)": round(data["study_time"]/60, 2)}
        for name, data in subjects.items()
    ])
    
    # Exibir tabela
    st.dataframe(df_subjects, use_container_width=True, hide_index=True)
    
    # Estatísticas rápidas
    total_time = sum(data["study_time"] for data in subjects.values())
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Matérias", len(subjects))
    with col2:
        st.metric("Tempo Total de Estudo", f"{total_time} min")
    with col3:
        st.metric("Tempo Total de Estudo", f"{round(total_time/60, 2)} h")

st.markdown("---")

# Seção: Registrar tempo de estudo
st.header("⏱️ Registrar Tempo de Estudo")

if subjects:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("record_time_form", clear_on_submit=True):
            subject_to_record = st.selectbox("Selecione a Matéria", list(subjects.keys()))
            time_to_add = st.number_input("Tempo de Estudo (minutos)", min_value=1, max_value=1440, value=30, step=5)
            record_button = st.form_submit_button("📝 Registrar Tempo", use_container_width=True)
            
            if record_button:
                if organizer.record_study_time(subject_to_record, time_to_add):
                    st.success(f"✅ Tempo de {time_to_add} minutos registrado para {subject_to_record}!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao registrar tempo de estudo.")
    
    with col2:
        st.info("💡 **Dica:** Registre seu tempo de estudo regularmente para acompanhar seu progresso!")
else:
    st.info("🎯 Adicione matérias para registrar tempo de estudo.")

st.markdown("---")

# Seção: Editar/Excluir matérias
st.header("✏️ Gerenciar Matérias")

if subjects:
    selected_subject = st.selectbox("Selecione a Matéria para Editar ou Excluir", list(subjects.keys()), key="manage_select")
    
    col_edit, col_delete = st.columns(2)
    
    with col_edit:
        st.subheader("✏️ Editar Matéria")
        with st.form("edit_subject_form", clear_on_submit=True):
            new_name_edit = st.text_input("Novo Nome da Matéria", value=selected_subject, placeholder="Digite o novo nome")
            edit_button = st.form_submit_button("💾 Salvar Edição", use_container_width=True)
            
            if edit_button:
                if new_name_edit.strip() and new_name_edit.strip() != selected_subject:
                    if organizer.update_subject_name(selected_subject, new_name_edit.strip()):
                        st.success(f"✅ Matéria atualizada para \'{new_name_edit}\'!")
                        st.rerun()
                    else:
                        st.error(f"❌ Não foi possível atualizar. O nome \'{new_name_edit}\' já existe.")
                elif not new_name_edit.strip():
                    st.error("❌ Por favor, digite um nome válido.")
                else:
                    st.warning("⚠️ O nome não foi alterado.")
    
    with col_delete:
        st.subheader("🗑️ Excluir Matéria")
        st.warning(f"⚠️ Você está prestes a excluir a matéria **{selected_subject}** e todos os dados associados.")
        
        if st.button("🗑️ Confirmar Exclusão", key="delete_subject_button", use_container_width=True, type="secondary"):
            if organizer.delete_subject(selected_subject):
                st.success(f"✅ Matéria \'{selected_subject}\' excluída com sucesso!")
                st.rerun()
            else:
                st.error(f"❌ Não foi possível excluir a matéria \'{selected_subject}\'.")
else:
    st.info("🎯 Nenhuma matéria disponível para editar ou excluir.")

st.markdown("---")

# Seção: Gráfico de distribuição
st.header("📊 Distribuição do Tempo de Estudo")

if subjects:
    # Preparar dados para o gráfico
    subject_names = [name for name, data in subjects.items()]
    study_times = [data["study_time"] for name, data in subjects.items()]
    
    if sum(study_times) > 0:
        # Criar DataFrame para o gráfico
        df_chart = pd.DataFrame({
            'Matéria': subject_names,
            'Tempo de Estudo': study_times
        })
        
        # Configurar o gráfico
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(df_chart)))
        
        wedges, texts, autotexts = ax.pie(
            df_chart['Tempo de Estudo'], 
            labels=df_chart['Matéria'], 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=colors,
            pctdistance=0.85
        )
        
        # Melhorar a aparência do gráfico
        ax.set_title('Distribuição do Tempo de Estudo por Matéria', fontsize=16, fontweight='bold', pad=20)
        
        # Melhorar a legibilidade dos textos
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Garantir que o gráfico seja um círculo
        ax.axis('equal')
        
        # Exibir o gráfico
        st.pyplot(fig)
        
        # Mostrar estatísticas detalhadas
        st.subheader("📈 Estatísticas Detalhadas")
        df_stats = df_chart.copy()
        df_stats['Percentual'] = (df_stats['Tempo de Estudo'] / df_stats['Tempo de Estudo'].sum() * 100).round(1)
        df_stats['Tempo (horas)'] = (df_stats['Tempo de Estudo'] / 60).round(2)
        df_stats = df_stats.sort_values('Tempo de Estudo', ascending=False)
        
        st.dataframe(df_stats, use_container_width=True, hide_index=True)
        
    else:
        st.info("📊 Registre tempo de estudo para ver a distribuição no gráfico.")
else:
    st.info("🎯 Adicione matérias e registre tempo de estudo para ver o gráfico.")

# Rodapé
st.markdown("---")
st.markdown("**💡 Dicas de Uso:**")
st.markdown("""
- 📝 Registre seu tempo de estudo logo após cada sessão
- 📊 Use o gráfico para identificar matérias que precisam de mais atenção
- 🎯 Defina metas de tempo de estudo para cada matéria
- 💾 Seus dados são salvos automaticamente no arquivo `study_data.json`
""")


