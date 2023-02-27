from flask import Flask , request

from doc_plus_pertinent import doc_plus_pertinent


app = Flask(__name__)

@app.route('/api/v1/articles/<string:sujet_rechercher>', methods=['GET'])
def process_json(sujet_rechercher):

    response = doc_plus_pertinent(sujet_rechercher)

    return response


