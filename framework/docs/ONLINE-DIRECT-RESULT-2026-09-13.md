# Direct trainer Online call — 2026-09-13

With the corrected payload active (SHA256 d15581fa...), the CLI command
`trainer.py launch-online` sent mailbox command 9 argument 0. The VM acknowledged
sequence 1 and returned `lastResult=-9` (`freemode transition failed`). Heartbeat
continued from 5078 to 5177; no crash or hang occurred.

An immediate read-only `online-status` then returned signedIn=1,
signedOnline=0, canAccess=0, accessReason=7, gameInProgress=0,
sessionActive=0. This is consistent with the native transition rejecting the
request because bit 2/signed-online is still clear. No flags were forced and no
additional host-session call was sent. The trainer overlay remains closed.

This command path is proven reachable, but it does not bypass Social Club
authentication or create a private LSO session. The next live test should observe
the credential/transition producer or a real request; do not loop launch-online or
blindly set signed-online.
