import math

import numpy as np

from oomodelling import ModelSolver, Model

HEATER_VOLTAGE = 12.0
HEATER_CURRENT = 10.45


class SystemModel4ParametersOpenLoopSimulator:
    def run_simulation(self, t0, tf,
                       # Initial state
                       initial_T, initial_T_heater, initial_room_T,
                       # Controller parameters
                       n_samples_heating: int, n_samples_period: int, controller_step_size: float,
                       # Plant parameters
                       C_air, G_box, C_heater, G_heater):
        model = SystemModel4ParametersOpenLoop(n_samples_period, n_samples_heating,
                                               C_air, G_box, C_heater, G_heater,
                                               initial_T, initial_T_heater)

        # Wire the lookup table to the _plant
        model.plant.in_room_temperature = lambda: initial_room_T

        # Run simulation
        sol = ModelSolver().simulate(model, t0, tf, controller_step_size, controller_step_size / 10.0)

        # Return model that has the results
        return model


class SystemModel4ParametersOpenLoop(Model):
    def __init__(self,
                 # Controller parameters
                 n_samples_period, n_samples_heating,
                 # Plant parameters
                 C_air,
                 G_box,
                 C_heater,
                 G_heater,
                 initial_box_temperature=35,
                 initial_heat_temperature=35,
                 initial_room_temperature=21):
        super().__init__()

        self.ctrl = ControllerOpenLoop(n_samples_period, n_samples_heating)
        self.plant = FourParameterIncubatorPlant(initial_room_temperature=initial_room_temperature,
                                                 initial_box_temperature=initial_box_temperature,
                                                 initial_heat_temperature=initial_heat_temperature,
                                                 C_air=C_air,
                                                 G_box=G_box,
                                                 C_heater=C_heater,
                                                 G_heater=G_heater)

        self.plant.in_heater_on = self.ctrl.heater_on

        self.save()


class PlantSimulator4Params:
    def run_simulation(self, timespan_seconds, initial_box_temperature, initial_heat_temperature,
                       room_temperature, heater_on,
                       C_air, G_box, C_heater, G_heater, controller_step_size):
        timetable = np.array(timespan_seconds)

        room_temperature_fun = create_lookup_table(timetable, np.array(room_temperature))
        heater_on_fun = create_lookup_table(timetable, np.array(heater_on))

        model = FourParameterIncubatorPlant(initial_room_temperature=room_temperature[0],
                                            initial_box_temperature=initial_box_temperature,
                                            initial_heat_temperature=initial_heat_temperature,
                                            C_air=C_air, G_box=G_box,
                                            C_heater=C_heater, G_heater=G_heater)
        model.in_room_temperature = lambda: room_temperature_fun(model.time())
        model.in_heater_on = lambda: heater_on_fun(model.time())

        start_t = timespan_seconds[0]
        end_t = timespan_seconds[-1]

        sol = ModelSolver().simulate(model, start_t, end_t + controller_step_size, controller_step_size,
                                     controller_step_size / 10.0,
                                     t_eval=timespan_seconds)
        return sol, model


def find_closest_idx(t, start_idx, time_range):
    assert start_idx >= 0
    idx = start_idx

    maxIdx = len(time_range)

    # Search backward
    while time_range[idx] > t and idx > 0:
        idx = idx - 1

    assert time_range[idx] <= t, f"{t}, {start_idx}, {idx}, {time_range[idx]}, {time_range[-1]}"

    # Search forward
    while (idx + 1) < maxIdx and time_range[idx + 1] <= t:
        idx = idx + 1

    assert idx < maxIdx
    assert time_range[idx] <= t < (time_range[idx + 1] if (idx + 1 < maxIdx) else math.inf)

    return idx


def create_lookup_table(time_range, data):
    """
    Implements an efficient lookup table.
    Uses the last_idx as a memory of the last request.
    Assumes that t is mostly increasing.
    """
    assert type(time_range) is np.ndarray, "Recommended to use numpy arrays for performance reasons."
    assert type(data) is np.ndarray, "Recommended to use numpy arrays for performance reasons."

    last_idx = 0

    def signal(t):
        nonlocal last_idx  # See http://zetcode.com/python/python-closures/
        last_idx = find_closest_idx(t, last_idx, time_range)
        return data[last_idx]  # constant extrapolation

    return signal


class ControllerOpenLoop(Model):
    def __init__(self,
                 n_samples_period,  # Total number of samples considered
                 n_samples_heating,  # Number of samples (out of n_samples_period) that the heater is on.
                 ):
        assert 0 < n_samples_period
        assert 0 <= n_samples_heating <= n_samples_period
        super().__init__()

        self.param_n_samples_heating = n_samples_heating
        self.param_n_samples_period = n_samples_period

        self.n_samples_heating = self.input(lambda: self.param_n_samples_heating)
        self.n_samples_period = self.input(lambda: self.param_n_samples_period)

        self.state_machine = ControllerOpenLoopSM(self.param_n_samples_period, self.param_n_samples_heating)
        self.cached_heater_on = False

        self.heater_on = self.var(lambda: self.cached_heater_on)

        self.save()

    def discrete_step(self):
        self.state_machine.step()
        self.cached_heater_on = self.state_machine.cached_heater_on
        return super().discrete_step()

    def reset_params(self, n_samples_heating, n_samples_period):
        self.param_n_samples_heating = n_samples_heating
        self.param_n_samples_period = n_samples_period
        self.state_machine = ControllerOpenLoopSM(self.param_n_samples_period, self.param_n_samples_heating)
        self.cached_heater_on = False


class ControllerOpenLoopSM():
    def __init__(self,
                 n_samples_period,  # Total number of samples considered
                 n_samples_heating,  # Number of samples (out of n_samples_period) that the heater is on.
                 ):
        assert 0 < n_samples_period
        assert 0 <= n_samples_heating <= n_samples_period

        self.n_samples_heating = n_samples_heating
        self.n_samples_period = n_samples_period

        self.current_state = "Initialized"
        # Holds the next sample for which an action has to be taken.
        self.next_action_timer = -1.0
        self.cached_heater_on = False

    def step(self):
        if self.current_state == "Initialized":
            self.cached_heater_on = False
            if 0 < self.n_samples_heating:
                self.current_state = "Heating"
                self.next_action_timer = self.n_samples_heating
            else:
                assert self.n_samples_heating == 0
                self.current_state = "Cooling"
                self.next_action_timer = self.n_samples_period - self.n_samples_heating
            return
        if self.current_state == "Heating":
            assert self.next_action_timer >= 0
            if self.next_action_timer > 0:
                self.cached_heater_on = True
                self.next_action_timer -= 1
            if self.next_action_timer == 0:
                self.current_state = "Cooling"
                self.next_action_timer = self.n_samples_period - self.n_samples_heating
            return
        if self.current_state == "Cooling":
            assert self.next_action_timer >= 0
            if self.next_action_timer > 0:
                self.cached_heater_on = False
                self.next_action_timer -= 1
            if self.next_action_timer == 0:
                self.current_state = "Heating"
                self.next_action_timer = self.n_samples_heating
            return


class TwoParameterIncubatorPlant(Model):
    def __init__(self, initial_heat_voltage=HEATER_VOLTAGE, initial_heat_current=HEATER_CURRENT,
                 initial_room_temperature=25.0, initial_box_temperature=25.0,
                 C_air=1.0, G_box=1.0):
        super().__init__()

        self.in_heater_on = self.input(lambda: False)
        self.in_heater_voltage = self.input(lambda: initial_heat_voltage)
        self.in_heater_current = self.input(lambda: initial_heat_current)
        self.in_room_temperature = self.input(lambda: initial_room_temperature)

        self.power_in = self.var(
            lambda: self.in_heater_voltage() * self.in_heater_current() if self.in_heater_on() else 0.0)

        self.G_box = self.input(lambda: G_box)
        self.C_air = self.input(lambda: C_air)

        self.T = self.state(initial_box_temperature)

        self.power_out_box = self.var(lambda: self.G_box() * (self.T() - self.in_room_temperature()))

        self.total_power_box = self.var(lambda: self.power_in() - self.power_out_box())

        self.der('T', lambda: (1.0 / self.C_air()) * (self.total_power_box()))

        self.save()


class FourParameterIncubatorPlant(TwoParameterIncubatorPlant):
    def __init__(self,
                 initial_heat_voltage=HEATER_VOLTAGE, initial_heat_current=HEATER_CURRENT,
                 initial_room_temperature=21.0, initial_box_temperature=25.0,
                 initial_heat_temperature=25.0,
                 C_air=1.0, G_box=1.0,
                 C_heater=1.0, G_heater=1.0):
        # Initialize 2p stuff
        super(FourParameterIncubatorPlant, self).__init__(initial_heat_voltage, initial_heat_current,
                                                          initial_room_temperature, initial_box_temperature, C_air,
                                                          G_box)

        self.edit()  # Go into edit mode

        self.C_heater = self.parameter(C_heater)
        self.G_heater = self.parameter(G_heater)

        self.T_heater = self.state(initial_heat_temperature)

        self.power_transfer_heat = self.var(lambda: self.G_heater * (self.T_heater() - self.T()))

        self.total_power_heater = self.var(lambda: self.power_in() - self.power_transfer_heat())

        # Override equation of TwoParameterIncubatorPlant
        self.total_power_box = self.ovar(lambda: self.power_transfer_heat() - self.power_out_box())

        self.der('T_heater', lambda: (1.0 / self.C_heater) * (self.total_power_heater()))

        self.save()  # Close edit mode
