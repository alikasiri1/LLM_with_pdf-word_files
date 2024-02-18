import re
import nltk
import string
from hazm import Lemmatizer
from langdetect import detect
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from hazm import stopwords_list, word_tokenize




################################################################################## Removal of Punctuations

def remove_punctuation(text):
    PUNCT_TO_REMOVE = string.punctuation.replace(".","").replace("%","").replace("@","").replace("-","") + "•"
    """custom function to remove the punctuation"""
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))


################################################################################## get words
def get_fa_word(text):
  tokens = word_tokenize(text) 
  d=''
  for word in tokens:
    if len(word)==1 and word !='و':
      d += word
    else:
      d += ' '+word
  return d.replace(" . " , ". ").replace(" - ","")


nltk.download('punkt')
def get_en_words(text):
  tokens = word_tokenize(text)
  filtered_tokens = " ".join([word for word in tokens])

  return filtered_tokens.replace(" . " , ". ").replace(" - ","")


################################################################################## remove_content_page
def remove_content_page(text , based_on_Rareword = True):
  list_words = ["Explanation of symbols" , "contents" , "فهرست" , "Illustrations"]
  if based_on_Rareword:
    txt = " ".join(extract_rare_words(text))
  else:
     txt = text
  for word in list_words:
    if word.lower()  in txt.lower():
      print("remove" , word +" page")
      return  " "
  return text


################################################################################## Lemmatizer
lemmatizer_fa = Lemmatizer() # Initialize the Lemmatizer
def Lemmatize_fa_text(text): # Farsi
  words = text.split()# Tokenize the text into words

  lemmatized_words = [lemmatizer_fa.lemmatize(word) for word in words]# Lemmatize each word in the text

  lemmatized_text = ' '.join(lemmatized_words) 

  return lemmatized_text


nltk.download('wordnet')
lemmatizer_en = WordNetLemmatizer()
def Lemmatize_en_text(text): # english
    return " ".join([lemmatizer_en.lemmatize(word) for word in text.split()])



################################################################################## stopwords
nltk.download('punkt')
nltk.download('stopwords')
# Sample English text
# english_text = "NLTK is a leading platform for building Python programs to work with human language data."
def remove_en_stopwords(text):
    tokens = word_tokenize(text) 

    
    english_stopwords = set(stopwords.words('english')) # Get English stopwords

    filtered_tokens = " ".join([word for word in tokens if word.lower() not in english_stopwords])
    return filtered_tokens




# Sample Persian text
# persian_text = "پردازش زبان‌های طبیعی یکی از حوزه‌های مهم در علوم کامپیوتر است."
def remove_fa_stopwords(text):
    tokens = word_tokenize(text)

    persian_stopwords = set(stopwords_list()) # Get Persian stopwords
    # persian_stopwords = ["است" , "در" , "را", "که", "من", "تو", "او", "این", "آن", "بعد"]

    filtered_tokens = " ".join([word for word in tokens if word not in persian_stopwords]) 
    return filtered_tokens


################################################################################## remove URL
def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')  
    return url_pattern.sub(r'', text)

################################################################################## extract Rare words 
def extract_rare_words(text, threshold=1):
    
    words = re.findall(r'\b\w+\b', text.lower()) 
    
    word_counts = Counter(words) # Count the frequency of each word
    
    rare_words = [word for word, count in word_counts.items() if count <= threshold] 

    return rare_words


################################################################################## remove Rarewords
def remove_rarewords(text):
    RAREWORDS = extract_rare_words(text)
    print(RAREWORDS)
    """custom function to remove the rare words"""
    return " ".join([word for word in str(text).split() if word.lower() not in RAREWORDS])


################################################################################## clean data
def clean_data(text , Remove_Urls = True , Lemmatize= True, stopwords=False):
  text =  remove_punctuation(text)
  language = detect(text)
  if language == 'en':
    text = get_en_words(text)
    text = remove_content_page(text)

    if Remove_Urls:
      text = remove_urls(text)
      
    if stopwords:
       text = remove_en_stopwords(text)

    if Lemmatize:
      text = Lemmatize_en_text(text)
    
    return text , "en"
  elif language == 'fa':
    text = get_fa_word(text)
    text = remove_content_page(text)

    if Remove_Urls:
      text = remove_urls(text)

    if stopwords:
       text = remove_fa_stopwords(text)

    if Lemmatize:
      text = Lemmatize_fa_text(text)
    
    return text , "fa"
  else:
    print("language is : " + language)
    # print(text)
    
    return " " , language

# print(clean_data(en_text))
# print(Lemmatize_fa_text("ناد42کجت"))