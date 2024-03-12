import random

class Character:
    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.health_before_attack = 100
        self.damage = 7
        self.special_damage = 7
        self.defense = 20
        self.special_defense = 5

    def calculate_damage(self, base_damage: int, defense: int, is_special_attack: bool) -> float:
        # Seleccionar el tipo de daño (normal o especial)
        damage = self.special_damage if is_special_attack else self.damage

        # Calcular probabilidad de crítico
        crit_chance = random.random()
        crit_probability = 0.2

        # Aplicar daño crítico si se cumple la probabilidad
        if crit_chance < crit_probability:
            damage *= 2

        # Calcular daño final teniendo en cuenta la defensa del objetivo
        final_damage = max(0, (damage / defense) * base_damage)
        return final_damage

    def attack(self, entity, is_special_attack=False) -> None:
        entity.health_before_attack = entity.health
        entity.health -= self.calculate_damage(self.damage, entity.defense, is_special_attack)

    def special_attack(self, entity) -> None:
        entity.health_before_attack = entity.health
        entity.health -= self.calculate_damage(self.special_damage, entity.special_defense, True)
    
class warrior(Character):
    def __init__(self,name: str):
        super().__init__(name)
        self.health = 120
        self.max_health = 120
        self.health_before_attack = 120
        self.damage = 15
        self.special_damage = 5
        self.defense = 15
        self.special_defense = 5

class wizard(Character):
    def __init__(self, name: str):
        super().__init__(name)
        self.health = 100
        self.max_health = 100
        self.health_before_attack = self.max_health
        self.damage = 9
        self.special_damage = 12
        self.defense = 12
        self.special_defense = 15

class normal_monster(Character):
    def __init__(self, name: str):
        super().__init__(name)
        self.health = 100
        self.max_health = 100
        self.health_before_attack = self.max_health
        self.damage = 9
        self.special_damage = 10
        self.defense = 10
        self.special_defense = 10

class super_monster(Character):
    def __init__(self):
        super().__init__("Super Goblin")
        self.health = 150
        self.max_health = 150
        self.health_before_attack = self.max_health
        self.damage = 15
        self.special_damage = 15
        self.defense = 15
        self.special_defense = 15