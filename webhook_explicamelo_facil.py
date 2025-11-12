from flask import Flask, request, jsonify

app = Flask(__name__)

print("🎓 MODO EXPLÍCAMELO FÁCIL - Iniciado")

# Base de conocimiento simple y directa
explicaciones = {
    "concebir": "🧠 **CONCEBIR en CDIO - Explicado Fácil**\n\nEs la fase donde PIENSAS y PLANEAS como ingeniero. Es como cuando quieres construir una casa y primero:\n\n• 🤔 Identificas el problema: ¿Qué necesitan las personas?\n• 📋 Planeas los requisitos: ¿Qué debe hacer el sistema?\n• 🎯 Defines objetivos: ¿Qué quieres lograr?\n• 🔍 Investigas tecnologías: ¿Qué herramientas usar?\n\n💡 **Ejemplo**: Antes de hacer un robot, piensas: '¿Para qué sirve? ¿Qué problemas resuelve?'",

    "diseñar": "📐 **DISEÑAR en CDIO - Explicado Fácil**\n\nEs cuando CREAS LOS PLANOS detallados de tu solución:\n\n• ✏️ Diseñas circuitos y diagramas\n• 💻 Planificas software y algoritmos\n• 📊 Seleccionas componentes electrónicos\n• 🎨 Haces prototipos en papel\n\n🔧 **Diferencia clave**: Concebir = QUÉ hacer, Diseñar = CÓMO hacerlo",

    "proyectos": "🛠️ **Proyectos CDIO - Explicado Fácil**\n\nSon proyectos REALES que haces durante la carrera:\n\n📅 **Semestres 1-3**: Proyectos básicos\n• Ejemplo: 'Semáforo inteligente con Arduino'\n\n📅 **Semestres 4-6**: Proyectos intermedios\n• Ejemplo: 'Sistema de riego automático'\n\n📅 **Semestres 7-10**: Proyectos complejos\n• Ejemplo: 'Robot para hospitales'\n\n✅ **Ventaja**: Aprendes haciendo, no solo memorizando.",

    "sistemas_digitales": "🔢 **Sistemas Digitales - Explicado Fácil**\n\nAprendes a crear sistemas que piensan en CEROS y UNOS:\n\n• 🎛️ Diseñar circuitos lógicos\n• 💾 Programar microcontroladores\n• 🤖 Crear sistemas embebidos\n• 📱 Desarrollar aplicaciones IoT\n\n💼 **Salida laboral**: Desarrollador de hardware, especialista en IoT",

    "telecomunicaciones": "📡 **Telecomunicaciones - Explicado Fácil**\n\nAprendes a hacer que los dispositivos SE COMUNIQUEN:\n\n• 🌐 Diseñar redes de comunicación\n• 📶 Trabajar con WiFi, Bluetooth, 5G\n• 🔒 Garantizar seguridad\n• 📞 Desarrollar sistemas de transmisión\n\n💼 **Salida laboral**: Ingeniero de telecomunicaciones, diseñador de redes",

    "automatizacion": "🏭 **Automatización y Control - Explicado Fácil**\n\nAprendes a crear sistemas que FUNCIONAN SOLOS:\n\n• 🤖 Programar robots industriales\n• ⚙️ Diseñar control automático\n• 🔄 Crear procesos automatizados\n• 📊 Desarrollar sistemas SCADA\n\n💼 **Salida laboral**: Ingeniero de automatización, especialista en robótica",

    "creditos": "📊 **Créditos Académicos - Explicado Fácil**\n\nSon como PUNTOS DE EXPERIENCIA en tu formación:\n\n🎯 **Total carrera**: 160 créditos\n\n📋 **Distribución**:\n• Formación Profesional: 138 créditos\n• Formación General: 6 créditos\n• Formación de Facultad: 10 créditos\n• Formación Personal: 6 créditos\n\n⏰ **En práctica**: 1 crédito ≈ 3 horas semanales",

    "proyecto_grado": "🎓 **Proyecto de Grado - Explicado Fácil**\n\nEs tu EXAMEN FINAL PRÁCTICO:\n\n🚀 **Características**:\n• Aplicas CDIO completo\n• Puede ser con empresa real\n• Usualmente en equipo\n• Resuelve problema real\n\n📝 **Ejemplos**:\n• 'Sistema para cultivos de aguacate'\n• 'Robot para biblioteca'\n• 'App para control de energía'"
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "active", "message": "Modo Explícamelo Fácil funcionando"})

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        print("📨 Datos recibidos")
        
        # Extraer pregunta de diferentes formatos
        pregunta = ""
        
        # Formato DialogFlow
        if "queryResult" in data:
            query_result = data["queryResult"]
            if "queryText" in query_result:
                pregunta = query_result["queryText"]
            elif "parameters" in query_result and "any" in query_result["parameters"]:
                pregunta = query_result["parameters"]["any"]
        
        # Formato directo
        if not pregunta and "question" in data:
            pregunta = data["question"]
        
        pregunta = pregunta.lower().strip() if pregunta else ""
        print(f"🔍 Pregunta: '{pregunta}'")
        
        # Si no hay pregunta, dar bienvenida
        if not pregunta:
            respuesta_texto = (
                "🎓 **Modo Explícamelo Fácil Activado**\n\n"
                "Pídeme que te explique fácilmente conceptos del PEP de Ingeniería Electrónica.\n\n"
                "💡 **Ejemplos**:\n"
                "'Explícame fácil qué es concebir en CDIO'\n"
                "'Explica fácil los proyectos CDIO'\n"
                "'¿Qué son sistemas digitales de forma simple?'"
            )
        else:
            # Buscar tema basado en palabras clave
            if "concebir" in pregunta:
                respuesta_texto = explicaciones["concebir"]
            elif "diseñar" in pregunta:
                respuesta_texto = explicaciones["diseñar"]
            elif "proyecto" in pregunta and "cdio" in pregunta:
                respuesta_texto = explicaciones["proyectos"]
            elif "sistema digital" in pregunta:
                respuesta_texto = explicaciones["sistemas_digitales"]
            elif "telecomunica" in pregunta:
                respuesta_texto = explicaciones["telecomunicaciones"]
            elif "automatiza" in pregunta:
                respuesta_texto = explicaciones["automatizacion"]
            elif "crédito" in pregunta or "credito" in pregunta:
                respuesta_texto = explicaciones["creditos"]
            elif "proyecto grado" in pregunta or "trabajo grado" in pregunta:
                respuesta_texto = explicaciones["proyecto_grado"]
            elif "cdio" in pregunta:
                respuesta_texto = "🔄 **CDIO Completo - Explicado Fácil**\n\nCDIO son 4 fases:\n\n1. 🧠 CONCEBIR: Pensar y planear\n2. 📐 DISEÑAR: Crear planos\n3. 🔨 IMPLEMENTAR: Construir\n4. 🚀 OPERAR: Hacer funcionar\n\n💡 **Es como una receta para ser buen ingeniero: Primero piensas, luego diseñas, después construyes y finalmente haces que funcione.**"
            else:
                respuesta_texto = (
                    "🤔 **Modo Explícamelo Fácil**\n\n"
                    "Puedo explicarte fácilmente sobre:\n\n"
                    "• 🧠 **CDIO y sus fases**: Concebir, Diseñar\n"
                    "• 🛠️ **Proyectos CDIO**: Cómo funcionan\n"
                    "• 🔢 **Líneas de profundización**: Sistemas Digitales, Telecomunicaciones, Automatización\n"
                    "• 📊 **Estructura académica**: Créditos, Proyecto de grado\n\n"
                    "¿Sobre cuál quieres que te explique?"
                )
        
        # Crear respuesta en formato DialogFlow
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
        
        print("✅ Respuesta enviada exitosamente")
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        # Respuesta de error simple
        error_response = {
            "fulfillmentText": "⚠️ Error temporal. Por favor, intenta de nuevo.",
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": ["⚠️ Error temporal. Por favor, intenta de nuevo."]
                    }
                }
            ]
        }
        return jsonify(error_response)

if __name__ == "__main__":
    print("✅ Webhook funcionando en puerto 5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
