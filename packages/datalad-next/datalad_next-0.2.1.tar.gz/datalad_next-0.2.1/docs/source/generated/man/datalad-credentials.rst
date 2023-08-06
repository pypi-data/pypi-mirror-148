.. _man_datalad-credentials:

datalad credentials
===================

Synopsis
--------
::

  datalad credentials [-h] [--prompt PROMPT] [-d DATASET] [--version] [{query|get|set|remove}] [[name] [:]property[=value] ...]


Description
-----------
Credential management and query

This command enables inspection and manipulation of credentials used
throughout DataLad.

The command provides four basic actions:


QUERY

When executed without any property specification, all known credentials
with all their properties will be yielded. Please note that this may not
include credentials that only comprise of a secret and no other properties,
or legacy credentials for which no trace in the configuration can be found.
Therefore, the query results are not guaranteed to contain all credentials
ever configured by DataLad.

When additional property/value pairs are specified, only credentials that
have matching values for all given properties will be reported. This can be
used, for example, to discover all suitable credentials for a specific
"realm", if credentials were annotated with such information.


SET

This is the companion to 'get', and can be used to store properties and
secret of a credential. Importantly, and in contrast to a 'get' operation,
given properties with no values indicate a removal request. Any matching
properties on record will be removed. If a credential is to be stored for
which no secret is on record yet, an interactive session will prompt a user
for a manual secret entry.

Only changed properties will be contained in the result record.

The appearance of the interactive secret entry can be configured with
the two settings `datalad.credentials.repeat-secret-entry` and
`datalad.credentials.hidden-secret-entry`.


REMOVE

This action will remove any secret and properties associated with a
credential identified by its name.


GET (plumbing operation)

This is a *read-only* action that will never store (updates of) credential
properties or secrets. Given properties will amend/overwrite those already
on record.  When properties with no value are given, and also no value for
the respective properties is on record yet, their value will be requested
interactively, if a ``--prompt`` text was provided too. This can be
used to ensure a complete credential record, comprising any number of
properties.


Details on credentials

A credential comprises any number of properties, plus exactly one secret.
There are no constraints on the format or property values or the secret,
as long as they are encoded as a string.

Credential properties are normally stored as configuration settings in a
user's configuration ('global' scope) using the naming scheme:

  `datalad.credential.<name>.<property>`

Therefore both credential name and credential property name must be
syntax-compliant with Git configuration items. For property names this
means only alphanumeric characters and dashes. For credential names
virtually no naming restrictions exist (only null-byte and newline are
forbidden). However, when naming credentials it is recommended to use
simple names in order to enable convenient one-off credential overrides
by specifying DataLad configuration items via their environment variable
counterparts (see the documentation of the ``configuration`` command
for details. In short, avoid underscores and special characters other than
'.' and '-'.

While there are no constraints on the number and nature of credential
properties, a few particular properties are recognized on used for
particular purposes:

- 'secret': always refers to the single secret of a credential
- 'type': identifies the type of a credential. With each standard type,
  a list of mandatory properties is associated (see below)
- 'last-used': is an ISO 8601 format time stamp that indicated the
  last (successful) usage of a credential

Standard credential types and properties

The following standard credential types are recognized, and their
mandatory field with their standard names will be automatically
included in a 'get' report.

- 'user_password': with properties 'user', and the password as secret
- 'token': only comprising the token as secret
- 'aws-s3': with properties 'key-id', 'session', 'expiration', and the
  secret_id as the credential secret

Legacy support

DataLad credentials not configured via this command may not be fully
discoverable (i.e., including all their properties). Discovery of
such legacy credentials can be assisted by specifying a dedicated
'type' property.

*Examples*

Report all discoverable credentials::

   % datalad credentials

Set a new credential mycred & input its secret interactively::

   % datalad credentials set mycred

Remove a credential's type property::

   % datalad credentials set mycred :type

Get all information on a specific credential in a structured record::

   % datalad -f json credentials get mycred

Upgrade a legacy credential by annotating it with a 'type' property::

   % datalad credentials set legacycred type=user_password

Obtain a (possibly yet undefined) credential with a minimum set of
properties. All missing properties and secret will be prompted for, no
information will be stored! This is mostly useful for ensuring
availability of an appropriate credential in an application context::

   % datalad credentials --prompt 'can I haz info plz?' get newcred :newproperty




Options
-------
{query|get|set|remove}
~~~~~~~~~~~~~~~~~~~~~~
which action to perform. Constraints: value must be one of ('query', 'get', 'set', 'remove') [Default: 'query']

[name] [:]property[=value]
~~~~~~~~~~~~~~~~~~~~~~~~~~
specification ofa credential name and credential properties. Properties are either given as name/value pairs or as a property name prefixed by a colon. Properties prefixed with a colon indicate a property to be deleted (action 'set'), or a property to be entered interactively, when no value is set yet, and a prompt text is given (action 'get'). All property names are case-insensitive, must start with a letter or a digit, and may only contain '-' apart from these characters. [PY: Property specifications should be given a as dictionary, e.g., spec={'type': 'user_password'}. However, a CLI-like list of string arguments is also supported, e.g., spec=['type=user_password'] PY].

**-h**, **--help**, **--help-np**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
show this help message. --help-np forcefully disables the use of a pager for displaying the help message

**--prompt** *PROMPT*
~~~~~~~~~~~~~~~~~~~~~
message to display when entry of missing credential properties is required for action 'get'. This can be used to present information on the nature of a credential and for instructions on how to obtain a credential. Constraints: value must be a string or value must be NONE

**-d** *DATASET*, **--dataset** *DATASET*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
specify a dataset whose configuration to inspect rather than the global (user) settings. Constraints: Value must be a Dataset or a valid identifier of a Dataset (e.g. a path) or value must be NONE

**--version**
~~~~~~~~~~~~~
show the module and its version which provides the command

Authors
-------
datalad is developed by The DataLad Team and Contributors <team@datalad.org>.
