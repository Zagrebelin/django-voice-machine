import datetime

from django.test import TestCase

from .. import models


class SchItemDisplayTestCase(TestCase):
    """
        в пн вт ср чт если это будни
        в пн вт ср чт если это выходной
        в пн вт ср чт
        в любой день если это будни
        в любой день если это выходной
        каждый день
        никогда

    """

    def test_single_days_workday(self):
        i = models.ScheduleItem(use_monday=True, use_workday=True)
        expected = 'В пн, если это рабочий день'
        actual = i.display_date
        self.assertEqual(expected, actual)

    def test_single_days_weekend(self):
        i = models.ScheduleItem(use_monday=True, use_holiday=True)
        expected = 'В пн, если это выходной или праздник'
        actual = i.display_date
        self.assertEqual(expected, actual)

    def test_single_days_both_workday_weekend(self):
        i = models.ScheduleItem(use_monday=True, use_holiday=True, use_workday=True)
        expected = 'В пн, если это выходной, праздник или рабочий день'
        actual = i.display_date
        self.assertEqual(expected, actual)

    # -----------------
    def test_several_days_workday(self):
        i = models.ScheduleItem(use_monday=True, use_tuesday=True, use_workday=True)
        expected = 'В пн вт, если это рабочий день'
        actual = i.display_date
        self.assertEqual(expected, actual)

    def test_several_days_weekend(self):
        i = models.ScheduleItem(use_monday=True, use_tuesday=True, use_holiday=True)
        expected = 'В пн вт, если это выходной или праздник'
        actual = i.display_date
        self.assertEqual(expected, actual)

    def test_several_days_both_workday_weekend(self):
        i = models.ScheduleItem(use_monday=True, use_tuesday=True, use_holiday=True, use_workday=True)
        expected = 'В пн вт, если это выходной, праздник или рабочий день'
        actual = i.display_date
        self.assertEqual(expected, actual)

    # -----------------
    def test_every_day_workday(self):
        i = models.ScheduleItem(use_monday=True,
                                use_tuesday=True,
                                use_wednesday=True,
                                use_thursday=True,
                                use_friday=True,
                                use_saturday=True,
                                use_sunday=True,
                                use_workday=True)
        expected = 'В любой день, если это рабочий день'
        actual = i.display_date
        self.assertEqual(expected, actual)

    def test_every_day_weekend(self):
        i = models.ScheduleItem(use_monday=True, use_tuesday=True, use_wednesday=True, use_thursday=True,
                                use_friday=True, use_saturday=True, use_sunday=True,
                                use_holiday=True)
        expected = 'В любой день, если это выходной или праздник'
        actual = i.display_date
        self.assertEqual(expected, actual)

    def test_every_day_both_workday_weekend(self):
        i = models.ScheduleItem(use_monday=True, use_tuesday=True, use_wednesday=True, use_thursday=True,
                                use_friday=True, use_saturday=True, use_sunday=True,
                                use_holiday=True, use_workday=True)
        expected = 'Каждый день'
        actual = i.display_date
        self.assertEqual(expected, actual)

    # -----------------
    def test_single_days_nor_weekend_workday(self):
        i = models.ScheduleItem(use_monday=True)
        expected = 'Никогда'
        actual = i.display_date
        self.assertEqual(expected, actual)

    def test_several_days_nor_weekend_workday(self):
        i = models.ScheduleItem(use_monday=True, use_tuesday=True)
        expected = 'Никогда'
        actual = i.display_date
        self.assertEqual(expected, actual)

    def test_every_day_nor_weekend_workday(self):
        i = models.ScheduleItem(use_monday=True, use_tuesday=True, use_wednesday=True, use_thursday=True,
                                use_friday=True, use_saturday=True, use_sunday=True)
        expected = 'Никогда'
        actual = i.display_date
        self.assertEqual(expected, actual)

    # -----------------
    def no_days_weekend(self):
        i = models.ScheduleItem(use_holiday=True)
        expected = 'Никогда'
        actual = i.display_date
        self.assertEqual(expected, actual)

    def no_days_workday(self):
        i = models.ScheduleItem(use_workday=True)
        expected = 'Никогда'
        actual = i.display_date
        self.assertEqual(expected, actual)

    def no_days_both_workday_weekend(self):
        i = models.ScheduleItem(use_holiday=True, use_workday=True)
        expected = 'Никогда'
        actual = i.display_date
        self.assertEqual(expected, actual)

    def no_days_at_all(self):
        i = models.ScheduleItem()
        expected = 'Никогда'
        actual = i.display_date
        self.assertEqual(expected, actual)


def time(hour, min):
    return datetime.datetime(2001, 1, 1, hour, min, 0)

class SchItemRenderTestCase(TestCase):
    def test_time(self):
        item = models.ScheduleItem(message="{{time}}")
        actual = item.render(datetime.datetime.now())
        self.assertIsInstance(actual, str)
        self.assertGreater(len(actual), 0)
        self.assertNotIn('{', actual)
        self.assertNotIn('}', actual)

    def test_date(self):
        item = models.ScheduleItem(message="{{date}}")
        actual = item.render(datetime.datetime.now())
        self.assertIsInstance(actual, str)
        self.assertGreater(len(actual), 0)
        self.assertNotIn('{', actual)
        self.assertNotIn('}', actual)

    def test_weekday(self):
        item = models.ScheduleItem(message="{{weekday}}")
        actual = item.render(datetime.datetime.now())
        self.assertIsInstance(actual, str)
        self.assertGreater(len(actual), 0)
        self.assertNotIn('{', actual)
        self.assertNotIn('}', actual)
