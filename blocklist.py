"""
blocklist.py

This file just contains blocklist of jwt tokens. It will be imported by the app and the logout resource so that after logging out,
the same token cannot be used again. This will happen by adding the token to this blocklist at the time of logout.

NOTE: We are currently using just a set to test this but set resets everytime you restart the app so the old tokens will actually be valid in this case
but that won't happen when you use database to maintain this blocklist. Hence using a database for blocklist is recommended
"""
BLOCKLIST = set()