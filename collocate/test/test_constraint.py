"""
Test the constraints
"""
import unittest
from collocate.test import mock
from numpy.testing import assert_equal


class TestSepConstraint(unittest.TestCase):

    def test_all_constraint_in_4d(self):
        from collocate.sepconstraint import SepConstraint
        import datetime as dt
        import numpy as np

        ug_data = mock.make_regular_4d_ungridded_data(as_data_frame=True)
        sample_point = mock.make_dummy_sample_points(latitude=[0.0], longitude=[0.0],
                                                     altitude=[50.0], air_pressure=[50.0],
                                                     time=[dt.datetime(1984, 8, 29)],
                                                     as_data_frame=True)
        # One degree near 0, 0 is about 110km in latitude and longitude, so 300km should keep us to within 3 degrees
        # in each direction
        h_sep = 1000
        # 15m altitude seperation
        a_sep = 15
        # 1 day (and a little bit) time seperation
        t_sep = np.timedelta64(1, 'D') + np.timedelta64(1, 'm')
        # Pressure constraint is 50/40 < p_sep < 60/50
        p_sep = 1.22

        constraint = SepConstraint(h_sep=h_sep, a_sep=a_sep, p_sep=p_sep, t_sep=t_sep)

        # Create the index
        constraint.index_data(ug_data)

        # This should leave us with 9 points: [[ 22, 23, 24]
        #                                      [ 27, 28, 29]
        #                                      [ 32, 33, 34]]
        ref_vals = np.array([27., 28., 29., 32., 33., 34.])

        new_points = constraint.constrain_points(sample_point, ug_data)
        new_vals = new_points.vals

        assert_equal(ref_vals, new_vals)

    def test_alt_constraint_in_4d(self):
        from collocate.sepconstraint import SepConstraint
        import datetime as dt
        import numpy as np

        ug_data = mock.make_regular_4d_ungridded_data(as_data_frame=True)
        sample_point = mock.make_dummy_sample_points(latitude=[0.0], longitude=[0.0], altitude=[50.0],
                                                     time=[dt.datetime(1984, 8, 29)],
                                                     as_data_frame=True)

        # 15m altitude seperation
        a_sep = 15

        constraint = SepConstraint(a_sep=a_sep)

        # This should leave us with 15 points. They are flattened in the process though.
        ref_vals = np.array([[21., 22., 23., 24., 25.],
                             [26., 27., 28., 29., 30.],
                             [31., 32., 33., 34., 35.]]).flatten()

        new_points = constraint.constrain_points(sample_point, ug_data)
        new_vals = new_points.vals

        assert_equal(ref_vals, new_vals)

    def test_horizontal_constraint_in_4d(self):
        from collocate.sepconstraint import SepConstraint
        import datetime as dt
        import numpy as np

        ug_data = mock.make_regular_4d_ungridded_data(as_data_frame=True)
        sample_point = mock.make_dummy_sample_points(latitude=[0.0], longitude=[0.0], altitude=[50.0],
                                                     time=[dt.datetime(1984, 8, 29)],
                                                     as_data_frame=True)

        # One degree near 0, 0 is about 110km in latitude and longitude, so 300km should keep us to within 3 degrees
        # in each direction
        constraint = SepConstraint(h_sep=1000)

        # Create the index
        constraint.index_data(ug_data)

        # This should leave us with 30 points. Use fortran ordering to match the resulting layout
        ref_vals = np.reshape(np.arange(50) + 1.0, (10, 5))[:, 1:4].flatten(order='F')

        new_points = constraint.constrain_points(sample_point, ug_data)
        new_vals = new_points.vals

        assert_equal(ref_vals, new_vals)

    def test_time_constraint_in_4d(self):
        from collocate.sepconstraint import SepConstraint
        import datetime as dt
        import numpy as np

        ug_data = mock.make_regular_4d_ungridded_data(as_data_frame=True)
        sample_point = mock.make_dummy_sample_points(latitude=[0.0], longitude=[0.0], altitude=[50.0],
                                                     time=[dt.datetime(1984, 8, 29)], as_data_frame=True)

        # 1 day (and a little bit) time seperation
        constraint = SepConstraint(t_sep=np.timedelta64(1, 'D') + np.timedelta64(1, 'm'))

        # This should leave us with 30 points
        ref_vals = np.reshape(np.arange(50) + 1.0, (10, 5))[:, 1:4].flatten()

        new_points = constraint.constrain_points(sample_point, ug_data)
        new_vals = new_points.vals

        assert_equal(ref_vals, new_vals)

    def test_pressure_constraint_in_4d(self):
        from collocate.sepconstraint import SepConstraint
        import datetime as dt
        import numpy as np

        ug_data = mock.make_regular_4d_ungridded_data(as_data_frame=True)
        sample_point = mock.make_dummy_sample_points(latitude=[0.0], longitude=[0.0], altitude=[50.0],
                                                     air_pressure=[24.0], time=[dt.datetime(1984, 8, 29)],
                                                     as_data_frame=True)

        constraint = SepConstraint(p_sep=2)

        # This should leave us with 20 points:
        ref_vals = np.array([[6., 7., 8., 9., 10.],
                             [11., 12., 13., 14., 15.],
                             [16., 17., 18., 19., 20.],
                             [21., 22., 23., 24., 25.]]).flatten()

        new_points = constraint.constrain_points(sample_point, ug_data)
        new_vals = new_points.vals

        assert_equal(ref_vals, new_vals)


if __name__ == '__main__':
    unittest.main()
