import os
import cv2
import shutil
import pandas as pd
import xml.etree.ElementTree as ET
from color import get_color

df = pd.read_json('fake.json', orient='records')

###########################################
##########  Verbo extraction  #############
###########################################
PATH1 = "/Volumes/Macintosh HD/Users/charlie/Documents/verbo1/"
PATH2 = "/Volumes/Macintosh HD/Users/charlie/Documents/verbo2/"
PATH3 = "/Volumes/Macintosh HD/Users/charlie/Documents/verbo3/"

def parseXML(xmlfile): 
    targets = ["CheckBox","Button","Chronometer","RadioButton","RatingBar","SeekBar","Spinner","ToggleButton","ProgressBar","Switch","ImageButton"]
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
            result.append((c,bounds))
        items += child.findall('node')
    return result

def get_screenshots_from_verbo():
    folders = os.listdir(PATH1)+os.listdir(PATH2)+os.listdir(PATH3)
    if '.DS_Store' in folders: folders.remove('.DS_Store')
    folders_app = {}
    for x in folders:
        folders_app[x.split('_')[0]] = x
    for i,row in df.iterrows():
        id = int(row['name'].split('-')[1])
        if id % 500 == 0:
            print(id)
        if id < 11463:
            package = row['package_name']
            if package not in folders_app.keys(): continue
            if os.path.isdir(PATH1+folders_app[package]+'/stoat_fsm_output/ui/'):
                path = PATH1+folders_app[package]+'/stoat_fsm_output/ui/'
            elif os.path.isdir(PATH2+folders_app[package]+'/stoat_fsm_output/ui/'):
                path = PATH2+folders_app[package]+'/stoat_fsm_output/ui/'
            else:
                path = PATH3+folders_app[package]+'/stoat_fsm_output/ui/'
        else:
            continue
        files = [x.replace('.xml','') for x in os.listdir(path) if x.endswith('.xml')]
        for f in files:
            ob = parseXML(path+f+'.xml')
            match = False
            for class_,bounds in ob:
                class_bool = False
                b_bool = False
                p_bool = False
                color_bool = False
                # test class
                if class_==row['widget_class']:
                    class_bool = True
                else:
                    continue
                # test bounds
                if bounds== row['coordinates']['from']+row['coordinates']['to']:
                    b_bool = True
                else:
                    continue
                # test path
                if os.path.exists(path+f+'.png'):
                    p_bool = True
                else:
                    continue
                # test color
                try:
                    image = cv2.imread(path+f+'.png')
                    widgets = image[bounds[1]:bounds[3], bounds[0]:bounds[2]]
                except:
                    continue
                colors = get_color(widgets)
                base_colors = row['color']
                if type(colors) == int or type(base_colors) == int: continue
                if 'Red' in colors.keys(): del colors['Red']
                if 'Red2' in colors.keys(): del colors['Red2']
                color_bool = all(abs(base_colors[c] - v)<=0.1 for c,v in colors.items())
                if class_bool and b_bool and p_bool and color_bool:
                    match = True
                    break
            # extract bounding image
            if match:
                cv2.rectangle(image, (bounds[0],bounds[1]), (bounds[2],bounds[3]), (0,0,255),2)
                cv2.imwrite('./screenshots/'+package+'-'+f+'-'+str(id)+'.png',image)
                break

###########################################
###########  Rico extraction  #############
###########################################
import json
PATH_RICO = "/Users/mac/Documents/Python/Data/Rico/"
PATH_SEMANTIC = "/Users/mac/Documents/Python/Data/Rico_Semantic/"
Threshold = 2

BAD = ['appcompatcheckbox','apswitchtab', 'ws_verticalseekbar', 'floatseekbar', 'reselectablespinner', 'standardswitch', 'simplecircularprogressbar', 'rangeseekbarlayout', 'robotoradiobutton', 'seekbarcompat', 'sequentialviewswitcher', 'workspaceswitchview', 'videoprogressbar', 'accountspinner', 'brainpopseekbar', 'robotocheckbox', 'profiletogglebutton', 'floatingactiontogglebutton', 'progressbarwithmilestone', 'checkboxopensans', 'radiobuttoncustomtemp', 'inputcheckbox', 'medibangseekbar', 'oncecheckbox', 'localizedcheckbox', 'telephonespinner', 'horizontalswipeprogressbarview', 'mytextswitcher', 'customcheckbox', 'phonetabswitcher', 'inertcheckbox', 'nodefaultspinner', 'sseekbar', 'citynameswitcher', 'iconprogressbar', 'chatswitchprofileview', 'xprogressbar', 'brightseekbar', 'colorablecheckboxpreference_', 'tintratingbar', 'accountswitcherview', 'materialbetterspinner', 'holocircleseekbar', 'settingsrowswitch', 'checkboxplus', 'radiobuttonex', 'timespinner', 'metatraderspinner', 'qradiobutton', 'cvpseekbar', 'mslswitch', 'childgrowthseekbar', 'pptogglebutton', 'colorableprogressbar_', 'animcheckbox', 'tabswitchview$tabswitchitemview', 'spinneroverlaydialog', 'heartcheckbox', 'qcenteredanimatableprogressbar', 'avspinnertextview', 'herecheckbox', 'accentedseekbar', 'progressspinnerview', 'customthemeseekbar', 'customfontcheckbox', 'eslspinner', 'fontablespinner', 'gsxaccountswitcherview', 'googleplaydownloaderprogressbar', 'choicespinner', 'stencilswitch', 'smartspinner', 'spinnercustom', 'multistatetogglebutton', 'userprefspinner', 'communityprogressbarview', 'sorttogglebutton', 'onoffswitch', 'contentloadingsmoothprogressbar', 'textseekbar', 'cuepointsseekbar', 'approgressbar', 'textprogressbar', 'nanaprogressbar', 'mybookstoolbarspinner', 'locationspinner', 'selectstatespinner', 'hintedspinnerwitherror', 'materialprogressbar', 'fontradiobutton', 'pathprogressspinner', 'myratingbar', 'flashswitcher', 'keyboardswitchview', 'jtvseekbar', 'nutritionprogressbar', 'mfmprogressbar', 'targetcheckbox', 'uccustomprogressbar', 'synchronizedprogressbar', 'myradiobutton', 'filterseekbarwidget', 'dottedprogressbar', 'formswitch', 'discreteseekbar', 'odigeospinner', 'checkboxview', 'ppprogressbar', 'quartzprogressbar', 'foodcheckboxes', 'smoothseekbar', 'maxwidthspinner', 'cmcheckbox', 'smoothprogressbar', 'segmentedradiobuttongroup', 'multilistenerspinner', 'fontcheckbox', 'notificationtoggleswitchview', 'seekbarex', 'viewswitchpreference', 'dimmerswitchwebview', 'countryspinner', 'customfadeoutseekbar', 'busuudiscreteseekbar', 'timeoutprogressbar', 'colorpickerseekbar', 'customprogressbar$a', 'seekbarscrollview', 'settingswitchitem', 'progressbarwidget', 'grxprogressbar', 'duoradiobutton', 'seekbarwithtopleftlabels', 'butteryprogressbar', 'settingsswitchview', 'discreterangeseekbar', 'parkmeseekbar', 'menuspinner', 'countabletogglebutton', 'spinnercompat', 'reenablingseekbar', 'seekbarrotator', 'mvxspinner', 'materialtogglebutton', 'circleprogressbar', 'markettextswitcher', 'spinnerwrapper$b4aspinner', 'listoniccheckboxwrapper', 'xplayratingbar', 'segmentednowseekbar', 'loadercheckbox_', 'teamuploadingspinner', 'progressbarcircular', 'slformcheckbox', 'cvpplaypausetogglebutton', 'mmfalseprogressbar', 'favoriteswitcherview', 'progressbardeterminate', 'quizprogressbar', 'mapcontrolspinner', 'progresscheckbox', 'switchview', 'circlecheckbox', 'seekbarcc', 'customtoggleswitch', 'volumeseekbar', 'rangeprogressbar', 'labeledtimeseekbar', 'dilatingdotsprogressbar', 'appcompatprogressbar', 'customtextinputlayoutspinner', 'amradiobutton', 'roundededgeprogressbar', 'o7progressbar', 'realviewswitcher', 'birthpreferencecheckboxview', 'partialselectioncheckbox', 'imcircularprogressbar', 'percentprogressbar', 'customfonttogglebutton', 'fullsizepopupspinner', 'fakeprogressbar', 'loadingprogressbar', 'spinnertextview', 'labelledswitchview', 'dialogspinner', 'switchbar', 'scorespinner', 'numberprogressbar', 'pullspinner', 'flipmeterspinner', 'nbcradiobutton', 'extendedswitchrendered', 'yprogressbar', 'dropdownspinnerview', 'headerprogressbarview', 'hyspinner', 'highlightselectedspinner', 'playpausetogglebutton', 'ringprogressbar', 'globalnavigationradiobutton', 'customfontradiobutton', 'beautyspinner', 'filterdiscreteseekbar', 'twothumbseekbar', 'compoundcheckboxpref', 'sltogglebutton', 'delayedprogressbar', 'framedprogressbar', 'videoloadingspinner', 'periodswitchertimeline_', 'nspinner', 'igprogressimageviewprogressbar', 'progressbaricecream', 'logininputswitcher', 'genderspinner', 'styledspinner', 'qualityswitcher', 'alertcheckboxrow', 'materialcheckboxagreementview', 'protectedseekbar', 'spinnerwithhint', 'selecteditemsizedspinner', 'customfontswitch', 'bulletedprogressbar', 'fontswitchcompat', 'stockspinner', 'parisinecheckbox', 'customimageviewwithprogressbar', 'pilltogglebutton', 'superverticalseekbar', 'textcheckbox', 'cfspinner', 'playdrawerdownloadswitchrow', 'creaspinner', 'trianglespinner', 'switchitemview', 'exchangespinner', 'switchtextview', 'epledspinner', 'checkboxwithlabel', 'phasedseekbar', 'fvrspinner', 'progressbarview', 'colorprogressbar', 'emotionratingbar', 'viewalarmtypespinnerpreference', 'slideswitch', 'singleappprogressbar', 'forminputcheckbox', 'tabradiobutton', 'ctratingbar', 'listoniccheckbox', 'betterspinner', 'nendadviewswitcher', 'progressbarindeterminatedeterminate', 'switcher', 'flexibleratingbar', 'gprogressbar', 'spinnerwithnovalue', 'switchex', 'inputspinner', 'circularprogressbar', 'ebatescircularprogressbar', 'weicoprogressbar', 'folderspinner', 'silenttogglebutton', 'dotsprogressbar', 'textswitcher', 'psautoswitchbtn', 'roundedprogressbar', 'progressbarcontainerview', 'seekbaroverlay', 'progressimageswitcher', 'seekbarpreference', 'simpsonsprogressbar', 'checkboxfont', 'switchrenderer', 'drawablecenterradiobutton', 'arrayswitchview', 'squaretogglebutton', 'pricespinner', 'themedcheckbox', 'consoleprogressbar', 'gradientspinner', 'aeprogressbar', 'hintspinner', 'mlcustomspinner', 'customfontcheckboxview', 'smartprogressbar', 'preferenceswitch', 'selectcategoryspinner', 'chatsettingsswitchview', 'customswitchview', 'baseswitch', 'checkboxitemview', 'ymarkedseekbar', 'foodlerratingbar', 'tutorialprogressbar', 'enhancedspinner', 'switchanimation', 'countryofresidencespinner', 'variationsdrawer$drawerradiobutton', 'odtogglebutton', 'sociallinktogglebutton', 'myseekbar', 'brandedprogressbar', 'showtimesdatespinner', 'videoprogressbarview', 'surveyprogressbar', 'channellistswitcher', 'verticalprogressbar', 'spinnerpatch', 'labeledcheckbox', 'issuedownloadprogressbar', 'selectroomspinner', 'mareriaprogressbar', 'postorageselectspinner', 'styledtogglebutton', 'typefacedradiobutton', 'switchingpaneframelayout', 'toggleableradiobutton', 'talkratingbar', 'autocompletespinner', 'epspinner', 'animatedradiobutton', 'inteditionspinner', 'anvatoseekbarui', 'seekbar_themable', 'spinnerwitherrortext', 'amprogressbar', 'filterrangeseekbar', 'swipetogglebutton', 'checkboxmaterial', 'contentloadingprogressbar', 'customspinnerblacktitle', 'ejradiobutton', 'squareprogressimageswitcher', 'colorablecheckbox', 'robotoswitch', 'toolbarprogressbar', 'customtogglebuttonview', 'colorswitchpanel', 'switchsettingsitemview', 'radiobuttondarktext', 'wmspinnerfield', 'kprogressbar', 'checkablelayoutcheckbox', 'ramblacheckbox', 'favoritecheckbox', 'lmradiobutton', 'togglebuttonwithtooltip', 'typefaceswitchcompat', 'trendingfilterspinneritemshortview', 'nodefaultmaterialspinner', 'playerlogoswitcher', 'progressbarwrapper', 'hcprogressbar', 'arcprogressbar', 'seekbarduedatehint', 'labelspinnerview_', 'checkboxwithpaddingfix', 'qccheckbox', 'borderradiobutton', 'interestswitchermodecard', 'rangeseekbar', 'wazeswitchview', 'dynamicsizingspinner', 'hiddenverticalseekbar', 'antennacheckbox', 'ebkseekbar', 'expandableswitch', 'bmprogressbar', 'datespinner', 'imageswitcher', 'phoneswitchview', 'centeredcheckbox', 'spinnercontainer', 'customtogglebuttonwithimageview', 'typefaceradiobutton', 'cabinclassspinnerwithtext', 'fundingsourcespinner', 'radiobuttonplus', 'nprspinner', 'looktogglebutton', 'fontsizeseekbar', 'dropdownspinner', 'nicespinner', 'purchasesubscriptionseekbar', 'wmspinner', 'zoomprogressimageswitcher', 'blockingprogressbar', 'spinnerlogininputswitcher', 'propertyspinnerloader', 'horizontalprogressbar', 'amountspinner', 'colorbitmapcheckbox', 'animatedtogglebutton', 'doubleseekbar', 'mapswitchview', 'toggleswitch', 'myspinner', 'seekbarpopup', 'roundcornerprogressbar', 'b4fradiobutton', 'slinputspinner', 'wdtimagetogglebutton', 'whiteprogressbar', 'guardianprogressbar', 'videoseekbar', 'smoothcheckbox', 'budgetprogressbar', 'progressbarindeterminate', 'robotolightcheckbox', 'materialspinnerlayout', 'beamprogressbar', 'fontawesomeratingbar', 'checkboxcustomfont', 'disabledseekbar', 'eqseekbar', 'googleprogressbar', 'filterageseekbar', 'customspinnerwhitetitle', 'gcmprogressbar', 'styledcheckbox', 'birthpreferencecheckboxnotesview', 'tintedcontentloadingprogressbar', 'wsiautoswitchingviewpager', 'tintabletogglebutton', 'translationswitch', 'colorableswitch', 'downloadprogressbar', 'expandablespinner', 'brightcoveseekbar', 'pgrcheckbox', 'countrylistspinner', 'viewcheckboxpreference', 'registrationoptionspinner', 'spinnerview', 'sortspinner', 'mcradiobutton', 'bufferingprogressbar', 'roundprogressbarwidthnumber', 'talabatradiobutton', 'customcachestateprogressbar', 'niumrangeseekbar', 'kcheckbox', 'viewspinnerpreference', 'sortorderspinner', 'circularprogressspinner', 'ppseekbar', 'sizechangecatchableradiobutton', 'ccarangeseekbarvertical', 'parisineradiobutton', 'overflowspinner', 'tabswitchview', 'materialcircularprogressbar', 'mmfcircularprogressbar', 'cvpauthprogressbar', 'progressbarhorizontalview', 'activityprogressbar', 'myprogressbar', 'myswitch', 'textfittogglebutton', 'vmbfadertextswitcher', 'extendedcheckbox3listview', 'vkseekbar', 'customseekbar', 'radiobuttonwithfont', 'fivestarrangeseekbar', 'gxcheckbox', 'fastprogressbar', 'hoursfrequencyspinner', 'ourspinner', 'onboardingprogressbar', 'pickstogglebutton', 'nbcswitch', 'fxseekbar', 'dynamicradiobutton', 'vastvideoprogressbarwidget', 'customtimespinner', 'stumbleprogressbar', 'multicolorprogressbar', 'sizeadjustableradiobutton', 'tiuiswitch$2', 'imagetogglebutton', 'viewswitcher', 'materialspinner', 'preferencecheckbox', 'switchpreferenceview', 'surveyseekbar', 'settingscheckbox', 'customspinner', 'settingstogglebutton', 'fanaticssizeradiobutton', 'animatedcheckbox', 'recyclerviewswitcher', 'ratingbardealhighlightstileview', 'offonviewswitcher', 'panelswitcher', 'geminiprogressbar', 'togglebuttongrouptablelayout', 'sortradiobutton', 'selectablespinner', 'circleseekbar', 'mttextspinner', 'customradiobutton', 'customprogressbarcircularindeterminate', 'reversedseekbar', 'qcityspinner', 'dropdownbelowspinner', 'imgurloadingprogressbar', 'mtswitch', 'countdownchronometer', 'themecheckbox', 'swipeprogressbar', 'cgchronometer', 'controllableseekbar', 'managedtogglebutton', 'pricerangeseekbar', 'tabsswitcherview', 'xplayseekbar', 'caristaswitch', 'relativelayoutwithcheckbox', 'toolbarspinner', 'yellowratingbar', 'modernviewswitcher', 'progressseekbar', 'holocircularprogressbar', 'tintedprogressbar', 'notskinnedicsspinner', 'togglebuttonlistview', 'bookingvalidatablespinner', 'spinnertoolbar', 'circularseekbar', 'roundprogressbar', 'tspinnerview', 'settingitemwithswitch', 'animatingprogressbar', 'extendedviewswitcher', 'togglebuttonnoelevation', 'stingrayswitch', 'checkboxtextview', 'radiobuttontab', 'sizetogglebutton', 'feedswitcherscrollview', 'customswitch', 'styledswitch', 'menuitemswitcherlayout', 'customtogglebutton', 'alphatogglebutton', 'twosideseekbarfilterview', 'eqswitch', 'heartprogressbar', 'clickablecheckboxlabel_', 'greyabletogglebutton', 'customseekbarview', 'colorcheckbox', 'pushdownspinner', 'playerseekbar', 'checkbox$check', 'inboxprogressbar', 'ratingspinner', 'viewcurrencyspinnerpreference', 'labeledtogglebutton', 'conditionalcheckedswitch', 'animatedswitcher', 'dotprogressbar', 'circularseekbarbass', 'adbreakseekbar', 'customprogressbar', 'strokeseekbar', 'multispinner', 'cynumberswitcher', 'timerprogressbar', 'dynamicradiobutton$customradiobutton', 'betterswitch', 'snappcheckbox', 'intermediatecheckbox', 'backwardcheckbox', 'hintspinnerview', 'fvrstartratingseekbarview', 'doodlecheckbox', 'regusseekbar', 'checkboxsummary', 'seekbarwithtextview', 'lockableseekbar', 'b4fcheckbox', 'mkradiobutton', 'circleprogressbarview', 'locomotiontypesradiobutton', 'progressbarwithpercentage', 'appcheckbox', 'mkspinner', 'shoppinglistsspinner', 'playlocalchannelstogglebutton', 'preferencesswitchview', 'checkboxchoice', 'pickerlongpressprogressbar', 'middleseekbar', 'labeledswitch', 'autoscaleradiobutton', 'videosliceseekbar', 'ljradiobutton', 'whiprogressbar', 'seekbarhorz', 'searchprogressbar', 'smallstarsratingbar', 'seekbaritemview', 'houndcheckbox', 'contentrefreshprogressbar', 'cuntouchableseekbar', 'teamspinner', 'loadingspinneratom', 'checkboxtonto', 'customthemeprogressbar', 'progressbarcompat', 'rightcheckbox', 'animatedprogressbar', 'larponrangeseekbar', 'progressspinner', 'customratingbar', 'seekbarlayout', 'animatehorizontalprogressbar', 'verticalswitchlinearlayout', 'supportseekbar', 'aviaryimagerestoreswitcher', 'mycheckbox', 'fragmentswitcher', 'zoomviewswitcher', 'colorseekbar', 'shopscoreratingbar', 'customthemeradiobutton', 'reversableseekbar', 'fvrcheckbox', 'resettableseekbar', 'checkboxholo', 'ndspinner', 'progressbarlayout', 'modalloadingspinner', 'selectiondifferentiatingspinner', 'spinnerlikematerialedittext', 'cmsspinner', 'switcherpanel', 'reactswitch', 'spinnerimageview', 'statespinner', 'verticalseekbarwrapper', 'profileaddressspinner', 'searchlistprogressbar', 'commonpositionseekbar', 'loadingspinnerview', 'likecheckbox', 'regusspinner', 'fabtogglebutton', 'numberspinnerview', 'progressbarrenderer', 'shapeprogressbar', 'slackprogressbar', 'validationedittextwithtogglebuttonsfield', 'gnspinner', 'refreshprogressbar', 'pageswitcher', 'whatsnewprogressbar', 'colorswitchpanelset', 'uaspinner', 'headermediaswitcher', 'reflectionspinner', 'actionbartogglecheckbox', 'animatedmuzeiloadingspinnerview', 'fpradiobutton', 'icsspinner', 'micswitcherview', 'progressbarcircularindeterminate', 'stackedhorizontalprogressbar', 'radiobuttoncell', 'serviceswitchermenu', 'rbprogressspinner', 'extendedcheckboxlistview', 'fioscheckbox', 'switchtablistview', 'addresstypespinner', 'typefacecheckbox']
def parseRico(jsonfile): 
    f = open(jsonfile,'r')
    data = json.load(f)
    R = []
    bnds = []
    queue = []
    try:
        queue.append(data['activity']['root']) 
    except:
        return 
    while len(queue) > 0:
        element = queue.pop()
        if element is None:
            continue
        if "children" in element.keys():
            queue += element["children"]
        # check class
        c = element['class'].split('.')[-1].lower()
        if c in targets_lower:
            # manually check progressbar in bad performance
            if c == 'progressbar':
                continue
            c = targets[targets_lower.index(c)]
        elif any(e in c for e in targets_lower):
            # manually filter
            # exlcude bad type and imagebutton & button
            if 'button' in c and not ('togglebutton' in c or 'radiobutton' in c):
                continue
            if  any(b in c for b in BAD):
                continue
            c = [targets[i] for i,e in enumerate(targets_lower) if (e in c.lower() and e != 'button')][0]
        else:
            continue
        # check bound
        bnd = element['bounds']
        if any(e < 0 for e in bnd) or bnd[0]>=bnd[2] or bnd[1]>=bnd[3] or bnd[0]>1440 or bnd[2]>1440 or bnd[1]>2560 or bnd[3]>2560 or bnd in bnds:
            continue
        if bnd[2]-bnd[0] < 10 or bnd[3]-bnd[1] < 10:
            continue
        R.append((c,bnd))
        bnds.append(bnd)
    return R

def parseSemantic(jsonfile):
    f = open(jsonfile,'r')
    data = json.load(f)
    bnds = []
    queue = []
    try:
        queue.append(data) 
    except:
        return 
    while len(queue) > 0:
        element = queue.pop()
        if element is None:
            continue
        if "children" in element.keys():
            queue += element["children"]
        if element['class'].split('.')[-1] == 'ImageButton' or element['class'].split('.')[-1] == 'Button':
            bnds += [element['bounds']]
    return bnds

def get_screenshots_from_rico():
    # merge rico info
    df1 = pd.read_csv('ui_details.csv')
    df2 = pd.read_csv('app_details.csv')
    df_ui = pd.merge(df1, df2, on='App Package Name')
    df_ui = df_ui[['UI Number', 'App Package Name',
        'Play Store Name', 'Category',
        'Number of Downloads', 'Date Updated']]
    df_ui.columns = ['UI Number', 'package_name',
        'application_name', 'category', 
        'downloads', 'date']

    for i,row in df.iterrows():
        targets = ["CheckBox","Button","Chronometer","RadioButton","RatingBar","SeekBar","Spinner","ToggleButton","ProgressBar","Switch","ImageButton"]
        targets_lower = ['checkbox', 'button', 'chronometer', 'radiobutton', 'ratingbar', 'seekbar', 'spinner', 'togglebutton', 'progressbar', 'switch', 'imagebutton']
        id = int(row['name'].split('-')[1])
        if id % 500 == 0:
            print(id)
        if id >= 11463:
            package = row['package_name']
            files = df_ui[df_ui["package_name"]==package]['UI Number'].tolist()
            for f in files:
                if not (os.path.exists(PATH_RICO+str(f)+'.json') and os.path.exists(PATH_RICO+str(f)+'.jpg')):continue
                # image = Image.open('/Users/mac/Documents/Python/Data/Rico/'+str(i)+'.jpg')
                # image = image.resize((1440,2560),Image.BICUBIC)
                ob = parseRico(PATH_RICO+str(f)+'.json')
                list1 = [x for x in ob if (x[0] == 'ImageButton' or x[0] == 'Button')]
                list2 = parseSemantic(PATH_SEMANTIC+str(f)+'.json')
                matched = [x for x in list1 if x[1] in list2]
                unmatched = len(list1) - len(matched)
                if unmatched >= Threshold:
                    ob = matched
                match = False
                for class_,bounds in ob:
                    class_bool = False
                    b_bool = False
                    p_bool = False
                    color_bool = False
                    # test class
                    if class_==row['widget_class']:
                        class_bool = True
                    else:
                        continue
                    # test bounds (normalise to 800*1280)
                    bounds = [bounds[0]/1.8,bounds[1]/2,bounds[2]/1.8,bounds[3]/2]
                    fake_bounds = row['coordinates']['from']+row['coordinates']['to']
                    if all(abs(bounds[i]-fake_bounds[i])<3 for i in range(len(bounds))):
                        b_bool = True
                    else:
                        continue
                    # test path
                    if os.path.exists(PATH_RICO+str(f)+'.jpg'):
                        p_bool = True
                    else:
                        continue
                    # test color
                    try:
                        image = cv2.imread(PATH_RICO+str(f)+'.jpg')
                        image = cv2.resize(image, (800, 1280), interpolation=cv2.INTER_CUBIC)
                        widgets = image[fake_bounds[1]:fake_bounds[3], fake_bounds[0]:fake_bounds[2]]
                    except:
                        continue
                    colors = get_color(widgets)
                    base_colors = row['color']
                    if type(colors) == int or type(base_colors) == int: continue
                    if 'Red' in colors.keys(): del colors['Red']
                    if 'Red2' in colors.keys(): del colors['Red2']
                    color_bool = all(abs(base_colors[c] - v)<=0.1 for c,v in colors.items())
                    if class_bool and b_bool and p_bool and color_bool:
                        match = True
                        break
                # extract bounding image
                if match:
                    cv2.rectangle(image, (fake_bounds[0],fake_bounds[1]), (fake_bounds[2],fake_bounds[3]), (0,0,255),2)
                    cv2.imwrite('./screenshots/'+package+'-'+str(f)+'-'+str(id)+'.png',image)
                    break


###########################################
###########  clean all widgets  ###########
###########################################
PATH_FROM = '/Users/mac/Documents/all_widgets/'
PATH_TO = './all_widgets/'
def clean():
    df_clean = pd.DataFrame(columns=['id','name','color','coordinates','dimensions','package_name','text','widget_class','application_name','downloads','url','category','Developer','font','sims','date','src'])
    screenshots = os.listdir('./screenshots/')
    if '.DS_Store' in screenshots: screenshots.remove('.DS_Store')
    df_id = df.copy()
    df_id['id'] = [int(x.split('-')[1]) for x in df_id.name.tolist()]
    
    for screenshot in screenshots:
        id = int(screenshot.split('-')[-1].replace('.png',''))
        series = df_id[df_id['id']==id].iloc[0]
        df_clean = df_clean.append({'id': id, 
                            'name':series['name'], 
                            'color':series['color'],
                            'coordinates':series['coordinates'],
                            'dimensions':series['dimensions'],
                            'package_name':series['package_name'],
                            'text':series['text'],
                            'widget_class':series['widget_class'],
                            'application_name':series['application_name'], 
                            'downloads':series['downloads'], 
                            'url':series['url'],
                            'category':series['category'],
                            'Developer':series['Developer'],
                            'font':series['font'],
                            'sims':series['sims'],
                            'date':series['date'],
                            'src':screenshot}, ignore_index=True)
        shutil.copyfile(PATH_FROM+series['name']+'.png',PATH_TO+series['name']+'.png')
    f = open('result.json','w')
    f.write(df_clean.to_json(orient='records', force_ascii=False))
    f.close()

if __name__ == '__main__': 
    get_screenshots_from_verbo()
    get_screenshots_from_rico()
    clean()
    # df = pd.read_json('result.json',orient='records')