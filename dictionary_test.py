# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import requests
import json

# TODO: replace with your own app_id and app_key
app_id = '03cecbef'
app_key = 'cd0910e09f829a72c5334baa50f3b5e3'


language = 'en'         #language code for API
word_id = 'is'      #word that's being retrieved from the dictionary
json_from_API = ''      #initialization of the storage variable
comment_text = ''       #initialize the comment definition response, eventually this will have the comment in it
#set up the API endpoint:

language = 'en'
word_id = 'changes'

url_root = 'https://od-api.oxforddictionaries.com:443/api/v1/inflections/' + language + '/' + word_id.lower()

    

url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()

r_root = requests.get(url_root, headers = {'app_id': app_id, 'app_key': app_key})
root_json = json.loads(json.dumps(r_root.json()))
part_of_speach=''
noun=''
verb=''

def first_Noun(json):
    #gets the first noun from the entries json, basically just extracting from weirdly formatted json
    noun=''
    for x in range(0,len(json["results"][0]['lexicalEntries'])):
        #try because not all elements of this list have 'lexicalCategory'
        try:
            part_of_speach=json["results"][0]['lexicalEntries'][x]['lexicalCategory']
            if(part_of_speach=='Noun'):
                noun=json["results"][0]['lexicalEntries'][x]['inflectionOf'][0]['text']
                break
        except:
            pass
    return noun
print(first_Noun(root_json))

def first_Verb(json):
    #gets the first verb from the entries json, basically just extracting from weirdly formatted json
    verb=''
    for x in range(0,len(json["results"][0]['lexicalEntries'])):
        #try because not all elements of this list have 'lexicalCategory'
        try:
            part_of_speach=json["results"][0]['lexicalEntries'][x]['lexicalCategory']
            if(part_of_speach=='Verb'):
                verb=json["results"][0]['lexicalEntries'][x]['inflectionOf'][0]['text']
                break
        except:
            pass
    return verb
print(first_Verb(root_json))


def define(word,part_of_speach):
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word.lower()
    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    comment_text = ''
    if r.status_code == 200: #only run the rest of the script if the word exists and the api works
        json_from_API = json.loads(json.dumps(r.json()))
    
        comment_text = json_from_API['results'][0]["id"] + "\n" + part_of_speach + "\n\n"
        #everything is in try except so that if the entries don't exist the bot wont crash
        try:
        #the definition then 2 new lines
            comment_text += "\t definition: " + json_from_API['results'][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
            comment_text += "\n\n"
        except:
            pass

        try:
            #example sentence
            comment_text += "\t example: " + json_from_API['results'][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["examples"][0]["text"]
        except:
            pass
            comment_text
    return comment_text
print(define(first_Verb(root_json),"verb"))
print(define(first_Noun(root_json),"noun"))