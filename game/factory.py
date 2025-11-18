from .entities import Enemy


class EnemyFactory:
    def create(self):
        return Enemy()


class Spawner:
    def __init__(self, all_group, enemies_group, delay=500):
        self.all_group = all_group
        self.enemies_group = enemies_group
        self.delay = delay
        self.last_spawn = 0
        self.factory = EnemyFactory()

    def update(self, now):
        if now - self.last_spawn >= self.delay:
            enemy = self.factory.create()
            self.all_group.add(enemy)
            self.enemies_group.add(enemy)
            self.last_spawn = now