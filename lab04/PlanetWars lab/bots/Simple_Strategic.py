class Simple_Strategic(object):

    def update(self, gameinfo):
        # Do nothing if there are more than 5 fleets
        if len(gameinfo.my_fleets) > 5:
            return
            pass

        if gameinfo.my_planets and gameinfo.not_my_planets:
            # print(gameinfo.my_planets)
            # choose planet with the most ships to sortie from
            src = max(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            # choose planet with the worst defence to attack
            dest = min(gameinfo.not_my_planets.values(), key = lambda p: p.num_ships)
            gameinfo.planet_order(src, dest, int(src.num_ships * 0.5))
            gameinfo.log("I'll send %d ships from planet %s to planet %s" % (src.num_ships, src, dest))
