import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

whiskas=pd.read_csv('C:/Users/PREDATOR/PycharmProjects/Study/mev/whiskas.csv')
laptop=pd.read_csv('C:/Users/PREDATOR/PycharmProjects/Study/mev/laptop.csv')
kulkas=pd.read_csv('C:/Users/PREDATOR/PycharmProjects/Study/mev/kulkas.csv')
parfume=pd.read_csv('C:/Users/PREDATOR/PycharmProjects/Study/mev/parfume.csv')
tanamanhias=pd.read_csv('C:/Users/PREDATOR/PycharmProjects/Study/mev/tanaman%20hias.csv')
df=pd.DataFrame(columns=['name', 'category', 'rating', 'shopid', 'price'])
data=df.append([whiskas,laptop,kulkas,parfume,tanamanhias])
data.reset_index(drop=True, inplace=True)
dataset=data[['name','category']]

dataset.head()


#Text Mining

#case folding
def casefolding(sentence):
    killpunctuation = str.maketrans('', '', r"-[]()\"#/*!$%^&@;:<>'{}-=~|.?,")
    sentence=sentence.lower()
    sentence=sentence.strip(" ")
    sentence = sentence.translate(killpunctuation)
    return sentence
dataset['name']=dataset['name'].apply(casefolding)
dataset.head()

#Tokenizing
def token (sentence):
    strings=sentence.split(' ')
    kosong=[]
    a=-1
    for word in strings:
        a=a+1
        if word == '':
            kosong.append(a)
    b=0
    c=0
    for d in kosong:
        c=d-b
        del strings[c]
        b=b+1
    return strings
dataset['name']=dataset['name'].apply(token)
dataset.head()


#Filtering

def buangstopwords(sentence) :
    filters=stopwords.words('indonesian','english')
    a=[]
    words=[]
    def labeling(a):
        if a in filters:
            return False
        else:
            return True
    fil=filter(labeling,sentence)
    for a in fil:
        words.append(a)
    return words
dataset['name']=dataset['name'].apply(buangstopwords)
dataset.head()


#Stemming

def stemming(sentence):
    factory=StemmerFactory()
    stems= factory.create_stemmer()
    a=[]
    for w in sentence:
        b=stems.stem(w)
        a.append(b)
    bersih=[]
    bersih=" ".join(a)
    print(bersih)
    return(bersih)
dataset['name']=dataset['name'].apply(stemming)

dataset.to_csv('data_bersih.csv',index=False)

#load saved data
dataclean=pd.read_csv('data_bersih.csv',encoding='latin1')
dataclean.head()
dataclean.dtypes
dataclean=dataclean.astype({'name':'string'})
dataclean=dataclean.astype({'category':'category'})

#tf idf

tf=TfidfVectorizer()
texttf=tf.fit_transform(dataclean['name'].astype('U'))

#Kmeans clustering

k=5
model=KMeans(n_clusters=k,init='k-means++',max_iter=100,n_init=1)
model.fit(texttf)
dataclean['clustering']=model.labels_
dataclean.head()

#output
dataclean.to_csv('data_output.csv',index=False)