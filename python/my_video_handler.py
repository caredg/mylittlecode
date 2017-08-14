#!/usr/bin/env python
############################################################################
#
# Author: Edgar Carrera
#The idea of this script is to take a list of directories with videos,
#check what format they are in,
#rotate them if necessary with exiftool, convert them to the right format mp4,
#concatenate them and upload them to youtube to the right list
# December 31, 2014
############################################################################


"""
   usage: %prog <user> <text file with full directories paths> [options] 
   -c, --clean : just perform the cleaning procedure
"""

import os, string, re,sys
import subprocess
import fileinput
import commands
import ntpath
from collections import OrderedDict
from datetime import datetime

DEBUG = False
printConfig = True

# _____________________OPTIONS_______________________________________________

############################################################################
# Code taken from http://code.activestate.com/recipes/278844/
############################################################################
import optparse
USAGE = re.compile(r'(?s)\s*usage: (.*?)(\n[ \t]*\n|$)')
def nonzero(self): # will become the nonzero method of optparse.Values
    "True if options were given"
    for v in self.__dict__.itervalues():
        if v is not None: return True
    return False

optparse.Values.__nonzero__ = nonzero # dynamically fix optparse.Values

class ParsingError(Exception): pass

optionstring=""

def exit(msg=""):
    raise SystemExit(msg or optionstring.replace("%prog",sys.argv[0]))

def parse(docstring, arglist=None):
    global optionstring
    optionstring = docstring
    match = USAGE.search(optionstring)
    if not match: raise ParsingError("Cannot find the option string")
    optlines = match.group(1).splitlines()
    try:
        p = optparse.OptionParser(optlines[0])
        for line in optlines[1:]:
            opt, help=line.split(':')[:2]
            short,long=opt.split(',')[:2]
            if '=' in opt:
                action='store'
                long=long.split('=')[0]
            else:
                action='store_true'
            p.add_option(short.strip(),long.strip(),
                         action = action, help = help.strip())
    except (IndexError,ValueError):
        raise ParsingError("Cannot parse the option string correctly")
    return p.parse_args(arglist)


#_________________________________________________________________________

###############################################################
def mp4_handler(filefullpath,deg_rotation):
###############################################################    

    filenamebase = os.path.basename(filefullpath).split('.')[0]
    filepath = os.path.dirname(filefullpath)

    #rotation (no conversion as it is already mp4)
    if deg_rotation == 0: 
        str_conversion = "cp "+filefullpath+" "+filepath+"/"+filenamebase+"_myconversion.mp4"
        os.system(str_conversion)
        return
    
    if deg_rotation == 90: mytranspose = "-vf 'transpose=1' "
    if deg_rotation == 180: mytranspose = "-vf 'transpose=2' "
    if deg_rotation == 270:
        print "Rotation for "+deg_rotation+" not implemented"
        exit()

    str_conversion = "avconv -i "+filefullpath+" "+mytranspose+" -c:v copy -c:a copy "+filepath+"/"+filenamebase+"_myconversion.mp4"

    os.system(str_conversion)



###############################################################
def mov_handler(filefullpath,deg_rotation):
###############################################################    

    filenamebase = os.path.basename(filefullpath).split('.')[0]
    filepath = os.path.dirname(filefullpath)

    #rotation and conversion
    if deg_rotation == 0: mytranspose = ""
    if deg_rotation == 90: mytranspose = "-vf 'transpose=1' "
    if deg_rotation == 180: mytranspose = "-vf 'transpose=2' "
    if deg_rotation == 270:
        print "Rotation for "+deg_rotation+" not implemented"
        exit()

    str_conversion = "avconv -i "+filefullpath+" -c:v libx264 "+mytranspose+" -strict experimental "+filepath+"/"+filenamebase+"_myconversion.mp4"

    os.system(str_conversion)

###############################################################
def concatenate_videos(youtubevideo,videosdict):
###############################################################
    #concatenate but with a limit of 500Mb to be able to
    #upload to youtube easily
    #str_cat = "MP4Box -split-size 1000000 -force-cat "
    str_cat = "MP4Box -force-cat "
    for videokey in videosdict:
        str_cat += "-cat "+videokey+" "
    str_cat += youtubevideo

    print str_cat
    os.system(str_cat)
    
    

###############################################################
def order_ordered_dictionary(unordered_ordereddict,valuename):
###############################################################    
    #this function orders a nested dictionary for videos
    #by the valuename value

    ordered_ordereddict = OrderedDict(sorted(unordered_ordereddict.iteritems(),key=lambda x: x[1][valuename]))

    return ordered_ordereddict


###############################################################
def rotate_and_convert_videos(videosdict):
###############################################################    

    for videokey in videosdict:
        deg_rotation = videosdict[videokey]['rotation']
        print deg_rotation
        filetype = videosdict[videokey]['filetype']
        #rotate and convert MOV
        if filetype == 'MOV':
            mov_handler(videokey,deg_rotation)
        #rotate MP4    
        if filetype == 'MP4':
            mp4_handler(videokey,deg_rotation)


###############################################################
def extract_videos_info(videosdict):
###############################################################    

    for videokey in videosdict:
        print "Extracting info for video file "+ os.path.basename(videokey)

        #get the filetype
        str_type = "exiftool "+videokey+ "| grep 'File Type'|awk '{print $4}'" 
        mypipe = subprocess.Popen(str_type,shell=True,stdout=subprocess.PIPE)
        filetype = str(mypipe.communicate()[0]).rstrip()
        videosdict[videokey]['filetype']=filetype
        
        #get rotation as int
        str_rot = "exiftool "+videokey+ "| grep 'Rotation'|awk '{print $3}'" 
        mypipe = subprocess.Popen(str_rot,shell=True,stdout=subprocess.PIPE)
        rotation = int(mypipe.communicate()[0])
        videosdict[videokey]['rotation']=rotation
        
        #get datetime of creation as datetime.datetime
        str_datetime = "exiftool "+videokey+ "| grep 'Track Create Date'|awk -v q=':' '{print $5 q $6}'|awk -F '-' '{print $1}'" 
        mypipe = subprocess.Popen(str_datetime,shell=True,stdout=subprocess.PIPE)
        datetimestr = str(mypipe.communicate()[0]).rstrip()
        mydatetime = datetime.strptime(datetimestr,"%Y:%m:%d:%H:%M:%S")
        videosdict[videokey]['datetime']=mydatetime

    return videosdict


###############################################################
def get_videos_dictionary(videospath,appendstring):
###############################################################    

    str_ls = "/bin/ls -1 -d "+videospath+"/*"+appendstring
    mypipe = subprocess.Popen(str_ls,shell=True,stdout=subprocess.PIPE)
    videoslist = mypipe.communicate()[0].replace(" ","\ ").rstrip().split('\n')
    videosdict={}
    #create empty subdicts for each video
    for thevideo in videoslist:
        videosdict[thevideo]={}
    return videosdict


###############################################################
def check_filetype_support(videosdict):
############################################################### 

    full_file_support = True
    for key in videosdict:
        filetype = videosdict[key]['filetype']
        if (not (filetype == 'MOV' or filetype == 'MP4')):
            full_file_support = False
            break

    return full_file_support



###############################################################
def upload_to_google(inflist,user):
###############################################################

    lin = open(inflist,"r")

    #list to keep track of failed albumns
    failed_albums=[]
    
    #loop over albums
    for line in lin.readlines():
        if line == '\n':
            continue
        cleanpath = line.lstrip().rstrip().replace(" ","\ ")
        #check if path actually exists (for some reason it does not like
        #cleanpath)
        if not(os.path.exists(line.rstrip())):
            print line.rstrip()+" does not exist. Please check."
            sys.exit(1)
        #extract directory name (albumname) wich will be video name at the end
        albumname = os.path.basename(cleanpath)
        print "\nWorking on album "+albumname+" ...."
        #get list of raw video files for the album
        videosdict = get_videos_dictionary(cleanpath,'')
        #extract raw videos information 
        print "Extracting raw video information ... "
        rawvideosdict = extract_videos_info(videosdict)
        #check if all videos in album have supported file types
        if not check_filetype_support(rawvideosdict):
            print "Sorry, at least one of the video files in album "+albumname+" is not supported"
            failed_albums.append(albumname)
            continue
        #rotate and convert raw videos if needed 
        rotate_and_convert_videos(rawvideosdict)
        #get list of converted files for the album
        convideosdict = get_videos_dictionary(cleanpath,'_myconversion.mp4')
        #extract converted videos information 
        print "Extracting converted video information ... "
        readyvideosdict = extract_videos_info(convideosdict)
        #order converted video dict
        o_readyvideosdict = order_ordered_dictionary(readyvideosdict,'datetime')
        #concatenate converted videos in a single file
        #print
        youtubevideo = cleanpath+"/"+albumname+"_youtube.mp4"
        concatenate_videos(youtubevideo,o_readyvideosdict)
        #videonamepath = cleanpath+"/"+albumname
        #upload video
        #myuploadcommand = "google youtube --post "+videonamepath+" -u "+user," --access=unlisted"

    if failed_albums:    
        print "\nThe following list of albumns weren't processed"
        print failed_albums

#######################################################
def get_default_options(option):
#######################################################

    dicOpt = {}

    # activate only clean procedure to remove the
    # original video files, which have been checked to be ok
    # and already uploaded.
    if not option.clean:
        dicOpt['clean'] = False
    else:
        dicOpt['clean'] = True

    
    return dicOpt



###############################################################
if __name__ =='__main__':
###############################################################    


    #import optionparser
    option,args = parse(__doc__)
    if(DEBUG): print args
    if len(args)< 2:
        exit()

    inflist = str(args[1])
    user = str(args[0])
    
    #check if input file exists
    if  not(os.path.isfile(inflist)):
        print inflist+" does not exist. Please check."
        sys.exit(1)


    #set default options
    dicOpt = get_default_options(option)
    if (printConfig):
        for k in dicOpt:
            print str(k)+" = "+str(dicOpt[k])


    #check if just cleaning is needed
    #it is best to keep this separated
    #as deleting originals needs checking beforehand
    #that everything went fine.
    justClean = dicOpt['clean']
    if(justClean):
        print "do the cleaning"
        sys.exit(0)

    #if no cleaning, do the whole thing
    #This is broken due to googleCL not being able to
    #authenticate any more....it sucks.
    upload_to_google(inflist,user)
