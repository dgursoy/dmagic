#!/usr/bin/env python
# -*- coding: utf-8 -*-

# #########################################################################
# Copyright (c) 2015, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2015. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

"""
Module for describing beamline/experiment specific data recipes.
"""

import os
import sys, getopt
import ConfigParser
from validate_email import validate_email

# see README.txt to set a globus personal shared folder
cf = ConfigParser.ConfigParser()
cf.read('globus.ini')
globus_address = cf.get('settings', 'cli_address')
globus_user = cf.get('settings', 'cli_user')

local_user = cf.get('globus connect personal', 'user') 
local_share1 = cf.get('globus connect personal', 'share1') 
local_share2 = cf.get('globus connect personal', 'share2') 
local_shared_folder = cf.get('globus connect personal', 'shared_folder')  

remote_user = cf.get('globus remote server', 'user') 
remote_share = cf.get('globus remote server', 'share') 
remote_shared_folder = cf.get('globus remote server', 'shared_folder')  

def main(argv):
    input_folder = ''
    input_email = ''

    try:
        opts, args = getopt.getopt(argv,"hf:e:",["ffolder=","eemail="])
    except getopt.GetoptError:
        print 'test.py -f <folder> -e <email>'
        #print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'globus_copy_share.py -f <folder> -e <email>'
            print 'copy data from globus connect personal ', local_user + local_share + os.sep + '<folder> to ' + remote_user + remote_share + os.sep + remote_shared_folder
            print 'share data from', remote_user + remote_share + os.sep + remote_shared_folder + "<folder>", ' with ' + "<email>"

            sys.exit()
        elif opt in ("-f", "--ffolder"):
            input_folder = arg
        elif opt in ("-e", "--eemail"):
            input_email = arg
    
    input_folder = os.path.normpath(input_folder) + os.sep # will add the trailing slash if it's not already there.

    globus_scp = "scp -r " + local_user + local_share1 + ":" + os.sep + input_folder + " " + remote_user + remote_share + ":" + remote_shared_folder
    globus_add = "acl-add " + local_user + local_share2  + os.sep + input_folder + " --perm r --email " + input_email
    print "python globus_copy_remote_share.py -f test -e decarlof@gmail.com"
    if validate_email(input_email) and os.path.isdir(local_shared_folder + input_folder):
        cmd_1 = "ssh " + globus_user + globus_address + " " + globus_scp
        cmd_2 = "ssh " + globus_user + globus_address + " " + globus_add
        print cmd_1
        print "ssh decarlo@cli.globusonline.org scp -r decarlo#data:/test/ petrel#tomography:/img/"
        #os.system(cmd1)
        print "Done data trasfer to: ", remote_user
        #os.system(cmd2)
        print cmd_2
        print "ssh decarlo@cli.globusonline.org acl-add decarlo#img/test/ --perm r --email decarlof@gmail.com"
        print "Download link sent to: ", input_email
    else:
        print "ERROR: "
        if not validate_email(input_email):
            print "email is not valid ..."
        else:
            print local_shared_folder + input_folder, "does not exists on the local server", 

    
if __name__ == "__main__":
    main(sys.argv[1:])
