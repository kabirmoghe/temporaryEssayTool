import pandas as pd
import plotly.graph_objects as go
import docx

import nltk
from nltk import pos_tag
from nltk import RegexpParser


def readFile(file):
    name = file["Student Name"].iloc[0]
    essay = file["Type of Essay"].iloc[0]
    draft = file["Draft Number"].iloc[0]
    comments = file["Total Number of Comments (Tallies)"].iloc[0]
    words = file["Total Words"].iloc[0]
    
    return name, essay, draft, comments, words

def aggregate(all_drafts):

    df = pd.DataFrame(columns = ['Student Name', 'Total Number of Drafts Shared','Total Number of Comments', 'Total Words', 'Number of Comments/Words','Mechanical Tallies', 'Ideas Tallies', 'Movement Tallies', 'Structure Tallies', 'Date of Submission', 'Total Number of Drafts', 'Total Number of Days'])
    
    drafts = len(all_drafts)

    comments = 0
    words = 0
    mechanical = 0
    ideas = 0
    movement = 0
    structure = 0
    submission = ""
    drafts_total = 0
    days = 0

    for draft in all_drafts:

        comments += int(draft["Total Number of Comments (Tallies)"].iloc[0])
        words += int(draft["Total Words"].iloc[0])
        mechanical += int(draft["Mechanical Tallies"].iloc[0])
        ideas += int(draft["Ideas Tallies"].iloc[0])
        movement += int(draft["Movement Tallies"].iloc[0])
        structure += int(draft["Structure Tallies"].iloc[0])

    last = all_drafts[-1]

    name, submission, days, drafts_total = last["Student Name"].iloc[0], last["Date of Submission"].iloc[0], int(last["Number of days up to this point"].iloc[0]), last["Draft Number"].iloc[0]
    
    u = pd.concat(all_drafts).reset_index(drop = True)

    u = u.sort_values("Draft Number")
    if "Unnamed: 0" in u.columns:
        u.drop("Unnamed: 0", axis = 1, inplace = True)
    u["Total Number of Comments (Tallies)"] = pd.to_numeric(u["Total Number of Comments (Tallies)"])

    # PLOTS ALL TALLIES VS. DRAFTS

    fig = go.Figure()

    fig.add_trace(go.Scatter(
            name='Mechanical',
            x=u['Draft Number'],
            y=u['Mechanical Tallies'],
            marker=dict(
                color='#69F68C'),
        ))

    fig.add_trace(go.Scatter(
            name='Ideas',
            x=u['Draft Number'],
            y=u['Ideas Tallies'],
            marker=dict(
                color='#EAB7F9')
        ))


    fig.add_trace(go.Scatter(
            name='Movement',
            x=u['Draft Number'],
            y=u['Movement Tallies'],
            marker=dict(
                color='#FF8195')
        ))


    fig.add_trace(go.Scatter(
            name='Structure',
            x=u['Draft Number'],
            y=u['Structure Tallies'],
            marker=dict(
                color='#FFC300')
        ))

    fig.update_traces(hoverinfo = 'text+name+y')

    fig.update_layout(
        yaxis_title='Tally', xaxis_title = 'Draft Number', font_family="Raleway", hoverlabel_font_family = 'Raleway', hovermode = "x unified", margin = dict(l=0,r=0,b=10,t=10))

    config = {'displayModeBar': False}

    fig.write_html('templates/{}tallyPlot.html'.format(name), full_html = False, config = config)

    return [drafts, comments, words, comments, mechanical, ideas, movement, structure, submission, drafts_total, days], u

def docPOS(doc): # PARTS OF SPEECH (POS)

    # Gets full text as paragraphs

    fullText = []
    for para in doc.paragraphs:
        txt = para.text
        if txt != "" and txt != " ":
            fullText.append(txt)

    # Gets tuples of words and parts of speech in the full text

    end = []

    for p in fullText:
        p = p.split()     
        tokens_tag = pos_tag(p)
        patterns= """mychunk:{<NN.?>*<VBD.?>*<JJ.?>*<CC>?}"""
        chunker = RegexpParser(patterns)
        x = chunker.parse(tokens_tag)
        
        for word in x:
            
            pair = tuple(word)
            
            if len(pair) == 1:
                end.append(pair[0])
            else:
                
                if type(pair[0]) == str:
                    end.append(pair)
                else:
                    for group in pair:
                        end.append(group)    

    # Data frame 

    def replace(pos):
        if pos=='JJR' or pos=='JJS':
            return "JJ"
        elif pos=="NNS" or pos=="NNP" or pos=="NNPS":
            return "NN"
        elif pos=="PRP$":
            return "PRP"
        elif pos=="RBR" or pos=="RBS":
            return "RB"
        elif pos=="VBG" or pos=="VBD" or pos=="VBN" or pos=="VBP" or pos=="VBZ":
            return "VB"
        else:
            return pos

    posTbl = pd.read_html('table.html')[0]
    posKey = dict(posTbl.values)

    posKey.pop("JJR")
    posKey.pop("JJS")
    posKey.pop("NNS")
    posKey.pop("NNP")
    posKey.pop("NNPS")
    posKey.pop("PRP$")
    posKey.pop("RBR")
    posKey.pop("RBS")
    posKey.pop("VBG")
    posKey.pop("VBD")
    posKey.pop("VBN")
    posKey.pop("VBP")
    posKey.pop("VBZ")

    colors = ["#D83333", "#1054A2", "#48C460", "#DCA83D", "#8215B9", "#6BBEDA", "#805F30", "#D094CA", "#7E7E7E", "#7E7E7E", "#7E7E7E", "#7E7E7E", "#7E7E7E", "#7E7E7E", "#7E7E7E", "#7E7E7E", "#7E7E7E", "#7E7E7E", "#7E7E7E", "#7E7E7E", "#7E7E7E"]
    colorDict = {}

    for i in range(len(posKey.keys())):
        colorDict[list(posKey.keys())[i]] = colors[i]
    
    end = []

    for p in fullText:
        
        para = []
        
        p = p.split()     
        tokens_tag = pos_tag(p)
        patterns= """mychunk:{<NN.?>*<VBD.?>*<JJ.?>*<CC>?}"""
        chunker = RegexpParser(patterns)
        x = chunker.parse(tokens_tag)
        
        for word in x:
            
            pair = tuple(word)
            
            if len(pair) == 1:
                para.append(pair[0])
            else:
                
                if type(pair[0]) == str:
                    para.append(pair)
                else:
                    for group in pair:
                        para.append(group) 
        
        end.append(para)

    wordList = []
    iPosList = []

    for para in end:
        
        wList = []
        pList = []
        
        for pair in para:
            wList.append(pair[0])
            pList.append(pair[1])
        
        wordList.append(wList)
        iPosList.append(pList)


    posList = []

    for para in iPosList:
        pList = [replace(pos) for pos in para]
        posList.append(pList)    

        
    dfList = []

    for i in range(len(end)):
        df = pd.DataFrame(columns=["Words", "POS"])

        df["Words"] = wordList[i]
        df["POS"] = posList[i]
        df["Full Text"] = df["POS"].map(posKey)
        df["Color"] = df["POS"].map(colorDict)
        listData = df.to_dict(orient='split')['data']
        dfList.append(listData)

    finalList = []
    
    
    for i in range(len(dfList)):
        
        curr = dfList[i]
        
        if curr != []:
            finalList.append(curr)
    
    usedColors = {}
    
    for para in finalList:
        for item in para:
            color = item[-1]
            if type(color) == str:
                if color not in usedColors:
                    usedColors[color] = 1
                else:
                    usedColors[color] = usedColors[color]+1
    
    colorLabels = []

    for color in usedColors.keys():
        if type(color) == str:
            if color =="#7E7E7E":
                colorLabels.append([color, "Other"])
            else:
                abbrevLabel = dict((v, k) for k, v in colorDict.items())[color]

                colorLabels.append([color,posKey[abbrevLabel]])
    
    return finalList, colorLabels, usedColors

def docSentence(doc): # SENTENCE LENGTH
    text = []
    for para in doc.paragraphs:
        txt = para.text
        if txt != "" and txt != " ":
            text.append(txt)

    p_sentences = []

    for p in text:
       
        sentences = []
       
        for sentence in p.split("."):
            if sentence != "" and sentence != " ":
                if sentence[-1] != "?" and sentence[-1] != "!":
                    sentences.append(sentence+".")
                else:
                    sentences.append(sentence)
               
        p_sentences.append(sentences)


    def getLength(sentence):
        length = 0
        for word in sentence.split():
            length += 1
        
        return length

    def classifySentence(sentence):
        length = getLength(sentence)
        if length > 25:
            return "Very Long"
        elif length > 20:
            return "Long"
        elif length >= 10:
            return "Medium"
        elif length >= 5:
            return "Short"
        else:
            return "Very Short"

    def punctuationFilter(paraList, punct):

        modified = []

        for p in paraList:

            sentences = []

            for sentence in p:
                if punct in sentence:
                    
                    punctSplit = sentence.split(punct)
                    
                    sentences.append(punctSplit[0]+punct)
                    sentences.append(punctSplit[1])
                else:
                    sentences.append(sentence)
            
            modified.append(sentences)
                    
        return modified
            
    categories = {"Very Short":"#DF8CE3", "Short":"#8CCBE3", "Medium":"#8CE397", "Long":"#E3D78C", "Very Long":"#E3938C"}
    #colors = ["#DF8CE3", "#8CCBE3", "#8CE397", "#E3D78C", "#E3938C"]

    p_types = []

    exclaim_cleared = punctuationFilter(p_sentences, "!") # Deals with !
    final_sentences = punctuationFilter(exclaim_cleared, "?") # Deals with ?

    for para in final_sentences:
        p_types.append([categories[classifySentence(s)] for s in para])
            
    pairs = []
        
    for i in range(len(final_sentences)):
        
        para = []
        
        for j in range(len(final_sentences[i])):
            
            para.append([final_sentences[i][j], p_types[i][j]])
            
        pairs.append(para)

    # TYPE TALLY    

    typeTally = {}

    for para in p_types:
        for color in para:
            if type(color) == str:
                if color not in typeTally:
                    typeTally[color] = 1
                else:
                    typeTally[color] = typeTally[color]+1

    typeInfo = []

    for sType in categories:
        
        color = categories[sType]
        
        if color not in typeTally:
            typeTally[color] = 0
        
        typeInfo.append([sType, color, typeTally[color]])

    return pairs, typeInfo

