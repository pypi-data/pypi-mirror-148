Changelog
=========


Version 0.8
-----------

Unreleased


Version 0.7.1
-------------

Released 2022-04-27

- Changed application path in Docker container from `/home/user` to
  `/app`. This is relevant when mounting the configuration file into the
  container.


Version 0.7
-----------

Released 2022-04-26

- Added support for Python 3.10.

- Expect config file to be mounted into Docker container.

- Use non-inline array of tables for IRC channels in TOML configuration
  examples.

- Reintroduce announcer as abstraction.

- Updated irc version to 20.0.0 (from 19.0.1).

- Updated rtoml to 0.7.1 (from 0.6.1).


Version 0.6
-----------

Released 2021-05-07

- Switched to using Python's logging mechanism directly, with different
  log levels. Removed function ``util.log``.

- Made the application's log level configurable.

- Enabled threading for the HTTP server to reduce blocking.

- Introduced an internal queue to decouple reception of HTTP requests
  from announcing messages on IRC.

- Added support for custom IRC commands to send after connecting
  (authentication, cloaking, flood protection, etc.).

- Updated rtoml to 0.6.1 (from 0.5.0).


Version 0.5
-----------

Released 2021-02-07

- Added support for Python 3.9.

- Added support for SSL connections to IRC servers.

- Changed prefix of authorization header value from ``WTRSGR`` to less
  awkward ``Token``.

- Removed handler to shut down Weitersager via private IRC message. It
  doesn't provide enough relevant value.

- Added command line option ``--version`` to show Weitersager's version.

- Updated rtoml to 0.5.0 (from 0.4.0).

- Include tests and other useful files in source distribution archive.


Version 0.4
-----------

Released 2020-10-11

- Added command line tool to generate secure tokens (which can be used as
  API tokens).

- Allow to configure a rate limit for the IRC connection, i.e. the maximum
  number of messages per second to send. This can prevent the bot from
  getting kicked (or even banned) from a channel because of flooding.

- Added exemplary Dockerfile.

- Added type hints.

- Updated rtoml to 0.4.0 (from 0.3.0).


Version 0.3
-----------

Released 2020-09-16

- Introduced TOML-based configuration file.

  - Added dependency on rtoml 0.3.0.

  - Moved IRC channel configuration from Python code to configuration
    file.

  - Moved IRC server and bot name configuration from command line
    arguments to configuration file.

  - Moved HTTP receiver configuration from command line arguments to
    configuration file.

  - Made configuration filename a required command line argument.

- Turned the stray run script into an actual entry point console script.

- Added support for IRC server password.

- Added optional HTTP authorization via API tokens.


Version 0.2
-----------

Released 2020-09-13

- Raised minimum Python version to 3.7.

- HTTP protocol was changed:

  - Only a single channel is allowed per message.

  - Response code for successful submit was changed from 200 (OK) to
    more appropriate 202 (Accepted).

- Divided code base into separate modules in a package.

- Switch to a ``src/`` layout.

- Dependency versions have been pinned.

- Updated irc version to 19.0.1 (from 12.3).

- Updated blinker to 1.4 (from 1.3).

- Do not use tox for tests anymore.

- Use ``dataclass`` instead of ``namedtuple`` for value objects.

- Allowed for custom shutdown predicate.


Version 0.1
-----------

Released 2015-04-24 at LANresort 2015

- First official release
