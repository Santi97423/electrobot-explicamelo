# entrenar_modelo.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import re

# --- Dataset simple (puedes ampliar) ---
preguntas = [
    # CDIO
    "qué es cdio", "modelo cdio", "significado de cdio", "qué significa cdio", "explica cdio",
    # Misión
    "cuál es la misión", "dime la misión", "cuál es la mision del programa",
    # Visión
    "cuál es la visión", "dime la visión", "qué dice la visión",
    # Perfil profesional
    "qué es perfil profesional", "qué hace un ingeniero electrónico", "perfil profesional del ingeniero electrónico",
    # Materias
    "qué materias hay", "malla curricular", "qué materias se ven en sexto semestre", "materias del programa",
    # Proyección social
    "qué es proyección social", "en qué consiste la proyección social"
]

clases = [
    "cdio","cdio","cdio","cdio","cdio",
    "mision","mision","mision",
    "vision","vision","vision",
    "perfil","perfil","perfil",
    "materias","materias","materias","materias",
    "proyeccion","proyeccion"
]

# --- Preprocesamiento básico ---
def limpiar_texto(t):
    t = t.lower()
    t = re.sub(r'[^a-záéíóúñ\s]', '', t)
    return t

preguntas = [limpiar_texto(p) for p in preguntas]

# --- Vectorizador TF-IDF ---
vectorizador = TfidfVectorizer()
X = vectorizador.fit_transform(preguntas)

# --- Modelo simple ---
modelo = LogisticRegression(max_iter=1000)
modelo.fit(X, clases)

# --- Guardar modelo y vectorizador ---
joblib.dump(modelo, "modelo_explicamelo_facil.joblib")
joblib.dump(vectorizador, "vectorizador.joblib")

print("✅ Modelo entrenado y guardado correctamente:")
print(" - modelo_explicamelo_facil.joblib")
print(" - vectorizador.joblib")
