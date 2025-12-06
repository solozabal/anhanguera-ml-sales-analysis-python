import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Garante que o diretório de assets existe
ASSET_DIR = "assets"
os.makedirs(ASSET_DIR, exist_ok=True)

# Estética global do Seaborn
sns.set_theme(context="notebook", style="whitegrid", palette="pastel", font_scale=1.15)
plt.rcParams.update({'axes.titlesize': 18, 'axes.titleweight': 'bold', 'axes.labelsize': 14, 'xtick.labelsize': 11, 'ytick.labelsize': 11, 'font.family': 'sans-serif', 'figure.facecolor': '#f5f7fa'})

# Parte 1: Criar e popular o banco de dados
print("Parte 1: Criar e popular o banco de dados")
conexao = sqlite3.connect('dados_vendas.db')
cursor = conexao.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas1 (
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    data_venda DATE,
    produto TEXT,
    categoria TEXT,
    valor_venda REAL
)
''')
cursor.execute('''
INSERT INTO vendas1 (data_venda, produto, categoria, valor_venda) VALUES
('2023-01-01', 'Produto A', 'Eletrônicos', 1500.00),
('2023-01-05', 'Produto B', 'Roupas', 350.00),
('2023-02-10', 'Produto C', 'Eletrônicos', 1200.00),
('2023-03-15', 'Produto D', 'Livros', 200.00),
('2023-03-20', 'Produto E', 'Eletrônicos', 800.00),
('2023-04-02', 'Produto F', 'Roupas', 400.00),
('2023-05-05', 'Produto G', 'Livros', 150.00),
('2023-06-10', 'Produto H', 'Eletrônicos', 1000.00),
('2023-07-20', 'Produto I', 'Roupas', 600.00),
('2023-08-25', 'Produto J', 'Eletrônicos', 700.00),
('2023-09-30', 'Produto K', 'Livros', 300.00),
('2023-10-05', 'Produto L', 'Roupas', 450.00),
('2023-11-15', 'Produto M', 'Eletrônicos', 900.00),
('2023-12-20', 'Produto N', 'Livros', 250.00);
''')
conexao.commit()
conexao.close()
print("Parte 1 concluída")

# Parte 2: Carregar dados no Pandas
print("Parte 2: Carregar dados no Pandas")
conexao = sqlite3.connect('dados_vendas.db')
df_vendas = pd.read_sql_query('SELECT * FROM vendas1', conexao)
conexao.close()
print("Primeiras linhas do DataFrame:")
print(df_vendas.head())
print("\nInformações do DataFrame:")
print(df_vendas.info())
print("\nDescrição estatística:")
print(df_vendas.describe())
print("\nValores ausentes por coluna:")
print(df_vendas.isnull().sum())
print("Parte 2 concluída")

# Parte 3: Análises com Pandas
print("Parte 3: Análises com Pandas")
df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'])
df_vendas['mes'] = df_vendas['data_venda'].dt.month
df_vendas['ano'] = df_vendas['data_venda'].dt.year
vendas_por_categoria = df_vendas.groupby('categoria')['valor_venda'].sum().reset_index()
print("\nTotal de vendas por categoria:")
print(vendas_por_categoria)
quantidade_vendas_categoria = df_vendas['categoria'].value_counts().reset_index()
quantidade_vendas_categoria.columns = ['categoria', 'quantidade_vendas']
print("\nQuantidade de vendas por categoria:")
print(quantidade_vendas_categoria)
vendas_por_produto = df_vendas.groupby('produto')['valor_venda'].sum().reset_index()
vendas_por_produto = vendas_por_produto.sort_values(by='valor_venda', ascending=False)
print("\nVendas por produto (ordenado por valor):")
print(vendas_por_produto)
vendas_por_mes = df_vendas.groupby('mes')['valor_venda'].sum().reset_index()
print("\nVendas por mês:")
print(vendas_por_mes)
print("Parte 3 concluída")

# -------- PARTE 4: VISUALIZAÇÕES MELHORADAS --------

# 1. Gráfico de barras - Total de Vendas por Categoria
print("Criando gráfico de barras - Total de Vendas por Categoria")
plt.figure(figsize=(8,6))
ax = sns.barplot(
    x='categoria', y='valor_venda', data=vendas_por_categoria, palette="Set2", edgecolor="black"
)
plt.title('Total Sales by Category', fontsize=18, weight='bold')
plt.xlabel('Category', fontsize=13)
plt.ylabel('Total Sales (R$)', fontsize=13)
for i, v in enumerate(vendas_por_categoria['valor_venda']):
    ax.text(i, v + 30, f'R${v:,.0f}', ha='center', va='bottom', color='dimgrey', fontweight='semibold')
plt.grid(axis='y', alpha=0.2)
plt.tight_layout()
barplot_path = os.path.join(ASSET_DIR, "sales_barplot_example.png")
plt.savefig(barplot_path, bbox_inches='tight', dpi=120)
plt.show()

# 2. Gráfico de pizza - Proporção de Vendas por Categoria
print("Criando gráfico de pizza - Proporção de Vendas por Categoria")
plt.figure(figsize=(8,8))
colors = sns.color_palette("rocket_r", len(vendas_por_categoria))
wedges, texts, autotexts = plt.pie(
    vendas_por_categoria['valor_venda'],
    labels=vendas_por_categoria['categoria'],
    autopct='%1.1f%%',
    colors=colors,
    wedgeprops={'edgecolor':'white'},
    textprops={'fontsize':12}
)
plt.setp(autotexts, size=14, weight='bold', color='white')
plt.title('Sales Distribution by Category', fontsize=17, weight='bold')
plt.tight_layout()
pieplot_path = os.path.join(ASSET_DIR, "sales_pie_example.png")
plt.savefig(pieplot_path, bbox_inches='tight', dpi=120)
plt.show()

# 3. Gráfico de barras - Quantidade de Vendas por Categoria
print("Criando gráfico de barras - Quantidade de Vendas por Categoria")
plt.figure(figsize=(8,6))
ax2 = sns.barplot(
    x='categoria', y='quantidade_vendas', data=quantidade_vendas_categoria, palette="cubehelix", edgecolor="black"
)
plt.title('Quantity of Sales by Category', fontsize=18, weight='bold')
plt.xlabel('Category', fontsize=13)
plt.ylabel('Quantity Sold', fontsize=13)
for i, v in enumerate(quantidade_vendas_categoria['quantidade_vendas']):
    ax2.text(i, v + 0.2, v, ha='center', va='bottom', color='dimgrey', fontweight='semibold')
plt.grid(axis='y', alpha=0.2)
plt.tight_layout()
barplot2_path = os.path.join(ASSET_DIR, "sales_quantity_barplot_example.png")
plt.savefig(barplot2_path, bbox_inches='tight', dpi=120)
plt.show()

# 4. Gráfico de barras - Top 5 Produtos mais Vendidos em Valor
print("Criando gráfico de barras - Top 5 Produtos mais Vendidos em Valor")
top5_produtos = vendas_por_produto.head(5)
plt.figure(figsize=(10,6))
ax3 = sns.barplot(
    x='valor_venda', y='produto', data=top5_produtos, palette="viridis", edgecolor="black"
)
plt.title('Top 5 Products by Sales Value', fontsize=18, weight='bold')
plt.xlabel('Total Sales (R$)', fontsize=13)
plt.ylabel('Product', fontsize=13)
for i, (v, p) in enumerate(zip(top5_produtos['valor_venda'], top5_produtos['produto'])):
    ax3.text(v + 30, i, f'R${v:,.0f}', va='center', ha='left', color='dimgrey', fontweight='semibold')
plt.grid(axis='x', alpha=0.2)
plt.tight_layout()
top5_path = os.path.join(ASSET_DIR, "top_5_products_example.png")
plt.savefig(top5_path, bbox_inches='tight', dpi=120)
plt.show()

# 5. Gráfico de linha - Vendas ao Longo dos Meses
print("Criando gráfico de linha - Vendas ao Longo dos Meses")
plt.figure(figsize=(10,6))
ax4 = sns.lineplot(
    x='mes', y='valor_venda', data=vendas_por_mes, marker='o', color="dodgerblue"
)
for i, v in enumerate(vendas_por_mes['valor_venda']):
    ax4.text(vendas_por_mes['mes'][i], v + 30, f'R${v:,.0f}', ha='center', va='bottom', color='dimgrey', fontweight='semibold', fontsize=11)
plt.title('Monthly Sales Trend', fontsize=18, weight='bold')
plt.xlabel('Month', fontsize=13)
plt.ylabel('Total Sales (R$)', fontsize=13)
plt.xticks(range(1,13))
plt.grid(True, alpha=0.2)
plt.tight_layout()
trend_path = os.path.join(ASSET_DIR, "sales_trend_example.png")
plt.savefig(trend_path, bbox_inches='tight', dpi=120)
plt.show()

# 6. Heatmap - Correlação entre Variáveis Numéricas
print("Criando heatmap - Correlação entre as Variáveis Numéricas")
plt.figure(figsize=(8,6))
corr = df_vendas[['valor_venda', 'mes', 'ano']].corr()
ax5 = sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, cbar=True, square=True, annot_kws={'size':14, 'weight':'bold'})
plt.title('Correlation Among Numeric Variables', fontsize=17, weight='bold')
plt.tight_layout()
heatmap_path = os.path.join(ASSET_DIR, "sales_heatmap_example.png")
plt.savefig(heatmap_path, bbox_inches='tight', dpi=120)
plt.show()

print("Parte 4 concluída")