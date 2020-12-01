# Brazilian Financial News
O seguinte projeto apresenta diferentes Web Crawlers para a extração de dados textuais de importantes sites relacionados ao mercado financeiro no Brasil.

------

#### *Execução:*

- Python 3.7
- Scrapy

##### - src/crawlers:

- Cada diretório possui um script **main.py** 
  - Infomoney
  - Money-Times
  - Suno

- A saída de cada script **main.py** ficara na pasta ***/data*** no mesmo diretório
  - Saída em formato JSON
    - Copiar os dados de saída e utilizar o recurso "Beautify" ou "Tree Viewer" do domínio abaixo
    - [Best JSON Viewer and JSON Beautifier Online (codebeautify.org)](https://codebeautify.org/jsonviewer)
  - Cada site com campos específicos (título, data de publicação, url, categoria e tags)

**- src/EDA:**

- Análise inicial dos dados coletados (Jupyter Notebook)
- Organizados em DataFrames indexados por Data da publicação da notícia

---

