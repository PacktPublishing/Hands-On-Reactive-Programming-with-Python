from collections import namedtuple
import json
from reactivex.notification import OnNext, OnError, OnCompleted
import reactivex as rx
import reactivex.operators as ops
from cyclotron import Component
from cyclotron.asyncio.runner import run

from rmux.framing.newline import frame, unframe

import rmux_client.tcp_client as tcp_client
import cyclotron_std.sys.stdout as stdout

Drivers = namedtuple('Drivers', ['tcp_client', 'stdout'])
Source = namedtuple('Source', ['tcp_client'])
Sink = namedtuple('Sink', ['tcp_client', 'stdout'])


def notification(obj):
    if obj['what'] == 'on_next':
        return OnNext(obj['item'])
    elif obj['what'] == 'on_completed':
        return OnCompleted()
    elif obj['what'] == 'on_error':
        return OnError(obj['error'])


def rmux_client(sources):
    response = sources.tcp_client.response.pipe(ops.share())
    tcp_connect = rx.just(tcp_client.Connect(
        host='127.0.0.1', port='8080'
    ))

    create_observable = response.pipe(
        ops.flat_map(lambda connection: 
            rx.just({'what': 'subscribe', 'id':42, 'name': '1234'}).pipe(
                ops.map(lambda i: json.dumps(i)),
                frame,
                ops.map(lambda j: tcp_client.Write(id=connection.id, data=j.encode()))
        ))
    )

    console = response.pipe(
        ops.flat_map(lambda connection: connection.observable.pipe(
            ops.map(lambda i: i.data.decode('utf-8')),
            unframe,
            ops.map(lambda i: json.loads(i)),
            ops.group_by(lambda i: i['id']),
            ops.flat_map(lambda subscription: subscription.pipe(
                ops.map(notification),
                ops.dematerialize(),
            ))
        )),
        ops.map(lambda i: "item: {}\n".format(i))
    )

    tcp_sink = rx.merge(tcp_connect, create_observable)

    return Sink(
        tcp_client=tcp_client.Sink(request=tcp_sink),
        stdout=stdout.Sink(data=console),
    )


def main():
    dispose = run(
        entry_point=Component(call=rmux_client, input=Source),
        drivers=Drivers(
            tcp_client=tcp_client.make_driver(),
            stdout=stdout.make_driver(),
        )
    )
    dispose()
