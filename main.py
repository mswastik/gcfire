from nicegui import app,ui
#import polars as pl
import pandas as pd
from datetime import datetime
import io
from google.cloud import aiplatform
import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

buffer = io.BytesIO()
today=datetime.today().replace(day=1)
ui.colors(primary='#6200EE',secondary='#03DAC5')
app.add_static_files('/resources', 'resources')

def navb():
    with ui.row(wrap=False).style('min-height: 50px; background-color:#000; margin-top:-15px; margin-left:-15px; min-width:102%; box-shadow:3px 3px #ababab'):
        with ui.link(target='/').style('min-height:50px'):
                ui.button('Home').style('min-height:50px; hover:bg-sky-200').props('push text-color=white color=black')
        with ui.link(target='/aboutme').style('min-height:50px'):
            ui.button('About Me').style('min-height:50px').props('push text-color=white color=black')
        with ui.link(target='/login').style('min-height:50px'):
            ui.button('Login').style('min-height:50px').props('push text-color=white color=black')
navb()
class A:
    def __init__(self) -> None:
        self.df=pd.DataFrame()
        self.udf=pd.DataFrame()
        self.idf=pd.DataFrame()
        self.item = ''
        self.ch=''
        self.ch1=''
        self.user='test'
        self.un=''
        self.pw=''
        self.lun=''
        self.lpw=''
a=A()

with ui.row(wrap=False).style('align-content:center; margin:auto; align:center'):
    with ui.link(target='/img'):
        with ui.card().classes('hover:bg-sky-200').style('transition:background 300ms; min-width:280px; min-height:300px'):
            with ui.image('/resources/img.jpeg').style('min-width:220px; min-height:280px'):
                ui.label('Image Recognition').classes('absolute-bottom text-center text-subtitle1')
    with ui.link(target='/fc'):
        with ui.card().classes('hover:bg-sky-200').style('transition:background 300ms; min-width:280px; min-height:300px'):
            with ui.image('/resources/fc.jpeg').style('min-width:220px; min-height:280px'):
                ui.label('Forecasting').classes('absolute-bottom text-center text-subtitle1')
    with ui.link(target='/cl'):
        with ui.card().classes('hover:bg-sky-200').style('transition:background 300ms; min-width:280px; min-height:300px'):
            with ui.image('/resources/cl.jpeg').style('min-width:220px; min-height:280px'):
             ui.label('Classification').classes('absolute-bottom text-center text-subtitle1')
    with ui.link(target='/reg'):
        with ui.card().classes('hover:bg-sky-200').style('transition:background 300ms; min-width:280px; min-height:300px'):
            with ui.image('/resources/reg.png').style('min-width:220px; min-height:280px'):
                ui.label('Regression').classes('absolute-bottom text-center text-subtitle1')

@ui.page('/fc')
def fc():
    navb()
    r2=ui.row(wrap=False)
    r3=ui.row()
    with r2:
        c1=ui.column()
        c2=ui.column()
        c3=ui.column()
        c4=ui.column()
    with r3:
        c31=ui.column()
        c32=ui.column()
    def dfile(e):
        a.df.to_excel(buffer,index=False)
        ui.download(src=buffer.getvalue(),filename='forecast.xlsx')

    with c1:
        dfb=ui.button('Download Forecast',on_click=dfile,color='primary')
        dfb.disable()
    def drawc():
        a.idf=a.idf['variable'].dt.month()
        a.idf=a.idf['variable'].dt.year()
        c31.clear()
        with c31:
            a.ch1=ui.echart({'xAxis':{'data':a.idf['variable'].to_list()},'yAxis': {},'series': [{'type': 'line', 'data': a.idf['value'].to_list()},{'type': 'line', 'data': []}]}).style('height:250px;width:650px')
            a.ch1.options['tooltip']={}
        c32.clear()
        with c32:
            a.ch=ui.echart({'xAxis':{'data': a.idf['month'].unique().to_list()},'yAxis': {},'legend':{},
                        'series': [{'type':'bar','name':i,'data': a.idf.filter('year'==i)['value'].to_list()} for i in a.idf['year'].unique()]
                        }).style('height:250px;width:650px')
            a.ch.options['tooltip']={}

    with c1:
        ui.button('Download Template',color='primary',on_click=lambda: ui.download(src="https://github.com/mswastik/fire/raw/8c707085c4e08c7e2275f1dae3d0a5976320e5d6/template.xlsx",filename='template.xlsx'))
    with c2:
        ui.upload(label='Upload Filled Template',auto_upload=True)

@ui.page('/img')
def img():
    navb()
    ui.label('Image Recognition')

@ui.page('/cl')
def cl():
    navb()
    ui.label('Classification')

@ui.page('/reg')
def reg():
    navb()
    with ui.card():
        ui.markdown('''This is a regression model trained using [MicrosoftLearning's Bike share data](https://github.com/MicrosoftLearning/mslearn-ai-fundamentals/tree/main/data/ml). 
                    It predicts the number of bike rentals for the day based on some external factors. It is trained using sklearn's which is inspired by LightGBM.
                    You can play around with these external factors and check the prediction based on the changed value.''')
    r1=ui.row()
    r2=ui.row()
    #mod=load('bike-rentals.pkl')
    #storage_client = storage.Client()
    #bucket = storage_client.bucket('hallowed-port-418405.appspot.com')
    #blob = bucket.blob('model.pkl')
    #with blob.open("rb") as f:
        #print(f.read())
    #    mod=load(f)
        #mod=load('https://storage.cloud.google.com/hallowed-port-418405.appspot.com/model.pkl')
    #print('Model Loaded '+str(mod))
    
    #print(endpoint)
    def predf(e):
        dft=pd.DataFrame([[day.value, mnth.value, year.value, season.value, holiday.value, weekday.value, workingday.value,
                            weathersit.value, temp.value, atemp.value, hum.value, windspeed.value]],columns=['day', 'mnth', 'year', 'season', 'holiday', 'weekday', 'workingday',
                            'weathersit', 'temp', 'atemp', 'hum', 'windspeed'])
        #print(dft.loc[0,:].to_json())
        #pred=mod.predict(dft)
        #headers = {"Authorization": "Bearer "}
        #response=requests.post('https://us-central1-aiplatform.googleapis.com/v1/projects/563926887952/locations/us-central1/endpoints/1662907982918189056:predict',
        #              json={"instances": [dft.iloc[0,:].to_json()]}),#auth=BearerAuth(''))
        #aiplatform.init(project='563926887952', location='us-central1')
        endpoint = aiplatform.Endpoint('1662907982918189056')
        #dft=dft.astype({"day":'int32',"mnth":'int32',"year":'int32',"season":'int32',"holiday":'int32',"weekday":'int32',"workingday":'int32'
        #               ,"weathersit":'int32'})
        #print(dft.values)
        response = endpoint.predict(instances=[list(dft.iloc[0,:])])
        pred=response.predictions
        print(pred)
        with r2:
            r2.clear()
            #with ui.card():
            ui.label('The predicted number of rentals is '+ str(pred))
            #print(pred)
    with r1:
        day=ui.number(label='Day',min=1,max=31,step=1,precision=0,value=1).props('dense')
        mnth=ui.number(label='Mnth',min=1,max=12,step=1,precision=0,value=1).props('dense')
        year=ui.select(label='year',options=[2011,2012],value=2011).props('dense options-dense')
        season=ui.select(label='season',options=[1,2,3,4],value=1,).style('min-width:85px').props('dense options-dense')
        holiday=ui.select(label='holiday',options=[0,1],value=0).style('min-width:85px').props('dense options-dense')
        weekday=ui.select(label='weekday',options=[0,1,2,3,4,5,6],value=1).style('min-width:85px').props('dense options-dense')
        workingday=ui.select(label='workingday',options=[0,1],value=1).style('min-width:85px').props('dense options-dense')
        weathersit=ui.select(label='weathersit',options=[0,1],value=1).style('min-width:85px').props('dense options-dense')
        temp=ui.number(label='temp',min=0,max=1,precision=6,step=.001,value=0.166667).props('dense')
        atemp=ui.number(label='atemp',min=0,max=1,precision=6,step=.001,value=0.565667).props('dense')
        hum=ui.number(label='hum',min=0,max=1,precision=6,step=.001,value=0.811250).props('dense')
        windspeed=ui.number(label='windspeed',min=0,max=1,step=.001,precision=6,value=0.233204).props('dense')
        btn=ui.button(text='Predict',on_click=predf)
        #day.sanitize()
        #mnth.sanitize()

@ui.page('/login')
def login():
    navb()
    with ui.tabs().classes('w-full') as tabs:
        two = ui.tab('Signup')
        one = ui.tab('Login')
    with ui.tab_panels(tabs, value=two).classes('w-full'):
        with ui.tab_panel(two):
            a.un=ui.input(label="Email ID",validation={'Not an email!': lambda value: ("@" in value) & ("." in value)}).classes('content-center').style('margin:auto;min-height:50px;min-width:300px')
            a.pw=ui.input(label="Password",password=True,password_toggle_button=True).classes('content-center').style('margin:auto;min-height:50px;min-width:300px')
            ui.button('Signup').style('margin:auto')
        with ui.tab_panel(one):
            a.lun=ui.input(label="Email ID",validation={'Not an email!': lambda value: ("@" in value) & ("." in value)}).style('margin:auto;min-height:50px;min-width:300px')
            a.lpw=ui.input(label="Password",password=True,password_toggle_button=True).style('margin:auto;min-height:50px;min-width:300px')
            ui.button('Login').style('margin:auto')

@ui.page('/aboutme')
def login():
    navb()
    ui.chat_message('''Hi,<br>
             I am Swastik. I have developed this web app on Python as POC. This site uses Google Cloud's App Engine service for hosting and serves some <br>
             trained AI/ML models using Vertex AI endpoints. This project is still under active development but you are welcome to explore it.<br>
             Do share feedback on my email ID <u><a style="color:blue;" href='mailto:m.swastik@gmail.com'>m.swastik@gmail.com</a></u>.
             <br><br>
             Regards,<br>
             Swastik Mishra''',
             name='Swastik',
             stamp="May'24",
             avatar='/resources/me.jpg',
             text_html=True)
ui.run(title="Machine Learning",binding_refresh_interval=1,reconnect_timeout=70)

