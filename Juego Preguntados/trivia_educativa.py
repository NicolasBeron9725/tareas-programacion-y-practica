# trivia_preguntados_pro.py
"""
Preguntados Técnico Pro
- Modo individual: 2-4 jugadores
- Modo equipos: 2 equipos (A y B) con 1-3 jugadores/ equipo
- Turnos: cada jugador/equipo gira la ruleta en su turno
  - Si acierta, sigue jugando
  - Si falla, pasa el turno
- Insignia por categoría: se obtiene al alcanzar 3 aciertos en esa categoría
- Gana quien consiga las 4 insignias (IA, Ciberseguridad, Programación, Redes)

Añadir preguntas:
- Crea un archivo trivia_educativa.py en el mismo directorio que defina:
    PREGUNTAS_INCRUSTADAS = [ { ... }, { ... }, ... ]
  (o usamos el botón "Cargar preguntas (JSON)" para importar un .json)
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ttkbootstrap import Window
import random, math
from collections import defaultdict

# ----------------------------- Configuración -----------------------------
CATEGORIAS = ["IA", "Ciberseguridad", "Programación", "Redes"]
EMOJIS = {"IA": "🧠", "Ciberseguridad": "🔒", "Programación": "💻", "Redes": "🌐"}
COLORES = {"IA": "#F6E05E", "Ciberseguridad": "#9AE6B4", "Programación": "#BFDBFE", "Redes": "#FBCFE8"}

# Preguntas de prueba
PREGUNTAS_INCRUSTADAS = [
  {
    "categoria": "IA",
    "dificultad": "fácil",
    "pregunta": "¿Qué es la inteligencia artificial?",
    "opciones": ["Una red social", "Un tipo de hardware", "Tecnología que simula el pensamiento humano", "Un lenguaje de programación"],
    "respuesta": "Tecnología que simula el pensamiento humano",
    "explicacion": "La IA permite que las máquinas realicen tareas que normalmente requieren inteligencia humana, como razonar, aprender o tomar decisiones."
  },
  {
    "categoria": "IA",
    "dificultad": "fácil",
    "pregunta": "¿Qué significa IA?",
    "opciones": ["Inteligencia Avanzada", "Inteligencia Artificial", "Interfaz Adaptativa", "Integración Automática"],
    "respuesta": "Inteligencia Artificial",
    "explicacion": "IA es la abreviatura de Inteligencia Artificial, una rama de la informática que busca simular procesos cognitivos humanos."
  },
  {
    "categoria": "IA",
    "dificultad": "fácil",
    "pregunta": "¿Cuál es un ejemplo de IA en uso cotidiano?",
    "opciones": ["Calculadora", "Semáforo", "Asistente virtual", "Reloj digital"],
    "respuesta": "Asistente virtual",
    "explicacion": "Los asistentes virtuales como Siri o Alexa utilizan IA para entender y responder preguntas humanas."
  },
  {
    "categoria": "IA",
    "dificultad": "fácil",
    "pregunta": "¿Qué tipo de datos usa el aprendizaje supervisado?",
    "opciones": ["Datos sin etiquetas", "Datos aleatorios", "Datos etiquetados", "Datos comprimidos"],
    "respuesta": "Datos etiquetados",
    "explicacion": "El aprendizaje supervisado se basa en ejemplos con etiquetas para que el modelo aprenda a predecir resultados."
  },
  {
    "categoria": "IA",
    "dificultad": "fácil",
    "pregunta": "¿Qué campo está más relacionado con IA?",
    "opciones": ["Biología", "Física", "Informática", "Geografía"],
    "respuesta": "Informática",
    "explicacion": "La IA es una subdisciplina de la informática que combina algoritmos, datos y modelos matemáticos."
  },
  {
    "categoria": "IA",
    "dificultad": "fácil",
    "pregunta": "¿Qué es un chatbot?",
    "opciones": ["Un virus", "Un robot físico", "Un programa que conversa", "Un tipo de red"],
    "respuesta": "Un programa que conversa",
    "explicacion": "Un chatbot es un sistema de IA diseñado para simular conversaciones con humanos."
  },
  {
    "categoria": "IA",
    "dificultad": "fácil",
    "pregunta": "¿Qué algoritmo se usa para clasificación?",
    "opciones": ["K-means", "Regresión lineal", "Árbol de decisión", "PCA"],
    "respuesta": "Árbol de decisión",
    "explicacion": "Los árboles de decisión son modelos que dividen los datos en ramas para clasificar o predecir resultados."
  },
  {
    "categoria": "IA",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es el aprendizaje no supervisado?",
    "opciones": ["Aprendizaje con etiquetas", "Agrupación sin etiquetas", "Entrenamiento supervisado", "Optimización de redes"],
    "respuesta": "Agrupación sin etiquetas",
    "explicacion": "El aprendizaje no supervisado busca patrones en datos sin etiquetas, como en el clustering."
  },
  {
    "categoria": "IA",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es una red neuronal?",
    "opciones": ["Un sistema de cables", "Un modelo estadístico", "Una estructura inspirada en el cerebro", "Una base de datos"],
    "respuesta": "Una estructura inspirada en el cerebro",
    "explicacion": "Las redes neuronales imitan el funcionamiento del cerebro para procesar información y aprender."
  },
  {
    "categoria": "IA",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es el sobreajuste?",
    "opciones": ["Un error de hardware", "Un modelo que generaliza bien", "Un modelo que memoriza los datos", "Una técnica de limpieza"],
    "respuesta": "Un modelo que memoriza los datos",
    "explicacion": "El sobreajuste ocurre cuando un modelo aprende demasiado los datos de entrenamiento y falla en nuevos casos."
  },
  {
    "categoria": "IA",
    "dificultad": "intermedia",
    "pregunta": "¿Qué técnica se usa para reducir dimensiones?",
    "opciones": ["SVM", "PCA", "KNN", "CNN"],
    "respuesta": "PCA",
    "explicacion": "El Análisis de Componentes Principales (PCA) reduce la cantidad de variables manteniendo la información esencial."
  },
  {
    "categoria": "IA",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es el aprendizaje profundo?",
    "opciones": ["Un tipo de clustering", "Una red neuronal con muchas capas", "Un algoritmo de regresión", "Un método de limpieza"],
    "respuesta": "Una red neuronal con muchas capas",
    "explicacion": "El aprendizaje profundo utiliza redes neuronales con múltiples capas para aprender representaciones complejas."
  },
  {
    "categoria": "IA",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es un perceptrón?",
    "opciones": ["Un tipo de sensor", "Una unidad de red neuronal", "Un algoritmo genético", "Un tipo de red social"],
    "respuesta": "Una unidad de red neuronal",
    "explicacion": "El perceptrón es la unidad básica de una red neuronal, que realiza cálculos simples para tomar decisiones."
  },
  {
    "categoria": "IA",
    "dificultad": "intermedia",
    "pregunta": "¿Qué mide la función de pérdida?",
    "opciones": ["La velocidad del modelo", "La precisión del hardware", "El error del modelo", "La cantidad de datos"],
    "respuesta": "El error del modelo",
    "explicacion": "La función de pérdida indica qué tan lejos está el modelo de la respuesta correcta durante el entrenamiento."
  },

  {
    "categoria": "IA",
    "dificultad": "difícil",
    "pregunta": "¿Qué es una red convolucional?",
    "opciones": ["Una red para texto", "Una red para imágenes", "Una red para audio", "Una red para clustering"],
    "respuesta": "Una red para imágenes",
    "explicacion": "Las redes convolucionales son ideales para procesar imágenes, detectando patrones como bordes y formas."
  },
  {
    "categoria": "IA",
    "dificultad": "difícil",
    "pregunta": "¿Qué es el gradiente descendente?",
    "opciones": ["Un tipo de activación", "Un método de optimización", "Una técnica de clustering", "Una función de pérdida"],
    "respuesta": "Un método de optimización",
    "explicacion": "El gradiente descendente ajusta los parámetros del modelo para minimizar el error en cada iteración."
  },
  {
    "categoria": "IA",
    "dificultad": "difícil",
    "pregunta": "¿Qué es el dropout?",
    "opciones": ["Una técnica de regularización", "Un tipo de red", "Un error de entrenamiento", "Una función de activación"],
    "respuesta": "Una técnica de regularización",
    "explicacion": "Dropout apaga aleatoriamente neuronas durante el entrenamiento para evitar el sobreajuste."
  },
  {
    "categoria": "IA",
    "dificultad": "difícil",
    "pregunta": "¿Qué es una función de activación?",
    "opciones": ["Una función que transforma la salida de una neurona", "Una función que mide el error", "Una función que agrupa datos", "Una función que reduce dimensiones"],
    "respuesta": "Una función que transforma la salida de una neurona",
    "explicacion": "Las funciones de activación permiten que las redes neuronales aprendan relaciones no lineales."
  },
  {
    "categoria": "IA",
    "dificultad": "difícil",
    "pregunta": "¿Qué es una red recurrente?",
    "opciones": ["Una red que procesa imágenes", "Una red que tiene ciclos", "Una red que reduce datos", "Una red que clasifica texto"],
    "respuesta": "Una red que tiene ciclos",
    "explicacion": "Las redes recurrentes tienen conexiones que permiten recordar información anterior, útiles para secuencias."
  },
  {
    "categoria": "IA",
  "dificultad": "difícil",
  "pregunta": "¿Qué es el backpropagation?",
  "opciones": ["Un algoritmo de clustering", "Un método de entrenamiento", "Una técnica de limpieza", "Un tipo de red"],
  "respuesta": "Un método de entrenamiento",
  "explicacion": "El backpropagation ajusta los pesos de una red neuronal calculando el error y propagándolo hacia atrás para mejorar el aprendizaje."
  },
  {
        "categoria": "IA",
        "dificultad": "difícil",
        "pregunta": "¿Qué es el aprendizaje por refuerzo?",
        "opciones": ["Aprendizaje con recompensas", "Aprendizaje sin etiquetas", "Aprendizaje supervisado", "Aprendizaje profundo"],
        "respuesta": "Aprendizaje con recompensas",
        "explicacion": "El aprendizaje por refuerzo implica que un agente aprende a tomar decisiones mediante recompensas y castigos."
  },
  {
    "categoria": "Redes",
    "dificultad": "fácil",
    "pregunta": "¿Qué es una red informática?",
    "opciones": ["Un grupo de computadoras conectadas", "Un tipo de software", "Un lenguaje de programación", "Un sistema operativo"],
    "respuesta": "Un grupo de computadoras conectadas",
    "explicacion": "Una red informática permite que varios dispositivos se comuniquen y compartan recursos entre sí."
  },
  {
    "categoria": "Redes",
    "dificultad": "fácil",
    "pregunta": "¿Qué significa Wi-Fi?",
    "opciones": ["Wireless Fidelity", "Wide Frequency", "Web Interface", "Windows File"],
    "respuesta": "Wireless Fidelity",
    "explicacion": "Wi-Fi es una tecnología que permite la conexión inalámbrica de dispositivos a internet."
  },
  {
    "categoria": "Redes",
    "dificultad": "fácil",
    "pregunta": "¿Qué dispositivo se usa para conectar redes diferentes?",
    "opciones": ["Switch", "Router", "Monitor", "Teclado"],
    "respuesta": "Router",
    "explicacion": "El router dirige el tráfico entre diferentes redes, como la red local y la red de internet."
  },
  {
    "categoria": "Redes",
    "dificultad": "fácil",
    "pregunta": "¿Qué es una dirección IP?",
    "opciones": ["Un número de teléfono", "Una dirección física", "Un identificador único para un dispositivo en la red", "Un tipo de cable"],
    "respuesta": "Un identificador único para un dispositivo en la red",
    "explicacion": "La dirección IP identifica a cada dispositivo en una red para que pueda comunicarse con otros."
  },
  {
    "categoria": "Redes",
    "dificultad": "fácil",
    "pregunta": "¿Qué es un switch?",
    "opciones": ["Un tipo de software", "Un dispositivo que conecta computadoras en red", "Un sistema operativo", "Un protocolo de seguridad"],
    "respuesta": "Un dispositivo que conecta computadoras en red",
    "explicacion": "El switch permite que varios dispositivos se comuniquen dentro de una red local."
  },
  {
    "categoria": "Redes",
    "dificultad": "fácil",
    "pregunta": "¿Qué es el cable Ethernet?",
    "opciones": ["Un cable para audio", "Un cable para energía", "Un cable para conectar dispositivos en red", "Un cable USB"],
    "respuesta": "Un cable para conectar dispositivos en red",
    "explicacion": "El cable Ethernet se usa para conectar computadoras y otros dispositivos a una red local."
  },
  {
    "categoria": "Redes",
    "dificultad": "fácil",
    "pregunta": "¿Qué es el protocolo HTTP?",
    "opciones": ["Un lenguaje de programación", "Un sistema operativo", "Un protocolo para transferir páginas web", "Un tipo de cable"],
    "respuesta": "Un protocolo para transferir páginas web",
    "explicacion": "HTTP permite la comunicación entre navegadores y servidores web para mostrar páginas."
  },
  {
    "categoria": "Redes",
    "dificultad": "intermedia",
    "pregunta": "¿Qué diferencia hay entre IPv4 e IPv6?",
    "opciones": ["Velocidad", "Seguridad", "Cantidad de direcciones disponibles", "Tipo de cable usado"],
    "respuesta": "Cantidad de direcciones disponibles",
    "explicacion": "IPv6 ofrece muchas más direcciones IP que IPv4, lo que permite conectar más dispositivos."
  },
  {
    "categoria": "Redes",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es una red LAN?",
    "opciones": ["Red de área amplia", "Red local", "Red inalámbrica", "Red de internet"],
    "respuesta": "Red local",
    "explicacion": "Una LAN conecta dispositivos en un área pequeña, como una casa o una oficina."
  },
  {
    "categoria": "Redes",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es una red WAN?",
    "opciones": ["Red de área local", "Red de área amplia", "Red inalámbrica", "Red de oficina"],
    "respuesta": "Red de área amplia",
    "explicacion": "Una WAN conecta redes que están geográficamente separadas, como sucursales de una empresa."
  },
  {
    "categoria": "Redes",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es el protocolo TCP/IP?",
    "opciones": ["Un lenguaje de programación", "Un sistema operativo", "Un conjunto de reglas para comunicación en red", "Un tipo de cable"],
    "respuesta": "Un conjunto de reglas para comunicación en red",
    "explicacion": "TCP/IP define cómo se transmiten los datos entre dispositivos en internet y redes locales."
  },
  {
    "categoria": "Redes",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es una máscara de subred?",
    "opciones": ["Un tipo de cable", "Una herramienta de seguridad", "Un número que divide la red y los hosts", "Un sistema operativo"],
    "respuesta": "Un número que divide la red y los hosts",
    "explicacion": "La máscara de subred determina qué parte de la dirección IP corresponde a la red y cuál al dispositivo."
  },
  {
    "categoria": "Redes",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es NAT?",
    "opciones": ["Un tipo de virus", "Un protocolo de seguridad", "Una técnica para traducir direcciones IP", "Un sistema operativo"],
    "respuesta": "Una técnica para traducir direcciones IP",
    "explicacion": "NAT permite que varios dispositivos compartan una sola dirección IP pública para acceder a internet."
  },
  {
    "categoria": "Redes",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es un servidor DNS?",
    "opciones": ["Un sistema de seguridad", "Un servidor que traduce nombres de dominio en IPs", "Un tipo de cable", "Un sistema operativo"],
    "respuesta": "Un servidor que traduce nombres de dominio en IPs",
    "explicacion": "El DNS convierte direcciones como www.ejemplo.com en direcciones IP que las computadoras pueden entender."
  },
  {
    "categoria": "Redes",
    "dificultad": "difícil",
    "pregunta": "¿Qué es el protocolo FTP?",
    "opciones": ["Un sistema de seguridad", "Un protocolo para transferir archivos", "Un lenguaje de programación", "Un tipo de cable"],
    "respuesta": "Un protocolo para transferir archivos",
    "explicacion": "FTP se usa para subir y descargar archivos entre computadoras en una red."
  },
  {
    "categoria": "Redes",
    "dificultad": "difícil",
    "pregunta": "¿Qué es una red peer-to-peer?",
    "opciones": ["Una red con servidor central", "Una red donde todos los dispositivos son iguales", "Una red inalámbrica", "Una red de área amplia"],
    "respuesta": "Una red donde todos los dispositivos son iguales",
    "explicacion": "En una red P2P, los dispositivos comparten recursos directamente sin un servidor central."
  },
  {
    "categoria": "Redes",
    "dificultad": "difícil",
    "pregunta": "¿Qué es el protocolo HTTPS?",
    "opciones": ["Un protocolo inseguro", "Una versión segura de HTTP", "Un tipo de cable", "Un sistema operativo"],
    "respuesta": "Una versión segura de HTTP",
    "explicacion": "HTTPS cifra la comunicación entre el navegador y el servidor para proteger los datos del usuario."
  },
  {
    "categoria": "Redes",
    "dificultad": "difícil",
    "pregunta": "¿Qué es el modelo OSI?",
    "opciones": ["Un sistema operativo", "Un protocolo de seguridad", "Un marco de referencia para redes", "Un lenguaje de programación"],
    "respuesta": "Un marco de referencia para redes",
    "explicacion": "El modelo OSI divide la comunicación en 7 capas para entender cómo viajan los datos en una red."
  },
  {
    "categoria": "Redes",
    "dificultad": "difícil",
    "pregunta": "¿Qué es el protocolo DHCP?",
    "opciones": ["Un sistema de seguridad", "Un protocolo que asigna direcciones IP automáticamente", "Un tipo de cable", "Un lenguaje de programación"],
    "respuesta": "Un protocolo que asigna direcciones IP automáticamente",
    "explicacion": "DHCP facilita la configuración de redes al asignar direcciones IP sin intervención manual."
  },
  {
  "categoria": "Redes",
  "dificultad": "difícil",
  "pregunta": "¿Qué es una dirección MAC?",
  "opciones": ["Una dirección postal", "Una dirección física única de un dispositivo de red", "Una contraseña de red", "Un tipo de protocolo"],
  "respuesta": "Una dirección física única de un dispositivo de red",
  "explicacion": "La dirección MAC identifica de forma única a cada dispositivo en una red local, y está asociada a su tarjeta de red."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "fácil",
    "pregunta": "¿Qué es un antivirus?",
    "opciones": ["Un tipo de virus", "Un programa que protege contra malware", "Un sistema operativo", "Una red privada"],
    "respuesta": "Un programa que protege contra malware",
    "explicacion": "El antivirus detecta y elimina software malicioso que puede dañar tu computadora o robar información."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "fácil",
    "pregunta": "¿Qué significa 'phishing'?",
    "opciones": ["Pescar en internet", "Robo de identidad mediante engaños", "Ataque físico a servidores", "Acceso remoto legal"],
    "respuesta": "Robo de identidad mediante engaños",
    "explicacion": "El phishing es una técnica que engaña al usuario para que revele información confidencial como contraseñas o datos bancarios."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "fácil",
    "pregunta": "¿Qué es una contraseña segura?",
    "opciones": ["123456", "Tu nombre", "Una combinación de letras, números y símbolos", "Solo letras"],
    "respuesta": "Una combinación de letras, números y símbolos",
    "explicacion": "Una contraseña segura es difícil de adivinar y protege mejor tus cuentas frente a ataques."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "fácil",
    "pregunta": "¿Qué es un firewall?",
    "opciones": ["Un virus", "Una red social", "Una barrera de seguridad entre redes", "Un tipo de cable"],
    "respuesta": "Una barrera de seguridad entre redes",
    "explicacion": "El firewall controla el tráfico entre redes y bloquea accesos no autorizados."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "fácil",
    "pregunta": "¿Qué es el malware?",
    "opciones": ["Software malicioso", "Un tipo de hardware", "Un sistema operativo", "Un lenguaje de programación"],
    "respuesta": "Software malicioso",
    "explicacion": "El malware incluye virus, troyanos y otros programas diseñados para dañar o robar información."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "fácil",
    "pregunta": "¿Qué es el spam?",
    "opciones": ["Correo no deseado", "Un tipo de virus", "Un sistema de seguridad", "Un protocolo de red"],
    "respuesta": "Correo no deseado",
    "explicacion": "El spam son mensajes no solicitados que suelen tener fines publicitarios o maliciosos."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "fácil",
    "pregunta": "¿Qué es una VPN?",
    "opciones": ["Una red pública", "Una red privada virtual", "Un tipo de virus", "Un sistema operativo"],
    "respuesta": "Una red privada virtual",
    "explicacion": "Una VPN cifra tu conexión y te permite navegar de forma segura y privada."
  },

  {
    "categoria": "Ciberseguridad",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es la autenticación de dos factores?",
    "opciones": ["Un tipo de contraseña", "Un método de verificación con dos pasos", "Un sistema operativo", "Un ataque de red"],
    "respuesta": "Un método de verificación con dos pasos",
    "explicacion": "Este método requiere dos pruebas de identidad, como contraseña y código enviado al celular."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es un ataque DDoS?",
    "opciones": ["Un ataque físico", "Un ataque de denegación de servicio distribuido", "Un error de software", "Un tipo de firewall"],
    "respuesta": "Un ataque de denegación de servicio distribuido",
    "explicacion": "Un DDoS satura un servidor con tráfico falso para que deje de funcionar correctamente."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es el ransomware?",
    "opciones": ["Un tipo de antivirus", "Un malware que secuestra datos", "Un sistema de respaldo", "Un protocolo de red"],
    "respuesta": "Un malware que secuestra datos",
    "explicacion": "El ransomware bloquea tus archivos y exige un pago para liberarlos."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es la ingeniería social?",
    "opciones": ["Un tipo de software", "Manipulación para obtener información", "Un sistema de redes", "Un lenguaje de programación"],
    "respuesta": "Manipulación para obtener información",
    "explicacion": "La ingeniería social explota la confianza humana para obtener datos confidenciales."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es el hashing?",
    "opciones": ["Un tipo de cifrado reversible", "Una técnica para ocultar datos", "Una función que transforma datos en valores únicos", "Un protocolo de red"],
    "respuesta": "Una función que transforma datos en valores únicos",
    "explicacion": "El hashing convierte datos en cadenas únicas que no pueden revertirse fácilmente."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es una brecha de seguridad?",
    "opciones": ["Un error de hardware", "Una falla que permite acceso no autorizado", "Un tipo de firewall", "Una red privada"],
    "respuesta": "Una falla que permite acceso no autorizado",
    "explicacion": "Una brecha de seguridad ocurre cuando alguien accede a sistemas o datos sin permiso."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es el cifrado?",
    "opciones": ["Un tipo de virus", "Un método para proteger datos", "Un sistema operativo", "Un lenguaje de programación"],
    "respuesta": "Un método para proteger datos",
    "explicacion": "El cifrado convierte la información en un formato ilegible para protegerla de accesos no autorizados."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "difícil",
    "pregunta": "¿Qué es el protocolo TLS?",
    "opciones": ["Un sistema de archivos", "Un protocolo de seguridad para comunicaciones", "Un tipo de malware", "Un lenguaje de programación"],
    "respuesta": "Un protocolo de seguridad para comunicaciones",
    "explicacion": "TLS cifra los datos transmitidos por internet, protegiendo la privacidad y autenticidad."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "difícil",
    "pregunta": "¿Qué es una firma digital?",
    "opciones": ["Una imagen escaneada", "Un método de autenticación criptográfica", "Un tipo de virus", "Un sistema operativo"],
    "respuesta": "Un método de autenticación criptográfica",
    "explicacion": "La firma digital verifica la identidad del remitente y garantiza que el mensaje no fue alterado."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "difícil",
    "pregunta": "¿Qué es el pentesting?",
    "opciones": ["Un tipo de cifrado", "Una prueba de penetración de seguridad", "Un protocolo de red", "Un sistema de respaldo"],
    "respuesta": "Una prueba de penetración de seguridad",
    "explicacion": "El pentesting simula ataques para detectar vulnerabilidades antes de que sean explotadas."
  },
  {
    "categoria": "Ciberseguridad",
    "dificultad": "difícil",
    "pregunta": "¿Qué es el principio de mínimo privilegio?",
    "opciones": ["Dar acceso total a todos", "Limitar el acceso solo a lo necesario", "Eliminar usuarios inactivos", "Usar contraseñas cortas"],
    "respuesta": "Limitar el acceso solo a lo necesario",
    "explicacion": "Este principio reduce riesgos al otorgar solo los permisos estrictamente necesarios a cada usuario."
  },
  {
  "categoria": "Ciberseguridad",
  "dificultad": "difícil",
  "pregunta": "¿Qué es el protocolo SSH?",
  "opciones": ["Un sistema de respaldo", "Un protocolo seguro para acceso remoto", "Un tipo de firewall", "Un lenguaje de programación"],
  "respuesta": "Un protocolo seguro para acceso remoto",
  "explicacion": "SSH permite conectarse de forma segura a otro dispositivo a través de una red, cifrando la comunicación."
 },
 {
  "categoria": "Ciberseguridad",
  "dificultad": "difícil",
  "pregunta": "¿Qué es OWASP?",
  "opciones": ["Un lenguaje de programación", "Una organización que promueve seguridad web", "Un tipo de malware", "Un sistema operativo"],
  "respuesta": "Una organización que promueve seguridad web",
  "explicacion": "OWASP publica recursos y buenas prácticas para proteger aplicaciones web contra vulnerabilidades comunes."
 },
 {
  "categoria": "Programación",
  "dificultad": "fácil",
  "pregunta": "¿Qué es un lenguaje de programación?",
  "opciones": ["Un idioma humano", "Una herramienta para diseñar ropa", "Un conjunto de instrucciones para computadoras", "Una red social"],
  "respuesta": "Un conjunto de instrucciones para computadoras",
    "explicacion": "Los lenguajes de programación permiten escribir instrucciones que una computadora puede entender y ejecutar."
  },
  {
    "categoria": "Programación",
    "dificultad": "fácil",
    "pregunta": "¿Cuál de estos es un lenguaje de programación?",
    "opciones": ["Python", "Excel", "Chrome", "Windows"],
    "respuesta": "Python",
    "explicacion": "Python es un lenguaje de programación popular por su simplicidad y versatilidad."
  },
  {
    "categoria": "Programación",
    "dificultad": "fácil",
    "pregunta": "¿Qué significa 'variable' en programación?",
    "opciones": ["Una constante", "Un tipo de error", "Un espacio para almacenar datos", "Un archivo de texto"],
    "respuesta": "Un espacio para almacenar datos",
    "explicacion": "Una variable guarda información que puede cambiar durante la ejecución del programa."
  },
  {
    "categoria": "Programación",
    "dificultad": "fácil",
    "pregunta": "¿Qué símbolo se usa para asignar valores en Python?",
    "opciones": ["==", ":", "=", "+"],
    "respuesta": "=",
    "explicacion": "El símbolo '=' se usa para asignar un valor a una variable en Python."
  },
  {
    "categoria": "Programación",
    "dificultad": "fácil",
    "pregunta": "¿Qué es un bucle?",
    "opciones": ["Un error de código", "Una estructura que repite acciones", "Una función matemática", "Un tipo de archivo"],
    "respuesta": "Una estructura que repite acciones",
    "explicacion": "Los bucles permiten ejecutar una parte del código varias veces, como 'for' o 'while'."
  },
  {
    "categoria": "Programación",
    "dificultad": "fácil",
    "pregunta": "¿Qué es un comentario en código?",
    "opciones": ["Una instrucción ejecutable", "Una nota que no se ejecuta", "Un error", "Una variable especial"],
    "respuesta": "Una nota que no se ejecuta",
    "explicacion": "Los comentarios explican el código y se ignoran durante la ejecución."
  },
  {
    "categoria": "Programación",
    "dificultad": "fácil",
    "pregunta": "¿Qué hace la función 'print()' en Python?",
    "opciones": ["Guarda datos", "Calcula operaciones", "Muestra información en pantalla", "Cierra el programa"],
    "respuesta": "Muestra información en pantalla",
    "explicacion": "La función 'print()' se usa para mostrar texto o resultados en la consola."
  },

  {
    "categoria": "Programación",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es una función en programación?",
    "opciones": ["Una variable especial", "Un error común", "Un bloque de código reutilizable", "Un tipo de archivo"],
    "respuesta": "Un bloque de código reutilizable",
    "explicacion": "Las funciones agrupan instrucciones que se pueden ejecutar varias veces con diferentes datos."
  },
  {
    "categoria": "Programación",
    "dificultad": "intermedia",
    "pregunta": "¿Qué significa 'debuggear'?",
    "opciones": ["Escribir código", "Eliminar errores", "Crear variables", "Diseñar interfaces"],
    "respuesta": "Eliminar errores",
    "explicacion": "Debuggear es el proceso de encontrar y corregir errores en el código."
  },
  {
    "categoria": "Programación",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es un condicional?",
    "opciones": ["Un tipo de bucle", "Una estructura que toma decisiones", "Una función matemática", "Un error de sintaxis"],
    "respuesta": "Una estructura que toma decisiones",
    "explicacion": "Los condicionales permiten ejecutar diferentes acciones según se cumpla una condición."
  },
  {
    "categoria": "Programación",
    "dificultad": "intermedia",
    "pregunta": "¿Qué significa 'return' en una función?",
    "opciones": ["Salir del programa", "Mostrar un mensaje", "Devolver un valor", "Crear una variable"],
    "respuesta": "Devolver un valor",
    "explicacion": "La instrucción 'return' permite que una función devuelva un resultado al ser llamada."
  },
  {
    "categoria": "Programación",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es un tipo de dato?",
    "opciones": ["Un error", "Una función", "Una categoría de valores", "Una variable especial"],
    "respuesta": "Una categoría de valores",
    "explicacion": "Los tipos de datos definen qué tipo de información puede almacenar una variable, como números o texto."
  },
  {
    "categoria": "Programación",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es una lista en Python?",
    "opciones": ["Un número", "Una cadena de texto", "Una colección ordenada de elementos", "Un archivo externo"],
    "respuesta": "Una colección ordenada de elementos",
    "explicacion": "Las listas permiten guardar múltiples valores en una sola variable, accesibles por índice."
  },
  {
    "categoria": "Programación",
    "dificultad": "intermedia",
    "pregunta": "¿Qué es un IDE?",
    "opciones": ["Un tipo de virus", "Un entorno de desarrollo", "Una función matemática", "Un sistema operativo"],
    "respuesta": "Un entorno de desarrollo",
    "explicacion": "Un IDE es una herramienta que facilita escribir, probar y depurar código, como VS Code o PyCharm."
  },
  {
    "categoria": "Programación",
    "dificultad": "difícil",
    "pregunta": "¿Qué es la recursividad?",
    "opciones": ["Un tipo de bucle", "Una función que se llama a sí misma", "Un error de compilación", "Una estructura condicional"],
    "respuesta": "Una función que se llama a sí misma",
    "explicacion": "La recursividad permite resolver problemas dividiéndolos en subproblemas similares."
  },
  {
    "categoria": "Programación",
    "dificultad": "difícil",
    "pregunta": "¿Qué es la programación orientada a objetos?",
    "opciones": ["Un estilo visual", "Una técnica para redes", "Un paradigma basado en clases y objetos", "Un lenguaje específico"],
    "respuesta": "Un paradigma basado en clases y objetos",
    "explicacion": "Este paradigma organiza el código en objetos que combinan datos y funciones relacionadas."
  },
  {
    "categoria": "Programación",
    "dificultad": "difícil",
    "pregunta": "¿Qué es una clase en programación?",
    "opciones": ["Una función especial", "Una estructura de control", "Un molde para crear objetos", "Un tipo de archivo"],
    "respuesta": "Un molde para crear objetos",
    "explicacion": "Una clase define las propiedades y comportamientos que tendrán los objetos creados a partir de ella."
  },
  {
    "categoria": "Programación",
    "dificultad": "difícil",
    "pregunta": "¿Qué es una excepción?",
    "opciones": ["Un tipo de bucle", "Un error controlado", "Una variable especial", "Un archivo externo"],
    "respuesta": "Un error controlado",
    "explicacion": "Las excepciones permiten manejar errores sin que el programa se detenga abruptamente."
  },
  {
    "categoria": "Programación",
    "dificultad": "difícil",
    "pregunta": "¿Qué significa 'herencia' en POO?",
    "opciones": ["Copiar código", "Compartir atributos entre clases", "Eliminar funciones", "Crear variables globales"],
    "respuesta": "Compartir atributos entre clases",
    "explicacion": "La herencia permite que una clase hija reutilice atributos y métodos de una clase padre."
  },
  {
  "categoria": "Programación",
  "dificultad": "difícil",
  "pregunta": "¿Qué significa 'herencia' en POO?",
  "opciones": ["Copiar código", "Compartir atributos entre clases", "Eliminar funciones", "Crear variables globales"],
  "respuesta": "Compartir atributos entre clases",
  "explicacion": "La herencia permite que una clase hija reutilice atributos y métodos definidos en una clase padre, promoviendo la reutilización de código."
 },
 {
  "categoria": "Programación",
  "dificultad": "difícil",
  "pregunta": "¿Qué es un decorador en Python?",
  "opciones": ["Un tipo de bucle", "Una función que modifica otra función", "Una variable especial", "Un archivo de configuración"],
  "respuesta": "Una función que modifica otra función",
  "explicacion": "Los decoradores permiten añadir funcionalidad a funciones existentes sin modificar su código original, usando el símbolo '@'."
 }
]

# ----------------------------- Helper trigonométrico -----------------------------
def math_cos(deg): return math.cos(math.radians(deg))
def math_sin(deg): return math.sin(math.radians(deg))
def question_prefix(cat): return f"{EMOJIS.get(cat,'?')}  Categoría: {cat}"

# ----------------------------- Aplicación -----------------------------
class TriviaEducativa(Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Preguntados Técnico Pro")
        self.state("zoomed")

        # Estado de juego
        self.modo = tk.StringVar(value="individual")  # "individual" o "equipos"
        self.jugadores_vars = []
        self.jugadores = []
        self.equipos = {"A": [], "B": []}
        self.team_member_idx = {"A": 0, "B": 0}
        self.turno_index = 0
        self.preguntas_por_cat = defaultdict(lambda: defaultdict(list))
        self.categoria_seleccionada = None
        self.pregunta_actual = None
        self.aciertos = {}
        self.insignias = {}
        self.tiempo_restante = 20

        self.cargar_preguntas_por_categoria()
        self.mostrar_pantalla_configuracion()

    # -------------------- Carga de preguntas --------------------
    def cargar_preguntas_por_categoria(self):
        self.preguntas_por_cat.clear()
        for p in PREGUNTAS_INCRUSTADAS:
            cat = p.get("categoria")
            dif = p.get("dificultad","fácil")
            if cat in CATEGORIAS:
                self.preguntas_por_cat[cat][dif].append(p)
        for cat in CATEGORIAS:
            for dif in self.preguntas_por_cat[cat]:
                random.shuffle(self.preguntas_por_cat[cat][dif])

    # -------------------- Configuración de jugadores --------------------
    def mostrar_pantalla_configuracion(self):
        for w in self.winfo_children(): w.destroy()
        header = ttk.Label(self, text="Preguntados Técnico Pro", font=("Helvetica",28))
        header.pack(pady=12)

        modo_frame = ttk.LabelFrame(self, text="Modo de juego")
        modo_frame.pack(pady=10, fill="x", padx=20)
        ttk.Radiobutton(modo_frame, text="Individual (2 a 4 jugadores)", variable=self.modo, value="individual").pack(anchor="w", padx=10, pady=3)
        ttk.Radiobutton(modo_frame, text="Por equipos (2 equipos, 1 a 3 jugadores por equipo)", variable=self.modo, value="equipos").pack(anchor="w", padx=10, pady=3)

        self.nombres_frame = ttk.LabelFrame(self, text="Jugadores / Equipos")
        self.nombres_frame.pack(pady=10, fill="x", padx=20)
        self.actualizar_campos_nombres()
        self.modo.trace_add("write", lambda *_: self.actualizar_campos_nombres())

        ttk.Button(self, text="Iniciar partida", command=self.iniciar_partida).pack(pady=14)

    def actualizar_campos_nombres(self):
        for w in self.nombres_frame.winfo_children(): w.destroy()
        self.jugadores_vars.clear()
        if self.modo.get() == "individual":
            ttk.Label(self.nombres_frame, text="Ingrese entre 2 y 4 jugadores:").pack(anchor="w", padx=8, pady=4)
            for i in range(4):
                var = tk.StringVar()
                row = ttk.Frame(self.nombres_frame); row.pack(fill="x", padx=8, pady=2)
                ttk.Label(row, text=f"Jugador {i+1}: ").pack(side="left")
                ttk.Entry(row, textvariable=var, width=30).pack(side="left")
                self.jugadores_vars.append(var)
        else:
            ttk.Label(self.nombres_frame, text="Equipo A (1 a 3 jugadores):").pack(anchor="w", padx=8, pady=2)
            for i in range(3):
                var = tk.StringVar()
                row = ttk.Frame(self.nombres_frame); row.pack(fill="x", padx=8, pady=2)
                ttk.Label(row, text=f"A - Jugador {i+1}: ").pack(side="left")
                ttk.Entry(row, textvariable=var, width=30).pack(side="left")
                self.jugadores_vars.append(("A",var))
            ttk.Separator(self.nombres_frame).pack(fill="x", pady=6)
            ttk.Label(self.nombres_frame, text="Equipo B (1 a 3 jugadores):").pack(anchor="w", padx=8, pady=2)
            for i in range(3):
                var = tk.StringVar()
                row = ttk.Frame(self.nombres_frame); row.pack(fill="x", padx=8, pady=2)
                ttk.Label(row, text=f"B - Jugador {i+1}: ").pack(side="left")
                ttk.Entry(row, textvariable=var, width=30).pack(side="left")
                self.jugadores_vars.append(("B",var))

    # -------------------- Iniciar partida --------------------
    def iniciar_partida(self):
        if self.modo.get() == "individual":
            nombres = [v.get().strip() for v in self.jugadores_vars if v.get().strip()]
            if not (2<=len(nombres)<=4):
                messagebox.showwarning("Jugadores insuficientes","Ingresá entre 2 y 4 jugadores.")
                return
            self.jugadores = nombres
            self.aciertos = {n: {"correctas":0,"incorrectas":0} for n in self.jugadores}
            self.insignias = {n: set() for n in self.jugadores}
        else:
            equipoA, equipoB = [], []
            for tag,var in self.jugadores_vars:
                name = var.get().strip()
                if name:
                    if tag=="A": equipoA.append(name)
                    else: equipoB.append(name)
            if not (1<=len(equipoA)<=3) or not (1<=len(equipoB)<=3):
                messagebox.showwarning("Jugadores por equipo inválidos","Cada equipo debe tener entre 1 y 3 jugadores.")
                return
            self.equipos = {"A":equipoA,"B":equipoB}
            self.aciertos = {"A":{"correctas":0,"incorrectas":0},"B":{"correctas":0,"incorrectas":0}}
            self.insignias = {"A":set(),"B":set()}
        self.turno_index = 0
        self.team_member_idx = {"A":0,"B":0}
        self.categoria_seleccionada = None
        self.pregunta_actual = None
        self.mostrar_pantalla_juego()

    # -------------------- Pantalla de juego --------------------
    def mostrar_pantalla_juego(self):
        for w in self.winfo_children(): w.destroy()
        top_frame = ttk.Frame(self)
        top_frame.pack(pady=10, fill="x")

        # Ruleta a la izquierda
        self.ruleta_canvas = tk.Canvas(top_frame, width=400, height=400, bg="#212529", highlightthickness=0)
        self.ruleta_canvas.pack(side="left", padx=10)
        self.dibujar_ruleta()

        # Pregunta y opciones a la derecha
        derecha_frame = ttk.Frame(top_frame)
        derecha_frame.pack(side="left", padx=20, fill="both", expand=True)

        self.turno_label = ttk.Label(derecha_frame, text=self.obtener_texto_turno(), font=("Helvetica",16,"bold"))
        self.turno_label.pack(pady=6)

        self.lbl_ruleta = ttk.Label(derecha_frame, text="Girá la ruleta para obtener categoría", font=("Helvetica",12))
        self.lbl_ruleta.pack(pady=4)

        self.btn_girar = ttk.Button(derecha_frame, text="🎡 Girar ruleta", command=self.iniciar_giro)
        self.btn_girar.pack(pady=4)

        self.tiempo_label = ttk.Label(derecha_frame, text="Tiempo: 20s", font=("Helvetica",14))
        self.tiempo_label.pack(pady=4)

        self.pregunta_frame = ttk.LabelFrame(derecha_frame, text="Pregunta")
        self.pregunta_frame.pack(fill="x", pady=10)

        self.pregunta_text = ttk.Label(self.pregunta_frame, text="Girá la ruleta para comenzar", font=("Helvetica",14), wraplength=600)
        self.pregunta_text.pack(pady=10)

        self.opcion_buttons = []
        opciones_frame = ttk.Frame(self.pregunta_frame)
        opciones_frame.pack(pady=6)
        for i in range(4):
            b = ttk.Button(opciones_frame, text=f"Opción {i+1}", command=lambda t=i: self.responder_opcion_por_indice(t))
            b.grid(row=i//2, column=i%2, padx=8, pady=4, sticky="ew")
            self.opcion_buttons.append(b)

        self.explicacion_label = ttk.Label(self.pregunta_frame, text="", font=("Helvetica",12), wraplength=600, foreground="#FFD700")
        self.explicacion_label.pack(pady=6)

        # Tablero de jugadores abajo
        self.tablero_frame = ttk.LabelFrame(self, text="Tablero de jugadores / Insignias")
        self.tablero_frame.pack(fill="x", padx=20, pady=10)
        self.actualizar_panel_insignias()

    # -------------------- Ruleta --------------------
    def dibujar_ruleta(self):
        c = self.ruleta_canvas
        c.delete("all")
        w, h = int(c["width"]), int(c["height"])
        cx, cy = w//2, h//2
        radio = min(w,h)//2 - 20
        ang = 90
        ang_span = 360 / len(CATEGORIAS)
        for cat in CATEGORIAS:
            color = COLORES.get(cat,"#ccc")
            c.create_arc(cx-radio, cy-radio, cx+radio, cy+radio, start=ang, extent=ang_span, fill=color, outline="white", width=2, tags=("sector", cat))
            mid = ang + ang_span/2
            rad_mid = radio*0.65
            x = cx + rad_mid * math_cos(mid)
            y = cy - rad_mid * math_sin(mid)
            c.create_text(x, y, text=EMOJIS[cat], font=("Arial",28))
            ang += ang_span
        # Flecha superior
        c.create_polygon(cx-18, cy-radio-10, cx+18, cy-radio-10, cx, cy-radio+20, fill="#ef4444", outline="white")
        # Centro con ?
        c.create_oval(cx-60, cy-60, cx+60, cy+60, fill="#fff", outline="#333", tags="centro")
        c.create_text(cx, cy, text="?", font=("Arial",32), tags="centro_text")

    def iniciar_giro(self):
        self.btn_girar.config(state="disabled")
        secuencia = random.choices(CATEGORIAS, k=28)
        def animar(i=0):
            if i < len(secuencia):
                cat = secuencia[i]
                self.ruleta_canvas.itemconfig("centro_text", text=EMOJIS[cat])
                self.after(60 + i*8, lambda: animar(i+1))
            else:
                cat_final = secuencia[-1]
                self.categoria_seleccionada = cat_final
                self.lbl_ruleta.config(text=f"Categoría: {cat_final} {EMOJIS[cat_final]}")
                self.mostrar_pregunta_de_categoria(cat_final)
        animar()

    # -------------------- Mostrar pregunta --------------------
    def mostrar_pregunta_de_categoria(self, categoria):
        difs = list(self.preguntas_por_cat[categoria].keys())
        if not difs:
            messagebox.showwarning("Sin preguntas", f"No hay preguntas en {categoria}")
            self.btn_girar.config(state="normal")
            return
        dif = random.choice(difs)
        lista = self.preguntas_por_cat[categoria][dif]
        if not lista:
            messagebox.showwarning("Sin preguntas", f"No hay preguntas en {categoria} - {dif}")
            self.btn_girar.config(state="normal")
            return
        self.pregunta_actual = lista.pop()
        pregunta_text = self.pregunta_actual.get("pregunta","")
        opciones = list(self.pregunta_actual.get("opciones",[]))
        random.shuffle(opciones)

        self.pregunta_text.config(text=question_prefix(categoria)+"\n\n"+pregunta_text)
        for i,b in enumerate(self.opcion_buttons):
            if i < len(opciones):
                b.config(text=opciones[i], state="normal")
            else:
                b.config(text="", state="disabled")
        self.explicacion_label.config(text="")
        self.tiempo_restante = 20
        self.actualizar_tiempo()

    # -------------------- Temporizador --------------------
    def actualizar_tiempo(self):
        self.tiempo_label.config(text=f"Tiempo: {self.tiempo_restante}s")
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.after(1000, self.actualizar_tiempo)
        else:
            correcta = self.pregunta_actual.get("respuesta")
            self.explicacion_label.config(text=f"Tiempo agotado. Respuesta correcta: {correcta}")
            for b in self.opcion_buttons: b.config(state="disabled")
            self.avanzar_turno_por_fallo()
            self.turno_label.config(text=self.obtener_texto_turno())
            self.btn_girar.config(state="normal")

    # -------------------- Responder --------------------
    def responder_opcion_por_indice(self, idx):
        seleccion = self.opcion_buttons[idx].cget("text")
        correcta = seleccion == self.pregunta_actual.get("respuesta")
        jugador_actual = self.obtener_actor_actual()
        if correcta:
            self.explicacion_label.config(text=f"✅ Correcto!\n{self.pregunta_actual.get('explicacion','')}")
            self.aciertos[jugador_actual]["correctas"] += 1
        else:
            self.explicacion_label.config(text=f"❌ Incorrecto.\nRespuesta correcta: {self.pregunta_actual.get('respuesta')}")
            self.aciertos[jugador_actual]["incorrectas"] += 1
        for b in self.opcion_buttons: b.config(state="disabled")
        self.actualizar_panel_insignias()
        self.avanzar_turno_por_fallo()
        self.turno_label.config(text=self.obtener_texto_turno())
        self.btn_girar.config(state="normal")

    # -------------------- Turnos --------------------
    def obtener_actor_actual(self):
        if self.modo.get()=="individual":
            return self.jugadores[self.turno_index % len(self.jugadores)]
        else:
            equipo = "A" if self.turno_index%2==0 else "B"
            return equipo

    def avanzar_turno_por_fallo(self):
        self.turno_index += 1

    # -------------------- Tablero de jugadores --------------------
    def actualizar_panel_insignias(self):
        for w in self.tablero_frame.winfo_children(): w.destroy()
        if self.modo.get()=="individual":
            for n in self.jugadores:
                frame = ttk.Frame(self.tablero_frame, relief="ridge", padding=6)
                frame.pack(fill="x", pady=4, padx=4)
                ttk.Label(frame, text=f"🧑 {n}", font=("Helvetica",12,"bold")).pack(anchor="w")
                ttk.Label(frame, text=f"✅ Correctas: {self.aciertos[n]['correctas']}").pack(anchor="w")
                ttk.Label(frame, text=f"❌ Incorrectas: {self.aciertos[n]['incorrectas']}").pack(anchor="w")
                ttk.Label(frame, text="Insignias: " + " ".join(self.insignias[n]) if self.insignias[n] else "Insignias: -").pack(anchor="w")
        else:
            for equipo in ["A","B"]:
                frame = ttk.Frame(self.tablero_frame, relief="ridge", padding=6)
                frame.pack(fill="x", pady=4, padx=4)
                ttk.Label(frame, text=f"Equipo {equipo}: " + ", ".join(self.equipos[equipo]), font=("Helvetica",12,"bold")).pack(anchor="w")
                ttk.Label(frame, text=f"✅ Correctas: {self.aciertos[equipo]['correctas']}").pack(anchor="w")
                ttk.Label(frame, text=f"❌ Incorrectas: {self.aciertos[equipo]['incorrectas']}").pack(anchor="w")
                ttk.Label(frame, text="Insignias: " + " ".join(self.insignias[equipo]) if self.insignias[equipo] else "Insignias: -").pack(anchor="w")

    def obtener_texto_turno(self):
        if self.modo.get()=="individual":
            return f"Turno: {self.jugadores[self.turno_index % len(self.jugadores)]}"
        else:
            equipo = "A" if self.turno_index%2==0 else "B"
            return f"Turno: Equipo {equipo} ({', '.join(self.equipos[equipo])})"

# -------------------- Ejecutar --------------------
if __name__=="__main__":
    app = TriviaEducativa()
    app.mainloop()