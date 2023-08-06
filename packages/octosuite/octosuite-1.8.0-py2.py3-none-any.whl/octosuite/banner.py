import os
from octosuite import colors
banner = f'''{colors.red}
       ▒█████   ▄████▄  ▄▄▄█████▓ ▒█████    ██████  █    ██  ██▓▄▄▄█████▓▓█████ 
      ▒██▒  ██▒▒██▀ ▀█  ▓  ██▒ ▓▒▒██▒  ██▒▒██    ▒  ██  ▓██▒▓██▒▓  ██▒ ▓▒▓█   ▀ 
      ▒██░  ██▒▒▓█    ▄ ▒ ▓██░ ▒░▒██░  ██▒░ ▓██▄   ▓██  ▒██░▒██▒▒ ▓██░ ▒░▒███   
      ▒██   ██░▒▓▓▄ ▄██▒░ ▓██▓ ░ ▒██   ██░  ▒   ██▒▓▓█  ░██░░██░░ ▓██▓ ░ ▒▓█  ▄ 
      ░ ████▓▒░▒ ▓███▀ ░  ▒██▒ ░ ░ ████▓▒░▒██████▒▒▒█████▓ ░██░  ▒██▒ ░ ░▒████▒
      ░ ▒░▒░▒░ ░ ░▒ ▒  ░  ▒ ░░   ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░▓    ▒ ░░   ░░ ▒░ ░
        ░ ▒ ▒░   ░  ▒       ░      ░ ▒ ▒░ ░ ░▒  ░ ░░░▒░ ░ ░  ▒ ░    ░     ░ ░  ░
      ░ ░ ░ ▒  ░          ░      ░ ░ ░ ▒  ░  ░  ░   ░░░ ░ ░  ▒ {colors.red_bg} v1.8.0 {colors.reset}{colors.red}
          ░ ░  ░ ░                   ░ ░        ░     ░      ░              ░  ░
               ░                              {colors.white}— Advanced Github {colors.red}OSINT{colors.white} Framework{colors.reset}



> {colors.white}Current user: {colors.green}{os.getlogin()}{colors.reset}
> {colors.white}Use {colors.green}help{colors.reset}{colors.white} command for usage{colors.reset}
> {colors.white}Commands are case sensitive{colors.reset}
  {'-'*27}


'''