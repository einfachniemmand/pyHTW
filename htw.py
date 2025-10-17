import requests
import getpass
from bs4 import BeautifulSoup
import sys
import re
import webbrowser
import atexit
import os
import tempfile
print("\033[32m           — — developed by bennosaurusrex — — \033[0m")
print(r"""
 _   _            _      _____ _           __        __   _     
| | | | __ _  ___| | __ |_   _| |__   ___  \ \      / /__| |__
| |_| |/ _` |/ __| |/ /   | | | '_ \ / _ \  \ \ /\ / / _ \ '_ \
|  _  | (_| | (__|   <    | | | | | |  __/   \ V  V /  __/ |_) |
|_| |_|\__,_|\___|_|\_\   |_| |_| |_|\___|    \_/\_/ \___|_.__/
""")
print("Please log in or register with your HTW credentials.")
def main():
    while True:
        usr = input("\n  Username: ")
        userexists = requests.get(f"https://hack.arrrg.de/check/{usr}")
        if userexists.text=="²bad²":
            pwd = getpass.getpass("  Password: ")
            url = "https://hack.arrrg.de/login"
            session = requests.Session()
            response = session.post(url, data={"username": usr, "password": pwd})
            print(f"\n🆗 Server responded with final status code {response.status_code}")
            if response.url == "https://hack.arrrg.de/map":
                print(f"✅ Logged in successfully as '{usr}'")
                return session, usr
        elif len(usr)>2:
            if input("  Do you want to create a new account? [yes|no]: ").strip().lower() in ("yes","y"):
                print("  Please review the privacy policy: https://hack.arrrg.de/privacy")
                pwd = getpass.getpass("  Please enter a password you will remember: ")
                if getpass.getpass("  Repeat the password: ") == pwd:
                    session = requests.Session();
                    form = session.get("https://hack.arrrg.de/register")
                    print(f"🆗 CRSF Form Website request finally returned {form.status_code}")
                    soup = BeautifulSoup(form.text, "html.parser")
                    crsf = soup.select_one('input[type="hidden"]').get("value")
                    if not crsf:
                        crsf = ""
                        print("⚠️ Could not fetch CSRF. Continue without.")
                    r = session.post("https://hack.arrrg.de/register", data={"username": usr, "pw1":pwd, "pw2":pwd, "csrf":crsf, "room":""})
                    print(f"🆗 Registration request finally returned {r.status_code}")
                    print(f"✅ Tried creating user '{usr}' with CSRF Token '{crsf}'.")
                    check = session.get("https://hack.arrrg.de/map")
                    if check.url!="https://hack.arrrg.de/map":
                        print("❌ An error occured. Please start over")
                    else:
                        return session, usr
                print("❌ The passwords did not match. Please start over")
        if input("⚠️ Credentials incorrect.\n  Try again? [yes|no]: ").strip().lower() not in ("y", "yes"):
            print("Aborting.")
            sys.exit(1)

def pnl(session, usr):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(r"""
 _  _         _     _____ _         __      __   _    
| || |__ _ __| |__ |_   _| |_  ___  \ \    / /__| |__ 
| __ / _` / _| / /   | | | ' \/ -_)  \ \/\/ / -_) '_ \
|_||_\__,_\__|_\_\   |_| |_||_\___|   \_/\_/\___|_.__/                                   
PROOVE YOUR SKILL""")
        print("\nSelect one of the following actions.")
        action = input("  [exit|logout|export|delete|stats|wechall|changepwd|challengelist|loadchallenge]: ").strip().lower()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(r"""
 _  _         _     _____ _         __      __   _    
| || |__ _ __| |__ |_   _| |_  ___  \ \    / /__| |__ 
| __ / _` / _| / /   | | | ' \/ -_)  \ \/\/ / -_) '_ \
|_||_\__,_\__|_\_\   |_| |_||_\___|   \_/\_/\___|_.__/                                   
htw/"""+action)
        if action=="loadchallenge":
            print("ℹ️ Use challengelist to get all available challengeIDs\n")
            chal = input("  Enter a challengeID: ").strip()
            r = session.get("https://hack.arrrg.de/map")
            print(f"\n🆗 Map request finally returned {r.status_code}")
            soup = BeautifulSoup(r.text, "html.parser")
            needle = f"/challenge/{chal}"
            target = None
            for a in soup.find_all("a", class_="no-underline"):
                href = a.get("href") or ""
                if needle == href or href.endswith(needle):
                    target = a
                    break
            if target:
                print(target)
                print(f"🔄️ Loading challenge {chal}: {target.get_text(' ', strip=True)}")
                chalCode = session.get(f"https://hack.arrrg.de/challenge/{chal}")
                print(f"🆗 Challenge finally returned {chalCode.status_code}")            
                soup = BeautifulSoup(chalCode.text, "html.parser")
                solvedCount = "Not solved yet";
                if soup.select(".container > p:nth-child(5) > span:nth-child(3)"):
                    solvedCount=soup.select(".container > p:nth-child(5) > span:nth-child(3)")[0].get_text().strip()
                html_content = r"""
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Gudea:ital,wght@0,400;0,700;1,400&display=swap');
                    *:not(.story-container,.story-container *,#chat-container,#chat-container *, body, html, .container, h2) {
                        display:none !important
                    }
                    .container {
                        padding-top:50px;
                        padding-bottom:75px;
                    }
                    img {
                        border-radius:5px;
                    }
                </style>
                <script>
                    setInterval(()=>{
                        fetch(location.href)
                        .then(res=>{if(res.status=="404"){window.close()}}).catch(error=>{window.close()})
                    },500)
                </script>
                """+str(soup);
                # Add prefixes to all urls
                soup_abs = BeautifulSoup(html_content, "html.parser")
                for tag in soup_abs.find_all(True):
                    for attr, val in list(tag.attrs.items()):
                        if isinstance(val, str):
                            if val.startswith("/"):
                                tag[attr] = "https://hack.arrrg.de" + val
                            else:
                                tag[attr] = re.sub(r'url\(\s*/(?!/)', r'url(https://hack.arrrg.de/', val)
                        elif isinstance(val, list):
                            new_vals = []
                            for item in val:
                                if isinstance(item, str) and item.startswith("/"):
                                    new_vals.append("https://hack.arrrg.de" + item)
                                else:
                                    new_vals.append(item)
                            tag[attr] = new_vals
                html_content = str(soup_abs)
                html_content = re.sub(r'(?<=["\'])/(?!/)', "https://hack.arrrg.de/", html_content)
                html_content = re.sub(r'url\(\s*/(?!/)', r'url(https://hack.arrrg.de/', html_content)

                with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as tmp:
                    tmp.write(html_content)
                    tmp_path = tmp.name
                webbrowser.open('file://' + os.path.abspath(tmp_path))
                atexit.register(lambda: os.remove(tmp_path))
                os.system('cls' if os.name == 'nt' else 'clear')
                print(r"""
 _  _         _     _____ _         __      __   _    
| || |__ _ __| |__ |_   _| |_  ___  \ \    / /__| |__ 
| __ / _` / _| / /   | | | ' \/ -_)  \ \/\/ / -_) '_ \
|_||_\__,_\__|_\_\   |_| |_||_\___|   \_/\_/\___|_.__/                                   
HTW/CHALLENGES/"""+chal)
                print(f"\033[90m{solvedCount} • \033[3mThe challenge has been opened in another window.\033[0m\033[0m")
                while True:
                    sol = input("\nEnter solution or 'quit' to abort: ").strip()
                    if sol.lower() in ("quit", "q", "exit"):
                        print("✅ Abort")
                        break
                    r = session.post(f"https://hack.arrrg.de/challenge/{chal}", data={"answer": sol})
                    soup = BeautifulSoup(r.text, "html.parser")
                    if soup.select("p.text-danger strong:not(p.status *)"):
                        print(f"\033[31m{sol} is not correct. ({r.status_code})\033[0m")
                        continue
                    elif soup.select("p.text-primary strong:not(p.status *)"):
                        print(f"\033[32m{sol} is correct. ({r.status_code})\033[0m")
                        break
                    else:
                        print(f"⚠️ No definitive result detected. Try again or type 'quit' to abort. ({r.status_code})")
                    os.remove(tmp_path)
            else:
                print(f"⚠️ You either have not unlocked challenge #{chal} yet or it does not exist")
        if action=="challengelist":
            r = session.get("https://hack.arrrg.de/map")
            print(f"\n🆗 Map request finally returned {r.status_code}")
            soup = BeautifulSoup(r.text, "html.parser")
            chals = soup.find_all("a", class_="no-underline")
            print(f"🆗 Found {len(chals)} challenges on the map\n")
            if not chals:
                print("⚠️ No challenges found")
            else:
                print("Listing available challenges:")
                entries = []
                for a in chals:
                    title = a.get_text(" ", strip=True)
                    href = a.get("href") or ""
                    entries.append(f"{title} (#{href.replace('/challenge/', '')})")
                print(f"\033[90m{str(", ".join(entries))}\033[0m")
                matches = []
                for a in chals:
                    circle = a.find("circle")
                    if not circle:
                        continue
                    fill = (circle.get("fill") or "").strip().lower()
                    if fill != "#666699":
                        matches.append(a)

                print(f"\nListing {len(matches)} unsolved challenges:")
                if not matches:
                    print("\033[3mYou're done for now. 😊\033[0m")
                else:
                    for a in matches:
                        href = a.get("href") or ""
                        title = a.get_text(" ", strip=True)
                        print(f"\033[90m - {title} (#{href.replace('/challenge/', '')})\033[0m")
                print("\nUse loadchallenge for further details.")
        if action=="delete":
            print(f"\n⚠️ This will terminate the account of '{usr}' permanently")
            if input("  Continue? [yes|no]: ") in ("y","yes"):
                form = session.get("https://hack.arrrg.de/delete")
                print(f"🆗 CRSF Form Website request finally returned {form.status_code}")
                if form.url == "https://hack.arrrg.de/delete":
                    soup = BeautifulSoup(form.text, "html.parser")
                    crsf = soup.select_one('input[type="hidden"]').get("value")
                else:
                    print("❌ Cannot access the deletion changing form. This request will fail. Continue anyways.")
                if not crsf:
                    crsf = ""
                    print("⚠️ Could not fetch CSRF. Continue without.")
                r = session.post("https://hack.arrrg.de/delete", data={"confirmation": usr, "csrf":crsf})
                print(f"🆗 Deletion request finally returned {r.status_code}")
                print(f"✅ Tried deleting user '{usr}' with CSRF Token '{crsf}'.")
            else:
                "\n✅ Abort."
        if action=="changepwd":
            v=True
            w=False
            if input("\n  Hide passwords? [yes|no]: ").strip().lower() in ("y","yes"):
                current = getpass.getpass("  Enter current password: ")
                new = getpass.getpass("  Enter new password: ")
                if getpass.getpass("  Repeat new password: ") != new:
                    print("⚠️ The new password did not match")
                    v=False
            else:
                current = input("  Enter current password: ")
                new = input("  Enter new password: ")
            if len(new)<5:
                print("⚠️ The new password must exceed 4 characters.")
                v=False
            if input(f"\nDo you really want to change the password of '{usr}'?\n  [yes|no]: ").strip().lower() not in ("y","yes"):
                print("\n✅ Abort.")
                v=False
            if v==True:
                initR = requests.post("https://hack.arrrg.de/login", data={"username": usr, "password": current})
                print(f"\n🆗 Login responded with final status code {initR.status_code}")
                if initR.url != "https://hack.arrrg.de/map":
                    print("⚠️ Your password will not be changed due to invalid credentials.")
                    w = True
                form = session.get("https://hack.arrrg.de/changepw")
                print(f"🆗 CRSF Form Website request finally returned {form.status_code}")
                if form.url == "https://hack.arrrg.de/changepw":
                    soup = BeautifulSoup(form.text, "html.parser")
                    crsf = soup.select_one('input[type="hidden"]').get("value")
                else:
                    print("❌ Cannot access the password changing form. This request will fail. Continue anyways.")
                    w = True

                if not crsf:
                    crsf = ""
                    print("⚠️ Could'nt fetch CSRF. Continue without.")
                    w = True
                r = session.post("https://hack.arrrg.de/changepw", data={"pw": current, "newpw1": new, "newpw2":new, "csrf":crsf})
                print(f"🆗 Password changing request finally returned {r.status_code}")
                print(f"✅ Tried changing Password for user '{usr}' with CSRF Token '{crsf}'. To check, relogin.")
                pwdAction = input("\nSelect one of the following actions.\n  [curpwd,oldpwd,finish,reverse]: ").strip().lower()
                if pwdAction=="curpwd":
                    if w==True:
                        print("❌ This Password has been submitted by you and is probably not correct anymore:")
                    print(f"\nThe current password is: {new}")
                if pwdAction=="oldpwd":
                    if w==True:
                        print("❌ This Password has been submitted by you and is probably not correct anymore:")
                    print(f"\nThe old password is: {current}")
                if pwdAction=="reverse":
                    if w==True:
                        print("❌ Cannot reverse.")
                    else:
                        r = session.post("https://hack.arrrg.de/changepw", data={"pw": new, "newpw1": current, "newpw2":current, "csrf":crsf})
                        print(f"\n🆗 Password changing request finally returned {r.status_code}")
                        print(f"✅ Tried changing back password for user '{usr}' with CSRF Token '{crsf}'. To check, relogin.")
        if action=="exit":
            print("ℹ️ To log out properly before exiting, use 'logout'.")
            print("✅ Exiting.")
            exit()
        if action=="export":
            r = session.get("https://hack.arrrg.de/export-data")
            print(f"🆗 Data request finally returned {r.status_code}")
            print(f"\033[90m \n{r.text}\033[0m")
        if action=="stats":
            r = session.get("https://hack.arrrg.de/profile")
            print(f"🆗 Data request finally returned {r.status_code}")
            soup = BeautifulSoup(r.text, "html.parser")
            print(soup.select_one(".container > p:nth-child(9)").text)
            print(soup.select_one(".container > p:nth-child(10)").text)
            print(soup.select_one(".container > p:nth-child(11)").text)
            print(soup.select_one(".container > p:nth-child(12)").text)
            print(soup.select_one(".container > p:nth-child(13)").text)
            elem14 = soup.select_one(".container > p:nth-child(14)")
            if elem14:
                txt14 = elem14.text.strip()
                if "wechall" not in txt14.lower():
                    print(txt14)
                    elem15 = soup.select_one(".container > p:nth-child(15)")
                    if elem15:
                        print(elem15.text)
            else:
                elem15 = soup.select_one(".container > p:nth-child(15)")
                if elem15:
                    print(elem15.text)
        def logout():
            r = session.get("https://hack.arrrg.de/logout")
            print(f"\n🆗 Logout finally returned {r.status_code}\n")
            print("Please log in with your HTW credentials.")
            python = sys.executable
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\033[3;31mPlease log in again or close this window.\033[0m")
            os.execv(python, [python] + sys.argv)
        if action=="logout":
            logout()

        if action=="wechall":
            r = session.get("https://hack.arrrg.de/profile")
            print(f"\n🆗 Data request finally returned {r.status_code}")
            soup = BeautifulSoup(r.text, "html.parser")
            container = soup.select_one(".container")
            token = None
            if container:
                for idx, child in enumerate(container.find_all(recursive=False), start=1):
                    if child.name != "p":
                        continue
                    if idx < 10:
                        continue
                    a = child.find("a", href=lambda h: h and "wechall" in h.lower())
                    text = child.get_text(" ", strip=True)
                    if a or "wechall" in text.lower():
                        m = re.search(r'Token:\s*([A-Za-z0-9@._-]+)', text)
                        if m:
                            token = m.group(1)
                        else:
                            m2 = re.search(r'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})', text)
                            if m2:
                                token = m2.group(1)
                        break
            if token:
                print(f"WeChall token: {token}")
            else:
                print("⚠️ WeChall token not found.")
        input("\n\033[90m⌛ Press Enter to continue...\033[0m")
        r = session.get("https://hack.arrrg.de/")
        if r.url!="https://hack.arrrg.de/map":
            logout()
            

if __name__ == "__main__":
    sess, user = main()
    pnl(sess, user)
