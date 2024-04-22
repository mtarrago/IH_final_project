import json
import math
from collections import defaultdict
from flask import Flask, abort, request
from flask_basicauth import BasicAuth
from flask_swagger_ui import get_swaggerui_blueprint
import pymysql

app = Flask(__name__)
app.config.from_file("flask_config.json", load=json.load)
auth = BasicAuth(app)

swaggerui_blueprint = get_swaggerui_blueprint(
    base_url='/docs',
    api_url='/static/openapi.yaml',
)
app.register_blueprint(swaggerui_blueprint)

MAX_PAGE_SIZE = 10

def remove_null_fields(obj):
    return {k:v for k, v in obj.items() if v is not None}

@app.route("/species/<species_id>")
@auth.required
def species(species_id):
    db_conn = pymysql.connect(host="localhost", user="root", database="biodiversity",
                              password= 'Eatyourdinner0991',
                              cursorclass=pymysql.cursors.DictCursor)

    with db_conn.cursor() as cursor:
        cursor.execute("""SELECT
                s.species_id,
                s.park_name,
                s.Category,
                s.sc_order,
                s.Family,
                s.scientific_name,
                s.common_names
            FROM species s
            WHERE s.species_id=%s
        """, (species_id, ))
        species = cursor.fetchone()
        if not species:
            abort(404)
        species = remove_null_fields(species)

    db_conn.close()
    return species



@app.route("/species")
@auth.required
def all_species():
    # URL parameters
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)
    include_details = bool(int(request.args.get('include_details', 0)))
    db_conn = pymysql.connect(host="localhost", user="root", database="biodiversity",
                              password='Eatyourdinner0991',
                              cursorclass=pymysql.cursors.DictCursor)
    # Get the movies
    with db_conn.cursor() as cursor:
        cursor.execute("""SELECT
                s.species_id,
                s.park_name,
                s.Category,
                s.sc_order,
                s.Family,
                s.scientific_name,
                s.common_names
            FROM species s
            ORDER BY s.species_id
            LIMIT %s
            OFFSET %s
        """, (page_size, page * page_size))
        all_species = cursor.fetchall()
        species_id = [spec['species_id'] for spec in all_species]
    return all_species
  
#     if include_details:
#         # Get genres
#         with db_conn.cursor() as cursor:
#             placeholder = ','.join(['%s'] * len(movie_ids))
#             cursor.execute(f"SELECT * FROM MoviesGenres WHERE movieId IN ({placeholder})",
#                         movie_ids)
#             genres = cursor.fetchall()
#         genres_dict = defaultdict(list)
#         for obj in genres:
#             genres_dict[obj['movieId']].append(obj['genre'])
      
#         # Get people
#         with db_conn.cursor() as cursor:
#             placeholder = ','.join(['%s'] * len(movie_ids))
#             cursor.execute(f"""
#                 SELECT
#                     MP.movieId,
#                     P.personId,
#                     P.primaryName AS name,
#                     P.birthYear,
#                     P.deathYear,
#                     MP.category AS role
#                 FROM MoviesPeople MP
#                 JOIN People P on P.personId = MP.personId
#                 WHERE movieId IN ({placeholder})
#             """, movie_ids)
#             people = cursor.fetchall()
#         people_dict = defaultdict(list)
#         for obj in people:
#             movieId = obj['movieId']
#             del obj['movieId']
#             people_dict[movieId].append(obj)
#         # Merge genres and people into movies
#         for movie in movies:
#             movieId = movie['movieId']
#             movie['genres'] = genres_dict[movieId]
#             movie['people'] = people_dict[movieId]
     # Get the total species count
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM species")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)
    db_conn.close()    
    return {
        'species': species,
        'next_page': f'/species?page={page+1}&page_size={page_size}&include_details={int(include_details)}',
        'last_page': f'/species?page={last_page}&page_size={page_size}&include_details={int(include_details)}',
    }


#    return {
#        'species': species,
#        'next_page': f'/species?page={page+1}&page_size={page_size}}&include_details={int(include_details)}',
#        'last_page': f'/species?page={last_page}&page_size={page_size}}&include_details={int(include_details)}',
#    }

#'species': species,
#        'next_page': f'/species?page={page+1}&page_size={page_size}',
#        'last_page': f'/species?page={last_page}&page_size={page_size}'