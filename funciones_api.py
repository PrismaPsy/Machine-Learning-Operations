from fastapi import FastAPI
import ast
import pandas as pd

rt_csv = 'Machine Learning Operations Steam/steam_games_procesado.csv'
steam_games = pd.read_csv(rt_csv)

app = FastAPI()

@app.get('/generos_mas_ofrecidos/{year}')
def get_generos_mas_ofrecidos(year: int):
    steam_games_filtrado = steam_games[steam_games['release_date'] == year]
    steam_games_filtrado = steam_games_filtrado.dropna(subset=['genres'])
    steam_games_filtrado['genres'] = steam_games_filtrado['genres'].apply(ast.literal_eval)
    
    generos_count = {}
    
    for lista_generos in steam_games_filtrado["genres"]:
        for genero in lista_generos:
            generos_count[genero] = generos_count.get(genero, 0) + 1
    generos_mas_ofrecidos = sorted(generos_count.items(), key = lambda x: x[1], reverse = True)
    return {'generos_ofrecidos' : generos_mas_ofrecidos[:5]}

@app.get('/juegos_lanzados/{year}')
def get_juegos_lanzados(year: int):
    steam_games_filtrado = steam_games[steam_games['release_date'] == year]
    juegos_lanzados = steam_games_filtrado['title'].tolist()
    return {'juegos_lanzados' : juegos_lanzados}

@app.get('/especificaciones_comunes/{year}')
def get_especificaciones_comunes(year: int):
    steam_games_filtrado = steam_games[steam_games['release_date'] == year]
    steam_games_filtrado = steam_games_filtrado.dropna(subset=['specs'])
    steam_games_filtrado['specs'] = steam_games_filtrado['specs'].apply(ast.literal_eval)
    specs_count = {}
    for lista_specs in steam_games_filtrado['specs']:
        for spec in lista_specs:
            specs_count[spec] = specs_count.get(spec, 0) + 1
    especificaciones_comunes = sorted(specs_count.items(), key = lambda x: x[1], reverse = True)
    return {'especificaciones_mas_comunes' : especificaciones_comunes[:5]}

@app.get('/early_acces/{year}')
def get_early_acces(year: int):
    steam_games_filtrado = steam_games[(steam_games['release_date'] == year) & (steam_games['early_access'] == True)]
    juegos_early_acces = steam_games_filtrado['title'].tolist()
    return {'juegos_early_acces' : juegos_early_acces}

@app.get('/analisis_de_sentimiento/{year}')
def get_analisis_de_sentimiento(year: int):
    steam_games_filtrado = steam_games[steam_games['release_date'] == year]
    registros = steam_games_filtrado.groupby('sentiment').size().reset_index(name = 'count')
    resultado = registros.to_dict(orient = 'records')
    return {'analisis_de_sentimiento' : resultado}

@app.get('/top_juegos_metascore/{year}')
def get_top_juegos_metascore(year: int):
    steam_games_filtrado = steam_games[(steam_games['release_date'] == year) & (~steam_games['metascore'].isnull())]
    steam_games_filtrado = steam_games_filtrado.dropna(subset = ['metascore'])
    steam_games_ordenado = steam_games_filtrado.sort_values(by = 'metascore', ascending = False)
    top_juegos = steam_games_ordenado.head(5)
    resultado = top_juegos[['title', 'metascore']].to_dict(orient = 'records')
    return {'top_juegos_metascore' : resultado}
