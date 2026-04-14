import ast

[ast.parse(open(f).read()) for f in ['src/verl/verl/separated_trainer/ppo/archive_pool.py', 'src/verl/verl/utils/reward_score/game.py', 'src/verl/verl/workers/reward_manager/game.py',
  'src/verl/verl/separated_trainer/ppo/ray_trainer.py']]

print('All syntax OK')