import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import json
import tqdm
from PIL import ImageFile, Image, ImageDraw
ImageFile.LOAD_TRUNCATED_IMAGES = True

targets = ["CheckBox","Button","Chronometer","RadioButton","RatingBar","SeekBar","Spinner","ToggleButton","ProgressBar","Switch","ImageButton"]
targets_lower = ['checkbox', 'button', 'chronometer', 'radiobutton', 'ratingbar', 'seekbar', 'spinner', 'togglebutton', 'progressbar', 'switch', 'imagebutton']

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

def read():
    c = []
    # 72219
    for i in tqdm.tqdm(range(72219)):
        imgfrom_ = 
        if not (os.path.exists('../Data/Rico/'+str(i)+'.json') and os.path.exists('../Data/Rico/'+str(i)+'.jpg')):
            continue
        # image = Image.open('../Data/Rico/'+str(i)+'.jpg')
        # image = image.resize((1440,2560),Image.BICUBIC)
        candidates = parseRico('../Data/Rico/'+str(i)+'.json')
        # check any noise in candidate
        # since rico sematic only consider Button and ImageButton
        # 1. extract all button and imagebutton in our candidates
        # 2. compare candidates and semantic
        # 3. if greater than threshold, only keep matched candidates and remove others (including other types)
        threshold = 2
        list1 = [x for x in candidates if (x[0] == 'ImageButton' or x[0] == 'Button')]
        list2 = parseSemantic('/Users/mac/Downloads/semantic_annotations/'+str(i)+'.json')
        matched = [x for x in list1 if x[1] in list2]
        unmatched = len(list1) - len(matched)
        if unmatched >= threshold:
            candidates = matched

         # Annotations
        c += [x[0] for x in candidates]
        if len(candidates) == 0: 
            continue
        img = Image.open(imgfrom_)
        img_name = imgfrom_.split('/')[-4]+imgfrom_.split('/')[-1]
        img_width, img_height = img.size
        img_depth = 3
        tree = pascal_xml(img_name,img_width, img_height,img_depth,ob)
        tree.write("./Annotations/"+a+"_"+i)
        # JPEGImages
        to = "./JPEGImages/"+a+"_"+i.replace('xml','png')
        copyfile(imgfrom_,to)
        # Main
        f = open("./ImageSets/Main/train.txt","a")
        f.write(a+"_"+i.replace('.xml','')+'\n')
        f.close()
    
    from collections import Counter
    print(Counter(classes))
            



if __name__ == '__main__': 
    # generate pascal format dataset
    read()
    # Counter({'ImageButton': 32606, 'Button': 26112, 'RadioButton': 5436, 'CheckBox': 4980, 'Spinner': 3495, 'Switch': 3186, 'ToggleButton': 2445, 'SeekBar': 1996, 'RatingBar': 1143, 'Chronometer': 32})