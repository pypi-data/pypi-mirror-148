from typing import Optional

from math import floor

import tcod.event

from hunter_pkg import player_actions as pact
from hunter_pkg import flogging
from hunter_pkg import log_level


flog = flogging.Flogging.get(__file__, log_level.LogLevel.get(__file__))

class InputHandler(tcod.event.EventDispatch[pact.PlayerAction]):
    def ev_quit(self, input: tcod.event.Quit):
        raise SystemExit()

    def ev_keydown(self, input: tcod.event.KeyDown):
        player_action: Optional[pact.PlayerAction] = None

        key = input.sym

        if key == tcod.event.K_UP:
            player_action = pact.ScrollUpPlayerAction()
        elif key == tcod.event.K_DOWN:
            player_action = pact.ScrollDownPlayerAction()
        elif key == tcod.event.K_LEFT:
            player_action = pact.ScrollLeftPlayerAction()
        elif key == tcod.event.K_RIGHT:
            player_action = pact.ScrollRightPlayerAction()
        elif key == tcod.event.K_h:
            player_action = pact.ToggleUIPlayerAction()
        elif key == tcod.event.K_f:
            player_action = pact.ToggleVisionPlayerAction()
        elif key == tcod.event.K_p or key == tcod.event.K_SPACE:
            player_action = pact.TogglePausePlayerAction()
        elif key == tcod.event.K_ESCAPE:
            player_action = pact.EscapePlayerAction()
        elif key == tcod.event.K_e:
            player_action = pact.ToggleEntityOverviewAction()
        elif key == tcod.event.K_2:
            player_action = pact.IncreaseGameSpeedPlayerAction()
        elif key == tcod.event.K_1:
            player_action = pact.DecreaseGameSpeedPlayerAction()
        elif key == tcod.event.K_F9:
            player_action = pact.DumpProfilerAction()

        return player_action

    def ev_mousemotion(self, input: tcod.event.MouseMotion):
        x = input.pixel[0]
        y = input.pixel[1]

        return pact.MouseMovementPlayerAction(x, y)

    def ev_mousebuttonup(self, input: tcod.event.MouseButtonUp):
        return pact.MouseUpPlayerAction()
