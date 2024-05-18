import re


all_elements_list=['H', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Pd', 'Ag', 'Au','Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Cs', 'Ba', 'Ce', 'Pt', 'Pb', '[gG]old','[cC]arbon','[aA]luminum','[sS]ilicon', '[pP]alladium', '[sS]ilver', '[cC]opper', '[pP]latinum', '[cC]arbide', '[nN]itride', '[oO]xide', '[fF]luoride', '[sS]ulfide', '[cC]hloride', '[aA]rsenide', '[sS]elenide', '[bB]romide', '[aA]ntimonide', '[tT]elluride', '[iI]odide','[gG]raphene']
startstr=r'(?:(?<=^)|(?<=[     \s@\/\(,;:\[\-‐−–]))'
anyspace=r'[     \s]'
anydash=r'[\-‐−–]'
nocapping=r'(?![\s\-‐−–](?:stabilized|capped|protected))'
desc_capping_optional=r'(?:\w*[\s\-‐−–](?:stabilized|capped|protected) )?'

nano=r'(?:[nN]ano[\-‐−–]?)'
endwith_nochar=r'(?:(?=[^\w])|(?=$))'
nolikeshape=r'(?![\-‐−–]?(?:like| ?shaped?))'

all_elements="(?:"
for elem in all_elements_list: all_elements+=elem+'|' 
all_elements= all_elements[:-1]+')'#?'
matformula='(?:'+all_elements+r'[ \d]?'+')+'+r'\)?' # silver (Ag) nanorods


morphdicts={}
targets_split_dict={}
strictelementNP={}

for target1 in ['Au']:

    if target1=='Au':
        element='(Au|[gG]old)'
        element_tight='(Au|G)'

    
    targets_split = element_tight[1:-1].split("|")+element[1:-1].split("|")
    targets_split_dict[target1] = targets_split[:-1]+[targets_split[-1][1]+targets_split[-1][4:],targets_split[-1][2]+targets_split[-1][4:]]


    strictAuNP = r'('+element+anyspace+r'|'+element_tight+r')'+r'(?:N[pPC])s?(?![\-‐−– ]core)'
    strictAunanop = element+anyspace + nano+r'(?:[pP]article|[sS]tructure|[cC]rystal|[cC]luster)s?(?![\-‐−– ]core)' #strict on nano
    flexiblenanoplate = r'(?:'+element+anyspace+r')?' + nano+r'[pP]lates?(?![\-‐−– ]core)' #nano strict
    strictelementNP[target1]=strictAuNP+'|'+strictAunanop

    morphdicts[target1]={
            'Rd':[
            startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'NRs?'+ endwith_nochar,
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'[rR]ods?'+ nolikeshape + endwith_nochar,     #gold rods are allowed by ? after nano however caution for gold wires
            startstr + '(?:'+'[rR]od[\-‐−–]?(?:like| ?shaped?)'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'[rR]od[\-‐−–]?(?:like| ?shaped?)'+')'+ endwith_nochar, #"AuNPs synthesized in this work were spherical in shape"
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+nano+'?'+'[rR]ods?'+')'+ endwith_nochar, 
            ],
            'Sph':[ #not catch NS
            # startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'NS[A-Z]*s?'+ endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'[sS]pher(?:e|oid)s?'+ nolikeshape + endwith_nochar,     #nano enforce
            startstr + '(?:'+'[sS]pher(?:e|oid)[\-‐−–]?(?:like| ?shaped?)'+'|[sS]pher(?:ical|oidal)'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'[sS]pher(?:e|oid)[\-‐−–]?(?:like| ?shaped?)'+'|[sS]pher(?:ical|oidal)'+')'+ endwith_nochar, #"AuNPs synthesized in this work were spherical in shape"
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+nano+'?'+'[sS]pher(?:e|oid)s?'+')'+ endwith_nochar,
            ],
            'Cb':[ #not catch NC
            # startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'NC[A-Z]*s?'+ endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:[cC]ub(?:e|oid)s?|[hH]exahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,     #nano enforce
            startstr + '(?:'+'(?:[cC]ub(?:e|oid)s?|[hH]exahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[cC]ub(?:ical|ic|oidal)|[hH]exahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'(?:[cC]ub(?:e|oid)s?|[hH]exahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[cC]ub(?:ical|ic|oidal)|[hH]exahedral'+')'+ endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+nano+'?'+'(?:[cC]ub(?:e|oid)s?|[hH]exahedr(?:ons?|a))'+')'+ endwith_nochar,
            ],
            'Ohd':[ # no acronym
            # startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'NO[A-Z]*s?'+ endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[oO]ctahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,     #gold rods are allowed by ? after nano however caution for gold wires
            startstr + '(?:'+'(?:[oO]ctahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[oO]ctahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[oO]ctahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[oO]ctahedral'+ ')'+ endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:[oO]ctahedr(?:ons?|a))'+ ')'+ endwith_nochar, 
            ],
            'triOhd':[ # no acronym
            # startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'NO[A-Z]*s?'+ endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:(?:(?:[tT]rigonal )?[tT]ris[\-‐−–]?|[tT]riakis[\-‐−– ]?)[oO]ctahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,
            startstr + '(?:'+'(?:(?:(?:[tT]rigonal )?[tT]ris[\-‐−–]?|[tT]riakis[\-‐−– ]?)[oO]ctahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[tT]risoctahedral'+'|[tT]riakis[\-‐−– ]?octaheral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:(?:(?:[tT]rigonal )?[tT]ris[\-‐−–]?|[tT]riakis[\-‐−– ]?)[oO]ctahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[tT]risoctaheral'+'|[tT]riakis[\-‐−– ]?octaheral'+ ')'+ endwith_nochar, 
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:(?:(?:[tT]rigonal )?[tT]ris[\-‐−–]?|[tT]riakis[\-‐−– ]?)[oO]ctahedr(?:ons?|a))'+ ')'+ endwith_nochar,
            ],
            'Ico':[ # no acronym
            # startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'NI[A-Z]*s?'+ endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[iI]cosahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,     #gold rods are allowed by ? after nano however caution for gold wires
            startstr + '(?:'+'(?:[iI]cosahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[iI]cosahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[iI]cosahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[iI]cosahedral'+ ')'+ endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:[iI]cosahedr(?:ons?|a))'+ ')'+ endwith_nochar, 
            ],
            'DoDeca':[ # no acronym
            # startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'ND[A-Z]*s?'+ endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[dD]odecahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,     #gold rods are allowed by ? after nano however caution for gold wires
            startstr + '(?:'+'(?:[dD]odecahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[dD]odecahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[dD]odecahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[dD]odecahedral'+ ')'+ endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:[dD]odecahedr(?:ons?|a))'+ ')'+ endwith_nochar, 
            ],
            'Thd':[ # no acronym
            # startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'NO[A-Z]*s?'+ endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+'(?:[tT]ri(?:gonal|angle|angular)[\-‐−– ])?'+nano+'?'+'(?:[tT]etrahedr(?:ons?|a)|[pP]yramids?)'+ nolikeshape + endwith_nochar,  #triangular nanopyramid
            startstr + '(?:'+'(?:[tT]etrahedr(?:ons?|a)|(?:[tT]ri(?:gonal|angle|angular)[\-‐−– ])?[pP]yramids?)[\-‐−–]?(?:like| ?shaped?)'+'|[tT]etrahedral|(?:[tT]ri(?:gonal|angle|angular)[\-‐−– ])?[pP]yramidal'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[tT]etrahedr(?:ons?|a)|(?:[tT]ri(?:gonal|angle|angular)[\-‐−– ])?[pP]yramids?)[\-‐−–]?(?:like| ?shaped?)'+'|[tT]etrahedral|(?:[tT]ri(?:gonal|angle|angular)[\-‐−– ])?[pP]yramidal' +')'+ endwith_nochar, 
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:[tT]etrahedr(?:ons?|a)|[pP]yramids?)'+')'+ endwith_nochar, 
            
            ],
            'Deca':[ # no acronym
            # startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'NO[A-Z]*s?'+ endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[dD]ecahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,     #gold rods are allowed by ? after nano however caution for gold wires
            startstr + '(?:'+'(?:[dD]ecahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[dD]ecahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[dD]ecahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[dD]ecahedral'+ ')'+ endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:[dD]ecahedr(?:ons?|a))'+ ')'+ endwith_nochar,  
            ],
            'Cohd':[ # no acronym
            # startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'NO[A-Z]*s?'+ endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[cC]uboctahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,     #gold rods are allowed by ? after nano however caution for gold wires
            startstr + '(?:'+'(?:[cC]uboctahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[cC]uboctahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[cC]uboctahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[cC]uboctahedral'+ ')'+ endwith_nochar, 
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:[cC]uboctahedr(?:ons?|a))'+ ')'+ endwith_nochar, 
            ],

            #Truncated variations - AuNPs were nouns were omitted here
                #     truncated tetrahedra
                #     truncated cube # 14 regular faces (6 octagonal and 8 triangular), 36 edges, and 24 vertices.
                #     truncated octahedra #==bitruncated cube #14 faces (8 regular hexagonal and 6 square), 36 edges, and 24 vertices
                #     truncated icosahedra #12 regular pentagonal faces, 20 regular hexagonal faces, 60 vertices and 90 edges.
                #     truncated dodecahedra #12 regular decagonal faces, 20 regular triangular faces, 60 vertices and 90 edges.
            'tCb':[
            startstr + '[tT]runcated '+'(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[cC]ub(?:e|oid)s?|[hH]exahedr(?:ons?|a))'+ nolikeshape + endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+'[tT]runcated '+nano+'?'+'(?:[cC]ub(?:e|oid)s?|[hH]exahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,      
            startstr + '[tT]runcated '+'(?:'+'(?:[cC]ub(?:e|oid)s?|[hH]exahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[cC]ub(?:ical|ic|oidal)|[hH]exahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'[tT]runcated '+'(?:'+'(?:[cC]ub(?:e|oid)s?|[hH]exahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[cC]ub(?:ical|ic|oidal)|[hH]exahedral'+')'+ endwith_nochar,
            ],
            'tOhd':[
            startstr + '[tT]runcated '+'(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[oO]ctahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,
            startstr + '(?:('+element+'|'+matformula+') )?'+'[tT]runcated '+nano+'?'+'(?:[oO]ctahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,
            startstr + '[tT]runcated '+'(?:'+'(?:[oO]ctahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[oO]ctahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'[tT]runcated '+'(?:'+'(?:[oO]ctahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[oO]ctahedral'+ ')'+ endwith_nochar, 
            ],
            'tIco':[ 
            startstr + '[tT]runcated '+'(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[iI]cosahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,
            startstr + '(?:('+element+'|'+matformula+') )?'+'[tT]runcated '+nano+'?'+'(?:[iI]cosahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,     #gold rods are allowed by ? after nano however caution for gold wires
            startstr + '[tT]runcated '+'(?:'+'(?:[iI]cosahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[iI]cosahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'[tT]runcated '+'(?:'+'(?:[iI]cosahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[iI]cosahedral'+ ')'+ endwith_nochar, 
            ],
            'tDoDeca':[ 
            startstr + '[tT]runcated '+'(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[dD]odecahedr(?:ons?|a))'+ nolikeshape + endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+'[tT]runcated '+nano+'?'+'(?:[dD]odecahedr(?:ons?|a))'+ nolikeshape + endwith_nochar, 
            startstr + '[tT]runcated '+'(?:'+'(?:[dD]odecahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[dD]odecahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'[tT]runcated '+'(?:'+'(?:[dD]odecahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[dD]odecahedral'+ ')'+ endwith_nochar, 
            ],
            'tThd':[
            startstr + '[tT]runcated '+'(?:('+element+'|'+matformula+') )?'+'(?:[tT]ri(?:gonal|angle|angular)[\-‐−– ])?'+nano+'?'+'(?:[tT]etrahedr(?:ons?|a)|[pP]yramids?)'+ nolikeshape + endwith_nochar, 
            startstr + '(?:('+element+'|'+matformula+') )?'+'[tT]runcated '+'(?:[tT]ri(?:gonal|angle|angular)[\-‐−– ])?'+nano+'?'+'(?:[tT]etrahedr(?:ons?|a)|[pP]yramids?)'+ nolikeshape + endwith_nochar, 
            startstr + '[tT]runcated '+'(?:'+'(?:[tT]etrahedr(?:ons?|a)|(?:[tT]ri(?:gonal|angle|angular)[\-‐−– ])?[pP]yramids?)[\-‐−–]?(?:like| ?shaped?)'+'|[tT]etrahedral|(?:[tT]ri(?:gonal|angle|angular)[\-‐−– ])?[pP]yramidal'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '[tT]runcated '+'(?:'+'(?:[tT]etrahedr(?:ons?|a)|(?:[tT]ri(?:gonal|angle|angular)[\-‐−– ])?[pP]yramids?)[\-‐−–]?(?:like| ?shaped?)'+'|[tT]etrahedral|(?:[tT]ri(?:gonal|angle|angular)[\-‐−– ])?[pP]yramidal' +')'+ endwith_nochar, 
            ],
            'tDeca':[ 
            startstr + '[tT]runcated '+'(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[dD]ecahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,    
            startstr + '(?:('+element+'|'+matformula+') )?'+'[tT]runcated '+nano+'?'+'(?:[dD]ecahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,    
            startstr + '[tT]runcated '+'(?:'+'(?:[dD]ecahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[dD]ecahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '[tT]runcated '+'(?:'+'(?:[dD]ecahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[dD]ecahedral'+ ')'+ endwith_nochar, 
            ],
            'tCohd':[ 
            startstr + '[tT]runcated '+'(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[cC]uboctahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,
            startstr + '(?:('+element+'|'+matformula+') )?'+'[tT]runcated '+nano+'?'+'(?:[cC]uboctahedr(?:ons?|a))'+ nolikeshape + endwith_nochar,
            startstr + '[tT]runcated '+'(?:'+'(?:[cC]uboctahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[cC]uboctahedral'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '[tT]runcated '+'(?:'+'(?:[cC]uboctahedr(?:ons?|a))[\-‐−–]?(?:like| ?shaped?)'+'|[cC]uboctahedral'+ ')'+ endwith_nochar, 
            ],

            #2D plate-like shapes - triangle, pentagon , hexagon, octagon - also counts triangular nanoplate
            'Pl':[
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:[pP]lates?)'+ nolikeshape + endwith_nochar,    # nano strict on nanoplate
            startstr + '(?:'+'(?:[pP]late)[\-‐−–]?(?:like| ?shaped?)'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[pP]late)[\-‐−–]?(?:like| ?shaped?)'+ ')'+ endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:[pP]lates?)'+ ')'+ endwith_nochar, 
            ],

            'Tri':[ #NT can be Tube
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[tT]riangles?)'+ nolikeshape + endwith_nochar, 
            startstr + '(?:'+'(?:[tT]riangles?)[\-‐−–]?(?:like| ?shaped?)'+'|[tT]riangular|[tT]rigonal'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[tT]riangles?)[\-‐−–]?(?:like| ?shaped?)'+'|[tT]riangular|[tT]rigonal'+ ')'+ endwith_nochar, 
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:[tT]riangles?)'+ ')'+ endwith_nochar, 
            
            ],
            'Pentag':[
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[pP]entagons?)'+ nolikeshape + endwith_nochar,    
            startstr + '(?:'+'(?:[pP]entagons?)[\-‐−–]?(?:like| ?shaped?)'+'|[pP]entagonal'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[pP]entagons?)[\-‐−–]?(?:like| ?shaped?)'+'|[pP]entagonal'+ ')'+ endwith_nochar, 
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:[pP]entagons?)'+')'+ endwith_nochar, 
            ],
            'Hexag':[
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[hH]exagons?)'+ nolikeshape + endwith_nochar,    
            startstr + '(?:'+'(?:[hH]exagons?)[\-‐−–]?(?:like| ?shaped?)'+'|[hH]exagonal'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[hH]exagons?)[\-‐−–]?(?:like| ?shaped?)'+'|[hH]exagonal'+ ')'+ endwith_nochar, 
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:[hH]exagons?)'+ ')'+ endwith_nochar, 
            
            ],
            'Octag':[
            startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[oO]ctagons?)'+ nolikeshape + endwith_nochar,    
            startstr + '(?:'+'(?:[oO]ctagons?)[\-‐−–]?(?:like| ?shaped?)'+'|[oO]ctagonal'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')' + endwith_nochar,
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[oO]ctagons?)[\-‐−–]?(?:like| ?shaped?)'+'|[oO]ctagonal'+ ')'+ endwith_nochar, 
            startstr + '(?:'+strictAuNP+'|'+strictAunanop+'|'+flexiblenanoplate+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+nano+'?'+'(?:[oO]ctagons?)'+ ')'+ endwith_nochar, 
            ],

            #Spiky stuff
            'Str':[ #not catch NS
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:[sS]tars?)'+ nolikeshape + endwith_nochar,     #actual stars came up so enforce nanostar 
                startstr + '(?:'+'(?:[sS]tars?)[\-‐−–]?(?:like| ?shaped?)'+'|[sS]tarry|[sS]tellular'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'(?:[sS]tars?)[\-‐−–]?(?:like| ?shaped?)'+'|[sS]tar(?:ry)'+')'+ endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+nano+'?'+'(?:[sS]tars?)'+')'+ endwith_nochar,
            ],
            'Flw': [
                startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'NFs?'+ endwith_nochar, # acronym yes
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[fF]lowers?)'+ nolikeshape + endwith_nochar,    
                startstr + '(?:'+'(?:[fF]lowers?)[\-‐−–]?(?:like| ?shaped?)'+'|[fF]lowery'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'(?:[fF]lowers?)[\-‐−–]?(?:like| ?shaped?)'+'|[fF]lowery'+')'+ endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+nano+'?'+'(?:[fF]lowers?)'+')'+ endwith_nochar,
            
            ],
            
            #long stuff
            'Tub':[ 
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:[tT]ubes?)'+ nolikeshape + endwith_nochar,    #nano strict on tubes
                startstr + '(?:'+'(?:[tT]ubes?)[\-‐−–]?(?:like| ?shaped?)'+'|[tT]ubular'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'(?:[tT]ubes?)[\-‐−–]?(?:like| ?shaped?)'+'|[tT]ubular'+')'+ endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+nano+'?'+'(?:[tT]ubes?)'+ ')'+ endwith_nochar,
            
            ],
            'Wr':[ 
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:[wW]ires?)'+ nolikeshape + endwith_nochar,    # nano strict on nanowire
                startstr + '(?:'+'(?:[wW]ires?)[\-‐−–]?(?:like| ?shaped?)'+'|[wW]iry'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'(?:[wW]ires?)[\-‐−–]?(?:like| ?shaped?)'+'|[wW]iry'+')'+ endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+nano+'?'+'(?:[wW]ires?)'+ ')'+ endwith_nochar,
            
            ],
            'BiPym':[
                startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'N?B[pP]s?'+ endwith_nochar,
                startstr + '(?:('+element+'|'+matformula+') )?'+'(?:[a-z]+gonal )?'+nano+'?'+'(?:[bB]i[\-‐−–]?[pP]yramids?)'+ nolikeshape + endwith_nochar,    # probably pentagonal not trigonal. also has gold pentagonal bipyramid
                startstr + '(?:'+'(?:[bB]i[\-‐−–]?[pP]yramids?)[\-‐−–]?(?:like| ?shaped?)'+'|[bB]i[\-‐−–]?[pP]yramidal'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'(?:[bB]i[\-‐−–]?[pP]yramids?)[\-‐−–]?(?:like| ?shaped?)'+'|[bB]i[\-‐−–]?[pP]yramidal'+')'+ endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+nano+'?'+'(?:[bB]i[\-‐−–]?[pP]yramids?)'+')'+ endwith_nochar,
            ],



            #skipping aunps were NOUN forms for below
            'Fib':[ 
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:[fF]ib(?:er|re|ril)s?)'+ nolikeshape + endwith_nochar,    # enforce nano
                startstr + '(?:'+'(?:[fF]ib(?:er|re|ril)s?)(?:like| ?shaped?)'+'|[fF]ibrous'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'(?:[fF]ib(?:er|re|ril)s?)(?:like| ?shaped?)'+'|[fF]ibrous'+')'+ endwith_nochar,
            ],
            'Psm':[ 
                startstr + '(?:('+element+'|'+matformula+') )?'+'(?:[a-z]*al )?'+nano+'?'+'(?:[pP]risms?)'+ nolikeshape + endwith_nochar,    # added for "gold hexagonal prisms"
                startstr + '(?:'+'(?:[pP]risms?)(?:like| ?shaped?)'+'|[pP]rismatic'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'(?:[pP]risms?)(?:like| ?shaped?)'+'|[pP]rismatic'+')'+ endwith_nochar,
            ],
            'Bone':[ 
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:(?:[dD]og[\-‐−–]?)?[bB]ones?)'+ nolikeshape + endwith_nochar,    
                startstr + '(?:'+'(?:(?:[dD]og[\-‐−–]?)?[bB]ones?)(?:like| ?shaped?)'+'|[bB]ony'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'(?:(?:[dD]og[\-‐−–]?)?[bB]ones?)(?:like| ?shaped?)'+'|[bB]ony'+')'+ endwith_nochar,
            ],
            'Dumbbell':[ 
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+'(?:[dD]umbbels?)'+ nolikeshape + endwith_nochar,    
                startstr + '(?:'+'(?:[dD]umbbels?)(?:like| ?shaped?)'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+'(?:'+'(?:[dD]umbbels?)(?:like| ?shaped?)'+')'+ endwith_nochar,
            ],  
            'Disk':[ 
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:[dD]is[kc]s?)'+ nolikeshape + endwith_nochar,    # enforce nano
                startstr + '(?:'+'(?:[dD]is[kc]s?)(?:like| ?shaped?)'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[dD]is[kc]s?)(?:like| ?shaped?)'+ ')'+ endwith_nochar,
            ], 
            'Cage':[ 
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:[cC]ages?)'+ nolikeshape + endwith_nochar,     # enforce nano
                startstr + '(?:'+'(?:[cC]ages?)(?:like| ?shaped?)'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[cC]ages?)(?:like| ?shaped?)'+ ')'+ endwith_nochar,
            ], 
            'Sheet':[ 
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:[sS]heets?)'+ nolikeshape + endwith_nochar,    #enforce nano
                startstr + '(?:'+'(?:[sS]heets?)(?:like| ?shaped?)'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[sS]heets?)(?:like| ?shaped?)'+ ')'+ endwith_nochar,
            ],
            'Belt':[ 
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:[bB]elts?)'+ nolikeshape + endwith_nochar,    #enforce nano
                startstr + '(?:'+'(?:[bB]elts?)(?:like| ?shaped?)'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[bB]elts?)(?:like| ?shaped?)'+ ')'+ endwith_nochar,
            ],
            'Ring':[ 
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:[rR]ings?)'+ nolikeshape + endwith_nochar,    #enforce nano
                startstr + '(?:'+'(?:[rR]ings?)(?:like| ?shaped?)'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
                startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ '(?:'+'(?:[rR]ings?)(?:like| ?shaped?)'+ ')'+ endwith_nochar,
            ],

            'O':[ 
                startstr + '[bB]ranched (?:('+element+'|'+matformula+') )?'+nano+'(?:particle|crystal|structure)s?'+ nolikeshape + endwith_nochar,    # enforce nano
                
                startstr + '(?:('+element+'|'+matformula+') )?'+nano+'(?:biprism|shell|dot|ribbon|platelet|chain|rattle|bar|antenna|box|needle|thorn|film|pillar|grain|cable|rice|dendrite|polyhedra|spindle|branch|urchin|matryoshka|popcorn|bead|strand|whisker|dimer|cross|flake|petal|micelle|horn|worm|needle|comb|scaffold|rose|diamond|spike|cup|raspberry|raspberries|leave|bowl)s?'+ nolikeshape + endwith_nochar,    # enforce nano
                startstr + '(?:'+'(?:biprism|shell|dot|ribbon|platelet|chain|rattle|bar|antenna|box|needle|thorn|film|pillar|grain|cable|rice|dendrite|polyhedra|spindle|branch|urchin|matryoshka|popcorn|bead|strand|whisker|dimer|cross|flake|petal|micelle|horn|worm|needle|comb|scaffold|rose|diamond|spike|cup|raspberry|raspberries|leave|bowl)s?(?:like| ?shaped?)'+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            ],
            # '':[ # no acronym
            # # startstr + '('+element+anyspace+'|'+element_tight+'|'+matformula+anyspace+'?'+')?'+'NO[A-Z]*s?'+ endwith_nochar, 
            # startstr + '(?:('+element+'|'+matformula+') )?'+nano+'?'+ NOUNFORM + nolikeshape + endwith_nochar,     #gold rods are allowed by ? after nano however caution for gold wires
            # startstr + '(?:'+'NOUNFORM[\-‐−–]?(?:like| ?shaped?)'+ADJFORMS+') '+ desc_capping_optional + '(?:'+strictAuNP+'|'+strictAunanop+')' + endwith_nochar,
            # startstr + '(?:'+strictAuNP+'|'+strictAunanop+')'+' (?:[a-z]* ){0,4}(?:were|was|are|is) '+ COPY +')'+ endwith_nochar, 
            # ],
        }

goldmorphacronym_regex_strict={
    'Au':[
        # '([A-Za-z]+ (?:[gG]old |Au )?(?:[nN]ano)?[A-Z]?[a-z]+) ?\(([A-Za-z](?:Au ?|[gG]old |G)[A-Za-rt-z]+)s?\)',#replaced with below two lines because thioglycolic acid (TGA) was caught
        '([A-Za-z]+ (?:[gG]old |Au )?(?:[nN]ano)?[A-Z]?[a-z]+) ?\(([A-Za-z](?:Au ?|[gG]old )[A-Za-rt-z]+)s?\)',

        # '((?:[gG]old |Au )?(?:[nN]ano)?[A-Z]?[a-z]+) ?\(((?:Au ?|[gG]old |G)[A-Za-rt-z]+)s?\)',#replaced with below two lines because Graphene oxide (GO) was detected as Gold Oxide
        '((?:[gG]old |Au )(?:[nN]ano)?[A-Z]?[a-z]+) ?\(((?:Au ?|[gG]old )[A-Za-rt-z]+)s?\)',
        '((?:[gG]old |Au )(?:[nN]ano)?[A-Z]?[a-z]+) ?\(((?:G)[A-Za-rt-z]+)s?\)',

        '(?:[gG]old |Au )((?:[A-Za-z]+ )?(?:[nN]ano)?[A-Z]?[a-z]+) ?\(([A-Z][A-Za-rt-z]+)s?\)',
    ]
}



Subrecipe_Dict_regex={

    'SeedSln':[
        '(Au ?|G|[gG]old)?NPs?(?!\w)',
        '([gG]old |Au )?[sS]eeds?( solution)?(?![\s\-–]mediated)',
    ],
    'GrowthSln':[
        '(separate|another) flask', # not 100% sure if growth is discussed later than the seedsln but assuming
        '(?<![sS]eed[\s\-–]mediated )(?<![sS]eeding )(?<![sS]eeded )(?<!\w)[gG]row(?:th solution)?(?!th method)',
    ],
    'FinalProd':[
        '(?<=\s)(Au ?|G)?NRs?',
        '(Au |[gG]old )?(?<=\s)([nN]ano)?[rR]ods?(like\w*|[^\w\s.,;:)]\w+)?(?=[^\w])',
    ],

}

Prec_Dict_regex={
    #Gold
        'AuCl3':[
            startstr+'AuCl3'+endwith_nochar,
            startstr+'[gG]old( ?\(III\))? [cC]hloride'+endwith_nochar,
            startstr+'[aA]uric( ?\(III\))? [cC]hloride'+endwith_nochar,
            startstr+'[gG]old( ?\(III\))? [tT]richloride'+endwith_nochar,
        ],
        'NaAuCl4':[
            startstr+'NaAuCl4(?: dehydrate)?'+endwith_nochar,
            startstr+'[sS]odium (?:[tT]etra)?[cC]hloroaurate( ?\(III\))?(?: dehydrate)?'+endwith_nochar,
            startstr+'[gG]old( ?\(III\))? (?:chloride sodium|sodium chloride)'+endwith_nochar,
            startstr+'[sS]odium [gG]old( ?\(III\))? [cC]hloride'+endwith_nochar,
        ],
        'AuCl4':[ #XAuCl4 would count here too
            startstr+'\w*(?<!Na)(?<!H)AuCl4( ?[\-‐−–])?'+endwith_nochar,
            startstr+'\w*AuCl4(?: (?:an)?[iI]ons?)?'+endwith_nochar,
            startstr+'[tT]etrachloroaurates?(?: (?:an)?[iI]ons?)?'+endwith_nochar,
        ],
        'HAuCl4':[
            startstr+'HAuCl4(?: ions?)?'+endwith_nochar,#added "ions" because 10.1016/j.bioelechem.2016.03.006 'HAuCl4 ions'
            startstr+'(?<![sS]odium )[hH]ydrogen [tT]etrachloroaurate( ?\(III\))?'+endwith_nochar,
            startstr+'([hH]ydrogen )?([tT]etra)?([cC]hloro)?auric( ?\(III\))? acid'+endwith_nochar,
        ],

        # maybe classify  into groups to distinguish x 3 4 ((?P<hyd>(x| ))|(?P<tri>(3|tri))|(?P<tetra>(4|tetra)))
        'HAuCl4·xH2O':[
            startstr+'HAuCl4 ?([hH]ydrate|[•·⋅.×✕     \s][     \s]?x[     \s]?H2O)'+endwith_nochar,
            startstr+'[gG]old( ?\(III\))? [cC]hloride [hH]ydrate'+endwith_nochar,
            startstr+'([hH]ydrogen )?([tT]etra)?[cC]hloroauric( ?\(III\))? [aA]cid [hH]ydrate'+endwith_nochar, # "hydrogen tetrachloroauric(III) acid trihydrate" was found. this is supposed to be typo leading to prenormalize_grouponly=0
            startstr+'(?<![sS]odium )([gG]old( ?\(III\))? )?([hH]ydrogen )?[tT]etrachloroaurate( ?\(III\))? [hH]ydrate'+endwith_nochar,
        ],
        'HAuCl4·3H2O':[
            startstr+'HAuCl4 ?([tT]rihydrate|[•·⋅.×✕     \s][     \s]?3[     \s]?H2O)'+endwith_nochar,
            startstr+'[gG]old( ?\(III\))? [cC]hloride [tT]rihydrate'+endwith_nochar,
            startstr+'([hH]ydrogen )?([tT]etra)?[cC]hloroauric( ?\(III\))? [aA]cid [tT]rihydrate'+endwith_nochar,
            startstr+'(?<![sS]odium )([gG]old( ?\(III\))? )?([hH]ydrogen )?[tT]etrachloroaurate( ?\(III\))? [tT]rihydrate'+endwith_nochar, #Ah some ppl write gold tetrachloroaurate. this should be wrong.. 10.1016/j.orgel.2014.03.039
        ],
        'HAuCl4·4H2O':[
            startstr+'HAuCl4 ?([tT]etrahydrate|[•·⋅.×✕     \s][     \s]?4[     \s]?H2O)'+endwith_nochar,
            startstr+'[gG]old( ?\(III\))? [cC]hloride [tT]etrahydrate'+endwith_nochar,
            startstr+'([hH]ydrogen )?([tT]etra)?[cC]hloroauric( ?\(III\))? [aA]cid [tT]etrahydrate'+endwith_nochar,
            startstr+'(?<![sS]odium )([gG]old( ?\(III\))? )?([hH]ydrogen )?[tT]etrachloroaurate( ?\(III\))? [tT]etrahydrate'+endwith_nochar,
        ],    
    
    #Silver
        # 'Ag':[
        # "Ag(?!NO3)[^.:;,)\s]*",    
        # "\w*[sS]ilver[^.:;,)\s]*",
        # ], #Au@Ag is caught, did not expect this so killed this.
        'Ag+':[ # Ag nanoparticle might be caught.. maybe only used for direct NER
            startstr+'Ag(?: ?\+)?'+endwith_nochar,
            startstr+'([sS]ilver|Ag)(?: ?\(I\)| ?\+)?(?: (cat)?ions?)?(?! [nN]itrate)'+endwith_nochar,
        ],
        'AgNO3':[
            startstr+'AgNO3'+endwith_nochar,
            startstr+'[sS]ilver(?: ?\([I+]\))? [nN]itrate'+endwith_nochar,
        ],
    
    #Reducing Agents
        'BH4':[ #XBH4
            startstr+'\w*(?<!Na)BH4'+endwith_nochar,
            startstr+'(?:\wium )?(?<![sS]odium )[bB]orohydride'+endwith_nochar,
        ],
        'NaBH4':[
            startstr+'NaBH4'+endwith_nochar,
            startstr+'[sS]odium [bB]orohydride'+endwith_nochar,
            startstr+'[sS]odium [tT]etra(hydridoborate|hydroborate)( ?\(III\))?'+endwith_nochar,
        ],
        'AA':[
            startstr+'C6H8O6'+endwith_nochar,
            startstr+'(?:(?:[lL][\-‐−–]?)?AA|VC|Vc)'+endwith_nochar,
            startstr+'(?:[lL](?:\(\+\))? ?[\-‐−–] ?)?(?:[aA]scorbic [aA]cid|[vV]itamin[ ?\-‐−–][cC])'+endwith_nochar,
        ],
        'HQ':[
            startstr+'HQ'+endwith_nochar,
            startstr+'(?:C6H4(OH)2|C6H6O2)'+endwith_nochar,
            startstr+'(?:[hH]ydroquinone|[qQ]uinol)'+endwith_nochar,
        ],
        'H2O2':[
            startstr+'H2O2'+endwith_nochar,
            startstr+'[hH]ydrogen [pP]eroxide'+endwith_nochar,
        ],

    
    #Stabilizers - !!! do not catch CTAB-stabilized seed as CTAB. -> Hmm maybe necessary for direct NER

        'Cit':[#error 'citrate-citric acid buffer'  10.1016/j.aca.2015.01.016 # ammonium citrate might count here
            startstr+'[cC]itrate(?: [tT]ribasic)?'+nocapping+endwith_nochar,
            startstr+'[cC]itric [aA]cid'+nocapping+endwith_nochar,
            startstr+'C6H[58]O7(?: [tT]ribasic)?'+nocapping+endwith_nochar,
        ],
        'NaCit':[
            startstr+'((?:[tT]ri-?)?[sS]odium[\-‐−–\s]|Na |Na3 )[cC]itrate(?: [tT]ribasic)?( [dD]ehydrate)?'+nocapping+endwith_nochar,
            startstr+'(?:Na3 ?C6H5O7|C6H5O7 ?Na3|C6H5Na3O7)(?: [tT]ribasic)?'+nocapping+endwith_nochar,    
        ],
        'NaCit·2H2O':[
            startstr+'((?:[tT]ri-?)?[sS]odium[\-‐−–\s]|Na |Na3 )[cC]itrate(?: [tT]ribasic)?( \w*(?<!de)hydrate|[     •·⋅.×✕][     \s]?\d[     \s]?H2O)(?: [tT]ribasic)?'+nocapping+endwith_nochar,
            startstr+'(?:Na3 ?C6H5O7|C6H5O7 ?Na3|C6H5Na3O7)(?: [tT]ribasic)?( \w*(?<!de)hydrate|[     •·⋅.×✕][     \s]?\d[     \s]?H2O)'+nocapping+endwith_nochar,
        ],

        'CTAB':[
            startstr+'C(?:\d*)?TA(?:B|[\-‐−–]?Br)'+nocapping+endwith_nochar,
            startstr+'([cC]eth?yl ?|(?:\d[\-‐−–])?[hH]exadecyl ?|\(\d[\-‐−–][hH]exadecyl\))[tT]rimethyl ?[aA]mmonium [bB]romide'+nocapping+endwith_nochar, # fixed 5DEC
            # startstr+'([cC]eth?yl ?|\d[\-‐−–][hH]exadecyl ?|\(\d[\-‐−–][hH]exadecyl\))[tT]rimethyl ?[aA]mmonium [bB]romide'+nocapping+endwith_nochar,
            startstr+'[cC]etrimonium [bB]romide'+nocapping+endwith_nochar,
        ],
        'CTAC':[
            startstr+'C(?:\d*)?TA(?:C|[\-‐−–]?Cl)'+nocapping+endwith_nochar,
            startstr+'([cC]eth?yl ?|\d[\-‐−–][hH]exadecyl ?|\(\d[\-‐−–][hH]exadecyl\))[tT]rimethyl ?[aA]mmonium [cC]hloride'+nocapping+endwith_nochar,
            startstr+'[cC]etrimonium [cC]loride'+nocapping+endwith_nochar,
        ],
        'xTA':[
            startstr+'[A-BD-Z](\d*)?TA(?:[BC]|[\-‐−–]?(?:Br|Cl))'+nocapping+endwith_nochar,
            startstr+'\w+(?<![cC]etyl)(?<![cC]etyl )(?<![hH]exadecyl)(?<![hH]exadecyl )(?<![hH]exadecyl\))[tT]rimethyl ?[aA]mmonium(?: [bB]romide| [cC]hloride)'+nocapping+endwith_nochar,
        ],
        'CTA':[ #CTAx
            startstr+'C(\d*)?TA\w*'+nocapping+endwith_nochar,
            startstr+'([cC]eth?yl ?|\d[\-‐−–][hH]exadecyl ?|\(\d[\-‐−–][hH]exadecyl\))[tT]rimethyl ?[aA]mmonium'+nocapping+endwith_nochar,
        ],

        'BSA':[
            startstr+'BSA'+nocapping+endwith_nochar,
            startstr+'[bB]ovine [sS]erum [aA]lbumin'+nocapping+endwith_nochar,
        ],
        'PVP':[
            startstr+'PVP(?:[\s\-‐−–]?\d+)?'+nocapping+endwith_nochar,
            startstr+'[pP]oly[\-‐−–]?\(?vinyl ?pyrrolidone\)?'+nocapping+endwith_nochar,
            startstr+'[pP]o(?:ly)?vidone'+nocapping+endwith_nochar,
            startstr+'\(?C6H9NO(?:\)n)?'+nocapping+endwith_nochar,
        ],
        'PDDA':[
            startstr+'PDDA(?:[\s\-‐−–]?\d+)?'+nocapping+endwith_nochar,
            startstr+'[pP]oly[\-‐−–]?\(?diallyl ?[dD]imethyl ?[aA]mmonium\)?( ?[cC]hloride)?'+nocapping+endwith_nochar,
        ],
        'TOAB':[
            startstr+'TOAB'+nocapping+endwith_nochar,
            startstr+'[tT]etra[\-‐−–]?((-N-)|(-n-))?octyl ?[aA]mmonium [bB]romide'+nocapping+endwith_nochar,
        ],
        'TEOS':[
            startstr+'TEOS'+nocapping+endwith_nochar,
            startstr+'[tT]etraethyl [oO]rthosilicate'+nocapping+endwith_nochar,
        ],
        'BDAC':[ # also BDAx
            startstr+'BDAC?'+nocapping+endwith_nochar,
            startstr+'[bB]enzyl ?[dD]imethyl ?(?:[hH]exadecyl ?)?[aA]mmonium(?: [cC]hloride)?'+nocapping+endwith_nochar,
        ],
        'xAC':[
            startstr+'\w+(?<![cC]etyl )(?<![hH]exadecyl )(?<![dD]imethyl )[aA]mmonium [cC]hloride'+nocapping+endwith_nochar,
        ],
        'xAB':[
            startstr+'\w+(?<![cC]etyl )(?<![hH]exadecyl )(?<![tT]rimethyl )(?<![tT]rimethyl)[aA]mmonium [bB]romide'+nocapping+endwith_nochar, # fixed 5DEC
            # startstr+'\w+(?<![cC]etyl )(?<![hH]exadecyl )(?<![dD]imethyl )[aA]mmonium [bB]romide'+nocapping+endwith_nochar,
        ],

        ###
        # # These two were added after the LLM validation
        # '5-BrSA':[  #xOl
        #     startstr+'(?:5-)?[bB]romosalicylic acid'+nocapping+endwith_nochar,
        #     startstr+'(?:5-)?BrSA'+nocapping+endwith_nochar,
        # ],
        # 'TritonX':[  #xOl
        #     startstr+'Triton(?: )?X(?:-100)?'+nocapping+endwith_nochar,
        # ],
        # # These two were added after the LLM validation
        ###

        'OlA':[  #xOl
            startstr+'C18H34O2'+nocapping+endwith_nochar,
            startstr+'(?<![sS]odium )[oO]leate'+nocapping+endwith_nochar,
            startstr+'[oO]leic [aA]cid'+nocapping+endwith_nochar,
        ],
        'NaOlA':[
            startstr+'(?:NaOL|C18H33NaO2)'+nocapping+endwith_nochar,
            startstr+'[sS]odium [oO]leate'+nocapping+endwith_nochar,
            startstr+'[oO]leic [aA]cid'+nocapping+endwith_nochar,
        ],
        'HEPES':[
            startstr+'(?:HEPES|C18H33NaO2)'+nocapping+endwith_nochar,
            startstr+'(?:[2N][\-‐−–])?\[?4[\-‐−–](2[\-‐−–][hH]ydroxyethyl)piperazine[\-‐−–][1N]′?[\-‐−–]yl\]?\s?ethanesulfonic acid'+nocapping+endwith_nochar,
            startstr+'(?:\d+[\-‐−–])?[pP]iperazineethanesulfonic acid'+nocapping+endwith_nochar,
            startstr+'(?:\w*ium )?N-(2-hydroxyethyl)piperazine-N′-(2-ethanesulfonate)'+nocapping+endwith_nochar,
        ],
        'Thiol':[
            startstr+'[\w\-‐−–]*[tT]hiol'+nocapping+endwith_nochar,#decanethiol
        ],
        'C18N3':[#412.7
            startstr+'C18N3'+nocapping+endwith_nochar,
            startstr+'(?:bis[\s\-‐−–]?)?\([aA]midoethyl[\-‐−–\s][cC]arbamoylethyl\) ?[oO]ctadecylamine'+nocapping+endwith_nochar,
        ],
        'GSH':[#307.3235 
            startstr+'(?:GSH|[gG]lutathione|C10H17N3O6S)'+nocapping+endwith_nochar,
        ],
        'PEI':[
            startstr+'(?:PEI|[pP]oly[\-‐−–\s]?\(?[eE]thylene ?[iI]mine\)?)'+nocapping+endwith_nochar,
        ],
        'Glu':[ #180.156
            startstr+'[gG]lucose'+nocapping+endwith_nochar,
        ],
        'ThGlu':[ #196.22
            startstr+'(?:\w[\s\-‐−–])?[tT]hioglucose'+nocapping+endwith_nochar,
        ],
        'Tann':[#1701.19
            startstr+'(?:[tT]annic [aA]cid|[tT]annin|C76H52O46)'+nocapping+endwith_nochar,
        ],
        'Cl':[
            startstr+'(?:[A-Za-z]+um [cC]hloride|[A-Z][a-z]?Cl\d?)'+endwith_nochar,
        ],
        'Br':[
            startstr+'(?:[A-Za-z]+um [bB]romide|[A-Z][a-z]?Br\d?)'+endwith_nochar,
        ],
        'I':[
            startstr+'(?:[A-Za-z]+um [iI]odide|[A-Z][a-z]?I\d?)'+endwith_nochar,
        ],

    #Solvent
        'DMF':[
            startstr+'(?:(?:(?:[nN\d], ?)?[nN\d])[\-‐−–])?(?:DMF|[dD]imethyl ?[fF]ormamide)'+endwith_nochar,
        ],
        'othersolvent':[#1,5-pentanediol–PVP
            startstr+'([oO]rganic|[nN]on ?[\-‐−–]? ?polar|[hH]ydro[\-‐−–]?phobic|[lL]ipophilic) solvent'+endwith_nochar,
            startstr+'([eE]thanol|[gG]lycerine|[tT]oluene|[aA]cetone|[mM]ethanol|C2H5OH|CH3OH|C2H5OH|C3H6O)'+endwith_nochar,
            startstr+'poly\([^\/.:;,\)\s]* ?[^\/.:;,\)\s]*ol\)'+endwith_nochar,
            startstr+'poly[^\/.:;,\)\s]* ?[^\/.:;,\)\s]*ol'+endwith_nochar,
            startstr+'([nN\d],[nN\d])[\-‐−–][^\/.:;,\-‐−–)\s]*ol'+endwith_nochar,#1,5-pentanediol
        ],        
        'H2O':[
            startstr+'(?<!\d[     ])(?<!\d)(?<![•·⋅×✕])H2O'+endwith_nochar,
            startstr+'(?:[hH]ighly )?(?:[dD]istilled |[pP]urified |DI )?(?<!\% in )[wW]ater(?! bath)'+endwith_nochar,
            startstr+'[aA]queous'+endwith_nochar,
        ],
    
    #Acidenv
        'HCl':[
            startstr+'(?:HCl|[hH]ydrochloric [aA]cid)'+endwith_nochar,
            startstr+'[hH]ydrochloric acid'+endwith_nochar,     
        ],
        'NaOH':[
            startstr+'(?:NaOH|[sS]odium [hH]ydroxide)'+endwith_nochar,
        ],
        'HNO3':[
            startstr+'(?:HNO3|[nN]itric [aA]cid)'+endwith_nochar,
        # "[aA]qua regia",
        ],
        'H2SO4':[
            startstr+'(?:H2SO4|[sS]ulfuric [aA]cid)'+endwith_nochar,
        ],
} 
amountparse_regex='(?:(?:(?<=^)|(?<=[\(\s]))((\d+(?:\.\d+)?(?:[    \s]?[×✕][    \s]?10[\-‐−–][    \s]?\d)?)([    \s]?[mμµ]?(?:mol|[gMmℓlL]|cm3|cc|(?:wt.?[    \s]?)?%(?:[    \s]?(?:\(?[wWvV]\/[wWvV]\)))?)(?:(?:[    \s][mμµ]?[ℓLl]?[    ]?[\-‐−–][    ]?1)|(?:\/(?:[mμµ]?[ℓLl]|cm3)))?),? )?(?:(?:of )?(?:a |an |the )?(?:fresh(?:ly prepared)?,? |newly made,? )?(?:(?:ice[\-‐−– ])?cold,? |ice[\-‐−– ]cooled,? |boiling,? )?(?:fresh(?:ly prepared)?,? |newly made,? )?(?:aqueous |seed |growth )?(?:(?:another |separate )?(?:solution|aliquot|portion|amount|mixture),? )?(?:containing |(?:consisted |consisting |consists )?of )?)?(?:a |an |the )?(?:freshly prepared (?:, |and )?|newly made (?:, |and )?)?(?:aqueous )?(?:(?:ice[\-‐−– ])?cold |ice[\-‐−– ]cooled |boiling )?(?:aqueous )?((\d+(?:\.\d+)?(?:[ \s]?[×✕][ \s]?10[\-‐−–][    \s]?\d)?)([    \s]?[mμµ]?(?:mol|[gMmℓlL]|cm3|cc|(?:wt.?[    \s]?)?%(?:[    \s]?(?:\(?[wWvV]\/[wWvV]\)))?)(?:(?: [mμµ]?[ℓLl][    ]?[\-‐−–][    ]?1)|(?:\/(?:[mμµ]?[ℓLl]|cm3)))?) )?)?(?:of )?(?:a |an )?(?:fresh(?:ly prepared)?,? |newly made,? )?(?:ice[\-‐−– ]cold,? |ultrapure |deionized |\w*-?distilled |room temperature |boiling )?(?:fresh(?:ly prepared)?,? |newly made,? )?(?:aqueous )?(?:(?:solution )?of )?PREC(?![\/\-‐−–]PREC)(?! seed solution)(?: ?\(PREC\))?(?:(?: aqueous)? solution)?( ?\([A-Za-z.,\-‐−– ]*[≥>]?[    \s]?((\d+(?:\.\d+)?(?:[    \s]?[×✕][    \s]?10[\-‐−–][    \s]?\d)?)([    \s]?[mμµ]?(?:mol|[gMmℓlL]|cm3|cc|(?:wt.?[    \s]?)?%(?:[    \s]?(?:\(?[wWvV]\/[wWvV]\)))?)(?:(?:[    \s][mμµ]?[ℓLl][    ]?[\-‐−–][    ]?1)|(?:\/(?:[mμµ]?[ℓLl]|cm3)))?))(?: in[\w ]{0,15} water)?((?:,|;| of) ?(\d+(?:\.\d+)?(?:[    \s]?[×✕][    \s]?10[\-‐−–][    \s]?\d)?)([    \s]?[mμµ]?(?:mol|[gMmℓlL]|cm3|cc|(?:wt.?[    \s]?)?%(?:[    \s]?(?:\(?[wWvV]\/[wWvV]\)))?)(?:(?:[    \s][mμµ]?[ℓLl][    ]?[\-‐−–][    ]?1)|(?:\/(?:[mμµ]?[ℓLl]|cm3)))?))?\))?' # fixed mol L- 1 space btwn L-1


realsolventlist=['DMF','othersolvent','H2O',]
solventlist=['DMF','othersolvent','H2O', 'H2SO4','HCl','NaOH','HNO3']
Prec_Dict_regex_nosolvent= {key:val for key, val in Prec_Dict_regex.items() if key not in solventlist}

Prec_Dict_regex_noaqueous={key:val for key, val in Prec_Dict_regex.items() if key!='H2O'}
Prec_Dict_regex_noaqueous['H2O']=Prec_Dict_regex['H2O'][:-1] # exclude "aqueous"

spaces_global=[' ',' ',' ',' ',u'\u202f',u'\xa0'] # [      \s]
spaces_global_replace=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','　']#[               　]
hyphons_global=['-','‐','−','–']  #[\-‐−–]
multiplysigns_global=['×','✕']
mu_global=['μ','µ']

Prec_Dict_regex_normalize={
'AuCl4-':['AuCl3', 'AuCl4','NaAuCl4', 'HAuCl4', 'HAuCl4·xH2O', 'HAuCl4·3H2O', 'HAuCl4·4H2O',],
'AgNO3':['Ag+', 'AgNO3',], #'Ag', 
'BH4-':['NaBH4','BH4'],
'Cit': ['Cit', 'NaCit', 'NaCit·2H2O',],
'CTAB':['CTAB',],
'xTA':['xTA','CTA'],
'CTAC':['CTAC',],

'TOAB':['TOAB',],
'BSA':['BSA',],
'PVP':['PVP',],
'PDDA':['PDDA',],    
'TEOS':['TEOS',],
'BDAC':['BDAC',],
'5-BrSA':['5-BrSA',],
'TritonX':['TritonX',],
'NH2OH':['NH2OH',],
'LSB':['LSB',],
'SDS':['SDS',],


'xAC':['xAC',],
'xAB':['xAB',],
'OlA':['OlA', 'NaOlA',],
'Thiol':['Thiol'],


'PEI':['PEI'],
'Glu':['Glu','ThGlu'],


'HEPES':['HEPES'], 
'C18N3':['C18N3'],
'GSH':['GSH'], 
'Tann':['Tann'],
'Cl':['Cl'],
'Br':['Br'],
'I':['I'],


'AA':['AA',],
'H2O2':['H2O2',],
'HQ':['HQ',],
    
'DMF':['DMF'],
'othersolvent':['othersolvent'],
'H2O':['H2O'],
    
'HCl':['HCl'],
'NaOH':['NaOH'],
'HNO3':['HNO3'],
'H2SO4':['H2SO4'],


'Other':[],   
}
map_precsubcat2cat = {prec: cat for cat, v in Prec_Dict_regex_normalize.items() for prec in v}


unitsbank_dict_regex={
    'concent':{
        1e3:[
            '^mol\/(?:m[ℓlL]|cm3|cc)$',
            '^mol[    \s](?:m[ℓlL]|cm3|cc)[\-‐−–]1$',
        ],
        1:['^[Mm]$',
            '^mol\/[ℓlL]$','^mmol\/(?:m[ℓlL]|cm3|cc)$',
            '^mol[    \s][ℓlL][\-‐−–]1$','^mmol[    \s](?:m[ℓlL]|cm3|cc)[\-‐−–]1$',],
        1e-3:['^m[Mm]$',
            '^mmol\/[ℓlL]$','^[μµ]mol\/(?:m[ℓlL]|cm3|cc)$',
            '^mmol[    \s][ℓlL][\-‐−–]1$','^[μµ]mol[    \s](?:m[ℓlL]|cm3|cc)[\-‐−–]1$'], 
        1e-6:[
            '^[μµ][Mm]$',
            '^[μµ]mol\/[ℓlL]$',
            '^[μµ]mol[    \s][ℓlL][\-‐−–]1$',],
        1e-9:['^nM$','^nmol\/[ℓlL]$',],
    },
    'vol':{
        1:['^[ℓlL]$'],
        1e-3:['^(?:m[ℓlL]|cm3|cc)$'], 
        1e-6:['^[μµ][ℓlL]$'], 
    },
    'wt':{
        1:['^g$'],
        1e-3:['^mg$'],
        1e-6:['^[μµ]g$'],
    },
    'wtpervol':{
        1e3:[
            '^g\/(?:m[ℓlL]|cm3|cc)$',
            '^g[    \s](?:m[ℓlL]|cm3|cc)[\-‐−–]1$',],
        1:['^g\/[ℓlL]$',
            '^g[    \s][ℓlL][\-‐−–]1$',
            '^mg\/(?:m[ℓlL]|cm3|cc)$',
            '^mg[    \s](?:m[ℓlL]|cm3|cc)[\-‐−–]1$',],
        1e1:['^[    \s]?%(?:[    \s]?(?:\(?[vVwW]\/[vV]\)?))$',],
    },
    'wtperwt':{
        1e1:['^(?:wt.?[    \s]?)?%(?:[    \s]?(?:\(?[wW]\/[wW]\)?))?$',
        
        ] 
    },
    'mole':{
        1:['^mols?$'],
        1e-3:['^mmols?$'],
        1e-6:['^[μµ]mols?$']
    }
}
unitclass_differentmap={
'concent':'concent_mol',
'vol':'vol', 
'wt':'wt',
'wtpervol':'concent_wt',
'wtperwt':'concent_wt',
'mole':'mole',
}
cat2unit_Dict_regex={cat: [unit for factor, unitlist in v.items() for unit in unitlist] for cat, v in unitsbank_dict_regex.items()}
scale2unit_Dict_regex={}#{factor: [unit for factor, unitlist in v.items() for unit in unitlist] for cat, v in unitsbank_dict_regex.items()}
for cat, v in unitsbank_dict_regex.items():
    for factor, unitlist in v.items():
        if factor not in scale2unit_Dict_regex.keys():
            scale2unit_Dict_regex[factor]=unitlist
        else:
            scale2unit_Dict_regex[factor].extend(unitlist)
SeedinGrowth_Dict_regex={
    'SeedinGrowth':[
        "(\d+(?:\.\d+)?(?:[    \s]?[×✕][    \s]?10[\-‐−–]\d)?)[     \s\-‐−–]?([\wμµ]?[ℓlL])[a-zA-Z\s\(\)]{1,25}(?:solution of (?:\w* )?)?seed(?:s| solution)?(?! mediated method)",
        "[sS]eeds?(?: solution)? ?\((\d+(?:\.\d+)?)\s?([\wμµ]?[ℓlL])\)", 
        "(?:different |various )?(?:amounts|aliquots|volumes) of seed(?:s| solutions?)(?![a-z])(?! mediated method)",
        
    ]
}
prec_molarmass={'AuCl3':303.33, 'AuCl4':338.779, 'NaAuCl4':361.77, 'HAuCl4':339.785, 'HAuCl4·xH2O':357.8, 'HAuCl4·3H2O':393.83, 'HAuCl4·4H2O':411.85, 'Ag':None, 'Ag+':None, 'AgNO3':169.87, 'NaBH4':37.83, 'AA':176.12, 'HQ':110.11, 'H2O2':34.015, 'Cit':189.10, 'NaCit':258.06, 'NaCit·2H2O':276.1, 'CTAB':364.45, 'xTAB':None, 'CTAC':320, 'BSA':66430.3, 'PVP':10000, 'PDDA':126.22, 'TOAB':546.79, 'TEOS':208.33, 'DMF':73.1, #'othersolvent',
    'H2O':18, 'HCl':36.458, 'NaOH':40.0, 'HNO3':63.01, 'H2SO4':98.079, 'BDAC':396.09, 'xAC':None, 'xAB':None,'othersolvent':None,'OlA':282.47,'NaOlA':304.44,'Thiol':None,
    'HEPES':238.3012,'xTA':None,'CTA':None,'BH4':None,
'C18N3':412.7,
'GSH':307.3235,
'Tann':1701.19,
'Cl':None,
'Br':None,
'I':None,
'5-BrSA':217.02,
'TritonX':647,
'LSB':336.550, #lauryl sulfobetaine
'SDS':288.38,
'NH2OH':69.49, # NH2OH.HCl

'PEI':None,
'Glu':180.156,
'ThGlu':196.22,
}

allowed_combination_useall=[
                ['concent', 'vol'],
                ['vol', 'concent'],

                ['wt', 'wtperwt'],
                ['wtperwt', 'wt'],
                ['vol', 'wtpervol'],
                ['wtpervol', 'vol'],
                ['vol', 'wtperwt'], #assume density=1g/ml
                ['wtperwt', 'vol'], #assume density=1g/ml

                ['mole'],

                ['wt',],
]
allowed_combination_useone=[
                ['mole', 'vol'],
                ['vol', 'mole'],
                ['vol', 'wt',],
                ['wt', 'vol',],
]
for comp in allowed_combination_useone + allowed_combination_useall:
    assert comp.count('vol')<2, print("review allowed units combination, this creates confusion in which volume to extract")
    assert comp.count('wt')<2, print("review allowed units combination, this creates confusion in which weight to extract")
