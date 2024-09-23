from zipfile import ZipFile, ZipExtFile
from os import path
from typing import IO
# from xml.etree import ElementTree as ET
from gamuLogger import Logger, LEVELS
from bs4 import BeautifulSoup as BS

Logger.setModule("moddesc")

try:
    from .config import Config
except ImportError:
    from config import Config
    

class ModDesc:
    def __init__(self, file : IO[bytes]):
        self.__soup = BS(file, "xml")
        Logger.deepDebug("Loaded modDesc.xml")
        
    
    @property
    def author(self) -> str:
        return self.__soup.modDesc.author.text
        
        
    @property
    def version(self) -> str:
        return self.__soup.modDesc.version.text
    
    @property
    def title(self) -> str:
        """
        Returns the title of the mod in the main language, or english if the main language is not found, or the first title if english is not found
        """        
        mainLanguage = Config().get("language", "en")
        titles = self.__soup.modDesc.title
        contents = titles.contents
        if "\n" in contents:
            contents.remove("\n")
        for titleElement in contents:
            if titleElement.name == mainLanguage:
                return titleElement.text
        for titleElement in contents:
            if titleElement.name == "en":
                return titleElement.text
        return contents[0].text
    
    @property
    def description(self) -> str:
        """
        Returns the description of the mod in the main language, or english if the main language is not found, or the first description if english is not found
        """        
        mainLanguage = Config().get("language", "en")
        descriptions = self.__soup.modDesc.description
        contents = descriptions.contents
        if "\n" in contents:
            contents.remove("\n")
        for descriptionElement in contents:
            if descriptionElement.name == mainLanguage:
                return descriptionElement.text.strip()
        for descriptionElement in contents:
            if descriptionElement.name == "en":
                return descriptionElement.text.strip()
        return contents[0].text.strip()
        
    @property
    def icon(self) -> str:
        return self.__soup.modDesc.iconFilename.text
    
    @property
    def supportMultiplayer(self) -> bool:
        return self.__soup.modDesc.multiplayer["supported"] == "true"
    
if __name__ == "__main__":
    Logger.setLevel("stdout", LEVELS.DEBUG)
    with open("mods/modDesc.xml", "r") as f:
        modDesc = ModDesc(f)
        print(modDesc.author)
        print(modDesc.version)
        print(modDesc.title)
        print(modDesc.description)
        print(modDesc.icon)
        print(modDesc.supportMultiplayer)