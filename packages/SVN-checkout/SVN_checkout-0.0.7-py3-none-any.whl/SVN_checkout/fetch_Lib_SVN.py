# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 09:43:53 2022

@author: s.vaghani
"""

import subprocess
import argparse
import yaml
import os.path
from os import path


def run_svn_command(svnCmd):
    
    proc = subprocess.Popen(
                                svnCmd, 
                                stdout = subprocess.PIPE, 
                                shell = True,
                                universal_newlines = True
                            )
    procComm = proc.communicate()
    
    #print(procComm[0])
    
    return procComm[0]


def getFileList(repoURL):
    
    svnCmd = [
                "svn", "ls",
                repoURL,
                "--depth", "infinity"
             ]
        
    return run_svn_command(svnCmd)
    
def creatDirectoryTree(repoURL, localRepoDir):
    
    print("Local directory created for: %s" %(localRepoDir))
    svnCmd = [
                "svn", "checkout",
                repoURL, localRepoDir,
                "--depth", "empty"
             ]
        
    run_svn_command(svnCmd)
    
    return 0


def updateSingleFile(localFilePath):
    
    tempStrContainer = []
    maxFilesToChkOut = 20
    
    tempStrContainer = [localFilePath[i:i + maxFilesToChkOut] for i in range(0, len(localFilePath), maxFilesToChkOut)]
    
    for fileList in tempStrContainer:
        print("----------------------- Updating files -----------------------")
        print("%s" %("\n".join(fileList)))
        
        svnCmd = [ "svn", "update" ] + fileList
        
        run_svn_command(svnCmd)
    
    return 0


def seprateFilepathNname(inputPath):
    
    fileName = inputPath.split("/")[-1]
    filePath = inputPath.split(fileName)[0]
    
    return [fileName, filePath]


'''
def checkoutSingleFileFromSvn(svnFilePath, repoRoot, localRepoRoot):
    
    fileName, filePath = seprateFilepathNname(svnFilePath) 
    
    if not path.exists(localRepoRoot + '/'+ filePath):
        creatDirectoryTree(
                            repoRoot + '/'+ filePath, 
                            localRepoRoot + '/'+ filePath)
    
    updateSingleFile(localRepoRoot + '/'+ svnFilePath)
    
    return 0
'''


################################################################################
############################ Checkout full repo ################################
################################################################################

def checkoutFullRepo(repoURL, destDir, username, revision):
    
    print("------------------------------------------------------------------")
    print("Checkout triggered for repo: %s" %(repoURL))
    print("Please wait....!!!")
    print("------------------------------------------------------------------")
    
    svnCmd = [
                "svn", "checkout",
                repoURL, destDir, 
                "--username", username
             ]
    
    if revision is not None:
        svnCmd = svnCmd + ["--revision", revision] 
        
    run_svn_command(svnCmd)
    
    return 0


################################################################################
############################  Read config data  ################################
################################################################################

def read_init_data_from_yaml(yamlFile):
    
    with open(yamlFile, 'r') as stream:
        initData = yaml.safe_load(stream)
    
    return initData


def checkout_svn_repo():
    
    print("Checkout is triggered...Please wait..!!!")
    
    rootLocalRepoDir = args.dest if (args.dest is not None) else  projectData['localRepoDir']
    
    for repo in repos2chkout:
        
        repoLink = rootRepoLink + '/' + repo
        localDir = rootLocalRepoDir + '/' + repo
        
        if args.fullRepo :
            checkoutFullRepo( 
                                 repoLink, 
                                 localDir, 
                                 uName,
                                 args.revision
                            )   
        else:
            
            FileList = getFileList(repoLink).split("\n")

            
            file2ckOut = []
            
            temp_filteredFileList = []

            for filePath in FileList:
                
                if filePath.endswith(fileFormate2Checkout):
                    filteredFileList.append(filePath)
                    temp_filteredFileList.append(filePath)
            
            for filename in temp_filteredFileList:
                #print("Checking out file: %s" %(filename))
                
                [f, filePath] = seprateFilepathNname(filename)
                
                if not path.exists(localDir + '/'+ filePath):
                    creatDirectoryTree(
                                        repoLink + '/'+ filePath, 
                                        localDir + '/'+ filePath
                                      )
                    
                file2ckOut.append(localDir + '/' + filename)
             
            updateSingleFile(file2ckOut)
           
    return 0


def saveFileList():
    fileFormate2Checkout = tuple(svnRepoData['file2Checkout'])
    
    for fType in fileFormate2Checkout:
        
        tempFileList = []
        
        for filePath in filteredFileList:
            if filePath.endswith(fType):
                tempFileList.append(filePath)
        
       
        txtFileName = fType + "_fileList.txt"
        txtFile = open(txtFileName, 'w')
        txtFile.write("\n".join(tempFileList))
        txtFile.close()
    
    return 0

###############################################################################    
parser = argparse.ArgumentParser(description='SVN checkout arguments')

parser.add_argument(      '--user',     type=str, help= "Username", default= None)
parser.add_argument(      '--repo',     type=str, help= "SVN repo URL", default= "")
parser.add_argument(      '--dest',     type=str, help= "Destination directory in local PC", default= None)
parser.add_argument('-y', '--yaml',     type=str, help= ".yaml file to read init config", default= None)
parser.add_argument('-r', '--revision', type=int, help= "SVN revision number to checkout", default= None)
parser.add_argument('-p', '--project',  type=str, help= "Project name: M2, S2, MOD", default= None)
parser.add_argument(      '--fullRepo', type=bool,help= "Checkout full repo", default= False)

'''
parser.add_argument('-d', '--depth',            type=str)
parser.add_argument('-f', '--force',            type=str)
parser.add_argument('-i', '--ignore-externals', type=str)
parser.add_argument('-q', '--quiet',            type=str)
'''

args = parser.parse_args()

svnRepoData = {}
projectData = {}

projectName = ""
uName = ""
rootRepoLink = ""
repos2chkout = {}

fileFormate2Checkout = ()

filteredFileList = []

if args.user is not None:

    if args.yaml is not None:
        
        if args.project is not None and args.project in ["M2", "S2", "MOD"]:
            
            svnRepoData = read_init_data_from_yaml(args.yaml)
            
            projectName = args.project
            
            projectData = svnRepoData['projects'][projectName]
            rootRepoLink = projectData['rootRepoLink']
            repos2chkout = projectData['repos']
             
            uName = args.user 
            
            fileFormate2Checkout = tuple(svnRepoData['file2Checkout'])
            
            fileFormate2Checkout = tuple(['.' + sub for sub in fileFormate2Checkout])
            
            checkout_svn_repo()
            saveFileList()
            
            print("Checkout Complete...!!!")
        else:
            print("Error: Please specify project name: M2, S2, MOD..!!!")
    else:
        print("Error: Please specify confige (.yaml) file..!!!")
else:
    print("Error: Username cannot be empty..!!!")




    
    

