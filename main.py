# main.py
import logging
import sys
from discord_rpc.config import Config
from discord_rpc.rpc_client import DiscordRPC
from colorama import init as colorama_init, Fore, Style

colorama_init(autoreset=True)

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.WHITE,
        logging.INFO: Fore.CYAN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, Fore.WHITE)
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"

def print_ascii_art():
    lavendar = "\033[95m"
    reset = "\033[0m"

    ascii = f"""{lavendar}
8888888888                                  8888888b.  8888888b.  8888888b.   .d8888b.  
888                                         888  "Y88b 888   Y88b 888   Y88b d88P  Y88b 
888                                         888    888 888    888 888    888 888    888 
8888888     8888b.  .d8888b  888  888       888    888 888   d88P 888   d88P 888        
888            "88b 88K      888  888       888    888 8888888P"  8888888P"  888        
888        .d888888 "Y8888b. 888  888       888    888 888 T88b   888        888    888 
888        888  888      X88 Y88b 888       888  .d88P 888  T88b  888        Y88b  d88P 
8888888888 "Y888888  88888P'  "Y88888       8888888P"  888   T88b 888         "Y8888P"  
                                  888                                                   
                             Y8b d88P                                                   
                              "Y88P"                                                    
{reset}"""
    print(ascii)

def main():
    print_ascii_art()

    handler = logging.StreamHandler(sys.stdout)
    formatter = ColorFormatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[handler])
    logger = logging.getLogger(__name__)

    try:
        config = Config()
        rpc = DiscordRPC(config)
        rpc.run()
    except Exception as e:
        logger.error("Fatal error in main: %s", e, exc_info=True)

if __name__ == "__main__":
    main()
