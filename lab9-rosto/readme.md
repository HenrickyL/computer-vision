# Roteiro de Leitura: Análise do Código de Detecção de Rostos

## Introdução
Neste código, implementamos e comparamos três métodos de detecção de rostos: Haar Cascade, YOLO e RetinaFace. A detecção de rostos é um campo fundamental da visão computacional, amplamente utilizado em diversas aplicações, como segurança e reconhecimento facial.

## Estrutura do Código

### Importações
- **Bibliotecas**: O código utiliza `cv2` para manipulação de imagens, `numpy` para operações matemáticas, `retinaface` para detecção avançada de rostos e `matplotlib` para visualização.

### Funções de Detecção de Rostos
1. **Haar Cascade**:
   - **Teoria**: Baseado em uma abordagem de aprendizado de máquina que utiliza características em cascata. O modelo é treinado para detectar padrões de rostos em imagens.
   - **Implementação**: A função converte a imagem para escala de cinza e utiliza um classificador pré-treinado para detectar rostos.

2. **YOLO (You Only Look Once)**:
   - **Teoria**: Um método que detecta objetos em tempo real, prevendo múltiplos bounding boxes e suas classes simultaneamente.
   - **Implementação**: A função pré-processa a imagem, passa pelo modelo YOLO e extrai as detecções com confiança acima de um determinado limiar.

3. **RetinaFace**:
   - **Teoria**: Um modelo profundo que utiliza redes neurais para detectar rostos, oferecendo alta precisão e pontos de referência faciais.
   - **Implementação**: A função utiliza a biblioteca RetinaFace para detectar rostos e retorna as coordenadas das áreas faciais.

### Avaliação de Desempenho
Para avaliar a eficácia dos métodos, utilizamos a Interseção sobre União (IoU):
- **IoU**: Mede a sobreposição entre duas caixas delimitadoras. Um IoU mais alto indica que as detecções são mais precisas.
- **Cálculo do IoU**: Para cada detecção de rosto dos métodos Haar Cascade e YOLO, calculamos o IoU em relação às detecções do RetinaFace, que é considerado um benchmark de precisão.

```python
haar_iou = np.mean([calculate_iou(hf, rf) for hf, rf in zip(haar_faces, retina_faces)])
yolo_iou = np.mean([calculate_iou(yf, rf) for yf, rf in zip(yolo_faces, retina_faces)])
