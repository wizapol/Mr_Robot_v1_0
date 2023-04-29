import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import git

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print(output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el comando:", e)
        print(e.output.decode('utf-8'))

def main():
    # Cargar el archivo .env
    load_dotenv()

    # Obtener la clave de API de Git
    git_api_key = os.getenv('GIT_API_KEY')
    git_url = os.getenv('GIT_REPOSITORY_URL')

    #utilizar el directorio raiz como carpeta base para el repositorio
    os.chdir(Path(__file__).parent.parent)
    

    #hacemos git init para inicializar el repositorio en visual studio desde la url especificada en el archivo .env
    run_command(f'git init {git_url}')
    
    #error handling para el caso de que no se pueda inicializar el repositorio
    try:
        repo = git.Repo.init(git_url)
    except git.exc.GitCommandError as error:
        print("Error al inicializar el repositorio:", error)
        print(error.output.decode('utf-8'))

    
    
    # Crear un commit con un mensaje
    commit_message = input("Ingresa un mensaje de commit: ")
    run_command(f'git commit -m "{commit_message}"')     

    # Subir los cambios al repositorio remoto utilizando la clave de API
    run_command(f'git push --set-upstream https://{git_api_key}@github.com/wizapol/Mr_Robot.git master')

if __name__ == "__main__":
    main()