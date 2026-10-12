# -*- coding: utf-8 -*-
"""Textos de la web en inglés (principal), español y ruso.

Todo lo que se lee en la web sale de aquí: para cambiar una frase, se cambia
en los tres idiomas y se ejecuta `python build.py`.
"""

WHATSAPP = "34665092090"
WHATSAPP_VISIBLE = "+34 665 09 20 90"
INSTAGRAM = "seawithjose"
EMAIL = "josemariahf612@gmail.com"
DOMINIO = "https://seawithjose.es"

IDIOMAS = ["en", "es", "ru"]          # el primero va en la raíz

T = {}

# ───────────────────────────────── INGLÉS ─────────────────────────────────
T["en"] = {
    "nombre_idioma": "English", "corto": "EN", "og_locale": "en_GB",
    "title": "Sea With Jose — Sailing, diving, fishing and jet ski in Marbella",
    "description": ("Private days at sea from Puerto Banús with Jose: oceanographer, yacht captain and "
                    "diving instructor. Sailing, scuba diving, fishing and jet ski in Marbella."),
    "saltar": "Skip to content",
    "nav": {"experiencias": "Experiences", "jose": "Jose", "buceo": "Diving", "como": "How it works", "faq": "FAQ"},
    "menu": "Menu", "whatsapp_corto": "WhatsApp",
    "hero_eyebrow": "36°29′ N · 4°57′ W — Puerto Banús, Marbella",
    "hero_h1": "The sea of Marbella, <em>with someone who knows it.</em>",
    "hero_lead": ("Sailing, diving, fishing and jet ski from Puerto Banús. I’m Jose: oceanographer, yacht captain "
                  "and diving instructor — and I’ll show you the sea the way I see it."),
    "hero_cta": "Plan my day on WhatsApp",
    "hero_cta2": "See the experiences",
    "carta_aria": "Nautical chart of the coast between San Pedro Alcántara and Marbella, with the real depth contours",
    "carta": {"banus": "Puerto José Banús", "sanpedro": "San Pedro Alcántara", "marbella": "Marbella",
              "galeon": "The Galleon · 6 m", "rioverde": "Río Verde", "alboran": "Alboran Sea", "oeste": "W", "norte": "N"},
    "parte": {
        "titulo": "Today’s sea", "lugar": "Río Verde · Puerto Banús beach",
        "agua": "Water", "aire": "Air, max.", "viento": "Wind", "oleaje": "Waves", "cielo": "Sky", "uv": "UV index",
        "puesta": "Sunset", "manana": "morning", "tarde": "afternoon",
        "fuente": "Official forecast by AEMET. I check it every morning before we go out.",
        "sin_datos": "Message me and I’ll tell you how the sea looks for your day.",
        "titulo_manana": "Tomorrow’s sea",
        "lecturas": {
            "calma": "Calm morning: ideal for a try dive or a swim stop.",
            "brisa": "A breeze in the afternoon: good sailing weather.",
            "movida": "Rough sea forecast — I’ll tell you if it’s worth going out.",
        },
        "palabras": {"flojo": "light", "moderado": "moderate", "fuerte": "strong", "débil": "calm",
                     "despejado": "clear", "poco nuboso": "partly cloudy", "intervalos nubosos": "cloudy spells",
                     "nuboso": "cloudy", "muy nuboso": "very cloudy", "cubierto": "overcast",
                     "lluvia escasa": "light rain", "lluvia": "rain", "chubascos": "showers",
                     "tormenta": "storms", "niebla": "fog", "bruma": "haze"},
    },
    "credenciales": [
        ("Oceanographer", "University of Cádiz"),
        ("Yacht Captain", "Spanish licence"),
        ("Diving instructor", "FEDAS · CMAS"),
        ("5 seasons", "skippering in Marbella"),
        ("Languages", "English · Español · Русский"),
    ],
    "exp_eyebrow": "Experiences",
    "exp_h2": "Four ways to spend a day at sea",
    "exp_intro": "Every trip is planned around you, the weather and what the sea is doing that day.",
    "experiencias": [
        {"id": "vela", "titulo": "Sailing from Puerto Banús",
         "frase": "Sails up, engine off. The quietest way to see the coast of Marbella.",
         "puntos": ["Half day, full day or sunset", "A swim stop in calm water", "Take the helm if you want to learn"],
         "cta": "Ask about sailing",
         "wa": "Hi Jose! I’d like to know more about sailing from Puerto Banús."},
        {"id": "buceo", "titulo": "Scuba diving",
         "frase": "From your very first breath underwater to an 18th-century warship at six metres.",
         "puntos": ["Try dives — no experience needed", "FEDAS · CMAS courses, valid worldwide",
                    "Guided dives and dive trips abroad"],
         "cta": "Ask about diving",
         "wa": "Hi Jose! I’d like to know more about diving with you."},
        {"id": "pesca", "titulo": "Fishing trips",
         "frase": "I’ll take you where the fish are biting — beginners, families and keen anglers alike.",
         "puntos": ["Bottom fishing or trolling", "Morning or afternoon", "New to fishing? I’ll show you how"],
         "cta": "Ask about fishing",
         "wa": "Hi Jose! I’d like to know more about your fishing trips."},
        {"id": "moto", "titulo": "Jet ski",
         "frase": "The Golden Mile from the water, at full throttle.",
         "puntos": ["Guided rides along the coast", "First time on a jet ski? I’ll brief you before we go"],
         "cta": "Ask about jet ski",
         "wa": "Hi Jose! I’d like to know more about jet ski rides."},
    ],
    "jose_eyebrow": "Who’s Jose",
    "jose_h2": "An oceanographer who made the sea his job",
    "jose_p": [
        ("I studied oceanography at the University of Cádiz. I’m a yacht captain and a FEDAS diving instructor, and "
         "I’ve spent the last five seasons skippering sailing yachts, motorboats and fishing boats out of Marbella "
         "and Puerto Banús."),
        ("So I know where the water stays calm when the wind picks up, where the dolphins usually are, and what lives "
         "on the seabed below your boat. I’ll share all of it with you — in English, Spanish or Russian."),
    ],
    "jose_foto": "Jose on a dive boat, ready to get in the water",
    "cuaderno": "Logbook",
    "bitacora": [
        ("2016", "First dives. Ten years later I’m still going back underwater."),
        ("2022", "First season as a charter skipper in Marbella."),
        ("2023", "Diving instructor (FEDAS · CMAS) and head of a charter fleet."),
        ("2025", "Sailing trips to see dolphins, and fishing charters."),
        ("2026", "Yacht Captain licence."),
    ],
    "buceo_eyebrow": "Diving in Marbella",
    "buceo_h2": "Underwater, Marbella is another city",
    "buceo_lead": ("Calm, shallow water, seagrass meadows, reefs and wrecks with centuries of history. "
                   "Whether it’s your first dive or your hundredth, there’s a plan for you."),
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
        "Its remains lie just six metres down: three centuries of history within reach of any diver, "
        "even on a try dive.",
    ],
    "pecio_datos": [("Depth", "about 6 m"), ("Level", "everyone, from a try dive"),
                    ("You’ll see", "cannons, frames and the life on the wreck")],
    "habichuelas_h": "The Beans Wreck — Punta Carnero",
    "habichuelas_p": ("The <em>Dina</em>, a 109-metre freighter that ran aground in an easterly storm in 1983 "
                      "carrying tinned beans. Today it’s a reef full of life between 8 and 12 metres."),
    "viajes_h": "Dive trips",
    "viajes_p": ("Every year I lead small-group trips to the world’s great dive destinations: the Maldives, "
                 "the Philippines, Indonesia. Tell me where you’d like to go next."),
    "fotos_buceo": {"pulpo": "An octopus on the seabed off Marbella", "ok": "Two divers giving the OK sign",
                    "tortuga": "Diving with a green turtle", "tiburon": "Divers watching a tiger shark"},
    "buceo_cta": "Ask about diving",
    "como_h2": "How a day with Jose works",
    "pasos": [
        ("Message me", "Tell me what you’d like to do, the date and how many of you are coming."),
        ("I plan it around the sea", "I check the forecast and suggest the best time and route. "
                                     "You get the price before you confirm."),
        ("Meet me at Puerto Banús", "Bring sunscreen, a towel and your swimsuit. I’ll take care of the rest."),
    ],
    "plan_h2": "Tell me your plan",
    "plan_intro": "Fill in a few details and WhatsApp opens with your message ready.",
    "plan": {"que": "What would you like to do?", "fecha": "Date", "personas": "How many people?",
             "nombre": "Your name", "notas": "Anything else?", "boton": "Send on WhatsApp",
             "nota": "Nothing is sent until you press send in WhatsApp.",
             "opciones": ["Sailing", "Scuba diving", "Fishing", "Jet ski", "Not sure yet"],
             "msg_inicio": "Hi Jose! I’d like to plan a day at sea.", "msg_actividad": "Activity",
             "msg_fecha": "Date", "msg_personas": "People", "msg_nombre": "Name", "msg_notas": "Notes"},
    "faq_h2": "Questions",
    "faq": [
        ("Do I need any experience?", "No. Sailing, fishing and jet ski are for everyone, and a try dive is designed "
                                      "for people who have never dived before. Tell me your level and I’ll adapt the plan."),
        ("Where do we meet?", "At Puerto José Banús, Marbella. I’ll send you the exact pontoon on WhatsApp."),
        ("What if the weather is bad?", "I only go out when the sea is safe and enjoyable. If it isn’t, "
                                        "we move your trip to another day."),
        ("Can children come?", "Yes, families are very welcome. Tell me their ages and I’ll suggest the right activity."),
        ("Which languages do you speak?", "English, Spanish and Russian."),
        ("How much does it cost?", "It depends on the activity, how long you want to be out and how many of you "
                                   "there are. Message me and I’ll send you the price before you confirm."),
    ],
    "final_h2": "See you at sea?",
    "final_p": "Message me on WhatsApp and I’ll get back to you with dates and prices.",
    "pie_lugar": "Puerto José Banús, 29660 Marbella (Málaga), Spain",
    "pie_legal": "Legal notice and privacy",
    "pie_creditos": "Bathymetry: EMODnet (CC BY 4.0) · Forecast: AEMET",
    "legal_title": "Legal notice and privacy — Sea With Jose",
    "legal_h1": "Legal notice and privacy",
    "legal": [
        ("Who runs this website", "Sea With Jose is the personal brand of José María Hinojosa Figueira, based in "
                                  "Marbella (Málaga, Spain). Contact: {email} · WhatsApp {tel}."),
        ("What this website does", "It presents my sea experiences and lets you contact me. It does not sell or "
                                   "take bookings: everything is agreed directly with me on WhatsApp or by email."),
        ("Your data", "If you write to me, I use your name and contact details only to answer you and organise your "
                      "trip, and I keep them only as long as that takes. You can ask me at any time to see, correct "
                      "or delete them by writing to {email}. You can also complain to the Spanish Data Protection "
                      "Agency (aepd.es)."),
        ("Cookies", "This website uses no cookies and no analytics. Fonts and images are served from the site itself."),
        ("Third parties", "The site is hosted on GitHub Pages (GitHub Inc.), which may record visitors’ IP addresses "
                          "for security. The WhatsApp and Instagram buttons take you to those services, which have "
                          "their own privacy policies."),
        ("Credits", "Bathymetry: EMODnet Bathymetry Consortium, CC BY 4.0. Beach forecast: information prepared by "
                    "the Spanish State Meteorological Agency (AEMET)."),
    ],
    "volver": "Back to the home page",
    "e404_h1": "This page is off the chart",
    "e404_p": "The address may be wrong or the page has moved.",
}

# ───────────────────────────────── ESPAÑOL ─────────────────────────────────
T["es"] = {
    "nombre_idioma": "Español", "corto": "ES", "og_locale": "es_ES",
    "title": "Sea With Jose — Vela, buceo, pesca y motos de agua en Marbella",
    "description": ("Días de mar desde Puerto Banús con Jose: oceanógrafo, capitán de yate e instructor de buceo. "
                    "Velero, buceo, pesca y motos de agua en Marbella."),
    "saltar": "Ir al contenido",
    "nav": {"experiencias": "Experiencias", "jose": "Jose", "buceo": "Buceo", "como": "Cómo funciona", "faq": "Preguntas"},
    "menu": "Menú", "whatsapp_corto": "WhatsApp",
    "hero_eyebrow": "36°29′ N · 4°57′ O — Puerto Banús, Marbella",
    "hero_h1": "El mar de Marbella, <em>con alguien que lo conoce.</em>",
    "hero_lead": ("Velero, buceo, pesca y motos de agua desde Puerto Banús. Soy Jose: oceanógrafo, capitán de yate "
                  "e instructor de buceo, y te enseño el mar como lo veo yo."),
    "hero_cta": "Organiza tu día por WhatsApp",
    "hero_cta2": "Ver experiencias",
    "carta_aria": "Carta náutica de la costa entre San Pedro Alcántara y Marbella, con las isobatas reales",
    "carta": {"banus": "Puerto José Banús", "sanpedro": "San Pedro Alcántara", "marbella": "Marbella",
              "galeon": "El Galeón · 6 m", "rioverde": "Río Verde", "alboran": "Mar de Alborán", "oeste": "O", "norte": "N"},
    "parte": {
        "titulo": "El mar hoy", "lugar": "Playa de Río Verde · Puerto Banús",
        "agua": "Agua", "aire": "Aire, máx.", "viento": "Viento", "oleaje": "Oleaje", "cielo": "Cielo", "uv": "Índice UV",
        "puesta": "Puesta de sol", "manana": "mañana", "tarde": "tarde",
        "fuente": "Previsión oficial de AEMET. La miro cada mañana antes de salir.",
        "sin_datos": "Escríbeme y te digo cómo pinta el mar para tu día.",
        "titulo_manana": "El mar mañana",
        "lecturas": {
            "calma": "Mañana en calma: ideal para un bautizo o un baño.",
            "brisa": "Brisa por la tarde: buen día para navegar a vela.",
            "movida": "Se espera mar movida: te digo si merece la pena salir.",
        },
        "palabras": {"flojo": "flojo", "moderado": "moderado", "fuerte": "fuerte", "débil": "débil",
                     "despejado": "despejado", "poco nuboso": "poco nuboso", "intervalos nubosos": "intervalos nubosos",
                     "nuboso": "nuboso", "muy nuboso": "muy nuboso", "cubierto": "cubierto",
                     "lluvia escasa": "lluvia escasa", "lluvia": "lluvia", "chubascos": "chubascos",
                     "tormenta": "tormenta", "niebla": "niebla", "bruma": "bruma"},
    },
    "credenciales": [
        ("Oceanógrafo", "Universidad de Cádiz"),
        ("Capitán de yate", "titulación española"),
        ("Instructor de buceo", "FEDAS · CMAS"),
        ("5 temporadas", "de patrón en Marbella"),
        ("Idiomas", "English · Español · Русский"),
    ],
    "exp_eyebrow": "Experiencias",
    "exp_h2": "Cuatro maneras de pasar un día en el mar",
    "exp_intro": "Cada salida se planifica contigo, con el tiempo y con lo que esté haciendo el mar ese día.",
    "experiencias": [
        {"id": "vela", "titulo": "Velero desde Puerto Banús",
         "frase": "Velas arriba y motor apagado: la forma más tranquila de ver la costa de Marbella.",
         "puntos": ["Medio día, día completo o puesta de sol", "Parada para bañarse en aguas tranquilas",
                    "Toma el timón si quieres aprender"],
         "cta": "Pregunta por el velero",
         "wa": "¡Hola Jose! Me gustaría saber más sobre las salidas en velero desde Puerto Banús."},
        {"id": "buceo", "titulo": "Buceo",
         "frase": "Desde tu primera respiración bajo el agua hasta un navío del siglo XVIII a seis metros.",
         "puntos": ["Bautizos, sin experiencia previa", "Cursos FEDAS · CMAS, válidos en todo el mundo",
                    "Inmersiones guiadas y viajes de buceo"],
         "cta": "Pregunta por el buceo",
         "wa": "¡Hola Jose! Me gustaría saber más sobre bucear contigo."},
        {"id": "pesca", "titulo": "Salidas de pesca",
         "frase": "Te llevo donde pica, seas principiante, familia o pescador con experiencia.",
         "puntos": ["Pesca a fondo o al curricán", "Por la mañana o por la tarde", "¿Es tu primera vez? Te enseño"],
         "cta": "Pregunta por la pesca",
         "wa": "¡Hola Jose! Me gustaría saber más sobre las salidas de pesca."},
        {"id": "moto", "titulo": "Motos de agua",
         "frase": "La Milla de Oro desde el mar, a todo gas.",
         "puntos": ["Rutas guiadas por la costa", "¿Primera vez en moto de agua? Te lo explico todo antes de salir"],
         "cta": "Pregunta por las motos de agua",
         "wa": "¡Hola Jose! Me gustaría saber más sobre las motos de agua."},
    ],
    "jose_eyebrow": "Quién es Jose",
    "jose_h2": "Un oceanógrafo que hizo del mar su trabajo",
    "jose_p": [
        ("Soy oceanógrafo por la Universidad de Cádiz, capitán de yate e instructor de buceo FEDAS, y llevo cinco "
         "temporadas como patrón de veleros, lanchas y barcos de pesca en Marbella y Puerto Banús."),
        ("Por eso sé dónde sigue el agua en calma cuando se levanta el viento, por dónde suelen andar los delfines y "
         "qué vive en el fondo bajo tu barco. Te lo cuento todo en inglés, en español o en ruso."),
    ],
    "jose_foto": "Jose en un barco de buceo, listo para meterse al agua",
    "cuaderno": "Cuaderno de bitácora",
    "bitacora": [
        ("2016", "Primeras inmersiones. Diez años después sigo volviendo bajo el agua."),
        ("2022", "Primera temporada como patrón de chárter en Marbella."),
        ("2023", "Instructor de buceo (FEDAS · CMAS) y responsable de una flota de chárter."),
        ("2025", "Salidas en velero para ver delfines y chárter de pesca."),
        ("2026", "Título de Capitán de Yate."),
    ],
    "buceo_eyebrow": "Buceo en Marbella",
    "buceo_h2": "Bajo el agua, Marbella es otra ciudad",
    "buceo_lead": ("Aguas tranquilas y poco profundas, praderas marinas, arrecifes y pecios con siglos de historia. "
                   "Sea tu primera inmersión o la número cien, hay un plan para ti."),
    "buceo_bloques": [
        ("Tu primera inmersión", "Aguas tranquilas y poco profundas, y yo a tu lado todo el rato. "
                                 "No hace falta experiencia: solo ganas."),
        ("Sácate el título", "Cursos FEDAS · CMAS: desde Buceador 1 Estrella (B1E), con el que buceas acompañado hasta "
                             "25 metros, hasta niveles avanzados y especialidades. Reconocidos en todo el mundo a través de CMAS."),
    ],
    "pecio_eyebrow": "Pecio frente a San Pedro Alcántara",
    "pecio_h": "El Galeón: el navío <em>Fernando</em>, 1760",
    "pecio_p": [
        ("Durante décadas todo el mundo lo llamó «el Galeón» y se decía que era francés. En 2026, el Instituto "
         "Andaluz del Patrimonio Histórico resolvió el misterio: es el <em>Fernando</em>, un navío español construido "
         "en Ferrol entre 1750 y 1751 y hundido en 1760."),
        "Sus restos descansan a solo seis metros: tres siglos de historia al alcance de cualquier buceador, "
        "incluso en un bautizo.",
    ],
    "pecio_datos": [("Profundidad", "unos 6 m"), ("Nivel", "todos, desde bautizo"),
                    ("Qué verás", "cañones, cuadernas y la vida sobre el pecio")],
    "habichuelas_h": "El barco de las Habichuelas — Punta Carnero",
    "habichuelas_p": ("El <em>Dina</em>, un mercante de 109 metros que embarrancó en un temporal de levante en 1983 "
                      "cargado de conservas de legumbres. Hoy es un arrecife lleno de vida entre 8 y 12 metros."),
    "viajes_h": "Viajes de buceo",
    "viajes_p": ("Cada año organizo viajes en grupo reducido a los grandes destinos del buceo: Maldivas, Filipinas, "
                 "Indonesia. Dime adónde te gustaría ir."),
    "fotos_buceo": {"pulpo": "Un pulpo en el fondo frente a Marbella", "ok": "Dos buceadores haciendo la señal de OK",
                    "tortuga": "Buceando junto a una tortuga verde", "tiburon": "Buceadores observando un tiburón tigre"},
    "buceo_cta": "Pregunta por el buceo",
    "como_h2": "Cómo es un día con Jose",
    "pasos": [
        ("Escríbeme", "Cuéntame qué te apetece, la fecha y cuántos sois."),
        ("Lo planifico según el mar", "Miro la previsión y te propongo la mejor hora y la mejor ruta. "
                                      "Sabrás el precio antes de confirmar."),
        ("Nos vemos en Puerto Banús", "Trae crema solar, toalla y bañador. Del resto me encargo yo."),
    ],
    "plan_h2": "Cuéntame tu plan",
    "plan_intro": "Rellena unos datos y se abrirá WhatsApp con el mensaje preparado.",
    "plan": {"que": "¿Qué te apetece?", "fecha": "Fecha", "personas": "¿Cuántas personas?",
             "nombre": "Tu nombre", "notas": "¿Algo más?", "boton": "Enviar por WhatsApp",
             "nota": "No se envía nada hasta que pulses enviar en WhatsApp.",
             "opciones": ["Velero", "Buceo", "Pesca", "Moto de agua", "Aún no lo sé"],
             "msg_inicio": "¡Hola Jose! Quiero organizar un día de mar.", "msg_actividad": "Actividad",
             "msg_fecha": "Fecha", "msg_personas": "Personas", "msg_nombre": "Nombre", "msg_notas": "Comentarios"},
    "faq_h2": "Preguntas",
    "faq": [
        ("¿Necesito experiencia?", "No. El velero, la pesca y las motos de agua son para todo el mundo, y el bautizo "
                                   "de buceo está pensado para quien nunca ha buceado. Cuéntame tu nivel y adapto el plan."),
        ("¿Dónde quedamos?", "En Puerto José Banús, Marbella. Te mando el pantalán exacto por WhatsApp."),
        ("¿Y si hace mal tiempo?", "Solo salgo cuando el mar está seguro y apetece. Si no lo está, "
                                   "pasamos tu salida a otro día."),
        ("¿Pueden venir niños?", "Sí, las familias son bienvenidas. Dime sus edades y te propongo la actividad adecuada."),
        ("¿En qué idiomas hablas?", "Inglés, español y ruso."),
        ("¿Cuánto cuesta?", "Depende de la actividad, del tiempo que quieras estar en el mar y de cuántos seáis. "
                            "Escríbeme y te paso el precio antes de confirmar."),
    ],
    "final_h2": "¿Nos vemos en el mar?",
    "final_p": "Escríbeme por WhatsApp y te respondo con fechas y precios.",
    "pie_lugar": "Puerto José Banús, 29660 Marbella (Málaga)",
    "pie_legal": "Aviso legal y privacidad",
    "pie_creditos": "Batimetría: EMODnet (CC BY 4.0) · Previsión: AEMET",
    "legal_title": "Aviso legal y privacidad — Sea With Jose",
    "legal_h1": "Aviso legal y privacidad",
    "legal": [
        ("Titular", "Sea With Jose es la marca personal de José María Hinojosa Figueira, con domicilio en Marbella "
                    "(Málaga). Contacto: {email} · WhatsApp {tel}."),
        ("Qué hace esta web", "Presenta mis experiencias en el mar y te permite contactar conmigo. No vende ni reserva "
                              "nada: todo se acuerda directamente conmigo por WhatsApp o por correo."),
        ("Tus datos", "Si me escribes, uso tu nombre y tus datos de contacto solo para responderte y organizar tu "
                      "salida, y los conservo únicamente el tiempo necesario para ello. Puedes pedirme en cualquier "
                      "momento verlos, corregirlos o borrarlos escribiendo a {email}, y reclamar ante la Agencia "
                      "Española de Protección de Datos (aepd.es)."),
        ("Cookies", "Esta web no usa cookies ni herramientas de analítica. Las tipografías y las imágenes se sirven "
                    "desde la propia web."),
        ("Terceros", "La web está alojada en GitHub Pages (GitHub Inc.), que puede registrar las direcciones IP de las "
                     "visitas por seguridad. Los botones de WhatsApp e Instagram te llevan a esos servicios, que tienen "
                     "sus propias políticas de privacidad."),
        ("Créditos", "Batimetría: EMODnet Bathymetry Consortium, CC BY 4.0. Previsión de playas: información elaborada "
                     "por la Agencia Estatal de Meteorología (AEMET)."),
    ],
    "volver": "Volver al inicio",
    "e404_h1": "Esta página está fuera de la carta",
    "e404_p": "Puede que la dirección esté mal escrita o que la página haya cambiado de sitio.",
}

# ───────────────────────────────── RUSO ─────────────────────────────────
T["ru"] = {
    "nombre_idioma": "Русский", "corto": "RU", "og_locale": "ru_RU",
    "title": "Sea With Jose — парус, дайвинг, рыбалка и гидроциклы в Марбелье",
    "description": ("Дни в море из Пуэрто-Бануса с Хосе — океанографом, капитаном яхты и инструктором по дайвингу. "
                    "Парусные прогулки, дайвинг, рыбалка и гидроциклы в Марбелье."),
    "saltar": "Перейти к содержанию",
    "nav": {"experiencias": "Чем заняться", "jose": "Хосе", "buceo": "Дайвинг", "como": "Как это работает", "faq": "Вопросы"},
    "menu": "Меню", "whatsapp_corto": "WhatsApp",
    "hero_eyebrow": "36°29′ с. ш. · 4°57′ з. д. — Пуэрто-Банус, Марбелья",
    "hero_h1": "Море Марбельи — <em>с тем, кто его знает.</em>",
    "hero_lead": ("Парус, дайвинг, рыбалка и гидроциклы из Пуэрто-Бануса. Я Хосе: океанограф, капитан яхты и "
                  "инструктор по дайвингу — и покажу вам море таким, каким вижу его сам."),
    "hero_cta": "Спланировать день в WhatsApp",
    "hero_cta2": "Посмотреть предложения",
    "carta_aria": "Морская карта побережья между Сан-Педро-Алькантара и Марбельей с реальными изобатами",
    "carta": {"banus": "Пуэрто-Хосе-Банус", "sanpedro": "Сан-Педро-Алькантара", "marbella": "Марбелья",
              "galeon": "«Галеон» · 6 м", "rioverde": "Рио-Верде", "alboran": "Море Альборан", "oeste": "W", "norte": "N"},
    "parte": {
        "titulo": "Море сегодня", "lugar": "Пляж Рио-Верде · Пуэрто-Банус",
        "agua": "Вода", "aire": "Воздух, макс.", "viento": "Ветер", "oleaje": "Волнение", "cielo": "Небо",
        "uv": "УФ-индекс", "puesta": "Закат", "manana": "утром", "tarde": "днём",
        "fuente": "Официальный прогноз AEMET. Я проверяю его каждое утро перед выходом в море.",
        "sin_datos": "Напишите мне — расскажу, каким будет море в ваш день.",
        "titulo_manana": "Море завтра",
        "lecturas": {
            "calma": "Спокойное утро: идеально для пробного погружения или купания.",
            "brisa": "Днём ветерок: хорошая погода для паруса.",
            "movida": "Ожидается волнение — подскажу, стоит ли выходить.",
        },
        "palabras": {"flojo": "слабый", "moderado": "умеренный", "fuerte": "сильный", "débil": "слабое",
                     "despejado": "ясно", "poco nuboso": "малооблачно", "intervalos nubosos": "переменная облачность",
                     "nuboso": "облачно", "muy nuboso": "значительная облачность", "cubierto": "пасмурно",
                     "lluvia escasa": "небольшой дождь", "lluvia": "дождь", "chubascos": "ливни",
                     "tormenta": "гроза", "niebla": "туман", "bruma": "дымка"},
    },
    "credenciales": [
        ("Океанограф", "Университет Кадиса"),
        ("Капитан яхты", "испанский диплом"),
        ("Инструктор по дайвингу", "FEDAS · CMAS"),
        ("5 сезонов", "шкипером в Марбелье"),
        ("Языки", "English · Español · Русский"),
    ],
    "exp_eyebrow": "Чем заняться",
    "exp_h2": "Четыре способа провести день в море",
    "exp_intro": "Каждый выход в море планируется под вас, погоду и то, каким будет море в этот день.",
    "experiencias": [
        {"id": "vela", "titulo": "Под парусом из Пуэрто-Бануса",
         "frase": "Паруса подняты, мотор выключен. Самый спокойный способ увидеть побережье Марбельи.",
         "puntos": ["Полдня, целый день или закат", "Остановка для купания в спокойной воде",
                    "Можно встать за штурвал и научиться"],
         "cta": "Спросить о парусной прогулке",
         "wa": "Здравствуйте, Хосе! Хотел(а) бы узнать подробнее о прогулке под парусом из Пуэрто-Бануса."},
        {"id": "buceo", "titulo": "Дайвинг",
         "frase": "От первого вдоха под водой до военного корабля XVIII века на глубине шести метров.",
         "puntos": ["Пробное погружение — опыт не нужен", "Курсы FEDAS · CMAS, признаются во всём мире",
                    "Погружения с гидом и дайв-туры за границу"],
         "cta": "Спросить о дайвинге",
         "wa": "Здравствуйте, Хосе! Хотел(а) бы узнать подробнее о дайвинге с вами."},
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
    "jose_eyebrow": "Кто такой Хосе",
    "jose_h2": "Океанограф, который сделал море своей работой",
    "jose_p": [
        ("Я изучал океанографию в Университете Кадиса, у меня диплом капитана яхты и инструктора по дайвингу FEDAS, "
         "а последние пять сезонов я работаю шкипером на парусных яхтах, моторных катерах и рыболовных лодках "
         "в Марбелье и Пуэрто-Банусе."),
        ("Поэтому я знаю, где вода остаётся спокойной, когда поднимается ветер, где обычно встречаются дельфины и кто "
         "живёт на дне под вашей лодкой. Расскажу обо всём — по-английски, по-испански или по-русски."),
    ],
    "jose_foto": "Хосе на дайв-боте перед погружением",
    "cuaderno": "Судовой журнал",
    "bitacora": [
        ("2016", "Первые погружения. Десять лет спустя я всё так же возвращаюсь под воду."),
        ("2022", "Первый сезон шкипером чартеров в Марбелье."),
        ("2023", "Инструктор по дайвингу (FEDAS · CMAS) и руководитель чартерного флота."),
        ("2025", "Парусные выходы к дельфинам и рыболовные чартеры."),
        ("2026", "Диплом капитана яхты."),
    ],
    "buceo_eyebrow": "Дайвинг в Марбелье",
    "buceo_h2": "Под водой Марбелья — другой город",
    "buceo_lead": ("Спокойная мелкая вода, луга морских трав, рифы и затонувшие корабли с многовековой историей. "
                   "Первое это погружение или сотое — план для вас найдётся."),
    "buceo_bloques": [
        ("Первое погружение", "Спокойная неглубокая вода, и я всё время рядом с вами. "
                              "Опыт не нужен — только любопытство."),
        ("Получите сертификат", "Курсы FEDAS · CMAS: от «Дайвера одной звезды» (B1E), с которым можно погружаться "
                                "с напарником до 25 метров, до продвинутых уровней и специализаций. "
                                "Сертификаты признаются во всём мире через CMAS."),
    ],
    "pecio_eyebrow": "Затонувший корабль у Сан-Педро-Алькантара",
    "pecio_h": "«Галеон»: линейный корабль <em>«Фернандо»</em>, 1760 год",
    "pecio_p": [
        ("Десятилетиями все называли его «Галеоном» и считали французским. В 2026 году Андалусский институт "
         "исторического наследия раскрыл тайну: это <em>«Фернандо»</em> — испанский линейный корабль, построенный "
         "в Ферроле в 1750–1751 годах и погибший в 1760-м."),
        "Его остатки лежат всего в шести метрах под поверхностью: три века истории, доступные любому дайверу, "
        "даже на пробном погружении.",
    ],
    "pecio_datos": [("Глубина", "около 6 м"), ("Уровень", "любой, с пробного погружения"),
                    ("Что увидите", "пушки, шпангоуты и жизнь на корабле")],
    "habichuelas_h": "«Корабль с фасолью» — Пунта-Карнеро",
    "habichuelas_p": ("<em>«Дина»</em> — 109-метровое грузовое судно, севшее на мель во время восточного шторма "
                      "в 1983 году с грузом консервированной фасоли. Сегодня это риф, полный жизни, "
                      "на глубине от 8 до 12 метров."),
    "viajes_h": "Дайв-туры",
    "viajes_p": ("Каждый год я вожу небольшие группы к великим дайв-направлениям мира: Мальдивы, Филиппины, "
                 "Индонезия. Расскажите, куда хотите поехать в следующий раз."),
    "fotos_buceo": {"pulpo": "Осьминог на дне у берегов Марбельи", "ok": "Два дайвера показывают знак «всё в порядке»",
                    "tortuga": "Погружение рядом с зелёной черепахой", "tiburon": "Дайверы наблюдают за тигровой акулой"},
    "buceo_cta": "Спросить о дайвинге",
    "como_h2": "Как проходит день с Хосе",
    "pasos": [
        ("Напишите мне", "Расскажите, чем хотите заняться, какого числа и сколько вас будет."),
        ("Я планирую по морю", "Проверю прогноз и предложу лучшее время и маршрут. "
                               "Цену вы узнаете до подтверждения."),
        ("Встречаемся в Пуэрто-Банусе", "Возьмите солнцезащитный крем, полотенце и купальник. Остальное — на мне."),
    ],
    "plan_h2": "Расскажите о своих планах",
    "plan_intro": "Заполните несколько полей — WhatsApp откроется с готовым сообщением.",
    "plan": {"que": "Чем хотите заняться?", "fecha": "Дата", "personas": "Сколько человек?",
             "nombre": "Как вас зовут?", "notas": "Что-нибудь ещё?", "boton": "Отправить в WhatsApp",
             "nota": "Сообщение уйдёт, только когда вы нажмёте «Отправить» в WhatsApp.",
             "opciones": ["Парусная прогулка", "Дайвинг", "Рыбалка", "Гидроцикл", "Пока не знаю"],
             "msg_inicio": "Здравствуйте, Хосе! Хочу спланировать день в море.", "msg_actividad": "Занятие",
             "msg_fecha": "Дата", "msg_personas": "Человек", "msg_nombre": "Имя", "msg_notas": "Комментарий"},
    "faq_h2": "Вопросы",
    "faq": [
        ("Нужен ли опыт?", "Нет. Парусные прогулки, рыбалка и гидроциклы подходят всем, а пробное погружение "
                           "рассчитано на тех, кто никогда не нырял. Расскажите о своём уровне, и я подстрою план."),
        ("Где встречаемся?", "В Пуэрто-Хосе-Банусе, Марбелья. Точный понтон пришлю в WhatsApp."),
        ("А если погода плохая?", "Я выхожу в море, только когда это безопасно и приятно. "
                                  "Если нет — перенесём выход на другой день."),
        ("Можно с детьми?", "Да, семьям всегда рады. Напишите возраст детей, и я предложу подходящее занятие."),
        ("На каких языках вы говорите?", "На английском, испанском и русском."),
        ("Сколько это стоит?", "Зависит от занятия, продолжительности и количества человек. Напишите мне, "
                               "и я пришлю цену до подтверждения."),
    ],
    "final_h2": "Увидимся в море?",
    "final_p": "Напишите мне в WhatsApp — отвечу с датами и ценами.",
    "pie_lugar": "Пуэрто-Хосе-Банус, 29660 Марбелья (Малага), Испания",
    "pie_legal": "Правовая информация и конфиденциальность",
    "pie_creditos": "Батиметрия: EMODnet (CC BY 4.0) · Прогноз: AEMET",
    "legal_title": "Правовая информация и конфиденциальность — Sea With Jose",
    "legal_h1": "Правовая информация и конфиденциальность",
    "legal": [
        ("Владелец сайта", "Sea With Jose — личный бренд Хосе Марии Инохосы Фигейры (José María Hinojosa Figueira), "
                           "Марбелья (Малага, Испания). Контакты: {email} · WhatsApp {tel}."),
        ("Назначение сайта", "Сайт рассказывает о моих морских программах и позволяет связаться со мной. Здесь ничего "
                             "не продаётся и не бронируется: всё согласуется напрямую со мной в WhatsApp или по почте."),
        ("Ваши данные", "Если вы мне пишете, я использую ваше имя и контакты только для ответа и организации выхода в "
                        "море и храню их лишь столько, сколько нужно для этого. В любой момент вы можете попросить "
                        "показать, исправить или удалить их, написав на {email}, а также подать жалобу в Испанское "
                        "агентство по защите данных (aepd.es)."),
        ("Cookies", "Сайт не использует cookies и аналитику. Шрифты и изображения загружаются с самого сайта."),
        ("Третьи лица", "Сайт размещён на GitHub Pages (GitHub Inc.), который может записывать IP-адреса посетителей "
                        "в целях безопасности. Кнопки WhatsApp и Instagram ведут на эти сервисы, у которых свои "
                        "правила конфиденциальности."),
        ("Источники", "Батиметрия: EMODnet Bathymetry Consortium, CC BY 4.0. Прогноз для пляжей: информация "
                      "Государственного метеорологического агентства Испании (AEMET)."),
    ],
    "volver": "На главную",
    "e404_h1": "Этой страницы нет на карте",
    "e404_p": "Возможно, адрес набран с ошибкой или страница переехала.",
}
