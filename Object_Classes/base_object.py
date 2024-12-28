import pygame
import constants

# Define our generic object class
# give it all the properties and methods of pygame.sprite.Sprite
class BaseObject(pygame.sprite.Sprite):
    def __init__(self, sprite, position, object_type):
        super(BaseObject, self).__init__()
        self.position = position
        self.object_type = object_type
                     
        # creates the visible texture
        self.sprite = pygame.image.load(sprite).convert_alpha()
        
        # creates the "hit-box"
        self.rect = self.sprite.get_rect(center=self.position)

        # adds object to a list of objects
        self.add_to_game_object_list()

    def add_to_game_object_list(self):
        constants.game.objects.append(self)

    def move(self, direction):
        self.position += direction
        self.rect.center = self.position # Update the rect position

    # updates the sprite
    def update(self):
        pygame.sprite.Sprite.update(self)
     
    # draws the object on the screen
    def draw(self):
        constants.game.screen.blit(self.sprite, self.rect.topleft - constants.game.camera)

    def delete_from_game_object_list(self):
        constants.game.objects.remove(self)

    # decides what happens when an object is interacted with
    def on_interact(self, Object):
        if Object.ObjectType == 3:
            self.delete_from_game_object_list()