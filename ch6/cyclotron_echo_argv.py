from collections import namedtuple
from rx import Observable
from cyclotron import Component
from cyclotron.rx import run

import cyclotron_std.sys.stdout as stdout
import cyclotron_std.sys.argv as argv

Drivers = namedtuple('Drivers', ['stdout', 'argv'])
Source = namedtuple('Source', ['argv'])
Sink = namedtuple('Sink', ['stdout'])


def echo(sources):
    console = sources.argv.argv.skip(1).map(lambda i: i + '\n')
    return Sink(
        stdout=stdout.Sink(data=console)
    )


if __name__ == '__main__':
    dispose = run(
        entry_point=Component(call=echo, input=Source),
        drivers=Drivers(
            stdout=stdout.make_driver(),
            argv=argv.make_driver(),
        )
    )
    dispose()
