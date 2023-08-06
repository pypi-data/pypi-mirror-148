import pytest
import numpy as np
from adannealing import Annealer, AbstractLoss


class WrongLoss:

    def __call__(self, x, y) -> float:
        return (x ** 2 + y ** 2) ** 2 - (x ** 2 + y ** 2)

    def on_fit_start(self, val):
        pass

    def on_fit_end(self, val):
        pass


class WrongLoss2(AbstractLoss):

    # noinspection PyMethodOverriding
    def __call__(self, x, y) -> float:
        return (x ** 2 + y ** 2) ** 2 - (x ** 2 + y ** 2)

    def on_fit_start(self, val):
        pass

    def on_fit_end(self, val):
        pass


class LossFunc(AbstractLoss):

    def __call__(self, w) -> float:
        x = w[0]
        return ((x - 5) * (x - 2) * (x - 1) * x)[0]

    def on_fit_start(self, val):
        pass

    def on_fit_end(self, val):
        pass


class LossFunc2D(AbstractLoss):

    def __call__(self, w) -> float:
        x = w[0]
        y = w[1]
        return ((x - 5) * (x - 2) * (x - 1) * x + 10 * y ** 2)[0]

    def on_fit_start(self, val):
        pass

    def on_fit_end(self, val):
        pass


# noinspection PyTypeChecker
@pytest.mark.parametrize(
    "loss,"
    "weights_step_size,"
    "bounds,"
    "init_states,"
    "temp_0,"
    "temp_min,"
    "alpha,"
    "iterations,"
    "verbose,"
    "expected_error_type,"
    "expected_error_message",
    [
        (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            False,
            TypeError,
            "The loss function must derive from AbstractLoss",
        ),
        (
            WrongLoss(),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            False,
            TypeError,
            "The loss function must derive from AbstractLoss",
        ),
        (
            WrongLoss2(),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            False,
            ValueError,
            "The loss function must accept exactly 1 parameter",
        ),
        (
            LossFunc(),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            False,
            TypeError,
            "'weights_step_size' can not be None",
        ),
        (
            LossFunc(),
            np.array([1]),
            None,
            None,
            None,
            0,
            0.85,
            None,
            False,
            TypeError,
            "'iterations' can not be None",
        ),
        (
            LossFunc(),
            np.array([1]),
            None,
            None,
            None,
            0,
            0.85,
            1000,
            True,
            ValueError,
            "At least one of 'init_states' and 'bounds' must be specified",
        ),
        (
            LossFunc(),
            np.array([1, 1]),
            np.array([-10, 10]),
            None,
            None,
            0,
            0.85,
            1000,
            False,
            ValueError,
            "'bounds' dimension should be (any, 2), got ",
        ),
        (
            LossFunc(),
            np.array([1, 1]),
            np.array([[-10, 10, 0]]),
            None,
            None,
            0,
            0.85,
            1000,
            False,
            ValueError,
            "'bounds' dimension should be (any, 2), got ",
        ),
        (
            LossFunc(),
            np.array([1, 1]),
            np.array([[10, -10]]),
            None,
            None,
            0,
            0.85,
            1000,
            False,
            ValueError,
            "Bounds are not valid",
        ),
        (
            LossFunc(),
            np.array([1, 1]),
            np.array([[-10, 10]]),
            None,
            None,
            0,
            0.85,
            1000,
            False,
            ValueError,
            "Shape of 'weights_step_size' should be (1,)",
        ),
        (
            LossFunc(),
            1,
            np.array([(-10, 10), (-10, 10)]),
            None,
            20,
            0,
            0.85,
            1000,
            True,
            None,
            "",
        ),
        (
            LossFunc(),
            (1, 1),
            np.array([(-10, 10), (-10, 10)]),
            None,
            20,
            0,
            0.85,
            1000,
            True,
            None,
            "",
        ),
        (
            LossFunc(),
            np.array((1, 1)),
            np.array([(-10, 10), (-10, 10)]),
            None,
            20,
            0,
            0.85,
            1000,
            True,
            None,
            "",
        ),
        (
            LossFunc(),
            [1, 1],
            np.array([(-10, 10), (-10, 10)]),
            None,
            20,
            0,
            0.85,
            1000,
            True,
            None,
            "",
        ),
        (
            LossFunc(),
            [1, np.nan],
            np.array([(-10, 10), (-10, 10)]),
            None,
            20,
            0,
            0.85,
            1000,
            True,
            ValueError,
            "can not contain NANs",
        ),
        (
            LossFunc(),
            np.nan,
            np.array([(-10, 10), (-10, 10)]),
            None,
            20,
            0,
            0.85,
            1000,
            True,
            ValueError,
            "can not be NAN",
        ),
        (
            LossFunc(),
            1,
            np.array([(-10, 10), (-10, 10)]),
            np.nan,
            20,
            0,
            0.85,
            1000,
            True,
            ValueError,
            "'init_states' can not be NAN",
        ),
        (
            LossFunc(),
            1,
            np.array([(-10, 10), (-10, 10)]),
            np.array([(-10, 10), (-10, 10)]),
            20,
            0,
            0.85,
            1000,
            True,
            ValueError,
            "'init_states' must be a 1-D numpy array",
        ),
        (
            LossFunc(),
            1,
            np.array([(-10, 10), (-10, 10)]),
            [0, 0],
            20,
            0,
            0.85,
            1000,
            True,
            None,
            "",
        ),
        (
            LossFunc(),
            1,
            np.array([(-10, 10), (-10, 10)]),
            (0, 0),
            20,
            0,
            0.85,
            1000,
            True,
            None,
            "",
        ),
        (
            LossFunc(),
            1,
            np.array([(-10, 10), (-10, 10)]),
            np.array([0, 0]),
            20,
            0,
            0.85,
            1000,
            True,
            None,
            "",
        ),
    ],
)
def test_init(
    loss,
    weights_step_size,
    bounds,
    init_states,
    temp_0,
    temp_min,
    alpha,
    iterations,
    verbose,
    expected_error_type,
    expected_error_message,
):
    if expected_error_type is not None:
        with pytest.raises(expected_error_type) as e:
            _ = Annealer(
                loss,
                weights_step_size,
                bounds,
                init_states,
                temp_0,
                temp_min,
                alpha,
                iterations,
                verbose,
            )
        assert expected_error_message in e.value.args[0]
    else:
        ann = Annealer(
            loss,
            weights_step_size,
            bounds,
            init_states,
            temp_0,
            temp_min,
            alpha,
            iterations,
            verbose,
        )
        assert isinstance(ann.weights_step_size, np.ndarray)
        assert ann.weights_step_size.dtype == float
        assert isinstance(ann.init_states, np.ndarray)
        assert ann.init_states.dtype == float
        assert isinstance(ann.temp_0, float)
        assert isinstance(ann.temp_min, float)
        assert isinstance(ann.alpha, float)
        assert isinstance(ann.verbose, bool)
        assert isinstance(ann.dimensions, int)
        assert isinstance(ann.iterations, int)


@pytest.mark.parametrize(
    "init_states,bounds,acceptance",
    [
        (None, np.array([[0, 6]]), None),
        (None, np.array([[0, 6]]), 0.01),
        (3.0, None, None),
        (3.0, None, 0.01),
        (3.0, np.array([[0, 6]]), None),
        (3.0, np.array([[0, 6]]), 0.01),
    ],
)
def test_fit_1d(init_states, bounds, acceptance):
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        ann = Annealer(loss=LossFunc(), weights_step_size=0.1, init_states=init_states, bounds=bounds, verbose=True)
        w0, lmin, _, _, _, _ = ann.fit(stopping_limit=acceptance)
        print(w0, lmin)
        if (np.isclose(w0, 4.0565, rtol=5e-1, atol=5e-1) and np.isclose(lmin, -24.057, rtol=5e-2, atol=5e-2)) or (
            np.isclose(w0, 0.39904, rtol=5e-1, atol=5e-1) and np.isclose(lmin, -1.7664, rtol=5e-2, atol=5e-2)
        ):
            break
        attempts += 1
    if attempts == max_attempts:
        raise AssertionError("Fit failed")


# @pytest.mark.parametrize(
#     "init_states,bounds,acceptance",
#     [
#         (None, ((0, 5), (-1, 1)), None),
#         (None, ((0, 5), (-1, 1)), 0.01),
#         ((3.0, 0.5), None, None),
#         ((3.0, 0.5), None, 0.01),
#         ((3.0, 0.5), ((0, 5), (-1, 1)), None),
#         ((3.0, 0.5), ((0, 5), (-1, 1)), 0.01),
#     ],
# )
# def test_fit_2d_microcanonical(init_states, bounds, acceptance):
#     attempts = 0
#     max_attempts = 5
#     while attempts < max_attempts:
#         ann = Annealer(loss=loss_func_2d, weights_step_size=0.1, init_states=init_states, bounds=bounds, verbose=True)
#         w0, lmin, _, _, _, _ = ann.fit(stopping_limit=acceptance, annealing_type="microcanonical", iterations=10000)
#         print(w0, lmin)
#         if (
#             np.isclose(w0[0], 4.0565, rtol=5e-1, atol=5e-1)
#             and np.isclose(w0[1], 0, rtol=5e-1, atol=5e-1)
#             and np.isclose(lmin, -24.057, rtol=5e-2, atol=5e-2)
#         ) or (
#             np.isclose(w0[0], 0.39904, rtol=5e-1, atol=5e-1)
#             and np.isclose(w0[1], 0, rtol=5e-1, atol=5e-1)
#             and np.isclose(lmin, -1.7664, rtol=5e-2, atol=5e-2)
#         ):
#             break
#         attempts += 1
#     if attempts == max_attempts:
#         raise AssertionError("Fit failed")


@pytest.mark.parametrize(
    "init_states,bounds,acceptance,schedule,alpha",
    [
        (None, np.array([[0, 5], [-1, 1]]), None, None, 0.85),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, None, 0.85),
        ((3.0, 0.5), None, None, None, 0.85),
        ((3.0, 0.5), None, 0.01, None, 0.85),
        ((3.0, 0.5), np.array([[0, 5], [-1, 1]]), None, None, 0.85),
        ((3.0, 0.5), np.array([[0, 5], [-1, 1]]), 0.01, None, 0.85),
        (None, np.array([[0, 5], [-1, 1]]), None, "linear", 0.5),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, "linear", 0.5),
        ((3.0, 0.5), None, None, "linear", 0.5),
        ((3.0, 0.5), None, 0.01, "linear", 0.5),
        ((3.0, 0.5), np.array([[0, 5], [-1, 1]]), None, "linear", 0.5),
        ((3.0, 0.5), np.array([[0, 5], [-1, 1]]), 0.01, "linear", 0.5),
        (None, np.array([[0, 5], [-1, 1]]), None, "logarithmic", 1),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, "logarithmic", 1),
        ((3.0, 0.5), None, None, "logarithmic", 1),
        ((3.0, 0.5), None, 0.01, "logarithmic", 1),
        ((3.0, 0.5), np.array([[0, 5], [-1, 1]]), None, "logarithmic", 1),
        ((3.0, 0.5), np.array([[0, 5], [-1, 1]]), 0.01, "logarithmic", 1),
        (None, np.array([[0, 5], [-1, 1]]), None, "geometric", 0.85),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, "geometric", 0.85),
        ((3.0, 0.5), None, None, "geometric", 0.85),
        ((3.0, 0.5), None, 0.01, "geometric", 0.85),
        ((3.0, 0.5), np.array([[0, 5], [-1, 1]]), None, "geometric", 0.85),
        ((3.0, 0.5), np.array([[0, 5], [-1, 1]]), 0.01, "geometric", 0.85),
    ],
)
def test_fit_2d(init_states, bounds, acceptance, schedule, alpha):
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        ann = Annealer(loss=LossFunc2D(), weights_step_size=0.1, init_states=init_states, bounds=bounds, verbose=True)
        w0, lmin, _, _, _, _ = ann.fit(
            stopping_limit=acceptance,
            alpha=alpha,
            cooling_schedule=schedule,
            iterations=5000 if schedule != "logarithmic" else 10000,
        )
        print(w0, lmin)
        if (
            np.isclose(w0[0], 4.0565, rtol=5e-1, atol=5e-1)
            and np.isclose(w0[1], 0, rtol=5e-1, atol=5e-1)
            and np.isclose(lmin, -24.057, rtol=5e-2, atol=5e-2)
        ) or (
            np.isclose(w0[0], 0.39904, rtol=5e-1, atol=5e-1)
            and np.isclose(w0[1], 0, rtol=5e-1, atol=5e-1)
            and np.isclose(lmin, -1.7664, rtol=5e-2, atol=5e-2)
        ):
            break
        attempts += 1
    if attempts == max_attempts:
        raise AssertionError("Fit failed")


@pytest.mark.parametrize(
    "init_states,bounds,acceptance,multiproc",
    [
        (None, np.array([[0, 5], [-1, 1]]), None, False),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, False),
        (None, np.array([[0, 5], [-1, 1]]), None, True),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, True),
    ],
)
def test_fit_2d_multipoint(init_states, bounds, acceptance, multiproc):
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        if multiproc:
            Annealer.set_cpu_limit(2)
        else:
            Annealer.set_cpu_limit(1)
        # noinspection PyTypeChecker
        ann = Annealer(loss=LossFunc2D(), weights_step_size=0.1, init_states=init_states, bounds=bounds, verbose=True)
        results = ann.fit(npoints=3, stopping_limit=acceptance)
        assert len(results) == 3
        success = 0
        for w0, lmin, _, _, _, _ in results:
            print(w0, lmin)
            if (
                np.isclose(w0[0], 4.0565, rtol=5e-1, atol=5e-1)
                and np.isclose(w0[1], 0, rtol=5e-1, atol=5e-1)
                and np.isclose(lmin, -24.057, rtol=5e-2, atol=5e-2)
            ) or (
                np.isclose(w0[0], 0.39904, rtol=5e-1, atol=5e-1)
                and np.isclose(w0[1], 0, rtol=5e-1, atol=5e-1)
                and np.isclose(lmin, -1.7664, rtol=5e-2, atol=5e-2)
            ):
                success += 1
        if success == 3:
            break
        attempts += 1
    if attempts == max_attempts:
        raise AssertionError("Fit failed")


@pytest.mark.parametrize(
    "init_states,bounds,acceptance,multiproc,npoints",
    [
        (None, np.array([[0, 5], [-1, 1]]), None, False, 3),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, False, 3),
        (None, np.array([[0, 5], [-1, 1]]), None, True, 3),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, True, 3),
        (None, np.array([[0, 5], [-1, 1]]), None, False, 4),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, False, 4),
        (None, np.array([[0, 5], [-1, 1]]), None, True, 4),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, True, 4),
        (None, np.array([[0, 5], [-1, 1]]), None, False, 5),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, False, 5),
        (None, np.array([[0, 5], [-1, 1]]), None, True, 5),
        (None, np.array([[0, 5], [-1, 1]]), 0.01, True, 5),
    ],
)
def test_fit_2d_multipoint_stop_soon(init_states, bounds, acceptance, multiproc, npoints):
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        if multiproc:
            Annealer.set_cpu_limit(2)
        else:
            Annealer.set_cpu_limit(1)
        # noinspection PyTypeChecker
        ann = Annealer(loss=LossFunc2D(), weights_step_size=0.1, init_states=init_states, bounds=bounds, verbose=True)
        w0, lmin, _, _, _, _ = ann.fit(npoints=npoints, stopping_limit=acceptance, stop_at_first_found=True)
        print(w0, lmin)
        if (
            np.isclose(w0[0], 4.0565, rtol=5e-1, atol=5e-1)
            and np.isclose(w0[1], 0, rtol=5e-1, atol=5e-1)
            and np.isclose(lmin, -24.057, rtol=5e-2, atol=5e-2)
        ) or (
            np.isclose(w0[0], 0.39904, rtol=5e-1, atol=5e-1)
            and np.isclose(w0[1], 0, rtol=5e-1, atol=5e-1)
            and np.isclose(lmin, -1.7664, rtol=5e-2, atol=5e-2)
        ):
            break
        attempts += 1
    if attempts == max_attempts:
        raise AssertionError("Fit failed")
