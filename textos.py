# -*- coding: utf-8 -*-
"""Textos de la web en inglés (principal), español y ruso.

Todo lo que se lee en la web sale de aquí: para cambiar una frase, se cambia
en los tres idiomas y se ejecuta `python build.py`. Los precios, los horarios
y los enlaces de pago están arriba del todo, una sola vez para los tres idiomas.

Estilo: habla Jose, en primera persona y sin frases de anuncio.
"""

WHATSAPP = "34665092090"
WHATSAPP_VISIBLE = "+34 665 09 20 90"
INSTAGRAM = "seawithjose"
EMAIL = "josemariahf612@gmail.com"
DOMINIO = "https://seawithjose.es"

IDIOMAS = ["en", "es", "ru"]          # el primero va en la raíz

# ─────────────────────────────── salidas en el Petit ───────────────────────────────
PRECIO_COMPARTIDA = 60                # € por persona
PRECIO_PRIVADA = 490                  # € por el barco entero, 2 horas
PLAZAS = 11                           # pasajeros como máximo, más el capitán
HORARIOS = ["10:30", "13:00", "15:30", "atardecer"]   # «atardecer»: puesta de sol − 1 h 45 min, la calcula la web
DIAS_RESERVA = 120                    # hasta cuántos días por delante se puede reservar
# Enlaces de pago de Stripe (Payment Links). Mientras estén vacíos, se reserva por WhatsApp.
# compartida: {número de personas: enlace}; privada: un enlace.
PAGOS = {"compartida": {}, "privada": ""}
# Reseñas reales (Google, CheckYeti…), en su idioma original. Lista vacía = el bloque no sale en la web.
# Formato: {"texto": "...", "nombre": "Anna", "origen": "Alemania", "fuente": "Google"}. Nunca inventarlas.
RESENAS = []

# ─────────────────────────────── la Bitácora (revista quincenal) ───────────────────────────────
# Formularios de suscripción de Brevo (Contactos > Formularios > Compartir), uno por idioma de la revista.
# Mientras estén vacíos, la página invita a escribir por WhatsApp.
REVISTA_FORMS = {"es": "https://24245cf8.sibforms.com/serve/MUIFAEmrpgChojMxJoy6P68lKnQH8Pdwr-1qUUHTz8eTHIz24_MokRkUUTL0Ddciyszt54Yy99S_mMPS4bzUsIa7bEnnK8uvHB7nZ3c1f3yjoMEvqG08nNosjRxRZGX-vZ8G_-YIc53MvrryVad9DcENcjd453jnG93gUSwdNseQz5Q7NfYePWa7uxB1Bq0XP5XDpgBcI6zk7awFXQ==",
                 "en": "https://24245cf8.sibforms.com/serve/MUIFAGrp6bXc-oWNuS0KXY4QRMBPDp2h17wWmvHhWyUffszoJi_RXKH3zXxd2RbImGjurzL10dDJgqhF2065Ydktwj50RXJy7du_Jvrlx7q9eiq4sTLFaVVHzEpeS3B--_12xGm2hbkJBz1I2kxtel95Qm-eWnQ6hgA7lcLN4XyyTvVzkMzLMHsmSWCEcfUiuAyxLvswzC2SqtxKfQ=="}
# Si SkylineWebcams o meteo365 autorizan a seawithjose.es, aquí va la dirección del reproductor de cada
# cámara (mismo orden que en T[...]["mar"]["camaras"]) y la web la enseña en directo en vez del enlace.
CAMARAS_EMBED = ["", "", ""]
# Parking Cristamar (calle Francisco Villalón): gratis para quien sale en el barco
PARKING = (36.49013, -4.95039)
PARKING_MAPS = "https://www.google.com/maps/search/?api=1&query=36.49013%2C-4.95039"
# Donde está amarrado el Petit en Puerto Banús (lo dio Jose el 14-10-2026)
BARCO = (36.485170, -4.951185)
BARCO_MAPS = "https://www.google.com/maps/search/?api=1&query=36.485170%2C-4.951185"

# ─────────────────────────────── la Senda Azul ───────────────────────────────
# Datos de «Málaga sumergida. Guía de buceo de la Senda Azul» (Turismo y Planificación Costa del Sol,
# 2024). Van de oeste a este; «banus» marca los que están a un paso de Puerto Banús.
SENDA_AZUL = [
    {"id": "chullera", "nombre": "Punta Chullera", "lugar": "Manilva", "prof": "0–30", "acceso": ["tierra", "barco"],
     "nivel": ["basico", "medio", "experto"], "vis": "buena", "banus": False,
     "que": {"en": "Sea fans and colourful nudibranchs below an old watchtower; snorkelling and try dives from the cove.",
             "es": "Gorgonias y babosas de colores junto a una torre vigía; esnórquel y bautizos desde la cala.",
             "ru": "Горгонии и яркие голожаберники у старой сторожевой башни; снорклинг и пробные погружения из бухты."}},
    {"id": "bovedas", "nombre": "El Placer de las Bóvedas", "lugar": "Marbella · San Pedro", "prof": "18–40",
     "acceso": ["barco"], "nivel": ["experto"], "vis": "media", "banus": True,
     "que": {"en": "A kilometre-long rocky bank off the Roman baths of Las Bóvedas, teeming with life. "
                   "A protected archaeological zone.",
             "es": "Un bajo rocoso de un kilómetro frente a las termas romanas de Las Bóvedas, lleno de vida. "
                   "Zona arqueológica protegida.",
             "ru": "Скалистая банка длиной в километр напротив римских терм Лас-Бóведас, полная жизни. "
                   "Охраняемая археологическая зона."}},
    {"id": "botones", "nombre": "Pecio de los Botones", "lugar": "Marbella · San Pedro", "prof": "8–10",
     "acceso": ["tierra", "barco"], "nivel": ["basico"], "vis": "media", "banus": True,
     "que": {"en": "“The Galleon”: the Spanish warship lost in 1760, 200 metres off San Pedro. Look, don’t touch.",
             "es": "«El Galeón»: el navío español hundido en 1760, a 200 metros de la orilla de San Pedro. "
                   "Se mira y no se toca.",
             "ru": "«Галеон»: испанский военный корабль, затонувший в 1760 году в 200 метрах от берега Сан-Педро. "
                   "Смотреть можно, трогать нельзя."}},
    {"id": "mineral", "nombre": "Torre del Mineral", "lugar": "Marbella", "prof": "6", "acceso": ["barco"],
     "nivel": ["basico"], "vis": "media", "banus": True,
     "que": {"en": "The old iron-ore loading pier: stone blocks, a sunken crane and a wreck, with hardly any current.",
             "es": "El viejo cargadero de mineral: bloques de piedra, una grúa y un barco hundidos, casi sin corriente.",
             "ru": "Старый рудный причал: каменные блоки, затонувший кран и судно, течения почти нет."}},
    {"id": "roqueillo", "nombre": "El Roqueíllo", "lugar": "Marbella", "prof": "29–33", "acceso": ["barco"],
     "nivel": ["experto"], "vis": "media", "banus": True,
     "que": {"en": "A rocky reef with anthias, lobsters, gorgonians and orange coral. Strong currents.",
             "es": "Un roquedal con antias, langostas, gorgonias y coral naranja. Corrientes fuertes.",
             "ru": "Скальный риф с антиасами, лангустами, горгониями и оранжевым кораллом. Сильные течения."}},
    {"id": "menapier", "nombre": "Pecio del Menapier", "lugar": "Mijas", "prof": "38–45", "acceso": ["barco"],
     "nivel": ["experto"], "vis": "mala", "banus": False,
     "que": {"en": "A Belgian cargo ship sunk in 1917, two miles off Calaburras lighthouse. A technical dive.",
             "es": "Un mercante belga hundido en 1917, a dos millas del faro de Calaburras. Buceo técnico.",
             "ru": "Бельгийское грузовое судно, затонувшее в 1917 году в двух милях от маяка Калабуррас. "
                   "Техническое погружение."}},
    {"id": "calaburras", "nombre": "Faro de Calaburras", "lugar": "Mijas", "prof": "0–22", "acceso": ["tierra", "barco"],
     "nivel": ["basico", "medio"], "vis": "regular", "banus": False,
     "que": {"en": "Sand and rock below an 1860s lighthouse; currents possible further out.",
             "es": "Arena y roca al pie de un faro del siglo XIX; lejos de la costa puede haber corriente.",
             "ru": "Песок и скалы у маяка XIX века; дальше от берега возможно течение."}},
    {"id": "marcelino", "nombre": "Piedras de Marcelino", "lugar": "Mijas", "prof": "8–14", "acceso": ["barco"],
     "nivel": ["medio"], "vis": "regular", "banus": False,
     "que": {"en": "Big stone blocks full of life. Bring a torch, an SMB and a compass.",
             "es": "Grandes bloques de piedra llenos de vida. Con linterna, boya y brújula.",
             "ru": "Большие каменные блоки, полные жизни. Нужны фонарь, буй и компас."}},
    {"id": "almirante", "nombre": "Laja del Almirante", "lugar": "Mijas", "prof": "18–25", "acceso": ["barco"],
     "nivel": ["medio"], "vis": "regular", "banus": False,
     "que": {"en": "Rock slabs and boulders carpeted with gorgonians. Torch, SMB and compass.",
             "es": "Lajas y grandes rocas tapizadas de gorgonias. Con linterna, boya y brújula.",
             "ru": "Плиты и валуны, покрытые горгониями. Фонарь, буй и компас."}},
    {"id": "yesera", "nombre": "Bajos de la Yesera", "lugar": "Fuengirola", "prof": "7", "acceso": ["tierra", "barco"],
     "nivel": ["basico"], "vis": "normal", "banus": False,
     "que": {"en": "Big boulders on sand 250 metres off the beach. Good for try dives.",
             "es": "Grandes piedras sobre arena a 250 metros de la orilla. Buena para bautizos.",
             "ru": "Крупные камни на песке в 250 метрах от берега. Подходит для пробных погружений."}},
    {"id": "isabella", "nombre": "Pecio Isabella", "lugar": "Benalmádena", "prof": "6–8", "acceso": ["barco"],
     "nivel": ["basico"], "vis": "regular", "banus": False,
     "que": {"en": "A sail-and-steam ship that went down in a storm in 1855 carrying sculptures and marble.",
             "es": "Un barco de vela y vapor hundido en un temporal en 1855, cargado de esculturas y mármol.",
             "ru": "Парусно-паровое судно, затонувшее в шторм в 1855 году с грузом скульптур и мрамора."}},
    {"id": "carmen", "nombre": "Baños del Carmen", "lugar": "Málaga", "prof": "0–6", "acceso": ["tierra"],
     "nivel": ["basico"], "vis": "normal", "banus": False,
     "que": {"en": "By the old seaside baths: snorkelling, small marine life and try dives.",
             "es": "Junto al antiguo balneario: esnórquel, vida pequeña y bautizos.",
             "ru": "У старой купальни: снорклинг, мелкая морская живность и пробные погружения."}},
    {"id": "arroz", "nombre": "El Barco del Arroz", "lugar": "Torrox", "prof": "5", "acceso": ["tierra", "barco"],
     "nivel": ["basico"], "vis": "buena", "banus": False,
     "que": {"en": "The supply ship Delfín, torpedoed in 1937, 60–80 metres from the beach. For every level.",
             "es": "El Delfín, un buque de víveres torpedeado en 1937, a 60–80 metros de la playa. Para todos los niveles.",
             "ru": "Судно снабжения «Дельфин», торпедированное в 1937 году, в 60–80 метрах от пляжа. "
                   "Для любого уровня."}},
    {"id": "maro", "nombre": "Acantilados de Maro", "lugar": "Nerja", "prof": "3–20", "acceso": ["barco"],
     "nivel": ["basico"], "vis": "buena", "banus": False,
     "que": {"en": "Caves, walls and posidonia meadows in a protected natural area. Great for snorkelling too.",
             "es": "Cuevas, paredes y praderas de posidonia en un paraje natural. También para esnórquel.",
             "ru": "Пещеры, стены и луга посидонии в природном парке. Отлично и для снорклинга."}},
    {"id": "cantarrijan", "nombre": "Cuevas de Cantarriján", "lugar": "Nerja", "prof": "3–15", "acceso": ["barco"],
     "nivel": ["basico"], "vis": "buena", "banus": False,
     "que": {"en": "Underwater caves and walls below the cliffs. Snorkelling too.",
             "es": "Cuevas y paredes bajo los acantilados. También para esnórquel.",
             "ru": "Подводные пещеры и стены под скалами. Подходит и для снорклинга."}},
]

T = {}

# ───────────────────────────────── INGLÉS ─────────────────────────────────
T["en"] = {
    "nombre_idioma": "English", "corto": "EN", "og_locale": "en_GB",
    "title": "Sailing trips from Puerto Banús, Marbella: dolphins and snorkelling · Sea With Jose",
    "description": ("Two hours under sail from Puerto Banús with Jose, yacht captain and oceanographer: dolphins, a swim "
                    "with mask and snorkel, drinks and nibbles included. Shared trip €60 per person; private €490 for "
                    "the boat, up to 11 guests."),
    "saltar": "Skip to content",
    "nav": {"precios": "Prices", "salida": "The trip", "barco": "The boat",
            "llegar": "Getting here", "revista": "Logbook"},
    "menu": "Menu", "whatsapp_corto": "WhatsApp", "reservar_corto": "Book",
    "wa_hola": "Hi Jose! I’d like to go sailing on the Petit.",
    "banderas_aria": "Sea With Jose spelt out in International Code of Signals flags",
    "hero_h1": "Sailing trips from Puerto Banús",
    "hero_lead": ("I’m Jose, a yacht captain and oceanographer. I take people sailing for two hours along the Marbella "
                  "coast on the Petit, a 12-metre sailing yacht. We stop for a swim well away from the beach and, with a "
                  "bit of luck, we see dolphins."),
    "hero_idiomas": "I speak English, Spanish and Russian.",
    "hero_precios": [("Shared", "€60", "per person"), ("Private", "€490", "the boat, 2 hours")],
    "hero_cta": "Book",
    "hero_cta2": "Message me on WhatsApp",
    "hero_foto_alt": "The Petit at anchor at sunset",
    "precios_h2": "Prices",
    "opciones": {
        "compartida": {"titulo": "Shared trip", "precio": "€60", "unidad": "per person",
                       "puntos": ["Two hours under sail, 11 people at most", "Water, soft drinks, beer and nibbles",
                                  "A swim with mask and snorkel, and I’ll tell you what lives down there",
                                  "Take the helm if you like", "Free cancellation up to 24 hours before"],
                       "cta": "Book a seat"},
        "privada": {"titulo": "Private trip", "precio": "€490", "unidad": "the whole boat, 2 hours",
                    "puntos": ["Just your group, up to 11 people", "You choose the time, sunset included",
                               "Water, soft drinks, beer and nibbles", "A swim with mask and snorkel",
                               "Add a paella, cocktails, decorations or a jet ski",
                               "Free cancellation up to 48 hours before"],
                    "cta": "Book the boat"},
    },
    "precios_nota": "Nothing else to pay on board. Just bring a swimsuit, a towel and sun cream.",
    "capitan": {"titulo": "Your skipper: Jose", "creds": ["Yacht captain", "Oceanographer", "FEDAS diving instructor"],
                "enlace": "More about me"},
    "resenas_h2": "What people say",
    "fotos_alt": {"petit-delfines": "Dolphins leaping in front of a sailing yacht",
                  "petit-banera": "The Petit’s cockpit under way",
                  "petit-proa": "The Petit’s teak foredeck"},
    "salida_h2": "What the trip is like",
    "pasos": [
        ("0:00", "We meet at the pontoon in Puerto Banús, 15 minutes before. I’ll send you the spot on WhatsApp."),
        ("0:15", "We motor out and hoist the sails past the harbour entrance. Then we head west or east, depending on the wind. Take the helm if you fancy it."),
        ("1:00", "Out at sea, far from the beach, we stop the boat for a swim with mask and snorkel."),
        ("2:00", "We sail back to Banús, closing the loop."),
    ],
    "salida_nota": "That’s the usual route. The wind and the sea decide the rest.",
    "carta_aria": ("Nautical chart of the coast between San Pedro Alcántara and Marbella, with the usual route of the "
                   "trip from Puerto Banús"),
    "carta": {"banus": "Puerto José Banús", "sanpedro": "San Pedro Alcántara", "marbella": "Marbella",
              "bano": "Swim", "rioverde": "Río Verde", "alboran": "Alboran Sea", "oeste": "W",
              "norte": "N", "ruta": "Depending on the wind"},
    "reserva_h2": "Booking",
    "reserva_intro": "Choose the day, the time and how many of you are coming. I’ll confirm on WhatsApp.",
    "form": {
        "tipo": "Trip", "tipos": {"compartida": "Shared", "privada": "Private"},
        "tipos_sub": {"compartida": "€60 per person", "privada": "€490 the boat"},
        "fecha": "Day", "hora": "Time", "atardecer": "Sunset",
        "personas": "People", "menos": "One person fewer", "mas": "One person more", "max": "11 at most",
        "nombre": "Your name", "nombre_ph": "",
        "extras": "Extras for private trips",
        "extras_nota": "Extras are priced separately. I’ll send you the price on WhatsApp before the trip.",
        "otra": "Anything else?",
        "total": "Total", "detalle_compartida": "{n} × €60", "detalle_privada": "The whole boat, 2 hours",
        "pagar": "Pay {total}", "whatsapp": "Book on WhatsApp",
        "seguro": "Payment is handled by Stripe. Your card details never go through this website.",
        "politica": ("Free cancellation up to 24 hours before a shared trip and 48 hours before a private one. If the "
                     "sea isn’t good enough to go out, we change the day or I give you your money back."),
        "sin_pago": "Card payment will be ready in a few days. For now, book on WhatsApp and I’ll confirm straight away.",
        "falta_fecha": "Choose a day.", "falta_hora": "Choose a time.", "falta_nombre": "Tell me your name.",
        "prevision": "AEMET forecast for that time: sailing {n}/10 ({banda})",
        "msg_inicio": "Hi Jose! I’d like to book a trip on the Petit.", "msg_tipo": "Trip", "msg_fecha": "Day",
        "msg_hora": "Time", "msg_personas": "People", "msg_extras": "Extras", "msg_nombre": "Name",
        "msg_total": "Total", "msg_ref": "Reference", "msg_pagado": "I’ve just paid online.",
    },
    "resumen": {"titulo": "Your booking", "salida": "Trip", "fecha": "Day", "hora": "Time", "pax": "People",
                "extras": "Extras", "total": "Total"},
    "extras_h2": "Extras for private trips",
    "extras_intro": ("For birthdays, proposals, hen and stag parties, or just because. Tell me what you’d like and "
                     "I’ll get it ready."),
    "extras": [
        {"id": "buffet", "titulo": "Buffet on board", "texto": "Nibbles, fruit and something sweet for everyone."},
        {"id": "paella", "titulo": "Paella", "texto": "To eat at anchor."},
        {"id": "cocteles", "titulo": "Cocktails", "texto": "And cava for a toast."},
        {"id": "tarta", "titulo": "Cake", "texto": "Your birthday or celebration cake."},
        {"id": "decoracion", "titulo": "Decorations", "texto": "Balloons, flowers and bunting, the way you want."},
        {"id": "moto", "titulo": "Jet ski", "texto": "For a spin during the trip."},
        {"id": "otra", "titulo": "Something else", "texto": "Music, a photographer, a surprise… just ask."},
    ],
    "extras_precio": "on request",
    "extras_cta": "Book a private trip",
    "barco_h2": "The Petit",
    "barco_sub": "Her name is P’tit Mousse, but everyone calls her the Petit.",
    "barco_p": [
        "She’s a centre-cockpit Jeanneau Sun Odyssey 42: 12.3 metres, a teak deck and a bimini that shades the cockpit.",
        "She’s stable and comfortable, with room for eleven guests plus the skipper.",
    ],
    "barco_datos": [("Model", "Jeanneau Sun Odyssey 42 CC"), ("Length", "12.3 m"), ("Guests", "11 + skipper"),
                    ("Berth", "Puerto José Banús")],
    "galeria": {"petit-azul": "The Petit moored under a blue sky",
                "petit-pantalan": "The Petit alongside a pontoon",
                "petit-cubierta": "The deck seen from the bow",
                "petit-bimini": "The bimini over the cockpit",
                "petit-fondeado": "The Petit at anchor"},
    "video_alt": "The Petit under way on a calm sea", "video_pausa": "Pause the video", "video_play": "Play the video",
    "jose_h2": "Who’ll take you out",
    "jose_p": [
        ("I studied oceanography at the University of Cádiz. I’m a yacht captain and a FEDAS diving instructor, and "
         "I’ve spent the last five seasons skippering sailing yachts, motorboats and fishing boats out of Marbella "
         "and Puerto Banús."),
        ("So I know where the water stays calm when the wind picks up, where the dolphins usually are and what lives "
         "on the seabed under the boat. I’ll tell you all about it in English, Spanish or Russian."),
    ],
    "jose_foto": "Jose on a boat, ready to dive",
    "cuaderno": "My logbook",
    "bitacora": [
        ("2016", "First dives. Ten years on, I still keep going back underwater."),
        ("2022", "First season as a charter skipper in Marbella."),
        ("2023", "Diving instructor (FEDAS · CMAS) and in charge of a charter fleet."),
        ("2025", "Sailing trips to see dolphins, and fishing charters."),
        ("2026", "Yacht Captain licence."),
    ],
    "mar": {
        "eyebrow": "The sea, right now",
        "h2": "How’s the sea today?",
        "intro": ("Three live webcams on the Marbella coast, and my score from 1 to 10 for sailing, diving and "
                  "fishing, worked out from the official AEMET forecast."),
        "camaras_h": "Live webcams", "en_directo": "Live", "ver": "Watch live",
        "camaras_nota": "The webcams belong to their owners and open on their own websites.",
        "camaras": [
            {"nombre": "Marbella marina", "que": "View of the marina in the town centre", "fuente": "SkylineWebcams",
             "url": "https://www.skylinewebcams.com/en/webcam/espana/andalucia/malaga/marbella-puerto-deportivo.html"},
            {"nombre": "Port and promenade", "que": "View of Marbella’s port and seafront promenade",
             "fuente": "SkylineWebcams", "url": "https://www.skylinewebcams.com/en/webcam/espana/andalucia/malaga/marbella.html"},
            {"nombre": "El Cable beach and La Bajadilla", "que": "The town beach and the fishing harbour",
             "fuente": "meteo365", "url": "https://meteo365.es/livecams/marbella.php"},
        ],
        "notas_h": "Score from 1 to 10", "dias_aria": "Choose the day", "hoy": "Today", "manana": "Tomorrow",
        "actividades": {"navegar": "Sailing", "bucear": "Diving", "pescar": "Fishing"},
        "bandas": ["Better another day", "Poor", "Fair", "Good", "Excellent"],
        "motivos": {
            "buen_viento": "Just the right wind for sailing.", "mar_tranquila": "Calm sea.",
            "sin_viento": "No wind: more swimming than sailing.", "poco_viento": "Light wind: slow sailing.",
            "viento_fresco": "Fresh breeze: the boat heels.", "viento": "A bit of wind.",
            "viento_fuerte": "Too much wind.", "rachas": "Strong gusts.", "marejadilla": "Small waves.",
            "marejada": "Choppy sea.", "mar_fuerte": "Rough sea.", "mar_de_fondo": "Swell.",
            "lluvia": "Rain likely.", "tormenta": "Risk of thunderstorms.", "niebla": "Fog or haze along the coast.",
            "agua_fria": "Cold water: thick wetsuit.", "aviso": "AEMET coastal warning.",
            "temporal": "Gale: we stay in port.",
        },
        "pasado": "over", "tramo": "h",
        "tabla": {"viento": "Wind", "racha": "Gusts", "mar": "Sea", "cielo": "Sky", "lluvia": "Rain", "agua": "Water", "fondo": "swell"},
        "mar_clases": ["calm, ripples", "smooth, up to 0.5 m", "slight, 0.5–1.25 m", "moderate, 1.25–2.5 m",
                       "rough, over 2.5 m"],
        "mar_cortos": ["calm", "smooth", "slight", "moderate", "rough"],
        "cielos": {"despejado": "clear", "poco_nuboso": "partly cloudy", "intervalos": "cloudy spells",
                   "nuboso": "cloudy", "cubierto": "overcast", "nubes_altas": "high cloud", "lluvia": "rain",
                   "lluvia_escasa": "light rain", "tormenta": "thunderstorms", "niebla": "fog", "bruma": "haze",
                   "calima": "dust haze"},
        "rumbos": {"N": "N", "NE": "NE", "E": "E", "SE": "SE", "S": "S", "SO": "SW", "O": "W", "NO": "NW", "C": "calm"},
        "kmh": "km/h",
        "costera_h": "AEMET coastal forecast · Málaga coastal waters",
        "costera_resumen": "Wind force {f} Beaufort, sea {m}.", "costera_a": " to ",
        "costera_texto": "Official text, in Spanish:", "costera_hasta": "Valid until {fin}.",
        "aviso_h": "AEMET warning for the Málaga coast",
        "como_h": "How I work out the score",
        "como": [
            ("Sailing", "the sweet spot is 13 to 28 km/h of wind (force 3 to 4) with a calm sea. Under 5 km/h we "
                        "motor; from 34 km/h, or with a choppy sea, the score drops fast."),
            ("Diving", "the state of the sea decides: up to small waves, good; choppy, so-so; anything more, no "
                       "diving. Wind over 20 km/h and swell take points off."),
            ("Fishing", "small waves at most and wind under 22 km/h."),
            ("All three", "thunderstorms, fog and rain take points off. With an AEMET coastal warning or a gale, the "
                          "score stays at 2 or below."),
        ],
        "aviso_legal": ("It’s a guide based on the forecast, not on the real sea: I make the final call at the "
                        "pontoon on the day, and if we can’t go out, we find another day."),
        "fuente": ("Forecast: AEMET (Río Verde – Puerto Banús beach, Marbella hour by hour and Málaga coastal "
                   "waters). Updated {hora}."),
        "cargando": "Loading the AEMET forecast…",
        "sin_datos": ("The AEMET forecast isn’t coming through right now. Message me and I’ll tell you how the sea "
                      "looks."),
    },
    "llegar_h2": "Getting here",
    "llegar_p": [
        "We leave from Puerto José Banús, in Marbella. When you book, I’ll send you the exact pontoon on WhatsApp.",
        ("If you’re coming by car, park at the Cristamar car park on Calle Francisco Villalón. It’s free if you’re "
         "sailing with us, and it’s a 10-minute walk to the boat."),
    ],
    "mapa": {"puerto": "Puerto José Banús", "parking": "Cristamar car park", "minutos": "10 min walk",
             "aria": "Map of Puerto Banús with the Cristamar car park and the walk to the harbour",
             "fuente": "Map: © OpenStreetMap contributors (ODbL)"},
    "llegar_enlace": "Open the car park in Google Maps",
    "llegar_barco": "Where the boat is",
    "buceo_h2": "Do you dive?",
    "buceo_lead": ("I’m also a FEDAS diving instructor. I’ll take you to the dive sites of Málaga’s Blue Path to suit "
                   "your level, or to your very first try dive."),
    "buceo_cta": "See all 15 dive sites",
    "buceo_title": "Diving in Marbella: the Blue Path dive sites · Sea With Jose",
    "buceo_description": ("The 15 dive sites of Málaga’s Blue Path with their depth, level and access, plus try dives "
                          "and FEDAS courses with Jose, diving instructor in Marbella."),
    "senda": {
        "eyebrow": "Diving · The Blue Path",
        "h1": "Málaga’s Blue Path, site by site",
        "lead": ("The Senda Azul (Blue Path) is the official dive guide to the Málaga coast: fifteen dives from Manilva "
                 "to Nerja, each with its depth, level and what you’ll see. Four of them are just off Puerto Banús."),
        "filtros": {"todos": "All", "basico": "Beginner", "medio": "Intermediate", "experto": "Advanced",
                    "banus": "Near Banús"},
        "campos": {"prof": "Depth", "nivel": "Level", "acceso": "Access", "vis": "Visibility"},
        "accesos": {"barco": "by boat", "tierra": "from the shore"},
        "niveles": {"basico": "Beginner", "medio": "Intermediate", "experto": "Advanced"},
        "visibilidades": {"buena": "good", "normal": "normal", "media": "average", "regular": "fair", "mala": "poor"},
        "cerca": "Near Banús", "salida": "Puerto Banús", "quiero": "I want to dive here",
        "msg": "Hi Jose! I’d like to dive at {sitio}. My level is: ",
        "fuente": ("Data: “Málaga sumergida. Guía de buceo de la Senda Azul”, Turismo y Planificación Costa del Sol "
                   "(2024). Water: 15–23 °C depending on the season."),
        "aviso": "Advanced dives need the right certification and experience; the Menapier is a technical dive.",
        "linea_aria": "The Blue Path dive sites along the Málaga coast, from Manilva in the west to Nerja in the east",
        "vacio": "No sites match that filter.",
    },
    "buceo_bloques": [
        ("Your first dive", "Calm, shallow water and me right beside you the whole time. "
                            "No experience needed, just curiosity."),
        ("Get certified", "FEDAS · CMAS courses: from One Star Diver (B1E), which lets you dive with a buddy "
                          "down to 25 metres, to advanced levels and specialties. Recognised worldwide through CMAS."),
    ],
    "pecio_eyebrow": "Wreck off San Pedro Alcántara",
    "pecio_h": "The Galleon: the warship <em>Fernando</em>, 1760",
    "pecio_p": [
        ("For decades everyone called it “the Galleon” and said it was French. In 2026 the Andalusian Institute "
         "of Historical Heritage solved the mystery: it is the <em>Fernando</em>, a Spanish ship of the line built "
         "in Ferrol in 1750–51 and lost in 1760."),
        "Its remains lie between eight and ten metres down, 200 metres from the beach: three centuries of history "
        "within reach of any diver.",
    ],
    "pecio_datos": [("Depth", "8–10 m"), ("Level", "beginner"), ("You’ll see", "frames, ballast and the life on the wreck")],
    "habichuelas_h": "The Beans Wreck at Punta Carnero",
    "habichuelas_p": ("The <em>Dina</em>, a 109-metre freighter that ran aground in an easterly storm in 1983 "
                      "carrying tinned beans. Today it’s a reef full of life between 8 and 12 metres."),
    "viajes_h": "Dive trips",
    "viajes_p": ("Every year I lead small-group trips to the world’s great dive destinations: the Maldives, "
                 "the Philippines, Indonesia. Tell me where you’d like to go next."),
    "fotos_buceo": {"pulpo": "An octopus on the seabed off Marbella", "ok": "Two divers giving the OK sign",
                    "tortuga": "Diving with a green turtle", "tiburon": "Divers watching a tiger shark"},
    "buceo_wa": "Hi Jose! I’d like to go diving with you.",
    "buceo_wa_cta": "Ask about diving",
    "pesca_h2": "If fishing is more your thing",
    "pesca_p": ("I also run fishing trips, bottom fishing or trolling, in the morning or the afternoon. If it’s your "
                "first time, I’ll show you how."),
    "pesca_cta": "Ask about fishing",
    "pesca_wa": "Hi Jose! I’d like to know more about your fishing trips.",
    "faq_h2": "Questions",
    "faq": [
        ("How much does it cost?", "A shared trip is €60 per person. A private trip is €490 for the whole boat for two "
                                   "hours, for up to 11 people. Extras for private trips are priced separately."),
        ("Do I need to know how to sail?", "No, I sail the boat. If you like, I’ll show you how to steer."),
        ("Where do we meet?", "At Puerto José Banús. I’ll send you the exact pontoon on WhatsApp."),
        ("Where can I park?", "At the Cristamar car park, a 10-minute walk from the boat. It’s free if you’re sailing "
                              "with us."),
        ("What should I bring?", "Swimsuit, towel, sunscreen and sunglasses."),
        ("What if the weather is bad?", "I only go out when the sea is right. If I cancel because of the weather, you "
                                        "choose another day or I give you your money back."),
        ("Can I cancel?", "Yes, for free up to 24 hours before a shared trip and 48 hours before a private one."),
        ("What’s included?", "Water, soft drinks, beer, some nibbles and a mask and snorkel for everyone. Nothing "
                             "else to pay on board."),
        ("Can children come?", "Of course. Tell me their ages when you book."),
        ("Which languages do you speak?", "English, Spanish and Russian."),
    ],
    "final_h2": "Coming aboard?",
    "final_p": "Book your seat or message me and I’ll help you choose.",
    "pie_lugar": "Puerto José Banús, 29660 Marbella (Málaga), Spain",
    "pie_legal": "Legal notice, bookings and privacy",
    "pie_creditos": "Photos: the Petit · Charts: EMODnet (CC BY 4.0) and OpenStreetMap (ODbL) · Forecast: AEMET",
    "legal_title": "Legal notice, bookings and privacy · Sea With Jose",
    "legal_h1": "Legal notice, bookings and privacy",
    "legal": [
        ("Who runs this website", "Sea With Jose is the personal brand of José María Hinojosa Figueira, based in "
                                  "Marbella (Málaga, Spain). Contact: {email} · WhatsApp {tel}."),
        ("What this website does", "It shows my sailing trips on the Petit and the extras for private trips, and "
                                   "lets you book and pay for them online. It also publishes the Sea Logbook, my fortnightly magazine, "
                                   "and official weather data for Marbella."),
        ("Bookings and payment", "Trips are paid in advance by card through Stripe, which processes the payment: this "
                                 "website never sees or stores your card details. Your booking is confirmed when I "
                                 "write to you on WhatsApp or by email. The prices shown are final prices. Extras for "
                                 "private trips are priced and paid separately."),
        ("Cancellations", "You can cancel for free up to 24 hours before a shared trip, or 48 hours before a private "
                          "one, and I’ll refund you in full. If I "
                          "cancel because of the state of the sea or for safety reasons, you choose another day or a "
                          "full refund. As this is a leisure activity on a specific date, the 14-day right of "
                          "withdrawal does not apply (article 103.l of the Spanish consumer protection law)."),
        ("On board", "For safety, the skipper decides the route, where to anchor and whether to go out or carry on "
                     "sailing."),
        ("Your data", "If you book or write to me, I use your name, contact details and booking details only to "
                      "organise your trip and meet my tax obligations, and I keep them only as long as required. "
                      "Stripe processes payment data as an independent controller (stripe.com/privacy). You can ask "
                      "me at any time to see, correct or delete your data by writing to {email}, and you can complain "
                      "to the Spanish Data Protection Agency (aepd.es)."),
        ("The Sea Logbook (newsletter)", "If you subscribe to the Logbook, I only use your email address (and your name, "
         "if you give it) to send you the magazine every fortnight, on the basis of the consent you give in the form "
         "and confirm by email (double opt-in). The list is kept by Brevo (Sendinblue SAS, France, EU) as data "
         "processor; Brevo records whether each issue is opened, only to measure the newsletter. Every issue has an "
         "unsubscribe link and I delete your data when you unsubscribe. You can also ask me to see, correct or delete "
         "it at {email}."),
        ("Cookies", "This website uses no cookies and no analytics. While you book, your browser keeps the details of "
                    "your booking so they can be shown again when you come back from the payment page. Fonts and "
                    "images are served from the site itself."),
        ("Third parties", "The site is hosted on GitHub Pages (GitHub Inc.), which may record visitors’ IP addresses "
                          "for security. The WhatsApp, Instagram and Google Maps links take you to those "
                          "services, which have their own privacy policies."),
        ("Credits", "Bathymetry: EMODnet Bathymetry Consortium, CC BY 4.0. Map of Puerto Banús: © OpenStreetMap "
                    "contributors, ODbL. Forecasts and Marbella weather data: information prepared by the Spanish State Meteorological Agency "
                    "(AEMET)."),
    ],
    "gracias": {"title": "Booking received · Sea With Jose", "h1": "Booking received",
                "p": "Thank you. As soon as I see your payment, I’ll confirm your trip on WhatsApp.",
                "resumen": "Your trip", "wa": "Message me on WhatsApp", "volver": "Back to the website",
                "sin": ("I can’t find your booking details in this browser, but don’t worry: Stripe has emailed you the "
                        "receipt. Message me and we’ll sort it out.")},
    "volver": "Back to the home page",
    "e404_h1": "This page is off the chart",
    "e404_p": "The address may be wrong or the page has moved.",
    "datos": {
        "title": "Official weather data in Marbella, hour by hour · Sea With Jose",
        "description": ("Wind, gusts, direction, rain, temperature and humidity measured by AEMET at Marbella marina, hour "
                        "by hour, with records back to 2004. Interactive charts and variable cross-checks."),
        "eyebrow": "Official data · AEMET",
        "h1": "Marbella weather, reading by reading",
        "lead": ("What the official AEMET stations in Marbella measure: wind, gusts, direction, rain, temperature and "
                 "humidity. You start with the last week; zoom out to the whole record and cross one variable with another."),
        "ahora_h": "Right now",
        "serie_h": "Over time",
        "var1": "Variable", "var2": "Compare with", "ninguna": "None",
        "rangos": {"7": "7 days", "30": "30 days", "365": "1 year", "todo": "All"},
        "zoom": "Reset zoom", "csv": "Download CSV",
        "zoom_ayuda": "Mouse wheel or pinch to zoom; drag to move.",
        "cruce_h": "Cross variables",
        "cruce_p": ("Pick two variables and see how they relate over the period chosen above. If one is wind direction, "
                    "you get the average of the other by where the wind blows from."),
        "eje_x": "X variable", "eje_y": "Y variable", "estacion": "Station",
        "estaciones": {"6076X": "Marbella, Marina (6076X)", "6083X": "Marbella (6083X)"},
        "nota": ("Hourly data since 14 October 2026, when I started saving it (AEMET only publishes the last 24 hours); "
                 "before that, one value per day. Wind is measured 10 m above ground."),
        "fuente": ("Source: Spanish State Meteorological Agency (AEMET), conventional observations and daily climate "
                   "values from its stations in the municipality of Marbella. © AEMET."),
        "error": "I couldn’t load the data. Please try again in a few minutes.",
        "js": {"vars": {"viento": "Mean wind", "racha": "Strongest gust", "dir": "Wind direction",
                        "lluvia": "Rain", "temp": "Air temperature", "humedad": "Humidity"},
               "rumbos": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
               "diario": "daily average", "media": "Average", "actualizado": "Latest reading:",
               "ultima_hora": "in the last hour",
               "cruce_rumbo": "Average by direction, {n} data pairs.",
               "cruce_r": "Correlation r = {r} ({lectura}), {n} data pairs.",
               "fuerte": "strong", "moderada": "moderate", "debil": "weak or none",
               "pocos": "Not enough data in this period."},
    },
    "revista": {
        "title": "The Sea Logbook: a free fortnightly magazine about the sea · Sea With Jose",
        "description": ("Every fortnight, in your inbox: the water temperature off Marbella, and the most interesting news "
                        "on diving, sailing, fishing, sea travel and the ocean. Written by Jose, captain and oceanographer."),
        "eyebrow": "Free · every fortnight",
        "h1": "The Sea Logbook",
        "lead": ("Every fortnight I send a short magazine about the sea: how the water has been off Marbella, and the "
                 "best news on diving, sailing, fishing and sea travel, picked and explained by me."),
        "ejes_h": "What’s inside",
        "ejes": [("mar", "The sea this fortnight", "Water temperature, waves and wind off Puerto Banús, and the moon for fishing."),
                 ("buceo", "Diving", "New sites, marine life, courses and what’s happening under the water."),
                 ("vela", "Sailing and boats", "Regattas, boats, seamanship and news from the marinas."),
                 ("pesca", "Fishing", "Seasons, species and the rules for recreational fishing."),
                 ("viajes", "Sea travel", "Destinations for diving and sailing, near and far."),
                 ("ciencia", "Ocean news", "Discoveries, whales, sharks and the stories that make the headlines.")],
        "susc_h": "Get it in your inbox",
        "susc_p": "Choose your language. You’ll get an email to confirm, and you can unsubscribe with one click.",
        "susc_es": "Subscribe in Spanish",
        "susc_en": "Subscribe in English",
        "susc_sin": "Subscriptions open very soon. Meanwhile, message me and I’ll add you.",
        "susc_wa": "Hi Jose! I’d like to receive the Sea Logbook.",
        "archivo_h": "Past issues",
        "archivo_vacio": "The first issue is on its way.",
        "archivo_idioma": {"es": "Spanish", "en": "English"},
        "privacidad": ("Your email is only used to send you the Logbook, through Brevo (Sendinblue SAS, EU). "
                       "You can unsubscribe at any time from any issue."),
        "estado": {"pendiente": ("Check your inbox", "I’ve sent you an email with a link to confirm your subscription."),
                   "ok": ("You’re in!", "The next issue of the Logbook will reach you in a few days.")},
    },
}

# ───────────────────────────────── ESPAÑOL ─────────────────────────────────
T["es"] = {
    "nombre_idioma": "Español", "corto": "ES", "og_locale": "es_ES",
    "title": "Salidas en velero desde Puerto Banús, Marbella: delfines y snorkel · Sea With Jose",
    "description": ("Dos horas a vela desde Puerto Banús con Jose, capitán de yate y oceanógrafo: delfines, baño con "
                    "gafas y tubo, bebida y picoteo incluidos. Compartida 60 € por persona; privada 490 € el barco, "
                    "hasta 11 personas."),
    "saltar": "Ir al contenido",
    "nav": {"precios": "Precios", "salida": "La salida", "barco": "El barco",
            "llegar": "Cómo llegar", "revista": "Bitácora"},
    "menu": "Menú", "whatsapp_corto": "WhatsApp", "reservar_corto": "Reservar",
    "wa_hola": "¡Hola Jose! Me gustaría salir a navegar en el Petit.",
    "banderas_aria": "Sea With Jose escrito con banderas del Código Internacional de Señales",
    "hero_h1": "Salidas en velero desde Puerto Banús",
    "hero_lead": ("Soy Jose, capitán de yate y oceanógrafo. Salgo a navegar dos horas por la costa de Marbella en el "
                  "Petit, un velero de 12 metros. Paramos a bañarnos lejos de la orilla y, con suerte, vemos delfines."),
    "hero_idiomas": "Hablo español, inglés y ruso.",
    "hero_precios": [("Compartida", "60 €", "por persona"), ("Privada", "490 €", "el barco, 2 horas")],
    "hero_cta": "Reservar",
    "hero_cta2": "Escríbeme por WhatsApp",
    "hero_foto_alt": "El Petit fondeado al atardecer",
    "precios_h2": "Precios",
    "opciones": {
        "compartida": {"titulo": "Salida compartida", "precio": "60 €", "unidad": "por persona",
                       "puntos": ["Dos horas a vela, como mucho 11 personas", "Agua, refrescos, cerveza y picoteo",
                                  "Baño con gafas y tubo, y te cuento qué vive ahí abajo",
                                  "Si quieres, llevas el timón", "Cancelación gratis hasta 24 horas antes"],
                       "cta": "Reservar plaza"},
        "privada": {"titulo": "Salida privada", "precio": "490 €", "unidad": "el barco entero, 2 horas",
                    "puntos": ["Solo tu grupo, hasta 11 personas", "Tú eliges la hora, también al atardecer",
                               "Agua, refrescos, cerveza y picoteo", "Baño con gafas y tubo",
                               "Puedes añadir paella, cócteles, decoración o una moto de agua",
                               "Cancelación gratis hasta 48 horas antes"],
                    "cta": "Reservar el barco"},
    },
    "precios_nota": "Nada más que pagar a bordo. Solo trae bañador, toalla y crema solar.",
    "capitan": {"titulo": "Tu capitán: Jose", "creds": ["Capitán de yate", "Oceanógrafo", "Instructor de buceo FEDAS"],
                "enlace": "Más sobre mí"},
    "resenas_h2": "Lo que cuentan",
    "fotos_alt": {"petit-delfines": "Delfines saltando delante de un velero",
                  "petit-banera": "La bañera del Petit navegando",
                  "petit-proa": "La cubierta de teca del Petit"},
    "salida_h2": "Así es la salida",
    "pasos": [
        ("0:00", "Nos vemos en el pantalán de Puerto Banús un cuarto de hora antes. Te mando la ubicación por WhatsApp."),
        ("0:15", "Salimos a motor y, pasada la bocana, izamos velas. Según el viento, vamos hacia un lado o hacia el otro. Si te apetece, llevas el timón."),
        ("1:00", "Mar adentro, lejos de la playa, paramos el barco y nos damos un baño con gafas y tubo."),
        ("2:00", "Volvemos a Banús a vela, cerrando la vuelta."),
    ],
    "salida_nota": "Es la ruta habitual. El viento y el mar deciden el resto.",
    "carta_aria": ("Carta náutica de la costa entre San Pedro Alcántara y Marbella, con la ruta habitual de la salida "
                   "desde Puerto Banús"),
    "carta": {"banus": "Puerto José Banús", "sanpedro": "San Pedro Alcántara", "marbella": "Marbella",
              "bano": "Baño", "rioverde": "Río Verde", "alboran": "Mar de Alborán", "oeste": "O",
              "norte": "N", "ruta": "Según el viento"},
    "reserva_h2": "Reserva",
    "reserva_intro": "Elige el día, la hora y cuántos sois. Te confirmo por WhatsApp.",
    "form": {
        "tipo": "Salida", "tipos": {"compartida": "Compartida", "privada": "Privada"},
        "tipos_sub": {"compartida": "60 € por persona", "privada": "490 € el barco"},
        "fecha": "Día", "hora": "Hora", "atardecer": "Atardecer",
        "personas": "Personas", "menos": "Una persona menos", "mas": "Una persona más", "max": "Como mucho 11",
        "nombre": "Tu nombre", "nombre_ph": "",
        "extras": "Extras para la privada",
        "extras_nota": "Los extras van aparte. Te paso el precio por WhatsApp antes de la salida.",
        "otra": "¿Algo más?",
        "total": "Total", "detalle_compartida": "{n} × 60 €", "detalle_privada": "El barco entero, 2 horas",
        "pagar": "Pagar {total}", "whatsapp": "Reservar por WhatsApp",
        "seguro": "El pago lo gestiona Stripe. Los datos de tu tarjeta no pasan por esta web.",
        "politica": ("Cancelación gratis hasta 24 horas antes en la compartida y 48 horas en la privada. Si el mar no "
                     "deja salir, cambiamos el día o te devuelvo el dinero."),
        "sin_pago": "El pago con tarjeta estará listo en unos días. Mientras, reserva por WhatsApp y te confirmo enseguida.",
        "falta_fecha": "Elige el día.", "falta_hora": "Elige la hora.", "falta_nombre": "Dime tu nombre.",
        "prevision": "Previsión de AEMET para esa hora: navegar {n}/10 ({banda})",
        "msg_inicio": "¡Hola Jose! Quiero reservar una salida en el Petit.", "msg_tipo": "Salida", "msg_fecha": "Día",
        "msg_hora": "Hora", "msg_personas": "Personas", "msg_extras": "Extras", "msg_nombre": "Nombre",
        "msg_total": "Total", "msg_ref": "Referencia", "msg_pagado": "Acabo de pagar por la web.",
    },
    "resumen": {"titulo": "Tu reserva", "salida": "Salida", "fecha": "Día", "hora": "Hora", "pax": "Personas",
                "extras": "Extras", "total": "Total"},
    "extras_h2": "Extras para las privadas",
    "extras_intro": "Para cumpleaños, pedidas, despedidas o porque sí. Dime qué te apetece y lo preparo.",
    "extras": [
        {"id": "buffet", "titulo": "Buffet a bordo", "texto": "Picoteo, fruta y algo dulce para todo el grupo."},
        {"id": "paella", "titulo": "Paella", "texto": "Para comer fondeados."},
        {"id": "cocteles", "titulo": "Cócteles", "texto": "Y cava para brindar."},
        {"id": "tarta", "titulo": "Tarta", "texto": "La de tu cumpleaños o la de tu celebración."},
        {"id": "decoracion", "titulo": "Decoración", "texto": "Globos, flores y banderines, como tú quieras."},
        {"id": "moto", "titulo": "Moto de agua", "texto": "Para dar una vuelta durante la salida."},
        {"id": "otra", "titulo": "Otra idea", "texto": "Música, fotógrafo, una sorpresa… Pídemelo."},
    ],
    "extras_precio": "a consultar",
    "extras_cta": "Reservar salida privada",
    "barco_h2": "El Petit",
    "barco_sub": "Se llama P’tit Mousse, pero todos lo llamamos el Petit.",
    "barco_p": [
        "Es un Jeanneau Sun Odyssey 42 de bañera central: 12,3 metros, cubierta de teca y un bimini que da sombra a la bañera.",
        "Es estable y cómodo, y caben once personas más el capitán.",
    ],
    "barco_datos": [("Modelo", "Jeanneau Sun Odyssey 42 CC"), ("Eslora", "12,3 m"), ("Pasajeros", "11 + capitán"),
                    ("Amarre", "Puerto José Banús")],
    "galeria": {"petit-azul": "El Petit amarrado con el cielo azul",
                "petit-pantalan": "El Petit abarloado a un pantalán",
                "petit-cubierta": "La cubierta vista desde proa",
                "petit-bimini": "El bimini sobre la bañera",
                "petit-fondeado": "El Petit fondeado"},
    "video_alt": "El Petit navegando con el mar en calma", "video_pausa": "Pausar el vídeo",
    "video_play": "Reproducir el vídeo",
    "jose_h2": "Quién te lleva",
    "jose_p": [
        ("Soy oceanógrafo por la Universidad de Cádiz, capitán de yate e instructor de buceo FEDAS. Llevo cinco "
         "temporadas de patrón en veleros, lanchas y barcos de pesca en Marbella y Puerto Banús."),
        ("Por eso sé dónde sigue el agua en calma cuando se levanta el viento, por dónde suelen andar los delfines y "
         "qué vive en el fondo debajo del barco. Te lo cuento en español, en inglés o en ruso."),
    ],
    "jose_foto": "Jose en un barco, listo para bucear",
    "cuaderno": "Mi cuaderno de bitácora",
    "bitacora": [
        ("2016", "Primeras inmersiones. Diez años después sigo volviendo bajo el agua."),
        ("2022", "Primera temporada como patrón de chárter en Marbella."),
        ("2023", "Instructor de buceo (FEDAS · CMAS) y responsable de una flota de chárter."),
        ("2025", "Salidas en velero para ver delfines y chárter de pesca."),
        ("2026", "Título de Capitán de Yate."),
    ],
    "mar": {
        "eyebrow": "El mar, ahora",
        "h2": "¿Cómo está el mar hoy?",
        "intro": ("Tres cámaras en directo de la costa de Marbella y mi nota del 1 al 10 para navegar, bucear y "
                  "pescar, hecha con la previsión oficial de AEMET."),
        "camaras_h": "Cámaras en directo", "en_directo": "En directo", "ver": "Ver en directo",
        "camaras_nota": "Las cámaras son de sus dueños y se abren en su propia web.",
        "camaras": [
            {"nombre": "Puerto deportivo de Marbella", "que": "Vista del puerto deportivo del centro",
             "fuente": "SkylineWebcams", "url": "https://www.skylinewebcams.com/es/webcam/espana/andalucia/malaga/marbella-puerto-deportivo.html"},
            {"nombre": "Puerto y paseo marítimo", "que": "Vista del puerto y del paseo marítimo de Marbella",
             "fuente": "SkylineWebcams", "url": "https://www.skylinewebcams.com/es/webcam/espana/andalucia/malaga/marbella.html"},
            {"nombre": "Playa de El Cable y La Bajadilla", "que": "La playa del centro y el puerto pesquero",
             "fuente": "meteo365", "url": "https://meteo365.es/es/livecams/marbella.php"},
        ],
        "notas_h": "Nota del 1 al 10", "dias_aria": "Elige el día", "hoy": "Hoy", "manana": "Mañana",
        "actividades": {"navegar": "Navegar", "bucear": "Bucear", "pescar": "Pescar"},
        "bandas": ["Mejor otro día", "Mala", "Regular", "Buena", "Muy buena"],
        "motivos": {
            "buen_viento": "Viento justo para ir a vela.", "mar_tranquila": "Mar tranquila.",
            "sin_viento": "Sin viento: más baño que vela.", "poco_viento": "Poco viento: se navega despacio.",
            "viento_fresco": "Viento fresco: se navega escorado.", "viento": "Algo de viento.",
            "viento_fuerte": "Demasiado viento.", "rachas": "Rachas fuertes.", "marejadilla": "Algo de ola.",
            "marejada": "Marejada: mar movida.", "mar_fuerte": "Mar fuerte.", "mar_de_fondo": "Mar de fondo.",
            "lluvia": "Probable lluvia.", "tormenta": "Riesgo de tormenta.",
            "niebla": "Niebla o bruma en la costa.", "agua_fria": "Agua fría: traje grueso.",
            "aviso": "Aviso costero de AEMET.", "temporal": "Temporal: no se sale.",
        },
        "pasado": "ya pasó", "tramo": "h",
        "tabla": {"viento": "Viento", "racha": "Rachas", "mar": "Mar", "cielo": "Cielo", "lluvia": "Lluvia",
                  "agua": "Agua", "fondo": "mar de fondo"},
        "mar_clases": ["rizada", "marejadilla, hasta 0,5 m", "marejada, 0,5–1,25 m", "fuerte marejada, 1,25–2,5 m",
                       "gruesa, más de 2,5 m"],
        "mar_cortos": ["rizada", "marejadilla", "marejada", "fuerte marejada", "gruesa"],
        "cielos": {"despejado": "despejado", "poco_nuboso": "poco nuboso", "intervalos": "intervalos nubosos",
                   "nuboso": "nuboso", "cubierto": "cubierto", "nubes_altas": "nubes altas", "lluvia": "lluvia",
                   "lluvia_escasa": "lluvia débil", "tormenta": "tormenta", "niebla": "niebla", "bruma": "bruma",
                   "calima": "calima"},
        "rumbos": {"N": "N", "NE": "NE", "E": "E", "SE": "SE", "S": "S", "SO": "SO", "O": "O", "NO": "NO", "C": "calma"},
        "kmh": "km/h",
        "costera_h": "Parte costero de AEMET · Aguas costeras de Málaga",
        "costera_resumen": "Viento fuerza {f}, mar {m}.", "costera_a": " a ",
        "costera_texto": "Texto oficial:", "costera_hasta": "Válido hasta {fin}.",
        "aviso_h": "Aviso de AEMET para la costa de Málaga",
        "como_h": "Cómo pongo la nota",
        "como": [
            ("Navegar", "lo ideal es viento de 13 a 28 km/h (fuerza 3 a 4) con mar tranquila. Con menos de 5 km/h "
                        "se va a motor; desde 34 km/h, o con marejada, la nota baja mucho."),
            ("Bucear", "manda el estado de la mar: con marejadilla o menos, bien; con marejada, regular; con más, no "
                       "se bucea. El viento de más de 20 km/h y el mar de fondo restan."),
            ("Pescar", "mar hasta marejadilla y viento por debajo de 22 km/h."),
            ("En las tres", "restan la tormenta, la niebla y la lluvia. Con aviso costero de AEMET o temporal, la "
                            "nota no pasa de 2."),
        ],
        "aviso_legal": ("Es una nota orientativa hecha con la previsión, no con el mar de verdad: la decisión final "
                        "la tomo yo en el pantalán el mismo día, y si no se puede salir, buscamos otro día."),
        "fuente": ("Previsión: AEMET (playa Río Verde – Puerto Banús, Marbella por horas y aguas costeras de "
                   "Málaga). Actualizada {hora}."),
        "cargando": "Cargando la previsión de AEMET…",
        "sin_datos": "Ahora mismo no me llega la previsión de AEMET. Escríbeme y te digo cómo está el mar.",
    },
    "llegar_h2": "Cómo llegar",
    "llegar_p": [
        "Salimos de Puerto José Banús, en Marbella. Cuando reserves, te mando por WhatsApp el pantalán exacto.",
        ("Si vienes en coche, aparca en el parking Cristamar, en la calle Francisco Villalón. Si sales en el barco, "
         "es gratis, y de ahí al barco hay 10 minutos andando."),
    ],
    "mapa": {"puerto": "Puerto José Banús", "parking": "Parking Cristamar", "minutos": "10 min andando",
             "aria": "Plano de Puerto Banús con el parking Cristamar y el camino andando hasta el puerto",
             "fuente": "Plano: © colaboradores de OpenStreetMap (ODbL)"},
    "llegar_enlace": "Abrir el parking en Google Maps",
    "llegar_barco": "Dónde está el barco",
    "buceo_h2": "¿Buceas?",
    "buceo_lead": ("También soy instructor de buceo FEDAS. Te llevo a los puntos de la Senda Azul de Málaga según tu "
                   "nivel y, si nunca has buceado, a tu primer bautizo."),
    "buceo_cta": "Ver los 15 puntos de buceo",
    "buceo_title": "Bucear en Marbella: los puntos de la Senda Azul · Sea With Jose",
    "buceo_description": ("Los 15 puntos de buceo de la Senda Azul de Málaga con su profundidad, nivel y acceso, y "
                          "bautizos y cursos FEDAS con Jose, instructor de buceo en Marbella."),
    "senda": {
        "eyebrow": "Buceo · La Senda Azul",
        "h1": "La Senda Azul, punto por punto",
        "lead": ("La Senda Azul es la guía oficial de buceo de la costa de Málaga: quince inmersiones de Manilva a "
                 "Nerja, cada una con su profundidad, su nivel y lo que vas a ver. Cuatro están a un paso de Puerto "
                 "Banús."),
        "filtros": {"todos": "Todos", "basico": "Básico", "medio": "Medio", "experto": "Experto",
                    "banus": "Cerca de Banús"},
        "campos": {"prof": "Profundidad", "nivel": "Nivel", "acceso": "Acceso", "vis": "Visibilidad"},
        "accesos": {"barco": "en barco", "tierra": "desde la orilla"},
        "niveles": {"basico": "Básico", "medio": "Medio", "experto": "Experto"},
        "visibilidades": {"buena": "buena", "normal": "normal", "media": "media", "regular": "regular", "mala": "mala"},
        "cerca": "Cerca de Banús", "salida": "Puerto Banús", "quiero": "Quiero bucear aquí",
        "msg": "¡Hola Jose! Me gustaría bucear en {sitio}. Mi nivel es: ",
        "fuente": ("Datos: «Málaga sumergida. Guía de buceo de la Senda Azul», Turismo y Planificación Costa del Sol "
                   "(2024). Agua: entre 15 y 23 °C según la época."),
        "aviso": ("Las inmersiones de nivel experto exigen la titulación y la experiencia adecuadas; el Menapier es "
                  "buceo técnico."),
        "linea_aria": "Los puntos de la Senda Azul a lo largo de la costa de Málaga, de Manilva al oeste a Nerja al este",
        "vacio": "Ningún punto cumple ese filtro.",
    },
    "buceo_bloques": [
        ("Tu primera inmersión", "Aguas tranquilas y poco profundas, y yo a tu lado todo el rato. "
                                 "No hace falta experiencia: solo ganas."),
        ("Sácate el título", "Cursos FEDAS · CMAS: desde Buceador 1 Estrella (B1E), con el que buceas acompañado hasta "
                             "25 metros, hasta niveles avanzados y especialidades. Reconocidos en todo el mundo a "
                             "través de CMAS."),
    ],
    "pecio_eyebrow": "Pecio frente a San Pedro Alcántara",
    "pecio_h": "El Galeón: el navío <em>Fernando</em>, 1760",
    "pecio_p": [
        ("Durante décadas todo el mundo lo llamó «el Galeón» y se decía que era francés. En 2026, el Instituto Andaluz "
         "del Patrimonio Histórico resolvió el misterio: es el <em>Fernando</em>, un navío español construido en "
         "Ferrol entre 1750 y 1751 y hundido en 1760."),
        "Sus restos descansan entre ocho y diez metros de profundidad, a 200 metros de la playa: tres siglos de "
        "historia al alcance de cualquier buceador.",
    ],
    "pecio_datos": [("Profundidad", "8–10 m"), ("Nivel", "básico"),
                    ("Qué verás", "cuadernas, lastre y la vida sobre el pecio")],
    "habichuelas_h": "El barco de las Habichuelas, en Punta Carnero",
    "habichuelas_p": ("El <em>Dina</em>, un mercante de 109 metros que embarrancó en un temporal de levante en 1983 "
                      "cargado de conservas de legumbres. Hoy es un arrecife lleno de vida entre 8 y 12 metros."),
    "viajes_h": "Viajes de buceo",
    "viajes_p": ("Cada año organizo viajes en grupo reducido a los grandes destinos del buceo: Maldivas, Filipinas, "
                 "Indonesia. Dime adónde te gustaría ir."),
    "fotos_buceo": {"pulpo": "Un pulpo en el fondo frente a Marbella", "ok": "Dos buceadores haciendo la señal de OK",
                    "tortuga": "Buceando junto a una tortuga verde", "tiburon": "Buceadores observando un tiburón tigre"},
    "buceo_wa": "¡Hola Jose! Me gustaría bucear contigo.",
    "buceo_wa_cta": "Pregunta por el buceo",
    "pesca_h2": "Y si lo tuyo es pescar",
    "pesca_p": ("También organizo salidas de pesca, a fondo o al curricán, por la mañana o por la tarde. Si es tu "
                "primera vez, te enseño."),
    "pesca_cta": "Pregunta por la pesca",
    "pesca_wa": "¡Hola Jose! Me gustaría saber más sobre las salidas de pesca.",
    "faq_h2": "Preguntas",
    "faq": [
        ("¿Cuánto cuesta?", "La compartida, 60 € por persona. La privada, 490 € por el barco entero durante dos horas, "
                            "para hasta 11 personas. Los extras de las privadas van aparte."),
        ("¿Tengo que saber navegar?", "No, el barco lo llevo yo. Si quieres, te enseño a llevar el timón."),
        ("¿Dónde quedamos?", "En Puerto José Banús. Te mando el pantalán exacto por WhatsApp."),
        ("¿Dónde aparco?", "En el parking Cristamar, a 10 minutos andando del barco. Si sales con nosotros, es gratis."),
        ("¿Qué llevo?", "Bañador, toalla, crema solar y gafas de sol."),
        ("¿Y si hace mal tiempo?", "Solo salgo si el mar está bien. Si cancelo por el tiempo, eliges otro día o te "
                                   "devuelvo el dinero."),
        ("¿Puedo cancelar?", "Sí, gratis hasta 24 horas antes en la compartida y 48 horas en la privada."),
        ("¿Qué incluye?", "Agua, refrescos, cerveza, algo de picoteo y gafas y tubo para todos. Nada más que pagar "
                          "a bordo."),
        ("¿Pueden venir niños?", "Claro. Dime sus edades al reservar."),
        ("¿En qué idiomas hablas?", "Español, inglés y ruso."),
    ],
    "final_h2": "¿Te vienes?",
    "final_p": "Reserva tu plaza o escríbeme y te ayudo a elegir.",
    "pie_lugar": "Puerto José Banús, 29660 Marbella (Málaga)",
    "pie_legal": "Aviso legal, reservas y privacidad",
    "pie_creditos": "Fotos: el Petit · Cartografía: EMODnet (CC BY 4.0) y OpenStreetMap (ODbL) · Previsión: AEMET",
    "legal_title": "Aviso legal, reservas y privacidad · Sea With Jose",
    "legal_h1": "Aviso legal, reservas y privacidad",
    "legal": [
        ("Titular", "Sea With Jose es la marca personal de José María Hinojosa Figueira, con domicilio en Marbella "
                    "(Málaga). Contacto: {email} · WhatsApp {tel}."),
        ("Qué hace esta web", "Enseña mis salidas en velero en el Petit y los extras de las salidas privadas, y "
                              "permite reservarlas y pagarlas. También publica la Bitácora del mar, mi revista quincenal, y los "
                              "datos oficiales del tiempo en Marbella."),
        ("Reservas y pagos", "Las salidas se pagan por adelantado con tarjeta a través de Stripe, que procesa el pago: "
                             "esta web no ve ni guarda los datos de tu tarjeta. La reserva queda confirmada cuando te "
                             "escribo por WhatsApp o por correo. Los precios que ves son precios finales. Los extras de "
                             "las privadas se presupuestan y se pagan aparte."),
        ("Cancelaciones", "Puedes cancelar gratis hasta 24 horas antes de una salida compartida, o 48 horas antes de "
                          "una privada, y te devuelvo todo el importe. Si "
                          "cancelo yo por el estado del mar o por seguridad, eliges otro día o la devolución íntegra. "
                          "Al tratarse de una actividad de ocio con fecha concreta, no se aplica el derecho de "
                          "desistimiento de 14 días (artículo 103.l de la Ley General para la Defensa de los "
                          "Consumidores y Usuarios)."),
        ("A bordo", "Por seguridad, el capitán decide la ruta, dónde fondear y si se puede salir o seguir navegando."),
        ("Tus datos", "Si reservas o me escribes, uso tu nombre, tus datos de contacto y los de la reserva solo para "
                      "organizar tu salida y cumplir mis obligaciones fiscales, y los conservo únicamente el tiempo "
                      "obligatorio. Stripe trata los datos del pago como responsable independiente "
                      "(stripe.com/privacy). Puedes pedirme en cualquier momento verlos, corregirlos o borrarlos "
                      "escribiendo a {email}, y reclamar ante la Agencia Española de Protección de Datos (aepd.es)."),
        ("La Bitácora del mar (boletín)", "Si te suscribes a la Bitácora, uso tu correo (y tu nombre, si lo das) solo "
         "para enviarte la revista cada quince días, con la base del consentimiento que das en el formulario y "
         "confirmas por correo (doble confirmación). La lista la guarda Brevo (Sendinblue SAS, Francia, UE) como "
         "encargado del tratamiento; Brevo registra si se abre cada número, solo para medir el boletín. Cada número "
         "trae un enlace para darte de baja y borro tus datos cuando te das de baja. También puedes pedirme verlos, "
         "corregirlos o borrarlos en {email}."),
        ("Cookies", "Esta web no usa cookies ni herramientas de analítica. Mientras reservas, tu navegador guarda los "
                    "datos de la reserva para enseñártelos al volver de la página de pago. Las tipografías y las "
                    "imágenes se sirven desde la propia web."),
        ("Terceros", "La web está alojada en GitHub Pages (GitHub Inc.), que puede registrar las direcciones IP de las "
                     "visitas por seguridad. Los enlaces de WhatsApp, Instagram y Google Maps te llevan a "
                     "esos servicios, que tienen sus propias políticas de privacidad."),
        ("Créditos", "Batimetría: EMODnet Bathymetry Consortium, CC BY 4.0. Plano de Puerto Banús: © colaboradores de "
                     "OpenStreetMap, ODbL. Previsiones y datos del tiempo en Marbella: información elaborada por la Agencia Estatal de Meteorología "
                     "(AEMET)."),
    ],
    "gracias": {"title": "Reserva recibida · Sea With Jose", "h1": "Reserva recibida",
                "p": "Gracias. En cuanto vea el pago, te confirmo la salida por WhatsApp.",
                "resumen": "Tu salida", "wa": "Escríbeme por WhatsApp", "volver": "Volver a la web",
                "sin": ("No encuentro los datos de tu reserva en este navegador, pero no te preocupes: Stripe te ha "
                        "mandado el recibo por correo. Escríbeme y lo vemos.")},
    "volver": "Volver al inicio",
    "e404_h1": "Esta página está fuera de la carta",
    "e404_p": "Puede que la dirección esté mal escrita o que la página haya cambiado de sitio.",
    "datos": {
        "title": "Datos oficiales del tiempo en Marbella, hora a hora · Sea With Jose",
        "description": ("Viento, rachas, dirección, lluvia, temperatura y humedad medidos por AEMET en el puerto de Marbella, "
                        "hora a hora y con el histórico desde 2004. Gráficas interactivas y cruce de variables."),
        "eyebrow": "Datos oficiales · AEMET",
        "h1": "El tiempo en Marbella, dato a dato",
        "lead": ("Lo que miden las estaciones oficiales de AEMET en Marbella: viento, rachas, dirección, lluvia, temperatura "
                 "y humedad. Por defecto ves la última semana; puedes ampliar hasta todo el histórico y cruzar unas "
                 "variables con otras."),
        "ahora_h": "Ahora mismo",
        "serie_h": "Evolución",
        "var1": "Variable", "var2": "Comparar con", "ninguna": "Ninguna",
        "rangos": {"7": "7 días", "30": "30 días", "365": "1 año", "todo": "Todo"},
        "zoom": "Quitar el zoom", "csv": "Descargar CSV",
        "zoom_ayuda": "Rueda del ratón o pellizco para acercar; arrastra para moverte.",
        "cruce_h": "Cruzar variables",
        "cruce_p": ("Elige dos variables y mira cómo se relacionan en el periodo elegido arriba. Si una es la dirección "
                    "del viento, verás la media de la otra según de dónde sopla."),
        "eje_x": "Variable X", "eje_y": "Variable Y", "estacion": "Estación",
        "estaciones": {"6076X": "Marbella, Puerto (6076X)", "6083X": "Marbella (6083X)"},
        "nota": ("Datos por horas desde el 14 de octubre de 2026, cuando empecé a guardarlos (AEMET solo publica las "
                 "últimas 24 horas); antes, un valor por día. El viento se mide a 10 m de altura."),
        "fuente": ("Fuente: Agencia Estatal de Meteorología (AEMET), observación convencional y valores climatológicos "
                   "diarios de sus estaciones en el término municipal de Marbella. © AEMET."),
        "error": "No he podido cargar los datos. Prueba de nuevo en unos minutos.",
        "js": {"vars": {"viento": "Viento medio", "racha": "Racha máxima", "dir": "Dirección del viento",
                        "lluvia": "Lluvia", "temp": "Temperatura del aire", "humedad": "Humedad"},
               "rumbos": ["N", "NE", "E", "SE", "S", "SO", "O", "NO"],
               "diario": "media del día", "media": "Media de", "actualizado": "Última medida:",
               "ultima_hora": "en la última hora",
               "cruce_rumbo": "Media por rumbo con {n} pares de datos.",
               "cruce_r": "Correlación r = {r} ({lectura}), con {n} pares de datos.",
               "fuerte": "relación fuerte", "moderada": "relación moderada", "debil": "relación débil o nula",
               "pocos": "No hay suficientes datos en este periodo."},
    },
    "revista": {
        "title": "Bitácora del mar: revista quincenal gratuita sobre el mar · Sea With Jose",
        "description": ("Cada quince días, en tu correo: la temperatura del agua en Marbella y lo más interesante del buceo, "
                        "la vela, la pesca, los viajes por mar y el océano. La escribe Jose, capitán y oceanógrafo."),
        "eyebrow": "Gratis · cada quince días",
        "h1": "Bitácora del mar",
        "lead": ("Cada quince días envío una revista corta sobre el mar: cómo ha estado el agua en Marbella y las mejores "
                 "noticias de buceo, vela, pesca y viajes por mar, elegidas y explicadas por mí."),
        "ejes_h": "Qué trae cada número",
        "ejes": [("mar", "El mar en la quincena", "Temperatura del agua, oleaje y viento frente a Puerto Banús, y la luna para pescar."),
                 ("buceo", "Buceo", "Inmersiones, fauna, cursos y lo que pasa bajo el agua."),
                 ("vela", "Vela y barcos", "Regatas, barcos, náutica y novedades de los puertos."),
                 ("pesca", "Pesca", "Temporadas, especies y normas de la pesca recreativa."),
                 ("viajes", "Viajes por mar", "Destinos para bucear y navegar, cerca y lejos."),
                 ("ciencia", "Noticias del océano", "Descubrimientos, ballenas, tiburones y las historias que dan que hablar.")],
        "susc_h": "Recíbela en tu correo",
        "susc_p": "Elige el idioma. Te llegará un correo para confirmar y puedes darte de baja con un clic.",
        "susc_es": "Suscribirme en español",
        "susc_en": "Suscribirme en inglés",
        "susc_sin": "La suscripción se abre muy pronto. Mientras tanto, escríbeme y te apunto.",
        "susc_wa": "¡Hola Jose! Me gustaría recibir la Bitácora del mar.",
        "archivo_h": "Números publicados",
        "archivo_vacio": "El primer número está en camino.",
        "archivo_idioma": {"es": "Español", "en": "Inglés"},
        "privacidad": ("Tu correo solo se usa para enviarte la Bitácora, a través de Brevo (Sendinblue SAS, UE). "
                       "Puedes darte de baja cuando quieras desde cualquier número."),
        "estado": {"pendiente": ("Revisa tu correo", "Te he enviado un mensaje con un enlace para confirmar la suscripción."),
                   "ok": ("¡Ya estás dentro!", "El próximo número de la Bitácora te llegará en unos días.")},
    },
}

# ───────────────────────────────── RUSO ─────────────────────────────────
T["ru"] = {
    "nombre_idioma": "Русский", "corto": "RU", "og_locale": "ru_RU",
    "title": "Прогулки под парусом из Пуэрто-Бануса, Марбелья: дельфины и снорклинг · Sea With Jose",
    "description": ("Два часа под парусом из Пуэрто-Бануса с Хосе, капитаном яхты и океанографом: дельфины, купание "
                    "с маской и трубкой, напитки и закуски включены. Групповая прогулка 60 € с человека, "
                    "индивидуальная 490 € за яхту, до 11 гостей."),
    "saltar": "Перейти к содержанию",
    "nav": {"precios": "Цены", "salida": "Прогулка", "barco": "Яхта",
            "llegar": "Как добраться", "revista": "Журнал"},
    "menu": "Меню", "whatsapp_corto": "WhatsApp", "reservar_corto": "Забронировать",
    "wa_hola": "Здравствуйте, Хосе! Хочу выйти в море на «Пти».",
    "banderas_aria": "Sea With Jose, написанное флагами Международного свода сигналов",
    "hero_h1": "Прогулки под парусом из Пуэрто-Бануса",
    "hero_lead": ("Меня зовут Хосе, я капитан яхты и океанограф. Два часа мы ходим под парусом вдоль побережья "
                  "Марбельи на «Пти», 12-метровой парусной яхте. Купаемся вдали от пляжа, а если повезёт, видим "
                  "дельфинов."),
    "hero_idiomas": "Говорю по-русски, по-английски и по-испански.",
    "hero_precios": [("Групповая", "60 €", "с человека"), ("Индивидуальная", "490 €", "яхта, 2 часа")],
    "hero_cta": "Забронировать",
    "hero_cta2": "Написать в WhatsApp",
    "hero_foto_alt": "«Пти» на якоре на закате",
    "precios_h2": "Цены",
    "opciones": {
        "compartida": {"titulo": "Групповая прогулка", "precio": "60 €", "unidad": "с человека",
                       "puntos": ["Два часа под парусом, не больше 11 человек", "Вода, газировка, пиво и закуски",
                                  "Купание с маской и трубкой, и я расскажу, кто живёт на дне",
                                  "Можно постоять за штурвалом", "Бесплатная отмена не позднее чем за 24 часа"],
                       "cta": "Забронировать место"},
        "privada": {"titulo": "Индивидуальная прогулка", "precio": "490 €", "unidad": "вся яхта, 2 часа",
                    "puntos": ["Только ваша компания, до 11 человек", "Время выбираете вы, в том числе закат",
                               "Вода, газировка, пиво и закуски", "Купание с маской и трубкой",
                               "Можно добавить паэлью, коктейли, украшения или гидроцикл",
                               "Бесплатная отмена не позднее чем за 48 часов"],
                    "cta": "Забронировать яхту"},
    },
    "precios_nota": "На борту больше ничего платить не нужно. Возьмите купальник, полотенце и солнцезащитный крем.",
    "capitan": {"titulo": "Ваш капитан: Хосе", "creds": ["Капитан яхты", "Океанограф", "Инструктор по дайвингу FEDAS"],
                "enlace": "Обо мне"},
    "resenas_h2": "Отзывы",
    "fotos_alt": {"petit-delfines": "Дельфины выпрыгивают перед парусной яхтой",
                  "petit-banera": "Кокпит «Пти» на ходу",
                  "petit-proa": "Тиковая палуба «Пти»"},
    "salida_h2": "Как проходит прогулка",
    "pasos": [
        ("0:00", "Встречаемся на причале в Пуэрто-Банусе за 15 минут до выхода. Точное место пришлю в WhatsApp."),
        ("0:15", "Выходим из порта на моторе и сразу за входом поднимаем паруса. Куда пойдём, на запад или на восток, решает ветер. Хотите, вставайте за штурвал."),
        ("1:00", "В открытом море, вдали от пляжа, останавливаемся и купаемся с маской и трубкой."),
        ("2:00", "Под парусом возвращаемся в Банус, замыкая круг."),
    ],
    "salida_nota": "Это обычный маршрут, остальное решают ветер и море.",
    "carta_aria": ("Морская карта побережья между Сан-Педро-Алькантара и Марбельей с обычным маршрутом прогулки из "
                   "Пуэрто-Бануса"),
    "carta": {"banus": "Пуэрто-Хосе-Банус", "sanpedro": "Сан-Педро-Алькантара", "marbella": "Марбелья",
              "bano": "Купание", "rioverde": "Рио-Верде", "alboran": "Море Альборан", "oeste": "W",
              "norte": "N", "ruta": "По ветру"},
    "reserva_h2": "Бронирование",
    "reserva_intro": "Выберите день, время и сколько вас будет. Я подтвержу в WhatsApp.",
    "form": {
        "tipo": "Прогулка", "tipos": {"compartida": "Групповая", "privada": "Индивидуальная"},
        "tipos_sub": {"compartida": "60 € с человека", "privada": "490 € за яхту"},
        "fecha": "День", "hora": "Время", "atardecer": "Закат",
        "personas": "Гостей", "menos": "На одного меньше", "mas": "На одного больше", "max": "Не больше 11",
        "nombre": "Ваше имя", "nombre_ph": "",
        "extras": "Дополнительно к индивидуальной прогулке",
        "extras_nota": "Дополнительные услуги оплачиваются отдельно. Цену пришлю в WhatsApp до прогулки.",
        "otra": "Что-то ещё?",
        "total": "Итого", "detalle_compartida": "{n} × 60 €", "detalle_privada": "Вся яхта, 2 часа",
        "pagar": "Оплатить {total}", "whatsapp": "Забронировать через WhatsApp",
        "seguro": "Оплату проводит Stripe. Данные карты не проходят через этот сайт.",
        "politica": ("Бесплатная отмена не позднее чем за 24 часа для групповой прогулки и за 48 часов для "
                     "индивидуальной. Если море не позволяет выйти, перенесём день или я верну деньги."),
        "sin_pago": "Оплата картой заработает через несколько дней. Пока бронируйте через WhatsApp, я сразу подтвержу.",
        "falta_fecha": "Выберите день.", "falta_hora": "Выберите время.", "falta_nombre": "Напишите своё имя.",
        "prevision": "Прогноз AEMET на это время: парус {n}/10 ({banda})",
        "msg_inicio": "Здравствуйте, Хосе! Хочу забронировать прогулку на «Пти».", "msg_tipo": "Прогулка",
        "msg_fecha": "День", "msg_hora": "Время", "msg_personas": "Гостей", "msg_extras": "Дополнительно",
        "msg_nombre": "Имя", "msg_total": "Итого", "msg_ref": "Номер брони", "msg_pagado": "Я только что оплатил(а) на сайте.",
    },
    "resumen": {"titulo": "Ваша бронь", "salida": "Прогулка", "fecha": "День", "hora": "Время", "pax": "Гостей",
                "extras": "Дополнительно", "total": "Итого"},
    "extras_h2": "Дополнительно к индивидуальным прогулкам",
    "extras_intro": ("Для дня рождения, предложения руки и сердца, девичника или просто так. Скажите, что вы хотите, и "
                     "я всё подготовлю."),
    "extras": [
        {"id": "buffet", "titulo": "Фуршет на борту", "texto": "Закуски, фрукты и что-нибудь сладкое на всех."},
        {"id": "paella", "titulo": "Паэлья", "texto": "Чтобы пообедать на якоре."},
        {"id": "cocteles", "titulo": "Коктейли", "texto": "И кава, чтобы поднять бокалы."},
        {"id": "tarta", "titulo": "Торт", "texto": "Ко дню рождения или к празднику."},
        {"id": "decoracion", "titulo": "Украшения", "texto": "Шары, цветы и флажки, как вам нравится."},
        {"id": "moto", "titulo": "Гидроцикл", "texto": "Прокатиться во время прогулки."},
        {"id": "otra", "titulo": "Другая идея", "texto": "Музыка, фотограф, сюрприз… Просто скажите."},
    ],
    "extras_precio": "по запросу",
    "extras_cta": "Забронировать индивидуальную прогулку",
    "barco_h2": "«Пти»",
    "barco_sub": "Её зовут P’tit Mousse, но все называют её просто «Пти».",
    "barco_p": [
        "Это Jeanneau Sun Odyssey 42 с центральным кокпитом: 12,3 метра, тиковая палуба и бимини, которое даёт тень.",
        "Яхта устойчивая и удобная, на борту помещаются одиннадцать гостей и капитан.",
    ],
    "barco_datos": [("Модель", "Jeanneau Sun Odyssey 42 CC"), ("Длина", "12,3 м"), ("Гостей", "11 + капитан"),
                    ("Стоянка", "Пуэрто-Хосе-Банус")],
    "galeria": {"petit-azul": "«Пти» у причала под синим небом",
                "petit-pantalan": "«Пти» у понтона",
                "petit-cubierta": "Палуба, вид с носа",
                "petit-bimini": "Бимини над кокпитом",
                "petit-fondeado": "«Пти» на якоре"},
    "video_alt": "«Пти» идёт по спокойному морю", "video_pausa": "Поставить видео на паузу",
    "video_play": "Воспроизвести видео",
    "jose_h2": "Кто вас повезёт",
    "jose_p": [
        ("Я изучал океанографию в Университете Кадиса, у меня диплом капитана яхты и инструктора по дайвингу FEDAS. "
         "Последние пять сезонов я работаю шкипером на парусных яхтах, катерах и рыболовных лодках в Марбелье и "
         "Пуэрто-Банусе."),
        ("Поэтому я знаю, где вода остаётся спокойной, когда поднимается ветер, где обычно встречаются дельфины и кто "
         "живёт на дне под яхтой. Расскажу обо всём по-русски, по-английски или по-испански."),
    ],
    "jose_foto": "Хосе на лодке перед погружением",
    "cuaderno": "Мой судовой журнал",
    "bitacora": [
        ("2016", "Первые погружения. Десять лет спустя я всё так же возвращаюсь под воду."),
        ("2022", "Первый сезон шкипером чартеров в Марбелье."),
        ("2023", "Инструктор по дайвингу (FEDAS · CMAS) и руководитель чартерного флота."),
        ("2025", "Парусные выходы к дельфинам и рыболовные чартеры."),
        ("2026", "Диплом капитана яхты."),
    ],
    "mar": {
        "eyebrow": "Море сейчас",
        "h2": "Какое сегодня море?",
        "intro": ("Три веб-камеры на побережье Марбельи и моя оценка от 1 до 10 для паруса, дайвинга и рыбалки — "
                  "по официальному прогнозу AEMET."),
        "camaras_h": "Веб-камеры онлайн", "en_directo": "Онлайн", "ver": "Смотреть онлайн",
        "camaras_nota": "Камеры принадлежат их владельцам и открываются на их сайтах.",
        "camaras": [
            {"nombre": "Яхтенная гавань Марбельи", "que": "Вид на марину в центре города",
             "fuente": "SkylineWebcams", "url": "https://www.skylinewebcams.com/ru/webcam/espana/andalucia/malaga/marbella-puerto-deportivo.html"},
            {"nombre": "Порт и набережная", "que": "Вид на порт и набережную Марбельи",
             "fuente": "SkylineWebcams", "url": "https://www.skylinewebcams.com/ru/webcam/espana/andalucia/malaga/marbella.html"},
            {"nombre": "Пляж Эль-Кабле и Ла-Бахадилья", "que": "Городской пляж и рыбацкая гавань",
             "fuente": "meteo365", "url": "https://meteo365.es/livecams/marbella.php"},
        ],
        "notas_h": "Оценка от 1 до 10", "dias_aria": "Выберите день", "hoy": "Сегодня", "manana": "Завтра",
        "actividades": {"navegar": "Парус", "bucear": "Дайвинг", "pescar": "Рыбалка"},
        "bandas": ["Лучше в другой день", "Плохо", "Так себе", "Хорошо", "Отлично"],
        "motivos": {
            "buen_viento": "Ветер как раз для паруса.", "mar_tranquila": "Спокойное море.",
            "sin_viento": "Штиль: больше купания, чем паруса.", "poco_viento": "Слабый ветер: идём медленно.",
            "viento_fresco": "Свежий ветер: яхта идёт с креном.", "viento": "Небольшой ветер.",
            "viento_fuerte": "Слишком сильный ветер.", "rachas": "Сильные порывы.", "marejadilla": "Небольшая волна.",
            "marejada": "Заметная волна.", "mar_fuerte": "Сильное волнение.", "mar_de_fondo": "Зыбь.",
            "lluvia": "Вероятен дождь.", "tormenta": "Возможна гроза.",
            "niebla": "Туман или дымка у берега.", "agua_fria": "Холодная вода: нужен толстый гидрокостюм.",
            "aviso": "Предупреждение AEMET для побережья.", "temporal": "Шторм: остаёмся в порту.",
        },
        "pasado": "прошло", "tramo": "ч",
        "tabla": {"viento": "Ветер", "racha": "Порывы", "mar": "Море", "cielo": "Небо", "lluvia": "Дождь",
                  "agua": "Вода", "fondo": "зыбь"},
        "mar_clases": ["рябь", "слабое волнение, до 0,5 м", "лёгкое волнение, 0,5–1,25 м",
                       "умеренное волнение, 1,25–2,5 м", "сильное волнение, больше 2,5 м"],
        "mar_cortos": ["рябь", "слабое волнение", "лёгкое волнение", "умеренное волнение", "сильное волнение"],
        "cielos": {"despejado": "ясно", "poco_nuboso": "малооблачно", "intervalos": "переменная облачность",
                   "nuboso": "облачно", "cubierto": "пасмурно", "nubes_altas": "перистые облака", "lluvia": "дождь",
                   "lluvia_escasa": "небольшой дождь", "tormenta": "гроза", "niebla": "туман", "bruma": "дымка",
                   "calima": "пыльная мгла"},
        "rumbos": {"N": "С", "NE": "СВ", "E": "В", "SE": "ЮВ", "S": "Ю", "SO": "ЮЗ", "O": "З", "NO": "СЗ",
                   "C": "штиль"},
        "kmh": "км/ч",
        "costera_h": "Прибрежный прогноз AEMET · воды у побережья Малаги",
        "costera_resumen": "Ветер по шкале Бофорта: {f}; море: {m}.", "costera_a": " или ",
        "costera_texto": "Официальный текст на испанском:", "costera_hasta": "Действует до {fin}.",
        "aviso_h": "Предупреждение AEMET для побережья Малаги",
        "como_h": "Как я ставлю оценку",
        "como": [
            ("Парус", "лучше всего ветер 13–28 км/ч (3–4 балла) и спокойное море. При ветре слабее 5 км/ч идём "
                      "на моторе; от 34 км/ч или при заметной волне оценка резко падает."),
            ("Дайвинг", "главное — состояние моря: до слабого волнения — хорошо, лёгкое волнение — так себе, "
                        "сильнее — не ныряем. Ветер больше 20 км/ч и зыбь снижают оценку."),
            ("Рыбалка", "волнение не больше слабого и ветер до 22 км/ч."),
            ("Для всех трёх", "гроза, туман и дождь снижают оценку. При предупреждении AEMET или шторме оценка "
                              "не выше 2."),
        ],
        "aviso_legal": ("Это ориентир по прогнозу, а не по реальному морю: окончательное решение я принимаю на "
                        "причале в день выхода, и если выйти нельзя, подберём другой день."),
        "fuente": ("Прогноз: AEMET (пляж Рио-Верде – Пуэрто-Банус, Марбелья по часам и прибрежные воды Малаги). "
                   "Обновлено {hora}."),
        "cargando": "Загружаю прогноз AEMET…",
        "sin_datos": "Сейчас прогноз AEMET недоступен. Напишите мне — расскажу, какое море.",
    },
    "llegar_h2": "Как добраться",
    "llegar_p": [
        "Мы выходим из порта Пуэрто-Хосе-Банус в Марбелье. После бронирования я пришлю в WhatsApp точный причал.",
        ("Если вы на машине, оставьте её на парковке Cristamar на улице Франсиско Вильялон. Для гостей яхты она "
         "бесплатная, а до яхты оттуда 10 минут пешком."),
    ],
    "mapa": {"puerto": "Пуэрто-Хосе-Банус", "parking": "Парковка Cristamar", "minutos": "10 минут пешком",
             "aria": "Карта Пуэрто-Бануса с парковкой Cristamar и пешим путём до порта",
             "fuente": "Карта: © участники OpenStreetMap (ODbL)"},
    "llegar_enlace": "Открыть парковку в Google Картах",
    "llegar_barco": "Где стоит яхта",
    "buceo_h2": "Ныряете?",
    "buceo_lead": ("Я ещё и инструктор по дайвингу FEDAS. Отвезу вас к точкам «Голубой тропы» Малаги под ваш уровень, "
                   "а если вы никогда не ныряли, на первое пробное погружение."),
    "buceo_cta": "Все 15 точек погружения",
    "buceo_title": "Дайвинг в Марбелье: точки «Голубой тропы» · Sea With Jose",
    "buceo_description": ("15 точек погружения «Голубой тропы» Малаги с глубиной, уровнем и доступом, а также пробные "
                          "погружения и курсы FEDAS с Хосе, инструктором по дайвингу в Марбелье."),
    "senda": {
        "eyebrow": "Дайвинг · «Голубая тропа»",
        "h1": "«Голубая тропа» Малаги: точка за точкой",
        "lead": ("Senda Azul («Голубая тропа») — официальный путеводитель по дайвингу на побережье Малаги: пятнадцать "
                 "погружений от Манильвы до Нерхи, у каждого — глубина, уровень и то, что вы увидите. Четыре из них — "
                 "совсем рядом с Пуэрто-Банусом."),
        "filtros": {"todos": "Все", "basico": "Начальный", "medio": "Средний", "experto": "Продвинутый",
                    "banus": "Рядом с Банусом"},
        "campos": {"prof": "Глубина", "nivel": "Уровень", "acceso": "Доступ", "vis": "Видимость"},
        "accesos": {"barco": "с лодки", "tierra": "с берега"},
        "niveles": {"basico": "Начальный", "medio": "Средний", "experto": "Продвинутый"},
        "visibilidades": {"buena": "хорошая", "normal": "нормальная", "media": "средняя", "regular": "посредственная",
                          "mala": "плохая"},
        "cerca": "Рядом с Банусом", "salida": "Пуэрто-Банус", "quiero": "Хочу нырнуть здесь",
        "msg": "Здравствуйте, Хосе! Хочу нырнуть в точке {sitio}. Мой уровень: ",
        "fuente": ("Данные: «Málaga sumergida. Guía de buceo de la Senda Azul», Turismo y Planificación Costa del Sol "
                   "(2024). Вода: 15–23 °C в зависимости от сезона."),
        "aviso": ("Для погружений продвинутого уровня нужны соответствующий сертификат и опыт; «Менапье» — "
                  "техническое погружение."),
        "linea_aria": "Точки «Голубой тропы» вдоль побережья Малаги — от Манильвы на западе до Нерхи на востоке",
        "vacio": "Нет точек, подходящих под этот фильтр.",
    },
    "buceo_bloques": [
        ("Первое погружение", "Спокойная неглубокая вода, и я всё время рядом с вами. Опыт не нужен — только "
                              "любопытство."),
        ("Получите сертификат", "Курсы FEDAS · CMAS: от «Дайвера одной звезды» (B1E), с которым можно погружаться с "
                                "напарником до 25 метров, до продвинутых уровней и специализаций. Сертификаты "
                                "признаются во всём мире через CMAS."),
    ],
    "pecio_eyebrow": "Затонувший корабль у Сан-Педро-Алькантара",
    "pecio_h": "«Галеон»: линейный корабль <em>«Фернандо»</em>, 1760 год",
    "pecio_p": [
        ("Десятилетиями все называли его «Галеоном» и считали французским. В 2026 году Андалусский институт "
         "исторического наследия раскрыл тайну: это <em>«Фернандо»</em> — испанский линейный корабль, построенный в "
         "Ферроле в 1750–1751 годах и погибший в 1760-м."),
        "Его остатки лежат на глубине восьми–десяти метров, в 200 метрах от пляжа: три века истории, доступные "
        "любому дайверу.",
    ],
    "pecio_datos": [("Глубина", "8–10 м"), ("Уровень", "начальный"),
                    ("Что увидите", "шпангоуты, балласт и жизнь на корабле")],
    "habichuelas_h": "«Корабль с фасолью» у Пунта-Карнеро",
    "habichuelas_p": ("<em>«Дина»</em> — 109-метровое грузовое судно, севшее на мель во время восточного шторма в 1983 "
                      "году с грузом консервированной фасоли. Сегодня это риф, полный жизни, на глубине от 8 до 12 "
                      "метров."),
    "viajes_h": "Дайв-туры",
    "viajes_p": ("Каждый год я вожу небольшие группы к великим дайв-направлениям мира: Мальдивы, Филиппины, Индонезия. "
                 "Расскажите, куда хотите поехать в следующий раз."),
    "fotos_buceo": {"pulpo": "Осьминог на дне у берегов Марбельи", "ok": "Два дайвера показывают знак «всё в порядке»",
                    "tortuga": "Погружение рядом с зелёной черепахой",
                    "tiburon": "Дайверы наблюдают за тигровой акулой"},
    "buceo_wa": "Здравствуйте, Хосе! Хочу понырять с вами.",
    "buceo_wa_cta": "Спросить о дайвинге",
    "pesca_h2": "А если вам больше по душе рыбалка",
    "pesca_p": ("Я также организую морскую рыбалку, донную или троллингом, утром или после обеда. Если вы рыбачите "
                "впервые, всё покажу."),
    "pesca_cta": "Спросить о рыбалке",
    "pesca_wa": "Здравствуйте, Хосе! Хотел(а) бы узнать подробнее о морской рыбалке.",
    "faq_h2": "Вопросы",
    "faq": [
        ("Сколько это стоит?", "Групповая прогулка стоит 60 € с человека. Индивидуальная, 490 € за всю яхту на два "
                               "часа, до 11 человек. Дополнительные услуги оплачиваются отдельно."),
        ("Нужно ли уметь ходить под парусом?", "Нет, яхтой управляю я. Если захотите, научу держать штурвал."),
        ("Где встречаемся?", "В Пуэрто-Хосе-Банусе. Точный причал пришлю в WhatsApp."),
        ("Где оставить машину?", "На парковке Cristamar, в 10 минутах пешком от яхты. Для гостей яхты она бесплатная."),
        ("Что взять с собой?", "Купальник, полотенце, солнцезащитный крем и солнечные очки."),
        ("А если погода плохая?", "Я выхожу в море, только когда оно спокойное. Если я отменю прогулку из-за погоды, "
                                  "выбирайте другой день или полный возврат денег."),
        ("Можно ли отменить бронь?", "Да, бесплатно не позднее чем за 24 часа для групповой прогулки и за 48 часов "
                                     "для индивидуальной."),
        ("Что включено?", "Вода, газировка, пиво, закуски, а также маска и трубка для каждого. На борту больше ничего "
                          "платить не нужно."),
        ("Можно ли с детьми?", "Конечно. Укажите их возраст при бронировании."),
        ("На каких языках вы говорите?", "На русском, английском и испанском."),
    ],
    "final_h2": "До встречи на борту?",
    "final_p": "Забронируйте место или напишите мне, я помогу выбрать.",
    "pie_lugar": "Пуэрто-Хосе-Банус, 29660 Марбелья (Малага), Испания",
    "pie_legal": "Правовая информация, бронирование и конфиденциальность",
    "pie_creditos": "Фото: «Пти» · Карты: EMODnet (CC BY 4.0) и OpenStreetMap (ODbL) · Прогноз: AEMET",
    "legal_title": "Правовая информация, бронирование и конфиденциальность · Sea With Jose",
    "legal_h1": "Правовая информация, бронирование и конфиденциальность",
    "legal": [
        ("Владелец сайта", "Sea With Jose, личный бренд Хосе Марии Инохосы Фигейры (José María Hinojosa Figueira), "
                           "Марбелья (Малага, Испания). Контакты: {email} · WhatsApp {tel}."),
        ("Назначение сайта", "Сайт рассказывает о прогулках под парусом на «Пти» и дополнительных услугах для "
                             "индивидуальных прогулок и позволяет забронировать и оплатить их. Здесь также выходит «Морской "
                             "журнал» и публикуются официальные данные о погоде в Марбелье."),
        ("Бронирование и оплата", "Прогулки оплачиваются заранее картой через Stripe, который проводит платёж: этот "
                                  "сайт не видит и не хранит данные вашей карты. Бронь подтверждается, когда я пишу вам "
                                  "в WhatsApp или по почте. Указанные цены окончательные. Дополнительные услуги для "
                                  "индивидуальных прогулок оцениваются и оплачиваются отдельно."),
        ("Отмена", "Вы можете бесплатно отменить бронь не позднее чем за 24 часа до групповой прогулки или за 48 часов "
                   "до индивидуальной, и я верну всю сумму. "
                   "Если прогулку отменяю я из-за состояния моря или по соображениям безопасности, вы выбираете "
                   "другой день или полный возврат. Поскольку это досуговая услуга на конкретную дату, 14-дневное "
                   "право на отказ не применяется (статья 103.l испанского закона о защите прав потребителей)."),
        ("На борту", "Ради безопасности маршрут, место якорной стоянки и возможность выйти в море или продолжить "
                     "прогулку определяет капитан."),
        ("Ваши данные", "Если вы бронируете или пишете мне, я использую ваше имя, контакты и данные брони только для "
                        "организации прогулки и выполнения налоговых обязательств и храню их только в течение "
                        "обязательного срока. Stripe обрабатывает платёжные данные как независимый оператор "
                        "(stripe.com/privacy). В любой момент вы можете попросить показать, исправить или удалить ваши "
                        "данные, написав на {email}, а также подать жалобу в Испанское агентство по защите данных "
                        "(aepd.es)."),
        ("Морской журнал (рассылка)", "Если вы подписались на журнал, я использую ваш email (и имя, если вы его "
         "указали) только для отправки журнала раз в две недели, на основании согласия, которое вы даёте в форме и "
         "подтверждаете по почте (двойное подтверждение). Список хранит Brevo (Sendinblue SAS, Франция, ЕС) как "
         "обработчик данных; Brevo отмечает, открыт ли номер, только для статистики рассылки. В каждом номере есть "
         "ссылка для отписки, и после отписки я удаляю ваши данные. Также можно попросить показать, исправить или "
         "удалить их по адресу {email}."),
        ("Cookies", "Сайт не использует cookies и аналитику. Пока вы бронируете, браузер хранит данные брони, чтобы "
                    "показать их вам после возвращения со страницы оплаты. Шрифты и изображения загружаются с самого "
                    "сайта."),
        ("Третьи лица", "Сайт размещён на GitHub Pages (GitHub Inc.), который может записывать IP-адреса посетителей "
                        "в целях безопасности. Ссылки на WhatsApp, Instagram и Google Карты ведут на эти "
                        "сервисы, у которых свои правила конфиденциальности."),
        ("Источники", "Батиметрия: EMODnet Bathymetry Consortium, CC BY 4.0. Карта Пуэрто-Бануса: © участники "
                      "OpenStreetMap, ODbL. Прогнозы: информация Государственного метеорологического агентства Испании "
                      "(AEMET)."),
    ],
    "gracias": {"title": "Бронь получена · Sea With Jose", "h1": "Бронь получена",
                "p": "Спасибо! Как только я увижу оплату, подтвержу прогулку в WhatsApp.",
                "resumen": "Ваша прогулка", "wa": "Написать мне в WhatsApp", "volver": "Вернуться на сайт",
                "sin": ("Я не нахожу данных вашей брони в этом браузере, но не волнуйтесь: Stripe отправил вам чек по "
                        "почте. Напишите мне, и мы всё уладим.")},
    "volver": "На главную",
    "e404_h1": "Этой страницы нет на карте",
    "e404_p": "Возможно, адрес набран с ошибкой или страница переехала.",
    "datos": {
        "title": "Официальные данные о погоде в Марбелье по часам · Sea With Jose",
        "description": ("Ветер, порывы, направление, осадки, температура и влажность по данным AEMET в порту Марбельи, "
                        "по часам и с архивом с 2004 года. Интерактивные графики и сравнение показателей."),
        "eyebrow": "Официальные данные · AEMET",
        "h1": "Погода в Марбелье: все измерения",
        "lead": ("Что измеряют официальные станции AEMET в Марбелье: ветер, порывы, направление, осадки, температуру и "
                 "влажность. Сначала видна последняя неделя; можно открыть весь архив и сравнить показатели между собой."),
        "ahora_h": "Сейчас",
        "serie_h": "Динамика",
        "var1": "Показатель", "var2": "Сравнить с", "ninguna": "Нет",
        "rangos": {"7": "7 дней", "30": "30 дней", "365": "1 год", "todo": "Всё"},
        "zoom": "Сбросить масштаб", "csv": "Скачать CSV",
        "zoom_ayuda": "Колесо мыши или щипок — масштаб; перетаскивание — сдвиг.",
        "cruce_h": "Сравнить показатели",
        "cruce_p": ("Выберите два показателя и посмотрите, как они связаны за выбранный выше период. Если один из них — "
                    "направление ветра, вы увидите среднее значение другого по направлениям."),
        "eje_x": "Показатель X", "eje_y": "Показатель Y", "estacion": "Станция",
        "estaciones": {"6076X": "Марбелья, порт (6076X)", "6083X": "Марбелья (6083X)"},
        "nota": ("Почасовые данные с 14 октября 2026 года, когда я начал их сохранять (AEMET публикует только последние "
                 "24 часа); раньше — одно значение в день. Ветер измеряется на высоте 10 м."),
        "fuente": ("Источник: Государственное метеорологическое агентство Испании (AEMET), наблюдения и суточные "
                   "климатические данные станций в муниципалитете Марбелья. © AEMET."),
        "error": "Не удалось загрузить данные. Попробуйте через несколько минут.",
        "js": {"vars": {"viento": "Средний ветер", "racha": "Макс. порыв", "dir": "Направление ветра",
                        "lluvia": "Осадки", "temp": "Температура воздуха", "humedad": "Влажность"},
               "rumbos": ["С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"],
               "diario": "среднее за день", "media": "Среднее:", "actualizado": "Последнее измерение:",
               "ultima_hora": "за последний час",
               "cruce_rumbo": "Среднее по направлениям, пар данных: {n}.",
               "cruce_r": "Корреляция r = {r} ({lectura}), пар данных: {n}.",
               "fuerte": "сильная связь", "moderada": "умеренная связь", "debil": "слабая или нет",
               "pocos": "Недостаточно данных за этот период."},
    },
    "revista": {
        "title": "Морской журнал: бесплатная рассылка раз в две недели · Sea With Jose",
        "description": ("Раз в две недели на почту: температура воды в Марбелье и самое интересное о дайвинге, парусе, "
                        "рыбалке, морских путешествиях и океане. Пишет Хосе, капитан и океанограф."),
        "eyebrow": "Бесплатно · раз в две недели",
        "h1": "Морской журнал",
        "lead": ("Раз в две недели я отправляю короткий журнал о море: какой была вода в Марбелье и лучшие новости о "
                 "дайвинге, парусе, рыбалке и морских путешествиях. Журнал выходит на английском и испанском."),
        "ejes_h": "Что в каждом номере",
        "ejes": [("mar", "Море за две недели", "Температура воды, волны и ветер у Пуэрто-Бануса и луна для рыбалки."),
                 ("buceo", "Дайвинг", "Места погружений, морская жизнь, курсы."),
                 ("vela", "Парус и яхты", "Регаты, яхты, морское дело и новости марин."),
                 ("pesca", "Рыбалка", "Сезоны, виды рыб и правила любительской рыбалки."),
                 ("viajes", "Морские путешествия", "Куда поехать нырять и ходить под парусом."),
                 ("ciencia", "Новости океана", "Открытия, киты, акулы и громкие истории.")],
        "susc_h": "Подписаться",
        "susc_p": "Выберите язык. Вам придёт письмо для подтверждения; отписаться можно в один клик.",
        "susc_es": "Подписаться (испанский)",
        "susc_en": "Подписаться (английский)",
        "susc_sin": "Подписка скоро откроется. А пока напишите мне, и я вас добавлю.",
        "susc_wa": "Здравствуйте, Хосе! Хочу получать морской журнал.",
        "archivo_h": "Вышедшие номера",
        "archivo_vacio": "Первый номер уже готовится.",
        "archivo_idioma": {"es": "Испанский", "en": "Английский"},
        "privacidad": ("Ваш адрес используется только для рассылки журнала через Brevo (Sendinblue SAS, ЕС). "
                       "Отписаться можно в любой момент из любого номера."),
        "estado": {"pendiente": ("Проверьте почту", "Я отправил вам письмо со ссылкой для подтверждения подписки."),
                   "ok": ("Вы подписаны!", "Следующий номер придёт через несколько дней.")},
    },
}
