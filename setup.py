import os

"""
Set up the repository to be found by the Python interpreter.

Opens `.bashrc` and appends the repository's root directory to PYTHONPATH.
"""

print('setup...')
repository_path = os.path.dirname(os.path.realpath(__file__))
bashrc_path = os.environ['HOME'] + '/.bashrc'

print('appending {} to ~/.bashrc ...'.format(repository_path))
f = open(bashrc_path, 'a')
f.write('\n\n\n## setup `quasistatic_process` ##\n')
f.write('export PYTHONPATH={}:${}\n'.format(repository_path, '{PYTHONPATH}'))
f.write('## end setup ##\n\n\n')
f.close()

print('setup completed')
