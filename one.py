import dash
import dash_html_components as html
import dash_core_components as dcc
import base64


import os 
import io 
from google.cloud import vision 



from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('myapikey.json')

client = vision.ImageAnnotatorClient(credentials = credentials)



creds_file = 'myapikey.json'


from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 












external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([

        html.Div([
            html.H5('Choose Image 	\ud83d\uddc3\ufe0f'),
            dcc.Upload(
                    id='upload-data',
                    children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
            ,' 	\ud83d\udcc1'
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin-bottom':'100%',
                        'margin': '1%'
                    },
                    # Allow multiple files to be uploaded
                   accept='image/*'
                )],className="ten columns offset-by-one"),


        html.Div([
        dcc.Input(id='input-1-keypress', type='text', value='text1'),
     dcc.Input(id='input-2-keypress', type='text', value='text2'),



            ],className="ten columns offset-by-one"),

        html.Div([

        html.Div(id='output-container')],className="ten columns offset-by-one")
    
])


@app.callback(dash.dependencies.Output('output-container', 'children'),
              [dash.dependencies.Input('upload-data','contents')],
              [dash.dependencies.State('upload-data', 'filename'),
                dash.dependencies.State('input-1-keypress', 'value'),
               dash.dependencies.State('input-2-keypress', 'value')]
               )
def update_output(value,h,text111,text222):
    if value is not None:
        string = value.split(';base64,')[-1]
        imgdata = base64.b64decode(string)
        filename = 'some_image.jpg'

        with open(filename, 'wb') as f:
            f.write(imgdata)


        f = 'some_image.jpg'
        with io.open(f, 'rb') as image: 
            content = image.read()
        


   
        

        image = vision.types.Image(content = content) 
        response = client.document_text_detection(image = image) 
        text1 = "The narrator sold the drawing for fifty pounds. He had bought it for ten shillings. He got a good profit of forty nine pounds ten."
        text2 = "The narrator sold the drawing for fifty pounds. He had bought it for ten shillings."
        
        print(type(text111))
        text1="".join(text111)
        text2="".join(text222)
        print(text1,text2)
        
        txt = [] 
        for page in response.full_text_annotation.pages: 
                for block in page.blocks: 
                    print('\nConfidence: {}%\n'.format(block.confidence * 100)) 
                    for paragraph in block.paragraphs: 

                        for word in paragraph.words: 
                            word_text = ''.join([symbol.text for symbol in word.symbols]) 
                            txt.append(word_text) 

        
        

        example_sent = "This is a sample sentence, showing off the stop words filtration."

        stop_words = set(stopwords.words('english')) 

        word_tokens1 = word_tokenize(text1) 
        word_tokens2 = word_tokenize(text2) 

        filtered_sentence1 = [w for w in word_tokens1 if not w in stop_words] 

        filtered_sentence1 = [] 

        for w in word_tokens1: 
            if w not in stop_words: 
                filtered_sentence1.append(w) 
                
        filtered_sentence2 = [x for x in word_tokens2 if not x in stop_words] 

        filtered_sentence2 = []

        for x in word_tokens2: 
            if x not in stop_words: 
                filtered_sentence2.append(x) 

        #print(word_tokens) 
        print(filtered_sentence1) 
        print(filtered_sentence2)

        for item in filtered_sentence1:
            for item1 in filtered_sentence2:
                if item == item1:
                    print (item)

        print ("****************\n")

        try:
            filtered_sentence1.remove('.')
            filtered_sentence2.remove('.')
        except:
            pass



        for item in filtered_sentence1:
            for item1 in filtered_sentence2:
                if item == item1:
                    print (item)

        print ("****************\n")

        marks = (len(filtered_sentence2)/len(filtered_sentence1))*3
        print(marks)
        text2=" ".join(txt)
        print(text2)
    
        return ["Text: "+str(text2)+"\n\nScore: "+str(marks)]


        
        


if __name__ == '__main__':
    app.run_server(debug=True)
