#Nigga this is not to protect my script to add a fucking grabber lol
#its just to fuck skids ;)



from pystyle import *
import requests, ssl, sys, multiprocessing, os
from multiprocessing import cpu_count
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar
from urllib.parse import urlparse
from threading import Thread
from random import randint

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False


requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
r = requests.Session()
r.cookies.set_policy(BlockCookies())


def Banner():
    Clear()
    Banner1 = r"""
╔╦╗  ╦  ╦╔═  ╔═╗  ╦ ╦  ╔═╗  ╦═╗  ╔═╗
 ║   ║  ╠╩╗  ╚═╗  ╠═╣  ╠═╣  ╠╦╝  ║╣ 
 ╩   ╩  ╩ ╩  ╚═╝  ╩ ╩  ╩ ╩  ╩╚═  ╚═╝

"""

    Banner2 = r"""
  ,           ,
 /             \
((__-^^-,-^^-__))
 `-_---' `---_-'
  <__|o` 'o|__>
     \  `  /
      ): :(
      :o_o:
       "-" 
       """

    cPrint(Colors.yellow_to_red, Add.Add(Banner2, Banner1, center=True))

def Clear():
    os.system("cls" if os.name == "nt" else "clear")

def cPrint(Color, Text):
    print(Center.XCenter(Colorate.Vertical(Color, f"{Text}", 2)))

def dPrint(Color, Text):
    print(Colorate.Vertical(Color, f"{Text}", 1))

def SendShare(itemID, headers):
    while True:
        try:
            print("Sent " + 
            r.post(
                f"http://api19.toutiao50.com/aweme/v1/aweme/stats/?channel=tiktok_web&device_type=iPad6,3device_id={randint(1000000000000000000, 9999999999999999999)}&os_version=13&version_code=220400&app_name=tiktok_web&device_platform=android&aid=1988",
                headers=headers,
                data=f"item_id={itemID}&share_delta=1"
                ).json()["log_pb"]["impr_id"]
            )
        except:
            pass

def ClearURI(itemID):
    host = urlparse(itemID).hostname.lower()
    if "vm.tiktok.com" == host or "vt.tiktok.com" == host:
        UrlParsed = urlparse(r.head(itemID, stream=True, verify=False, allow_redirects=True, timeout=5).url)
        return UrlParsed.path.split("/")[3]
    else:
        UrlParsed = urlparse(itemID)
        return UrlParsed.path.split("/")[3]

def Title(Content):
    global DebugMode
    if os.name == 'posix':
        sys.stdout.write(f"\33]0;{Content}\a")
        sys.stdout.flush()
        return False
    elif os.name == 'nt':
        os.system(f"title {Content}")
        return False
    else:
        pass

def SpamThread(itemID, Headers, Threads):
    for i in range(Threads):
        try:
            Thread(target=SendShare, args=(itemID,Headers, )).start()
        except:
            pass
def SpamProcess(itemID, Headers, Threads, Process):
    for i in range(Process):
        try:
            multiprocessing.Process(target=SpamThread, args=(itemID, Headers, Threads, )).start()
        except:
            pass

if __name__ == "__main__":
    Title("TikShare / github.com/wizz1337 / discord.gg/devcenter")
    Banner()
    try:
        itemID  = ClearURI(Write.Input("Video Link > ", Colors.yellow_to_red, interval=0.0001))
    except:
        dPrint(Colors.yellow_to_red, "Please put a valid video link : <https://www.tiktok.com/@user/video/000000>")

    try:
        NThread = int(Write.Input("Thread Amount > ", Colors.yellow_to_red, interval=0.0001))
    except:
        dPrint(Colors.yellow_to_red, "Please put a value")
    
    Process = int(cpu_count) / 2
    dPrint(Colors.yellow_to_red, f"Using {str(Process)}")

    dPrint(Colors.yellow_to_red, "Amount is inf !")

    Headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0"
    }
    Banner()

    SpamThread(itemID, Headers, NThread)

