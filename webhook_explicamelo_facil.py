from flask import Flask, request, jsonify
import re
import random

app = Flask(__name__)

print("🎓 MODO EXPLÍCAMELO FÁCIL - Activado (PEP 2016-2025)")

# ==================== BASE DE CONOCIMIENTO ESPECIALIZADA ====================
explicaciones_faciles = {
    # --- CONCEPTOS CDIO AVANZADOS ---
    "concebir_cdio": {
        "preguntas": ["qué es concebir en cdio", "fase concebir", "concebir cdio"],
        "respuesta": "🧠 **CONCEBIR en CDIO - Explicado Fácil**\n\nEs la fase donde **piensas y planeas** como ingeniero. Es como cuando quieres construir una casa y primero:\n\n• 🤔 **Identificas el problema**: ¿Qué necesitan las personas?\n• 📋 **Planeas los requisitos**: ¿Qué debe hacer el sistema?\n• 🎯 **Defines objetivos**: ¿Qué quieres lograr?\n• 🔍 **Investigas tecnologías**: ¿Qué herramientas usar?\n\n**Ejemplo real**: Antes de hacer un robot, piensas: '¿Para qué sirve? ¿Qué problemas resuelve? ¿Qué características debe tener?'",
        "ejemplo_practico": "🔧 **En la carrera**: En tu primer proyecto, antes de diseñar circuitos, defines QUÉ debe hacer tu sistema y PARA QUIÉN."
    },
    
    "diseñar_cdio": {
        "preguntas": ["qué es diseñar en cdio", "fase diseñar", "diseñar cdio"],
        "respuesta": "📐 **DISEÑAR en CDIO - Explicado Fácil**\n\nEs cuando **creas los planos detallados** de tu solución. Como un arquitecto que dibuja cada detalle de la casa:\n\n• ✏️ **Diseñas circuitos**: Diagramas y esquemas\n• 💻 **Planificas software**: Flujos y algoritmos\n• 📊 **Seleccionas componentes**: Qué resistencias, chips usar\n• 🎨 **Prototipas en papel**: Bocetos y modelos\n\n**Diferencia clave**: Concebir = QUÉ hacer, Diseñar = CÓMO hacerlo",
        "ejemplo_practico": "🔧 **En un proyecto**: Diseñas el circuito del robot, eliges los sensores, planificas cómo se comunicarán las partes."
    },
    
    "proyectos_cdio": {
        "preguntas": ["proyectos cdio", "cómo son los proyectos cdio", "ejemplos proyectos cdio"],
        "respuesta": "🛠️ **Proyectos CDIO - Explicado Fácil**\n\nSon proyectos **reales y progresivos** que haces durante la carrera:\n\n**Semestres 1-3**: Proyectos básicos\n• Ejemplo: 'Semáforo inteligente con Arduino'\n\n**Semestres 4-6**: Proyectos intermedios  \n• Ejemplo: 'Sistema de riego automático con sensores'\n\n**Semestres 7-10**: Proyectos complejos\n• Ejemplo: 'Robot de telepresencia para hospitales'\n\n**Ventaja**: Aprendes haciendo, no solo memorizando teoría.",
        "progresion": "De simple → complejo, individual → en equipo"
    },
    
    # --- LÍNEAS DE PROFUNDIZACIÓN ---
    "sistemas_digitales": {
        "preguntas": ["sistemas digitales", "línea sistemas digitales", "qué son sistemas digitales"],
        "respuesta": "🔢 **Sistemas Digitales - Explicado Fácil**\n\nEs la línea donde aprendes a **crear sistemas que piensan en 0s y 1s**. Como enseñarle a las máquinas a tomar decisiones.\n\n**Qué aprenderás**:\n• 🎛️ Diseñar circuitos lógicos\n• 💾 Programar microcontroladores\n• 🤖 Crear sistemas embebidos\n• 📱 Desarrollar aplicaciones IoT\n\n**Salida laboral**: Desarrollador de hardware, diseñador de sistemas embebidos, especialista en IoT",
        "ejemplos_vida_real": ["Sistemas de seguridad", "Dispositivos médicos", "Control industrial", "Electrodomésticos inteligentes"]
    },
    
    "telecomunicaciones": {
        "preguntas": ["telecomunicaciones", "línea telecomunicaciones", "qué son telecomunicaciones"],
        "respuesta": "📡 **Telecomunicaciones - Explicado Fácil**\n\nEs la línea donde aprendes a **hacer que los dispositivos se comuniquen**. Como crear 'redes sociales' para máquinas.\n\n**Qué aprenderás**:\n• 🌐 Diseñar redes de comunicación\n• 📶 Trabajar con WiFi, Bluetooth, 5G\n• 🔒 Garantizar seguridad en comunicaciones\n• 📞 Desarrollar sistemas de transmisión\n\n**Salida laboral**: Ingeniero de telecomunicaciones, diseñador de redes, especialista en comunicaciones móviles",
        "ejemplos_vida_real": ["Redes celulares", "Sistemas de internet", "Comunicaciones satelitales", "Redes empresariales"]
    },
    
    "automatizacion_control": {
        "preguntas": ["automatización y control", "línea automatización", "qué es automatización"],
        "respuesta": "🏭 **Automatización y Control - Explicado Fácil**\n\nEs la línea donde aprendes a **crear sistemas que funcionan solos**. Como darle 'cerebro' a las máquinas para que tomen decisiones automáticas.\n\n**Qué aprenderás**:\n• 🤖 Programar robots y brazos mecánicos\n• ⚙️ Diseñar sistemas de control industrial\n• 🔄 Crear procesos automatizados\n• 📊 Desarrollar sistemas SCADA\n\n**Salida laboral**: Ingeniero de automatización, especialista en control industrial, diseñador de sistemas robóticos",
        "ejemplos_vida_real": ["Líneas de producción automáticas", "Sistemas de riego inteligente", "Control de tráfico", "Robots industriales"]
    },
    
    # --- ESTRUCTURA ACADÉMICA ---
    "creditos": {
        "preguntas": ["créditos", "cuántos créditos", "qué son créditos académicos"],
        "respuesta": "📊 **Sistema de Créditos - Explicado Fácil**\n\nLos créditos son como **'puntos de experiencia'** que ganas en tu formación:\n\n**Total carrera**: 160 créditos\n\n**Distribución**:\n• 🎯 Formación Profesional: 138 créditos (tu especialidad)\n• 🌟 Formación General: 6 créditos (visión amplia)\n• 💼 Formación de Facultad: 10 créditos (base ingenieril)\n• 👤 Formación Personal: 6 créditos (desarrollo humano)\n\n**En práctica**: 1 crédito ≈ 3 horas de trabajo semanal (clase + estudio)",
        "analogia": "Como subir de nivel en un videojuego: más créditos = más habilidades de ingeniero"
    },
    
    "proyecto_grado": {
        "preguntas": ["proyecto de grado", "trabajo de grado", "qué es proyecto grado"],
        "respuesta": "🎓 **Proyecto de Grado - Explicado Fácil**\n\nEs tu **'examen final práctico'** donde demuestras todo lo aprendido. Como el jefe final de un videojuego.\n\n**Características**:\n• 🚀 Aplicas CDIO completo\n• 💼 Puede ser con empresa real\n• 👥 Usualmente en equipo\n• 📈 Resuelve problema real\n\n**Ejemplos recientes**:\n• 'Sistema de monitoreo para cultivos de aguacate'\n• 'Robot para asistencia en biblioteca'\n• 'App para control de energía en hogares'",
        "duracion": "Generalmente 1-2 semestres"
    }
}

# ==================== SISTEMA DE DETECCIÓN MEJORADO ====================
def detectar_tema_explicacion(pregunta):
    """Detecta qué tema de explicación fácil se solicita"""
    pregunta = pregunta.lower().strip()
    
    # Buscar en todas las explicaciones
    for tema_id, contenido in explicaciones_faciles.items():
        for keyword in contenido["preguntas"]:
            if keyword in pregunta:
                return tema_id, 0.95
    
    # Búsqueda por palabras clave secundarias
    keywords_secundarios = {
        "concebir_cdio": ["concebir", "pensar", "planear", "idea"],
        "diseñar_cdio": ["diseñar", "planos", "esquema", "diagrama"],
        "proyectos_cdio": ["proyecto cdio", "proyecto integrador"],
        "sistemas_digitales": ["digital", "microcontrolador", "embebido", "iot"],
        "telecomunicaciones": ["telecom", "comunicación", "redes", "wifi", "bluetooth"],
        "automatizacion_control": ["automatización", "control", "robot", "industrial"],
        "creditos": ["crédito", "créditos", "puntos"],
        "proyecto_grado": ["proyecto grado", "trabajo grado", "trabajo final"]
    }
    
    for tema_id, palabras in keywords_secundarios.items():
        for palabra in palabras:
            if palabra in pregunta:
                return tema_id, 0.8
    
    return None, 0.0

def generar_respuesta_explicacion(tema_id, pregunta_original):
    """Genera respuesta en formato DialogFlow"""
    if tema_id in explicaciones_faciles:
        contenido = explicaciones_faciles[tema_id]
        
        respuesta = contenido["respuesta"]
        
        # Agregar ejemplo práctico si existe
        if "ejemplo_practico" in contenido:
            respuesta += f"\n\n💡 **En la práctica**: {contenido['ejemplo_practico']}"
        
        # Agregar ejemplos de vida real si existen
        if "ejemplos_vida_real" in contenido:
            respuesta += f"\n\n🏠 **Ejemplos en la vida real**:\n" + "\n".join([f"• {ejemplo}" for ejemplo in contenido["ejemplos_vida_real"]])
        
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [respuesta]
                    }
                }
            ],
            "payload": {
                "telegram": {
                    "text": respuesta,
                    "parse_mode": "Markdown"
                }
            }
        }
    
    # Si no encuentra tema específico
    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        "🤔 **Modo Explícamelo Fácil**\n\n"
                        "Puedo explicarte fácilmente sobre:\n\n"
                        "• 🧠 **Fases CDIO**: Concebir, Diseñar\n"
                        "• 🛠️ **Proyectos CDIO**: Cómo funcionan\n"
                        "• 🔢 **Líneas de profundización**: Sistemas Digitales, Telecomunicaciones, Automatización\n"
                        "• 📊 **Estructura académica**: Créditos, Proyecto de grado\n\n"
                        "¿Sobre cuál quieres que te explique de forma fácil?"
                    ]
                }
            }
        ]
    }

# ==================== RUTAS PRINCIPALES ====================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "🎓 Modo Explícamelo Fácil - PEP 2016-2025",
        "status": "active",
        "modo": "explicaciones_faciles",
        "temas_disponibles": list(explicaciones_faciles.keys()),
        "version": "PEP-1.0"
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Obtener datos de DialogFlow
        data = request.get_json()
        print("📨 Datos recibidos:", data)
        
        # Extraer pregunta según formato DialogFlow
        pregunta = ""
        
        if "queryResult" in data and "queryText" in data["queryResult"]:
            pregunta = data["queryResult"]["queryText"]
        elif "queryResult" in data and "parameters" in data["queryResult"]:
            params = data["queryResult"]["parameters"]
            if "any" in params:
                pregunta = params["any"]
        else:
            # Formato directo para pruebas
            pregunta = data.get("question", "")
        
        pregunta = pregunta.strip()
        print(f"🔍 Procesando pregunta: '{pregunta}'")
        
        if not pregunta:
            return jsonify({
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                "🎓 **Modo Explícamelo Fácil Activado**\n\n"
                                "Pídeme que te explique fácilmente cualquier concepto del PEP de Ingeniería Electrónica.\n\n"
                                "Ejemplo: 'Explícame fácil qué es concebir en CDIO'"
                            ]
                        }
                    }
                ]
            })
        
        # Detectar si es una solicitud de "explicación fácil"
        if "explica" in pregunta.lower() or "explicame" in pregunta.lower() or "facil" in pregunta.lower():
            tema_id, confianza = detectar_tema_explicacion(pregunta)
            
            if tema_id:
                print(f"✅ Tema detectado: {tema_id} (confianza: {confianza})")
                return jsonify(generar_respuesta_explicacion(tema_id, pregunta))
            else:
                # No se detectó tema específico
                return jsonify({
                    "fulfillmentMessages": [
                        {
                            "text": {
                                "text": [
                                    "🤔 **Modo Explícamelo Fácil**\n\n"
                                    "Detecté que quieres una explicación fácil, pero no estoy seguro del tema.\n\n"
                                    "Puedo explicarte sobre:\n"
                                    "• Fases de CDIO (Concebir, Diseñar)\n"
                                    "• Líneas de profundización\n"
                                    "• Proyectos de grado\n"
                                    "• Sistema de créditos\n\n"
                                    "¿Sobre cuál específicamente?"
                                ]
                            }
                        }
                    ]
                })
        else:
            # No es una solicitud de explicación fácil
            return jsonify({
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                "💡 **Tip**: Si quieres una explicación fácil de algún concepto, "
                                "usa frases como:\n\n"
                                "'Explícame fácil qué es CDIO'\n"
                                "'Explica fácil las líneas de profundización'\n"
                                "'¿Qué es concebir en CDIO de forma simple?'"
                            ]
                        }
                    }
                ]
            })
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "⚠️ Lo siento, hubo un error en el modo Explícamelo Fácil. "
                            "Intenta de nuevo en un momento."
                        ]
                    }
                }
            ]
        }), 500

@app.route("/temas", methods=["GET"])
def listar_temas():
    """Endpoint para ver temas disponibles"""
    temas_info = {}
    for tema_id, contenido in explicaciones_faciles.items():
        temas_info[tema_id] = {
            "preguntas_clave": contenido["preguntas"],
            "descripcion": contenido["respuesta"][:100] + "..."
        }
    
    return jsonify({
        "modo_explicaciones_faciles": temas_info,
        "total_temas": len(temas_info)
    })

if __name__ == "__main__":
    print("✅ Modo Explícamelo Fácil - Listo en puerto 5000")
    print("🎓 Temas especializados del PEP 2016-2025")
    print("🌐 Webhook activo para DialogFlow")
    app.run(host="0.0.0.0", port=5000, debug=False)
