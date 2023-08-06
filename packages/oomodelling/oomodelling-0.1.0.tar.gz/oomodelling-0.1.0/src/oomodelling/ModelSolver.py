import logging
import numpy as np
from scipy.integrate import solve_ivp, RK45
from oomodelling.Model import Model


class ModelSolver:
    def __init__(self):
        super().__init__()
        self._l = logging.getLogger("ModelSolver")

    def simulate(self, model: Model, start_t: float, stop_t: float, comm_step: float, max_solver_step: float = None, t_eval=None):
        if max_solver_step is None:
            self._l.warning("It is recommended to define max_solver_step, as this affects the accuracy with which the communication times occur. "
                                    "For now i'm assuming that max_solver_step=comm_step/10.0 .")
            max_solver_step = comm_step/10.0
        if max_solver_step >= comm_step:
            self._l.warning(
                "solver_step_size >= comm_step_size. It is recommended that solver_step_size < comm_step_size. "
                "For example: solver_step_size = comm_step_size/10.")
        model.set_time(start_t)
        model.assert_initialized()
        f = model.derivatives()
        x = model.state_vector()
        # Record first time.
        model.record_state(x, start_t)
        sol = solve_ivp(f, (start_t, stop_t), x, method=StepRK45, comm_step_size=comm_step,
                        max_step=max_solver_step, model=model, t_eval=t_eval)
        if not sol.success:
            raise ValueError(sol)
        if t_eval is not None:
            expected = len(t_eval)
            results_len = len(sol.y[0])
            assert expected == results_len, f"t_eval was ignored. Expected {expected} results. " \
                                            f"Got {results_len} instead. " \
                                            "This is a problem with scipy solver or you used the wrong type for t_eval."
            model_signals = len(model.signals["time"])
            if not expected == model_signals:
                self._l.info(f"The signals attribute is computed based on max_step and not based on t_eval. "
                             f"Therefore model.signals contains {model_signals} points and t_eval contains {expected} points."
                             f"Using t_eval implies that you rely on sol.y instead of the stored signals.")

        return sol


class StepRK45(RK45):

    def __init__(self, fun, t0, y0, t_bound, max_step=np.inf,
                 rtol=1e-3, atol=1e-6, vectorized=False,
                 first_step=None, **extraneous):
        assert max_step < np.inf, "Max step is infinity."
        self._model: Model = extraneous.pop('model')
        self._comm_step_size = extraneous.pop('comm_step_size')
        super().__init__(fun, t0, y0, t_bound, max_step=max_step,
                         rtol=rtol, atol=atol, vectorized=vectorized,
                         first_step=first_step, **extraneous)

    def step(self):
        msg = super().step()
        if msg is not None:
            raise ValueError(msg)
        step_taken = self.t - self._model.get_last_commit_time()
        if step_taken >= self._comm_step_size:
            update_state = self._model.discrete_step()
            if update_state:
                self.y = self._model.state_vector()
            """
            Record the state after the discrete_step is taken.
            This is because, if we have a step function on a control signal, we want to record the values that will be given to the continuous solver.
            The alternative is to record the signals before the discrete_step happens. 
            The problem with the alternative is that we could not see the step at time t, but that step happens and becomes an input to the continuous solver.
            The result is a plot that shows only shows the step (that happened at time t), at time t+H, 
            but the effects of the step (that happened at time t) on the continuous state can already be seen at time t+H.
            So the results seem to show that the step only happened at time t+H, 
            but its effects can already be seen at time t+H, without any time passing, which is a causality violation.
            """
            self._model.record_state(self.y, self.t)
            assert np.isclose(self.t, self._model.get_last_commit_time()), "Commit was made to the model."
