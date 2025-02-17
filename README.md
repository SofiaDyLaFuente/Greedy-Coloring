# Greedy-Coloring

*Projeto 3 da disciplina Teoria e Aplicação de Grafos (UnB) - 2024.2*
- Professor: Dibio Leandro Borges  
- Aluna: Sofia Dy La Fuente Monteiro  
- Matrícula: 211055530

### Para executar o programa:
Versão do Python: 3.11

#### 1 - Instalar as seguintes bibliotecas:

**NetworkX**  
```bash
pip install networkx
```

**Matplotlib**
```bash
pip install matplotlib
```

**Numpy**
```bash
pip install numpy
```

#### 2 - Executar o código:
Clone o repositório:

```bash
git clone https://github.com/SofiaDyLaFuente/Greedy-Coloring.git
```
Vá até a pasta do projeto:
```bash
cd Greedy-Coloring
```
Execute o programa:
```bash
python Greedy-Coloring.py
```

--------

### Observações importantes

- **Limitações do Algoritmo**: O código não está completamente otimizado. Foi necessário estipular um número máximo de tentativas (500) para que o programa pare caso não encontre uma combinação de jogos válida dentro desse limite. Se isso ocorrer, será necessário rodar o programa novamente.
  
- **Eficiência**: O algoritmo geralmente encontra uma solução entre 10 e 200 tentativas, mas não há garantia de que ele sempre conseguirá em menos tentativas.
