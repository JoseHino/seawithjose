# -*- coding: utf-8 -*-
"""Textos de la web en inglés (principal), español y ruso.

Todo lo que se lee en la web sale de aquí: para cambiar una frase, se cambia
en los tres idiomas y se ejecuta `python build.py`. Los precios, los horarios
y los enlaces de pago están arriba del todo, una sola vez para los tres idiomas.
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
# Si SkylineWebcams o meteo365 autorizan a seawithjose.es, aquí va la dirección del reproductor de cada
# cámara (mismo orden que en T[...]["mar"]["camaras"]) y la web la enseña en directo en vez del enlace.
CAMARAS_EMBED = ["", "", ""]

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
    "title": "Sea With Jose — Sailing trips from Puerto Banús, Marbella",
    "description": ("Sail Marbella aboard the Petit with Jose, yacht captain and oceanographer. Shared trips at €60 "
                    "per person and two-hour private charters for up to 11 guests, from Puerto Banús."),
    "saltar": "Skip to content",
    "nav": {"salidas": "Trips", "petit": "The Petit", "mar": "Sea today", "buceo": "Diving", "jose": "Jose",
            "faq": "FAQ"},
    "menu": "Menu", "whatsapp_corto": "WhatsApp", "reservar_corto": "Book",
    "wa_hola": "Hi Jose! I’d like to go sailing on the Petit.",
    "hero_eyebrow": "Puerto Banús · Marbella",
    "hero_h1": "Sail Marbella <em>aboard the Petit.</em>",
    "hero_lead": ("A 12-metre sailing yacht, her captain and the open sea off Puerto Banús. Two hours to swim far "
                  "from the beach, take the helm if you like and look out for dolphins."),
    "hero_precios": [("Shared", "€60", "per person"), ("Private", "€490", "2 h · up to 11 guests")],
    "hero_cta": "Book your trip",
    "hero_cta2": "Ask me on WhatsApp",
    "hero_foto_alt": "The Petit at anchor at sunset, against the light",
    "hero_delfines_alt": "Dolphins leaping in front of a sailing yacht",
    "hero_chip": "Today at sea", "hero_chip_agua": "water {t} °C", "hero_chip_sol": "sunset {h}",
    "credenciales": [
        ("Yacht Captain", "Spanish licence"),
        ("Oceanographer", "University of Cádiz"),
        ("Diving instructor", "FEDAS · CMAS"),
        ("5 seasons", "skippering in Marbella"),
        ("Languages", "English · Español · Русский"),
    ],
    "salidas_eyebrow": "Sailing trips",
    "salidas_h2": "Choose how you sail",
    "salidas_intro": ("Both leave from Puerto Banús and last two hours. I’m always at the helm — or right next to you "
                      "if you’d like to steer."),
    "opciones": {
        "compartida": {"titulo": "Shared trip", "precio": "€60", "unidad": "per person",
                       "puntos": ["Two hours under sail", "Share the Petit with other travellers — 11 at most",
                                  "A swim in open water when the sea allows", "Take the helm if you fancy it"],
                       "cta": "Book a seat", "foto_alt": "The Petit’s cockpit under way, with the wheel"},
        "privada": {"titulo": "Private trip", "precio": "€490", "unidad": "the whole boat · 2 h",
                    "puntos": ["The Petit just for your group, up to 11 guests", "You pick the time — sunset included",
                               "Your route: swimming, dolphins or the coast",
                               "Make it yours with food, drinks and decorations"],
                    "cta": "Book the boat", "foto_alt": "The Petit at anchor in clear water"},
    },
    "ruta_eyebrow": "Your trip, step by step",
    "ruta_h2": "Two hours, more or less like this",
    "ruta_nota": "This is the usual course: the wind and the sea decide the rest.",
    "ruta_pasos": [
        ("0:00", "Boarding at Puerto Banús", "I’ll meet you at the pontoon 15 minutes before; you’ll get the exact "
                                             "spot on WhatsApp."),
        ("0:15", "Sails up", "We motor out of the harbour and hoist the sails as soon as we clear the entrance. "
                             "Take the helm if you like."),
        ("0:45", "Anchor and swim", "We stop in a quiet spot off San Pedro to swim far from the beach."),
        ("1:15", "Open sea", "We sail further out — that’s where the dolphins usually show up."),
        ("2:00", "Back to Banús", "We sail home with the whole coast of Marbella ahead of us."),
    ],
    "carta_aria": ("Nautical chart of the coast between San Pedro Alcántara and Marbella, with the usual course of "
                   "the trip from Puerto Banús"),
    "carta": {"banus": "Puerto José Banús", "sanpedro": "San Pedro Alcántara", "marbella": "Marbella",
              "galeon": "The Galleon · 8–10 m", "rioverde": "Río Verde", "alboran": "Alboran Sea", "oeste": "W",
              "norte": "N", "ruta": "Usual course"},
    "reservar_eyebrow": "Booking",
    "reservar_h2": "Book and pay in a minute",
    "reservar_intro": "Choose the day, the time and how many of you are coming. I’ll confirm your trip on WhatsApp.",
    "form": {
        "tipo": "Type of trip", "tipos": {"compartida": "Shared", "privada": "Private"},
        "tipos_sub": {"compartida": "€60 per person", "privada": "€490 · whole boat"},
        "fecha": "Day", "hora": "Departure time", "atardecer": "Sunset",
        "personas": "People", "menos": "One person fewer", "mas": "One person more", "max": "11 people at most",
        "nombre": "Your name", "nombre_ph": "So I know who’s coming",
        "extras": "Make your private trip yours",
        "extras_nota": "Extras are quoted separately: I’ll send you the price on WhatsApp before the trip.",
        "otra": "Another idea? Tell me",
        "total": "Total", "detalle_compartida": "{n} × €60", "detalle_privada": "Whole boat, 2 h",
        "pagar": "Pay {total} by card", "whatsapp": "Book on WhatsApp instead",
        "seguro": "Secure payment with Stripe. Your card details never touch this website.",
        "politica": ("Free cancellation up to 48 hours before. If the sea isn’t right for sailing, we change the date "
                     "or I refund you in full."),
        "sin_pago": "Card payment is coming very soon. For now, book on WhatsApp and I’ll confirm right away.",
        "falta_fecha": "Choose a day.", "falta_hora": "Choose a departure time.", "falta_nombre": "Tell me your name.",
        "prevision": "AEMET forecast for that time: sailing {n}/10 · {banda}",
        "msg_inicio": "Hi Jose! I’d like to book a trip on the Petit.", "msg_tipo": "Trip", "msg_fecha": "Day",
        "msg_hora": "Time", "msg_personas": "People", "msg_extras": "Extras", "msg_nombre": "Name",
        "msg_total": "Total", "msg_ref": "Reference", "msg_pagado": "I’ve just paid online.",
    },
    "billete": {"titulo": "Boarding pass", "barco": "Vessel", "barco_v": "Petit", "puerto": "From",
                "puerto_v": "Puerto Banús", "fecha": "Date", "hora": "Time", "pax": "Guests", "tipo": "Trip",
                "extras": "Extras", "total": "Total", "capitan": "Captain", "capitan_v": "Jose"},
    "pers_eyebrow": "Private trips",
    "pers_h2": "Make it yours",
    "pers_intro": ("Birthdays, proposals, hen and stag parties — or just a great day with your people. Tell me what "
                   "you have in mind and I’ll have it ready on board."),
    "extras": [
        {"id": "buffet", "titulo": "Buffet on board", "texto": "Nibbles, fruit and something sweet for the whole group."},
        {"id": "paella", "titulo": "Paella", "texto": "To enjoy at anchor, with Marbella as the backdrop."},
        {"id": "cocteles", "titulo": "Cocktails", "texto": "Cocktails and cava for a toast at sea."},
        {"id": "tarta", "titulo": "Cake", "texto": "Your birthday or celebration cake, waiting on board."},
        {"id": "decoracion", "titulo": "Decorations", "texto": "Balloons, flowers, bunting: the boat dressed your way."},
        {"id": "otra", "titulo": "Anything else", "texto": "Music, a photographer, a surprise… Just ask."},
    ],
    "pers_nota": "Extras are quoted separately, depending on your group.",
    "pers_cta": "Book a private trip",
    "petit_eyebrow": "The boat",
    "petit_h2": "The Petit",
    "petit_sub": "P’tit Mousse — “the Petit” to her friends",
    "petit_p": [
        ("A centre-cockpit Jeanneau Sun Odyssey 42: 12.3 metres long, with a teak deck and a bimini that shades the "
         "cockpit."),
        "A stable, comfortable cruising yacht with room for eleven guests to sail at ease.",
    ],
    "petit_datos": [("Model", "Jeanneau Sun Odyssey 42 CC"), ("Length", "12.3 m"), ("Guests", "up to 11 + captain"),
                    ("Base", "Puerto José Banús")],
    "galeria": {"petit-azul": "The Petit moored under a deep blue sky",
                "petit-banera": "The cockpit under way, with the wheel",
                "petit-proa": "The teak foredeck and the bow",
                "petit-pantalan": "The Petit alongside a pontoon in turquoise water",
                "petit-cubierta": "The deck seen from the bow",
                "petit-bimini": "The bimini over the centre cockpit",
                "petit-fondeado": "The Petit at anchor"},
    "video_alt": "The Petit under way on a calm sea", "video_pausa": "Pause the video", "video_play": "Play the video",
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
    "buceo_eyebrow": "Diving · The Blue Path",
    "buceo_h2": "Marbella carries on underwater",
    "buceo_lead": ("I’m a FEDAS diving instructor. I’ll take you to the dive sites of Málaga’s Blue Path (Senda Azul) "
                   "to suit your level — from your first try dive to banks 40 metres down."),
    "buceo_cta": "See all 15 dive sites",
    "buceo_title": "Diving in Marbella: the Blue Path dive sites — Sea With Jose",
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
                            "No experience needed — just curiosity."),
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
    "habichuelas_h": "The Beans Wreck — Punta Carnero",
    "habichuelas_p": ("The <em>Dina</em>, a 109-metre freighter that ran aground in an easterly storm in 1983 "
                      "carrying tinned beans. Today it’s a reef full of life between 8 and 12 metres."),
    "viajes_h": "Dive trips",
    "viajes_p": ("Every year I lead small-group trips to the world’s great dive destinations: the Maldives, "
                 "the Philippines, Indonesia. Tell me where you’d like to go next."),
    "fotos_buceo": {"pulpo": "An octopus on the seabed off Marbella", "ok": "Two divers giving the OK sign",
                    "tortuga": "Diving with a green turtle", "tiburon": "Divers watching a tiger shark"},
    "buceo_wa": "Hi Jose! I’d like to go diving with you.",
    "buceo_wa_cta": "Ask about diving",
    "jose_eyebrow": "Your captain",
    "jose_h2": "An oceanographer who made the sea his job",
    "jose_p": [
        ("I studied oceanography at the University of Cádiz. I’m a yacht captain and a FEDAS diving instructor, and "
         "I’ve spent the last five seasons skippering sailing yachts, motorboats and fishing boats out of Marbella "
         "and Puerto Banús."),
        ("So I know where the water stays calm when the wind picks up, where the dolphins usually are, and what lives "
         "on the seabed below your boat. I’ll share all of it with you — in English, Spanish or Russian."),
    ],
    "jose_foto": "Jose on a boat, ready to get in the water",
    "cuaderno": "Logbook",
    "bitacora": [
        ("2016", "First dives. Ten years later I’m still going back underwater."),
        ("2022", "First season as a charter skipper in Marbella."),
        ("2023", "Diving instructor (FEDAS · CMAS) and head of a charter fleet."),
        ("2025", "Sailing trips to see dolphins, and fishing charters."),
        ("2026", "Yacht Captain licence."),
    ],
    "tambien_eyebrow": "More at sea",
    "tambien_h2": "Fishing and jet ski",
    "tambien": [
        {"id": "pesca", "titulo": "Fishing trips",
         "frase": "I’ll take you where the fish are biting — beginners, families and keen anglers alike.",
         "puntos": ["Bottom fishing or trolling", "Morning or afternoon", "New to fishing? I’ll show you how"],
         "cta": "Ask about fishing", "wa": "Hi Jose! I’d like to know more about your fishing trips."},
        {"id": "moto", "titulo": "Jet ski",
         "frase": "The Golden Mile from the water, at full throttle.",
         "puntos": ["Guided rides along the coast", "First time on a jet ski? I’ll brief you before we go"],
         "cta": "Ask about jet ski", "wa": "Hi Jose! I’d like to know more about jet ski rides."},
    ],
    "faq_h2": "Questions",
    "faq": [
        ("How much does it cost?", "A shared trip is €60 per person. A private trip is €490 for the whole boat for two "
                                   "hours, for up to 11 guests. Extras for private trips (food, drinks, decorations) "
                                   "are quoted separately."),
        ("Do I need to know how to sail?", "No. I sail the boat — you just enjoy it. If you’d like, I’ll show you how "
                                           "to steer."),
        ("Where do we meet?", "At Puerto José Banús, Marbella. I’ll send you the exact pontoon on WhatsApp."),
        ("What should I bring?", "Swimsuit, towel, sunscreen and sunglasses."),
        ("What if the weather is bad?", "I only go out when the sea is safe and enjoyable. If I cancel because of the "
                                        "weather, you choose: another date or a full refund."),
        ("Can I cancel?", "Yes, free of charge up to 48 hours before your trip."),
        ("Can children come?", "Yes, families are very welcome. Tell me their ages when you book."),
        ("Which languages do you speak?", "English, Spanish and Russian."),
    ],
    "final_h2": "See you on board?",
    "final_p": "Book your seat or message me on WhatsApp and I’ll help you choose.",
    "pie_lugar": "Puerto José Banús, 29660 Marbella (Málaga), Spain",
    "pie_legal": "Legal notice, bookings and privacy",
    "pie_creditos": "Photos: the Petit · Bathymetry: EMODnet (CC BY 4.0) · Forecast: AEMET · Dive sites: Senda Azul",
    "legal_title": "Legal notice, bookings and privacy — Sea With Jose",
    "legal_h1": "Legal notice, bookings and privacy",
    "legal": [
        ("Who runs this website", "Sea With Jose is the personal brand of José María Hinojosa Figueira, based in "
                                  "Marbella (Málaga, Spain). Contact: {email} · WhatsApp {tel}."),
        ("What this website does", "It presents my sailing trips on the Petit and my other experiences at sea, and "
                                   "lets you book and pay for sailing trips online."),
        ("Bookings and payment", "Trips are paid in advance by card through Stripe, which processes the payment: this "
                                 "website never sees or stores your card details. Your booking is confirmed when I "
                                 "write to you on WhatsApp or by email. Prices shown are final prices. Extras for "
                                 "private trips are quoted and paid separately."),
        ("Cancellations", "You can cancel free of charge up to 48 hours before your trip and I’ll refund you in full. "
                          "If I cancel because of the state of the sea or for safety reasons, you choose another date "
                          "or a full refund. As this is a leisure activity on a specific date, the 14-day right of "
                          "withdrawal does not apply (article 103.l of the Spanish consumer protection law)."),
        ("On board", "For safety, the captain decides the route, where to anchor and whether to go out or carry on "
                     "sailing."),
        ("Your data", "If you book or write to me, I use your name, contact details and booking details only to "
                      "organise your trip and meet my tax obligations, and I keep them only as long as required. "
                      "Stripe processes payment data as an independent controller (stripe.com/privacy). You can ask "
                      "me at any time to see, correct or delete your data by writing to {email}, and you can complain "
                      "to the Spanish Data Protection Agency (aepd.es)."),
        ("Cookies", "This website uses no cookies and no analytics. While you book, your browser keeps the details of "
                    "your booking so they can be shown to you when you come back from the payment page. Fonts and "
                    "images are served from the site itself."),
        ("Third parties", "The site is hosted on GitHub Pages (GitHub Inc.), which may record visitors’ IP addresses "
                          "for security. The WhatsApp, Instagram and webcam links take you to those services, which "
                          "have their own privacy policies."),
        ("Credits", "Bathymetry: EMODnet Bathymetry Consortium, CC BY 4.0. Forecasts: information prepared by the "
                    "Spanish State Meteorological Agency (AEMET). Dive sites: “Málaga sumergida. Guía de buceo de la "
                    "Senda Azul”, Turismo y Planificación Costa del Sol."),
    ],
    "gracias": {"title": "Booking received — Sea With Jose", "h1": "Booking received!",
                "p": "Thank you. As soon as I see your payment, I’ll confirm your trip on WhatsApp.",
                "resumen": "Your trip", "wa": "Message me on WhatsApp", "volver": "Back to the website",
                "sin": ("I can’t find your booking details in this browser, but don’t worry: Stripe has emailed you the "
                        "receipt. Message me and we’ll sort it out.")},
    "volver": "Back to the home page",
    "e404_h1": "This page is off the chart",
    "e404_p": "The address may be wrong or the page has moved.",
}

# ───────────────────────────────── ESPAÑOL ─────────────────────────────────
T["es"] = {
    "nombre_idioma": "Español", "corto": "ES", "og_locale": "es_ES",
    "title": "Sea With Jose — Salidas en velero desde Puerto Banús, Marbella",
    "description": ("Navega por Marbella a bordo del Petit con Jose, capitán de yate y oceanógrafo. Salidas "
                    "compartidas a 60 € por persona y privadas de dos horas para hasta 11 personas, desde Puerto "
                    "Banús."),
    "saltar": "Ir al contenido",
    "nav": {"salidas": "Salidas", "petit": "El Petit", "mar": "El mar hoy", "buceo": "Buceo", "jose": "Jose",
            "faq": "Preguntas"},
    "menu": "Menú", "whatsapp_corto": "WhatsApp", "reservar_corto": "Reservar",
    "wa_hola": "¡Hola Jose! Me gustaría navegar en el Petit.",
    "hero_eyebrow": "Puerto Banús · Marbella",
    "hero_h1": "A vela por Marbella, <em>a bordo del Petit.</em>",
    "hero_lead": ("Un velero de 12 metros, su capitán y el mar abierto frente a Puerto Banús. Dos horas para bañarte "
                  "lejos de la orilla, llevar el timón si te apetece y buscar delfines."),
    "hero_precios": [("Compartida", "60 €", "por persona"), ("Privada", "490 €", "2 h · hasta 11 personas")],
    "hero_cta": "Reserva tu salida",
    "hero_cta2": "Pregúntame por WhatsApp",
    "hero_foto_alt": "El Petit fondeado al atardecer, a contraluz",
    "hero_delfines_alt": "Delfines saltando delante de un velero",
    "hero_chip": "Hoy en el mar", "hero_chip_agua": "agua {t} °C", "hero_chip_sol": "puesta de sol {h}",
    "credenciales": [
        ("Capitán de yate", "titulación española"),
        ("Oceanógrafo", "Universidad de Cádiz"),
        ("Instructor de buceo", "FEDAS · CMAS"),
        ("5 temporadas", "de patrón en Marbella"),
        ("Idiomas", "English · Español · Русский"),
    ],
    "salidas_eyebrow": "Salidas en velero",
    "salidas_h2": "Elige cómo quieres navegar",
    "salidas_intro": ("Las dos salen de Puerto Banús y duran dos horas. El barco lo llevo yo, o voy a tu lado si te "
                      "apetece llevar el timón."),
    "opciones": {
        "compartida": {"titulo": "Salida compartida", "precio": "60 €", "unidad": "por persona",
                       "puntos": ["Dos horas a vela", "Compartes el Petit con otros viajeros: 11 como máximo",
                                  "Baño en mar abierto si el mar lo permite", "Lleva el timón si te apetece"],
                       "cta": "Reservar plaza", "foto_alt": "La bañera del Petit navegando, con el timón"},
        "privada": {"titulo": "Salida privada", "precio": "490 €", "unidad": "el barco entero · 2 h",
                    "puntos": ["El Petit solo para tu grupo, hasta 11 personas", "Tú eliges la hora, también al atardecer",
                               "Ruta a tu medida: baño, delfines o costa",
                               "Personalízala con comida, bebida y decoración"],
                    "cta": "Reservar el barco", "foto_alt": "El Petit fondeado en aguas claras"},
    },
    "ruta_eyebrow": "Tu salida, paso a paso",
    "ruta_h2": "Dos horas, más o menos así",
    "ruta_nota": "Es la ruta habitual: el viento y el mar deciden el resto.",
    "ruta_pasos": [
        ("0:00", "Embarque en Puerto Banús", "Te espero en el pantalán 15 minutos antes; te mando la ubicación exacta "
                                             "por WhatsApp."),
        ("0:15", "Velas arriba", "Salimos del puerto a motor e izamos velas nada más pasar la bocana. Si quieres, "
                                 "llevas el timón."),
        ("0:45", "Fondeo y baño", "Paramos en una zona tranquila frente a San Pedro para bañarnos lejos de la orilla."),
        ("1:15", "Mar abierto", "Navegamos a vela mar adentro: es donde suelen aparecer los delfines."),
        ("2:00", "De vuelta a Banús", "Volvemos a vela con toda la costa de Marbella de frente."),
    ],
    "carta_aria": ("Carta náutica de la costa entre San Pedro Alcántara y Marbella, con la ruta habitual de la salida "
                   "desde Puerto Banús"),
    "carta": {"banus": "Puerto José Banús", "sanpedro": "San Pedro Alcántara", "marbella": "Marbella",
              "galeon": "El Galeón · 8–10 m", "rioverde": "Río Verde", "alboran": "Mar de Alborán", "oeste": "O",
              "norte": "N", "ruta": "Ruta habitual"},
    "reservar_eyebrow": "Reserva",
    "reservar_h2": "Reserva y paga en un minuto",
    "reservar_intro": "Elige el día, la hora y cuántos sois. Te confirmo la salida por WhatsApp.",
    "form": {
        "tipo": "Tipo de salida", "tipos": {"compartida": "Compartida", "privada": "Privada"},
        "tipos_sub": {"compartida": "60 € por persona", "privada": "490 € · barco entero"},
        "fecha": "Día", "hora": "Hora de salida", "atardecer": "Atardecer",
        "personas": "Personas", "menos": "Una persona menos", "mas": "Una persona más", "max": "11 personas como máximo",
        "nombre": "Tu nombre", "nombre_ph": "Para saber quién viene",
        "extras": "Personaliza tu salida privada",
        "extras_nota": "Los extras se presupuestan aparte: te paso el precio por WhatsApp antes de la salida.",
        "otra": "¿Otra idea? Cuéntamela",
        "total": "Total", "detalle_compartida": "{n} × 60 €", "detalle_privada": "Barco entero, 2 h",
        "pagar": "Pagar {total} con tarjeta", "whatsapp": "Prefiero reservar por WhatsApp",
        "seguro": "Pago seguro con Stripe. Los datos de tu tarjeta no pasan por esta web.",
        "politica": ("Cancelación gratis hasta 48 horas antes. Si el mar no está para salir, cambiamos la fecha o te "
                     "devuelvo todo el dinero."),
        "sin_pago": "Muy pronto podrás pagar aquí con tarjeta. De momento, reserva por WhatsApp y te confirmo al momento.",
        "falta_fecha": "Elige un día.", "falta_hora": "Elige la hora de salida.", "falta_nombre": "Dime tu nombre.",
        "prevision": "Previsión de AEMET para esa hora: navegar {n}/10 · {banda}",
        "msg_inicio": "¡Hola Jose! Quiero reservar una salida en el Petit.", "msg_tipo": "Salida", "msg_fecha": "Día",
        "msg_hora": "Hora", "msg_personas": "Personas", "msg_extras": "Extras", "msg_nombre": "Nombre",
        "msg_total": "Total", "msg_ref": "Referencia", "msg_pagado": "Acabo de pagar por la web.",
    },
    "billete": {"titulo": "Tarjeta de embarque", "barco": "Barco", "barco_v": "Petit", "puerto": "Salida",
                "puerto_v": "Puerto Banús", "fecha": "Día", "hora": "Hora", "pax": "Pasajeros", "tipo": "Tipo",
                "extras": "Extras", "total": "Total", "capitan": "Capitán", "capitan_v": "Jose"},
    "pers_eyebrow": "Salidas privadas",
    "pers_h2": "Hazla tuya",
    "pers_intro": ("Cumpleaños, pedidas, despedidas o simplemente un buen día con los tuyos. Dime qué te apetece y lo "
                   "tengo listo a bordo."),
    "extras": [
        {"id": "buffet", "titulo": "Buffet a bordo", "texto": "Picoteo, fruta y algo dulce para todo el grupo."},
        {"id": "paella", "titulo": "Paella", "texto": "Para comer fondeados, con Marbella de fondo."},
        {"id": "cocteles", "titulo": "Coctelería", "texto": "Cócteles y cava para brindar en el mar."},
        {"id": "tarta", "titulo": "Tarta", "texto": "La de tu cumpleaños o tu celebración, esperando a bordo."},
        {"id": "decoracion", "titulo": "Decoración", "texto": "Globos, flores, banderines: el barco decorado a tu gusto."},
        {"id": "otra", "titulo": "Lo que se te ocurra", "texto": "Música, fotógrafo, una sorpresa… Pídemelo."},
    ],
    "pers_nota": "Los extras se presupuestan aparte, según el grupo.",
    "pers_cta": "Reservar salida privada",
    "petit_eyebrow": "El barco",
    "petit_h2": "El Petit",
    "petit_sub": "P’tit Mousse, «el Petit» para los amigos",
    "petit_p": [
        ("Un Jeanneau Sun Odyssey 42 de bañera central: 12,3 metros de eslora, cubierta de teca y un bimini que da "
         "sombra a la bañera."),
        "Un velero de crucero estable y cómodo, con sitio para que once personas naveguen a gusto.",
    ],
    "petit_datos": [("Modelo", "Jeanneau Sun Odyssey 42 CC"), ("Eslora", "12,3 m"),
                    ("Pasajeros", "hasta 11 + capitán"), ("Base", "Puerto José Banús")],
    "galeria": {"petit-azul": "El Petit amarrado bajo un cielo azul intenso",
                "petit-banera": "La bañera navegando, con el timón",
                "petit-proa": "La cubierta de teca y la proa",
                "petit-pantalan": "El Petit abarloado a un pantalán, en agua turquesa",
                "petit-cubierta": "La cubierta vista desde proa",
                "petit-bimini": "El bimini sobre la bañera central",
                "petit-fondeado": "El Petit fondeado"},
    "video_alt": "El Petit navegando en un mar en calma", "video_pausa": "Pausar el vídeo",
    "video_play": "Reproducir el vídeo",
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
    "buceo_eyebrow": "Buceo · La Senda Azul",
    "buceo_h2": "Bajo el agua, Marbella sigue",
    "buceo_lead": ("Soy instructor de buceo FEDAS. Te llevo a los puntos de la Senda Azul de Málaga según tu nivel: "
                   "desde tu primer bautizo hasta los bajos de 40 metros."),
    "buceo_cta": "Ver los 15 puntos de buceo",
    "buceo_title": "Bucear en Marbella: los puntos de la Senda Azul — Sea With Jose",
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
    "habichuelas_h": "El barco de las Habichuelas — Punta Carnero",
    "habichuelas_p": ("El <em>Dina</em>, un mercante de 109 metros que embarrancó en un temporal de levante en 1983 "
                      "cargado de conservas de legumbres. Hoy es un arrecife lleno de vida entre 8 y 12 metros."),
    "viajes_h": "Viajes de buceo",
    "viajes_p": ("Cada año organizo viajes en grupo reducido a los grandes destinos del buceo: Maldivas, Filipinas, "
                 "Indonesia. Dime adónde te gustaría ir."),
    "fotos_buceo": {"pulpo": "Un pulpo en el fondo frente a Marbella", "ok": "Dos buceadores haciendo la señal de OK",
                    "tortuga": "Buceando junto a una tortuga verde", "tiburon": "Buceadores observando un tiburón tigre"},
    "buceo_wa": "¡Hola Jose! Me gustaría bucear contigo.",
    "buceo_wa_cta": "Pregunta por el buceo",
    "jose_eyebrow": "Tu capitán",
    "jose_h2": "Un oceanógrafo que hizo del mar su trabajo",
    "jose_p": [
        ("Soy oceanógrafo por la Universidad de Cádiz, capitán de yate e instructor de buceo FEDAS, y llevo cinco "
         "temporadas como patrón de veleros, lanchas y barcos de pesca en Marbella y Puerto Banús."),
        ("Por eso sé dónde sigue el agua en calma cuando se levanta el viento, por dónde suelen andar los delfines y "
         "qué vive en el fondo bajo tu barco. Te lo cuento todo en inglés, en español o en ruso."),
    ],
    "jose_foto": "Jose en un barco, listo para meterse al agua",
    "cuaderno": "Cuaderno de bitácora",
    "bitacora": [
        ("2016", "Primeras inmersiones. Diez años después sigo volviendo bajo el agua."),
        ("2022", "Primera temporada como patrón de chárter en Marbella."),
        ("2023", "Instructor de buceo (FEDAS · CMAS) y responsable de una flota de chárter."),
        ("2025", "Salidas en velero para ver delfines y chárter de pesca."),
        ("2026", "Título de Capitán de Yate."),
    ],
    "tambien_eyebrow": "Más mar",
    "tambien_h2": "Pesca y motos de agua",
    "tambien": [
        {"id": "pesca", "titulo": "Salidas de pesca",
         "frase": "Te llevo donde pica, seas principiante, familia o pescador con experiencia.",
         "puntos": ["Pesca a fondo o al curricán", "Por la mañana o por la tarde", "¿Es tu primera vez? Te enseño"],
         "cta": "Pregunta por la pesca", "wa": "¡Hola Jose! Me gustaría saber más sobre las salidas de pesca."},
        {"id": "moto", "titulo": "Motos de agua",
         "frase": "La Milla de Oro desde el mar, a todo gas.",
         "puntos": ["Rutas guiadas por la costa", "¿Primera vez en moto de agua? Te lo explico todo antes de salir"],
         "cta": "Pregunta por las motos de agua",
         "wa": "¡Hola Jose! Me gustaría saber más sobre las motos de agua."},
    ],
    "faq_h2": "Preguntas",
    "faq": [
        ("¿Cuánto cuesta?", "La salida compartida cuesta 60 € por persona. La privada, 490 € por el barco entero durante "
                            "dos horas, para hasta 11 personas. Los extras de las privadas (comida, bebida, decoración) "
                            "se presupuestan aparte."),
        ("¿Tengo que saber navegar?", "No. El barco lo llevo yo; tú solo disfruta. Si te apetece, te enseño a llevar "
                                      "el timón."),
        ("¿Dónde quedamos?", "En Puerto José Banús, Marbella. Te mando el pantalán exacto por WhatsApp."),
        ("¿Qué llevo?", "Bañador, toalla, crema solar y gafas de sol."),
        ("¿Y si hace mal tiempo?", "Solo salgo cuando el mar está seguro y apetece. Si cancelo por el tiempo, eliges: "
                                   "otra fecha o la devolución de todo el dinero."),
        ("¿Puedo cancelar?", "Sí, gratis hasta 48 horas antes de la salida."),
        ("¿Pueden venir niños?", "Sí, las familias son bienvenidas. Dime sus edades al reservar."),
        ("¿En qué idiomas hablas?", "Inglés, español y ruso."),
    ],
    "final_h2": "¿Nos vemos a bordo?",
    "final_p": "Reserva tu plaza o escríbeme por WhatsApp y te ayudo a elegir.",
    "pie_lugar": "Puerto José Banús, 29660 Marbella (Málaga)",
    "pie_legal": "Aviso legal, reservas y privacidad",
    "pie_creditos": "Fotos: el Petit · Batimetría: EMODnet (CC BY 4.0) · Previsión: AEMET · Puntos de buceo: Senda Azul",
    "legal_title": "Aviso legal, reservas y privacidad — Sea With Jose",
    "legal_h1": "Aviso legal, reservas y privacidad",
    "legal": [
        ("Titular", "Sea With Jose es la marca personal de José María Hinojosa Figueira, con domicilio en Marbella "
                    "(Málaga). Contacto: {email} · WhatsApp {tel}."),
        ("Qué hace esta web", "Presenta mis salidas en velero en el Petit y mis otras experiencias en el mar, y permite "
                              "reservar y pagar las salidas en velero."),
        ("Reservas y pagos", "Las salidas se pagan por adelantado con tarjeta a través de Stripe, que procesa el pago: "
                             "esta web no ve ni guarda los datos de tu tarjeta. La reserva queda confirmada cuando te "
                             "escribo por WhatsApp o por correo. Los precios que ves son precios finales. Los extras de "
                             "las salidas privadas se presupuestan y se pagan aparte."),
        ("Cancelaciones", "Puedes cancelar gratis hasta 48 horas antes de la salida y te devuelvo todo el importe. Si "
                          "cancelo yo por el estado del mar o por seguridad, eliges otra fecha o la devolución íntegra. "
                          "Al tratarse de una actividad de ocio con fecha concreta, no se aplica el derecho de "
                          "desistimiento de 14 días (artículo 103.l de la Ley General para la Defensa de los "
                          "Consumidores y Usuarios)."),
        ("A bordo", "Por seguridad, el capitán decide la ruta, el fondeo y si se puede salir o seguir navegando."),
        ("Tus datos", "Si reservas o me escribes, uso tu nombre, tus datos de contacto y los de la reserva solo para "
                      "organizar tu salida y cumplir mis obligaciones fiscales, y los conservo únicamente el tiempo "
                      "obligatorio. Stripe trata los datos del pago como responsable independiente "
                      "(stripe.com/privacy). Puedes pedirme en cualquier momento verlos, corregirlos o borrarlos "
                      "escribiendo a {email}, y reclamar ante la Agencia Española de Protección de Datos (aepd.es)."),
        ("Cookies", "Esta web no usa cookies ni herramientas de analítica. Mientras reservas, tu navegador guarda los "
                    "datos de la reserva para enseñártelos al volver de la página de pago. Las tipografías y las "
                    "imágenes se sirven desde la propia web."),
        ("Terceros", "La web está alojada en GitHub Pages (GitHub Inc.), que puede registrar las direcciones IP de las "
                     "visitas por seguridad. Los enlaces de WhatsApp, Instagram y las cámaras te llevan a esos "
                     "servicios, que tienen sus propias políticas de privacidad."),
        ("Créditos", "Batimetría: EMODnet Bathymetry Consortium, CC BY 4.0. Previsiones: información elaborada por la "
                     "Agencia Estatal de Meteorología (AEMET). Puntos de buceo: «Málaga sumergida. Guía de buceo de "
                     "la Senda Azul», Turismo y Planificación Costa del Sol."),
    ],
    "gracias": {"title": "Reserva recibida — Sea With Jose", "h1": "¡Reserva recibida!",
                "p": "Gracias. En cuanto vea el pago, te confirmo la salida por WhatsApp.",
                "resumen": "Tu salida", "wa": "Escríbeme por WhatsApp", "volver": "Volver a la web",
                "sin": ("No encuentro los datos de tu reserva en este navegador, pero no te preocupes: Stripe te ha "
                        "mandado el recibo por correo. Escríbeme y lo vemos.")},
    "volver": "Volver al inicio",
    "e404_h1": "Esta página está fuera de la carta",
    "e404_p": "Puede que la dirección esté mal escrita o que la página haya cambiado de sitio.",
}

# ───────────────────────────────── RUSO ─────────────────────────────────
T["ru"] = {
    "nombre_idioma": "Русский", "corto": "RU", "og_locale": "ru_RU",
    "title": "Sea With Jose — прогулки под парусом из Пуэрто-Бануса, Марбелья",
    "description": ("Прогулки под парусом в Марбелье на яхте «Пти» с Хосе — капитаном яхты и океанографом. "
                    "Групповые выходы за 60 € с человека и индивидуальные двухчасовые прогулки до 11 гостей из "
                    "Пуэрто-Бануса."),
    "saltar": "Перейти к содержанию",
    "nav": {"salidas": "Прогулки", "petit": "«Пти»", "mar": "Море сегодня", "buceo": "Дайвинг", "jose": "Хосе",
            "faq": "Вопросы"},
    "menu": "Меню", "whatsapp_corto": "WhatsApp", "reservar_corto": "Забронировать",
    "wa_hola": "Здравствуйте, Хосе! Хочу выйти в море на «Пти».",
    "hero_eyebrow": "Пуэрто-Банус · Марбелья",
    "hero_h1": "Под парусом в Марбелье — <em>на борту «Пти».</em>",
    "hero_lead": ("12-метровая парусная яхта, её капитан и открытое море у Пуэрто-Бануса. Два часа, чтобы искупаться "
                  "вдали от пляжа, постоять за штурвалом и поискать дельфинов."),
    "hero_precios": [("Групповая", "60 €", "с человека"), ("Индивидуальная", "490 €", "2 ч · до 11 гостей")],
    "hero_cta": "Забронировать прогулку",
    "hero_cta2": "Спросить в WhatsApp",
    "hero_foto_alt": "«Пти» на якоре на закате, против света",
    "hero_delfines_alt": "Дельфины выпрыгивают из воды перед парусной яхтой",
    "hero_chip": "Сегодня в море", "hero_chip_agua": "вода {t} °C", "hero_chip_sol": "закат в {h}",
    "credenciales": [
        ("Капитан яхты", "испанский диплом"),
        ("Океанограф", "Университет Кадиса"),
        ("Инструктор по дайвингу", "FEDAS · CMAS"),
        ("5 сезонов", "шкипером в Марбелье"),
        ("Языки", "English · Español · Русский"),
    ],
    "salidas_eyebrow": "Прогулки под парусом",
    "salidas_h2": "Выберите свою прогулку",
    "salidas_intro": ("Обе начинаются в Пуэрто-Банусе и длятся два часа. Яхтой управляю я — или стою рядом, если вам "
                      "захочется порулить."),
    "opciones": {
        "compartida": {"titulo": "Групповая прогулка", "precio": "60 €", "unidad": "с человека",
                       "puntos": ["Два часа под парусом", "«Пти» вместе с другими путешественниками — не больше 11",
                                  "Купание в открытом море, если позволяет погода", "Можно постоять за штурвалом"],
                       "cta": "Забронировать место", "foto_alt": "Кокпит «Пти» на ходу, штурвал"},
        "privada": {"titulo": "Индивидуальная прогулка", "precio": "490 €", "unidad": "вся яхта · 2 ч",
                    "puntos": ["«Пти» только для вашей компании, до 11 гостей", "Время выбираете вы, в том числе закат",
                               "Маршрут на ваш вкус: купание, дельфины или берег",
                               "Дополните угощением, напитками и украшениями"],
                    "cta": "Забронировать яхту", "foto_alt": "«Пти» на якоре в прозрачной воде"},
    },
    "ruta_eyebrow": "Ваша прогулка шаг за шагом",
    "ruta_h2": "Два часа — примерно так",
    "ruta_nota": "Это обычный маршрут: остальное решают ветер и море.",
    "ruta_pasos": [
        ("0:00", "Посадка в Пуэрто-Банусе", "Встречаю вас на причале за 15 минут до выхода; точное место пришлю "
                                            "в WhatsApp."),
        ("0:15", "Поднимаем паруса", "Выходим из порта на моторе и сразу за входом поднимаем паруса. Хотите — "
                                     "вставайте за штурвал."),
        ("0:45", "Якорь и купание", "Встаём на якорь в тихом месте у Сан-Педро и купаемся вдали от берега."),
        ("1:15", "Открытое море", "Идём под парусом мористее — именно там обычно появляются дельфины."),
        ("2:00", "Обратно в Банус", "Возвращаемся под парусом, и перед вами всё побережье Марбельи."),
    ],
    "carta_aria": ("Морская карта побережья между Сан-Педро-Алькантара и Марбельей с обычным маршрутом прогулки из "
                   "Пуэрто-Бануса"),
    "carta": {"banus": "Пуэрто-Хосе-Банус", "sanpedro": "Сан-Педро-Алькантара", "marbella": "Марбелья",
              "galeon": "«Галеон» · 8–10 м", "rioverde": "Рио-Верде", "alboran": "Море Альборан", "oeste": "W",
              "norte": "N", "ruta": "Обычный маршрут"},
    "reservar_eyebrow": "Бронирование",
    "reservar_h2": "Бронирование и оплата за минуту",
    "reservar_intro": "Выберите день, время и количество гостей. Я подтвержу прогулку в WhatsApp.",
    "form": {
        "tipo": "Тип прогулки", "tipos": {"compartida": "Групповая", "privada": "Индивидуальная"},
        "tipos_sub": {"compartida": "60 € с человека", "privada": "490 € · вся яхта"},
        "fecha": "День", "hora": "Время выхода", "atardecer": "Закат",
        "personas": "Гостей", "menos": "На одного меньше", "mas": "На одного больше", "max": "Не больше 11 человек",
        "nombre": "Ваше имя", "nombre_ph": "Чтобы я знал, кто придёт",
        "extras": "Сделайте индивидуальную прогулку особенной",
        "extras_nota": "Дополнительные услуги оплачиваются отдельно: я пришлю цену в WhatsApp до прогулки.",
        "otra": "Есть другая идея? Расскажите",
        "total": "Итого", "detalle_compartida": "{n} × 60 €", "detalle_privada": "Вся яхта, 2 ч",
        "pagar": "Оплатить {total} картой", "whatsapp": "Забронировать через WhatsApp",
        "seguro": "Безопасная оплата через Stripe. Данные карты не проходят через этот сайт.",
        "politica": ("Бесплатная отмена не позднее чем за 48 часов. Если море не позволяет выйти, перенесём дату "
                     "или я верну деньги полностью."),
        "sin_pago": "Оплата картой появится совсем скоро. Пока бронируйте через WhatsApp — я сразу подтвержу.",
        "falta_fecha": "Выберите день.", "falta_hora": "Выберите время выхода.", "falta_nombre": "Напишите своё имя.",
        "prevision": "Прогноз AEMET на это время: парус {n}/10 · {banda}",
        "msg_inicio": "Здравствуйте, Хосе! Хочу забронировать прогулку на «Пти».", "msg_tipo": "Прогулка",
        "msg_fecha": "День", "msg_hora": "Время", "msg_personas": "Гостей", "msg_extras": "Дополнительно",
        "msg_nombre": "Имя", "msg_total": "Итого", "msg_ref": "Номер брони", "msg_pagado": "Я только что оплатил(а) на сайте.",
    },
    "billete": {"titulo": "Посадочный талон", "barco": "Яхта", "barco_v": "Пти", "puerto": "Отправление",
                "puerto_v": "Пуэрто-Банус", "fecha": "Дата", "hora": "Время", "pax": "Гостей", "tipo": "Прогулка",
                "extras": "Дополнительно", "total": "Итого", "capitan": "Капитан", "capitan_v": "Хосе"},
    "pers_eyebrow": "Индивидуальные прогулки",
    "pers_h2": "Сделайте её своей",
    "pers_intro": ("Дни рождения, предложения руки и сердца, девичники и мальчишники — или просто хороший день с "
                   "близкими. Расскажите, что вы задумали, и всё будет готово на борту."),
    "extras": [
        {"id": "buffet", "titulo": "Фуршет на борту", "texto": "Закуски, фрукты и что-нибудь сладкое на всю компанию."},
        {"id": "paella", "titulo": "Паэлья", "texto": "Чтобы пообедать на якоре на фоне Марбельи."},
        {"id": "cocteles", "titulo": "Коктейли", "texto": "Коктейли и кава, чтобы поднять бокалы в море."},
        {"id": "tarta", "titulo": "Торт", "texto": "Торт ко дню рождения или празднику ждёт вас на борту."},
        {"id": "decoracion", "titulo": "Украшения", "texto": "Шары, цветы, флажки: яхта украшена по вашему вкусу."},
        {"id": "otra", "titulo": "Всё, что придумаете", "texto": "Музыка, фотограф, сюрприз… Просто скажите."},
    ],
    "pers_nota": "Дополнительные услуги оплачиваются отдельно, в зависимости от компании.",
    "pers_cta": "Забронировать индивидуальную прогулку",
    "petit_eyebrow": "Яхта",
    "petit_h2": "«Пти»",
    "petit_sub": "P’tit Mousse — для друзей просто «Пти»",
    "petit_p": [
        ("Jeanneau Sun Odyssey 42 с центральным кокпитом: 12,3 метра, тиковая палуба и бимини, которое даёт тень "
         "в кокпите."),
        "Устойчивая и удобная круизная яхта, на которой с комфортом разместятся одиннадцать гостей.",
    ],
    "petit_datos": [("Модель", "Jeanneau Sun Odyssey 42 CC"), ("Длина", "12,3 м"), ("Гостей", "до 11 + капитан"),
                    ("Стоянка", "Пуэрто-Хосе-Банус")],
    "galeria": {"petit-azul": "«Пти» у причала под ярко-синим небом",
                "petit-banera": "Кокпит на ходу, штурвал",
                "petit-proa": "Тиковая палуба и нос яхты",
                "petit-pantalan": "«Пти» у понтона в бирюзовой воде",
                "petit-cubierta": "Палуба, вид с носа",
                "petit-bimini": "Бимини над центральным кокпитом",
                "petit-fondeado": "«Пти» на якоре"},
    "video_alt": "«Пти» идёт по спокойному морю", "video_pausa": "Поставить видео на паузу",
    "video_play": "Воспроизвести видео",
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
    "buceo_eyebrow": "Дайвинг · «Голубая тропа»",
    "buceo_h2": "Под водой Марбелья продолжается",
    "buceo_lead": ("Я инструктор по дайвингу FEDAS. Отвезу вас к точкам «Голубой тропы» (Senda Azul) Малаги под ваш "
                   "уровень — от первого пробного погружения до банок на глубине 40 метров."),
    "buceo_cta": "Все 15 точек погружения",
    "buceo_title": "Дайвинг в Марбелье: точки «Голубой тропы» — Sea With Jose",
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
    "habichuelas_h": "«Корабль с фасолью» — Пунта-Карнеро",
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
    "jose_eyebrow": "Ваш капитан",
    "jose_h2": "Океанограф, который сделал море своей работой",
    "jose_p": [
        ("Я изучал океанографию в Университете Кадиса, у меня диплом капитана яхты и инструктора по дайвингу FEDAS, "
         "а последние пять сезонов я работаю шкипером на парусных яхтах, моторных катерах и рыболовных лодках в "
         "Марбелье и Пуэрто-Банусе."),
        ("Поэтому я знаю, где вода остаётся спокойной, когда поднимается ветер, где обычно встречаются дельфины и кто "
         "живёт на дне под вашей лодкой. Расскажу обо всём — по-английски, по-испански или по-русски."),
    ],
    "jose_foto": "Хосе на лодке перед погружением",
    "cuaderno": "Судовой журнал",
    "bitacora": [
        ("2016", "Первые погружения. Десять лет спустя я всё так же возвращаюсь под воду."),
        ("2022", "Первый сезон шкипером чартеров в Марбелье."),
        ("2023", "Инструктор по дайвингу (FEDAS · CMAS) и руководитель чартерного флота."),
        ("2025", "Парусные выходы к дельфинам и рыболовные чартеры."),
        ("2026", "Диплом капитана яхты."),
    ],
    "tambien_eyebrow": "Ещё в море",
    "tambien_h2": "Рыбалка и гидроциклы",
    "tambien": [
        {"id": "pesca", "titulo": "Морская рыбалка",
         "frase": "Отвезу вас туда, где клюёт, — и новичков, и семьи, и опытных рыбаков.",
         "puntos": ["Донная рыбалка или троллинг", "Утром или после обеда", "Рыбачите впервые? Всё покажу"],
         "cta": "Спросить о рыбалке",
         "wa": "Здравствуйте, Хосе! Хотел(а) бы узнать подробнее о морской рыбалке."},
        {"id": "moto", "titulo": "Гидроциклы",
         "frase": "Золотая миля Марбельи с воды — на полном газу.",
         "puntos": ["Прогулки с гидом вдоль побережья", "Впервые на гидроцикле? Перед стартом всё объясню"],
         "cta": "Спросить о гидроциклах",
         "wa": "Здравствуйте, Хосе! Хотел(а) бы узнать подробнее о прогулках на гидроцикле."},
    ],
    "faq_h2": "Вопросы",
    "faq": [
        ("Сколько это стоит?", "Групповая прогулка — 60 € с человека. Индивидуальная — 490 € за всю яхту на два часа, "
                               "до 11 гостей. Дополнительные услуги для индивидуальных прогулок (еда, напитки, "
                               "украшения) оплачиваются отдельно."),
        ("Нужно ли уметь ходить под парусом?", "Нет. Яхтой управляю я, а вы просто отдыхаете. Если захотите, научу "
                                               "держать штурвал."),
        ("Где встречаемся?", "В Пуэрто-Хосе-Банусе, Марбелья. Точный причал пришлю в WhatsApp."),
        ("Что взять с собой?", "Купальник, полотенце, солнцезащитный крем и солнечные очки."),
        ("А если погода плохая?", "Я выхожу в море только тогда, когда это безопасно и приятно. Если я отменю прогулку "
                                  "из-за погоды, выбирайте: другая дата или полный возврат денег."),
        ("Можно ли отменить бронь?", "Да, бесплатно не позднее чем за 48 часов до прогулки."),
        ("Можно ли с детьми?", "Да, семьям всегда рады. Укажите возраст детей при бронировании."),
        ("На каких языках вы говорите?", "На английском, испанском и русском."),
    ],
    "final_h2": "До встречи на борту?",
    "final_p": "Забронируйте место или напишите мне в WhatsApp — помогу выбрать.",
    "pie_lugar": "Пуэрто-Хосе-Банус, 29660 Марбелья (Малага), Испания",
    "pie_legal": "Правовая информация, бронирование и конфиденциальность",
    "pie_creditos": "Фото: «Пти» · Батиметрия: EMODnet (CC BY 4.0) · Прогноз: AEMET · Точки погружений: Senda Azul",
    "legal_title": "Правовая информация, бронирование и конфиденциальность — Sea With Jose",
    "legal_h1": "Правовая информация, бронирование и конфиденциальность",
    "legal": [
        ("Владелец сайта", "Sea With Jose — личный бренд Хосе Марии Инохосы Фигейры (José María Hinojosa Figueira), "
                           "Марбелья (Малага, Испания). Контакты: {email} · WhatsApp {tel}."),
        ("Назначение сайта", "Сайт рассказывает о прогулках под парусом на «Пти» и других моих морских программах и "
                             "позволяет забронировать и оплатить прогулки онлайн."),
        ("Бронирование и оплата", "Прогулки оплачиваются заранее картой через Stripe, который обрабатывает платёж: этот "
                                  "сайт не видит и не хранит данные вашей карты. Бронь подтверждается, когда я пишу вам "
                                  "в WhatsApp или по почте. Указанные цены — окончательные. Дополнительные услуги для "
                                  "индивидуальных прогулок оцениваются и оплачиваются отдельно."),
        ("Отмена", "Вы можете бесплатно отменить бронь не позднее чем за 48 часов до прогулки, и я верну всю сумму. "
                   "Если прогулку отменяю я из-за состояния моря или по соображениям безопасности, вы выбираете "
                   "другую дату или полный возврат. Поскольку это досуговая услуга на конкретную дату, 14-дневное "
                   "право на отказ не применяется (статья 103.l испанского закона о защите прав потребителей)."),
        ("На борту", "Ради безопасности маршрут, место якорной стоянки и возможность выйти в море или продолжить "
                     "прогулку определяет капитан."),
        ("Ваши данные", "Если вы бронируете или пишете мне, я использую ваше имя, контакты и данные брони только для "
                        "организации прогулки и выполнения налоговых обязательств и храню их лишь в течение "
                        "обязательного срока. Stripe обрабатывает платёжные данные как независимый оператор "
                        "(stripe.com/privacy). В любой момент вы можете попросить показать, исправить или удалить ваши "
                        "данные, написав на {email}, а также подать жалобу в Испанское агентство по защите данных "
                        "(aepd.es)."),
        ("Cookies", "Сайт не использует cookies и аналитику. Пока вы бронируете, браузер хранит данные брони, чтобы "
                    "показать их вам после возвращения со страницы оплаты. Шрифты и изображения загружаются с самого "
                    "сайта."),
        ("Третьи лица", "Сайт размещён на GitHub Pages (GitHub Inc.), который может записывать IP-адреса посетителей "
                        "в целях безопасности. Ссылки на WhatsApp, Instagram и веб-камеры ведут на эти сервисы, у "
                        "которых свои правила конфиденциальности."),
        ("Источники", "Батиметрия: EMODnet Bathymetry Consortium, CC BY 4.0. Прогнозы: информация Государственного "
                      "метеорологического агентства Испании (AEMET). Точки погружений: «Málaga sumergida. Guía de "
                      "buceo de la Senda Azul», Turismo y Planificación Costa del Sol."),
    ],
    "gracias": {"title": "Бронь получена — Sea With Jose", "h1": "Бронь получена!",
                "p": "Спасибо! Как только я увижу оплату, подтвержу прогулку в WhatsApp.",
                "resumen": "Ваша прогулка", "wa": "Написать мне в WhatsApp", "volver": "Вернуться на сайт",
                "sin": ("Я не нахожу данных вашей брони в этом браузере, но не волнуйтесь: Stripe отправил вам чек по "
                        "почте. Напишите мне, и мы всё уладим.")},
    "volver": "На главную",
    "e404_h1": "Этой страницы нет на карте",
    "e404_p": "Возможно, адрес набран с ошибкой или страница переехала.",
}
