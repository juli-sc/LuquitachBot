import streamlit as st#importamos la libreria
from groq import Groq #? Nueva Importacion

st.set_page_config(page_title="luquitach bot", page_icon="🎆") #Le damos un titulo a la pestaña de la pagina

#titulo de la pagina
st.title("Luquitach bot V.1")

#ingreso de datos
nombre = st.text_input("¿Cual es tu nombre?")

#crear un boton con funcionalidad
if st.button("SALUDAR") : 
    st.write(f"¡Hola,{nombre}! ¿que onda?")

MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#Nos conecta a la API, crear usuario
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] #obteniendo clave de nuestro arcivo
    return Groq(api_key = clave_secreta) #crea al usuario

#cliente = usuario de groq | modelo es la IA seleccionada | el mensaje del usuario
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content" : mensajeDeEntrada}],
        stream = True

    )

def inicializar_estado(): # simula el historial de mensajes
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #memoria de mensajes

def actualizar_historial(rol, contenido, avatar):
    #el metodo append() agrega un elemento a la lista
    st.session_state.mensajes.append(
        {"role":rol, "content": contenido, "avatar": avatar}

    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes :
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) :
            st.markdown(mensaje["content"])

#contenedor del chat
def area_chat():
    contenedorDelChat = st.container(height= 400, border= True)
    #agrupamos los mensajes en el area del chat 
    with contenedorDelChat : mostrar_historial()



#? creando funcion con diseño de la pagina
def configurar_pagina():
    st.title("Luquitach")
    st.sidebar.title("Configuracion")
    seleccion = st.sidebar.selectbox(
        "Elegi modelo", #titulo
        MODELO, #tiene que estar en una lista
        index=0

    )
    return seleccion #deculeve un dato

def generar_respuesta(chat_completo):
    respuesta_completa = "" #texto vacio
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main() : #Funcion principal

 #invocacion de funciones
 modelo = configurar_pagina() #llamamos la funcion
 #st.write(f"el usuario eligio el modelo {modelo}")
 clienteUsuario = crear_usuario_groq()
 inicializar_estado()#llama a la uncion historial
 area_chat() #creamos el sector para ver los mensaje
 mensaje = st.chat_input("Escribi tu mensaje...")  
 
 
 if mensaje:
     actualizar_historial("user", mensaje, "😎") #visualizamos el mensaje del usuario
     chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
     if chat_completo:
         with st.chat_message("assistant") :
             respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
             actualizar_historial("assistant", respuesta_completa, "👺")
             st.rerun()
#indicamos que nuestra funcion pricipal es main()
if __name__ == "__main__":
    main()
