from openai import OpenAI
import os 

def getResponse(userInput):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    with open('jsonSchema.txt', 'r') as f:
        jsonSchema = f.read()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "using the JSON attached, keeping the same struct and change everything to the theme of user input."},
            {"role": "assistant", "content": "create 10 new elements on data. By starting with 0, increase the number by 5 each time"},
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
    userInput = input("Qual tema você quer gerar? ")
    response = getResponse(userInput)
    print(response)
    responseSave = saveResponse(response,userInput)

if __name__ == "__main__":
    main()