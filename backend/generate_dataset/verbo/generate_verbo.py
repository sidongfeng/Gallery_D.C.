import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import tqdm
import pandas as pd
import xml.etree.ElementTree as ET
from PIL import ImageFile, Image
ImageFile.LOAD_TRUNCATED_IMAGES = True

targets = ["CheckBox","Button","Chronometer","RadioButton","RatingBar","SeekBar","Spinner","ToggleButton","ProgressBar","Switch","ImageButton"]

def parseXML(xmlfile): 
    result = []
    tree = ET.parse(xmlfile) 
    root = tree.getroot()
    items = root.findall('node')
    while len(items)>0:
        child = items.pop(0)
        try:
            c = child.get('class').rsplit('.',1)[1]
        except:
            continue
        bounds = [int(x) for x in child.get('bounds')[1:-1].replace('][',',').split(',')]
        if c in targets:
            result.append((c,bounds,child.get('text')))
        items += child.findall('node')
    return result

def generate(id,df):
    if not os.path.isdir('./all_widgets/'): os.mkdir('./all_widgets/')
    json_dir = dir_path+"/5k_data/train_data_path.json"
    f = open(json_dir,'r')
    data = eval(f.read())
    f.close()
    for v,apps in data.items():
        for a in tqdm.tqdm(apps):
            for i in apps[a]:
                xmlfrom_ = dir_path+"/"+v+"/"+a+"/stoat_fsm_output/ui/"+i
                imgfrom_ = dir_path+"/"+v+"/"+a+"/stoat_fsm_output/ui/"+i.replace('xml','png')
                if not (os.path.exists(xmlfrom_) and os.path.exists(imgfrom_)):
                    continue
                ob = parseXML(xmlfrom_)
                # crop
                image = Image.open(imgfrom_)
                for class_, bounds, text in ob:
                    try:
                        im = image.crop(bounds)
                        im.save('./all_widgets/'+class_+'-'+str(id)+'.png')
                        id+=1
                        
                        df = df.append({'id': id, 
                                    'name':class_+'-'+str(id), 
                                    'color':"",
                                    'coordinates':{"from": [bounds[0], bounds[1]], "to": [bounds[2], bounds[3]]},
                                    'dimensions':{"height": abs(bounds[3]-bounds[1]), "width": abs(bounds[2]-bounds[0])},
                                    'package_name':a,
                                    'text':text,
                                    'widget_class':class_,
                                    'application_name':"", 
                                    'downloads':"", 
                                    'url':'',
                                    'category':"",
                                    'Developer':"",
                                    'font':"",
                                    'sims':[],
                                    'date':"",
                                    'src':imgfrom_}, ignore_index=True)
                    except:
                        continue
    return id, df

if __name__ == '__main__': 
    # generate widgets dataset
    id = 0
    df = pd.DataFrame(columns=['id','name','color','coordinates','dimensions','package_name','text','widget_class','application_name','downloads','url',
            'category','Developer','font','sims','date'])
    df = df.fillna(0)
    id, df = generate(id,df)
    print(id)
    print(df.text)
