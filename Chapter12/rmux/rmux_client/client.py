from collections import namedtuple
import json
from rx.core.notification import OnNext, OnError, OnCompleted
from rx import Observable
from cyclotron import Component
from cyclotron_aio.runner import run

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
    response = sources.tcp_client.response.share()
    tcp_connect = Observable.just(tcp_client.Connect(
        host='127.0.0.1', port='8080'
    ))

    create_observable = (
        response
        .flat_map(lambda connection: 
            Observable.just({'what': 'subscribe', 'id':42, 'name': '1234'})
            .map(lambda i: json.dumps(i))
            .let(frame)
            .map(lambda j: tcp_client.Write(id=connection.id, data=j.encode()))
        )
    )

    console = (
        response
        .flat_map(lambda connection: connection.observable
            .map(lambda i: i.data.decode('utf-8'))
            .let(unframe)
            .map(lambda i: json.loads(i))
            .group_by(lambda i: i['id'])            
            .flat_map(lambda subscription: subscription
                .map(notification)
                .dematerialize()
            )
        )
        .map(lambda i: "item: {}\n".format(i))
    )

    tcp_sink = Observable.merge(tcp_connect, create_observable)

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
