import pygame
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):

    images = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY = False, False
        self.DOWN_KEY, self.UP_KEY = False, False
        self.on_ground = True
        self.frictionx = -.12
        self.frictiony = -.12
        self.images.append(Spritesheet('spritesheet.png').parse_sprite('gato1.png'))
        self.images.append(Spritesheet('spritesheet.png').parse_sprite('1otag.png'))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.position, self.velocity = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.facing = -1

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt, tiles, direction):
        self.horizontal_movement(dt, direction)
        self.checkCollisionsx(tiles)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles)

    def horizontal_movement(self,dt,direction):
        if direction:
            self.facing = direction

        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
            
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= .3
        elif self.RIGHT_KEY:
            self.acceleration.x += .3
        self.acceleration.x += self.velocity.x * self.frictionx
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(1.5)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x


    def vertical_movement(self,dt):
        self.acceleration.y = 0
        if self.UP_KEY:
            self.acceleration.y -= .3
        elif self.DOWN_KEY:
            self.acceleration.y += .3
        self.acceleration.y += self.velocity.y * self.frictiony
        self.velocity.y += self.acceleration.y * dt
        self.limit_velocity(1.5)
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.y = self.position.y

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def limit_velocity(self, max_vel):
        self.velocity.y = max(-max_vel, min(self.velocity.y, max_vel))
        if abs(self.velocity.y) < .01: self.velocity.y = 0

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisionsx(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    def checkCollisionsy(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:  # Hit tile moving up
                self.position.y = tile.rect.top - self.rect.h
                self.rect.y = self.position.y
            elif self.velocity.y < 0:  # Hit tile moving down
                self.position.y = tile.rect.bottom
                self.rect.y = self.position.y
