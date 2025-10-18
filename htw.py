import requests
import getpass
from bs4 import BeautifulSoup
import sys
import re
import webbrowser
import atexit
import os
import tempfile
import shutil
import random
import json
from wcwidth import wcwidth
xp="?"
print("\033[32m           — — developed by bennosaurusrex — — \033[0m")
print(r""" _   _            _      _____ _           __        __   _     
| | | | __ _  ___| | __ |_   _| |__   ___  \ \      / /__| |__
| |_| |/ _` |/ __| |/ /   | | | '_ \ / _ \  \ \ /\ / / _ \ '_ \
|  _  | (_| | (__|   <    | | | | | |  __/   \ V  V /  __/ |_) |
|_| |_|\__,_|\___|_|\_\   |_| |_| |_|\___|    \_/\_/ \___|_.__/
""")
print("\033[33mIt's highly recommended to use Always On Top.\033[0m")
print("Please log in or register with your HTW credentials.")
def main():
    global xp
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
                xp = getXP(response)
                return session, usr, pwd
        elif len(usr)>2:
            if input("  Do you want to create a new account? [yes|no]: ").strip().lower() in ("yes","y"):
                print("  Please review the privacy policy: https://hack.arrrg.de/privacy")
                pwd = getpass.getpass("  Please enter a password you will remember: ")
                if getpass.getpass("  Repeat the password: ") == pwd:
                    session = requests.Session()
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
                    print(f"\n🆗 Server responded with final status code {check.status_code}")
                    if check.url!="https://hack.arrrg.de/map":
                        print("❌ An error occured. Please start over")
                    else:
                        print(f"✅ Logged in successfully as '{usr}'")
                        xp = getXP(check)
                        return session, usr, pwd
                print("❌ The passwords did not match. Please start over")
        if input("⚠️ Credentials incorrect.\n  Try again? [yes|no]: ").strip().lower() not in ("y", "yes"):
            print("Aborting.")
            sys.exit(1)

def pnl(session, usr, pwd):
    global xp
    template = False
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[90m"+(f"{"\033[33mConnected to template \033[90m| " if template == True else ""}{usr} | {xp}XP".rjust(shutil.get_terminal_size().columns))+"\033[0m")
        print(r""" _  _         _     _____ _         __      __   _    
| || |__ _ __| |__ |_   _| |_  ___  \ \    / /__| |__ 
| __ / _` / _| / /   | | | ' \/ -_)  \ \/\/ / -_) '_ \
|_||_\__,_\__|_\_\   |_| |_||_\___|   \_/\_/\___|_.__/ 
PROOVE YOUR SKILL""")
        print("\nSelect one of the following actions.")
        action = input("  [NEW: autofill|exit|logout|export|delete|reset|stats|wechall|lang|changepwd|list|challenge|template]: ").strip().lower()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[90m"+(f"{"\033[33mConnected to template \033[90m| " if template == True else ""}{usr} | {xp}XP".rjust(shutil.get_terminal_size().columns))+"\033[0m")
        print(r""" _  _         _     _____ _         __      __   _    
| || |__ _ __| |__ |_   _| |_  ___  \ \    / /__| |__ 
| __ / _` / _| / /   | | | ' \/ -_)  \ \/\/ / -_) '_ \
|_||_\__,_\__|_\_\   |_| |_||_\___|   \_/\_/\___|_.__/ 
htw/"""+action)
        r = session.get("https://hack.arrrg.de/")
        if r.url!="https://hack.arrrg.de/map":
            logout()
        else:
            xp=getXP(r)
        if action=="template":
            print("\nHeads up! You are about to create a template. \nPlease note the following beforehand:\n\n - You are advised to only use it on your own behalf\n - The template will be created as 'htwdata.json'. If this file already exists and cannot be identified as a htw template, it will get deleted.\n - Note, that every solution you enter in this will in this session will be saved in the template.\n - Users have to be on the same level or lower as you to use your template. To reset your level, use reset.")
            if input("\n  Turn templates on? [yes|no]: ") in ("y","yes"):
                template=True
                try:
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    json_path = os.path.join(script_dir, 'htwdata.json')
                    if os.path.exists(json_path):
                        try:
                            with open(json_path, 'r', encoding='utf-8') as jf:
                                existing = json.load(jf)
                            if isinstance(existing, dict) and 'lang' in existing and isinstance(existing['lang'], str):
                                session.cookies.set('htw_language_preference', existing['lang'], domain='hack.arrrg.de')
                                print(f"✅ Templates activated! Language set to {existing['lang']} from {json_path}")
                            else:
                                print("✅ Templates activated! Start by doing your first challenge.")
                        except Exception as e:
                            print(f"✅ Templates activated! Existing template has no valid syntax and will be deleted. \nStart by doing your first challenge.")
                    else:
                        print("✅ Templates activated! Start by doing your first challenge.")
                except Exception:
                    template = True
                    print("✅ Templates activated! Start by doing your first challenge.")

            else:
                template=False
                print("✅ Templates turned off.")
        if action=="lang":
            if template:
                print("❌ You cannot change the language while being connected to a template.")
            else:
                if session.cookies.get('htw_language_preference') == "de":
                    session.cookies.set('htw_language_preference', 'en', domain='hack.arrrg.de')
                else:
                    session.cookies.set('htw_language_preference', 'de', domain='hack.arrrg.de')
            print("\n✅ The HTW language is now set to "+ session.cookies.get('htw_language_preference'))
        if action=="reset":
            if input(f"\nHeads up! You are about to reset your account: '{usr}'.\nPlease note the following beforehand: \n - The content of your account will be permanently terminated. \n - Your local templates are not getting deleted. \n - You will be logged out of all devices but you may log in afterwards. \n - The Developer has no liability of any kind.\n\n  Continue? [yes|no]: ").strip().lower() in ("y","yes"):
                print("🔄️ Deleting contents")
                form = session.get("https://hack.arrrg.de/delete")
                print(f"🆗 CRSF Form Website request finally returned {form.status_code}")
                crsf=""
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
                print(f"⚠️ Logged out")
                print(f"✅ Tried deleting user '{usr}' with CSRF Token '{crsf}'.")
                print("🔄️ Creating log in")
                session = requests.Session()
                print("ℹ️ Reset session")
                form = session.get("https://hack.arrrg.de/register")
                print(f"🆗 CRSF Form Website request finally returned {form.status_code}")
                soup = BeautifulSoup(form.text, "html.parser")
                crsf = soup.select_one('input[type="hidden"]').get("value")
                if not crsf:
                    crsf = ""
                    print("⚠️ Could not fetch CSRF. Continue without.")
                r = session.post("https://hack.arrrg.de/register", data={"username": usr, "pw1":pwd, "pw2":pwd, "csrf":crsf, "room":""})
                print(f"🆗 Credential registration request finally returned {r.status_code}")
                print(f"✅ Tried creating user login '{usr}' with CSRF Token '{crsf}'.")
                check = session.get("https://hack.arrrg.de/map")
                print(f"\n🆗 Server responded with final status code {check.status_code}")
                if check.url!="https://hack.arrrg.de/map":
                    print("❌ An error occured. Please start over")
                else:
                    print(f"✅ Welcome back, '{usr}'!")
            else:
                "✅ Abort."
        if action=="autofill":
            print("\nNEW: Place a JSON htw template named 'htwdata.json' in the same folder as this program to apply the template onto your account.")
            script_dir = os.path.dirname(os.path.abspath(__file__))
            default_path = os.path.join(script_dir, 'htwdata.json')
            path = default_path
            if not os.path.exists(path):
                user_path = input("  JSON path (leave empty to abort): ").strip()
                if not user_path:
                    print("⚠️ No JSON provided. Abort autofill.")
                else:
                    path = user_path
            if path and os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception as e:
                    print(f"⚠️ Failed to read/parse JSON: {e}")
                    data = None
                if data is None:
                    print("⚠️ No data to autofill.")
                else:
                    try:
                        if session.cookies.get('htw_language_preference') != data[next(iter(data))]:
                            print(f"ℹ️ Switched HTW language from {session.cookies.get('htw_language_preference')} to {data[next(iter(data))]}")
                            session.cookies.set('htw_language_preference', data[next(iter(data))], domain='hack.arrrg.de')
                        del data[next(iter(data))]
                    except Exception:
                        pass
                    print(f"\n🆗 Loaded {len(data)} entries from {path}.\n🔄️ Start applying...")
                    completed = 0
                    failed=[]
                    def updateProgress():
                        print(f"{completed}/{len(data)*2} | {round(completed/len(data)*50)}% completed")
                    for k, v in data.items():
                        available = session.get(f"https://hack.arrrg.de{k}")
                        soup = BeautifulSoup(available.text, "html.parser")
                        completed+=1
                        updateProgress()
                        if not (soup.select(f"a[href='/feedback/{k.replace("/challenge/","")}']") or f"a[href='/hint/{k.replace("/challenge/","")}']"):
                            failed.append(f" - {soup.select_one("h2").get_text()} (#{k.replace("/challenge/","")}) - 403")
                            completed+=1
                            updateProgress()
                            continue
                        if k.replace("/challenge/","")=="15":
                            v=usr[::-1]
                            print("ℹ️ Did not use template for 15 (304)")
                        if k.replace("/challenge/","")=="118":
                            r = session.post(f"https://hack.arrrg.de{k}", data={"q1":"4","q2":"4","q3":"4","q4":"2","good":"-","improve":"-","recommend":"yes","answer": "_",})
                            print("ℹ️ Did not use template for 118 (405)")
                        elif k.replace("/challenge/","") in ("303","338"):
                            results=[]
                            for p in soup.select("div.row p"):
                                span = p.find("span")
                                if span:
                                    expr = span.get_text().replace("=", "")
                                    try:
                                        results.append(str(eval(expr)))
                                    except:
                                        pass
                            sol = results
                            sdata = {f"ans{i}": v for i, v in enumerate(sol)}
                            sdata["answer"] = "ok"
                            print("ℹ️ Did not use template for "+k.replace("/challenge/","")+" (405)")
                            r = session.post(f"https://hack.arrrg.de{k}", data=sdata)
                        else:
                            r = session.post(f"https://hack.arrrg.de{k}", data={"answer": v})
                        soup = BeautifulSoup(r.text, "html.parser")
                        completed+=1
                        updateProgress()
                        if soup.select("p.text-danger strong:not(p.status *)"):
                            failed.append(f" - {soup.select_one("h2").get_text()} (#{k.replace("/challenge/","")}) - 406")
                            continue
                        elif not soup.select("p.text-primary strong:not(p.status *)"):
                            failed.append(f" - {soup.select_one("h2").get_text()} (#{k.replace("/challenge/","")}) - 422")
                            continue
                    print(f"\n✅ Finish applying {len(data)} entries with {len(failed)} failure(s):")
                    print("\n".join(failed))
                    if len(failed) == 0:
                        print("You can try running this again to reduce failures if the list was not properly sorted.")
                    

        if action=="challenge":
            print("ℹ️ Use list to get all available challengeIDs\n")
            chal = input("  Enter a challengeID (leave empty for unfinished challenge): ").strip()
            # Allow immediate quit from the challenge prompt
            if chal.lower() in ("quit", "q", "exit"):
                print("✅ Abort")
                continue
            random_mode = (chal == "")
            while True:
                r = session.get("https://hack.arrrg.de/map")
                print(f"\n🆗 Map request finally returned {r.status_code}")
                soup = BeautifulSoup(r.text, "html.parser")
                target = None
                if random_mode:
                    candidates = []
                    for a in soup.find_all("a", class_="no-underline"):
                        circle = a.find("circle")
                        if not circle:
                            continue
                        fill = (circle.get("fill") or "").strip().lower()
                        # unfinished/available challenges are those not greyed out
                        if fill != "#666699":
                            candidates.append(a)
                    if not candidates:
                        print("\n\033[3mYou're done for now. No unfinished challenges left.\033[0m")
                        break
                    target = random.choice(candidates)
                    href = (target.get("href") or "").strip().replace("/challenge/", "")
                    m = re.search(r'/challenge/([^/]+)$', href)
                    if m:
                        chal = m.group(1)
                    else:
                        chal = href.strip("/")
                else:
                    needle = f"/challenge/{chal}"
                    for a in soup.find_all("a", class_="no-underline"):
                        href = a.get("href") or ""
                        if needle == href or href.endswith(needle):
                            target = a
                            break

                if not target:
                    print(f"⚠️ You either have not unlocked challenge #{chal} yet or it does not exist")
                    break

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
                    p.status, .page-header, .container > p:nth-child(5), #challenge_form, small a, .container > div:nth-child(6), .container > div:nth-child(7) {
                        display:none !important
                    }
                    .container {
                        padding-top:50px;
                        padding-bottom:0px;
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
                r = session.get("https://hack.arrrg.de/")
                if r.url!="https://hack.arrrg.de/map":
                    logout()
                else:
                    xp=getXP(r)
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\033[90m"+(f"{"\033[33mConnected to template \033[90m| " if template == True else ""}{usr} | {xp}XP".rjust(shutil.get_terminal_size().columns))+"\033[0m")
                print(r""" _  _         _     _____ _         __      __   _    
| || |__ _ __| |__ |_   _| |_  ___  \ \    / /__| |__ 
| __ / _` / _| / /   | | | ' \/ -_)  \ \/\/ / -_) '_ \
|_||_\__,_\__|_\_\   |_| |_||_\___|   \_/\_/\___|_.__/ 
HTW/CHALLENGES/"""+chal+" - "+soup_abs.select_one("h2").get_text())
                print(f"\033[90m{solvedCount} • \033[3mThe challenge has been opened in another window.\033[0m\033[0m")
                while True:
                    if chal in ("300","118","303","338","328"):
                        print("⚠️ Leave the field free below to solve it automatically.")
                    sol = input("\nEnter solution or 'quit' to abort and 'skip' to skip: ").strip()
                    if sol.lower() in ("skip", "s"):
                        if random_mode:
                            print("➡️ Skipping to next unfinished challenge...")
                            break
                        else:
                            print("⚠️ 'skip' only valid in random mode. Use empty challenge ID to enable random mode.")
                            continue

                    if sol=="" and chal in ("300","118","328"):
                        print("\n🔄️ Solving this task automatically...")
                        if chal == "300":
                            sol="htw4ever"
                        if chal == "328":
                            sol="community_archiv_freischalten"
                    if sol.lower() in ("quit", "q", "exit"):
                        print("✅ Abort")
                        random_mode = False
                        break
                    results=[]
                    if sol=="" and chal in ("303","338"):
                        for p in soup_abs.select("div.row p"):
                            span = p.find("span")
                            if span:
                                expr = span.get_text().replace("=", "")
                                try:
                                    results.append(str(eval(expr)))
                                except:
                                    pass
                    if sol=="" and chal == "118":
                        r = session.post(f"https://hack.arrrg.de/challenge/{chal}", data={"q1":"4","q2":"4","q3":"4","q4":"2","good":"-","improve":"-","recommend":"yes","answer": "_",})
                    elif sol=="" and chal in ("303","338"):
                        data = {f"ans{i}": v for i, v in enumerate(results)}
                        data["answer"] = "ok"
                        r = session.post(f"https://hack.arrrg.de/challenge/{chal}", data=data)
                        print(r.text)
                    else:
                        r = session.post(f"https://hack.arrrg.de/challenge/{chal}", data={"answer": sol})
                    soup = BeautifulSoup(r.text, "html.parser")
                    if soup.select_one("p.text-danger strong:not(p.status *)"):
                        print(f"\033[31m{soup.select_one("p.text-danger strong:not(p.status *)").get_text().split()[0]} is not correct. ({r.status_code})\033[0m")
                        continue
                    elif soup.select_one("p.text-primary strong:not(p.status *)"):
                        print(f"\033[32m{soup.select_one("p.text-primary strong:not(p.status *)").get_text().split()[0]} is correct. ({r.status_code})\033[0m")
                        if template:
                            try:
                                script_dir = os.path.dirname(os.path.abspath(__file__))
                                json_path = os.path.join(script_dir, 'htwdata.json')
                                lang = session.cookies.get('htw_language_preference')
                                data = None
                                if os.path.exists(json_path):
                                    try:
                                        with open(json_path, 'r', encoding='utf-8') as jf:
                                            data = json.load(jf)
                                        if not isinstance(data, dict) or 'lang' not in data:
                                            data = {'lang': lang}
                                    except Exception:
                                        data = {'lang': lang}
                                else:
                                    data = {'lang': lang}

                                key = f"/challenge/{chal}"
                                if key in data:
                                    try:
                                        del data[key]
                                    except Exception:
                                        pass
                                data[key] = sol
                                with open(json_path, 'w', encoding='utf-8') as jf:
                                    json.dump(data, jf, ensure_ascii=False, indent=4)
                                print(f"✅ Saved solved challenge to template")
                            except Exception as e:
                                print(f"⚠️ Failed saving template: {e}")
                        if random_mode:
                            break
                        else:
                            random_mode = False
                            break
                    else:
                        print(f"⚠️ No definitive result detected. Try again or type 'quit' to abort. ({r.status_code})")
                os.remove(tmp_path)
                if random_mode:
                    continue
                else:
                    break
        if action=="list":
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
                print("\nUse challenge for further details.")
        if action=="delete":
            print(f"\n⚠️ This will terminate the account of '{usr}' permanently. The Developer has no liability of any kind.")
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
            print(f"\n🆗 Data request finally returned {r.status_code}")
            print(f"\033[90m \n{r.text}\033[0m")
        if action=="stats":
            r = session.get("https://hack.arrrg.de/profile")
            print(f"\n🆗 Data request finally returned {r.status_code}\n")
            soup = BeautifulSoup(r.text, "html.parser")
            print("  "+soup.select_one(".container > p:nth-child(9)").text)
            print("  "+soup.select_one(".container > p:nth-child(10)").text)
            print("  "+soup.select_one(".container > p:nth-child(11)").text)
            print("  "+soup.select_one(".container > p:nth-child(12)").text)
            print("  "+soup.select_one(".container > p:nth-child(13)").text)
            elem14 = soup.select_one(".container > p:nth-child(14)")
            if elem14:
                txt14 = elem14.text.strip()
                if "wechall" not in txt14.lower():
                    print(txt14)
                    elem15 = soup.select_one(".container > p:nth-child(15)")
                    if elem15:
                        print("  "+elem15.text)
            else:
                elem15 = soup.select_one(".container > p:nth-child(15)")
                if elem15:
                    print("  "+elem15.text)
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
            print(f"\n🆗 Data request finally returned {r.status_code}\n")
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
                print(f"  WeChall token: {token}")
            else:
                print("⚠️ WeChall token not found.")
        input("\n\033[90m⌛ Press Enter to continue...\033[0m")
        r = session.get("https://hack.arrrg.de/")
        if r.url!="https://hack.arrrg.de/map":
            logout()
        else:
            xp=getXP(r)
            
def getXP (req):
    if not req.text:
        return "?"
    xpSoup = BeautifulSoup(req.text, "html.parser")
    if xpSoup.select_one("#statusbar-user-score"):
        return xpSoup.select_one("#statusbar-user-score").get_text().strip()
    return "?"

if __name__ == "__main__":
    sess, user, pwd = main()
    pnl(sess, user, pwd)
