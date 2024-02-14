
from datetime import datetime
import unittest
import sys
from pathlib import Path

pyswap_path = Path("/home/zawadzkim/projects/pySWAP")
sys.path.append(str(pyswap_path.resolve()))


class TestEnvironment(unittest.TestCase):

    def test_environment_creation(self):
        from pyswap.core.simsettings import Environment
        pathwork = Path("/path/to/work")
        pathatm = Path("/path/to/atm")
        pathcrop = Path("/path/to/crop")
        pathdrain = Path("/path/to/drain")
        env = Environment(pathwork, pathatm, pathcrop, pathdrain)
        self.assertEqual(env.pathwork, pathwork)
        self.assertEqual(env.pathatm, pathatm)
        self.assertEqual(env.pathcrop, pathcrop)
        self.assertEqual(env.pathdrain, pathdrain)
        self.assertEqual(env.swscre, 0)
        self.assertEqual(env.swerror, 0)


class TestSimPeriod(unittest.TestCase):

    def test_sim_period_creation(self):
        from pyswap.core.simsettings import SimPeriod

        tstart = datetime(2022, 1, 1)
        tend = datetime(2022, 12, 31)
        sim_period = SimPeriod(tstart, tend)
        self.assertEqual(sim_period.tstart, tstart)
        self.assertEqual(sim_period.tend, tend)

    def test_sim_period_tstart_str(self):
        from pyswap.core.simsettings import SimPeriod

        tstart = datetime(2022, 1, 1)
        tend = datetime(2022, 12, 31)
        sim_period = SimPeriod(tstart, tend)
        self.assertEqual(sim_period.tstart_str, "2022-01-01")

    def test_sim_period_tend_str(self):
        from pyswap.core.simsettings import SimPeriod

        tstart = datetime(2022, 1, 1)
        tend = datetime(2022, 12, 31)
        sim_period = SimPeriod(tstart, tend)
        self.assertEqual(sim_period.tend_str, "2022-12-31")


class TestOutputDates(unittest.TestCase):

    def test_output_dates_creation(self):
        from pyswap.core.simsettings import OutputDates
        output_dates = OutputDates()
        self.assertEqual(output_dates.nprintday, 1)
        self.assertTrue(output_dates.swmonth)
        self.assertFalse(output_dates.swyrvar)
        self.assertIsNone(output_dates.period)
        self.assertIsNone(output_dates.swres)
        self.assertIsNone(output_dates.swodat)
        self.assertIsNone(output_dates.outdatin)
        self.assertIsNone(output_dates.datefix)
        self.assertIsNone(output_dates.outdat)


class TestOutputFiles(unittest.TestCase):

    def test_output_files_creation(self):
        from pyswap.core.simsettings import OutputFiles
        output_files = OutputFiles()
        self.assertEqual(output_files.outfil, "result")
        self.assertFalse(output_files.swheader)
        self.assertFalse(output_files.swwba)
        self.assertFalse(output_files.swend)
        self.assertFalse(output_files.swvap)
        self.assertFalse(output_files.swbal)
        self.assertFalse(output_files.swblc)
        self.assertFalse(output_files.swsba)
        self.assertFalse(output_files.swate)
        self.assertFalse(output_files.swbma)
        self.assertFalse(output_files.swdrf)
        self.assertFalse(output_files.swswb)
        self.assertFalse(output_files.swini)
        self.assertFalse(output_files.swinc)
        self.assertFalse(output_files.swcrp)
        self.assertFalse(output_files.swstr)
        self.assertFalse(output_files.swirg)
        self.assertTrue(output_files.swcsv)
        self.assertIsNone(output_files.inlist_csv)
        self.assertFalse(output_files.swcsv_tz)
        self.assertIsNone(output_files.inlist_csv_tz)
        self.assertEqual(output_files.swafo, 0)
        self.assertEqual(output_files.swaun, 0)
        self.assertIsNone(output_files.critdevmasbal)
        self.assertFalse(output_files.swdiscrvert)
        self.assertIsNone(output_files.numnodnew)
        self.assertIsNone(output_files.dznew)


if __name__ == "__main__":
    unittest.main()
