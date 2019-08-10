import gamelib
import random
import math
import warnings
from sys import maxsize

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

Additional functions are made available by importing the AdvancedGameState 
class from gamelib/advanced.py as a replacement for the regular GameState class 
in game.py.

You can analyze action frames by modifying algocore.py.

The GameState.map object can be manually manipulated to create hypothetical 
board states. Though, we recommended making a copy of the map to preserve 
the actual current map state.
"""


class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()
        self.attack_parity = True

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]


    # Returns a score, where a higher score indicates more enemy units close by the path
    def get_cost_of_path(self, game_state, start_location):
        path = game_state.find_path_to_edge(start_location, game_state.game_map.TOP_LEFT)
        if path is None:
            return None

        score = 0
        THRESHOLD = 5

        for coord in path:
            for x in range(0, 28):
                for y in range(14, 28):
                    if game_state.game_map.in_arena_bounds([x,y]) and game_state.contains_stationary_unit([x,y]) and game_state.game_map.distance_between_locations(coord, [x,y]) < THRESHOLD:
                        score += 1
        return score

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.starter_strategy(game_state)

        game_state.submit_turn()

    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """
    def starter_strategy(self, game_state):
        """
        Then build additional defenses.
        """
        self.build_defences(game_state)

        """
        Finally deploy our information units to attack.
        """
        self.deploy_attackers(game_state)

    def build_defences(self, game_state):
        wall_pieces = [
                # Initial destructors (high priority)
                (DESTRUCTOR, (3, 11), (0, 1)), # type, position, priority (lower is better)
                (DESTRUCTOR, (9, 11), (0, 1)),
                (DESTRUCTOR, (14, 11), (0, 1)),
                (DESTRUCTOR, (19, 11), (0, 1)),
                (DESTRUCTOR, (24, 11), (0, 1)),

                # Edge guards (highest priority)
                (FILTER, (0, 13), (0, 0)),
                (FILTER, (1, 12), (0, 0)),
                (FILTER, (27, 13), (0, 0)),
                (FILTER, (26, 12), (0, 0)),

                # Initial side filters (high priority)
                (FILTER, (2, 11), (0, 2)),
                (FILTER, (8, 11), (0, 2)),
                (FILTER, (13, 11), (0, 2)),
                (FILTER, (15, 11), (0, 2)),
                (FILTER, (20, 11), (0, 2)),
                (FILTER, (21, 11), (0, 2)),
                (FILTER, (25, 11), (0, 2)),
                (FILTER, (25, 12), (0, 2)),
                (FILTER, (26, 13), (0, 2)),

                # Secondary edge destructors
                (DESTRUCTOR, (5, 11), (1, 0)),
                (DESTRUCTOR, (22, 11), (1, 0)),

                # Secondary edge guards
                (FILTER, (23, 11), (1, 1)),
                (FILTER, (26, 12), (2, 0)),

                # Middle filters
                (FILTER, (7, 11), (1, 2)),
                (FILTER, (10, 11), (1, 2)),
                (FILTER, (11, 11), (1, 2)),
                (FILTER, (12, 11), (1, 2)),
                (FILTER, (13, 11), (1, 2)),
                (FILTER, (15, 11), (1, 2)),
                (DESTRUCTOR, (16, 11), (1, 2)),
                (FILTER, (17, 11), (1, 2)),
                (FILTER, (18, 11), (1, 2)),

                # Encryptors
                (ENCRYPTOR, (8, 9), (1, 1)),
                (ENCRYPTOR, (5, 9), (2, 1)),
                (ENCRYPTOR, (6, 9), (2, 2)),
                (ENCRYPTOR, (7, 9), (2, 3)),
                (ENCRYPTOR, (3, 12), (3, 0)),

                # Left hole
                (DESTRUCTOR, (6, 11), (2, 0)),
                (DESTRUCTOR, (4, 9), (2, 1)),
                (DESTRUCTOR, (2, 12), (2, 1)),
                (DESTRUCTOR, (3, 10), (2, 1)),
                (DESTRUCTOR, (1, 13), (2, 0)),
                (FILTER, (2, 13), (2, 0)),
                (FILTER, (3, 13), (2, 0)),
                (FILTER, (4, 13), (2, 0)),
                (FILTER, (5, 13), (2, 2)),
                (FILTER, (6, 13), (2, 2)),
                (DESTRUCTOR, (7, 13), (2, 3)),
                (FILTER, (8, 13), (2, 3)),
                (FILTER, (9, 13), (2, 3)),
                (DESTRUCTOR, (10, 13), (2, 3)),
                (FILTER, (11, 13), (2, 3)),
                (FILTER, (12, 13), (2, 3)),
                (FILTER, (13, 13), (2, 3)),
                (FILTER, (14, 13), (2, 3)),
                (FILTER, (15, 13), (2, 3)),
                (DESTRUCTOR, (16, 13), (2, 3)),
                (FILTER, (17, 13), (2, 3)),
                (FILTER, (18, 13), (2, 3)),
                (FILTER, (19, 13), (2, 3)),
                (DESTRUCTOR, (20, 13), (2, 3)),
        ]
        wall_pieces.sort(key = lambda x: x[2])

        for (_type, location, _) in wall_pieces:
            if game_state.get_resource(game_state.CORES) < game_state.type_cost(_type):
                break

            if game_state.can_spawn(_type, location):
                game_state.attempt_spawn(_type, location)

    def deploy_attackers(self, game_state):
        if (game_state.get_resource(game_state.BITS) < 9):
            return

        locs = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        loc_costs = []
        for loc in locs:
            cost = self.get_cost_of_path(game_state, loc)
            if cost != None:
                loc_costs.append([loc, cost])

        if self.attack_parity:
            loc = min(loc_costs, key=lambda x: x[1])[0]
            while game_state.can_spawn(PING, loc):
                game_state.attempt_spawn(PING, loc)
        else:
#            if game_state.can_spawn(SCRAMBLER, [19, 5], 2):
#                game_state.attempt_spawn(SCRAMBLER, [19, 5], 2)

            loc = max(loc_costs, key=lambda x: x[1])[0]
            while game_state.can_spawn(EMP, loc):
                game_state.attempt_spawn(EMP, loc)

        self.attack_parity = not self.attack_parity

        """
        First lets check if we have 10 bits, if we don't we lets wait for 
        a turn where we do.
        """
        """
        if self.attack_parity:

            while game_state.can_spawn(PING, [6, 7]):
                game_state.attempt_spawn(PING, [6, 7])
        else:
            if (game_state.get_resource(game_state.BITS) < 9):
                return
#            if game_state.can_spawn(SCRAMBLER, [19, 5], 2):
#                game_state.attempt_spawn(SCRAMBLER, [19, 5], 2)

            while game_state.can_spawn(EMP, [21, 7]):
                game_state.attempt_spawn(EMP, [21, 7])
        self.attack_parity = not self.attack_parity
        """

        """
        NOTE: the locations we used above to spawn information units may become 
        blocked by our own firewalls. We'll leave it to you to fix that issue 
        yourselves.

        Lastly lets send out Scramblers to help destroy enemy information units.
        A complex algo would predict where the enemy is going to send units and 
        develop its strategy around that. But this algo is simple so lets just 
        send out scramblers in random locations and hope for the best.

        Firstly information units can only deploy on our edges. So lets get a 
        list of those locations.
        """
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        
        """
        Remove locations that are blocked by our own firewalls since we can't 
        deploy units there.
        """
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)
        
        """
        While we have remaining bits to spend lets send out scramblers randomly.
        """
        while game_state.get_resource(game_state.BITS) >= game_state.type_cost(SCRAMBLER) and len(deploy_locations) > 0:
           
            """
            Choose a random deploy location.
            """
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]
            
            game_state.attempt_spawn(SCRAMBLER, deploy_location)
            """
            We don't have to remove the location since multiple information 
            units can occupy the same space.
            """
        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location) and not location in [[17,3], [19,5], [18, 4]]:
                filtered.append(location)
        return filtered

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
