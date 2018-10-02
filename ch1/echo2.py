import sys
from rx import Observable

argv = Observable.from_(sys.argv[1:]) \
    .map(lambda i: i.capitalize())

argv.subscribe(
    on_next=lambda i: print("on_next: {}".format(i)),
    on_error=lambda e: print("on_error: {}".format(e)),
    on_completed=lambda: print("on_completed"))
print("done")
