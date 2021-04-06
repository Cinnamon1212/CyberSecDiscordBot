import discord, os
from bs4 import BeautifulSoup as soup
from discord.ext import commands
from discord import Embed
from pygicord import Paginator

class recourses(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="OSRecourses", description="OS support", aliases=["OS"])
    async def OS(self, ctx):
        pages = []
        main = Embed(title="OS Suggestions and recourses", colour=discord.Colour.random())
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

        ossuggest = Embed(title="Suggested operating systems", colour=discord.Colour.random())
        ossuggest.add_field(name="[Parrot OS](https://parrotsec.org/)", value="Parrot OS is an incredible OS designed for cyber security and forensics, featuring a huge array of preinstalled tools.", inline=False)
        ossuggest.add_field(name="[Ubuntu](https://ubuntu.com/)", value="Ubuntu is a commonly used day to day Linux distro, knowns for it's elegant design and constant support.", inline=False)
        ossuggest.add_field(name="[Arch Linux](https://archlinux.org/)", value="Arch is a lightweight and flexible Linux distro. Arch prides itself on being as simplistic as possible, allowing the user to build the OS to their liking", inline=False)
        ossuggest.add_field(name="[Windows 10](https://www.microsoft.com/en-gb/software-download/windows10)",
                           value="While windows is heavily critizied for many (somewhat valid) reasons; Windows 10 provides a great, easy to use OS for day to day activities", inline=False)
        ossuggest.add_field(name="[Ubuntu Touch](https://ubports.com/)",
                            value="Ubuntu touch is an open source phone OS, while this is no longer in development, the OS brings the capabilities of your Ubuntu Desktop to your pocket with a satisfying interface", inline=False)
        ossuggest.set_footer(text=f"Please use the 🔢 button to jump to a page (page 2 out of 7)")
        pages.append(ossuggest)

        linux = Embed(title="Linux support", colour=discord.Colour.random())
        linux.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/150px-Tux.svg.png")
        linux.add_field(name="Stackoverflow Linux", value="https://stackoverflow.com/questions/tagged/linux", inline=False)
        linux.add_field(name="Ask ubuntu", value="https://askubuntu.com/", inline=False)
        linux.add_field(name="Debian forums", value="http://forums.debian.net/", inline=False)
        linux.add_field(name="Arch forums", value="https://bbs.archlinux.org/", inline=False)
        linux.add_field(name="Ask Fedora", value="https://ask.fedoraproject.org/", inline=False)
        linux.add_field(name="Kali forums", value="https://forums.kali.org/", inline=False)
        linux.set_footer(text=f"Please use the 🔢 button to jump to a page (page 3 out of 7)")
        pages.append(linux)

        windows = Embed(title="Windows support", colour=discord.Colour.random())
        windows.set_thumbnail(url="http://pngimg.com/uploads/windows_logos/windows_logos_PNG28.png")
        windows.add_field(name="Microsoft answers", value="https://answers.microsoft.com/en-us", inline=False)
        windows.add_field(name="Windows 10 forums", value="https://www.tenforums.com/", inline=False)
        windows.add_field(name="Windows server docs", value="https://docs.microsoft.com/en-us/windows-server/", inline=False)
        windows.add_field(name="Windows server forums", value="https://social.technet.microsoft.com/Forums/windowsserver/en-US/home?category=windowsserver", inline=False)
        windows.set_footer(text=f"Please use the 🔢 button to jump to a page (page 4 out of 7)")
        pages.append(windows)

        macos = Embed(title="Mac OS support", colour=discord.Colour.random())
        macos.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/MacOS_original_logo.svg/1024px-MacOS_original_logo.svg.png")
        macos.add_field(name="Apple Support", value="https://support.apple.com/en-gb/macos", inline=False)
        macos.add_field(name="Mac OS support community", value="https://discussions.apple.com/community/mac_os", inline=False)
        macos.add_field(name="OS X forums", value="https://macosx.com/", inline=False)
        macos.add_field(name="Catalina discussion", value="https://discussions.apple.com/community/mac_os/catalina", inline=False)
        macos.add_field(name="Big Sur discussion", value="https://discussions.apple.com/community/mac_os/big-sur", inline=False)
        macos.add_field(name="Mojave discussion", value="https://discussions.apple.com/community/mac_os/mojave", inline=False)
        macos.set_footer(text=f"Please use the 🔢 button to jump to a page (page 5 out of 7)")
        pages.append(macos)

        mobile = Embed(title="Mobile OS support", colour=discord.Colour.random())
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

        funos = Embed(title="Fun operating systems", colour=discord.Colour.random())
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


    @commands.command(name="ProgrammingRecourses")

        
def setup(client):
    client.add_cog(recourses(client))
