"""
Datos de entrada del modelo. Editá libremente estos valores:
 - ELO: rating de fuerza de cada selección (fuente: DTAI KU Leuven, pre-torneo).
   Bajá/subí un número para simular lesiones o forma (ej: España sin Yamal -> 1979 a ~1945).
 - FIXTURE: los 72 partidos de fase de grupos. host = anfitrión con localía (o None).
"""

# Rating Elo por selección (DTAI KU Leuven, 20.000 simulaciones, pre-torneo)
ELO = {
    "Mexico": 1800, "Sudafrica": 1526, "Corea del Sur": 1754, "Chequia": 1691,
    "Canada": 1741, "Suiza": 1781, "Qatar": 1591, "Bosnia": 1589,
    "Brasil": 1885, "Marruecos": 1736, "Escocia": 1684, "Haiti": 1583,
    "Estados Unidos": 1765, "Paraguay": 1706, "Australia": 1747, "Turquia": 1771,
    "Alemania": 1867, "Curazao": 1520, "Costa de Marfil": 1618, "Ecuador": 1793,
    "Paises Bajos": 1868, "Japon": 1833, "Suecia": 1701, "Tunez": 1583,
    "Belgica": 1816, "Egipto": 1632, "Iran": 1757, "Nueva Zelanda": 1599,
    "Espana": 1979, "Uruguay": 1803, "Arabia Saudita": 1616, "Cabo Verde": 1489,
    "Francia": 1939, "Senegal": 1727, "Noruega": 1746, "Irak": 1653,
    "Argentina": 1965, "Argelia": 1659, "Austria": 1749, "Jordania": 1628,
    "Portugal": 1874, "Colombia": 1855, "Uzbekistan": 1711, "RD Congo": 1538,
    "Inglaterra": 1886, "Croacia": 1821, "Ghana": 1478, "Panama": 1699,
}

# Equipos de los 12 grupos (para encabezados y reportes)
GRUPOS = {
    "A": ["Mexico", "Sudafrica", "Corea del Sur", "Chequia"],
    "B": ["Canada", "Suiza", "Qatar", "Bosnia"],
    "C": ["Brasil", "Marruecos", "Escocia", "Haiti"],
    "D": ["Estados Unidos", "Paraguay", "Australia", "Turquia"],
    "E": ["Alemania", "Ecuador", "Costa de Marfil", "Curazao"],
    "F": ["Paises Bajos", "Japon", "Suecia", "Tunez"],
    "G": ["Belgica", "Iran", "Egipto", "Nueva Zelanda"],
    "H": ["Espana", "Uruguay", "Arabia Saudita", "Cabo Verde"],
    "I": ["Francia", "Senegal", "Noruega", "Irak"],
    "J": ["Argentina", "Austria", "Argelia", "Jordania"],
    "K": ["Portugal", "Colombia", "Uzbekistan", "RD Congo"],
    "L": ["Inglaterra", "Croacia", "Panama", "Ghana"],
}

# Anfitriones que juegan de local en su país (reciben bonus de Elo)
HOSTS = {"Mexico", "Estados Unidos", "Canada"}

# Los 72 partidos: (grupo, local, visitante, jornada, anfitrion_local_o_None)
FIXTURE = [
    ("A", "Mexico", "Sudafrica", 1, "Mexico"), ("A", "Corea del Sur", "Chequia", 1, None),
    ("A", "Chequia", "Sudafrica", 2, None), ("A", "Mexico", "Corea del Sur", 2, "Mexico"),
    ("A", "Chequia", "Mexico", 3, "Mexico"), ("A", "Corea del Sur", "Sudafrica", 3, None),
    ("B", "Canada", "Bosnia", 1, "Canada"), ("B", "Qatar", "Suiza", 1, None),
    ("B", "Suiza", "Bosnia", 2, None), ("B", "Canada", "Qatar", 2, "Canada"),
    ("B", "Suiza", "Canada", 3, "Canada"), ("B", "Bosnia", "Qatar", 3, None),
    ("C", "Brasil", "Marruecos", 1, None), ("C", "Haiti", "Escocia", 1, None),
    ("C", "Escocia", "Marruecos", 2, None), ("C", "Brasil", "Haiti", 2, None),
    ("C", "Brasil", "Escocia", 3, None), ("C", "Marruecos", "Haiti", 3, None),
    ("D", "Estados Unidos", "Paraguay", 1, "Estados Unidos"), ("D", "Australia", "Turquia", 1, None),
    ("D", "Estados Unidos", "Australia", 2, "Estados Unidos"), ("D", "Turquia", "Paraguay", 2, None),
    ("D", "Turquia", "Estados Unidos", 3, "Estados Unidos"), ("D", "Paraguay", "Australia", 3, None),
    ("E", "Alemania", "Curazao", 1, None), ("E", "Costa de Marfil", "Ecuador", 1, None),
    ("E", "Alemania", "Costa de Marfil", 2, None), ("E", "Ecuador", "Curazao", 2, None),
    ("E", "Ecuador", "Alemania", 3, None), ("E", "Curazao", "Costa de Marfil", 3, None),
    ("F", "Paises Bajos", "Japon", 1, None), ("F", "Suecia", "Tunez", 1, None),
    ("F", "Paises Bajos", "Suecia", 2, None), ("F", "Tunez", "Japon", 2, None),
    ("F", "Japon", "Suecia", 3, None), ("F", "Tunez", "Paises Bajos", 3, None),
    ("G", "Belgica", "Egipto", 1, None), ("G", "Iran", "Nueva Zelanda", 1, None),
    ("G", "Belgica", "Iran", 2, None), ("G", "Nueva Zelanda", "Egipto", 2, None),
    ("G", "Egipto", "Iran", 3, None), ("G", "Nueva Zelanda", "Belgica", 3, None),
    ("H", "Espana", "Cabo Verde", 1, None), ("H", "Arabia Saudita", "Uruguay", 1, None),
    ("H", "Espana", "Arabia Saudita", 2, None), ("H", "Uruguay", "Cabo Verde", 2, None),
    ("H", "Cabo Verde", "Arabia Saudita", 3, None), ("H", "Uruguay", "Espana", 3, None),
    ("I", "Francia", "Senegal", 1, None), ("I", "Irak", "Noruega", 1, None),
    ("I", "Francia", "Irak", 2, None), ("I", "Noruega", "Senegal", 2, None),
    ("I", "Noruega", "Francia", 3, None), ("I", "Senegal", "Irak", 3, None),
    ("J", "Argentina", "Argelia", 1, None), ("J", "Austria", "Jordania", 1, None),
    ("J", "Argentina", "Austria", 2, None), ("J", "Jordania", "Argelia", 2, None),
    ("J", "Jordania", "Argentina", 3, None), ("J", "Argelia", "Austria", 3, None),
    ("K", "Portugal", "RD Congo", 1, None), ("K", "Uzbekistan", "Colombia", 1, None),
    ("K", "Portugal", "Uzbekistan", 2, None), ("K", "Colombia", "RD Congo", 2, None),
    ("K", "Colombia", "Portugal", 3, None), ("K", "RD Congo", "Uzbekistan", 3, None),
    ("L", "Inglaterra", "Croacia", 1, None), ("L", "Ghana", "Panama", 1, None),
    ("L", "Inglaterra", "Ghana", 2, None), ("L", "Panama", "Croacia", 2, None),
    ("L", "Panama", "Inglaterra", 3, None), ("L", "Croacia", "Ghana", 3, None),
]
