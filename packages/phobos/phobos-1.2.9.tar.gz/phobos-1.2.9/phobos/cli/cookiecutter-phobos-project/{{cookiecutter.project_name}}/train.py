import os
import logging

from polyaxon.tracking import Run

import torch 

from phobos import Runner
from phobos import Grain

logging.basicConfig(level=logging.WARNING)

################### Polyaxon / Local ###################
"""
Initialization to use datalab or local system for training.
"""

experiment = None
if not Runner.local_testing():
    experiment = Run()


################### Polyaxon / Local ###################

################### Arguments ###################

"""Initialize all arguments passed via metadata.json
"""
args = Grain(yaml_file='metadata.yaml', polyaxon_exp=experiment)

################### Arguments ###################

weights_dir = args.run.checkpoint_path

if not Runner.local_testing():
    weights_dir = os.path.join(experiment.get_artifacts_path(), 'checkpoints')

if not os.path.exists(weights_dir):
    os.makedirs(weights_dir)

################### Intialize Runner ###################

runner = Runner(args, polyaxon_exp=experiment)

################### Intialize Runner ###################

################### Train ###################
"""Dice coeffiecient is used to select best model weights.
Use metric as you think is best for your problem.
"""

best_val = -1e5
best_metrics = None

logging.info('STARTING training')

for step, outputs in runner.trainer():
    if runner.master():
        print(f'step: {step}')
        outputs.print()

        val_recall = runner.tracking.track_outputs["label"].means['val_metrics']['recall']
        if val_recall > best_val:
            best_val = val_recall
            cpt_path = os.path.join(weights_dir,
                                    'checkpoint_epoch_'+ str(step) + '.pt')
            state_dict = runner.model.module.state_dict() if runner.args.distributed \
                else runner.model.state_dict()
            torch.save(state_dict, cpt_path)

################### Train ###################