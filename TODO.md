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
- [ ] (t02) me | opened #8 | `commit.py` loses a parked message when a second message is piped in while one is parked. It bit twice in one session: pipe B while A is parked and A is gone, silently. Refuse the new message, or park under a second name, or print what is being overwritten
- [ ] (t03) me | opened #22 | `commit.py --parked` commits the parked message against whatever is staged now, which need not be what was staged when it was parked. It produced two commits today whose message and diff do not match, in two repositories. Record the staged file list alongside the parked message and refuse when it has changed
