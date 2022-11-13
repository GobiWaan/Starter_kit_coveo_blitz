#!/usr/bin/env python
import os
import json
import numpy as np
import sys

from bot import Bot
from game_message import Tick, Map, Position, TideLevels, directions


class Game:
    def __init__(self, game_file_txt: str):
        self.visited_ports = []

        self.current_tick = 0

        self.ship_spawn_location = None
        self.ship_position = None
        
        self.load_constant_values_from_game_file(game_file_txt)

    def load_constant_values_from_game_file(self, game_file_txt: str):
        with open(game_file_txt, 'r') as f:
            fs = f.readlines()
            first_line = fs[0]
            data = json.loads(first_line)

            # Load map height values
            self.topology = np.array(data['map']['topology'])
            # Load locations of ports
            self.ports = data['map']['ports']
            # Load tide levels
            self.tide_max = data['map']["tideLevels"]['max']
            self.tide_min = data['map']["tideLevels"]['min']
            # Load water levels
            self.water_levels_for_every_tick = [json.loads(i)['tideSchedule'] for i in fs]

    def get_tick(self):
        tick = Tick(
            currentTick=self.current_tick,
            totalTicks=400,
            map=Map(
                topology=self.topology.tolist(),
                ports=[Position(**i) for i in self.ports],
                tideLevels=TideLevels(max=self.tide_max, min=self.tide_min),
            ),
            currentLocation=self.ship_position if self.ship_position else None,
            spawnLocation=self.ship_spawn_location if self.ship_spawn_location else None,
            visitedPortIndices=self.visited_ports,
            tideSchedule=self.water_levels_for_every_tick[self.current_tick],
            isOver=False
        )

        return tick

    def increase_tick(self):
        self.current_tick += 1

    def play_action(self, action):
        print(action)
        if action.kind == 'spawn':
            self.ship_spawn_location = action.position
            self.ship_position = action.position
            return True
        elif action.kind == 'sail':
            direction_indices = dict(zip(directions, [
                (-1, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
                (1, 0),
                (1, -1),
                (0, -1),
                (-1, -1)
            ]))[action.direction]
            self.ship_position.row += direction_indices[0]
            self.ship_position.column += direction_indices[1]

            if self.topology[self.ship_position.row][self.ship_position.column] >= self.water_levels_for_every_tick[self.current_tick][0]:
                print("[ERROR] Can't navigate there")
                self.ship_position.row -= direction_indices[0]
                self.ship_position.column -= direction_indices[1]

            return True
        elif action.kind == 'dock':
            self.visited_ports.append(self.ports.index({'row': self.ship_position.row, 'column': self.ship_position.column}))
            return True
        elif action.kind == 'anchor':
            return True
        else:
            return False


if __name__ == '__main__':
    game_file = sys.argv[1]
    game = Game(game_file)
    bot = Bot()
    while True: 
        if not game.play_action(bot.get_next_move(game.get_tick())):
            break
        game.increase_tick()
        if game.current_tick > 400:
            break

