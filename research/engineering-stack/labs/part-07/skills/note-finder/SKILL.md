---
name: note-finder
description: Finds team notes that mention a word and quotes them with their note IDs. Use when someone asks what the notes say about a service, owner or schedule. Not for adding or deleting notes.
license: MIT
metadata:
  author: lab
  version: "0.7"
---

# Note finder

1. Call the `search_notes` tool with one word from the question.
2. Quote each matching note with its ID, such as [n2].
3. If nothing matches, say so; don't guess.
