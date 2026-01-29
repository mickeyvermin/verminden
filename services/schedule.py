# TODO:
#  - Merge schedules/events
#  - Extend events
#  - Create events
#  - Edit events
#  - Recurring events (every X days or on specific date of every month,...)


# Events should have version number
# Groups cache their members' version numbers
# Every time a member click on group schedule, a check is ran that checks if the cached
# versions of every corresponding member is the same as the current version of every member.
# If any difference is detected, fetch every person's current version number and cache that
# as new version numbers then adjust the group schedule accordingly.
async def merge_schedule_service(group_id: int, create):