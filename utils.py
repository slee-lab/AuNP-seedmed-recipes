from regex_patterns import *
from chemdataextractor.doc import Paragraph 

def filter_overlap(searchresults,debug=False):
    """
    remove overlapping spans, as keywords have overlaps and have different subcategories 
    patch: sometimes length span is not always the answer, if same length detected after introducing \w*, we also give priority to the category, hydrates are more "specific"
    input: (list(category) of list(keywords) of dict)
            [
             [{'category': 'AuCl3', 'span': (68, 86), 'text': 'gold(III) chloride'}],
             [{'category': 'HAuCl4', 'span': (0, 6), 'text': 'HAuCl4'},
              {'category': 'HAuCl4', 'span': (46, 52), 'text': 'HAuCl4'},],
             [{'category': 'HAuCl4·3H2O', 'span': (46, 57), 'text': 'HAuCl4⋅3H2O'}],
             [{'category': 'HAuCl4·4H2O', 'span': (68, 99), 'text': 'gold(III) chloride tetrahydrate'}]
            ]
    output: (list of dict)
            [{'category': 'HAuCl4', 'span': (0, 6), 'text': 'HAuCl4'},
             {'category': 'HAuCl4·3H2O', 'span': (46, 57), 'text': 'HAuCl4⋅3H2O'},
             {'category': 'HAuCl4·4H2O', 'span': (68, 99), 'text': 'gold(III) chloride tetrahydrate'}]
    """
    toks=sorted([match for cat in searchresults for match in cat], key=lambda tuple1: tuple1['span']) #flatten and sort by span
    if debug:
        print("toks in sorted span order:", toks)
    toks_idx_2delete=[]
    scan={'span':(-1,-1)} #scan is copy of last(most previous) token.
    for i in range(len(toks)):
        if debug:
            print("prev_tok ",scan['span'], "current_tok ",toks[i]['span'])
        tokstart=toks[i]['span'][0]
        tokend=toks[i]['span'][1]
        if scan['span']==toks[i]['span']: # this can happen because of generous regex we usepatch
            if scan['category'] in toks[i]['category']: # this also covers same category cautght by two different regexs
                toks_idx_2delete.append(i-1)
                scan=toks[i]
            elif toks[i]['category'] in scan['category']:
                toks_idx_2delete.append(i)
                #(DONT update scan)
            #still AuCl3 is not in HAuCl4
            elif len(scan['category']) < len(toks[i]['category']):
                toks_idx_2delete.append(i-1)
                scan=toks[i]
            else:
                toks_idx_2delete.append(i)
                #(DONT update scan)
        elif scan['span'][1] < tokstart: 
            scan=toks[i]
        else:# tokstart <= scan[1]
            if scan['span'][1] >= tokend: #(9, 26) met (19, 26), or even (19,20). former replaces latter
                assert scan['span'][0] < tokstart
                toks_idx_2delete.append(i)
                #(DONT update scan)
            elif scan['span'][0] == tokstart: # (46,52) met (46,57) which means latter(tok) replaces former(scan).
                assert scan['span'][1] < tokend 
                toks_idx_2delete.append(i-1)
                scan=toks[i]
            else: #partial overlap. (46,52) met (50,57)
                if scan['category']==toks[i]['category']:
                    toks_idx_2delete.append(i-1)
                span_new=(scan['span'][0],tokend)
                text_new=scan['text']+toks[i]['text'][-(tokend-scan['span'][1]):]
                scan['span']=span_new
                scan['text']=text_new
                toks[i]['span']=span_new
                toks[i]['text']=text_new        
        
    toks_idx_2delete=reversed(toks_idx_2delete)
    for i in toks_idx_2delete:
        toks.pop(i)
        
    return toks


def regex_search(keyset,text,sub2cat=None,debug=False):
    """
    input: keyset (dict)  {cat: list of regex keywords}
    output: list of dict with span, text, and category as keys.
    """
    searchresults=[]
    if isinstance(keyset,str):
        keyset={'default_cat':[keyset]}
    for cat,keys in keyset.items():
        searchresult=[]
        if debug:
            for key in keys:
                print("key",key)
                for search in re.finditer(key,text):
                    # print({'text':search.group(),'span':search.span(), 'category':cat} )
                    search_thiskey={'text':search.group(),'groups':search.groups(),'span':search.span(), 'category':cat}
                    print(search_thiskey)
                    searchresult.append(search_thiskey)
            if len(searchresult)>0:
                searchresults.append(searchresult)
        else:
            # if sub2cat is None:
            #     searchresult=[{'text':search.group(),'groups':search.groups(),'span':search.span(), 'category':cat} for key in keys for search in re.finditer(key,text)]
            # else:
            #     searchresult=[{'text':search.group(),'groups':search.groups(),'span':search.span(), 'category':cat} for key in keys for search in re.finditer(key,text)]
            searchresult=[{'text':search.group(),'groups':search.groups(),'span':search.span(), 'category':cat} for key in keys for search in re.finditer(key,text)]
            if len(searchresult)>0:
                searchresults.append(searchresult)
    if sub2cat is None:
        if debug:
            return filter_overlap(searchresults, debug=True)
        else:
            return filter_overlap(searchresults)
    else:
        if debug:
            filteredlist=filter_overlap(searchresults, debug=True)
        else:
            filteredlist=filter_overlap(searchresults)

        for i in range(len(filteredlist)):
            filteredlist[i]['subcategory']=filteredlist[i]['category']
            filteredlist[i]['category']=sub2cat[filteredlist[i]['category']]
        return filteredlist


def morph_acronym_catcher(text,target,debug=False): 
    outputdict={}

    if target=='Au':
        acronym_regex=goldmorphacronym_regex_strict
    elif target=='Ag':
        acronym_regex=silvermorphacronym_regex_strict
    elif target=='Cu':
        acronym_regex=coppermorphacronym_regex_strict
    elif target=='Pt':
        acronym_regex=ptmorphacronym_regex_strict
    elif target=='Pd':
        acronym_regex=pdmorphacronym_regex_strict

    rgxsrch = regex_search(acronym_regex,text)

    if len(rgxsrch)>0:
        for srch in rgxsrch:

            if debug:
                try:
                    srch['groups'][0][-1]=='s'
                except:
                    pass
            if srch['groups'][0][-1]=='s':
                raveledtext=srch['groups'][0][:-1]
            else:
                raveledtext=srch['groups'][0]

            if (srch['groups'][1][0:2]=='Au' or srch['groups'][1][0]=='G') and srch['groups'][0][1:4]!='old' and srch['groups'][0][:2]!='Au':
                raveledtext='Gold '+raveledtext


            outputdict[srch['groups'][1]]=raveledtext
    return outputdict

def convert_goldmorphacronym(text,goldacronymtable):
    for key in goldacronymtable.keys():
        if isinstance(text,str):
            text=text.replace(key,goldacronymtable[key])
        elif isinstance(text,dict):
            text['text']=text['text'].replace(key,goldacronymtable[key])
    return text   


def trimspace(text):
    if text=="":
        return text
    elif text.startswith(" "):
        return trimspace(text[1:])
    elif text.endswith(" "):
        return trimspace(text[:-1])
    else:
        return text

def process_regex_groups(rgx_output1,targets_split):
    rgx_output=rgx_output1.copy()
    for morph in rgx_output:
        processed_grp=[trimspace(grp) for grp in morph['groups'] if grp is not None]
        if processed_grp==[]:
            morph['groups']=[] # all none
        else:
            #enforce regex gets only target category
            if all([grp in targets_split for grp in processed_grp]):
                morph['groups']=[targets_split[0]] #e.g. Au
            else:
                morph['groups']=['other']
    return rgx_output

def detect_anytarget_morph(target,text_input,debug=False):
    rgxrslt=regex_search(morphdicts[target],text_input)
    if debug:
        pprint(rgxrslt)
    rgxrslt = process_regex_groups(rgxrslt,targets_split=targets_split_dict[target])
    cats = list(set([morph['groups'][0] if len(morph['groups'])==1 else 'blank' for morph in rgxrslt]))
    if target in cats:
        # filter out other, dont know if blank is gold or other target
        output = [morph for morph in rgxrslt if morph['groups']!=['other']]
    elif cats==['blank']:
        output = rgxrslt[:]
    else:
        output = []
    return output


 

def removecomps(listinput,listtorm):
    list1=listinput.copy()
    # listtormapp=[comp for comp in listtorm if comp in listinput]
    # [list1.remove(comp) for comp in listtormapp]
    for comp in listtorm:
        list1 = list(filter(lambda a: a != comp, list1))
    return list1

def contains_precamount(text,preconly=False,HAuCl4ind=False,debug=False):
    rsltlist = parse_prec_amounts_regex(text)
    if debug:
        print(rsltlist)
   
    if len(rsltlist)>0:
        if preconly: return True
        else:
            return any([True if len(list(prec.items())[0][1])>0 else False for prec in rsltlist])
    else:
        return False

def pars_sents_tokenizer(input1):
    pars = removecomps(input1.split("\n"),['']) # par tokenization
    sentsinpars = [Paragraph(partext).sentences for partext in pars]

    input1=[] # empty it and rewrite with tokenized ver
    pars_containprecamount=[]
    for paridx in range(len(pars)):
        
        pars_containprecamount.append(contains_precamount(pars[paridx]))

        for sent in Paragraph(pars[paridx]).sentences:
            input1.append({'senttext':sent.text,'paridx':paridx,'HAuCl4amount':contains_HAuCl4amount(sent.text),'precamount':contains_precamount(sent.text),'prec':contains_precamount(sent.text,preconly=True)})
    return input1,pars_containprecamount

def subrecipe_separate(input1,version="v1.1",debug=False,HAuCl4switch=False,initiate_whenprecamounts=False):

    status='None'
    seedsln=[]
    growthsln=[]
    mixsln=[]
    seedamount=[]
    seedamountunit=[]
    growth_END=False
 
    if version=='v1.1':
        input1,pars_containprecamount = pars_sents_tokenizer(input1)

        if pars_containprecamount==[]:
            return "error: no precamounts", sent
        for idx in range(len(input1)): # sentence iteration
            sent = input1[idx]['senttext']
            thisparidx = input1[idx]['paridx']      

            if debug:
                searchrslt=regex_search(Subrecipe_Dict_regex,sent)
                pprint(searchrslt)
            for cleantok in spaces_global:
                sent.replace(cleantok,' ')

            sentclasses=list(set([comp['category'] for comp in regex_search(Subrecipe_Dict_regex,sent)]))
            mixstep = regex_search(SeedinGrowth_Dict_regex,sent)
            # print(status,sent)
            if status=='None' and len(seedsln)==0 and len(growthsln)==0:
                if initiate_whenprecamounts and not pars_containprecamount[thisparidx]:
                    continue

                sentclasses = removecomps(sentclasses,['FinalProd']) # FinalProd does not mean growth sln in this case.

                if sentclasses == ['GrowthSln']:  # This should not be GrowthSln due to "grown": Uniform Au nanorods were grown using the seed-mediated growth process described previously. so when switching from None to GrowthSln you should check no "growth" or "seed-mediated" is mentioned 
                    if len(regex_search({'_':["[gG]row(?:th solution)?","[sS]eed[\s\-–]mediated"]},sent))!=0:
                        continue

                if len(mixstep)==1:
                    growthsln.append(idx)
                    mixsln.append(idx)
                    status='mix'
                    if len(mixstep[0]['groups'])!=0: # [] can happen from "different amounts of seed sln"
                        seedamount.append(mixstep[0]['groups'][0])
                        seedamountunit.append(mixstep[0]['groups'][1])


                if len(sentclasses)>0: # either seed or growth

                    if sentclasses==['SeedSln']:# INITIATE: 'None' -> 'Seedsln'

                        for i in range(idx): #scan from beginning, for previous sentences than this sent idx
                            if input1[i]['paridx']==thisparidx and input1[i]['precamount']: # so from here include until current sent
                                for j in range(i,idx):
                                    seedsln.append(j)
                                break
                        seedsln.append(idx)

                    elif sentclasses==['GrowthSln']:# INITIATE: 'None' -> 'GrowthSln'

                        for i in range(idx): #scan from beginning, for previous sentences than this sent idx
                            if input1[i]['paridx']==thisparidx and input1[i]['precamount']: # so from here include until current sent
                                growthsln.append(i)
                        growthsln.append(idx)

                    else:
                        if debug:
                            print("\nerror- one sentence with seed and growth, or directly to mix from none\n", sentclasses, "\n",sent)#, sent['sentence']

                        if not contains_precamount(sent):#consider as summary before initiation. e.g. "The gold nanoseeds were synthesized first and a growth process was performed 30 min afterwards.
                            continue
                        else:
                            return "error: sentclasses", sent

                    status = sentclasses[0]      
            
            elif status in ['SeedSln','GrowthSln']:
                otherstatus = removecomps(['SeedSln','GrowthSln'],[status])[0]

                if len(mixstep)==1: # STATUS: -> 'MIX' but also include this sent to growth.
                    # example "Step two, to obtain the Au NRs, 5 mL of aqueous HAuCl4 solution (5.0 mM), 75 μL of aqueous AgNO3 solution (0.1 M), 30 mL of aqueous CTAB solution (0.2 M), 75 μL of aqueous HCl solution (2.0 M), and 3.5 mL of aqueous ascorbic acid solution (0.1 M) were mixed, followed by the addition of 0.1 mL of the Au seed solution."
                    growthsln.append(idx)
                    mixsln.append(idx)
                    status='mix'
                    if len(mixstep[0]['groups'])!=0: # [] can happen from "different amounts of seed sln"
                        seedamount.append(mixstep[0]['groups'][0])
                        seedamountunit.append(mixstep[0]['groups'][1])
                    
                elif len(mixstep)==0: #we either keep going or switch to the other
                    if status not in sentclasses:
                        if otherstatus in sentclasses: # if other switch to other
                            if status=='SeedSln':
                                if len(growthsln)==0:
                                    growthsln.append(idx)
                                    status = otherstatus
                                else:
                                    seedsln.append(idx)
                            else:#if status=='GrowthSln'
                                if len(seedsln)==0:
                                    seedsln.append(idx)
                                    status = otherstatus
                                else:
                                    growthsln.append(idx)


                        elif status=='SeedSln' and 'FinalProd' in sentclasses: #switch to Growth e.g. NP -> NR
                            growthsln.append(idx)             
                            status = otherstatus
                        elif input1[idx-1]['paridx']!=thisparidx and input1[idx]['precamount']: # if paragraph change and precamount exist, switch.
                            if status=='SeedSln': growthsln.append(idx)
                            else: seedsln.append(idx)
                            status = otherstatus                           

                        else:
                            
                            if HAuCl4switch and any([input1[sentidx1]['HAuCl4amount'] for sentidx1 in range(idx)]) and input1[idx]['HAuCl4amount'] and len(growthsln)*len(seedsln)==0: #prev sents had HAuCl4 and this sent have HAuCl4 and has not already switched-> switch:
                                if status=='SeedSln': growthsln.append(idx)
                                else: seedsln.append(idx)
                                status = otherstatus                                
                            else: #keep going
                                if status=='SeedSln': 
                                    seedsln.append(idx) 
                                else: #status=='GrowthSln'
                                    growthsln.append(idx)                                
                    else: 
                        if status=='SeedSln' and ('FinalProd' in sentclasses or 'GrowthSln' in sentclasses):
                            if 'FinalProd' in sentclasses and not contains_precamount(sent): #keep going. e.g. 'This solution was stored at room temperature within 1−3 h and was used as the seed solution for the synthesis of gold nanorods.'
                                #keep going.
                                seedsln.append(idx)    
                            else:
                                # print(sentclasses)
                                return 'error: conflicting sentclasses when switching', sent
                        elif status=='GrowthSln' and ('SeedSln' in sentclasses):
                            return 'error: conflicting sentclasses when switching', sent
                        else: #keep going
                            if status=='SeedSln': 
                                seedsln.append(idx) 
                            else: #status=='GrowthSln'
                                growthsln.append(idx)  
                else:
                    if debug:
                        print('error: two mixstep detection ',sent)
         
                    return 'error: two mixstep detection ',sent
           

            elif status=='mix': 
                if thisparidx==input1[mixsln[0]]['paridx']: #same par

                    if growth_END:

                        growth_END=True
                        mixsln.append(idx)
 

                    else: # still look for precs if they are not yet to be parsed.
                        if check_stringsinsent(breakstrings, sent):
                            # print()
                            growth_END=True
                        growthtext="" # growthtext until now.
                        for growthidx in growthsln:
                            growthtext+=input1[growthidx]['senttext']
                        # print("printinghere",growthtext)
                        growthprecs_tillnow = [prec['precursor_category'] for prec in precnormalize_amount_grouponly(parse_prec_amounts_regex(growthtext)) if len(prec['amount'])>0]                      
                        # precs_thissent = [prec['precursor_category'] for prec in precnormalize_amount_grouponly(parse_prec_amounts_regex(sent)) if len(prec['amount'])>0]
                        precs_thissent = [prec['precursor_category'] for prec in precnormalize_amount_grouponly(parse_prec_amounts_regex(sent)) if len(prec['amount'])>0]#UPDATE30AUG2022: should work on sentence BEFORE the centrifuge redisperse etc mentioned.
                        
                        # prec_yettobeadded=[prec for precs_thissent if prec not in growthprecs_tillnow]
                        if len([prec for prec in precs_thissent if prec not in growthprecs_tillnow])>0:
                            growthsln.append(idx)
                        else:
                            mixsln.append(idx)

                else:# paragraph change -> end sentence iteration
                    break

        if len(seedamount)>1 or len(seedamountunit)>1:
            return 'error: 2 or more seedamount ',sent
        if status=='None':
            return 'error: subrecipe not initiated ',sent
        return seedsln, growthsln, mixsln, seedamount, seedamountunit, status


def parse_prec_amounts_inner(text,rgxrslt=["do_regex"], debug=False,standardizeunit=True,return_regexPREC=True):
    """tokenized_sents=Paragraph(text).sentences,rgxrslt_sents=[regex_search(Prec_Dict_regex_noaqueous, sent.text) for sent in Paragraph(text).sentences]

    # Note:  text should be sentence text, rgxrslt should have keys: span, text

    # united output form like that of prec_NER: [{'Hexadecyltrimethyl ammonium bromide': ['291.56', 'mg']}, {'CTAB': []}, {'HAuCl4': ['68', 'μL', '0.5', 'M']}, {'CTAB': []}]
    # output will be processed if units combination is allowed in precnormalize_amount

    Consider parsing for:
    After each cycle, the supernatant was removed and the pellet containing GNRs is diluted to reach a final ligand concentration of CTAB of 0.5 mM.

    if return_regexPREC, consider only sentence inputs, not paragrpahs.

    """
    if rgxrslt==['do_regex']:
        rgxrslt=regex_search(Prec_Dict_regex_noaqueous, text)
        # print(rgxrslt)
    
    rsltlist=[]
    loopindicator=0

    for sent in [text]:#assume always one sent

        loopindicator=1
        if isinstance(sent, str):
            senttext=sent
        else:
            senttext=sent.text
        
        if len(rgxrslt)==0:

            continue


        senttext_PRECmasked = senttext
        firstprec=True

        rgxrslt_idx=len(rgxrslt)-1

        

        for prec in reversed(rgxrslt):
            
            if firstprec:
                senttext_PRECmasked=senttext_PRECmasked[:prec['span'][0]]+"PREC"+senttext_PRECmasked[prec['span'][1]:]
                firstprec=False
            else:
                if lastspan==prec['span']:

                    rgxrslt.pop(rgxrslt_idx)
                    
                else:
                    senttext_PRECmasked=senttext_PRECmasked[:prec['span'][0]]+"PREC"+senttext_PRECmasked[prec['span'][1]:]
            rgxrslt_idx = rgxrslt_idx-1

            lastspan=prec['span']



        rgx_PREConly = regex_search({'_':['PREC']}, senttext_PRECmasked)

        assert len(rgx_PREConly)==len(rgxrslt), senttext #should be perfect matching

        rgx_PREC = regex_search(amountparse_regex, senttext_PRECmasked)
        if len(rgx_PREConly)>len(rgx_PREC): #we had PREC seed solution, PREC[\/\-‐−–]PREC forms that was not counted in rgx_PREC, should 
            # rgx_PREC_spanlist=[precamount['span'] for precamount in rgx_PREC]
            for PRECidx in reversed(range(len(rgx_PREConly))):
                PREC=rgx_PREConly[PRECidx]
                if any([span_includes(PREC['span'],precamount['span']) for precamount in rgx_PREC]): # note, should be one True  if exist
                    pass
                else: # remove this PREC from rgxrslt
                    # print("remove",rgxrslt[PRECidx])
                    rgxrslt.pop(PRECidx)

        if debug:
            print(senttext)
            print(rgxrslt)
            print()
            print(senttext_PRECmasked)
            pprint(rgx_PREConly)
            print()
            print(senttext_PRECmasked)
            pprint(rgx_PREC)
            print()

        PRECnum_peramount=[search['text'].count("PREC") for search in rgx_PREC]

        if PRECnum_peramount==[]:
            continue


        elif max(PRECnum_peramount)>=2:

            rgxrslt_grouped=[]
            rgxrslt_idx=0
            for PRECnum in PRECnum_peramount:
                rgxrslt_grouped.append(rgxrslt[rgxrslt_idx:rgxrslt_idx+PRECnum])
                rgxrslt_idx=rgxrslt_idx+PRECnum

            for grp in rgxrslt_grouped:
                if len(list(set([map_precsubcat2cat[comp['category']] for comp in grp])))==1: #  all same category prec in one group

                    pass
                elif len(list(set([map_precsubcat2cat[comp['category']] for comp in grp])))>1:

                    if return_regexPREC:
                        return [], rgx_PREC, senttext_PRECmasked
                    else:
                        return []
        

        assert sum(PRECnum_peramount)==len(rgxrslt), print(senttext,"\n",rgxrslt,"\n",senttext_PRECmasked,"\n",rgx_PREC)

        amounts = [parse_amounts_fromphrase(rgxprec,standardizeunit=standardizeunit) for rgxprec in rgx_PREC]

        if len(amounts)>1: #multiple amounts, with 1st one having concent, vol and rest having only concent
            firstunt=unitclass(amounts[0]["1st_unit"])
            secondunt=unitclass(amounts[0]["2nd_unit"])


        rgxrslt_idx=-1
        for idx in range(len(rgx_PREC)):
            outputdict={}
            amount = amounts[idx] 

            amount_list = [item for key, item in amount.items() if item is not None]

            rgxrslt_idx+=PRECnum_peramount[idx]
            precname=rgxrslt[rgxrslt_idx]['text']
            outputdict[precname]=amount_list
            rsltlist.append(outputdict)    


    if return_regexPREC:
        if loopindicator==0:
            return rsltlist, [], ""
        elif len(rgxrslt)==0:
            return rsltlist, [], ""
        else:
            return rsltlist, rgx_PREC, senttext_PRECmasked
    else:
        return rsltlist

def parse_prec_amounts_regex(text,tokenized_sents=[],precNERrslt=['do_regex'],debug=False,standardizeunit=True,mode='default'):

    """

    # Note:  text should be sentence text, rgxrslt should have keys: span, text

    Solved x mL containing 0.1 M PREC11, 0.2 M PREC22 issue. in this case, outputs following.
    PREC11: [x mL 0.1 M ], PREC22: [0.3 mol]


cocent  concent (volconcent concent concent)    volconcent  (volconcent concent)    concent
0       1       2           3       4           5           6           7           8


if current == concnet: 
    if (consec_flag or prev = volconcent) and (canbelinked_nothingbetwn): #first hit at 3
        consec_flag=True
        convert_to_mol(3,4)
    else:
        consec_flag=False
extend(parserrslt)
        # convert_to+m

    """
    if tokenized_sents==[]:
        tokenized_sents=[sent.text for sent in Paragraph(text).sentences]
    if precNERrslt == ['do_regex']:
        precNERrslt=[regex_search(Prec_Dict_regex_noaqueous, sent) for sent in tokenized_sents]
    else:
        assert len(tokenized_sents)==len(precNERrslt), print(tokenized_sents, precNERrslt) 

    output_manysents=[]
    sentidxx=-1
    for sent in tokenized_sents:
        sentidxx+=1

        consec_prevvol_numunt=(None,None)

        parserslt,rgxPREC, sent_PRECmasked = parse_prec_amounts_inner(sent,rgxrslt=precNERrslt[sentidxx],return_regexPREC=True)
        if debug:
            if sent!=sent_PRECmasked:
                print(rgxPREC)
            
        if len(parserslt)>0:
            for idx in range(len(parserslt)):
                thisprec=[unitclass(comp) for comp in list(parserslt[idx].items())[0][1] if unitclass(comp) is not None]
                if thisprec in [['concent_mol'],['concent_wt']]: 
        
                    if idx==0:
                        prevprec=[]
                    else:
                        prevprec=[unitclass(comp) for comp in list(parserslt[idx-1].items())[0][1] if unitclass(comp) is not None]

                    phrase_btwn = removecomps(sent_PRECmasked[rgxPREC[idx-1]['span'][1]:rgxPREC[idx]['span'][0]].split(" "),['','in','and','aqueous'])
                
                    if (prevprec in [['concent_mol','vol'],['concent_wt','vol'],['vol','concent_mol'],['vol','concent_wt']] or consec_prevvol_numunt!=(None,None)) and len(phrase_btwn)<=2:     #which contains

                        if consec_prevvol_numunt==(None,None):
                            prevvolnum = isnum(list(parserslt[idx-1].items())[0][1][prevprec.index('vol')*2])
                            prevvolunt = map_unit2scale(list(parserslt[idx-1].items())[0][1][prevprec.index('vol')*2+1],mode=mode)
                        else:
                            prevvolnum = consec_prevvol_numunt[0]
                            prevvolunt = consec_prevvol_numunt[1]    
                        consec_prevvol_numunt = (prevvolnum,prevvolunt)
                        
                        numhere = isnum(list(parserslt[idx].items())[0][1][0])
                        unthere = map_unit2scale(list(parserslt[idx].items())[0][1][1],mode=mode)
                        # print(numhere,unthere,prevvolnum,prevvolunt)
                        if numhere>0 and prevvolnum>0:
                            valhere = numhere * unthere #converted to M
                            valhere*= prevvolnum * prevvolunt # converted to mol
                            # print(valhere)
                            valtowrite=[str(valhere),'mol']
                            parserslt[idx]={list(parserslt[idx].items())[0][0]:valtowrite}
                    else:
                        consec_prevvol_numunt=(None,None)
            output_manysents.extend(parserslt)
    return output_manysents
def span_includes(small,large):
    """
    input: two tuples  span
    """
    if large[0]<=small[0] and small[1]<=large[1]:
        return True
    else:
        return False


def parse_amounts_fromphrase(prec_phrase,version="v2",standardizeunit=True,purityonly=False,debug=True):
    """
    input: phrase containing one PREC (regex search output)
    output: amounts info surrounding this PREC 

    """
    
    if version=="v2":
        units_priority = {'vol':0,'mole':1,'concent_mol':2,'concent_wt':3,'wt':4}
   
        numunts = [[prec_phrase['groups'][grp-1],clean_space(prec_phrase['groups'][grp])] for grp in [2,5,9,12] if prec_phrase['groups'][grp] is not None]

        if purityonly:
            numunts = [comp for comp in numunts if ispurity(comp)]
            if len(numunts)>0:
                if "%" in prec_phrase['groups'][9]:

                    if re.search(companynameonly_regex,prec_phrase['groups'][6].replace('PREC',"")) is not None:
                        company=re.search(companynameonly_regex,prec_phrase['groups'][6].replace('PREC',"")).group()
                    else:
                        company=None

                    
                    return {"1st_number":prec_phrase['groups'][8], "1st_unit":company, "2nd_number":None, "2nd_unit":None}
                else:
                    return {"1st_number":None, "1st_unit":None, "2nd_number":None, "2nd_unit":None}
            else:
                return {"1st_number":None, "1st_unit":None, "2nd_number":None, "2nd_unit":None}


        else:
            numunts = [comp for comp in numunts if not ispurity(comp)] # filter purities

        if len(numunts)>2 and ('final' in prec_phrase['groups'][6] or 'f.c.' in prec_phrase['groups'][6]): # Group 6 this is parentheses. Here then kill final concentration
            numunts=[[prec_phrase['groups'][grp-1],clean_space(prec_phrase['groups'][grp])] for grp in [2,5] if prec_phrase['groups'][grp] is not None]
            numunts = [comp for comp in numunts if not ispurity(comp)] # filter purities







        if len(numunts)==0: # no amount
            return {"1st_number":None, "1st_unit":None, "2nd_number":None, "2nd_unit":None}
        elif len(numunts)==1:
            return {"1st_number":numunts[0][0], "1st_unit":numunts[0][1], "2nd_number":None, "2nd_unit":None}
        elif len(numunts)==2:
            return {"1st_number":numunts[0][0], "1st_unit":numunts[0][1], "2nd_number":numunts[1][0], "2nd_unit":numunts[1][1]}
        elif len(numunts)==3: 
            if standardizeunit:
                numunts = standardize_unit(numunts)

            numunts = sorted(numunts, key=lambda d: units_priority[unitclass(d[-1])])

            if contains_sameelement([unitclass(comp[-1]) for comp in numunts])[0]: 
                samecheck=[]
                idxtokill=None
                for idx in contains_sameelement([unitclass(comp[-1]) for comp in numunts])[1]:
                    samecheck.append(numunts[idx])
                    idxtokill=idx
                if len(samecheck)==2 and samecheck[0]==samecheck[1]: 
                    numunts.pop(idxtokill)
                    assert len(numunts)==2, print(numunts)
                    # print(numunts)
                    return {"1st_number":numunts[0][0], "1st_unit":numunts[0][1], "2nd_number":numunts[1][0], "2nd_unit":numunts[1][1]}

                else:
                    print("Other types,same_unt_conflict: ", prec_phrase['text'])
                    return {"1st_number":None, "1st_unit":None, "2nd_number":None, "2nd_unit":None}
                    
            else:
                numunts=numunts[:2]
                # print(numunts)
                return {"1st_number":numunts[0][0], "1st_unit":numunts[0][1], "2nd_number":numunts[1][0], "2nd_unit":numunts[1][1]}

        elif len(numunts)==4:
            if debug:
                print("Other types,numunts==4: ", prec_phrase['text'])
                return {"1st_number":None, "1st_unit":None, "2nd_number":None, "2nd_unit":None}
        else:
            if debug:
                print("Other types,else: ", prec_phrase['text'])
                return {"1st_number":None, "1st_unit":None, "2nd_number":None, "2nd_unit":None}



    elif version=="v1":
        groups_binary = [0 if comp is None else 1 for comp in prec_phrase['groups']]

        if sum(groups_binary)==0: # no amount
            return {"1st_number":None, "1st_unit":None, "2nd_number":None, "2nd_unit":None}
        elif groups_binary==[1,1,1,1,1,1,0,0,0,0,0,0,0]:
            vol_num=prec_phrase['groups'][1]
            vol_unt=clean_space(prec_phrase['groups'][2])
            concent_num=prec_phrase['groups'][4]
            concent_unt=clean_space(prec_phrase['groups'][5])
        elif groups_binary==[1,1,1,0,0,0,1,1,1,1,0,0,0]:
            vol_num=prec_phrase['groups'][1]
            vol_unt=clean_space(prec_phrase['groups'][2])
            concent_num=prec_phrase['groups'][8]
            concent_unt=clean_space(prec_phrase['groups'][9])

        elif groups_binary==[1,1,1,0,0,0,0,0,0,0,0,0,0]:
            vol_num=prec_phrase['groups'][1]
            vol_unt=clean_space(prec_phrase['groups'][2])
            concent_num=None
            concent_unt=None
        elif groups_binary==[0,0,0,0,0,0,1,1,1,1,1,1,1]: 
            # Type 4: PREC (5 mL,0.1 M)"  -> group 7 (group 9,10,12,13)
            first_unt=clean_space(prec_phrase['groups'][9])
            second_unt=clean_space(prec_phrase['groups'][12])
            vol_num=prec_phrase['groups'][8]
            vol_unt=first_unt
            concent_num=prec_phrase['groups'][11]
            concent_unt=second_unt

        elif groups_binary==[0,0,0,0,0,0,1,1,1,1,0,0,0]: 
            
            first_unt=clean_space(prec_phrase['groups'][9])
            vol_num=prec_phrase['groups'][8]
            vol_unt=first_unt
            concent_num=None
            concent_unt=None

  
        elif groups_binary==[0,0,0,1,1,1,1,1,1,1,0,0,0]: # 30 mM PREC (1.5 mL)
            first_unt=clean_space(prec_phrase['groups'][5])
            second_unt=clean_space(prec_phrase['groups'][9])
            vol_num=prec_phrase['groups'][4]
            vol_unt=first_unt
            concent_num=prec_phrase['groups'][8]
            concent_unt=second_unt
 

        elif groups_binary==[0,0,0,1,1,1,0,0,0,0,0,0,0]: # 30 mM PREC
            first_unt=clean_space(prec_phrase['groups'][5])
            vol_num=prec_phrase['groups'][4]
            vol_unt=first_unt
            concent_num=None
            concent_unt=None

        else: #Other types not accounted for
            if debug:
                print("Other types: ", prec_phrase['text'])


            return {"1st_number":None, "1st_unit":None, "2nd_number":None, "2nd_unit":None}
        return {"1st_number":vol_num, "1st_unit":vol_unt, "2nd_number":concent_num, "2nd_unit":concent_unt}

def clean_space(text,mode='unit'):
    if mode=='unit':
        
        for char in spaces_global:
            text=text.replace(char," ")

        while len(text)>0:
            if text[0]==" ":
                text=text[1:]
            elif text[-1]==" ":
                text=text[:-1]
            else:
                break
    elif mode=='replace':
        for char in spaces_global_replace:
            text=text.replace(char," ")
        if len(text)==0:
            return ""       

    else:

        for char in spaces_global:
            text=text.replace(char,"")
        if mode=='GPT3num':
            if text[0]=='~': text=text[1:]
            if text[:3]=='10-': text='1✕'+text
    if len(text)==0:
        return 0
    else:
        return text
        
def ispurity(list1):
    threshold=99
    assert len(list1)==2
    if list1[1][-1]=="%":
        num=isnum(list1[0])
        if num>=94: 
            return True
        elif num>90:
            print("% with 90<num<=94:", num)
    return False

def unitclass(text):
    if text is None:
        return None
    output=map_unit2cat(text,errorreturn=None)
    if output is not None:
        return unitclass_differentmap[output]
    else:
        return None 


def map_unit2cat(unit,errorreturn='',mode='default'):
    if mode=='default':
        srch=regex_search(cat2unit_Dict_regex,unit)
    else:
        srch=regex_search(cat2unit_Dict_regex_afterLLM,unit)

    if len(srch)==1:
        return srch[0]['category']
    else:
        return errorreturn

def map_unit2scale(unit,mode='default'):
    if mode=='default':
        srch=regex_search(scale2unit_Dict_regex,unit)
    else:
        srch=regex_search(scale2unit_Dict_regex_afterLLM,unit)

    if len(srch)==1:
        return srch[0]['category']
    else:
        return ''


isunit_errors=[]
def isunit(unitornum,mode='default'):
    """
    input: string (supposed to be unit)
    output: return unit and if not unit return -1 
    """
    if map_unit2cat(unitornum,mode=mode)!='':
        return unitornum
    else:
        isunit_errors.append(unitornum)
        return -1
    
isnum_errors=[]
scientificx10_= [chx+'10'+ch_ for chx in multiplysigns_global for ch_ in hyphons_global]
def contains_scientific(text):
    for sci in scientificx10_:
        if text.count(sci)==1:
            return sci
        elif text.count(sci)>1: 
            return 0

def isnum(unitornum):
    """
    input: (string) num or unit or others e.g. 2.3, 34×10-3, we dont care about large numbers >1
    output: (float) numeric value >0, -1 if error
    """
    try:
        num=float(unitornum)
        return num
    except:
        num = clean_space(unitornum,mode='general')
        if isinstance(num,int): 
            return -1
        else:
            x10_ = contains_scientific(num)
            if isinstance(x10_,int): 

                isnum_errors.append(unitornum)
                return -1
            else:

                if num[-5:-1]==x10_ and num[:4]!=x10_: #Scientific numeric e.g. 34×10-3. Check it does not start nor end with x10
                    num=num.replace(x10_,'e-') #convect to float()-able form
                    try:
                        num=float(num)
                        return num
                    except:
                        return -1

def contains_HAuCl4amount(text,preconly=False,debug=False):
    rsltlist = parse_prec_amounts_regex(text)
    rsltlist = precnormalize_amount_grouponly(rsltlist) 
    if debug:
        print(rsltlist)
    if preconly:
        return (any(['HAuCl4' in comp['precursor_category'] for comp in rsltlist]))
    else:
        return any(['HAuCl4' in prec['precursor_category'] and len(prec['amount'])>0 for prec in rsltlist])

def mol_normalize_concent(category_amount,include_vol_inL=0,output_finalvol=False,mode='default'):
    """
    input e.g. [ {'precursor_category': 'HAuCl4', 'amount': [['68', 'μL', '0.5', 'M']]}, {'precursor_category': 'CTAB', 'amount': [['291.56', 'mg']]}  ]
    also, include_vol_inL=     is made for seed solution volume, or some other solution that should be counted into that relates to dilution of the concentrations.
    This only takes effect when flask_volume >0. if 0 discarded
    output - calculate mmols of each precursors and update the amount to one mmol value
    error - return 0 when some precursors are there but dont have amount info, or if there are many amounts for one precursor. (EXCEPT 'Other' precursor) 
    TODO!!  ADD possible units combinations when M/L info are parsed.
    # category_amount is actually subcategory. This is necessary due to different molar mass

    When amount is blank, look for others in same category and if that has amount replace it. if not, leave it BLANK we do forgive blank amount.
    When multiple amounts for one prec category, returns "error_multiple" string for the amount of that category. if it is solvent, we allow multiple volumes
    When strange amount (unallowed units) returns "error_unallowed" string
    When blank amount for a prec category, returns "ND" string for the amount of that category.
    example input:
    [{'amount': [], 'precursor_category': 'AuCl3'},
    {'amount': [['200', 'μL', '100', 'mM']], 'precursor_category': 'AA'},
    {'amount': [['2', 'mL', '1', 'mM']], 'precursor_category': 'AgNO3'},
    {'amount': [['85', 'μL', '40', 'mM']], 'precursor_category': 'HAuCl4'},
    {'amount': [['2.695', 'mL']], 'precursor_category': 'H2O'},
    {'amount': [['30', 'μL', '1', 'mM'], ['85', 'μL', '50', 'mM']], 'precursor_category': 'NaBH4'},
    {'amount': [['5', 'M', '0.4', 'M']], 'precursor_category': 'CTAB'},
    {'amount': [], 'precursor_category': 'PVP'}]
    example output: (in M/mM)
    [('Other' is ignored too)
    {'amount': "solvent", 'precursor_category': 'H2O'}, # can be error_unallowed if other than volume only
    {'amount': 2, 'precursor_category': 'AA'},
    {'amount': 3, 'precursor_category': 'AgNO3'},
    {'amount': 4.1, 'precursor_category': 'HAuCl4'},
    {'amount': "error_multiple", 'precursor_category': 'NaBH4'},
    {'amount': "error_unallowed", 'precursor_category': 'CTAB'},
    {'amount': "ND", 'precursor_category': 'PVP'}]

    error:
    returns 0 if input is {'precursor_category':'Other','amount':[]}
    returns 0 if everything is error or ND
    

    """

    if isinstance(category_amount,int):
        print("input for mol_concent_normalize (category_amount) error",category_amount)
        if output_finalvol:
            return 0, 0
        else:
            return 0

    if mode!='default': 
        if 'Other' in [comp['precursor_category'] for comp in category_amount]:
            if output_finalvol:
                return 0, 0
            else:
                return 0#1

    if len(category_amount)==1 and category_amount[0]['precursor_category']=='Other': 
        if output_finalvol:
            return 0, 0
        else:
            return 0#1

    cat_subcat_amount={}
    for subcat_amount in category_amount:
        if subcat_amount['precursor_category']!='Other':
            cat = map_precsubcat2cat[subcat_amount['precursor_category']]
            if cat in cat_subcat_amount.keys():
                cat_subcat_amount[cat].append(subcat_amount)
            else:
                cat_subcat_amount[cat]=[subcat_amount]
    for cat in cat_subcat_amount:
        amounts_cat = [amount for subcat in cat_subcat_amount[cat] for amount in subcat['amount']]
        if len(amounts_cat)==0: #all blank category
            for subcat in cat_subcat_amount[cat]: subcat['amount']="ND"
        elif len(amounts_cat)>1: #multiple
            if cat not in realsolventlist:

                for subcat in cat_subcat_amount[cat]: subcat['amount']="error_multiple"
            else: # this is solvent, make sure there is one subcat, if not print error
                if len(cat_subcat_amount[cat])!=1:
                    print("more than two subcategories of solvents", cat_subcat_amount[cat])
                    if output_finalvol:
                        return 0, 0
                    else:
                        return 0#2
        else: # we have 1 amount so filter blank amount
            temp_removeidx=[]
            for idx in range(len(cat_subcat_amount[cat])):
                if cat_subcat_amount[cat][idx]['amount']==[]:
                    temp_removeidx.append(idx)
            for idx in reversed(temp_removeidx): cat_subcat_amount[cat].pop(idx)
    new_cats_amount = [ {'precursor_category':cat, 'precsubcat':cat_subcat_amount[cat][0]['precursor_category'],'amount':cat_subcat_amount[cat][0]['amount']} for cat in cat_subcat_amount]
    category_amount=new_cats_amount[:] # this is real category, not subcat anymore <- nope. updated due to parsefrom_amountlist mass->mol conversion error


    if len(category_amount)==0:
        if output_finalvol:
            return 0, 0
        else:
            return 0#3

    flask_volume=float(0)
    for prec in category_amount: 
        # searchprec.remove(prec['precursor_category'])
        if prec['precursor_category']!='Other' and isinstance(prec['amount'],list): # recall no 'Other' anyways.

            if prec['precursor_category'] in realsolventlist:

                indic, precvolume = parsefrom_amountlist(prec,solvent=True,mode=mode)
                if indic<0:#error
                    prec['amount']="error_notallowed_"+str(indic)
                else:
                    prec['amount']="solvent"
                # skip solvent in amounts
            else:
                assert len(prec['amount'])==1

                precamount, precvolume = parsefrom_amountlist(prec,mode=mode) # string((# of moles)) + " mol" if mol and float(concentration in M) only if concent
                if isinstance(precamount,int) and precamount<0:#error
                    prec['amount']="error_notallowed_"+str(precamount)
                else:
                    prec['amount']=precamount
            flask_volume+=precvolume
            prec.pop('precsubcat')


    if flask_volume==0:
        if all([isinstance(comp['amount'],float) for comp in category_amount]):
            print("zero volume: ", category_amount)

            if output_finalvol:
                return category_amount, 0
            else:
                return category_amount
        else:

            if output_finalvol:
                return 0, 0
            else:
                return category_amount # fixed from 4 to returning itself to featurize binary for only volume detected cases


    for prec in category_amount:
        if isinstance(prec['amount'],str) and len(prec['amount'])>4 and prec['amount'][-4:]==" mol":
                prec['amount'] = float(prec['amount'][:-4])/(flask_volume+include_vol_inL)
                        
    if output_finalvol:
        return category_amount, flask_volume+include_vol_inL
    else:
        return category_amount

def precnormalize_amount_grouponly(precslist,log10=False,normalize=True,contain_solvent=False,normalize_multipleamounts=True,mode='default'): #normalize and reduce (set)
    """
    input: list of dict{precs&amount} in a paragraph e.g. [{'Hexadecyltrimethyl ammonium bromide': ['291.56', 'mg']}, {'CTAB': []}, {'HAuCl4': ['68', 'μL', '0.5', 'M']}, {'CTAB': []}]
    output: mol_normalize(   [ {'precursor_category': 'HAuCl4', 'amount': [['68', 'μL', '0.5', 'M']]}, {'precursor_category': 'CTAB', 'amount': [['291.56', 'mg']]}  ]    )
    dependency: Prec_Dict
    Error: return 0 when multiple category is detected in one prec
    Or Error from mol_normalize()
    """
    if mode=='default':
        if contain_solvent:
            Dict_map=Prec_Dict_regex
        else:
            Dict_map=Prec_Dict_regex_nosolvent
    elif mode=='afterLLMaddition':
        if contain_solvent:
            Dict_map=Prec_Dict_regex_afterLLM
        else:
            Dict_map=Prec_Dict_regex_nosolvent_afterLLM     
    category_amount=[]
    for item in precslist:
        prec = list(item.items())[0][0]
        amount= list(item.items())[0][1]

        multicount = [comp['category'] for comp in regex_search(Dict_map,prec)]
        if len(multicount)==0: #other
            category_amount.append({'precursor_category':'Other','amount':[]})
        elif len(multicount)==1:
            category_amount.append({'precursor_category':multicount[0],'amount':amount})
        else: 
            return 0      
    # Group same precursors.
    precursor_categories = list(set([item['precursor_category'] for item in category_amount]))
    grouped_category_amount = [ {'precursor_category':cat,'amount':[]} for cat in precursor_categories]
    [ prec['amount'].append(item['amount']) for item in category_amount for prec in grouped_category_amount if item['precursor_category']==prec['precursor_category'] and item['amount']!=[] ]

    if normalize_multipleamounts:
        for prec in grouped_category_amount:
            if prec['precursor_category'] not in realsolventlist and len(prec['amount'])>1:
                # we minimize multiple. check if an amountlist is a subset of the aother amountlist.
                # e.g.1.[20ml,1M], [1M] -> [20ml,1M]  e.g.2. [20ml,1M], [20ml,1M] -> [20ml,1M]
                sortedprecamount=sorted(prec['amount'], key=len)
                if all([True if all([True if numunit in sortedprecamount[-1] else False for numunit in amount]) else False for amount in sortedprecamount[:-1]]):
                    prec['amount']=[sortedprecamount[-1]]

    return grouped_category_amount

def precnormalize_amount(precslist,include_vol_inL=0,log10=False,version="Concentration",mode='default',output_finalvol=False): #normalize and reduce (set)
    """
    input: list of dict{precs&amount} in a paragraph e.g. [{'Hexadecyltrimethyl ammonium bromide': ['291.56', 'mg']}, {'CTAB': []}, {'HAuCl4': ['68', 'μL', '0.5', 'M']}, {'CTAB': []}]
    output: mol_normalize(   [ {'precursor_category': 'HAuCl4', 'amount': [['68', 'μL', '0.5', 'M']]}, {'precursor_category': 'CTAB', 'amount': [['291.56', 'mg']]}  ]    )
    dependency: Prec_Dict
    Error: return 0 when multiple category is detected in one prec
    Or Error from mol_normalize()
    """

    if version=="SoluteMoleFraction":
        grouped_category_amount=precnormalize_amount_grouponly(precslist,contain_solvent=False,mode=mode)
        return mol_normalize(grouped_category_amount,log10=log10,normalize=normalize,mode=mode)
    elif version=="Concentration":
        grouped_category_amount=precnormalize_amount_grouponly(precslist,contain_solvent=True,mode=mode)
        return mol_normalize_concent(grouped_category_amount,include_vol_inL=include_vol_inL,output_finalvol=output_finalvol,mode=mode)

breakstrings=[" re-dispers"," redispers"," centrifug" ," stored",' incubate',' washed' ]
def check_stringsinsent(strings,sent):
    for string in strings:
        if string in sent:
            return True
    return False


def unit2mmol(units,molarmass,millimol=True,output_vol=False,mode='default'):
    """
    input: (ordered) units in ONE amount e.g. ['ml','M'], ['mmol','ml']
           (float) molar mass of a precursor
    output: 1. (list of int) indicator telling you what idxs to multiply e.g. [0,1], [0]
            2. (int) scaling from unit conversion to mmol e.g. 100
            returns multiply_idxlist, scaling if output_vol False
            returns multiply_idxlist (note this is BOOLEAN list!! of use or not to use in in numbers_inamount), scaling, volumenum_idx (just int index in numbers_inamount), volumescale2liter if output_vol True

    error: returns [],0 when len(units)>3 or len(units)==0:
            returns [],-1 when error occured when dividing by molar mass
            returns [],-2 when error - not allowed units combination
            
            returns 4 outputs last two being volume number idx, scaling for volume:    
                returns multiply_idxlist, scaling, -1, -1 if no volume info nor concentration info, like weight only
                returns [0], scaling, -8, -8 and last two indicate this is concentration-only
                returns [],-8, 0, volumescaling if volume-only
                returns [], 0,-1,-1 if error len(units)>3 or len(units)==0: 
                returns [],-1,-1,-1 if error dividing molar mass
                returns [],-2,-1,-1 if not allowed units comb
    """

    if len(units)>3 or len(units)==0:
        if output_vol:
            return [],0,-1,-1
        else:
            return [],0
    
    units_categories=[map_unit2cat(comp,mode=mode) for comp in units]
    if units_categories in allowed_combination_useall:
        multiply_idxlist=[1 for comp in units_categories]
    elif units_categories in allowed_combination_useone:
        multiply_idxlist=[0 if comp=='vol' else 1 for comp in units_categories]

    # "Concentration-only" will be allowed
    elif units_categories in [['concent'], ['wtpervol'], ['wtperwt']]:
        if output_vol:
            scaling = map_unit2scale(units[0],mode=mode)
            if units_categories==['concent']:
                pass
            else: # 'wt'
                try:
                    scaling /= molarmass
                except:
                    if output_vol:
                        return [],-1,-1,-1
                    else:
                        return [],-1
            # now is M
            if millimol:
                scaling*=1000
            return [0], scaling, -8, -8 
        else:
            return [],-2
    elif units_categories==['vol'] and output_vol: #allow 
            volumescale2liter = map_unit2scale(units[0],mode=mode)
            return [],-8, 0, volumescale2liter
    elif output_vol:
        return [],-2,-1,-1
    else: #not allowed
        return [],-2 # was [],0
    units_scaling = [map_unit2scale(units[idx],mode=mode) if multiply_idxlist[idx]==1 else 1 for idx in range(len(units))]
    scaling=1
    for comp in units_scaling:
        scaling *= comp
    if millimol:
        scaling *= 1000 #mol to mmol

    if ('wt' in units_categories) or ('wtpervol' in units_categories) or ('wtperwt' in units_categories):
        try:
            scaling /= molarmass
        except:
            if output_vol:
                return [],-1,-1,-1
            else:
                return [],-1

    if output_vol:
        if 'vol' in units_categories:
            unitcatvolidx = units_categories.index('vol') 
            volumescale2liter = map_unit2scale(units[unitcatvolidx],mode=mode)
            return multiply_idxlist, scaling, unitcatvolidx, volumescale2liter
        elif 'wt' in units_categories and len(units_categories)>1:
            unitcatwtidx = units_categories.index('wt')
            volumescale2liter = map_unit2scale(units[unitcatwtidx],mode=mode)*0.001
            return multiply_idxlist, scaling, unitcatwtidx, volumescale2liter
        else: # no volume info here
            return multiply_idxlist, scaling, -1, -1
        
    else:
        assert len(multiply_idxlist)>0 and scaling>0, print("unit2mmol strange")
        return multiply_idxlist, scaling


def parsefrom_amountlist(prec, solvent=False, mode='default'):
    """
    input: (dict) prec
            ex1. {'precursor_category': 'HAuCl4', 'amount': [['68', 'μL', '0.5', 'M']]} # one amount
            ex2. {'precursor_category': 'H2O', 'amount': [['68', 'μL'],['668', 'μL']]}
            ex3. {'precursor_category': 'H2O', 'amount': []}
    output: 
            if solvent,
                 1, (float) volume of the solution
                (negative integer), 0 if error
            else:
                (string) "(number of moles) mol", (float) volume of the solution
                (float) concentration in M, 0 if concentration-only
                (negative integer), 0 if error
    """

    volumetrackingforloop_justforsolvent = 0
    for amount in prec['amount']: # only case there are many is solvent when it has multiple volume-only amounts
        if len(amount)%2==1:
    
            return -1,0
        else:
            size=int(len(amount)/2)
            numbers_inamount=[isnum(amount[i*2]) for i in range(size)]
            if -1 in numbers_inamount: 

                return -2,0
            units_inamount=[isunit(amount[i*2+1],mode=mode) for i in range(size)]
            if -1 in units_inamount:

                return -3,0
            multiply_idxlist, scaling, volumenum_idx, volumescale2liter = unit2mmol(units_inamount,molarmass=prec_molarmass[prec['precsubcat']],millimol=False,output_vol=True,mode=mode) 
            if solvent:
                if scaling==-8: 
                    precvolume = numbers_inamount[0] * volumescale2liter
                    volumetrackingforloop_justforsolvent+=precvolume

                else: # error from unit2mmol
                    return -4,0
    if solvent:

        return 1, volumetrackingforloop_justforsolvent
    else: #not solvent, asserted that we have one amount.
        if scaling <= 0: # error from unit2mmol
            return -5,0
        else:
            if volumescale2liter==-8: #concentration-only
                prec_concent = numbers_inamount[0] * scaling
                return prec_concent, 0
            else:
                prec_mol=1
                for j in range(len(numbers_inamount)):
                    if multiply_idxlist[j]==1:
                        prec_mol*=numbers_inamount[j]
                prec_mol*= scaling

                if volumescale2liter==-1: # mol only
                    return str(prec_mol)+" mol", 0
                else:
                    return str(prec_mol)+" mol", numbers_inamount[volumenum_idx] * volumescale2liter
       