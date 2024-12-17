# ¿OpenCV como GameEngine?  
**Alejandro Barrena Millán**

## **1. Introducción**

### **Motivación**

Este estudio surge como un proyecto para la asignatura de Imagen Digital en la Universidad de Extremadura (UEx). Muchos de nosotros elegimos esta asignatura con la motivación adicional de que, según el plan, en la segunda mitad de la asignatura se trabajará con Unity. Sin embargo, la primera parte del curso se centra en OpenCV, y el interés general por desarrollar videojuegos hizo que muchos no quisieran esperar a Unity para comenzar sus proyectos de juegos. A lo largo de las clases, varios compañeros han creado pequeños minijuegos o proyectos que se asemejan a videojuegos utilizando OpenCV. Sin embargo, hasta ahora, nadie se había detenido a analizar si estos proyectos eran realmente viables en términos de rendimiento, funcionalidad y escalabilidad; simplemente comenzaron y siguieron desarrollando sin evaluar sus limitaciones.

### **Objetivo**

El objetivo principal de este estudio es evaluar la flexibilidad de OpenCV y demostrar hasta qué punto puede adaptarse a un entorno de desarrollo de videojuegos. Nos enfocaremos en explorar los límites y las capacidades de OpenCV para funcionar como *game engine* propio, construyéndolo con ayuda de librerías auxiliares para crear una experiencia lo más completa posible en términos de jugabilidad, físicas, entradas, y otros aspectos clave de un videojuego.

### **Alcance**

Para mantener la pureza del estudio y cumplir con el objetivo de construir un motor de juego propio, se prohíbe el uso de *game engines* preexistentes, como Pygame, incluso si es solo para el sistema de audio. Esto garantizará que toda la funcionalidad del juego se logre con OpenCV y librerías complementarias de propósito general, evaluando OpenCV en sí y no en combinación con otros motores de juego, si el resultado es satisfactorio concluiremos debatiendo si es viable crear nuestro propio *game engine* con OpenCV.

### **Resumen de Resultados**

Como adelantamiento de los resultados, descubriremos que OpenCV no es viable para funcionar como un *game engine* completo. Sin embargo, el estudio representa un experimento interesante y ofrece una visión valiosa sobre los límites de esta herramienta y su potencial en el desarrollo de videojuegos básicos.

## **2. Definición de Game Engine**

Para evaluar la viabilidad de OpenCV como *game engine*, es esencial entender primero qué es un *game engine* y qué características mínimas debe ofrecer.

### **¿Qué es un Game Engine?**

Un *game engine* es un entorno de desarrollo diseñado específicamente para facilitar la creación de videojuegos. Estos motores proporcionan una serie de herramientas y sistemas integrados que permiten a los desarrolladores crear entornos interactivos y complejos sin tener que construir todas las funcionalidades desde cero. Los motores de juego se encargan de aspectos críticos como el renderizado, la física, la gestión de audio y entradas, y la organización de escenas, permitiendo que los desarrolladores se centren en la lógica y la jugabilidad.

### **Componentes Esenciales de un Game Engine**

Para cumplir con su propósito, un *game engine* debe incluir los siguientes elementos:

1. **Renderizado Gráfico**: La capacidad de dibujar en pantalla gráficos bidimensionales (2D) y tridimensionales (3D). Esto incluye la carga de texturas, modelado de objetos y efectos visuales como iluminación y sombras.
  
2. **Física y Colisiones**: Un sistema de físicas que gestione los movimientos y la interacción entre objetos, de forma que el juego pueda simular fenómenos como gravedad, rebotes y choques, y que detecte las colisiones entre entidades.
  
3. **Entradas del Usuario**: La posibilidad de capturar y responder a las entradas del jugador (teclado, ratón, mandos, etc.) para hacer que el juego sea interactivo y reactivo a las acciones del usuario.
  
4. **Audio**: Funcionalidades de sonido para reproducir efectos y música que mejoren la inmersión y la experiencia del juego.

5. **Gestión de Escenas**: Un sistema que permita organizar y cambiar entre distintos estados o pantallas del juego (como menús, niveles o pantallas de victoria/derrota) de manera estructurada.

### **Comparación Inicial: Game Engine vs. OpenCV**

OpenCV es una biblioteca de procesamiento de imágenes y visión por computadora, no un motor de videojuegos. Esto significa que carece de muchas de las funcionalidades integradas de un *game engine*. A continuación, se detalla cómo planeamos suplir cada componente de un *game engine* con OpenCV y otras herramientas:

- **Renderizado Gráfico**: OpenCV puede encargarse del renderizado 2D básico, como dibujar objetos, moverlos en pantalla, y aplicar algunos efectos básicos. Sin embargo, carece de soporte para gráficos 3D o efectos avanzados (como sombras o iluminación en 3D), lo que limita su capacidad para videojuegos modernos.

- **Física y Colisiones**: OpenCV no incluye un motor de físicas, por lo que se requiere apoyo de otras herramientas, como **NumPy**, para realizar cálculos de física básicos, como detección de colisiones o movimientos básicos de los objetos. Esto permite simular efectos sencillos de colisión, aunque no es comparable a motores de física dedicados.

- **Entradas del Usuario**: OpenCV no incluye un sistema para capturar entradas del usuario. Para suplir esto, utilizaremos **Pynput**, una biblioteca de Python que permite capturar eventos de teclado y ratón. Con Pynput, podemos simular el control del jugador en el juego, aunque sin la integración directa que ofrecen los *game engines* tradicionales.

- **Audio**: OpenCV no tiene soporte para manejar audio, y aunque normalmente se recurriría a **Pygame** para gestionar música y efectos de sonido, en este estudio se descarta por considerarse otro *game engine*. Esto deja el proyecto sin opciones de audio, lo que es una limitación considerable para una experiencia de juego completa.

- **Gestión de Escenas**: OpenCV no dispone de un sistema de escenas, pero es posible implementar una gestión manual de diferentes pantallas o estados en el juego (como el menú, niveles, y pantalla de fin de juego). Esto requiere programar de forma personalizada la lógica para cambiar entre escenas, lo cual puede ser tosco y requiere un esfuerzo adicional en comparación con motores que incluyen este sistema de forma integrada.

En este estudio, evaluaremos si es posible suplir estas carencias mediante el uso de bibliotecas adicionales y con desarrollo manual, de manera que OpenCV, junto a otras herramientas, pueda simular un *game engine* básico. La carencia de soporte para audio y gestión avanzada de escenas, junto con las limitaciones en físicas y renderizado, presentará un desafío importante y guiará nuestro análisis sobre si OpenCV es o no viable como motor de videojuegos.

## **3. Proyectos de Prueba y Evaluación**

Para analizar la viabilidad de OpenCV como *game engine*, desarrollamos varios proyectos básicos, cada uno de los cuales explora diferentes aspectos del desarrollo de videojuegos. A continuación, se describen los puntos fuertes y débiles de cada proyecto, así como las posibles soluciones a las limitaciones observadas.

### **Laberinto**

El primer proyecto fue un juego de laberinto básico, con el objetivo de evaluar la capacidad de OpenCV para gestionar IA y generar gráficos bidimensionales simples.

- **Aspectos Positivos**: Este proyecto demostró que es posible implementar lógica compleja en OpenCV, incluyendo una IA que utiliza el algoritmo A* para perseguir al jugador. También logramos generar figuras geométricas bidimensionales básicas.
  
- **Limitaciones**: La jugabilidad resultó ser tosca, ya que para moverse a la izquierda se requiere pulsar la tecla dos veces, en lugar de mantenerla presionada. Además, los gráficos se ven poco atractivos, ya que OpenCV no soporta texturas detalladas.
  
- **Posibles Mejoras**: Implementar un control más fluido, posiblemente manteniendo la tecla pulsada, y mejorar la apariencia visual mediante la carga de imágenes para texturizar los objetos del laberinto.

### **Bomberman**

El segundo proyecto fue una versión simplificada del clásico Bomberman, con funcionalidad multijugador local en el mismo teclado.

- **Aspectos Positivos**: Se lograron cargar texturas para los personajes y obstáculos, y el juego ofrece un rendimiento aceptable. El juego es multijugador local y no presenta ralentizaciones.
  
- **Limitaciones**: Debido a que OpenCV no admite transparencia en las imágenes PNG de forma directa, fue necesario eliminar los colores de fondo con filtros manuales. Además, persisten los problemas de control poco fluido, y no hay un sistema de audio. La gestión de escenas resultó ser demasiado compleja de implementar, por lo que no se pudo añadir un menú de inicio.

- **Posibles Mejoras**: Trabajar en una solución para controles más fluidos y mejorar la gestión de escenas para permitir un flujo más natural entre pantallas como el menú de inicio y el juego en sí.

### **Undertale Papyrus Combat**

Este proyecto simula un sistema de combate basado en el juego *Undertale*, con el objetivo de emular una jugabilidad rápida y atractiva.

- **Aspectos Positivos**: La estética del juego es agradable y similar al original. Para lograr controles más fluidos, los comandos del jugador se separaron en un hilo distinto del de renderizado, logrando así la primera experiencia con controles realmente suaves. Las físicas y el renderizado básico funcionan como en los proyectos anteriores.

- **Limitaciones**: Surgieron problemas de rendimiento al intentar procesar vídeos para los ataques, revelando la baja eficiencia de OpenCV para manejar operaciones complejas en tiempo real. Aún no existe un sistema de audio, y la gestión de escenas sigue siendo rudimentaria; al cambiar de escena, se abre una nueva ventana en lugar de hacerlo dentro del mismo flujo de juego.

- **Posibles Mejoras**: Optimizar el uso de recursos para reducir el impacto en el rendimiento, especialmente en escenas con mayor carga gráfica, y explorar opciones para implementar audio sin recurrir a Pygame.

### **Experimentos en 3D**

Finalmente, se probaron proyectos en 3D, visualizando un cubo tridimensional y creando una versión simplificada de *Doom* mediante técnicas de raycasting, lo cual representa un desafío para OpenCV debido a su enfoque bidimensional.

- **Visualización de un Cubo en 3D**: Fue posible mostrar un cubo en 3D básico, aunque OpenCV no permite importar modelos 3D. Esto limita las opciones a figuras simples, pero demuestra que, en teoría, OpenCV puede generar gráficos en tres dimensiones.
  
- **DOOM 3D (Raycasting)**: Se logró recrear el estilo de *Doom* utilizando raycasting, una técnica para simular gráficos 3D. Sin embargo, aunque el proyecto funcionó, quedó claro que OpenCV no es viable para desarrollar juegos en 3D debido a la programación compleja y a la falta de soporte nativo para manejar gráficos 3D con eficiencia.

- **Conclusión**: OpenCV tiene capacidad para generar gráficos básicos en 3D, pero no es viable para desarrollar videojuegos complejos o en estilo "Doomlike", dado el nivel de programación y esfuerzo requerido para compensar sus limitaciones.

En conjunto, estos proyectos muestran que, aunque es posible realizar videojuegos simples en OpenCV, el desarrollo es lento y requiere múltiples soluciones alternativas para cubrir las funciones mínimas de un *game engine*. Cada proyecto ofrece lecciones sobre las limitaciones de OpenCV y proporciona ideas sobre cómo superar algunas de ellas, aunque a un coste considerable en términos de esfuerzo y rendimiento.

## **Menciones Honoríficas**

En esta sección, queremos reconocer a algunos compañeros cuyos proyectos destacaron en la exploración de OpenCV como motor de videojuegos, mostrando cómo es posible superar algunas de las limitaciones de la biblioteca, aunque con esfuerzo adicional.

1. **Pablo Natera Muñoz**  
   Su proyecto *Nintendo DS* logró implementar un sistema de control de escenas innovador y funcional en OpenCV. Cada juego en su proyecto es un archivo `.py` independiente, que se gestiona desde una ventana principal que emula la consola Nintendo DS. Este enfoque permitió a Pablo ejecutar y controlar distintos juegos desde una misma ventana, demostrando que es posible gestionar escenas en OpenCV. Sin embargo, este avance muestra que, aunque viable, el control de escenas en OpenCV requiere un esfuerzo y una organización cuidadosos.

2. **Víctor Andrés Navareño Moza**  
   Víctor desarrolló un juego con gráficos de alta calidad que además utiliza reconocimiento facial en OpenCV para los controles, en lugar de recurrir a otras bibliotecas de entrada. Este proyecto demostró el potencial de OpenCV para integrar controles avanzados y creativos, como el seguimiento facial, mostrando cómo OpenCV puede abrir nuevas formas de interacción sin depender de *game engines* tradicionales, aunque esto también incrementa la complejidad del desarrollo.

Estas menciones subrayan los logros alcanzados por nuestros compañeros y destacan soluciones innovadoras que abordan algunas de las limitaciones clave de OpenCV en el ámbito del desarrollo de videojuegos.

## **Conclusiones**

A lo largo de este estudio, hemos explorado las posibilidades y limitaciones de OpenCV en el desarrollo de videojuegos, encontrando que, aunque técnicamente es posible crear experiencias jugables simples, la biblioteca está lejos de cumplir con los requisitos de un *game engine* completo. 

OpenCV permite implementar mecánicas básicas, gráficos 2D y hasta efectos visuales en 3D, pero estos intentos suelen ser complejos y demandan trabajo adicional para compensar sus carencias. Por ejemplo, el control de escenas es funcional pero rudimentario y difícil de gestionar, y los controles requieren una organización cuidadosa para ser fluidos. La física y detección de colisiones pueden abordarse con ayuda de bibliotecas externas, pero la falta de optimización afecta al rendimiento en proyectos más ambiciosos. Además, la ausencia de soporte de audio limita la inmersión, impidiendo que OpenCV proporcione una experiencia completa de juego.

En conclusión, aunque OpenCV puede usarse para prototipos y juegos básicos, no es una opción viable para proyectos de videojuegos completos. Este experimento, no obstante, destaca cómo herramientas alternativas pueden inspirar enfoques creativos en el desarrollo, ofreciendo a los desarrolladores una plataforma experimental para innovar y aprender.

# **Manual del Programador**

## **Laberinto**

Este código implementa un juego de laberinto utilizando OpenCV. A continuación se resumen las funciones principales:

### **Funciones principales**
- **Generación de laberinto**: `generate_maze(size)` (crea el laberinto usando DFS).
- **Dibujo en pantalla**: `draw_maze(img, maze, player_pos, exit_pos, enemy_pos)` (dibuja el laberinto, jugador, salida y enemigo).
- **Movimiento**: `move_player(key, player_pos, maze)` (mueve al jugador con W, A, S, D), `move_enemy(player_pos, enemy_pos, maze)` (mueve al enemigo hacia el jugador).
- **Algoritmos**: `a_star(maze, start, goal)` (encuentra el camino más corto), `add_wall(player_pos, maze)` y `remove_wall(player_pos, maze)` (añadir o quitar paredes).

### **Controles del juego**
- **W, A, S, D**: Mover al jugador.
- **P**: Añadir una pared.
- **Q**: Quitar una pared.
- **ESC**: Salir del juego.

## **Bomberman**

### **Visión General**
Implementación de Bomberman en Python usando OpenCV para gráficos. El juego soporta hasta 3 jugadores (2 humanos + 1 IA).

### **Funciones Principales**
- **create_grid()**: Genera el mapa aleatorio o predeterminado.
- **draw_grid(frame, grid)**: Dibuja el estado actual del juego.
- **draw_player(frame, player, player_number)**: Renderiza los jugadores.
- **main()**: Loop principal del juego y gestión de eventos.

### **Clases Clave**
- **Player**: Gestiona al jugador (posición, bombas, power-ups).
- **Bomb**: Maneja las bombas (temporizador, explosión, alcance).
- **AIPlayer**: Implementa la IA (hereda de Player).

### **Controles**
- **Jugador 1**: WASD (movimiento), Espacio (bomba).
- **Jugador 2**: Flechas (movimiento), Enter (bomba).
- **ESC**: Salir.

### **Estados del Grid**
- **0**: Vacío.
- **1**: Muro indestructible.
- **2**: Bomba.
- **3**: Bloque destructible.
- **4**: Explosión.
- **5-8**: Power-ups.

### **Power-ups**
- **Bomb Up**: Aumenta el máximo de bombas.
- **Fire Up**: Aumenta el alcance de la explosión.
- **Kick Up**: Permite patear bombas.
- **Spike Bomb**: Bomba especial.

## **Undertale Combat**

### **Visión General**
Este código implementa un juego de combate inspirado en Undertale usando OpenCV para la visualización y pynput para la captura de entradas del teclado. El juego se estructura en combate y opciones interactivas con el enemigo.

### **Funciones Principales**
- **Clases principales**:
  - **Jugador**: Gestiona el inventario y las acciones del jugador. 
    - `mostrar_inventario()`, `usar_objeto(interface)`.
  - **Enemigo**: Gestiona las interacciones con el enemigo (nivel de amistad, ataques).
    - `ajustar_nivel_amistad()`, `atacar(jugador, attack_in_progress, interface)`.
  - **UndertaleInterface**: Maneja la interfaz gráfica del juego y las entradas del jugador.
    - `draw_dialog(text, color)`, `show_act_menu(enemy)`, `handle_input(player, enemy)`, `run(player, enemy)`.

### **Juego Principal**
El juego se ejecuta a través de la función `run(player, enemy)` en la clase **UndertaleInterface**, donde se dibujan los menús, se manejan las entradas y se gestionan las acciones de combate.

### **Controles del Juego**
- **A**: Mover la selección a la izquierda.
- **D**: Mover la selección a la derecha.
- **Enter**: Seleccionar opción.
- **ESC**: Salir o regresar al menú principal.

### **Estructura del Juego**
- **Combate**: El jugador selecciona entre las opciones FIGHT, ACT, ITEM y MERCY.
- **Submenús**:
  - **ACT**: Realizar acciones para aumentar el nivel de amistad con el enemigo.
  - **ITEM**: Usar objetos del inventario.
  
El código del combate es modular y organiza las acciones en distintos archivos `.py`, lo que facilita su expansión y modificación.

## **Doom-like Shooter**

### **Visión General**
Juego estilo Doom 2D con raycasting, enemigos# ¿OpenCV como GameEngine?  
**Alejandro Barrena Millán**

## **1. Introducción**

### **Motivación**

Este estudio surge como un proyecto para la asignatura de Imagen Digital en la Universidad de Extremadura (UEx). Muchos de nosotros elegimos esta asignatura con la motivación adicional de que, según el plan, en la segunda mitad de la asignatura se trabajará con Unity. Sin embargo, la primera parte del curso se centra en OpenCV, y el interés general por desarrollar videojuegos hizo que muchos no quisieran esperar a Unity para comenzar sus proyectos de juegos. A lo largo de las clases, varios compañeros han creado pequeños minijuegos o proyectos que se asemejan a videojuegos utilizando OpenCV. Sin embargo, hasta ahora, nadie se había detenido a analizar si estos proyectos eran realmente viables en términos de rendimiento, funcionalidad y escalabilidad; simplemente comenzaron y siguieron desarrollando sin evaluar sus limitaciones.

### **Objetivo**

El objetivo principal de este estudio es evaluar la flexibilidad de OpenCV y demostrar hasta qué punto puede adaptarse a un entorno de desarrollo de videojuegos. Nos enfocaremos en explorar los límites y las capacidades de OpenCV para funcionar como *game engine* propio, construyéndolo con ayuda de librerías auxiliares para crear una experiencia lo más completa posible en términos de jugabilidad, físicas, entradas, y otros aspectos clave de un videojuego.

### **Alcance**

Para mantener la pureza del estudio y cumplir con el objetivo de construir un motor de juego propio, se prohíbe el uso de *game engines* preexistentes, como Pygame, incluso si es solo para el sistema de audio. Esto garantizará que toda la funcionalidad del juego se logre con OpenCV y librerías complementarias de propósito general, evaluando OpenCV en sí y no en combinación con otros motores de juego, si el resultado es satisfactorio concluiremos debatiendo si es viable crear nuestro propio *game engine* con OpenCV.

### **Resumen de Resultados**

Como adelantamiento de los resultados, descubriremos que OpenCV no es viable para funcionar como un *game engine* completo. Sin embargo, el estudio representa un experimento interesante y ofrece una visión valiosa sobre los límites de esta herramienta y su potencial en el desarrollo de videojuegos básicos.

## **2. Definición de Game Engine**

Para evaluar la viabilidad de OpenCV como *game engine*, es esencial entender primero qué es un *game engine* y qué características mínimas debe ofrecer.

### **¿Qué es un Game Engine?**

Un *game engine* es un entorno de desarrollo diseñado específicamente para facilitar la creación de videojuegos. Estos motores proporcionan una serie de herramientas y sistemas integrados que permiten a los desarrolladores crear entornos interactivos y complejos sin tener que construir todas las funcionalidades desde cero. Los motores de juego se encargan de aspectos críticos como el renderizado, la física, la gestión de audio y entradas, y la organización de escenas, permitiendo que los desarrolladores se centren en la lógica y la jugabilidad.

### **Componentes Esenciales de un Game Engine**

Para cumplir con su propósito, un *game engine* debe incluir los siguientes elementos:

1. **Renderizado Gráfico**: La capacidad de dibujar en pantalla gráficos bidimensionales (2D) y tridimensionales (3D). Esto incluye la carga de texturas, modelado de objetos y efectos visuales como iluminación y sombras.
  
2. **Física y Colisiones**: Un sistema de físicas que gestione los movimientos y la interacción entre objetos, de forma que el juego pueda simular fenómenos como gravedad, rebotes y choques, y que detecte las colisiones entre entidades.
  
3. **Entradas del Usuario**: La posibilidad de capturar y responder a las entradas del jugador (teclado, ratón, mandos, etc.) para hacer que el juego sea interactivo y reactivo a las acciones del usuario.
  
4. **Audio**: Funcionalidades de sonido para reproducir efectos y música que mejoren la inmersión y la experiencia del juego.

5. **Gestión de Escenas**: Un sistema que permita organizar y cambiar entre distintos estados o pantallas del juego (como menús, niveles o pantallas de victoria/derrota) de manera estructurada.

### **Comparación Inicial: Game Engine vs. OpenCV**

OpenCV es una biblioteca de procesamiento de imágenes y visión por computadora, no un motor de videojuegos. Esto significa que carece de muchas de las funcionalidades integradas de un *game engine*. A continuación, se detalla cómo planeamos suplir cada componente de un *game engine* con OpenCV y otras herramientas:

- **Renderizado Gráfico**: OpenCV puede encargarse del renderizado 2D básico, como dibujar objetos, moverlos en pantalla, y aplicar algunos efectos básicos. Sin embargo, carece de soporte para gráficos 3D o efectos avanzados (como sombras o iluminación en 3D), lo que limita su capacidad para videojuegos modernos.

- **Física y Colisiones**: OpenCV no incluye un motor de físicas, por lo que se requiere apoyo de otras herramientas, como **NumPy**, para realizar cálculos de física básicos, como detección de colisiones o movimientos básicos de los objetos. Esto permite simular efectos sencillos de colisión, aunque no es comparable a motores de física dedicados.

- **Entradas del Usuario**: OpenCV no incluye un sistema para capturar entradas del usuario. Para suplir esto, utilizaremos **Pynput**, una biblioteca de Python que permite capturar eventos de teclado y ratón. Con Pynput, podemos simular el control del jugador en el juego, aunque sin la integración directa que ofrecen los *game engines* tradicionales.

- **Audio**: OpenCV no tiene soporte para manejar audio, y aunque normalmente se recurriría a **Pygame** para gestionar música y efectos de sonido, en este estudio se descarta por considerarse otro *game engine*. Esto deja el proyecto sin opciones de audio, lo que es una limitación considerable para una experiencia de juego completa.

- **Gestión de Escenas**: OpenCV no dispone de un sistema de escenas, pero es posible implementar una gestión manual de diferentes pantallas o estados en el juego (como el menú, niveles, y pantalla de fin de juego). Esto requiere programar de forma personalizada la lógica para cambiar entre escenas, lo cual puede ser tosco y requiere un esfuerzo adicional en comparación con motores que incluyen este sistema de forma integrada.

En este estudio, evaluaremos si es posible suplir estas carencias mediante el uso de bibliotecas adicionales y con desarrollo manual, de manera que OpenCV, junto a otras herramientas, pueda simular un *game engine* básico. La carencia de soporte para audio y gestión avanzada de escenas, junto con las limitaciones en físicas y renderizado, presentará un desafío importante y guiará nuestro análisis sobre si OpenCV es o no viable como motor de videojuegos.

## **3. Proyectos de Prueba y Evaluación**

Para analizar la viabilidad de OpenCV como *game engine*, desarrollamos varios proyectos básicos, cada uno de los cuales explora diferentes aspectos del desarrollo de videojuegos. A continuación, se describen los puntos fuertes y débiles de cada proyecto, así como las posibles soluciones a las limitaciones observadas.

### **Laberinto**

El primer proyecto fue un juego de laberinto básico, con el objetivo de evaluar la capacidad de OpenCV para gestionar IA y generar gráficos bidimensionales simples.

- **Aspectos Positivos**: Este proyecto demostró que es posible implementar lógica compleja en OpenCV, incluyendo una IA que utiliza el algoritmo A* para perseguir al jugador. También logramos generar figuras geométricas bidimensionales básicas.
  
- **Limitaciones**: La jugabilidad resultó ser tosca, ya que para moverse a la izquierda se requiere pulsar la tecla dos veces, en lugar de mantenerla presionada. Además, los gráficos se ven poco atractivos, ya que OpenCV no soporta texturas detalladas.
  
- **Posibles Mejoras**: Implementar un control más fluido, posiblemente manteniendo la tecla pulsada, y mejorar la apariencia visual mediante la carga de imágenes para texturizar los objetos del laberinto.

### **Bomberman**

El segundo proyecto fue una versión simplificada del clásico Bomberman, con funcionalidad multijugador local en el mismo teclado.

- **Aspectos Positivos**: Se lograron cargar texturas para los personajes y obstáculos, y el juego ofrece un rendimiento aceptable. El juego es multijugador local y no presenta ralentizaciones.
  
- **Limitaciones**: Debido a que OpenCV no admite transparencia en las imágenes PNG de forma directa, fue necesario eliminar los colores de fondo con filtros manuales. Además, persisten los problemas de control poco fluido, y no hay un sistema de audio. La gestión de escenas resultó ser demasiado compleja de implementar, por lo que no se pudo añadir un menú de inicio.

- **Posibles Mejoras**: Trabajar en una solución para controles más fluidos y mejorar la gestión de escenas para permitir un flujo más natural entre pantallas como el menú de inicio y el juego en sí.

### **Undertale Papyrus Combat**

Este proyecto simula un sistema de combate basado en el juego *Undertale*, con el objetivo de emular una jugabilidad rápida y atractiva.

- **Aspectos Positivos**: La estética del juego es agradable y similar al original. Para lograr controles más fluidos, los comandos del jugador se separaron en un hilo distinto del de renderizado, logrando así la primera experiencia con controles realmente suaves. Las físicas y el renderizado básico funcionan como en los proyectos anteriores.

- **Limitaciones**: Surgieron problemas de rendimiento al intentar procesar vídeos para los ataques, revelando la baja eficiencia de OpenCV para manejar operaciones complejas en tiempo real. Aún no existe un sistema de audio, y la gestión de escenas sigue siendo rudimentaria; al cambiar de escena, se abre una nueva ventana en lugar de hacerlo dentro del mismo flujo de juego.

- **Posibles Mejoras**: Optimizar el uso de recursos para reducir el impacto en el rendimiento, especialmente en escenas con mayor carga gráfica, y explorar opciones para implementar audio sin recurrir a Pygame.

### **Experimentos en 3D**

Finalmente, se probaron proyectos en 3D, visualizando un cubo tridimensional y creando una versión simplificada de *Doom* mediante técnicas de raycasting, lo cual representa un desafío para OpenCV debido a su enfoque bidimensional.

- **Visualización de un Cubo en 3D**: Fue posible mostrar un cubo en 3D básico, aunque OpenCV no permite importar modelos 3D. Esto limita las opciones a figuras simples, pero demuestra que, en teoría, OpenCV puede generar gráficos en tres dimensiones.
  
- **DOOM 3D (Raycasting)**: Se logró recrear el estilo de *Doom* utilizando raycasting, una técnica para simular gráficos 3D. Sin embargo, aunque el proyecto funcionó, quedó claro que OpenCV no es viable para desarrollar juegos en 3D debido a la programación compleja y a la falta de soporte nativo para manejar gráficos 3D con eficiencia.

- **Conclusión**: OpenCV tiene capacidad para generar gráficos básicos en 3D, pero no es viable para desarrollar videojuegos complejos o en estilo "Doomlike", dado el nivel de programación y esfuerzo requerido para compensar sus limitaciones.

En conjunto, estos proyectos muestran que, aunque es posible realizar videojuegos simples en OpenCV, el desarrollo es lento y requiere múltiples soluciones alternativas para cubrir las funciones mínimas de un *game engine*. Cada proyecto ofrece lecciones sobre las limitaciones de OpenCV y proporciona ideas sobre cómo superar algunas de ellas, aunque a un coste considerable en términos de esfuerzo y rendimiento.

## **Menciones Honoríficas**

En esta sección, queremos reconocer a algunos compañeros cuyos proyectos destacaron en la exploración de OpenCV como motor de videojuegos, mostrando cómo es posible superar algunas de las limitaciones de la biblioteca, aunque con esfuerzo adicional.

1. **Pablo Natera Muñoz**  
   Su proyecto *Nintendo DS* logró implementar un sistema de control de escenas innovador y funcional en OpenCV. Cada juego en su proyecto es un archivo `.py` independiente, que se gestiona desde una ventana principal que emula la consola Nintendo DS. Este enfoque permitió a Pablo ejecutar y controlar distintos juegos desde una misma ventana, demostrando que es posible gestionar escenas en OpenCV. Sin embargo, este avance muestra que, aunque viable, el control de escenas en OpenCV requiere un esfuerzo y una organización cuidadosos.

2. **Víctor Andrés Navareño Moza**  
   Víctor desarrolló un juego con gráficos de alta calidad que además utiliza reconocimiento facial en OpenCV para los controles, en lugar de recurrir a otras bibliotecas de entrada. Este proyecto demostró el potencial de OpenCV para integrar controles avanzados y creativos, como el seguimiento facial, mostrando cómo OpenCV puede abrir nuevas formas de interacción sin depender de *game engines* tradicionales, aunque esto también incrementa la complejidad del desarrollo.

Estas menciones subrayan los logros alcanzados por nuestros compañeros y destacan soluciones innovadoras que abordan algunas de las limitaciones clave de OpenCV en el ámbito del desarrollo de videojuegos.

## **Conclusiones**

A lo largo de este estudio, hemos explorado las posibilidades y limitaciones de OpenCV en el desarrollo de videojuegos, encontrando que, aunque técnicamente es posible crear experiencias jugables simples, la biblioteca está lejos de cumplir con los requisitos de un *game engine* completo. 

OpenCV permite implementar mecánicas básicas, gráficos 2D y hasta efectos visuales en 3D, pero estos intentos suelen ser complejos y demandan trabajo adicional para compensar sus carencias. Por ejemplo, el control de escenas es funcional pero rudimentario y difícil de gestionar, y los controles requieren una organización cuidadosa para ser fluidos. La física y detección de colisiones pueden abordarse con ayuda de bibliotecas externas, pero la falta de optimización afecta al rendimiento en proyectos más ambiciosos. Además, la ausencia de soporte de audio limita la inmersión, impidiendo que OpenCV proporcione una experiencia completa de juego.

En conclusión, aunque OpenCV puede usarse para prototipos y juegos básicos, no es una opción viable para proyectos de videojuegos completos. Este experimento, no obstante, destaca cómo herramientas alternativas pueden inspirar enfoques creativos en el desarrollo, ofreciendo a los desarrolladores una plataforma experimental para innovar y aprender.

# **Manual del Programador**

## **Laberinto**

Este código implementa un juego de laberinto utilizando OpenCV. A continuación se resumen las funciones principales:

### **Funciones principales**
- **Generación de laberinto**: `generate_maze(size)` (crea el laberinto usando DFS).
- **Dibujo en pantalla**: `draw_maze(img, maze, player_pos, exit_pos, enemy_pos)` (dibuja el laberinto, jugador, salida y enemigo).
- **Movimiento**: `move_player(key, player_pos, maze)` (mueve al jugador con W, A, S, D), `move_enemy(player_pos, enemy_pos, maze)` (mueve al enemigo hacia el jugador).
- **Algoritmos**: `a_star(maze, start, goal)` (encuentra el camino más corto), `add_wall(player_pos, maze)` y `remove_wall(player_pos, maze)` (añadir o quitar paredes).

### **Controles del juego**
- **W, A, S, D**: Mover al jugador.
- **P**: Añadir una pared.
- **Q**: Quitar una pared.
- **ESC**: Salir del juego.

## **Bomberman**

### **Visión General**
Implementación de Bomberman en Python usando OpenCV para gráficos. El juego soporta hasta 3 jugadores (2 humanos + 1 IA).

### **Funciones Principales**
- **create_grid()**: Genera el mapa aleatorio o predeterminado.
- **draw_grid(frame, grid)**: Dibuja el estado actual del juego.
- **draw_player(frame, player, player_number)**: Renderiza los jugadores.
- **main()**: Loop principal del juego y gestión de eventos.

### **Clases Clave**
- **Player**: Gestiona al jugador (posición, bombas, power-ups).
- **Bomb**: Maneja las bombas (temporizador, explosión, alcance).
- **AIPlayer**: Implementa la IA (hereda de Player).

### **Controles**
- **Jugador 1**: WASD (movimiento), Espacio (bomba).
- **Jugador 2**: Flechas (movimiento), Enter (bomba).
- **ESC**: Salir.

### **Estados del Grid**
- **0**: Vacío.
- **1**: Muro indestructible.
- **2**: Bomba.
- **3**: Bloque destructible.
- **4**: Explosión.
- **5-8**: Power-ups.

### **Power-ups**
- **Bomb Up**: Aumenta el máximo de bombas.
- **Fire Up**: Aumenta el alcance de la explosión.
- **Kick Up**: Permite patear bombas.
- **Spike Bomb**: Bomba especial.

## **Undertale Combat**

### **Visión General**
Este código implementa un juego de combate inspirado en Undertale usando OpenCV para la visualización y pynput para la captura de entradas del teclado. El juego se estructura en combate y opciones interactivas con el enemigo.

### **Funciones Principales**
- **Clases principales**:
  - **Jugador**: Gestiona el inventario y las acciones del jugador. 
    - `mostrar_inventario()`, `usar_objeto(interface)`.
  - **Enemigo**: Gestiona las interacciones con el enemigo (nivel de amistad, ataques).
    - `ajustar_nivel_amistad()`, `atacar(jugador, attack_in_progress, interface)`.
  - **UndertaleInterface**: Maneja la interfaz gráfica del juego y las entradas del jugador.
    - `draw_dialog(text, color)`, `show_act_menu(enemy)`, `handle_input(player, enemy)`, `run(player, enemy)`.

### **Juego Principal**
El juego se ejecuta a través de la función `run(player, enemy)` en la clase **UndertaleInterface**, donde se dibujan los menús, se manejan las entradas y se gestionan las acciones de combate.

### **Controles del Juego**
- **A**: Mover la selección a la izquierda.
- **D**: Mover la selección a la derecha.
- **Enter**: Seleccionar opción.
- **ESC**: Salir o regresar al menú principal.

### **Estructura del Juego**
- **Combate**: El jugador selecciona entre las opciones FIGHT, ACT, ITEM y MERCY.
- **Submenús**:
  - **ACT**: Realizar acciones para aumentar el nivel de amistad con el enemigo.
  - **ITEM**: Usar objetos del inventario.
  
El código del combate es modular y organiza las acciones en distintos archivos `.py`, lo que facilita su expansión y modificación.

## **Doom-like Shooter**

### **Visión General**
Juego estilo Doom 2D con raycasting, enemigos que persiguen al jugador y disparos.

### **Características**
- **Mapa**: Generado aleatoriamente, 1 = pared, 0 = espacio libre.
- **Movimiento Jugador**: 
  - **W**: Adelante, **S**: Atrás, **A/D**: Gira.
- **Disparo**: **Espacio** elimina enemigos en línea de visión.
- **Enemigos**: Persiguen al jugador con A*.
- **Raycasting**: Proyecta rayos para detectar paredes y enemigos.
- **Minimapa**: Muestra jugador y enemigos.

### **Controles**
- **A**: Gira izquierda
- **D**: Gira derecha
- **W**: Mover adelante
- **S**: Mover atrás
- **Espacio**: Disparar
- **Q**: Salir

### **Algoritmos**
- **Raycasting**: Simula la visión 3D.
- **A***: Movimiento de enemigos.

### **Inicio**
- Mapa aleatorio y jugador en posición inicial.
- Enemigos generados aleatoriamente, fuera de paredes.
