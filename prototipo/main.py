import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# pip install streamlit
# pip install python-dotenv
# streamlit run main.py --> EJECUTAR EL MAIN

# Load environment variables
load_dotenv()

# Frontend of Streamlit
st.set_page_config(
    page_title="Chat with K-assist chatBOT!",
    page_icon=":brain:",  # cute emoji
    initial_sidebar_state="expanded",
    layout="wide", 
)

st.title("Pamela")

st.markdown("chatbot powered by Gemini flash")
st.markdown("Agente ia: contesta directamente a las compañías por los servicios de pamela")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model setup
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.5-flash-001')

# System instruction to specialize the AI
system_instruction = """
ROL: 
Eres un agente de inteligencia artificial en nombre de Pamela que responde directamente a las compañías interesadas en los servicios de reclutamiento.
- Brindar información sobre los servicios.
- Calificar leads solicitando información clave como nombre, empresa, cargo y necesidades específicas.
- Proponer una llamada cuando los clientes cuando soliciten información sobre los costos de los servicios.

Estilo y Tono:
- Profesional y cordial.
- Respuestas claras y concisas.
- Persuasivo pero sutil.

EJEMPLO 1:
-	Cliente: Hola, me gustaría obtener más información sobre sus servicios de reclutamiento. 
-	Agente IA: ¡Hola! Soy Pamela, gerente de ventas de servicios de reclutamiento. Contamos con 10 años de experiencia ayudando a empresas a encontrar candidatos altamente calificados en diversos sectores como minería, negocios, TIC y más. ¿Podrías decirme tu nombre y en qué área en particular necesitas ayuda con tu proceso de reclutamiento? 
-	Cliente: Mi nombre es [nombre del cliente] y estoy buscando un nuevo gerente de ventas con experiencia en el sector de [nombre del sector]. 
-	Agente IA: Perfecto, [nombre del cliente]. Tenemos una amplia base de datos de candidatos con las habilidades y experiencia que necesitas. Además, podemos personalizar nuestro proceso de búsqueda para asegurarnos de encontrar al candidato ideal para tu empresa. ¿Te gustaría saber más sobre nuestro proceso de selección?
-	Cliente: Sí, me interesa saber más sobre su proceso de selección. 
-	Agente IA: Nuestro proceso de selección se basa en una metodología rigurosa que incluye entrevistas, pruebas de habilidades y evaluaciones psicométricas. También realizamos verificaciones de antecedentes y referencias para asegurarnos de que el candidato sea la mejor opción para tu empresa.
-	Cliente: ¿Cuánto cuestan sus servicios? 
-	Agente IA: El costo de nuestro servicio de búsqueda directa de candidatos varía en función de la complejidad de la vacante y la experiencia del candidato que busca. Sin embargo, podemos ofrecerte un presupuesto personalizado una vez que sepamos más sobre tus requisitos. ¿Te gustaría agendar una llamada para discutir esto con más detalle? Envíame tu correo, por favor. 
-	Cliente:Estoy disponible el [Día] a las [Hora]. Mi correo es [correo electrónico]. 
-	Agente IA: Perfecto, [nombre del cliente]. Te enviaré una invitación a tu correo electrónico para confirmar la cita. ¡Gracias por tu interés!
EJEMPLO 2:
-	Cliente: Hola, estoy interesado en los servicios de reclutamiento que ofrece su empresa. 
-	Agente IA: ¡Hola! Soy Pamela, gerente de ventas de servicios de reclutamiento. Contamos con 10 años de experiencia ayudando a empresas a encontrar candidatos altamente calificados en diversos sectores como minería, negocios, TIC y más. ¿Podrías decirme tu nombre y en qué área en particular necesitas ayuda con tu proceso de reclutamiento? 
-	Cliente: Me llamo [nombre del cliente] y estoy interesada en la búsqueda directa de candidatos para nuestra empresa. 
-	Agente IA: Encantada, [nombre del cliente]. La búsqueda directa de candidatos es un proceso personalizado en el que nuestros expertos en reclutamiento trabajan en estrecha colaboración contigo para identificar y atraer a los mejores candidatos para tus vacantes. Utilizamos métodos como la publicación de ofertas de empleo en bolsas de trabajo y redes sociales, búsqueda en bases de datos de candidatos, networking y referencias. ¿Te gustaría saber más sobre el costo de este servicio? Cliente: Sí, ¿cuánto cuesta este servicio? 
-	Agente IA: El costo de nuestro servicio de búsqueda directa de candidatos varía en función de la complejidad de la vacante y la experiencia del candidato que busca. Sin embargo, podemos ofrecerte un presupuesto personalizado una vez que tengamos más información sobre tus necesidades específicas. ¿Te gustaría agendar una llamada para discutir esto con más detalle? Envíame tu correo, por favor. 
-	Cliente: Claro, mi correo es [correo electrónico]. Estoy disponible mañana a las [Hora]. 
-	Agente IA: Perfecto, [nombre del cliente]. Te enviaré una invitación a tu correo electrónico para confirmar la cita. ¡Gracias por tu interés!
"""

# Translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session if not already initialized
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chat history
for message in st.session_state.chat_session.history:
    print(message)  # Add this line to inspect the structure of message
    if isinstance(message, dict):
        role = message.get("role")  # Access role using dictionary key
        if role:
            with st.chat_message(translate_role_for_streamlit(role)):
                st.markdown(message.get("parts", [])[0].get("text", ""))  # Access text using dictionary keys

# User input
user_prompt = st.chat_input("Escriba un mensaje")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    
    # Send the system instruction along with the user's message if it's the first user message
    if len(st.session_state.chat_session.history) == 0:
        full_prompt = system_instruction + "\nUser: " + user_prompt
    else:
        full_prompt = user_prompt

    # Send user input to Gemini model
    gemini_response = st.session_state.chat_session.send_message(full_prompt)
    
    # Display model response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
    
    # Update chat history
    st.session_state.chat_session.history.append({
        "role": "user",
        "parts": [{"text": user_prompt}]
    })
    st.session_state.chat_session.history.append({
        "role": "model",
        "parts": [{"text": gemini_response.text}]
    })