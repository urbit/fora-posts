#!/usr/local/bin/python

import os
import random


incol = ['general',
        'answers',
        'proposals',
        'updates'
#        'archive'
        ]

outcol = ["~2015.1.1..20.31.30..4933",
    "~2015.2.2..20.31.30..4933",
    "~2015.3.3..20.31.30..4933",
    "~2015.4.4..20.31.30..4933"
#    "~2015.5.5..20.31.30..4933",
        ]

ship = '~zod'
case = 10

def convert_collection(idx):
    indir = "./fora/"+incol[idx]+"/posts/"
    outdir = "./output/"+outcol[idx]+"/"

    fora = sorted(os.listdir(indir))
    mds = list(filter(lambda x: x[-3:] == '.md', fora))

    for x in mds:
        convert_posts(fora, idx, x)

def convert_posts(fora, idx, post):
    indir = "./fora/"+incol[idx]+"/posts/"
    outdir = "./output/"+outcol[idx]+"/"

    prefix = post[:-8]
    random.seed(post)
    suffix = random.randrange(1000, 9999)

    date = prefix + str(suffix)
    outfilename = date + ".umd"

    infile = open(indir + post, 'r')
    incontent = infile.readlines()
    h = incontent[:9]
    b = incontent[9:]

    outheader = [':-  :~\n',
            '  [%owner \'' + h[4][8:-1] + '\']\n',
            '  [%comments \'.y\']\n',
            '  [%type \'fora\']\n',
            '  [%last-modified \'' + date + '\']\n',
            '  [%date-created \'' + date + '\']\n',
            '  [%name \'' + h[3][7:-1] + '\']\n',
            '    ==\n',
            ';>\n']

    outfile = open(outdir + outfilename, 'w')
    outfile.writelines(outheader + b + ['\n', '\n'])
    outfile.close()
    infile.close()

    configfile = open(outdir + date + ".collections-config", 'w')
    configlines = ['full-path: /%s/home/%d/web/collections/%s/%s/collections-config\n'
            %(ship, case, outcol[idx], date),
        'name: comments\n',
        'description: comments\n',
        'owner: %s\n'%(ship),
        'date-created: %s\n'%(date),
        'last-modified: %s\n'%(date),
        'type: comments\n',
        'comments: n\n',
        'sort-key: ~\n',
        'visible: n']

    configfile.writelines(configlines)
    configfile.close()
 
    if post[:-3] in fora:
        # comments exist
        # therefore create subdirectory
        try:
            os.mkdir(outdir + date)
        except:
            pass
        # iterate through all comment .md files
        coms = os.listdir(indir + post[:-3] + "/comments")

        for y in coms:
            convert_comments(idx, post, date, y)


def convert_comments(idx, inpar, outpar, com):
    indir = "./fora/"+incol[idx]+"/posts/"
    outdir = "./output/"+outcol[idx]+"/"

    random.seed(com)
    date = com[:-7] + str(random.randrange(1000, 9999))
    outfilename = date + ".umd"

    infile = open(indir + inpar[:-3] + "/comments/"+ com, 'r')
    incontent = infile.readlines()
    h = incontent[:1]
    b = incontent[1:]


    outheader = [':-  :~\n',
            '  [%owner \'' + h[0][4:-2] + '\']\n',
            '  [%type \'comments\']\n',
            '  [%last-modified \'' + date + '\']\n',
            '  [%date-created \'' + date + '\']\n',
            '    ==\n',
            ';>\n',
            '\n']

    outcontent = outheader + b + ['\n', '\n']
    outpath = outdir + outpar + '/' + date + '.umd'
    outfile = open(outpath, 'w')
    outfile.writelines(outcontent)
    outfile.close()
    infile.close()



for idx in range(4):
    outdir = "./output/"+outcol[idx]
    try:
        os.mkdir(outdir)
    except:
        pass

    configfile = open(outdir + ".collections-config", 'w')
    configlines = ['full-path: /%s/home/%d/web/collections/%s/collections-config\n'
            %(ship, case, outcol[idx]),
        'name: %s\n'%(incol[idx]),
        'description: %s\n'%(incol[idx]),
        'owner: %s\n'%(ship),
        'date-created: %s\n'%(outcol[idx]),
        'last-modified: %s\n'%(outcol[idx]),
        'type: fora\n',
        'comments: y\n',
        'sort-key: ~\n',
        'visible: y']

    configfile.writelines(configlines)
    configfile.close()

    convert_collection(idx)


