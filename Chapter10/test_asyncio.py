from unittest import TestCase
import asyncio
from rx import Observable


class AsyncIOTestCase(TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.stop()
        self.loop.close()

    def test_example(self):
        future = self.loop.create_future()

        expected_result = [42]
        expected_error = None
        actual_result = []
        actual_error = None

        def on_next(i):
            actual_result.append(i)

        def on_error(e):
            nonlocal actual_error
            actual_error = e

        def on_completed():
            self.loop.stop()

        Observable.from_future(future).subscribe(
            on_next=on_next,
            on_error=on_error,
            on_completed=on_completed
        )

        self.assertEqual([], actual_result)
        self.loop.call_soon(lambda: future.set_result(42))
        self.loop.run_forever()
        self.assertEqual(expected_result, actual_result)