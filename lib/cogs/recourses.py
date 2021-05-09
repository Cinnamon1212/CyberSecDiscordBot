import discord, os
from bs4 import BeautifulSoup as soup
from discord.ext import commands
from discord import Embed
from pygicord import Paginator

class recourses(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="OSRecourses", description="OS support and recommendations", aliases=["OS"])
    async def OS(self, ctx):
        pages = []
        main = Embed(title="OS Suggestions and recourses", colour=discord.Colour.red())
        main.set_thumbnail(url="https://www.howtogeek.com/wp-content/uploads/2018/08/img_5b68e80f77e33.png")
        main.add_field(name="```(1) Main page```", value="⠀", inline=False)
        main.add_field(name="```(2) OS Suggestions```", value="⠀", inline=False)
        main.add_field(name="```(3) Linux support```", value="⠀", inline=False)
        main.add_field(name="```(4) Windows support```", value="⠀", inline=False)
        main.add_field(name="```(5) Mac OS support```", value="⠀", inline=False)
        main.add_field(name="```(6) Mobile OS support```", value="⠀", inline=False)
        main.add_field(name="```(7) Fun operating systems```", value="⠀", inline=False)
        main.set_footer(text=f"Please use the 🔢 button to jump to a page (page 1 out of 7)")
        pages.append(main)

        ossuggest = Embed(title="Suggested operating systems", colour=discord.Colour.red())
        ossuggest.add_field(name="[Parrot OS](https://parrotsec.org/)", value="Parrot OS is an incredible OS designed for cyber security and forensics, featuring a huge array of preinstalled tools.", inline=False)
        ossuggest.add_field(name="[Ubuntu](https://ubuntu.com/)", value="Ubuntu is a commonly used day to day Linux distro, knowns for it's elegant design and constant support.", inline=False)
        ossuggest.add_field(name="[Arch Linux](https://archlinux.org/)", value="Arch is a lightweight and flexible Linux distro. Arch prides itself on being as simplistic as possible, allowing the user to build the OS to their liking", inline=False)
        ossuggest.add_field(name="[Windows 10](https://www.microsoft.com/en-gb/software-download/windows10)",
                           value="While windows is heavily critizied for many (somewhat valid) reasons; Windows 10 provides a great, easy to use OS for day to day activities", inline=False)
        ossuggest.add_field(name="[Ubuntu Touch](https://ubports.com/)",
                            value="Ubuntu touch is an open source phone OS, while this is no longer in development, the OS brings the capabilities of your Ubuntu Desktop to your pocket with a satisfying interface", inline=False)
        ossuggest.set_footer(text=f"Please use the 🔢 button to jump to a page (page 2 out of 7)")
        pages.append(ossuggest)

        linux = Embed(title="Linux support", colour=discord.Colour.red())
        linux.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/150px-Tux.svg.png")
        linux.add_field(name="Stackoverflow Linux", value="https://stackoverflow.com/questions/tagged/linux", inline=False)
        linux.add_field(name="Ask ubuntu", value="https://askubuntu.com/", inline=False)
        linux.add_field(name="Debian forums", value="http://forums.debian.net/", inline=False)
        linux.add_field(name="Arch forums", value="https://bbs.archlinux.org/", inline=False)
        linux.add_field(name="Ask Fedora", value="https://ask.fedoraproject.org/", inline=False)
        linux.add_field(name="Kali forums", value="https://forums.kali.org/", inline=False)
        linux.set_footer(text=f"Please use the 🔢 button to jump to a page (page 3 out of 7)")
        pages.append(linux)

        windows = Embed(title="Windows support", colour=discord.Colour.red())
        windows.set_thumbnail(url="http://pngimg.com/uploads/windows_logos/windows_logos_PNG28.png")
        windows.add_field(name="Microsoft answers", value="https://answers.microsoft.com/en-us", inline=False)
        windows.add_field(name="Windows 10 forums", value="https://www.tenforums.com/", inline=False)
        windows.add_field(name="Windows server docs", value="https://docs.microsoft.com/en-us/windows-server/", inline=False)
        windows.add_field(name="Windows server forums", value="https://social.technet.microsoft.com/Forums/windowsserver/en-US/home?category=windowsserver", inline=False)
        windows.set_footer(text=f"Please use the 🔢 button to jump to a page (page 4 out of 7)")
        pages.append(windows)

        macos = Embed(title="Mac OS support", colour=discord.Colour.red())
        macos.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/MacOS_original_logo.svg/1024px-MacOS_original_logo.svg.png")
        macos.add_field(name="Apple Support", value="https://support.apple.com/en-gb/macos", inline=False)
        macos.add_field(name="Mac OS support community", value="https://discussions.apple.com/community/mac_os", inline=False)
        macos.add_field(name="OS X forums", value="https://macosx.com/", inline=False)
        macos.add_field(name="Catalina discussion", value="https://discussions.apple.com/community/mac_os/catalina", inline=False)
        macos.add_field(name="Big Sur discussion", value="https://discussions.apple.com/community/mac_os/big-sur", inline=False)
        macos.add_field(name="Mojave discussion", value="https://discussions.apple.com/community/mac_os/mojave", inline=False)
        macos.set_footer(text=f"Please use the 🔢 button to jump to a page (page 5 out of 7)")
        pages.append(macos)

        mobile = Embed(title="Mobile OS support", colour=discord.Colour.red())
        mobile.set_thumbnail(url="https://appsamurai.com/wp-content/uploads/2017/07/android-and-ios-development.jpg")
        mobile.add_field(name="Android help", value="https://support.google.com/android/?hl=en-GB#topic=7313011", inline=False)
        mobile.add_field(name="Android docs", value="https://developer.android.com/docs", inline=False)
        mobile.add_field(name="Android forums", value="https://androidforums.com/", inline=False)
        mobile.add_field(name="IOS support", value="https://support.apple.com/en-gb/iphone", inline=False)
        mobile.add_field(name="IOS forums", value="https://forums.imore.com/ios/", inline=False)
        mobile.add_field(name="Windows mobile End of support FAQ", value="https://support.microsoft.com/en-us/windows/windows-10-mobile-end-of-support-faq-8c2dd1cf-a571-00f0-0881-bb83926d05c5", inline=False)
        mobile.add_field(name="Windows 10 mobile forums", value="https://social.technet.microsoft.com/Forums/en-US/home?forum=win10itpromobile", inline=False)
        mobile.set_footer(text=f"Please use the 🔢 button to jump to a page (page 6 out of 7)")
        pages.append(mobile)

        funos = Embed(title="Fun operating systems", colour=discord.Colour.red())
        funos.add_field(name="[Temple OS](https://templeos.org/)",
                        value="Temple OS is a well known OS made by Terry A. Davis, a developer who unfortunately died in 2018. The OS is written in `HolyC` and features an 8-bit ASCII display.", inline=False)
        funos.add_field(name="[Windows ME](https://winworldpc.com/product/windows-me/final)",
                        value="Windows ME was designed to be a successor to windows 98. Instead, it was a car crash of constant BSODs and self destructive features such as rebooting removed viruses", inline=False)
        funos.add_field(name="[Java OS](Yet to find)",
                        value="Yet another train wreck of an OS. JavaOS, developed by Sun Microsystems was an OS written in Java, not C. This causes the OS to be excruciatingly slow, constant freezing and impossible multi-tasking.", inline=False)
        funos.add_field(name="[Red Star OS](https://archiveos.org/redstar/)", value="Red star OS/North Korean OS is a Linux based OS developed by KCC featuring a modified version of Firefox called Naenara for browsing 'Kwangmyong'", inline=False)
        funos.set_footer(text=f"Please use the 🔢 button to jump to a page (page 7 out of 7)")
        pages.append(funos)
        paginator = Paginator(pages=pages)
        await paginator.start(ctx)


    @commands.command(name="ProgrammingRecourses", description="Programming support", aliases=["ProgRecourses", "programming"])
    async def ProgRecourses(self, ctx):
        pages = []

        main = Embed(title="Programming Recourses", colour=discord.Colour.red())
        main.add_field(name="```(1) Main```", value="⠀", inline=False)
        main.add_field(name="```(2) Python```", value="⠀", inline=False)
        main.add_field(name="```(3) C Family```", value="⠀", inline=False)
        main.add_field(name="```(4) Java```", value="⠀", inline=False)
        main.add_field(name="```(5) Go ```", value="⠀", inline=False)
        main.add_field(name="```(6) Swift```", value="⠀", inline=False)
        main.add_field(name="```(7) Web development + databases```", value="⠀", inline=False)
        main.set_footer(text=f"Please use the 🔢 button to jump to a page (page 1 out of 6)")
        pages.append(main)

        python = Embed(title="Python Recourses", colour=discord.Colour.red())
        python.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/768px-Python-logo-notext.svg.png")
        python.add_field(name="Python website", value="https://www.python.org/", inline=False)
        python.add_field(name="Learn python", value="https://www.learnpython.org/", inline=False)
        python.add_field(name="W3Schools", value="https://www.w3schools.com/python/default.asp", inline=False)
        python.add_field(name="Violent python", value="[Amazon link](https://www.amazon.co.uk/Violent-Python-Cookbook-Penetration-Engineers/dp/1597499579)", inline=False)
        python.add_field(name="Tensorflow with python", value="[Google play](https://play.google.com/store/books/details?pcampaignid=books_read_action&id=3_rEDwAAQBAJ)", inline=False)
        python.add_field(name="Web apps with python", value="https://realpython.com/python-web-applications/", inline=False)
        python.add_field(name="Discord.py", value="https://discordpy.readthedocs.io/en/latest/index.html#getting-started", inline=False)
        python.set_footer(text=f"Please use the 🔢 button to jump to a page (page 2 out of 6)")
        pages.append(python)

        cfamily = Embed(title="C family recourses", colour=discord.Colour.red())
        cfamily.set_thumbnail(url="https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/106186202/original/838192fff0216caf59ce6571211694c39ed7e328/do-programming-work-of-c-family-language-accurately.jpg")
        cfamily.add_field(name="C family list", value="https://en.wikipedia.org/wiki/List_of_C-family_programming_languages", inline=False)
        cfamily.add_field(name="Learn C", value="https://www.learn-c.org/", inline=False)
        cfamily.add_field(name="Learn C#", value="https://www.learncs.org/", inline=False)
        cfamily.add_field(name="Learn C++", value="https://www.learn-cpp.org/", inline=False)
        cfamily.add_field(name="C board forums", value="https://cboard.cprogramming.com/", inline=False)
        cfamily.set_footer(text=f"Please use the 🔢 button to jump to a page (page 3 out of 6)")
        pages.append(cfamily)

        java = Embed(title="Java recourses", colour=discord.Colour.red())
        java.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Java_programming_language_logo.svg/1200px-Java_programming_language_logo.svg.png")
        java.add_field(name="Java website", value="https://www.java.com/", inline=False)
        java.add_field(name="W3Schools java", value="https://www.w3schools.com/java/", inline=False)
        java.add_field(name="Android apps with Java", value="https://developer.android.com/codelabs/build-your-first-android-app", inline=False)
        java.add_field(name="Java forum", value="https://community.oracle.com/community/java", inline=False)
        java.set_footer(text=f"Please use the 🔢 button to jump to a page (page 4 out of 6)")
        pages.append(java)

        go = Embed(title="Go recourses", colour=discord.Colour.red())
        go.set_thumbnail(url="https://sdtimes.com/wp-content/uploads/2018/02/golang.sh_-490x490.png")
        go.add_field(name="Go lang wiki", value="https://golang.org/doc/articles/wiki/", inline=False)
        go.add_field(name="Go lang forums", value="https://forums.online-go.com/?utm_source=devglan", inline=False)
        go.add_field(name="Learn Go lang", value="https://www.codecademy.com/learn/learn-go", inline=False)
        go.set_footer(text=f"Please use the 🔢 button to jump to a page (page 5 out of 6)")
        pages.append(go)

        web = Embed(title="Web development and databases recourses", colour=discord.Colour.red())
        web.set_thumbnail(url="https://www.pngfind.com/pngs/m/170-1706361_web-development-icon-web-development-logo-png-transparent.png")
        web.add_field(name="W3Schools", value="https://www.w3schools.com/", inline=False)
        web.add_field(name="Learn HTML and CSS", value="https://www.codecademy.com/catalog/language/html-css", inline=False)
        web.add_field(name="Learn PHP", value="https://www.learn-php.org/", inline=False)
        web.add_field(name="Learn JavaScript", value="https://www.learn-js.org/", inline=False)
        web.add_field(name="Learn SQL", value="https://www.codecademy.com/learn/learn-sql", inline=False)
        web.add_field(name="Database implementation", value="https://stackoverflow.com/questions/13177882/implementing-a-database-how-to-get-started", inline=False)
        web.add_field(name="Mongo DB", value="https://www.mongodb.com/", inline=False)
        web.set_footer(text=f"Please use the 🔢 button to jump to a page (page 6 out of 6)")
        pages.append(web)

        paginator = Paginator(pages=pages)
        await paginator.start(ctx)

    @commands.command(name="hackingbasics", description="Useful hacking recourses", aliases=["learnhacking", "hacking", "hbasics"])
    async def hackingrecourses(self, ctx):
        pages = []

        main = Embed(title="Hacking basics", colour=discord.Colour.red())
        main.add_field(name="```(1) Main```", value="⠀", inline=False)
        main.add_field(name="```(2) What is ethical hacking?```", value="⠀", inline=False)
        main.add_field(name="```(3) Stages of penetration testing```", value="⠀", inline=False)
        main.add_field(name="```(4) Do's and Don'ts of a pentest```", value="⠀", inline=False)
        main.add_field(name="```(5) Cyber security jobs ```", value="⠀", inline=False)
        main.add_field(name="```(6) Places you can learn```", value="⠀", inline=False)
        main.set_footer(text=f"Please use the 🔢 button to jump to a page (page 1 out of 6)")
        pages.append(main)

        ethicalhacking = Embed(title="What is ethical hacking?", colour=discord.Colour.red())
        explanation = """
Ethical hacking is when a security expert (often a penetration tester) attempts to gain access to an IT system of which they are permitted to test.
This is done in order to expose potential vulnerabilities in the system so they may be patched before a black hat hacker exploits them.
        """
        ethicalhacking.add_field(name="Explained", value=explanation, inline=False)
        typesofhackers = """
White hat:
    A white hat hacker is something who hacks ethically in order to improve the security of an IT system.

Gray hat:
    A gray hat is someone who sits between a black hat and white hat however often don't have the same malicious intent as a black hat hacker

Black hat:
    A black hat hacker is someone who hacks with malicious intent, often for monetary gain or to cause harm to others.

Note: Only white hat hacking is condone by the bot owner. Please follow your local laws.
        """
        ethicalhacking.add_field(name="Types of hackers", value=typesofhackers, inline=False)
        commonlyusedterms = """
Script kiddie (skid):
    Someone who relies soley on premade scripts with little to no actual knowledge

Hacktivism:
    When hacking is used to spread a message or belief (such as anonymous or Lulzsec)

Footprinting:
    Footprinting is the act of performing passive recon on a target, finding information without actively engaging with the target.

OSINT:
    OSINT (open source intellegence) refers to publicly available information, similar to doxing, it's used to gather information on a target via openly accessible information.

IoT:
    IoT (internet of things) refers to all physical objects on the internet that have embedded software however it's commonly used to refer to non-daily use devices such as sensors, games consoles, printers, etc.
        """
        ethicalhacking.add_field(name="Commonly used terms", value=commonlyusedterms, inline=False)
        ethicalhacking.set_footer(text=f"Please use the 🔢 button to jump to a page (page 2 out of 6)")
        pages.append(ethicalhacking)

        stages = Embed(title="Stages of penetration testing", colour=discord.Colour.red())
        recon = """
Reconnaissance is the first and most important stage of penetration testing. This can be split into two types:

Passive:
    Passive recon is indirectly gathering information on a target without directly interacting with them. This includes:
    Checking social media accounts
    Checking public webistes
    Using publicly available software

Active:
    Active recon involves directly trying to gain information such as services, open ports, domains, etc. Some examples:
    Port scanning
    Web crawling
    Subdomain bruteforcing
        """
        stages.add_field(name="#1 Reconnaissance", value=recon, inline=False)
        scanning = """
Scanning is when an attacker actively scans for further information, types of scans include:
    Network mapping
    Port scanning
    Vulnerability scanning
    Service enumeration
        """
        stages.add_field(name="#2 Scanning", value=scanning, inline=False)
        exploitation = """
Exploitation is the stage where the "hack" happens. While this can be exciting, it can't happen if you skip the two previous steps.
Examples of exploitation:
    Bruteforcing accounts
    Service exploitation
    Web app hacking
    Uploading malware
    Reverse engineering
        """
        stages.add_field(name="#3 Exploitation", value=exploitation, inline=False)
        post = """
So you've finally got some foothold on your target, there's four vital steps you must take:

1) Escalate your privilleges, ideally to a root/admin account
2) Secure a stable backdoor (Usually through SSH or some other secure shell)
3) Gather evidence to use in your report
4) Clear your track (clear logs, migrate process, remove files you've created, timestomp files you've accessed)
        """
        stages.add_field(name="#4 Post exploitation", value=post, inline=False)
        reporting = """
You've completed your job, you now need to report your findings to the target in a format they can use to improve their security.
Include:
Videos/images to evidence your stages
A written explanation in layman terms (the target may not be as tech savvy as you)
Suggested fixes with links to patches or alternative software/hardware
        """
        stages.add_field(name="#5 Reporting", value=reporting, inline=False)
        stages.set_footer(text=f"Please use the 🔢 button to jump to a page (page 3 out of 6)")
        pages.append(stages)

        dosanddonts = Embed(title="Do's and don'ts of pentesting", colour=discord.Colour.red())
        do = """
#1 Get express, preferably written, permission from a target before engaging in a pentest
#2 Clarify and respect boundaries and stay within your given scope
#3 Use mostly self-made tools and manual testing
#4 Attempt more than one method of entry
#5 Give your findings in a clear and precise report
#6 Offer training to the target (and their employees)
        """
        dosanddonts.add_field(name="Do", value=do, inline=False)
        dont = """
#1 Cause damage to an IT system/Physical property of the target (you will be held liable.)
#2 Disrupt their business, this may lead to them losing customers/income
#3 Disclose vulnerabilities without express permission from the target
#4 Steal private information during a pentest for personal use
#5 Access customer accounts/accounts out of the scope
#6 Spread information on the pentest outside of what's agreed with the target
        """
        dosanddonts.add_field(name="Don't", value=dont, inline=False)
        dosanddonts.set_footer(text=f"Please use the 🔢 button to jump to a page (page 4 out of 6)")
        pages.append(dosanddonts)

        jobs = Embed(title="Jobs in cyber security", colour=discord.Colour.red())
        CISO = """
A CISO is typically a mid executive level position who oversees general operations regarding IT security.
They are directly responsible for planning, co-ordinating and directing all IT system security implemntations

Average salary: £117,155 / year (26/3/2021)
        """
        jobs.add_field(name="Chief information security officer (CISO)", value=CISO, inline=False)
        FCA = """
Forensic computer analysts are responsible for investigating IT security related incidents, such as ransomware and phishing attacks.
Average salary: £34,888 (21/2/2021)
        """
        jobs.add_field(name="Forensic computer analyst", value=FCA, inline=False)
        pentester = """
A pentester is someone who uses ethical hacking to expose vulnerabilities in an IT system and help patch them.
Average salary: £54,244 (11/04/2021)
        """
        jobs.add_field(name="Penetration tester", value=pentester, inline=False)
        consultant = """
An IT security consultant is responsible for advising a client on how to protect their organizations' cyber sec objectives.
Average salary: £63,906 (11/04/2021)
        """
        jobs.add_field(name="IT security consultant", value=consultant, inline=False)
        jobs.set_footer(text=f"Please use the 🔢 button to jump to a page (page 5 out of 6)")
        pages.append(jobs)

        learn = Embed(title="Places you can learn", colour=discord.Colour.red())
        learn.add_field(name="Cybrary", value="https://www.cybrary.it/", inline=False)
        learn.add_field(name="Udemy", value="https://www.udemy.com/topic/cyber-security/", inline=False)
        learn.add_field(name="Youtube", value="https://www.youtube.com/results?search_query=cyber+security", inline=False)
        learn.add_field(name="Null Byte", value="https://null-byte.wonderhowto.com/", inline=False)
        learn.add_field(name="Tryhackme", value="https://tryhackme.com/", inline=False)
        learn.set_footer(text=f"Please use the 🔢 button to jump to a page (page 6 out of 6)")
        pages.append(learn)

        paginator = Paginator(pages=pages)
        await paginator.start(ctx)


def setup(client):
    client.add_cog(recourses(client))
