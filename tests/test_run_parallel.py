import pytest

from pyswap import run_parallel, testcase


def failing_model():
    # Passes pyswap validation, but SWAP stops: no irrigation date falls
    # within the one-day simulation period.
    model = testcase.get("hupselbrook")
    model.generalsettings.tend = model.generalsettings.tstart
    return model


def test_run_parallel_raises_naming_the_failed_runs(tmp_path):
    models = [testcase.get("hupselbrook"), failing_model()]
    with pytest.raises(
        RuntimeError, match=r"1 of 2 model runs failed \(indices \[1\]\)"
    ):
        run_parallel(models, path=tmp_path, silence_warnings=True, processes=2)


def test_run_parallel_captures_errors(tmp_path):
    models = [testcase.get("hupselbrook"), failing_model()]
    ok, failed = run_parallel(
        models, path=tmp_path, silence_warnings=True, on_error="capture", processes=2
    )
    assert ok.success
    assert ok.error is None
    assert ok.csv is not None
    assert not failed.success
    assert "no input date within simulation period" in failed.error


def test_run_times_out(tmp_path):
    with pytest.raises(RuntimeError, match=r"did not finish within 0\.01 s"):
        testcase.get("hupselbrook").run(tmp_path, silence_warnings=True, timeout=0.01)
