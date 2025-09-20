from googletrans import Translator

traductor = Translator()

# Traducir texto (ejemplo: español → inglés)
resultado = traductor.translate("Hola amiga, ¿cómo estás?", src="es", dest="en")

print("Texto original:", resultado.origin)
print("Traducción:", resultado.text)
print("Idioma detectado:", resultado.src)
