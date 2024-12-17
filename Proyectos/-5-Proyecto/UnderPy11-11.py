import threading
import time
import cv2
import numpy as np
from pynput import keyboard
import random
from Ataque.AtaqueCV2 import Game


class Objeto:
    def __init__(self, nombre, mensaje_uso, vida_cura):
        self.nombre = nombre
        self.mensaje_uso = mensaje_uso
        self.vida_cura = vida_cura

    def usar(self, jugador, interface):
        jugador.vida = min(jugador.vida_maxima, jugador.vida + self.vida_cura)
        interface.draw_dialog(f"{self.mensaje_uso} Vida actual: {jugador.vida}")



class Jugador:
    def __init__(self, vida_maxima, nivel, interface):
        self.inventario = [
            Objeto("Pocion", "Usaste una poción y recuperaste 10 puntos de vida.", 10),
            Objeto("Chuleta", "Usaste una chuleta y recuperaste 20 puntos de vida.", 20),
            Objeto("Bola de nieve", "Usaste la Bola de nieve. ¡No pasó nada!", 0)
        ]
        self.vida = vida_maxima
        self.vida_maxima = vida_maxima
        self.nivel = nivel
        self.interface=interface

    def mostrar_inventario(self):
        print("Inventario:")
        for i, objeto in enumerate(self.inventario, 1):
            print(f"[{i}]: {objeto.nombre}")
    
    def usar_objeto(self, interface):
        if not self.inventario:
            interface.draw_dialog("No tienes objetos.")
            return
        self.mostrar_inventario()
        eleccion = input("Elige un objeto para usar (número): ")
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(self.inventario):
            objeto_seleccionado = self.inventario[int(eleccion) - 1]
            objeto_seleccionado.usar(self, interface)
            self.inventario.remove(objeto_seleccionado)
        else:
            interface.draw_dialog("Selección no válida.")



class Enemigo:
    def __init__(self, nombre, vida_maxima, perdonarLvl, interface):
        self.nombre = nombre
        self.vida = vida_maxima
        self.vida_maxima = vida_maxima
        self.interface=interface
        self.nivel_amistad = 0
        self.perdonarLvl = perdonarLvl
        self.dialogos = {
            0: ["¡Nyeh heh heh! ¡Yo, el GRAN PAPYRUS, nunca perderé!", 
                "¡Incluso si me ganas, aún seré tu amigo!", 
                "¡Preparado para ser impresionado por mis ataques!"],
            3: ["Hmm... ¿estás empezando a disfrutar de mi compañía?", 
                "¡Mis huesos son indestructibles, pero también mi corazón!", 
                "¡Vamos, no te contengas!"],
            6: ["¿No te estarás... enamorando de mí?", 
                "Este es el final, pero puedo perdonarte..."],
        }
        self.acciones = {
            0: [
                {"nombre": "Flirtear", "dialogo": "¡Flirteas con Papyrus! Él se sonroja.", "amistad": 1},
                {"nombre": "Elogiar", "dialogo": "Le dices a Papyrus que sus habilidades de cocinero son impresionantes. ¡Se siente halagado!", "amistad": 1},
            ],
            3: [
                {"nombre": "Flirtear más", "dialogo": "¡Papyrus está nervioso! ¡Le estás causando sentimientos inesperados!", "amistad": 2},
                {"nombre": "Elogiar más", "dialogo": "Le dices a Papyrus que es el esqueleto más guapo del mundo. Él no sabe cómo reaccionar.", "amistad": 2},
            ],
            6: [
                {"nombre": "Declaración", "dialogo": "Le dices a Papyrus que te has enamorado de él. ¡Se sonroja tanto que casi se derrite!", "amistad": 2},
            ]
        }
        self.ataques = {
            0: ["/papyrus/1_processed.avi"],
            1: ["/papyrus/2_processed.avi"],
            2: ["/papyrus/3_processed.avi"],
            3: ["/papyrus/4_processed.avi"]
        }
        self.actualDialogo = self.get_dialogo()

    def ajustar_nivel_amistad(self):
        if self.nivel_amistad < 0:
            self.nivel_amistad = 0

    def obtener_nivel_valido(self, diccionario):
        niveles_disponibles = sorted(diccionario.keys())
        for nivel in reversed(niveles_disponibles):
            if self.nivel_amistad >= nivel:
                return nivel
        return niveles_disponibles[0]

    def get_dialogo(self):
        nivel_valido = self.obtener_nivel_valido(self.dialogos)
        return random.choice(self.dialogos[nivel_valido])

    def get_acciones(self):
        nivel_valido = self.obtener_nivel_valido(self.acciones)
        return self.acciones.get(nivel_valido, [])

    def get_ataques(self):
        nivel_valido = self.obtener_nivel_valido(self.ataques)
        return self.ataques.get(nivel_valido, [])

    
    def atacar(self, jugador, attack_in_progress, interface):
        ataque = random.choice(self.get_ataques())
        attack_in_progress = True
        interface.draw_dialog(f"Papyrus te ataca con {ataque}.")
        
        # Iniciar el juego de ataque en una ventana separada sin bloquear
        game = Game('papyrus', ataque)
        game_thread = threading.Thread(target=game.run)
        game_thread.start()
        
        # Esperar a que el juego termine
        game_thread.join()
        hits_recibidos = game.hits  # Capturar el número de hits recibidos
        attack_in_progress = False
        self.nivel_amistad+=1
        # Continuar con el ataque después de que el juego termine
        jugador.vida -= 2*hits_recibidos
        interface.draw_dialog(f"Papyrus te quita {2*hits_recibidos} puntos de vida. Vida actual: {jugador.vida}")

class UndertaleInterface:
    def __init__(self, width=1100):
        self.width = width
        self.height = int(width * 3/4)
        
        # Colores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        # Cargamos las imágenes necesarias
        self.papyrus_sprite = cv2.imread('papyrus.png', cv2.IMREAD_UNCHANGED)
        if self.papyrus_sprite is None:
            self.papyrus_sprite = np.zeros((200, 150, 4), dtype=np.uint8)
            self.papyrus_sprite[:, :, 3] = 255
        else:
            # Redimensionar el sprite
            desired_height = int(self.height * 0.3)
            aspect_ratio = self.papyrus_sprite.shape[1] / self.papyrus_sprite.shape[0]
            desired_width = int(desired_height * aspect_ratio)
            self.papyrus_sprite = cv2.resize(self.papyrus_sprite, (desired_width, desired_height))
        
        # Estado del juego
        self.selected_option = 0
        self.options = ['FIGHT', 'ACT', 'ITEM', 'MERCY']
        self.submenu = None  # Indica si estamos en un submenu ("ACT" o "ITEM")
        self.attack_in_progress = False
        
        # Crear ventana
        self.window = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.running = True
        self.keys_pressed = {'a': False, 'd': False, 'enter': False, 'esc': False}  # Agregar 'esc' aquí

    def draw_dialog(self, text, color=(0, 255, 255)):
        """Dibuja el diálogo sobre el sprite en color amarillo."""
        sprite_y = self.height // 2 - self.papyrus_sprite.shape[0]
        dialog_x, dialog_y = 50, sprite_y - 50  # Encima del sprite de Papyrus
        cv2.putText(self.window, text, (dialog_x, dialog_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
 
    def show_act_menu(self, enemy):
        """Muestra el menú de acciones de "ACT"."""
        self.clear_dialog()
        for i, action in enumerate(enemy.get_acciones(), 1):
            cv2.putText(self.window, f"{i}. {action['nombre']}", (70, 400 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.WHITE, 2)

    def show_item_menu(self, player):
        """Muestra el inventario del jugador en el diálogo."""
        self.clear_dialog()
        for i, objeto in enumerate(player.inventario, 1):
            cv2.putText(self.window, f"{i}. {objeto.nombre}", (70, 400 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.WHITE, 2)

    def draw_interface(self, player, enemy):
        # Limpiar ventana
        self.window.fill(0)
        
        # Calcular dimensiones de las secciones
        half_height = self.height // 2
        dialog_height = int(self.height * 0.3)
        stats_height = int(self.height * 0.08)
        buttons_height = int(self.height * 0.12)
        
        # Posicionar y dibujar sprite de Papyrus
        sprite_height = self.papyrus_sprite.shape[0]
        sprite_width = self.papyrus_sprite.shape[1]
        sprite_x = (self.width - sprite_width) // 2
        sprite_y = half_height - sprite_height
        self.window[sprite_y:sprite_y + sprite_height, sprite_x:sprite_x + sprite_width] = self.papyrus_sprite
        
        # Dibujar caja de diálogo
        dialog_y = half_height
        cv2.rectangle(self.window, (50, dialog_y), (self.width-50, dialog_y + dialog_height), self.WHITE, 2)
        
        # Dibujar stats del jugador
        stats_y = dialog_y + dialog_height
        cv2.putText(self.window, f'Chara LV.{player.nivel}     HP {player.vida}/{player.vida_maxima}',
                    (50, stats_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.WHITE, 2)
        
        # Dibujar botones de acción
        button_width = self.width // 4
        button_y = self.height - buttons_height
        for i, option in enumerate(self.options):
            x = i * button_width
            color = self.WHITE if i == self.selected_option else (128, 128, 128)
            cv2.rectangle(self.window, (x + 10, button_y), (x + button_width - 10, self.height - 10), color, 2)
            cv2.putText(self.window, option, (x + 20, button_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            

    def handle_selection(self, player, enemy):
        """Manejo de la opción seleccionada."""
        if self.selected_option == 0:
            enemy.atacar(player, self.attack_in_progress, self)
        elif self.selected_option == 1:  # ACT
            self.submenu = "ACT"
            self.show_act_menu(enemy)
        elif self.selected_option == 2:  # ITEM
            self.submenu = "ITEM"
            self.show_item_menu(player)

    def handle_submenu_input(self, player, enemy):
        """Manejo de la entrada en el submenú actual."""
        if self.submenu == "ACT":
            eleccion = input("Elige una acción para realizar (número): ")
            acciones = enemy.get_acciones()
            if eleccion.isdigit() and 1 <= int(eleccion) <= len(acciones):
                accion = acciones[int(eleccion) - 1]
                enemy.nivel_amistad += accion['amistad']
                self.draw_dialog(accion['dialogo'])
            else:
                print("Selección no válida.")
        elif self.submenu == "ITEM":
            player.usar_objeto(self)
            self.draw_dialog("Usaste un objeto.")
        self.submenu = None  # Volver al menú principal

    def handle_input(self, player, enemy):
        """Modifica el manejo de entradas para permitir regresar con ESC."""
        if self.submenu:
            if self.keys_pressed['esc']:
                self.submenu = None  # Regresar al menú principal
                self.clear_dialog()
                return None
            else:
                self.handle_submenu_input(player, enemy)  # Manejo del submenú
                return None
        else:
            # Lógica original de manejo de entradas en el menú principal
            if self.attack_in_progress:
                return None
            if self.keys_pressed['a']:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                time.sleep(0.3)
            elif self.keys_pressed['d']:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                time.sleep(0.3)
            elif self.keys_pressed['enter']:
                self.keys_pressed['enter'] = False
                return self.options[self.selected_option]
        return None

    def clear_dialog(self):
        """Borra el contenido de diálogo."""
        dialog_y = self.height // 2
        cv2.rectangle(self.window, (50, dialog_y), (self.width - 50, dialog_y + int(self.height * 0.3)), self.BLACK, -1)

    def on_press(self, key):
        try:
            if key.char == 'a':
                self.keys_pressed['a'] = True
            elif key.char == 'd':
                self.keys_pressed['d'] = True
        except AttributeError:
            if key == keyboard.Key.enter:
                self.keys_pressed['enter'] = True

    def on_release(self, key):
        try:
            if key.char == 'a':
                self.keys_pressed['a'] = False
            elif key.char == 'd':
                self.keys_pressed['d'] = False
        except AttributeError:
            if key == keyboard.Key.enter:
                self.keys_pressed['enter'] = False
            elif key == keyboard.Key.esc:
                self.running = False
                return False
    
    def run(self, player, enemy):
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()
    
        while self.running:
            self.draw_interface(player, enemy)
            cv2.imshow('Undertale Combat', self.window)
    
            action = self.handle_input(player, enemy)
            if action:
                self.handle_selection(player, enemy)
    
            if cv2.waitKey(10) & 0xFF == 27:
                break
    
        cv2.destroyAllWindows()
        listener.stop()

if __name__ == "__main__":
    interface = UndertaleInterface()
    jugador = Jugador(vida_maxima=30, nivel=1, interface= interface)
    papyrus = Enemigo(nombre="Papyrus", vida_maxima=15, perdonarLvl=6, interface= interface)
    
    interface.run(jugador, papyrus)
