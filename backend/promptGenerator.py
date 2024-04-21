from openai import OpenAI
import os 

def getResponse(userInput):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    with open('jsonSchema.txt', 'r') as f:
        jsonSchema = f.read()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "Creates a JSON based of the attached schema and change everything to the theme of user input."},
            {"role": "user", "content": userInput},
            {"role": "assistant", "content": jsonSchema},
            ]
    )   
    return response
   
def saveResponse(response, userInput):
    # Save the response
    userInputsanity = sanity_check_string(userInput)
    #  but only the message
    messageContent = response.choices[0].message.content
    fileName = findAvailableFilename(userInputsanity)
    with open(fileName, 'w') as file:
        file.write(messageContent)
    return fileName
def findAvailableFilename(base_name):
    # Check if the path with the name is already exist
    index = 1
    while True:
        file_name = f"{base_name}{index}.json"
        if not os.path.exists(file_name):
            return file_name
        index += 1

def sanity_check_string(input_string):
    # Remove spaces and convert to lowercase
    sanitized_string = input_string.replace(" ", "").lower()
    return sanitized_string

def main():
    # Podemos colocar a main para receber o paramento do userInput, e retornar o path que tá
    userInput = input("Qual tema você quer gerar? ")
    response = getResponse(userInput)
    responseSave = saveResponse(response,userInput)
    return responseSave

if __name__ == "__main__":
    main()
