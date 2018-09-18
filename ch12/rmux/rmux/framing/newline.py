from rx import Observable


def frame(datagram):
    def on_subscribe(observer):
        def on_next(i):
            if '\n' in i:
                observer.on_error(ValueError('newline must be escaped'))
            observer.on_next(i + '\n')

        datagram.subscribe(
            on_next=on_next,
            on_error=observer.on_error,
            on_completed=observer.on_completed,
        )
    return Observable.create(on_subscribe)


def unframe(data):
    def on_subscribe(observer):
        acc = ''

        def on_next(i):
            nonlocal acc
            lines = i.split('\n')
            lines[0] = acc + lines[0]
            acc = lines[-1]
            datagrams = lines[0:-1]
            for datagram in datagrams:
                observer.on_next(datagram)

        data.subscribe(
            on_next=on_next,
            on_error=observer.on_error,
            on_completed=observer.on_completed,
        )
    return Observable.create(on_subscribe)