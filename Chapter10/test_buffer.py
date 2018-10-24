from unittest import TestCase
from rx import Observable
from rx.subjects import Subject


class BufferTestCase(TestCase):

    def test_nominal(self):
        numbers = Subject()
        windows = Subject()

        expected_numbers = [ [1, 2], [3, 4, 5]]
        expected_error = None
        actual_numbers = []
        actual_error = None

        def on_next(i):
            actual_numbers.append(i)

        def on_error(e):
            nonlocal actual_error
            actual_error = e

        numbers.buffer(windows).subscribe(
            on_next=on_next,
            on_error=on_error
        )

        numbers.on_next(1)
        numbers.on_next(2)
        windows.on_next(True)
        numbers.on_next(3)
        numbers.on_next(4)
        numbers.on_next(5)
        windows.on_next(True)

        self.assertEqual(None, actual_error)
        self.assertEqual(expected_numbers, actual_numbers)


    def test_error(self):
        numbers = Subject()
        windows = Subject()

        expected_numbers = []
        expected_error = None
        actual_numbers = []
        actual_error = None

        def on_next(i):
            actual_numbers.append(i)

        def on_error(e):
            nonlocal actual_error
            actual_error = e

        numbers.buffer(windows).subscribe(
            on_next=on_next,
            on_error=on_error
        )

        numbers.on_next(1)
        numbers.on_next(2)
        numbers.on_error(ValueError())

        self.assertIsInstance(actual_error, ValueError)
        self.assertEqual(expected_numbers, actual_numbers)
