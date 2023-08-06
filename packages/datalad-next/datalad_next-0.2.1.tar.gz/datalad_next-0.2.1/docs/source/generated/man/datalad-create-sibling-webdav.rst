.. _man_datalad-create-sibling-webdav:

datalad create-sibling-webdav
=============================

Synopsis
--------
::

  datalad create-sibling-webdav [-h] [-d DATASET] [-s NAME] [--storage-name NAME] [--mode {annex|filetree|annex-only|filetree-only|git-only}] [--credential NAME] [--existing {skip|error|reconfigure}] [-r] [-R LEVELS] [--version] URL


Description
-----------
Create a sibling(-tandem) on a WebDAV server

WebDAV is standard HTTP protocol extension for placing files on a server
that is supported by a number of commercial storage services (e.g.
4shared.com, box.com), but also instances of cloud-storage solutions like
Nextcloud or ownCloud. These software packages are also the basis for
some institutional or public cloud storage solutions, such as EUDAT B2DROP.

For basic usage, only the URL with the desired dataset location on a WebDAV
server needs to be specified for creating a sibling. However, the sibling
setup can be flexibly customized (no storage sibling, or only a storage
sibling, multi-version storage, or human-browsable single-version storage).

This command does not check for conflicting content on the WebDAV
server!

When creating siblings recursively for a dataset hierarchy, subdatasets
exports are placed at their corresponding relative paths underneath the
root location on the WebDAV server.


Git-annex implementation details

Storage siblings are presently always configured to be enabled
automatically on cloning a dataset. Due to a limitation of git-annex, this
will initially fails (missing credentials), but a command to properly
enable the storage sibling will be displayed.
See https://github.com/datalad/datalad/issues/6634 for details.

This command does not (and likely will not) support embedding credentials
in the repository (see ``embedcreds`` option of the git-annex ``webdav``
special remote; https://git-annex.branchable.com/special_remotes/webdav),
because such credential copies would need to be updated, whenever they
change or expire. Instead, credentials are retrieved from DataLad's
credential system. In many cases, credentials are determined automatically,
based on the HTTP authentication realm identified by a WebDAV server.

This command does not support setting up encrypted remotes (yet). Neither
for the storage sibling, nor for the regular Git-remote. However, adding
support for it is primarily a matter of extending the API of this command,
and to pass the respective options on to the underlying git-annex
setup.

This command does not support setting up chunking for webdav storage
siblings (https://git-annex.branchable.com/chunking).

*Examples*

Create a WebDAV sibling tandem for storage a dataset's file content
and revision history. A user will be prompted for any required
credentials, if they are not yet known.::

   % datalad create-sibling-webdav "https://webdav.example.com/myds"

Such a dataset can be cloned by DataLad via a specially crafted URL.
Again, credentials are automatically determined, or a user is prompted
to enter them::

   % datalad clone "datalad-annex::?type=webdav&encryption=none&url=https://webdav.example.com/myds"




Options
-------
URL
~~~
URL identifying the sibling root on the target WebDAV server. Constraints: value must be a string

**-h**, **--help**, **--help-np**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
show this help message. --help-np forcefully disables the use of a pager for displaying the help message

**-d** *DATASET*, **--dataset** *DATASET*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
specify the dataset to process. If no dataset is given, an attempt is made to identify the dataset based on the current working directory. Constraints: Value must be a Dataset or a valid identifier of a Dataset (e.g. a path) or value must be NONE

**-s** NAME, **--name** NAME
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
name of the sibling. If none is given, the hostname-part of the WebDAV URL will be used. With RECURSIVE, the same name will be used to label all the subdatasets' siblings. Constraints: value must be a string or value must be NONE

**--storage-name** NAME
~~~~~~~~~~~~~~~~~~~~~~~
name of the storage sibling (git-annex special remote). Must not be identical to the sibling name. If not specified, defaults to the sibling name plus '-storage' suffix. If only a storage sibling is created, this setting is ignored, and the primary sibling name is used. Constraints: value must be a string or value must be NONE

**--mode** {annex|filetree|annex-only|filetree-only|git-only}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Siblings can be created in various modes: full-featured sibling tandem, one for a dataset's Git history and one storage sibling to host any number of file versions ('annex'). A single sibling for the Git history only ('git-only'). A single annex sibling for multi-version file storage only ('annex-only'). is an alternative to the standard (annex) storage sibling setup that is capable of storing any number of historical file versions using a content hash layout ('annex'|'annex-only'), the 'filetree' mode can used. This mode offers a human- readable data organization on the WebDAV remote that matches the file tree of a dataset (branch). However, it can, consequently, only store a single version of each file in the file tree. This mode is useful for depositing a single dataset snapshot for consumption without DataLad. The 'filetree' mode nevertheless allows for cloning such a single-version dataset, because the full dataset history can still be pushed to the WebDAV server. Git history hosting can also be turned off for this setup ('filetree-only'). When both a storage sibling and a regular sibling are created together, a publication dependency on the storage sibling is configured for the regular sibling in the local dataset clone. Constraints: value must be one of ('annex', 'filetree', 'annex-only', 'filetree- only', 'git-only') [Default: 'annex']

**--credential** NAME
~~~~~~~~~~~~~~~~~~~~~
name of the credential providing a user/password credential to be used for authorization. The credential can be supplied via configuration setting 'datalad.credential.<name>.user|secret', or environment variable DATALAD_CREDENTIAL_<NAME>_USER|SECRET, or will be queried from the active credential store using the provided name. If none is provided, the last-used credential for the authentication realm associated with the WebDAV URL will be used. Only if a credential name was given, it will be encoded in the URL of the created WebDAV Git remote, credential auto-discovery will be performed on each remote access.

**--existing** {skip|error|reconfigure}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
action to perform, if a (storage) sibling is already configured under the given name. In this case, sibling creation can be skipped ('skip') or the sibling (re-)configured ('reconfigure') in the dataset, or the command be instructed to fail ('error'). Constraints: value must be one of ('skip', 'error', 'reconfigure') [Default: 'error']

**-r**, **--recursive**
~~~~~~~~~~~~~~~~~~~~~~~
if set, recurse into potential subdatasets.

**-R** LEVELS, **--recursion-limit** LEVELS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
limit recursion into subdatasets to the given number of levels. Constraints: value must be convertible to type 'int' or value must be NONE

**--version**
~~~~~~~~~~~~~
show the module and its version which provides the command

Authors
-------
datalad is developed by The DataLad Team and Contributors <team@datalad.org>.
