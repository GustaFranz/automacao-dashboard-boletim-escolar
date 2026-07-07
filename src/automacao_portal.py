from pathlib import Path
import time
import webbrowser
import pyautogui
import shutil


# Coordenadas calibradas em monitor 1920x1080, escala Windows 125% (1536x864 lógico),
# Chrome maximizado e zoom do navegador em 100%.
email = "coordenacao@colegiocaminhosfuturo.local"
senha = "Demo@2026"

pasta_projeto = Path(__file__).resolve().parent.parent
portal_login = pasta_projeto / "portal_simulado" / "login.html"
pasta_prints = pasta_projeto / "saidas" / "prints"
pasta_downloads = Path.home() / "Downloads"
pasta_simulados = pasta_projeto / "dados" / "simulados"


def esperar(segundos=2):
    time.sleep(segundos)


def abrir_portal():
    caminho_chrome = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(caminho_chrome))
    webbrowser.get("chrome").open(portal_login.as_uri())
    esperar(3)


def fazer_login():
    pyautogui.click(691, 449)
    pyautogui.write(email)
    esperar(1)
    pyautogui.click(684, 547)
    esperar(1)
    pyautogui.write(senha)
    pyautogui.click(709, 618)
    esperar(2)

def painel_simulado_da_turma(x, y):
    pyautogui.click(x, y)
    esperar(2)

def baixar_csv_turma(p, z):
    pyautogui.click(p, z)
    esperar(2)

def mover_csv_baixado(nome_arquivo):
    origem = pasta_downloads / nome_arquivo
    destino = pasta_simulados / nome_arquivo

    if not origem.exists():
        print(f"Arquivo não encontrado: {origem}")
        return

    if destino.exists():
        destino.unlink()

    shutil.move(origem, destino)
    print(f"Arquivo movido para: {destino}")

def botao_voltar():
    pyautogui.click(29, 88)
    esperar(2)


abrir_portal()
fazer_login()
esperar(2)

painel_simulado_da_turma(351, 459)  # Aba 6º ano
esperar(2)
baixar_csv_turma(349, 407)  # Baixar CSV 6º ano 
esperar(2)
mover_csv_baixado("simulado_6ano.csv")
botao_voltar()

painel_simulado_da_turma(808, 462)  # Aba 7º ano
baixar_csv_turma(349, 407)  # Baixar CSV 7º 
esperar(2)
mover_csv_baixado("simulado_7ano.csv")
botao_voltar()

painel_simulado_da_turma(1268, 459)  # Aba 8º ano
baixar_csv_turma(349, 407)  # Baixar CSV 8º
esperar(2)
mover_csv_baixado("simulado_8ano.csv")


