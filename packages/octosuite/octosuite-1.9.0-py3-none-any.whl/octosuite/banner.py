import os
from octosuite import colors

version = 'v1.9.0'
banner = f'''{colors.red}
       ▒█████   ▄████▄  ▄▄▄█████▓ ▒█████    ██████  █    ██  ██▓▄▄▄█████▓▓█████ 
      ▒██▒  ██▒▒██▀ ▀█  ▓  ██▒ ▓▒▒██▒  ██▒▒██    ▒  ██  ▓██▒▓██▒▓  ██▒ ▓▒▓█   ▀ 
      ▒██░  ██▒▒▓█    ▄ ▒ ▓██░ ▒░▒██░  ██▒░ ▓██▄   ▓██  ▒██░▒██▒▒ ▓██░ ▒░▒███   
      ▒██   ██░▒▓▓▄ ▄██▒░ ▓██▓ ░ ▒██   ██░  ▒   ██▒▓▓█  ░██░░██░░ ▓██▓ ░ ▒▓█  ▄ 
      ░ ████▓▒░▒ ▓███▀ ░  ▒██▒ ░ ░ ████▓▒░▒██████▒▒▒█████▓ ░██░  ▒██▒ ░ ░▒████▒
      ░ ▒░▒░▒░ ░ ░▒ ▒  ░  ▒ ░░   ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░▓    ▒ ░░   ░░ ▒░ ░
        ░ ▒ ▒░   ░  ▒       ░      ░ ▒ ▒░ ░ ░▒  ░ ░░░▒░ ░ ░  ▒ ░    ░     ░ ░  ░
      ░ ░ ░ ▒  ░          ░      ░ ░ ░ ▒  ░  ░  ░   ░░░ ░ ░  ▒ {colors.red_bg} {version} {colors.reset}{colors.red}
          ░ ░  ░ ░                   ░ ░        ░     ░      ░              ░  ░
               ░                              {colors.white}— Advanced Github {colors.red}OSINT{colors.white} Framework{colors.reset}



> {colors.white}Current user: {colors.green}{os.getlogin()}{colors.reset}
> {colors.white}Use {colors.green}help{colors.reset}{colors.white} command for usage{colors.reset}
> {colors.white}Commands are case sensitive{colors.reset}
  {'-'*27}


'''