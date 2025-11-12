from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import re
import numpy as np

app = Flask(__name__)

# --- ENTRENAR MODELO AL INICIAR ---
print("🔄 Inicializando y entrenando modelo...")

# Dataset mejorado
preguntas = [
    # CDIO
    "qué es cdio", "modelo cdio", "significado de cdio", "qué significa cdio", "explica cdio", "hablame de cdio",
    "cdio explicacion", "concepto cdio", "definicion cdio", "para que sirve cdio",
    
    # Misión
    "cuál es la misión", "dime la misión", "cuál es la mision del programa", "misión de la carrera",
    "qué es la mision", "objetivo del programa", "propósito del programa", "misión del ingeniero electrónico",
    
    # Visión
    "cuál es la visión", "dime la visión", "qué dice la visión", "visión de la carrera",
    "qué es la vision", "futuro del programa", "visión a futuro", "hacia dónde va el programa",
    
    # Perfil profesional
    "qué es perfil profesional", "qué hace un ingeniero electrónico", "perfil profesional del ingeniero electrónico",
    "campo laboral", "en qué trabaja un ingeniero electronico", "competencia del ingeniero",
    "habilidades del ingeniero electronico", "qué puede hacer un ingeniero electronico",
    
    # Materias
    "qué materias hay", "malla curricular", "qué materias se ven en sexto semestre", "materias del programa",
    "plan de estudios", "asignaturas de la carrera", "cursos de electronica", "pensum academico",
    "qué se estudia en electronica", "ramas de la electronica",
    
    # Proyección social
    "qué es proyección social", "en qué consiste la proyección social", "proyeccion social de la universidad",
    "impacto social del programa", "proyectos sociales de la carrera", "vinculación con la comunidad"
]

clases = [
    "cdio", "cdio", "cdio", "cdio", "cdio", "cdio", "cdio", "cdio", "cdio", "cdio",
    "mision", "mision", "mision", "mision", "mision", "mision", "mision", "mision",
    "vision", "vision", "vision", "vision", "vision", "vision", "vision", "vision",
    "perfil", "perfil", "perfil", "perfil", "perfil", "perfil", "perfil", "perfil",
    "materias", "materias", "materias", "materias", "materias", "materias", "materias", "materias", "materias", "materias",
    "proyeccion", "proyeccion", "proyeccion", "proyeccion", "proyeccion", "proyeccion"
]

# Preprocesamiento
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúñü\s]', '', texto)
    return texto.strip()

# Limpiar preguntas
preguntas_limpias = [limpiar_texto(p) for p in preguntas]

# Entrenar modelo
vectorizador = TfidfVectorizer()
X = vectorizador.fit_transform(preguntas_limpias)

modelo = LogisticRegression(max_iter=1000, random_state=42)
modelo.fit(X, clases)

print("✅ Modelo entrenado exitosamente!")
print(f"📊 Clases disponibles: {set(clases)}")

# Base de conocimientos con respuestas detalladas
base_conocimiento = {
    "cdio": {
        "respuesta": "CDIO es un modelo educativo innovador que significa: **Concebir, Diseñar, Implementar y Operar**. Es un framework que prepara a los ingenieros para enfrentar desafíos reales del mundo profesional, desarrollando no solo conocimientos técnicos sino también habilidades de trabajo en equipo, comunicación y liderazgo.",
        "ejemplos": ["Desarrollo de proyectos integradores", "Aprendizaje basado en problemas reales", "Trabajo en equipos multidisciplinarios"]
    },
    "mision": {
        "respuesta": "La **misión** del programa de Ingeniería Electrónica es formar profesionales integrales con sólidos conocimientos técnicos, capacidad innovadora y compromiso social. Buscamos desarrollar ingenieros que contribuyan al progreso tecnológico del país con ética y responsabilidad ambiental.",
        "enfoque": "Excelencia académica + Innovación + Responsabilidad social"
    },
    "vision": {
        "respuesta": "La **visión** del programa es ser reconocido como uno de los mejores programas de Ingeniería Electrónica a nivel nacional, destacándonos por nuestra investigación aplicada, vinculación con la industria y formación de profesionales altamente competitivos que lideren la transformación tecnológica.",
        "objetivos": ["Acreditación de alta calidad", "Investigación de impacto", "Vinculación internacional"]
    },
    "perfil": {
        "respuesta": "El **ingeniero electrónico** egresado de nuestro programa está capacitado para: Diseñar sistemas electrónicos y de telecomunicaciones, Desarrollar proyectos de automatización y control, Gestionar redes y sistemas de comunicación, Innovar en el área de Internet de las Cosas (IoT) y robótica, Dirigir proyectos de investigación y desarrollo tecnológico.",
        "campos_laborales": ["Telecomunicaciones", "Automatización industrial", "Desarrollo de hardware", "Investigación tecnológica", "Consultoría técnica"]
    },
    "materias": {
        "respuesta": "El **plan de estudios** incluye: Matemáticas y física avanzada, Circuitos y sistemas electrónicos, Electrónica digital y microcontroladores, Programación y algoritmos, Telecomunicaciones y redes, Control y automatización, Procesamiento de señales, Proyectos integradores por semestre.",
        "enfoque": "Formación teórico-práctica con proyectos aplicados desde primeros semestres"
    },
    "proyeccion": {
        "respuesta": "La **proyección social** de nuestro programa se manifiesta mediante: Desarrollo de proyectos tecnológicos para comunidades vulnerables, Asesoría técnica a pequeñas y medianas empresas, Programas de alfabetización digital, Ferias de ciencia y tecnología para colegios, Proyectos de energía renovable y sostenibilidad.",
        "impacto": "Vinculación universidad-empresa-sociedad para el desarrollo regional"
    }
}

# --- RUTAS ---
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "🤖 Bot 'Explícamelo Fácil' funcionando correctamente",
        "status": "active",
        "topics_available": list(base_conocimiento.keys()),
        "version": "2.0"
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        
        if not data or "question" not in data:
            return jsonify({
                "error": "No se recibió pregunta",
                "instruction": "Envía una pregunta en formato JSON: {'question': 'tu pregunta aquí'}"
            }), 400

        pregunta = data["question"]
        print(f"📥 Pregunta recibida: {pregunta}")

        # Preprocesar pregunta
        pregunta_limpia = limpiar_texto(pregunta)
        
        # Transformar y predecir
        X_pregunta = vectorizador.transform([pregunta_limpia])
        prediccion = modelo.predict(X_pregunta)[0]
        confianza = np.max(modelo.predict_proba(X_pregunta))
        
        print(f"🎯 Tema detectado: {prediccion} (confianza: {confianza:.2f})")

        # Generar respuesta
        if prediccion in base_conocimiento:
            info = base_conocimiento[prediccion]
            respuesta = {
                "answer": info["respuesta"],
                "detected_topic": prediccion,
                "confidence": round(float(confianza), 2),
                "original_question": pregunta,
                "status": "success"
            }
            
            # Agregar información adicional si existe
            if "ejemplos" in info:
                respuesta["examples"] = info["ejemplos"]
            if "enfoque" in info:
                respuesta["focus"] = info["enfoque"]
            if "campos_laborales" in info:
                respuesta["career_fields"] = info["campos_laborales"]
                
        else:
            respuesta = {
                "answer": f"🤔 He detectado que preguntas sobre '{prediccion}'. Estoy aprendiendo sobre este tema y pronto tendré más información detallada para ti.",
                "detected_topic": prediccion,
                "confidence": round(float(confianza), 2),
                "original_question": pregunta,
                "status": "learning"
            }

        return jsonify(respuesta)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "error": "Error interno del servidor",
            "message": str(e),
            "status": "error"
        }), 500

@app.route("/topics", methods=["GET"])
def list_topics():
    """Endpoint para listar todos los temas disponibles"""
    topics_info = {}
    for topic, info in base_conocimiento.items():
        topics_info[topic] = {
            "description": info["respuesta"][:100] + "...",
            "has_examples": "ejemplos" in info,
            "has_career_info": "campos_laborales" in info
        }
    
    return jsonify({
        "available_topics": topics_info,
        "total_topics": len(topics_info)
    })

if __name__ == "__main__":
    print("🚀 Iniciando servidor Flask...")
    app.run(host="0.0.0.0", port=5000, debug=False)
