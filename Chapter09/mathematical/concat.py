import rx
import rx.operators as ops

numbers1 = rx.from_([1, 2, 3, 4])
numbers2 = rx.from_([11, 12])

numbers1.pipe(ops.concat(numbers2)).subscribe(
    on_next=lambda i: print("on_next {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed")
)
