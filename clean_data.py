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




en_text = """ enPuls Pro - in brief 5

Page  5
 What is enPuls Pro? A state of the art therapeutic massager.

Radial pulse therapy Radial Pulse Therapy is a procedure for relief of minor muscle aches and
pains and for temporary increas e in local blood circulation.

What does
enPuls Pro do? The handpiece contains a projectile  that is accelerated through the
electromagnetic transfer of kinetic energy. This kinetic energy is transferred
into impact energy in the applicator head. The impact energy delivered from
the applicator head results in radial pul ses developed in the target tissue.
With enPulsPro, a maximum penetrati on depth of about 35 mm into human
tissue can be achieved.

How does the
enPuls Pro generate
radial pulses? An electromagnetic field is generated at the rear end of the handpiece by
means of a coil.
A projectile is accelerated through t he field crashing into the applicator head
at the front of the handpiece generating radial pulses t hat spread radially into
the tissue.

Why  enPuls Pro? The innovative technology allows for a compact design without a
compressor.
The modern multi-color display, showin g all therapy-relevant  parameters, the
modern touch operation and the ab ility to simultaneously connect 2
handpieces.
Customisable program startup settings and a clear, simple menu offer
maximum convenience for the user.

Adjustable frequencies and various appl icators enable the therapy to be
tailored to the respective status of the patient.

What else does
enPuls Pro offer? An integrated VAS scale provides an orie nting overview of the chronological
progression and success of the therapy.

Intended use enPulsPro is an electromagnetic t herapy system for the generation and
application of radial pulses in orthopedics and physiotherapy.

Note: The application of the device is reserv ed to medical professionals (such as
physicians, therapists and health paraprofessionals).

 enPulsPro has been constructed and desi gned solely for the application on
superficial skin problems in humans.

 The device is intended for use mechanical massage devices."""
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
      return  ""
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
english_text = "NLTK is a leading platform for building Python programs to work with human language data."
def remove_en_stopwords(text):
    tokens = word_tokenize(text) 

    
    english_stopwords = set(stopwords.words('english')) # Get English stopwords

    filtered_tokens = " ".join([word for word in tokens if word.lower() not in english_stopwords])
    return filtered_tokens




# Sample Persian text
persian_text = "پردازش زبان‌های طبیعی یکی از حوزه‌های مهم در علوم کامپیوتر است."
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
def clean_data(text , Remove_Urls = True , Lemmatize= True ):
  text =  remove_punctuation(text)

  if detect(text) == 'en':
    text = get_en_words(text)
    text = remove_content_page(text)
    if Remove_Urls:
      text = remove_urls(text)
    if Lemmatize:
      text = Lemmatize_en_text(text)

    return text , "en"
  elif detect(text) == 'fa':
    text = get_fa_word(text)
    text = remove_content_page(text)
    if Remove_Urls:
      text = remove_urls(text)
    if Lemmatize:
      text = Lemmatize_fa_text(text)

    return text , "fa"
  else:
    print("language is : " + detect(text))
    return None

print(clean_data(en_text))