import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_page_content(url):
    """Faz a requisição HTTP para a URL e retorna o conteúdo HTML."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro para status de requisição ruim
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return None

def parse_articles(html_content):
    """Parseia o HTML e extrai títulos, links e resumos dos artigos."""
    soup = BeautifulSoup(html_content, 'html.parser')
    articles_data = []

    # Encontrando todos os containers de artigos (ajuste o seletor conforme necessário)
    articles = soup.find_all('div', class_='gs-c-promo')

    for article in articles:
        # Extraindo título
        title_tag = article.find('h3')
        title = title_tag.get_text(strip=True) if title_tag else "Título não encontrado"

        # Extraindo link
        link_tag = article.find('a', href=True)
        link = f"https://www.bbc.com{link_tag['href']}" if link_tag else "Link não encontrado"

        # Extraindo resumo (se existir)
        summary_tag = article.find('p')
        summary = summary_tag.get_text(strip=True) if summary_tag else "Resumo não encontrado"

        articles_data.append({
            'Título': title,
            'Link': link,
            'Resumo': summary
        })

    return articles_data

def save_to_csv(data, filename):
    """Salva os dados extraídos em um arquivo CSV."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Dados salvos em {filename}")

def main():
    url = "https://www.bbc.com/news/technology"
    print("Iniciando web scraper...")

    # Buscar conteúdo da página
    html_content = fetch_page_content(url)
    if not html_content:
        print("Falha ao obter conteúdo da página.")
        return

    # Parsear os artigos da página
    articles_data = parse_articles(html_content)

    # Salvar os dados em um arquivo CSV
    if articles_data:
        save_to_csv(articles_data, 'artigos_tecnologia_bbc.csv')
    else:
        print("Nenhum dado de artigo foi encontrado.")

if __name__ == "__main__":
    main()
