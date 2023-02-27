import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial import distance
from fonction_utiles import doc_without_stop_word, lemma, similaire


def doc_plus_pertinent(requete):
    ## data apres traitement
    data = pd.read_csv('article_traitement.csv')
    nlp = spacy.load("fr_core_news_sm")
    
    # Liste des termes à retenir de la requête
    requete_filtre=[]
    # Traiter la requête
    doc = nlp(requete)
    requete_filtre = doc_without_stop_word(doc)
    requete_filtre = lemma(requete_filtre)
    ## On ajoute la requete à la fin du dataframe
    data=data.append({'identifiantArticle' : 'la requete','text_filtre' : requete_filtre}, ignore_index=True)
    #data=pd.concat([pd.DataFrame(data), pd.DataFrame([{'identifiantArticle' : 'la requete','text_filtre' : requete_filtre}])], ignore_index=True)
    ### Représentation des données 
    vectorizer = TfidfVectorizer(sublinear_tf=True,min_df=5,max_df=0.95)
    tfidf_dtm=vectorizer.fit_transform(data['text_filtre'])
    tfidf_dtm.shape
    termsVect = vectorizer.get_feature_names_out()
    tdidf_df = pd.DataFrame(tfidf_dtm.toarray(), columns=termsVect)

    N = len(data)-1
    ### vecteur de la requete
    ##Le dernier element du dataFrame
    request = tdidf_df.iloc[N,:].values
    
    plus_pertinent = similaire(tdidf_df,request,data,30)
    if len(plus_pertinent) > 0 :
        doc_json = plus_pertinent.to_json(orient='records')
        return doc_json
    else:
        return {requete:"NOT FOUND !"}
    

    