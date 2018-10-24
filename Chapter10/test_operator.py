from unittest import TestCase
from rx import Observable

def integer_passthrough(numbers):
    def on_subscribe(observer):
        def on_next(i):
            if type(i) is int:
                observer.on_next(i)
            else:
                observer.on_error(TypeError("Item is not an integer"))

        disposable = numbers.subscribe(
            on_next=on_next,
            on_error= lambda e: observer.on_error(e),
            on_completed= lambda: observer.on_completed()
        )
        return disposable

    return Observable.create(on_subscribe)


class IntegerPassthroughTestCase(TestCase):

    def test_next(self):
        numbers = Observable.from_([1, 2, 3, 4])
        expected_numbers = [1, 2, 3, 4]
        expected_error = None
        actual_numbers = []
        actual_error = None

        def on_next(i):
            actual_numbers.append(i)

        def on_error(e):
            nonlocal actual_error
            actual_error = e

        integer_passthrough(numbers).subscribe(
            on_next=on_next,
            on_error=on_error
        )

        self.assertEqual(None, actual_error)
        self.assertEqual(expected_numbers, actual_numbers)

    def test_error_on_string(self):        
        numbers = Observable.from_([1, 2, 'c', 4])
        expected_numbers = [1, 2]
        actual_numbers = []
        actual_error = None

        def on_next(i):
            actual_numbers.append(i)

        def on_error(e):
            nonlocal actual_error
            actual_error = e

        integer_passthrough(numbers).subscribe(
            on_next=on_next,
            on_error=on_error
        )

        self.assertIsInstance(actual_error, TypeError)
        self.assertEqual(expected_numbers, actual_numbers)


    def test_forward_error(self):        
        numbers = Observable.throw(ValueError())
        expected_numbers = []
        actual_numbers = []
        actual_error = None

        def on_next(i):
            actual_numbers.append(i)

        def on_error(e):
            nonlocal actual_error
            actual_error = e

        integer_passthrough(numbers).subscribe(
            on_next=on_next,
            on_error=on_error
        )

        self.assertIsInstance(actual_error, ValueError)
        self.assertEqual(expected_numbers, actual_numbers)
