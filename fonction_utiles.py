
import pandas as pd
import spacy
from scipy.spatial import distance

nlp = spacy.load("fr_core_news_sm")

# Définition de Fonction doc_without_stop_word pour le pre-traitement des textes
def doc_without_stop_word(text):
    doc = nlp(text)
    filtered = [str(token.text).lower() for token in doc if token.is_stop==False and token.text.isalpha()==True]
    filtered_text = ' '.join(filtered)
    return filtered_text


## Une foction qui lemmatise un text
def lemma(text):
    doc = nlp(text)
    filtered_text = ""
    for token in doc:
        if filtered_text=="":
            filtered_text = filtered_text+token.lemma_
        else:
            filtered_text = filtered_text+' '+token.lemma_
    return filtered_text

## Similarité cosinus
### On calcul les documents les plus similaire par rapport à la requete
def similaire(tab_vector,request,data,topN=50):
    my_df = []
    taille = len(data)-1
    for i in range(taille):
        # vecteur de chaque texte
        doc_vect = tab_vector.iloc[i,:].values
        # distance cosinus entre les deux vecteurs
        cos_dist = distance.cosine(doc_vect.tolist(), request.tolist())
        sim_cos = 1 - cos_dist
        if sim_cos<1:
            d = {
                'identifiantArticle': data.iloc[i,1],
                'titreArticle': data.iloc[i,6],
                'similarite': sim_cos,
                'contenuArticle': data.iloc[i,7]
            }
            my_df.append(d)
    ##On trie
    if len(my_df) > 0 :
        my_similaire = pd.DataFrame(my_df)
        ##Trier du plus pertinent au moins pertinent 
        my_similaire = my_similaire.sort_values(by = 'similarite', ascending = False)
        ##On retourne les topN les plus pertinents 
        return my_similaire.iloc[0:topN]
    else:
        return my_df
    
    