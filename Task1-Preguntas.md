# Laboratorio 6

1. **En un juego de suma cero para dos jugadores, ¿cómo funciona el algoritmo
minimax para determinar la estrategia óptima para cada jugador? ¿Puede
explicarnos el concepto de "valor minimax" y su importancia en este
contexto?**
En un juego de suma cero para dos jugadores, el algoritmo minimax funciona
explorando todas las posibles jugadas hasta una profundidad determinada y
evaluando el resultado de cada una de esas jugadas. Para cada jugada, el
algoritmo asume que el oponente jugará de manera óptima, maximizando su
propia ganancia y minimizando la ganancia del jugador actual. El "valor
minimax" es el resultado esperado del juego si ambos jugadores juegan de
manera óptima. En este contexto, determina la mejor jugada para el jugador
actual, maximizando su resultado esperado mientras minimiza el mejor
resultado posible para el oponente.  
  

2. **Compare y contraste el algoritmo minimax con la poda alfa-beta. ¿Cómo
mejora la poda alfa-beta la eficiencia del algoritmo minimax,
particularmente en árboles de caza grandes? Proporcione un ejemplo para
ilustrar la diferencia en la complejidad computacional entre la poda minimax
y alfa-beta.** 
El algoritmo minimax y la poda alfa-beta son algoritmos relacionados para
encontrar la estrategia óptima en juegos de suma cero. La poda alfa-beta
mejora la eficiencia del minimax al eliminar ramas innecesarias en el árbol de
búsqueda. Mientras que el minimax explora todas las ramas posibles, la poda
alfa-beta elimina ramas que no afectarán la elección final de la jugada. Esto se
logra mediante la utilización de dos valores, alfa y beta, que representan el
valor mínimo garantizado para el jugador maximizador y el valor máximo
garantizado para el jugador minimizador, respectivamente. Si se encuentra
una rama que ya no afectará la elección final (es decir, que no cambiará los
valores de alfa o beta), se poda esa rama y se evita su exploración, lo que
reduce significativamente el número de nodos evaluados.  

  
3. **¿Cuál es el papel de expectiminimax en juegos con incertidumbre, como
aquellos que involucran nodos de azar o información oculta? ¿En qué se
diferencia el expectiminimax del minimax en el manejo de resultados
probabilísticos y cuáles son los desafíos clave que aborda?** 
Expectiminimax es una extensión del algoritmo minimax que se utiliza en
juegos con incertidumbre, como aquellos con nodos de azar o información
oculta. En lugar de suponer que el oponente siempre tomará la mejor decisión
posible, el expectiminimax considera todas las posibles acciones del
oponente, incluyendo acciones aleatorias, y calcula el valor esperado de cada
jugada. Esto implica manejar distribuciones de probabilidad en lugar de
resultados deterministas. Los desafíos clave que aborda expectiminimax
incluyen la necesidad de modelar y evaluar la incertidumbre en el juego, así
como la complejidad adicional que surge al considerar múltiples resultados
posibles en cada jugada.

## Referencias

* Wikipedia. (n.d.). Wikipedia. Retrieved from Minimax: [https://en.wikipedia.org/wiki/Minimax#:~:text=Minimax%20is%20used%20in%20zero,maximizing%20one's%20own%20minimum%20gain.](https://en.wikipedia.org/wiki/Minimax#:~:text=Minimax%20is%20used%20in%20zero,maximizing%20one's%20own%20minimum%20gain.)    
* Geeks for Geeks. (2023, enero 16). Minimax Algorithm in Game Theory | Set 4 (Alpha-Beta Pruning) . Retrieved from Geeks for Geeks: [https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/)  
* Geeks for Geeks. (2021, octubre 25). Geeks for Geeks. Retrieved from Expectimax Algorithm in Game Theory: [https://www.geeksforgeeks.org/expectimax-algorithm-in-game-theory/)](https://www.geeksforgeeks.org/expectimax-algorithm-in-game-theory/)

