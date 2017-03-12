import datetime
import functools
from unittest import TestCase, main
from .humanize_render import time_as_string, int_to_str, decline, weekday_as_string, date_as_string


class TimeTestCase(TestCase):
    @staticmethod
    def create_test(hour, minute):
        def test(self):
            """

            :param self:
            :type self: TestCase
            :return:
            """
            dt = datetime.datetime(2001, 1, 1, hour, minute, 0)
            actual = time_as_string(dt)
            self.assertIsInstance(actual, str)
            self.assertGreater(len(actual), 0)

        return test

    @classmethod
    def generate_tests(cls):
        for hour in range(23):
            for minute in range(60):
                setattr(cls, f'test_{hour:02}_{minute:02}', cls.create_test(hour, minute))


class DateTestCase(TestCase):
    def test_1_jan(self):
        self.assertEqual(date_as_string(datetime.datetime(2017, 1, 1)), 'первое января')

    def test_11_mar(self):
        self.assertEqual(date_as_string(datetime.datetime(2017, 3, 11)), 'одиннадцатое марта')


class IntToStrTestCase(TestCase):
    def test_0(self):
        self.assertEqual(int_to_str(0), 'ноль')

    def test_4(self):
        self.assertEqual(int_to_str(4), 'четыре')

    def test_10(self):
        self.assertEqual(int_to_str(10), 'десять')

    def test_12(self):
        self.assertEqual(int_to_str(12), 'двенадцать')

    def test_30(self):
        self.assertEqual(int_to_str(30), 'тридцать')

    def test_42(self):
        self.assertEqual(int_to_str(42), 'сорок два')


class DeclineTestCase(TestCase):
    def setUp(self):
        self.func = functools.partial(decline, zero='столов', one='стол', two='стола')

    def test_0(self):
        self.assertEqual(self.func(0), 'столов')

    def test_1(self):
        self.assertEqual(self.func(1), 'стол')

    def test_2(self):
        self.assertEqual(self.func(2), 'стола')

    def test_3(self):
        self.assertEqual(self.func(3), 'стола')

    def test_4(self):
        self.assertEqual(self.func(4), 'стола')

    def test_5(self):
        self.assertEqual(self.func(5), 'столов')

    def test_6(self):
        self.assertEqual(self.func(6), 'столов')

    def test_10(self):
        self.assertEqual(self.func(10), 'столов')

    def test_12(self):
        self.assertEqual(self.func(12), 'столов')

    def test_15(self):
        self.assertEqual(self.func(15), 'столов')

    def test_20(self):
        self.assertEqual(self.func(20), 'столов')

    def test_21(self):
        self.assertEqual(self.func(21), 'стол')

    def test_22(self):
        self.assertEqual(self.func(22), 'стола')

    def test_23(self):
        self.assertEqual(self.func(23), 'стола')

    def test_24(self):
        self.assertEqual(self.func(24), 'стола')

    def test_25(self):
        self.assertEqual(self.func(25), 'столов')

    def test_26(self):
        self.assertEqual(self.func(26), 'столов')


class WeekdayTestCase(TestCase):
    def test_пн(self):
        self.assertEqual(weekday_as_string(datetime.datetime(2017, 3, 6)), 'понедельник')

    def test_вт(self):
        self.assertEqual(weekday_as_string(datetime.datetime(2017, 3, 7)), 'вторник')

    def test_ср(self):
        self.assertEqual(weekday_as_string(datetime.datetime(2017, 3, 8)), 'среда')

    def test_чт(self):
        self.assertEqual(weekday_as_string(datetime.datetime(2017, 3, 9)), 'четверг')

    def test_пт(self):
        self.assertEqual(weekday_as_string(datetime.datetime(2017, 3, 10)), 'пятница')

    def test_сб(self):
        self.assertEqual(weekday_as_string(datetime.datetime(2017, 3, 11)), 'суббота')

    def test_вс(self):
        self.assertEqual(weekday_as_string(datetime.datetime(2017, 3, 12)), 'воскресенье')


TimeTestCase.generate_tests()

if __name__ == '__main__':
    main()
