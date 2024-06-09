# Main renderer class should contain:
# -> list of all layers, and their corresponding postprocessing effects.

# Layers have an index, that decides when they are rendered (ie. descending order, so layer 0 is the final one rendered

import pygame
import operator

from BASE_GAME_FILES.scripts.AestheticSystems import PostProcessing_Renderer


class RenderLayer:
    def __init__(self, layer_index, PP_Effects: list[str], layer_size):
        self.index = layer_index
        self.layer_size = layer_size
        self.display = None
        self.reset_layer()

        self.post_processing_renderer: PostProcessing_Renderer = PostProcessing_Renderer(self.display, PP_Effects)

    def reset_layer(self):
        self.display = pygame.Surface((self.layer_size[0] / 2, self.layer_size[1] / 2)).convert_alpha()
        self.display.fill([0, 0, 0, 0])

    def render_post_processing(self):
        self.post_processing_renderer.RenderEffects()


class Renderer:
    def __init__(self, number_layers, global_post_processing_effects: list[str], gameSpecs, usePP):
        self.use_pp = usePP
        self.game_specs = gameSpecs

        self.layers: list[RenderLayer] = []
        for index in range(number_layers):
            self.add_layer(RenderLayer(index, [], self.game_specs.SIZE))
        self.layers = self.sort_layers()

        self.post_processing_renderer: PostProcessing_Renderer = PostProcessing_Renderer(self.layers[0].display, global_post_processing_effects)

    def sort_layers(self) -> list[RenderLayer]:
        return sorted(self.layers, key=operator.attrgetter('index'))

    def render_frame(self):
        for layer in self.layers[::-1]:
            if self.use_pp: layer.post_processing_renderer.RenderEffects()
            self.game_specs.screen.blit(pygame.transform.scale(layer.display, self.game_specs.screen.get_size()), (0, 0))
            layer.reset_layer()
        if self.use_pp: self.post_processing_renderer.RenderEffects()
        pygame.display.update()

    def add_layer(self, layer: RenderLayer):
        if any(layer.index == _layer.index for _layer in self.layers):
            return
        self.layers.append(layer)
        self.layers = self.sort_layers()

    def remove_layer(self, layer_index):
        for layer in self.layers:
            if layer.index == layer_index:
                self.layers.remove(layer)
                self.layers = self.sort_layers()
                break
