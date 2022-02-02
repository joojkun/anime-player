# Neste arquivo ficaram as funções do programa, serão exportadas para o código principal
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
import subprocess as s


def scrap_soup(url: str):
    """
    Função que acessa o site e retorna o conteúdo HTML da página para raspagem de dados
    :param url: Página que será acessada
    :return: Conteúdo HTML da página
    """
    # HEADERS
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68'}

    # Request para poder acessar o site
    req = Request(url, headers=headers)
    response = urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    return soup


def search_anime():
    # Perguntando ao usuário qual anime ele deseja assistir
    nome_anime_pesquisa = str(input("Digite o nome do anime que você deseja assistir: "))

    # Pesquisando no site o nome do anime que o usuário escolheu
    site_scrap = scrap_soup(url=f"https://animesonline.cc/search/{'+'.join(nome_anime_pesquisa.split())}")

    # Raspando os dados da pagina após pesquisar o nome do anime
    # Caso não encontre o anime solicitado, o pograma irá pedir para o usuário digitar o nome do anime denovo
    # e tbm oferecerá uma opção para encerrar o programa
    while site_scrap.find('div', {'class': 'no-result animation-2'}) is not None:
        pesquisar_dnovo = str(input(f"{50*'='}\nO anime solicitado não foi encontrado, deseja tentar novamente?"
                                    "\nTentar novamente: Sim/s\nEncerrar: Não/n\nDigite: "))
        if pesquisar_dnovo == 's':
            search_anime()
            return
        else:
            return
    # Caso o programa encontre o anime solicitado pelo usuário
    # Raspando a tag com os animes
    lista_animes_encontrados = site_scrap.find('div', {'class': 'module'})\
        .find_all('div', {'id': 'archive-content'})
    # Guardando os animes em um dicionário
    dict_animes_encontrados = {}
    # Mensagem com o nome dos animes encontrados
    msg_animes_encontrados = f"{50 * '='}\nOs animes encontrados foram:\n"
    for anime in lista_animes_encontrados:
        # Nome do anime
        nome_anime = anime.find('h3').get_text().strip()
        # Link para a lista de episódios do anime
        link_anime = anime.find('h3').find('a').get('href')
        # Adicionando anime do dicionário
        dict_animes_encontrados[nome_anime] = [link_anime]
        # Posição na lista de animes encontrados
        index_anime = list(dict_animes_encontrados.keys()).index(nome_anime) + 1
        msg_animes_encontrados += f"{index_anime} - {anime.find('h3').get_text().strip()}\n"
    # Enviando mensagem com o nome dos animes encontrados
    print(f"{msg_animes_encontrados}{50 * '='}")
    # Perguntando ao usuário qual dos animes encontrados ele deseja assistir
    while True:
        anime_selecionado = str(input("Selecione o anime que deseja assistir digitando o número"
                                      " correspondente aos títulos dos animes a cima"
                                      " (para encerrar o programa digite 'fechar'): "))
        if anime_selecionado == 'fechar':
            return
        else:
            try:
                anime_selecionado = list(dict_animes_encontrados.keys())[int(anime_selecionado)-1]
                print(f"{50 * '='}\nVocê selecionou {anime_selecionado}!\n{50 * '='}")
                time.sleep(1)
                return dict_animes_encontrados[anime_selecionado][0]
            except ValueError:
                print(f"{50 * '='}\nNúmero não correspondente :/, tente mais uma vez...\n{50 * '='}")
                time.sleep(1)
            except IndexError:
                print(f"{50 * '='}\nNúmero não correspondente :/, tente mais uma vez...\n{50 * '='}")
                time.sleep(1)


def search_ep(url_ep):
    # Url em que se encontra o link do arquivo de vídeo
    lista_temp = scrap_soup(url=url_ep).find_all('div', {'class': 'se-c'})
    dict_temp = dict()
    for temporada in lista_temp:
        temp_nome = temporada.find_next('div', {'class': 'se-q'}) \
            .find('span', {'class': 'title'}).get_text().strip()
        eps_lista = temporada.find_next('div', {'class': 'se-a'}).find_all('li')
        dict_temp[temp_nome] = {}
        for episodio in eps_lista:
            nome_ep = episodio.find('div', {'class': 'episodiotitle'}).find('a').get_text()
            link_ep = episodio.find('div', {'class': 'episodiotitle'}).find('a').get('href')
            dict_temp[temp_nome][nome_ep] = link_ep
    # Escolhendo a temporada e o episódio
    while True:
        # Caso o anime possua apenas uma temporada
        if len(dict_temp) > 1:
            temp_escolhida = f"""Temporada  {str(input(f"Selecione uma das"
                                                       f" temporadas (1~{len(dict_temp.keys())}): "))}"""
        else:
            temp_escolhida = 'Temporada  1'
        try:
            ep_escolhido = int(input(f"{50*'='}\nDigite o número do episódio que você deseja assistir"
                                     f" (1~{len(dict_temp[temp_escolhida].keys())}): "))
            ep_escolhido = list(dict_temp[temp_escolhida].keys())[int(ep_escolhido) - 1]
            return dict_temp[temp_escolhida][ep_escolhido]
        except KeyError:
            print(f"{50*'='}\nTemporada não disponível ;-;, tente novamente...\n{50*'='}")
        except ValueError:
            print(f"{50*'='}\nEpisódio não disponível ;-;, tente novamente...\n{50*'='}")
        except IndexError:
            print(f"{50*'='}\nEpisódio não disponível ;-;, tente novamente...\n{50*'='}")
        time.sleep(1)


def select_idioma(url_select_idioma):
    soup = scrap_soup(url=url_select_idioma)
    if soup.find('div', {'id': 'option-2', 'class': 'play-box-iframe fixidtab'}) is None:
        link_player_anime = soup.find('iframe').get('src')
        return link_player_anime
    else:
        idioma_anime = str(input(f"{50*'='}\nSelecione o idioma do anime (Dublado | Legendado): "))
        if idioma_anime.lower() == 'dublado':
            link_player_anime = soup.find('iframe').get('src')
            return link_player_anime
        elif idioma_anime.lower() == 'legendado':
            link_player_anime = soup.find('div', {'id': 'option-2', 'class': 'play-box-iframe fixidtab'}).find(
                'iframe').get('src')
            return link_player_anime
        else:
            pass


def play_anime(url_pn):
    # Encontrando a tag em que está o link do vídeo
    tag_video = scrap_soup(url_pn).find('script', {'type': 'text/javascript'})
    # Extraindo da string encontrada o link
    # Index onde começa o link
    index_inicio = str(tag_video).find('play_url') + 11
    # Index onde termina o link
    index_final = str(tag_video)[index_inicio:].find('"')
    # Link completo
    link_ep = str(tag_video)[index_inicio:index_final + index_inicio]
    # Executando o VLC com o link do episódio encontrado
    s.call(['C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe', link_ep, 'vlc://quit'])


an_select = search_anime()
ep_select = search_ep(an_select)
id_select = select_idioma(ep_select)
play_anime(id_select)
