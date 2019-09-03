from collections import namedtuple
import json
import rx
import rx.operators as ops
from rx.core.notification import OnNext, OnError, OnCompleted
from cyclotron import Component
from cyclotron.asyncio.runner import run

import rmux_server.tcp_server as tcp_server
from rmux.framing.newline import frame, unframe

Drivers = namedtuple('Drivers', ['tcp_server'])
Source = namedtuple('Source', ['tcp_server'])
Sink = namedtuple('Sink', ['tcp_server'])


def materialize_repr(notification, id):
    if type(notification) is OnNext:
        return {
            'what': 'on_next',
            'item': notification.value,
            'id': id,
        }
    elif type(notification) is OnError:
        return {
            'what': 'on_error',
            'error': str(notification.exception),
            'id': id,
        }
    elif type(notification) is OnCompleted:
        return {
            'what': 'on_completed',
            'id': id,
        }


def one_two_three_four():
    return rx.from_(['1', '2', '3', '4'])


def lets_go():
    return rx.just("let's go")


create_observable = {
    '1234': one_two_three_four,
    'heyho': lets_go,
}


def rmux_server(sources):
    tcp_listen = rx.just(tcp_server.Listen(
        host='127.0.0.1', port='8080'
    ))

    beat = sources.tcp_server.response.pipe(
        ops.flat_map(lambda connection: connection.observable.pipe(
            ops.map(lambda i: i.data.decode('utf-8')),
            unframe,
            ops.map(lambda i: json.loads(i)),
            ops.flat_map(lambda subscription: create_observable[subscription['name']]().pipe(
                ops.materialize(),
                ops.map(lambda i: materialize_repr(i, subscription['id'])),
            )),
            ops.map(lambda i: json.dumps(i)),
            frame,
            ops.map(lambda j: tcp_server.Write(id=connection.id, data=j.encode()))
        ))
    )

    tcp_sink = rx.merge(tcp_listen, beat)
    return Sink(
        tcp_server=tcp_server.Sink(request=tcp_sink),
    )


def main():
    dispose = run(
        entry_point=Component(call=rmux_server, input=Source),
        drivers=Drivers(
            tcp_server=tcp_server.make_driver(),
        )
    )
    dispose()
