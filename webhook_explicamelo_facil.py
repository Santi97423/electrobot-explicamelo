from flask import Flask, request, jsonify
import re

app = Flask(__name__)

print("🎓 MODO EXPLÍCAMELO FÁCIL - Activado (PEP 2016-2025)")

# ==================== BASE DE CONOCIMIENTO ESPECIALIZADA ====================
explicaciones_faciles = {
    "concebir_cdio": {
        "preguntas": ["qué es concebir en cdio", "fase concebir", "concebir cdio"],
        "respuesta": "🧠 **CONCEBIR en CDIO - Explicado Fácil**\n\nEs la fase donde **piensas y planeas** como ingeniero. Es como cuando quieres construir una casa y primero:\n\n• 🤔 **Identificas el problema**: ¿Qué necesitan las personas?\n• 📋 **Planeas los requisitos**: ¿Qué debe hacer el sistema?\n• 🎯 **Defines objetivos**: ¿Qué quieres lograr?\n• 🔍 **Investigas tecnologías**: ¿Qué herramientas usar?\n\n**Ejemplo real**: Antes de hacer un robot, piensas: '¿Para qué sirve? ¿Qué problemas resuelve? ¿Qué características debe tener?'"
    },
    
    "diseñar_cdio": {
        "preguntas": ["qué es diseñar en cdio", "fase diseñar", "diseñar cdio"],
        "respuesta": "📐 **DISEÑAR en CDIO - Explicado Fácil**\n\nEs cuando **creas los planos detallados** de tu solución. Como un arquitecto que dibuja cada detalle de la casa:\n\n• ✏️ **Diseñas circuitos**: Diagramas y esquemas\n• 💻 **Planificas software**: Flujos y algoritmos\n• 📊 **Seleccionas componentes**: Qué resistencias, chips usar\n• 🎨 **Prototipas en papel**: Bocetos y modelos\n\n**Diferencia clave**: Concebir = QUÉ hacer, Diseñar = CÓMO hacerlo"
    },
    
    "proyectos_cdio": {
        "preguntas": ["proyectos cdio", "cómo son los proyectos cdio", "ejemplos proyectos cdio"],
        "respuesta": "🛠️ **Proyectos CDIO - Explicado Fácil**\n\nSon proyectos **reales y progresivos** que haces durante la carrera:\n\n**Semestres 1-3**: Proyectos básicos\n• Ejemplo: 'Semáforo inteligente con Arduino'\n\n**Semestres 4-6**: Proyectos intermedios  \n• Ejemplo: 'Sistema de riego automático con sensores'\n\n**Semestres 7-10**: Proyectos complejos\n• Ejemplo: 'Robot de telepresencia para hospitales'\n\n**Ventaja**: Aprendes haciendo, no solo memorizando teoría."
    },
    
    "sistemas_digitales": {
        "preguntas": ["sistemas digitales", "línea sistemas digitales", "qué son sistemas digitales"],
        "respuesta": "🔢 **Sistemas Digitales - Explicado Fácil**\n\nEs la línea donde aprendes a **crear sistemas que piensan en 0s y 1s**. Como enseñarle a las máquinas a tomar decisiones.\n\n**Qué aprenderás**:\n• 🎛️ Diseñar circuitos lógicos\n• 💾 Programar microcontroladores\n• 🤖 Crear sistemas embebidos\n• 📱 Desarrollar aplicaciones IoT\n\n**Salida laboral**: Desarrollador de hardware, diseñador de sistemas embebidos, especialista en IoT"
    },
    
    "telecomunicaciones": {
        "preguntas": ["telecomunicaciones", "línea telecomunicaciones", "qué son telecomunicaciones"],
        "respuesta": "📡 **Telecomunicaciones - Explicado Fácil**\n\nEs la línea donde aprendes a **hacer que los dispositivos se comuniquen**. Como crear 'redes sociales' para máquinas.\n\n**Qué aprenderás**:\n• 🌐 Diseñar redes de comunicación\n• 📶 Trabajar con WiFi, Bluetooth, 5G\n• 🔒 Garantizar seguridad en comunicaciones\n• 📞 Desarrollar sistemas de transmisión\n\n**Salida laboral**: Ingeniero de telecomunicaciones, diseñador de redes, especialista en comunicaciones móviles"
    },
    
    "automatizacion_control": {
        "preguntas": ["automatización y control", "línea automatización", "qué es automatización"],
        "respuesta": "🏭 **Automatización y Control - Explicado Fácil**\n\nEs la línea donde aprendes a **crear sistemas que funcionan solos**. Como darle 'cerebro' a las máquinas para que tomen decisiones automáticas.\n\n**Qué aprenderás**:\n• 🤖 Programar robots y brazos mecánicos\n• ⚙️ Diseñar sistemas de control industrial\n• 🔄 Crear procesos automatizados\n• 📊 Desarrollar sistemas SCADA\n\n**Salida laboral**: Ingeniero de automatización, especialista en control industrial, diseñador de sistemas robóticos"
    },
    
    "creditos": {
        "preguntas": ["créditos", "cuántos créditos", "qué son créditos académicos"],
        "respuesta": "📊 **Sistema de Créditos - Explicado Fácil**\n\nLos créditos son como **'puntos de experiencia'** que ganas en tu formación:\n\n**Total carrera**: 160 créditos\n\n**Distribución**:\n• 🎯 Formación Profesional: 138 créditos (tu especialidad)\n• 🌟 Formación General: 6 créditos (visión amplia)\n• 💼 Formación de Facultad: 10 créditos (base ingenieril)\n• 👤 Formación Personal: 6 créditos (desarrollo humano)\n\n**En práctica**: 1 crédito ≈ 3 horas de trabajo semanal"
    },
    
    "proyecto_grado": {
        "preguntas": ["proyecto de grado", "trabajo de grado", "qué es proyecto grado"],
        "respuesta": "🎓 **Proyecto de Grado - Explicado Fácil**\n\nEs tu **'examen final práctico'** donde demuestras todo lo aprendido. Como el jefe final de un videojuego.\n\n**Características**:\n• 🚀 Aplicas CDIO completo\n• 💼 Puede ser con empresa real\n• 👥 Usualmente en equipo\n• 📈 Resuelve problema real\n\n**Ejemplos recientes**:\n• 'Sistema de monitoreo para cultivos de aguacate'\n• 'Robot para asistencia en biblioteca'\n• 'App para control de energía en hogares'"
    }
}

def detectar_tema_explicacion(pregunta):
    """Detecta qué tema de explicación fácil se solicita"""
    pregunta = pregunta.lower().strip()
    
    # Buscar en todas las explicaciones
    for tema_id, contenido in explicaciones_faciles.items():
        for keyword in contenido["preguntas"]:
            if keyword in pregunta:
                return tema_id
    
    # Búsqueda por palabras clave
    keywords_secundarios = {
        "concebir_cdio": ["concebir", "pensar", "planear"],
        "diseñar_cdio": ["diseñar", "planos", "esquema"],
        "proyectos_cdio": ["proyecto cdio", "proyecto integrador"],
        "sistemas_digitales": ["digital", "microcontrolador", "embebido"],
        "telecomunicaciones": ["telecom", "comunicación", "redes"],
        "automatizacion_control": ["automatización", "control", "robot"],
        "creditos": ["crédito", "créditos", "puntos"],
        "proyecto_grado": ["proyecto grado", "trabajo grado"]
    }
    
    for tema_id, palabras in keywords_secundarios.items():
        for palabra in palabras:
            if palabra in pregunta:
                return tema_id
    
    return None

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "🎓 Modo Explícamelo Fácil - PEP 2016-2025",
        "status": "active",
        "temas_disponibles": list(explicaciones_faciles.keys())
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Obtener datos de DialogFlow
        data = request.get_json()
        print("📨 Datos recibidos de DialogFlow")
        
        # Extraer pregunta
        pregunta = ""
        
        if "queryResult" in data:
            query_result = data["queryResult"]
            if "queryText" in query_result:
                pregunta = query_result["queryText"]
            elif "parameters" in query_result and "any" in query_result["parameters"]:
                pregunta = query_result["parameters"]["any"]
        
        # Si no se encuentra en formato DialogFlow, buscar formato directo
        if not pregunta:
            pregunta = data.get("question", "")
        
        pregunta = pregunta.strip()
        print(f"🔍 Pregunta a procesar: '{pregunta}'")
        
        if not pregunta:
            # Respuesta de bienvenida al modo
            response = {
                "fulfillmentText": "🎓 **Modo Explícamelo Fácil Activado**\n\nPídeme que te explique fácilmente cualquier concepto del PEP de Ingeniería Electrónica.\n\nEjemplo: 'Explícame fácil qué es concebir en CDIO'",
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                "🎓 **Modo Explícamelo Fácil Activado**\n\nPídeme que te explique fácilmente cualquier concepto del PEP de Ingeniería Electrónica.\n\nEjemplo: 'Explícame fácil qué es concebir en CDIO'"
                            ]
                        }
                    }
                ]
            }
            return jsonify(response)
        
        # Detectar si es solicitud de explicación fácil
        es_modo_facil = any(palabra in pregunta.lower() for palabra in ["explica", "explicame", "facil", "fácil", "simple"])
        
        if es_modo_facil:
            tema_id = detectar_tema_explicacion(pregunta)
            
            if tema_id:
                explicacion = explicaciones_faciles[tema_id]["respuesta"]
                print(f"✅ Tema detectado: {tema_id}")
                
                response = {
                    "fulfillmentText": explicacion,
                    "fulfillmentMessages": [
                        {
                            "text": {
                                "text": [explicacion]
                            }
                        }
                    ]
                }
            else:
                # No se detectó tema específico
                mensaje = (
                    "🤔 **Modo Explícamelo Fácil**\n\n"
                    "Puedo explicarte fácilmente sobre:\n\n"
                    "• 🧠 **Fases CDIO**: Concebir, Diseñar\n"
                    "• 🛠️ **Proyectos CDIO**: Cómo funcionan\n"
                    "• 🔢 **Líneas de profundización**: Sistemas Digitales, Telecomunicaciones, Automatización\n"
                    "• 📊 **Estructura académica**: Créditos, Proyecto de grado\n\n"
                    "¿Sobre cuál quieres que te explique de forma fácil?"
                )
                
                response = {
                    "fulfillmentText": mensaje,
                    "fulfillmentMessages": [
                        {
                            "text": {
                                "text": [mensaje]
                            }
                        }
                    ]
                }
        else:
            # No es modo fácil, dar instrucciones
            mensaje = (
                "💡 **Para usar el Modo Explícamelo Fácil**:\n\n"
                "Usa frases como:\n"
                "• 'Explícame fácil qué es CDIO'\n"
                "• 'Explica fácil las líneas de profundización'\n"
                "• '¿Qué es concebir en CDIO de forma simple?'"
            )
            
            response = {
                "fulfillmentText": mensaje,
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [mensaje]
                        }
                    }
                ]
            }
        
        print("✅ Respuesta enviada a DialogFlow")
        return jsonify(response)
            
    except Exception as e:
        print(f"❌ Error en webhook: {e}")
        error_response = {
            "fulfillmentText": "⚠️ Lo siento, hubo un error en el modo Explícamelo Fácil. Intenta de nuevo en un momento.",
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": ["⚠️ Lo siento, hubo un error en el modo Explícamelo Fácil. Intenta de nuevo en un momento."]
                    }
                }
            ]
        }
        return jsonify(error_response)

if __name__ == "__main__":
    print("✅ Modo Explícamelo Fácil - Listo en puerto 5000")
    print("🎓 Especializado en PEP Ingeniería Electrónica")
    app.run(host="0.0.0.0", port=5000, debug=False)
