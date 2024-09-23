# Reconhecimento e Colorização de Dígitos MNIST com CNN

## Introdução
- O objetivo do projeto é criar um modelo para **reconhecimento de dígitos** utilizando a base de dados **MNIST**.
- Após o reconhecimento, os dígitos são coloridos de acordo com a **paridade**:
  - **Números pares** são coloridos em **azul**.
  - **Números ímpares** são coloridos em **vermelho**.

## Estrutura do Projeto

### 1. Treinamento da CNN (Convolutional Neural Network)
- Utilizamos a biblioteca **Keras** para criar e treinar um modelo de CNN.
- A CNN recebe as imagens em **escala de cinza (28x28)**, e passa por várias camadas:
  - **Camadas convolucionais** para extração de características.
  - **Pooling** para redução de dimensionalidade.
  - **Camadas densas** para classificação final.
- O modelo é treinado para reconhecer os dígitos de **0 a 9**.
- Após o treinamento, o modelo atinge uma **acurácia** de cerca de **98%** no conjunto de teste.

### 2. Previsão e Colorização dos Dígitos
- Com o modelo treinado, fazemos a **previsão** do dígito nas imagens de teste.
- Usamos a previsão para determinar se o dígito é **par** ou **ímpar**:
  - Se o número é **par**: colorimos a imagem em **azul**.
  - Se o número é **ímpar**: colorimos a imagem em **vermelho**.
- O processo de colorização é feito aplicando cores nas imagens originais de **escala de cinza**.

### 3. Exibição dos Resultados
- Após colorir as imagens, exibimos alguns exemplos para visualizar o resultado:
  - **Exemplo**: o dígito **2** aparece colorido em **azul**, e o **3** em **vermelho**.

## Conclusão
- Este projeto combina **classificação de imagens** com **operações de colorização**.
- Usamos a CNN para identificar os dígitos e uma lógica simples para colorir os dígitos com base na paridade.
- Esse pipeline pode ser estendido para outras tarefas de visão computacional.

