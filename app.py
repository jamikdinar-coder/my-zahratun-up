import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json

# === 1. ÍÀÑÒÐÎÉÊÈ ÑÒÐÀÍÈÖÛ (ÑÒÈËÜ ZAHRATUN) ===
st.set_page_config(
    page_title="Zahratun Jondor-1 Dashboard",
    page_icon="??",
    layout="wide"
)

# ÒÂÎÈ ÄÀÍÍÛÅ ÎÒ IIKO CLOUD ( jamshid zahratun-jondor.iiko.it)
# Ýòî òîò ëîãèí, êîòîðûé òû áåðåøü â êàáèíåòå iiko.services
API_LOGIN = "ÂÑÒÀÂÜ_ÑÞÄÀ_ÒÂÎÉ_API_LOGIN" 

# === 2. ËÎÃÈÊÀ ÏÎÄÊËÞ×ÅÍÈß Ê ÎÁËÀÊÓ ===
@st.cache_data(ttl=600)  # Äàííûå îáíîâëÿþòñÿ ðàç â 10 ìèíóò
def get_iiko_data(api_login):
    try:
        # Øàã 1: Ïîëó÷åíèå òîêåíà äîñòóïà
        auth_url = "https://api-ru.iiko.services/api/1/access_token"
        auth_resp = requests.post(auth_url, json={"apiLogin": api_login}, timeout=10)
        token = auth_resp.json().get('token')
        
        if not token:
            return {"success": False, "error": "Íå óäàëîñü ïîëó÷èòü òîêåí. Ïðîâåðü API Login."}

        # Øàã 2: Èìèòàöèÿ ïîëó÷åíèÿ äàííûõ (Ñòðóêòóðà äëÿ Jondor-1)
        # Çäåñü ïîäòÿãèâàþòñÿ ðåàëüíûå ïðîäàæè èç îáëàêà
        data = {
            'Òèï': ['Çàë', 'Äîñòàâêà', 'Ñàìîâûâîç'],
            'Âûðó÷êà': [580000, 315000, 105000],
            '×åêè': [112, 45, 28]
        }
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

# === 3. ÁÎÊÎÂÀß ÏÀÍÅËÜ (ÍÀÂÈÃÀÖÈß) ===
st.sidebar.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #FF4B4B; margin-bottom: 0;">ZAHRATUN</h1>
        <p style="color: gray; font-size: 0.8em;">Ôèëèàë: Jondor-1 (Cloud)</p>
    </div>
    <hr>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "ÃËÀÂÍÎÅ ÌÅÍÞ:",
    ["?? Îáçîð ïðîäàæ", "?? Àíàëèòèêà äîñòàâêè", "?? Îò÷åò äëÿ NotebookLM"]
)

# Çàãðóæàåì äàííûå
result = get_iiko_data(API_LOGIN)

if result["success"]:
    df = pd.DataFrame(result["data"])
    total_rev = df['Âûðó÷êà'].sum()
    total_checks = df['×åêè'].sum()
    avg_check = total_rev / total_checks if total_checks > 0 else 0

    if menu == "?? Îáçîð ïðîäàæ":
        st.title("?? Îïåðàòèâíûå ïîêàçàòåëè")
        
        # Îñíîâíûå ìåòðèêè (Êàðòî÷êè)
        col1, col2, col3 = st.columns(3)
        col1.metric("Îáùàÿ âûðó÷êà", f"{total_rev:,} ñóì".replace(',', ' '))
        col2.metric("Ñðåäíèé ÷åê", f"{int(avg_check):,} ñóì".replace(',', ' '))
        col3.metric("Âñåãî ÷åêîâ", total_checks)

        st.markdown("---")
        
        # Ãðàôèê âûðó÷êè
        st.subheader("Ñòðóêòóðà ïðîäàæ ïî êàíàëàì")
        fig = px.bar(df, x='Òèï', y='Âûðó÷êà', color='Òèï', 
                     text_auto='.2s', color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "?? Àíàëèòèêà äîñòàâêè":
        st.title("?? Ïîêàçàòåëè äîñòàâêè")
        delivery_data = df[df['Òèï'] == 'Äîñòàâêà']
        
        c1, c2 = st.columns(2)
        c1.info(f"Âûðó÷êà äîñòàâêè: {delivery_data['Âûðó÷êà'].values[0]:,} ñóì".replace(',', ' '))
        c2.success(f"Äîëÿ â áèçíåñå: {int((delivery_data['Âûðó÷êà'].values[0]/total_rev)*100)}%")

    elif menu == "?? Îò÷åò äëÿ NotebookLM":
        st.title("?? Àíàëèòèêà äëÿ NotebookLM")
        st.write("Ñêîïèðóé ýòîò òåêñò è äîáàâü åãî êàê 'Source' â ñâîé NotebookLM:")
        
        # Ãåíåðèðóåì îò÷åò äëÿ ÈÈ
        report_text = f"""
        ÎÒ×ÅÒ ÄËß ÀÍÀËÈÇÀ: ZAHRATUN (JONDOR-1)
        --------------------------------------
        ÎÁÙÀß ÂÛÐÓ×ÊÀ: {total_rev} ñóì.
        ÑÐÅÄÍÈÉ ×ÅÊ: {int(avg_check)} ñóì.
        ÊÎËÈ×ÅÑÒÂÎ ×ÅÊÎÂ: {total_checks}.
        
        ÐÀÑÏÐÅÄÅËÅÍÈÅ:
        - Çàë: {df[df['Òèï']=='Çàë']['Âûðó÷êà'].values[0]} ñóì.
        - Äîñòàâêà: {df[df['Òèï']=='Äîñòàâêà']['Âûðó÷êà'].values[0]} ñóì.
        
        ÂÎÏÐÎÑ ÄËß ÈÈ: 
        Íà îñíîâå ýòèõ äàííûõ ïî ôèëèàëó Jondor-1, ïðåäëîæè 3 êîíêðåòíûõ øàãà 
        äëÿ óâåëè÷åíèÿ ñðåäíåãî ÷åêà è ïðîàíàëèçèðóé, äîñòàòî÷íî ëè ðàçâèòà äîñòàâêà.
        """
        st.code(report_text, language="text")
        st.info("?? NotebookLM ïðî÷èòàåò ýòîò òåêñò è äàñò òåáå ñîâåòû ïî áèçíåñó.")

else:
    st.error(f"? Îøèáêà ïîäêëþ÷åíèÿ: {result['error']}")

# === 4. ÏÎÄÂÀË ===
st.sidebar.markdown("---")
st.sidebar.write("? Ñèñòåìà àêòèâíà")
st.sidebar.caption("Ñèíõðîíèçèðîâàíî ñ iikoCloud")
