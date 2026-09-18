# Open debts

Every item this project owes itself, in one place, because `tools/lookback.py` prints this file
and `tools/commit.py` refuses a sixth work unit without a lookback. That is the whole mechanism:
the list is spoken on a schedule nobody has to remember.

It exists because prose debts do not work. In the project this template was distilled from, three
items sat in a diligently written log, unread, for hundreds of work units. They were not
forgotten. They were recorded and never looked at again.

Format: `- [ ] (id) owner | opened #N | what it is`
Close by changing `[ ]` to `[x]` and appending ` | closed #M`. Do not delete closed lines: an item
dropped on purpose is evidence, and one that keeps reopening is a finding.

`owner: user` (or a collaborator's name) means it is not yours to start. List it anyway. An item
nobody can start and nobody can see is worse than one blocked in the open.

## Example section, replace with your own

- [ ] (t01) me | opened #1 | [Replace: something this project owes itself, stated so that a
      stranger could tell whether it is done]
