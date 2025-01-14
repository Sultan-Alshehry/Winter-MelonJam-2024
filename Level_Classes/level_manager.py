import constants, pygame
import Object_Classes.tile_class as tiles
from Visual_Effects.effects import CircleScreenTransition, BlockScreenTransition
from Visual_Effects.flash import Flash
from Visual_Effects.pills_effect import TakePills

flash_effect = Flash((50, 0, 0, 50), 80, 40, flash_duration = 35)
pills_effect = TakePills(3000)

class LevelManager:

    def __init__(self, levels_list, main_menu, intro_cutscene, ending_cutscene):
        self.levels = levels_list
        self.current_level = -1
        self.current_scene = 0
        self.last_scene = -1
        self.main_menu = main_menu
        self.intro_scene = intro_cutscene
        self.end_scene = ending_cutscene

        self.level_transition = BlockScreenTransition(30, (0, 0, 0), 0, on_finish=self.load_level)
        self.scene_transition = CircleScreenTransition(60, (0, 0, 0), 50, 70, 8, 1, on_finish=self.load_scene)
        self.end_transition = CircleScreenTransition(60, (0, 0, 0), 50, 70, 8, 1, on_finish=ending_cutscene)

    def load_level(self):
        self.load_scene()

    def load_scene(self):
        if self.current_level == -1:
            return
        game = constants.game
        game.objects.clear()
        game.decorations.clear()
        scene = self.levels[self.current_level].scenes[self.current_scene]
        game.background = pygame.transform.scale(scene.background, (constants.WIDTH, constants.HEIGHT))

        tiles.draw_tile_list(scene.tiles)
        if self.last_scene <= self.current_scene:
            game.player.set_position(scene.player_position)
        else:
            game.player.set_position(scene.player_position_back)
            game.player.direction = "left"
        game.player.transition = False
        if not game.took_pills:
            flash_effect.start()
        if scene.on_load:
            scene.on_load()

    def restart_scene(self):
        self.scene_transition.direction = 0
        self.scene_transition.start()

    def next_scene(self):
        self.last_scene = self.current_scene
        self.current_scene += 1
        if self.current_scene >= len(self.levels[self.current_level].scenes):
            self.next_level()
        else:
            self.scene_transition.direction = 1
            self.scene_transition.start()

    def previous_scene(self):
        if self.current_level == len(self.levels) - 1:
            if constants.game.took_pills:
                self.finish()
            constants.game.player.transition = False
            return
        self.last_scene = self.current_scene
        self.current_scene -= 1
        if self.current_scene < 0:
            self.current_scene = 0
            self.previous_level()
        else:
            self.scene_transition.direction = 0
            self.scene_transition.start()

    def next_level(self):
        self.current_level += 1
        if self.current_level >= len(self.levels):
            self.take_pills()
        else:
            self.current_scene = 0
            self.last_scene = -1
            self.level_transition.direction = 1
            self.level_transition.start()

    def previous_level(self):
        self.current_level -= 1
        if self.current_level < 0:
            self.current_level = 0
            if constants.game.took_pills:
                self.finish()
            #constants.game.player.transition = False
            return
        else:
            self.current_scene = len(self.levels[self.current_level].scenes) - 1
            self.last_scene = self.current_scene + 1
            self.level_transition.direction = 0
            self.level_transition.start()

    def take_pills(self):
        pygame.time.wait(300)
        pills_effect.start()
        self.last_scene += 2
        constants.game.player.transition = False
        constants.game.took_pills = True

    def finish(self):
        constants.game.player.transition = True
        constants.game.player.set_position((0, -100))
        #self.end_transition.start()
        self.end_scene()
