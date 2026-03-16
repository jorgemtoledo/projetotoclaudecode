# Dashboard de Ações Brasileiras

Dashboard interativo para análise técnica e de performance de ações da B3, construído com Streamlit e Plotly.

Ativos monitorados: **PETR4**, **ITUB4** e **VALE3**.

---

## Funcionalidades

### Preço & Indicadores
- Gráfico de candlestick com sobreposição de médias móveis (SMA 20/50/200 e EMA 9/21)
- Bandas de Bollinger
- Volume negociado

### Osciladores
- RSI (14 períodos) com linhas de sobrecompra/sobrevenda
- MACD com histograma de divergência

### Performance
- Retorno acumulado normalizado comparando os três ativos
- Tabela de métricas: retorno total, volatilidade anualizada, Sharpe ratio e drawdown máximo

### Correlação
- Heatmap de correlação entre os retornos diários dos ativos

### Dados
- Tabela com dados brutos (OHLCV + indicadores)
- Exportação em CSV

---

## Instalação

**Pré-requisitos:** Python 3.10 ou superior.

### 1. Clone o repositório

```bash
git clone https://github.com/jorgemtoledo/projetotoclaudecode.git
cd projetotoclaudecode
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Como rodar

```bash
streamlit run app.py
```

O app abre automaticamente em `http://localhost:8501`.

Na primeira execução os dados são baixados do Yahoo Finance e armazenados em cache local (`data/cache/`) por 1 hora. As execuções seguintes carregam do cache.

---

## Estrutura do projeto

```
projetotoclaudecode/
├── app.py                  # Ponto de entrada — orquestra tabs e componentes
├── requirements.txt
├── config/
│   └── settings.py         # Tickers, período, cores e configurações de cache
├── data/
│   ├── fetcher.py          # Download via yfinance + cache Parquet
│   └── cache/              # Arquivos .parquet gerados em runtime
├── analysis/
│   ├── indicators.py       # SMA, EMA, RSI, Bollinger Bands, MACD
│   └── performance.py      # Retornos, volatilidade, Sharpe, drawdown, correlação
└── components/
    ├── sidebar.py          # Controles laterais (seleção de ativo e período)
    ├── charts.py           # Todos os gráficos Plotly
    └── metrics_cards.py    # Linha de KPIs
```

---

## Dependências principais

| Pacote | Versão mínima | Uso |
|---|---|---|
| streamlit | 1.32.0 | Interface web |
| yfinance | 0.2.37 | Dados de mercado |
| pandas | 2.2.0 | Manipulação de dados |
| numpy | 1.26.0 | Cálculos numéricos |
| plotly | 5.20.0 | Gráficos interativos |
| pyarrow | 15.0.0 | Cache em formato Parquet |
