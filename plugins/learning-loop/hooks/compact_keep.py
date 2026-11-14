"""PreCompact hook: tells Claude what to keep when it shortens a long conversation.

Claude Code adds this script's printed text to its summary instructions. It never writes
a handover note: notes written automatically at this point proved useless.
"""
import sys

print(
    "When summarising, keep what the handover skill needs, in plain words: the current state of the work and how "
    "each part was checked (the commands and their results); decisions made and why; approaches tried and dropped; "
    "anything the person corrected; anything left only in a temporary place (scratch folders, uncommitted or "
    "unpushed work), with where it is; the person's own pending steps; and lessons noted for the handover. "
    "Keep names and roles exactly as people gave them. Do not write a handover note because of this summary."
)
sys.exit(0)
