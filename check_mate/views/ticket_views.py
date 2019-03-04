# when the first ticket is added to a project, set the project status to active, set ticket status to not started
# When task is added to a ticket keep status as not started, until a task is set to active, or the ticket settings are manually overwritten
# While tasks are active in ticket, keep ticket status set to active
# Once all tasks are marked as complete, update ticket status to complete

# Given a user is authenticated
# When the user is viewing a project board
# And it's associated issue tickets
# Then they should be able to select an issue ticket to open up the detail view

# When the user selects the ticket detail view
# Then they should be able to see the ticket name, description, status, completion status bar, assigned team member, activity history, and all associated tasks
# And they should be given an affordance to add a new related task

# Given a user is authenticated
# When the user is viewing the project board
# Then the user should be able to view all tickets associated with that project and their status
# And they should be given an affordance to add a new issue ticket

# When the user selects the option to add a new issue ticket
# Then they should be presented with a form, where they can provide information about the task such as name, description, status and assigned team member

# When the user submits the form
# If the data is valid, they will be taken to the ticket detail page
# If the data is not valid, they will be shown an error message on the form and asked to supply valid data

# Given a user is authenticated
# When the user is viewing a issue ticket detail view
# Then the user should be able to view all details of the ticket, including name, description, ticket status, completion status bar, ticket history and all related tasks
# And they should be given an affordance to edit the details of the issue ticket

# When the user selects the option to edit ticket details
# Then they should be presented with a form, that is pre-populated with existing ticket data, where they can update information about the task such as name, description, status and assigned team member

# When the user submits the form
# If the data is valid, they will be taken back to the updated ticket detail page
# If the data is not valid, they will be shown an error message on the form and asked to supply valid data