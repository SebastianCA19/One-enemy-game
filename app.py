import tkinter as tk
from tkinter import ttk
from characters import *
import random
import time

# Crear la raíz
app = tk.Tk()
app.title("ONE ENEMIES GAME")
app.geometry("1100x580")
app.resizable(0, 0)
app.configure(bg="#222831")

# Configurar la cuadrícula
app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=2)
app.columnconfigure(2, weight=1)

# Crear métodos y variables
type_class = tk.IntVar(value= -1)
entry = tk.StringVar()
control_var = tk.StringVar()


def get_class(class_type: str):
    if class_type == "Mago":
        type_class.set(1)
        info_player.set("Estás creando un mago")
    else:
        type_class.set(0)
        info_player.set("Estás creando un guerrero")

def start_battle(class_type: int, name: str):
    
    def atk(player, enemy):
        player.attack(enemy)
        enemy_health.set(int(enemy.health))
        
        if enemy.health <= 0:
            enemy.health = 0
            enemy_health.set(enemy.health)
            game_finished(0)
            decrease_health_bar(enemy, 0)  # Muestra la barra de salud completa como 0 (totalmente vacía)
        else:
            player_battle_info.set(f"{player.name} ha hecho {int((enemy.health_before_attack - enemy.health))} de daño")
            decrease_health_bar(enemy, (enemy.health / enemy.max_health) * 350)
            enemy_atk(enemy, player)

    def special_atk(player, enemy):
        player.special_attack(enemy)
        enemy_health.set(int(enemy.health))
        player_health.set(int(player.health))

        if enemy.health <= 0:
            enemy.health = 0
            enemy_health.set(enemy.health)
            game_finished(0)
            decrease_health_bar(enemy, 0)  # Muestra la barra de salud completa como 0 (totalmente vacía)
        else:
            player_battle_info.set(f"{player.name} ha hecho {int(enemy.health_before_attack - enemy.health)} de daño")
            decrease_health_bar(enemy, (enemy.health / enemy.max_health) * 350)
            enemy_atk(enemy, player)

    def enemy_atk(enemy, player):
        type_atk = random.choice([0, 1])
        
        if type_atk == 0:
            enemy.attack(player)
            player_health.set(int(player.health))
            enemy_battle_info.set(f"{enemy.name} ha hecho {int((player.health_before_attack - player.health))} de daño")
            
            if player.health <= 0:
                player.health = 0
                player_health.set(player.health)
                game_finished(1)
                decrease_health_bar(player, 0)  # Muestra la barra de salud completa como 0 (totalmente vacía)
            else:
                decrease_health_bar(player, (player.health / player.max_health) * 350)
        else:
            enemy.special_attack(player)
            player_health.set(int(player.health))
            enemy_battle_info.set(f"{enemy.name} ha hecho {int((player.health_before_attack - player.health))} de daño")
            
            if player.health <= 0:
                player.health = 0
                player_health.set(player.health)
                game_finished(1)
                decrease_health_bar(player, 0)  # Muestra la barra de salud completa como 0 (totalmente vacía)
            else:
                decrease_health_bar(player, (player.health / player.max_health) * 350)
        

    def decrease_health_bar(character, health : int):
        if isinstance(character, wizard) or isinstance(character, warrior):
            player_health_bar.delete("player_health_bar")
            player_health_bar.create_rectangle(10, 10, 10 + health, 30, fill="green", outline="black", tags="player_health_bar")
        else:
            enemy_health_bar.delete("enemy_health_bar")
            enemy_health_bar.create_rectangle(10, 10, 10 + health, 30, fill="green", outline="black", tags="enemy_health_bar")

    def game_finished(result: int):

        game_result = tk.StringVar(value=" ")
        if result == 0:
            game_result.set("HAS GANADO :D")
        else:
            game_result.set("HAS PERDIDO D:")
        

        #Configuramos la ventana
        game_finished_window = tk.Toplevel(battle_window)
        game_finished_window.geometry("300x300")
        game_finished_window.configure(bg="#222831") 
        
        game_finished_window.columnconfigure(0, weight=1)
        game_finished_window.columnconfigure(1, weight=2)
        game_finished_window.columnconfigure(2, weight=2)
        game_finished_window.columnconfigure(3, weight=2)
        game_finished_window.rowconfigure(0, weight=2)
        game_finished_window.rowconfigure(1, weight=2)

        game_finished_window.title("Final del juego")
        label_game_result = tk.Label(game_finished_window, textvariable=game_result, bg="#222831", fg="#EEEEEE",font=("Arial", 20))
        label_game_result.grid(row=0, column=1, columnspan=2, sticky="s")
        buttonn_exit = tk.Button(game_finished_window, text="Salir", bg="#76ABAE", fg="#31363F", width=15, height=2, borderwidth=1,
                                 command=lambda: [game_finished_window.destroy(), battle_window.destroy()])
        buttonn_exit.grid(row=1, column=1, columnspan=2, pady=10, sticky="n")
                                                    

    player = None
    # Verificamos el tipo de personaje que escogió
    if class_type != -1 and  len(name) > 0:
        if class_type == 1:
            player = wizard(name)
        else:
            player = warrior(name)
        control_var.set("Empieza la aventura")
        goblin = normal_monster("Goblin")

        battle_window = tk.Toplevel(app)
        battle_window.title("Game")
        battle_window.geometry("1100x580")
        battle_window.resizable(0, 0)
        battle_window.configure(bg="#222831") 

        battle_window.columnconfigure(3, weight=4)
        battle_window.rowconfigure(0, weight=1)
        battle_window.rowconfigure(2, weight=1)

        #Variables
        player_name = tk.StringVar(value= player.name)
        enemy_name = tk.StringVar(value=  goblin.name)
        enemy_health = tk.IntVar(value=goblin.health)
        player_health = tk.IntVar(value=player.health)
        player_battle_info = tk.StringVar(value= " ")
        enemy_battle_info = tk.StringVar(value= " ")
        
        #Widgets del jugador
        player_name_label = tk.Label(master= battle_window, textvariable=player_name, bg="#222831", fg="#EEEEEE",font=("Arial", 20))
        player_name_label.grid(row=0, column= 1, padx= 20, pady= 20,sticky="s")
        player_health_bar = tk.Canvas(master=battle_window, width=350, height=30, bg="white")
        player_health_bar.grid(row=1, column=1, padx=20, pady=20,sticky="s")
        player_health_bar.create_rectangle(10, 10, 10 + ((player.health / 100) * 350), 30, fill="green", outline="black", tags="player_health_bar")
        player_health_label = tk.Label(master=battle_window, textvariable=player_health, bg="#222831", fg="#EEEEEE",font=("Arial", 15))
        player_health_label.grid(row=2, column= 1, padx= 20, pady= 20,sticky="n")
    
        atk_button = tk.Button(master=battle_window, text="ATAQUE" ,bg="#76ABAE", fg="#31363F", width=15, height=2, borderwidth=1,
                                  command= lambda: atk(player, goblin))
        atk_button.grid(row=2, column=0, padx=10, pady=10, sticky="ne")
        spec_atk_button = tk.Button(master=battle_window, text="ATAQUE ESPECIAL" ,bg="#76ABAE", fg="#31363F", width=15, height=2, borderwidth=1,
                                    command= lambda: special_atk(player,goblin))
        spec_atk_button.grid(row=2, column=2, padx=10, pady=10, sticky="nw")

        #Widgets del enemigo
        enemy_label = tk.Label(master= battle_window, textvariable=enemy_name, bg="#222831", fg="#EEEEEE",font=("Arial", 20))
        enemy_label.grid(row=0, column= 3, padx= 20, pady= 20,sticky="s")
        enemy_health_bar = tk.Canvas(battle_window, width=350,height=30, bg="white")
        enemy_health_bar.grid(row=1,column=3,padx=20,pady=20,sticky="s")
        enemy_health_bar.create_rectangle(10, 10, 10 + ((goblin.health / 100) * 350), 30, fill="green", outline="black", tags="enemy_health_bar")
        enemy_health_label = tk.Label(master=battle_window, textvariable=enemy_health, bg="#222831", fg="#EEEEEE",font=("Arial", 15))
        enemy_health_label.grid(row=2, column= 3, padx= 20, pady= 20,sticky="n")

        #Info de la batalla
        player_battle_info_label = tk.Label(master=battle_window, textvariable=player_battle_info, bg="#222831", fg="#EEEEEE",font=("Arial", 15))
        player_battle_info_label.grid(row= 2, column= 1,pady=60, sticky="s")
        enemy_battle_info_label = tk.Label(master=battle_window, textvariable=enemy_battle_info, bg="#222831", fg="#EEEEEE",font=("Arial", 15))
        enemy_battle_info_label.grid(row= 2 , column= 3, pady=60, sticky="s")

    else:
        control_var.set("Hace falta el nombre o el tipo de personaje")


# Crear widgets
title_game = tk.Label(app, text="TWO ENEMIES GAME", font=("Roboto", 30), bg="#222831", fg="#EEEEEE")
title_game.grid(row=1, column=1, padx=20, pady=20, sticky="n")

label = tk.Label(app, text="Elige un nombre y una clase", font=("Arial", 14), bg="#222831", fg="#EEEEEE")
label.grid(row=2, column=1, padx=20, pady=20)

# Seleccionar clase y nombre
button_wizard = tk.Button(app, text="Mago", bg="#76ABAE", fg="#31363F", width=20, height=2, font=("Arial", 17),
                          borderwidth=1,
                          command=lambda: get_class("Mago"))
button_wizard.grid(row=3, column=0, padx=20, pady=20)

button_warrior = tk.Button(app, text="Guererro", bg="#76ABAE", fg="#31363F", width=20, height=2, font=("Arial", 17),
                           borderwidth=1,
                           command=lambda: get_class("Guerrero"))
button_warrior.grid(row=3, column=2, padx=20, pady=20)

text_name = tk.Entry(app, width=30, justify='center', font=("Arial", 16), textvariable=entry)
text_name.insert(0, "")
text_name.grid(row=3, column=1, padx=20, pady=20)

#Variables de control
info_player = tk.StringVar()
info = tk.Label(app, text=" ", font=("Arial", 14), bg="#222831", fg="#EEEEEE", textvariable=info_player)
info.grid(row=4, column=1, padx=20, pady=20)

button_send = tk.Button(app, text="Iniciar Aventura!", bg="#76ABAE", fg="#31363F", width=20, height=2, font=("Arial", 17),
                           borderwidth=1, command=lambda: start_battle(type_class.get(), entry.get()))
button_send.grid(row=5, column=1, padx=20, pady=20)

control = tk.Label(app, text=" ", font=("Arial", 14), bg="#222831", fg="#EEEEEE", textvariable=control_var)
control.grid(row=6, column=1, padx=20, pady=20)

app.mainloop()