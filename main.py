# --- Imports (se necessário, mas randint é geralmente global no MakeCode Python) ---
# from random import randint # Geralmente não é necessário no MakeCode Arcade Python

# --- Tipos de Sprite ---
# SpriteKind.player já existe
Raindrop = SpriteKind.create()

# --- Variáveis Globais ---
player_sprite: Sprite = None
base_raindrop_speed = 25  # Velocidade inicial das gotas
current_raindrop_speed = base_raindrop_speed
score_for_difficulty_increase = 50  # Aumenta dificuldade a cada X pontos
next_difficulty_increase_score = score_for_difficulty_increase

raindrop_spawn_interval = 2000  # ms (tempo entre novas gotas)
min_raindrop_spawn_interval = 600  # ms (intervalo mínimo de spawn)
spawn_timer = 0  # Contador para o próximo spawn

# --- Configurações Iniciais do Jogo ---
def start_game():
    global player_sprite, current_raindrop_speed, next_difficulty_increase_score
    global raindrop_spawn_interval, spawn_timer

    # Reinicializa variáveis para um novo jogo (caso seja chamado após um game over)
    current_raindrop_speed = base_raindrop_speed
    next_difficulty_increase_score = score_for_difficulty_increase
    raindrop_spawn_interval = 2000
    spawn_timer = 0

    scene.set_background_image(img("""
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
    """))
    # Se quiser um efeito de chuva simples (não tão bom quanto o JS original, mas algo)
    # effects.bubbles.start_screen_effect(500) # Ou star_field, etc.

    player_sprite = sprites.create(img("""
        . . . . . . . . . . . . . . . .
        . . . . . f f f f f f . . . . .
        . . . . f 5 5 5 5 5 5 f . . . .
        . . . f 5 5 5 5 5 5 5 5 f . . .
        . . f 5 5 5 5 5 5 5 5 5 5 f . .
        . f 5 5 5 5 5 5 5 5 5 5 5 5 f .
        . f d d d d d d d d d d d d f .
        . f d d d d d d d d d d d d f .
        . . f f f f f f f f f f f f . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
        . . . . . . . . . . . . . . . .
    """), SpriteKind.player)
    player_sprite.set_position(screen.width // 2, screen.height - 15)
    player_sprite.set_stay_in_screen(True)
    controller.move_sprite(player_sprite, 120, 0)

    info.set_score(0)
    info.set_life(3)

# --- Criar Gotas de Chuva ---
def create_raindrop():
    global current_raindrop_speed
    num1 = randint(1, 9)
    num2 = randint(1, 9)
    operation_type = randint(0, 2)  # 0: Adição, 1: Subtração, 2: Multiplicação
    
    problem_text = ""
    correct_answer = 0

    if operation_type == 0:  # Adição
        problem_text = f"{num1} + {num2}"
        correct_answer = num1 + num2
    elif operation_type == 1:  # Subtração (garantir resultado positivo)
        if num1 < num2:  # Troca os números se num1 for menor
            num1, num2 = num2, num1 # Pythonic swap
        problem_text = f"{num1} - {num2}"
        correct_answer = num1 - num2
    else:  # Multiplicação
        num1 = randint(1, 7)  # Números menores para multiplicação inicial
        num2 = randint(1, 7)
        problem_text = f"{num1} × {num2}"  # Usar '×' para visual
        correct_answer = num1 * num2

    raindrop_sprite = sprites.create(img("""
        . . . . . . . .
        . . . 4 4 . . .
        . . 4 5 5 4 . .
        . 4 5 5 5 5 4 .
        . 4 5 5 5 5 4 .
        . 4 5 5 5 5 4 .
        . 4 4 5 5 4 4 .
        . . 4 4 4 4 . .
    """), Raindrop)

    raindrop_sprite.say(problem_text, raindrop_spawn_interval * 1.5)

    # Armazenar dados na gota para uso posterior
    # MakeCode Python sprites têm um dicionário 'data'
    raindrop_sprite.data["problem"] = problem_text
    raindrop_sprite.data["answer"] = correct_answer
    raindrop_sprite.data["processed"] = False  # Flag para evitar processamento duplo

    raindrop_sprite.set_position(randint(10, screen.width - 10), 0 - raindrop_sprite.height)
    raindrop_sprite.vy = current_raindrop_speed
    raindrop_sprite.set_flag(SpriteFlag.AUTO_DESTROY, True)

# --- Loop Principal para Criar Gotas ---
def on_update_interval():
    global spawn_timer
    if info.life() <= 0:
        return

    spawn_timer += game.event_context().delta_time * 1000 # delta_time é em segundos

    if spawn_timer >= raindrop_spawn_interval:
        create_raindrop()
        spawn_timer = 0 # Reseta o contador
game.on_update(on_update_interval)


# --- Colisão: Jogador coleta Gota ---
def on_player_overlap_raindrop(sprite: Sprite, otherSprite: Sprite):
    global current_raindrop_speed, next_difficulty_increase_score, raindrop_spawn_interval
    
    # Ignorar se a gota já foi processada ou se o jogo acabou
    if otherSprite.data.get("processed") or info.life() <= 0:
        return
    otherSprite.data["processed"] = True # Marcar como processada

    problem = otherSprite.data.get("problem")
    correct_answer = otherSprite.data.get("answer")

    otherSprite.destroy() # Destruir a gota IMEDIATAMENTE

    # Perguntar a resposta ao jogador
    answer_length = len(str(correct_answer))
    if answer_length == 0: # Caso especial para resposta 0, por exemplo.
        answer_length = 1
        
    user_answer = game.ask_for_number(f"Resolva: {problem}?", answer_length)

    if user_answer == correct_answer:
        info.change_score_by(10)
        music.ba_ding.play()
        sprite.say("👍", 300) # Feedback positivo
    else:
        info.change_life_by(-1)
        music.wawawawaa.play() # Som de erro
        sprite.say(f"👎 Era {correct_answer}", 800) # Feedback negativo com resposta

    # Verificar aumento de dificuldade (se o jogador ainda tiver vidas)
    if info.score() >= next_difficulty_increase_score and info.life() > 0:
        current_raindrop_speed += 7
        if raindrop_spawn_interval > min_raindrop_spawn_interval:
            raindrop_spawn_interval -= 200
        next_difficulty_increase_score += score_for_difficulty_increase
sprites.on_overlap(SpriteKind.player, Raindrop, on_player_overlap_raindrop)

# --- Gota atinge o chão (não foi coletada) ---
def on_raindrop_destroyed(destroyed_sprite: Sprite):
    # Só penaliza se a gota NÃO foi processada (ou seja, não coletada pelo jogador)
    # E se o jogador ainda tem vidas.
    if not destroyed_sprite.data.get("processed") and info.life() > 0:
        # Verifica se a gota foi destruída perto da parte inferior da tela
        if destroyed_sprite.bottom >= screen.height - 5: # 5 é uma pequena margem
            info.change_life_by(-1)
            music.power_down.play() # Som de perda
            scene.camera_shake(4, 200) # Efeito de tela tremendo
sprites.on_destroyed(Raindrop, on_raindrop_destroyed)

# --- Game Over ---
def on_life_zero():
    game.over(False, effects.splatter)
info.on_life_zero(on_life_zero)

# --- Iniciar o Jogo ---
start_game()
