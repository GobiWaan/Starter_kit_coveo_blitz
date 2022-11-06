from game_message import Tick, Action, Spawn, Sail, Dock, Anchor, directions

# Tick has form :
# {
#   currentTick: number;
#   totalTicks: number;
#   currentLocation: Position | null;
#   spawnLocation: Position | null;
#   map: {
#     topology: number[][];
#     tideLevels: {
#       max: number;
#       min: number;
#     },
#     ports: Position[];
#   };
#   visitedPortIndices: number[];
#   tideSchedule: number[];
#   isOver: boolean;
# }



class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        # find nearest dock - > choose fastest route {predict tide movement -> }-> start moving 
    def _find_nearest_dock(tick: Tick) -> directions:
        pass
    def get_next_move(self, tick: Tick) -> Action:
        """
        Here is where the magic happens, for now the move is random. I bet you can do better ;)
        """
        if tick.currentLocation is None:
            return Spawn(tick.map.ports[0])
        
        return Sail(directions[tick.currentTick % len(directions)])
