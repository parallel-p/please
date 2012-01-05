import os

for dir in os.walk('.'):
  if not os.path.exists(os.path.join(dir[0],'__init__.py')) and not '.svn' in dir[0]:
    with open(os.path.join(dir[0], '__init__.py'), 'w'):
      pass
    print(dir[0])
    os.system('svn add ' + os.path.join(dir[0], '__init__.py'))
