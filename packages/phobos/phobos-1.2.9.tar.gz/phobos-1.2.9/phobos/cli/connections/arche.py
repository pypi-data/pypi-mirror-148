import os
from functools import partial

import polyaxon_sdk
from polyaxon.client import PolyaxonClient, RunClient
from polyaxon.schemas.cli.client_config import ClientConfig
from polyaxon.polyaxonfile import check_polyaxonfile
from polyaxon.managers.ignore import IgnoreConfigManager


_USER = "default"

__all__ = ["Arche"]

class Arche:
    def __init__(self, url):
        self.client = PolyaxonClient(
            config = ClientConfig(
                host=url,
                use_https=None,
                verify_ssl=None
            )
        )
        
        #partials
        self.listProjects = partial(self.client.projects_v1.list_project_names, owner=_USER)
        self.getProject = partial(self.client.projects_v1.get_project, owner=_USER)
        self.createProject = partial(self.client.projects_v1.create_project, owner=_USER)

    def checkProject(self, project):
        try:
            _ = self.listProjects()
        except:
            print("Unable to connect to Arche")
        # step 2: check if project already exists
        try:
            resp = self.getProject(name=project['name'])
            if resp.to_dict()['uuid']:
                print(f"Found {project['name']} on Arche!")
                return True
            else:
                print("Unknown Exception")
        except:
            # project does not exist, Create new project
            print("Project not found on Arche!")
            try:
                resp = self.createProject(
                    body = project
                )
                if resp.to_dict()['uuid']:
                    print(f"Project: {project['name']} created on Arche...")
                    return True
                else:
                    print("Unknown Exception")
            except:
                print(f"Unable to retreive or create project: {project['name']} on Arche :(")
                return False
        return False
    
    def createRun(self, project, polyaxon_file, **kwargs):
        # step 1: Able to connect to Arche
        
        if not self.checkProject(project):
            return
        
        print("Creating new run ...")
        runClient = RunClient(
            owner = _USER,
            project = project['name'],
            client = self.client
        )
        try:
            op_spec = check_polyaxonfile(
                polyaxonfile=polyaxon_file,
                params=None,
                presets=None,
                queue=None,
                nocache=None,
                cache=None,
                verbose=False,
                is_cli=False,
            )
            content = polyaxon_sdk.V1OperationBody(
                content=op_spec.to_dict(dump=True),
                is_managed=True,
                pending=polyaxon_sdk.V1RunPending.APPROVAL
            )
            resp = runClient._create(content)
            if resp.to_dict()['uuid']:
                print(f"Run: {resp.to_dict()['uuid']} created successfully!")
                dir_ = os.curdir
                files = IgnoreConfigManager.get_unignored_filepaths(dir_)
                resp = runClient.upload_artifacts(
                    files=files,
                    path="code",
                    overwrite=True,
                    relative_to=None
                )
                resp = runClient.upload_artifacts_dir('./', path='code')
                if resp.status_code != 200:
                    runClient.delete()
                    print("Unable to upload Artifacts!")
                runClient.approve()
                print(f"Started run: {runClient.run_uuid} on Arche...")
            else:
                print("Run error")
                return
        except:
            print("Error in running the experiment on Arche")
            return

    def run_tensorboard(self, project, uuid):
        '''Runs tensorboard integration to polyaxon'''
        
        if not self.checkProject(project):
            return

        runClient = RunClient(
            owner = _USER,
            project = project['name'],
            client = self.client
        )

        if len(uuid) == 1:
            try:
                resp = runClient.create_from_hub(component='tensorboard', params={
                    'uuid': uuid[0]
                })
                print(f"Tensorboard running with UUID: {resp.to_dict()['uuid']}")
            except:
                print("Failed to start Tensorboard")
        else:
            try:
                resp = runClient.create_from_hub(component='tensorboard:multi-run', params={
                    'uuids': list(uuid)
                })
                print(f"Tensorboard running with UUID: {resp.to_dict()['uuid']}")
            except:
                print("Failed to start Tensorboard")