#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import glob
#import commands

host = "keio-server"
server_workdir = "~/documents"

def is_extension_in_dir(dir_path, ext_without_dot):
    file_name = dir_path + '/*.' + ext_without_dot
    file_list = glob.glob(file_name)
    return len(file_list) > 0

def extract_last_element_name(fullpath, sp='/'):
#    id=fullpath.split(sp)
#    lastnum=len(id)-1
#    return id[lastnum]
    idx0 = fullpath.rfind(sp, 0, -1)
    return  fullpath[idx0 + len(sp):]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        target_dir_path_local  = os.getcwd()
    else:
        target_dir_path_local = sys.argv[1]

    if is_extension_in_dir(target_dir_path_local, 'tex') == False:
        print("keio-tex: No file name specified, and I couldn't find any.")
        print('''Usage : ./keio-tex.py [target_dir_path_local]
        if there is no argument, this script looks in the directory
        which it called for .tex files.''')
    else:
        # TODO: send only rewrited files
        # TODO: rsync
        send_texdir_command = "scp -r " + target_dir_path_local + " " \
                + host + ":" + server_workdir + "/"
        print("$ " + send_texdir_command)
        os.system(send_texdir_command)

        target_dir_path_server = server_workdir + "/" \
                + extract_last_element_name(target_dir_path_local)
        ssh_latexmk_command = "ssh " + host + " 'cd " + target_dir_path_server \
                + "; latexmk'"
        print("$ " + ssh_latexmk_command)
        os.system(ssh_latexmk_command)

        # TODO: receive only target .pdf file
        receive_pdf_command = "scp " + host + ":" + target_dir_path_server \
                + "/*.pdf " + target_dir_path_local
        print("$ " + receive_pdf_command)
        os.system(receive_pdf_command)
