# TCP protocol

[toc]

## Communication

There are one `server` node and several `client` nodes.
The TCP communication is bidirectional.

```plantuml
!theme vibrant
title Communication process
== Echo stage (low delay) ==

Client -> Server: echo package
Server -> Client: echoBack package

== Sending stage (random delay) ==

Client -> Server: content package
activate Server #DarkSalmon
activate Worker 
Server <--> Worker: working load
...seconds later...
Server -> Client: contentBack package
deactivate Worker
deactivate Server
```

## Echo package and time zone

The echo package is used for estimate the offset between clients and server machine.
If the response is received quickly enough, the offset of the time zones is estimated.

```plantuml
!theme vibrant
title Echo package
note over Client: Client time zone \n1730798716.6721733
note over Server: Server time zone \n1730798716.0512562

group Echo package [As quick as possible]
    Client -> Server: <timeClient>
    Server -> Client: <timeClient>, <timeServer>
end

== Estimate offset ==
alt#Gold #LightBlue Got within 1ms
    Server <-> Client: offset = timeServer - timeClient
else #Pink Failure
    Server <--> Client: offset is unknown
end
```

## Content package

## Package warping

The package is wrapped before sending.
The head is package length to prevent TCP sticking package.

```plantuml
!theme vibrant
title: Package in TCP
left to right direction
map Wrapped.header {
    bytesLength (255) => 0x000000FF
    bytesLength (10) => 0x0000000A
    echoPackage (10) => 0e0000000A
}
map Wrapped.Body.bytes {
}
Wrapped.header -> Wrapped.Body.bytes
```

So, the wrapped package is read in two steps

- Read head, read fixed 10 bytes for body length;
- Read body, read 1024 length buf until the body is all extracted.

```plantuml
!theme vibrant
title: Read wrapped body
start
:Read head (10 bytes);
:Convert to body length (n);

if (n > 1024) then (yes)
    repeat 
        :read 1024 bytes;
        :n -= 1024;
    repeat while (n > 1024 ?) is (yes)
else (no)
    :Read n bytes;
endif

:Work with body;

stop

```
