from PIL import Image
import argparse
import requests
import os
import sys
import time
import re

# Scryfall API
def apiFetch(cardName, setCode=None, collectorNumber=None):
    if setCode and collectorNumber:
        url = f"https://api.scryfall.com/cards/{setCode}/{collectorNumber}"
        print(f"\SetCode Fetch")

    else:
        url = f"https://api.scryfall.com/cards/named?exact={cardName}"
        print(f"\nCardname Fetch")

    #API requests that we send requests in a staggered amount, so minimum set at .05
    time.sleep(0.05)

    response = requests.get(url)
    if response.status_code == 200:
        print(f"\nSuccessful Fetch")
        cardData = response.json()
        imageUrl = cardData['image_uris']['large']
        print(f"\nImageURL from APIFetch: {imageUrl}")
        return imageUrl
    else:
        print(f"\nError fetching card data (Status {response.status_code})")
        try:
            errorDetails = response.json()
            print(f"Error Details: {errorDetails}")
        except ValueError:
            print("Unable to parse error response as JSON.")

def downloadCard(imageUrl, outputPath):
    if not imageUrl:
        return   
    imageResponse = requests.get(imageUrl)
    if imageResponse.status_code == 200:
        with open(outputPath, 'wb') as imgFile:
            imgFile.write(imageResponse.content)
        print(f"\nImage saved to '{outputPath}'")
    else:
        print(f"\nError downloading image (Status code {imageResponse.status_code})")
    
def ParsedInput(cardInput):
    #Parsing input to collect the card name separated by a set number in parenthesis or collector number
    pattern = r"^(.*?)(?:\s*\((\w+)\))?\s*(\d+)?$"
    match = re.match(pattern, cardInput.strip())
    if match:
        cardName = match.group(1).strip()
        setCode = match.group(2) if match.group(2) else None
        collectorNumber = match.group(3) if match.group(3) else None
        return cardName, setCode, collectorNumber
    else:
        return cardInput.strip(), None, None  

def main():
    directoryName = "ProxyImageHolder"
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    rootDir = os.path.abspath(os.path.join(scriptDir, directoryName))
    
    #Directory Generation
    try:
        os.mkdir(directoryName)
        print(f"Directory '{directoryName}' created, proxies will be created here.")
    except FileExistsError:
        print(f"Directory '{directoryName}' already exists, feel free to delete the current one and start fresh.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directoryName}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    while True:
        try:
            userInput = input("\nEnter Magic card name: ")
            if not userInput:
                print(f"\nPlease enter a valid card name.")
                continue
            cardName, setCode, collectorNumber = ParsedInput(userInput)
            imageUrl = apiFetch(cardName, setCode, collectorNumber)

            if imageUrl:
                outputPath = os.path.join(rootDir, f"{userInput.replace(' ', '_')}.jpg")
                downloadCard(imageUrl, outputPath)
                print(f"\nYou searched for: {userInput}")    
            
        except EOFError:
            # Exit on Ctrl+C
            print("\nExiting console.")
            break

if __name__ == "__main__":
    main()