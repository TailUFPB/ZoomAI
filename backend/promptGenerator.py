from openai import OpenAI
import os 

def getResponse(userInput):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    with open('jsonSchema.txt', 'r') as f:
        jsonSchema = f.read()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "keep the same struct and change everything to the theme of user input."},
            {"role": "assistant", "content": "create 10 new elements on data. By starting with 0, increase the number by 5 each time"},
            {"role": "user", "content": userInput},
            {"role": "assistant", "content": jsonSchema},     
        ] 
            
    )   
    return response
   
def main():
    userInput = input("Qual tema você quer gerar? ")
    response = getResponse(userInput)
    mensagem = response.choices[0].message.content
    print(mensagem)

if __name__ == "__main__":
    main()