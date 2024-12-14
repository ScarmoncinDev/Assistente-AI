import os
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import openai
import re

# Defina sua chave de API da OpenAI
openai.api_key = 'sua-chave-api-aqui'

# Inicialização do pyttsx3
engine = pyttsx3.init("sapi5")
engine.setProperty('voice', engine.getProperty("voices")[0].id)
engine.setProperty('rate', 150)  # Velocidade da fala
engine.setProperty('volume', 1)  # Volume (0.0 a 1.0)
wikipedia.set_lang("pt")

def speak(audio):
    """Função para fazer o assistente falar"""
    engine.say(audio)
    engine.runAndWait()

def get_command():
    """Função para capturar e reconhecer o comando de voz"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        r.pause_threshold = 1  # Espera para terminar a fala
        audio = r.listen(source)
    try:
        print("Reconhecendo...")
        command = r.recognize_google(audio, language='pt-br')
        print("Usuário falou:", command)
    except Exception as e:
        print(e)
        speak("Não entendi, pode repetir?")
        return ""
    return command.lower()

def query_chatgpt(query):
    """Função para fazer uma pergunta ao ChatGPT e obter a resposta"""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Você pode usar outros modelos, como GPT-4, se disponível.
            prompt=query,
            max_tokens=200,  # Limita a resposta a 200 tokens
            n=1,  # Número de respostas
            stop=None,
            temperature=0.7,  # Determina a criatividade da resposta
        )
        return response.choices[0].text.strip()  # Retorna a resposta gerada
    except Exception as e:
        print(f"Erro ao chamar a API do ChatGPT: {e}")
        speak("Desculpe, houve um erro ao processar sua solicitação.")
        return ""

def search_wikipedia(command):
    """Função para procurar no Wikipedia"""
    command = re.sub(r"procure na|pesquise na", "", command)  # Remove comandos extras
    command = re.sub(r"wikipédia", "", command)  # Remove "wikipédia"
    try:
        results = wikipedia.summary(command, sentences=2)
        speak(f"De acordo com a Wikipédia, {results}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Há múltiplas opções para '{command}'. Tente ser mais específico.")
    except wikipedia.exceptions.HTTPTimeoutError:
        speak("A Wikipédia está demorando para responder. Tente novamente mais tarde.")
    except Exception as e:
        speak("Desculpe, não consegui encontrar o que você procura.")

def open_website(website):
    """Função para abrir sites"""
    speak(f"Abrindo {website}")
    webbrowser.open(website)

def open_calculator():
    """Função para abrir a calculadora"""
    speak("Abrindo a Calculadora")
    os.startfile("C:\\Windows\\System32\\calc.exe")

def main():
    """Função principal para executar o assistente"""
    speak("Assistente Digita foi ativada")
    speak("Como eu posso te ajudar?")

    while True:
        command = get_command()

        if command:
            # Verificação de comandos programados
            if "wikipédia" in command:
                search_wikipedia(command)
            elif "youtube" in command:
                open_website("https://youtube.com")
            elif "google" in command:
                open_website("https://google.com")
            elif "calculadora" in command:
                open_calculator()
            elif "tchau" in command:
                speak("Tchau tchau")
                break  # Saída controlada do loop
            elif "pergunta" in command or "como" in command:
                speak("Consultando a inteligência artificial...")
                response = query_chatgpt(command)  # Faz a pergunta ao ChatGPT
                speak(response)
            else:
                # Se o comando não for reconhecido, o assistente pergunta ao ChatGPT
                speak("Não entendi o comando. Vou perguntar ao ChatGPT...")
                response = query_chatgpt(command)  # Pergunta ao ChatGPT
                speak(response)

if __name__ == "__main__":
    main()
