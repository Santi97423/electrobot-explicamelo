from flask import Flask, request, jsonify
import random

app = Flask(__name__)

print("🎓 MODO EXPLÍCAMELO FÁCIL - Respuestas mejoradas")

# Base de conocimiento con múltiples respuestas por tema
explicaciones = {
    "concebir": [
        "Te explico la fase CONCEBIR en CDIO de manera sencilla:\n\nImagina que eres un arquitecto que va a construir una casa. Antes de dibujar los planos, primero piensas: ¿Qué necesita la familia? ¿Cuántas habitaciones? ¿Qué estilo prefieren?\n\nEn CDIO, Concebir es exactamente eso: Es la etapa donde defines el QUÉ y el POR QUÉ de tu proyecto. Piensas en el problema, investigas las necesidades y planeas los objetivos antes de empezar a diseñar.\n\nEjemplo práctico: Antes de crear un robot, te preguntas: ¿Para qué servirá? ¿Qué problemas resolverá? ¿Qué características debe tener para ser útil?",
        
        "Hablemos de CONCEBIR en CDIO de forma clara:\n\nConcebir es como soñar despierto con un proyecto. Es el momento creativo donde imaginas posibilidades y defines la visión de lo que quieres crear.\n\nPaso a paso:\n1. Identificas un problema o necesidad\n2. Investigas cómo otros lo han resuelto\n3. Defines qué quieres lograr\n4. Piensas en qué tecnologías podrías usar\n\nEs la base de todo buen proyecto: sin una buena concepción, el diseño puede ir en la dirección equivocada."
    ],
    
    "sistemas_digitales": [
        "Te explico Sistemas Digitales de forma sencilla:\n\nPiensa en los sistemas digitales como el lenguaje secreto de las computadoras. Todo lo que hacen los dispositivos electrónicos se reduce a ceros y unos, como un código morse moderno.\n\nEn esta línea aprenderás a:\n- Diseñar circuitos que toman decisiones\n- Programar microcontroladores como Arduino\n- Crear dispositivos inteligentes para hogares\n- Desarrollar sistemas embebidos para automóviles\n\nEs como aprender a hablar el idioma de las máquinas para que hagan lo que tú quieras.",
        
        "Hablemos de Sistemas Digitales de manera simple:\n\nTodo a nuestro alrededor se está volviendo digital. Tu celular, tu televisor, hasta tu nevera pronto tendrá inteligencia. Los sistemas digitales son la magia detrás de esto.\n\nAprenderás a crear circuitos que procesan información, programas que controlan dispositivos y sistemas que se comunican entre sí. Es una de las áreas con más oportunidades laborales porque cada día aparecen nuevos dispositivos inteligentes."
    ],
    
    "automatizacion": [
        "Te explico Automatización y Control de forma fácil:\n\nImagina una fábrica donde las máquinas trabajan solas, tomando decisiones inteligentes sin necesidad de supervisión constante. Eso es automatización.\n\nEn esta línea aprenderás a:\n- Programar robots que ensamblan productos\n- Diseñar sistemas que controlan procesos industriales\n- Crear algoritmos que optimizan el consumo de energía\n- Desarrollar sistemas de supervisión para plantas completas\n\nEs como darle cerebro a las máquinas para que trabajen de manera inteligente y eficiente.",
        
        "Hablemos de Automatización de forma clara:\n\nLa automatización es hacer que las cosas funcionen solas. Como cuando programas tu cafetera para que prepare café a las 7 AM sin que tú estés presente.\n\nEn ingeniería electrónica, esto significa crear sistemas que:\n- Monitorean variables como temperatura y presión\n- Toman decisiones basadas en esos datos\n- Actúan automáticamente para mantener condiciones ideales\n- Aprenden y se adaptan con el tiempo\n\nEs una de las áreas más emocionantes porque combina electrónica, programación e inteligencia artificial."
    ],
    
    "proyectos_cdio": [
        "Te explico los Proyectos CDIO de manera simple:\n\nEn lugar de aprender teoría aburrida en exámenes, en Ingeniería Electrónica aprendes haciendo proyectos reales. Es como aprender a nadar metiéndote a la piscina.\n\nAsí funciona:\nPrimeros semestres: Proyectos pequeños como un semáforo inteligente\nSemestres intermedios: Sistemas más complejos como riego automático\nÚltimos semestres: Proyectos grandes con aplicaciones reales\n\nLa ventaja es que cuando te gradúes, ya tendrás experiencia resolviendo problemas reales, no solo conocimientos teóricos.",
        
        "Hablemos de los Proyectos CDIO de forma sencilla:\n\nCada semestre trabajas en un proyecto que integra todo lo aprendido. Es como subir niveles en un videojuego:\n\nNivel 1-3: Aprendes las bases con proyectos guiados\nNivel 4-6: Desarrollas proyectos más independientes\nNivel 7-10: Trabajas en proyectos complejos con clientes reales\n\nEsta metodología te prepara mejor para el mundo laboral porque simula cómo se trabaja en la industria real."
    ],
    
    "telecomunicaciones": [
        "Te explico Telecomunicaciones de forma fácil:\n\nPiensa en las telecomunicaciones como el sistema nervioso del mundo moderno. Son las venas y arterias que permiten que la información viaje de un lugar a otro.\n\nEn esta línea aprenderás a:\n- Diseñar redes de comunicación eficientes\n- Trabajar con tecnologías como WiFi, Bluetooth y 5G\n- Garantizar que la información viaje segura\n- Desarrollar sistemas de transmisión de datos\n\nEs una especialidad con enorme futuro porque cada día dependemos más de estar conectados.",
        
        "Hablemos de Telecomunicaciones de manera clara:\n\nCuando envías un mensaje por WhatsApp, haces una videollamada o ves Netflix, estás usando telecomunicaciones. Es la magia que hace posible la comunicación a distancia.\n\nComo ingeniero en telecomunicaciones podrás:\n- Diseñar redes para empresas y ciudades\n- Desarrollar sistemas de comunicación seguros\n- Trabajar en compañías de internet y telefonía\n- Crear tecnologías para el internet del futuro\n\nEs un campo en constante evolución con muchas oportunidades."
    ],
    
    "creditos": [
        "Te explico los Créditos académicos de forma sencilla:\n\nLos créditos son como puntos de experiencia que ganas en tu formación. Cada materia te da ciertos créditos según su complejidad y carga de trabajo.\n\nEn Ingeniería Electrónica:\nTotal necesarios: 160 créditos\nDistribución:\n- 138 créditos en tu especialidad técnica\n- 6 créditos en formación general\n- 10 créditos en base ingenieril\n- 6 créditos en desarrollo personal\n\nEn práctica, 1 crédito representa aproximadamente 3 horas de trabajo semanal entre clase y estudio independiente.",
        
        "Hablemos del sistema de Créditos de manera simple:\n\nImagina que los créditos son como monedas en un videojuego. Necesitas 160 monedas para graduarte, y las ganas aprobando materias.\n\nCada tipo de materia te da diferentes monedas:\n- Materias técnicas: la mayoría de tus monedas\n- Materias generales: te dan visión amplia\n- Materias de facultad: base de ingeniería\n- Materias personales: desarrollo humano\n\nEs un sistema diseñado para que tengas una formación equilibrada."
    ],
    
    "proyecto_grado": [
        "Te explico el Proyecto de Grado de forma clara:\n\nEs tu examen final práctico donde demuestras todo lo aprendido en la carrera. Es como el jefe final de un videojuego donde aplicas todas tus habilidades.\n\nCaracterísticas principales:\n- Aplicas el método CDIO completo\n- Puede ser con una empresa real\n- Generalmente trabajas en equipo\n- Resuelves un problema del mundo real\n\nEjemplos de proyectos recientes:\n- Sistema de monitoreo para cultivos de aguacate\n- Robot para asistencia en bibliotecas\n- Aplicación para control de energía en hogares",
        
        "Hablemos del Proyecto de Grado de manera sencilla:\n\nEs tu oportunidad de demostrar que eres un ingeniero completo. Durante 1 o 2 semestres desarrollas un proyecto que integra todo lo aprendido.\n\nAsí funciona:\n1. Escoges un problema que te apasione\n2. Diseñas una solución innovadora\n3. La construyes y pruebas\n4. Demuestras que funciona\n\nEs la transición perfecta entre ser estudiante y convertirte en profesional, porque trabajas como lo harías en una empresa real."
    ]
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "active", 
        "message": "Modo Explícamelo Fácil con respuestas mejoradas",
        "temas_disponibles": list(explicaciones.keys())
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("📨 Datos recibidos de DialogFlow")
        
        # Detectar qué intent se activó
        intent_name = ""
        if "queryResult" in data and "intent" in data["queryResult"]:
            intent_name = data["queryResult"]["intent"]["displayName"]
        
        print(f"🔍 Intent detectado: {intent_name}")
        
        # Mapear intents a temas
        intent_to_topic = {
            "facil_concebir": "concebir",
            "facil_sistemas_digitales": "sistemas_digitales", 
            "facil_automatizacion": "automatizacion",
            "facil_proyectos_cdio": "proyectos_cdio",
            "facil_telecomunicaciones": "telecomunicaciones",
            "facil_creditos": "creditos",
            "facil_proyecto_grado": "proyecto_grado"
        }
        
        # Obtener respuesta aleatoria para el tema
        if intent_name in intent_to_topic:
            tema = intent_to_topic[intent_name]
            respuestas = explicaciones[tema]
            respuesta_texto = random.choice(respuestas)
            print(f"✅ Tema: {tema}, Respuesta seleccionada")
        else:
            # Intent no reconocido
            respuesta_texto = "Hola! Soy tu asistente para explicaciones fáciles. Puedo ayudarte a entender conceptos de Ingeniería Electrónica de forma simple y clara. ¿Sobre qué tema quieres que te explique?"
        
        response = {
            "fulfillmentText": respuesta_texto,
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [respuesta_texto]
                    }
                }
            ]
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        error_msg = "En este momento estoy teniendo dificultades técnicas. Por favor, intenta de nuevo en un momento."
        return jsonify({
            "fulfillmentText": error_msg,
            "fulfillmentMessages": [{"text": {"text": [error_msg]}}]
        })

if __name__ == "__main__":
    print("✅ Webhook mejorado - Listo en puerto 5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
