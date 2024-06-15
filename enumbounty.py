import subprocess
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    banner = """
==================================================================================
        .    '      _______________
                ==c(___(o(______(_()
                        \=\
                         )=\
                        //|\\
                       //|| \\
                      // ||  \\
                     //  ||   \\
                    //         \\ By axroot
    ___________                      __________                     __          
    \_   _____/ ____  __ __  _____   \______   \ ____  __ __  _____/  |_ ___.__.
     |    __)_ /    \|  |  \/     \   |    |  _//  _ \|  |  \/    \   __<   |  |
     |        \   |  \  |  /  Y Y  \  |    |   (  <_> )  |  /   |  \  |  \___  |
    /_______  /___|  /____/|__|_|  /  |______  /\____/|____/|___|  /__|  / ____|
            \/     \/            \/          \/                  \/      \/     
==================================================================================    
    """
    print(banner)

def show_menu():
    print("Please choose an option:")
    print("[1] - Check Requirements")
    print("[2] - Start Enumeration")
    print("[3] - About The Tool")
    print("[0] - Exit")

def check_requirements():
    print("\nChecking Requirements...\n")
    requirements = ["subfinder", "httpx-toolkit", "katana", "dirsearch"]
    for req in requirements:
        try:
            result = subprocess.run(f"which {req}", shell=True, check=True, text=True, capture_output=True)
            print(f"{req} is installed: {result.stdout.strip()} ✅")
        except subprocess.CalledProcessError:
            print(f"{req} is not installed. ❌")

def start_enumeration():
    print("\nStarting Enumeration...\n")
    domain = input("Please enter the domain to enumerate (example.com): ")
    
    commands = [
        f"subfinder -d {domain} -all -recursive > subdomain.txt",
        "cat subdomain.txt | httpx-toolkit -ports 80,443,8080,8000,8888 -threads 200 > subdomains_alive.txt",
        "katana -u subdomains_alive.txt -d 5 -ps -pss waybackarchive,commoncrawl,alienvault -kf -jc -fx -ef woff,css,png,svg,jpg,woff2,jpeg,gif,svg -o allurls.txt",
        "cat allurls.txt | grep -E '\\.js$' >> js.txt",
        f"dirsearch -u https://{domain} -e conf,config,bak,backup,swp,old,db,sql,asp,aspx,aspx~,asp~,py,py~,rb,rb~,php,php~,bak,bkp,cache,cgi,conf,csv,html,inc,jar,js,json,jsp,jsp~,lock,log,rar,old,sql,sql.gz,http://sql.zip,sql.tar.gz,sql~,swp,swp~,tar,tar.bz2,tar.gz,txt,wadl,zip,.log,.xml,.js.,.json -o dirsearch.txt"
    ]

    for command in commands:
        print(f"\n[*] Executing command: {command}\n")
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            if result.stdout:
                print(f"Output:\n{result.stdout}")
            if result.stderr:
                print(f"[X] Errors:\n{result.stderr}")
            print(f"[✅]Command completed successfully: {command}\n")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the command ❌:\n{e.stderr}")
            break

def about():
    print("The Enum Bounty tool automates the enumeration process in Bug Bounty programs by performing \na wide variety of enumeration tasks. With Enum Bounty, you can efficiently discover subdomains, \nidentify active services and ports, gather URLs, and locate sensitive files, all in an automated manner.")

def main():
    while True:
        clear_screen()
        display_banner()
        show_menu()
        choice = input("\nEnter your choice -> ")
        
        clear_screen()
        display_banner()

        if choice == '1':
            check_requirements()
        elif choice == '2':
            start_enumeration()
        elif choice == '3':
            about()
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
