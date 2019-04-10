[Suzuki Kasami Algorithm]

--Independently running version, without combination with master program

--Version 1

[Illustration]

1. The "Queue updating" is not made by monitoring thread when token owner hold the token. Queue is updated when main thread try to invoke "func csEnter".

2. The token is passed only when "func csEnter" is invoked. That means, master program has to frequently call the "func csEnter" to keep token passing.