from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from accounts.models import MyUser

'''
		This command were designed to make groups named 'normal_users' and 'managers' in order to manage 
	different permissions per group.
'''

class Command(BaseCommand):
	help = 'Create a new group'

	def add_arguments(self, parser):
		# Positional arguments
		parser.add_argument(
			'--groupname',
			dest='groupname', 
			nargs=1, 
			type=str)

		# Named (optional) arguments
		parser.add_argument(
			'--permission',
			dest='permission',
			nargs='*',
		)

	# handle() method must me implemented.
	def handle(self, *args, **options):
		## Group_name(must), permissions(optional) should be given.
		group_name = options['groupname'][0]
		group = Group.objects.create(name=group_name)
		permission_list = options['permission']
#		<NOTE>
#		There should be a process of finding permissions & setting permissions	
#		group.permissions.set(options['permission'])
		self.stdout.write(self.style.SUCCESS('Successfully created a group named %s' % group_name))
		self.stdout.write(self.style.SUCCESS('Successfully granted permissions: %s' % ', '.join(permission_list)))



'''
	- BaseCommand.help 
	: A short description of the command, which will be printed in the help message when the user runs the command:
		 python manage.py help <command>
	
	- BaseCommand.add_arguments(parser)
	: Custom commands should override this method to add both positional and optional arguments accepted by the command.

	- BaseCommand.handle(*args, **options)
	: The actual logic of the command. Subclasses must implement this method.
	: It may return a Unicode string which will be printed to stdout.


	<nargs>
	- The "nargs" keyword argument associates a different number of command-line arguments with a single action.
	- N (an integer). N arguments from the command line will be gathered together into a list. 
		nargs='*'
		: All command-line arguments present are gathered into a list. 
		: Note that ait doesn't make much sense to have more than one positional argument with nargs='*', but multiple optional arguments with nargs='*' is possible.

	<dest>
	Most ArgumentParser actions add some value as an attribute of the object returned by parse_args().
	The name of this attribute is determined by the "dest" keyword argument of add_argument().
	For positional argument actions, "dest" is normally supplied as the first argument to add_argument():

	<action>
	The "action" keyword argument specifies how the command-line arguments should be handled.
		'append'
		: This stores a list, and appends each argument value to the list. 
		: This is useful to allow an option to be specified multiple times.

	<metavar>
	string presenting available sub-commands in help; by default it is None and presents sub-commands in form {cmd1, cmd2, ...}	

'''
