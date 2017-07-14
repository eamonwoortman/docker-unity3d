from shutil import copyfile
import os
import subprocess
import time 
import shutil
import signal
import re

unityPackagesFolder = os.path.expanduser('~/.local/share/unity3d/Packages/node_modules/')
ulfFile = os.path.expanduser('~/.local/share/unity3d/Unity/Unity_v5.x.ulf')
unityLauncherAssetFolder = os.path.expanduser('~/.local/share/unity3d/Packages/node_modules/unity-editor-home/dist/assets')
unityLaunchJs='%s/unity-editor-home.js' % unityLauncherAssetFolder
activateUnityProcess = 'xvfb-run --auto-servernum --server-args="-screen 0 640x480x24:32" /opt/Unity/Editor/Unity -logFile /output/unity_auth_test.log'

def clear_unity_launcher_files():
    try:
        shutil.rmtree(unityPackagesFolder)
        print('Patched file removed.')
    except:
        pass

def is_license_registered():
    return os.path.exists(ulfFile)
    
def is_patched():
    f = open(unityLaunchJs, 'r', encoding='utf-8')
    content = f.read()
    f.close()
    if (content.find('UNITY_USER') != -1):
        return True
    return False

def patch_unity_editor():
    if (is_patched()):
        return False;

    licenseMatchStr = r'controller\("license\.controller",\s?\[(.*?)\}\]\)'
    licenseSubstitudeStr = r"""controller("license.controller",[\g<1>, /* automatically pick the free license options */            (function() {                b.license.selectedOption = 'personal';                b.personalOption = 'none';                b.eulaConfirmed = 1;                b.submitSerial();            })();}])"""

    loginFindStr = "a.isSigningIn=!1,a.remember=!0,"            
    loginReplaceStr = """            
                /* automatically login with the environment variables */ 
                (function() { 
                    a.isSigningIn = !0, g.login(env.UNITY_USER, env.UNITY_PASSWORD, 1).success(function() { 
                        console.log('Automatic login succesful'); 
                        1 == c.history.length ? c.unityApi.closeHomeWindow() : c.history.back() 
                    }).error(function(b) { 
                        var err = 'Automatic login failed, code=' + b.code + ', err=' + ((b.error == null) ? 'Undefined' : b.error.code); 
                        console.log(err); 
                        window.close();  
                    }).finally(function() { 
                        a.isSigningIn = !1  
                    })  
                })();a.isSigningIn=!1,a.remember=!0,"""
                    
    envFindStr = "function utButtonDirective(){"
    envReplaceStr = """
    env = {
      UNITY_USER: '%s',
      UNITY_PASSWORD: '%s'
    }
    function utButtonDirective(){
    """%((os.getenv('UNITY_USER', 'invalid@username.com'), os.getenv('UNITY_PASSWORD', 'invalidpassword')))

    gettingStartedFindStr = """controller("gettingstarted.controller",["$scope","$filter","$window",function(b,c,d){"""
    gettingStartedReplaceStr = """controller("gettingstarted.controller",["$scope","$filter","$window",function(b,c,d){ (function(){ d.unityApi.closeHomeWindow(); })();"""

    updateShowFlagsFindStr = """updateShowFlags=function(){"""
    updateShowFlagsReplaceStr = """updateShowFlags=function(){a.connectInfo={workOffline:false};""" 
    
    with open(unityLaunchJs, 'r', encoding="utf-8") as file :
      filedata = file.read()
    filedata = filedata.replace(loginFindStr, loginReplaceStr).replace(envFindStr, envReplaceStr).replace(gettingStartedFindStr, gettingStartedReplaceStr).replace(updateShowFlagsFindStr, updateShowFlagsReplaceStr)
    filedata = re.sub(licenseMatchStr, licenseSubstitudeStr, filedata, flags=re.S)
    with open(unityLaunchJs, 'w', encoding="utf-8") as file:
      file.write(filedata)

    return True

# first clean the launcher files
clear_unity_launcher_files()    
    
# then start Unity to restory the Unity launcher    
p = subprocess.Popen('exec %s'%activateUnityProcess, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)

count = 0
size = 0
lastSize = 0
print ('Waiting for Unity to initialize')

# wait until the launcher files have been restored
while (count < 150):
    count = count + 1
    try:
        size = os.path.getsize(unityLaunchJs)
    except:
        pass

    if (size == 0):
        time.sleep(0.1)
        continue
        
    if (size != lastSize):
        lastSize = size
    else:
        break

    time.sleep(0.1)
               
print('Patching unity editor...')

# attempt to patch it
while(patch_unity_editor() == False):
    time.sleep(0.1)
    
time.sleep(0.5)

print('Waiting for it to register itself...')    

count = 0
while (count < 10):
    patch_unity_editor()
    count = count + 1
    
    if (is_license_registered() == True):
        break
    time.sleep(1)
    
if (is_license_registered() == True):
    print('Successfully automatically registered license!')
else: 
    print('Failed to automatically register license.')

# clear any traces of the patched launcher files
clear_unity_launcher_files()            

p.kill()
os.killpg(os.getpgid(p.pid), signal.SIGTERM)
