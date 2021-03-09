# Brazilian Financial News
O seguinte projeto apresenta diferentes Web Crawlers para a extração de dados textuais de importantes sites de notícias relacionadas ao mercado financeiro brasileiro.

------

#### *Execução:*

- Python 3.7
- Scrapy

##### - src/crawlers:

- Cada diretório possui um script **main.py** 
  - Infomoney
  - Money-Times
  - Suno
  - Fundamentus
  - B3

- A saída de cada script **main.py** ficara na pasta ***/data*** no mesmo diretório
  - Configurado para extrair as 10 últimas páginas de publicação de cada domínio (editável para coletar notícias mais antigas) 
  - Saída em formato JSON
    - Copiar os dados de saída e utilizar o recurso "Beautify" ou "Tree Viewer" do domínio abaixo
    - [Best JSON Viewer and JSON Beautifier Online (codebeautify.org)](https://codebeautify.org/jsonviewer)
  - Cada site com campos específicos (título, data de publicação, url, categoria e tags)

**- src/EDA:**

- Análise inicial dos dados coletados (Jupyter Notebook)
- Organizados em DataFrames indexados por Data da publicação da notícia

---

