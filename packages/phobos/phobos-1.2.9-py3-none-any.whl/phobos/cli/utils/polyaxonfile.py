def getExpConfigs(meta):
    project, deployment = meta['project'], meta['deployment']

    expmap = getExperimentsMap(project)
    polymap = getPolyAxonFileMap(deployment)
    url = deployment['url']

    return expmap, polymap, url

def getPolyAxonFileMap(meta):
    pmeta = meta['run']

    distributed = meta['distributed']

    polymap = {}

    polymap['version'] = 1.1
    polymap['kind'] = 'component'
    polymap['name'] = meta['name']

    run = {}
    container = {}
    container['name'] = meta['name']
    container['image'] = pmeta['container']['image']
    container['command'] = ['/bin/bash', 'run.sh']
    
    container['resources'] = {}
    
    container['resources']['limits'] = {}
    container['resources']['requests'] = {}

    container['resources']['limits']['nvidia.com/gpu'] = pmeta['container']['resources']['limits']
    container['resources']['requests']['nvidia.com/gpu'] = pmeta['container']['resources']['requests']

    container['workingDir'] = '{{ globals.run_artifacts_path }}/code'

    environment = {}
    environment['nodeSelector'] = {}
    environment['nodeSelector']['arche'] = pmeta['nodepool']

    if not distributed:
        run['kind'] = 'job' if not pmeta['kind'] else pmeta['kind']
        run['connections'] = pmeta['connections']
        run['container'] = container
        run['environment'] = environment
    else:
        run['cleanPodPolicy'] = 'All'
        run['kind'] = 'pytorchjob' if not pmeta['kind'] else pmeta['kind']

        master, worker = {}, {}
        master['connections'] = pmeta['connections']
        worker['connections'] = pmeta['connections']
        master['container'] = container
        worker['container'] = container

        master['environment'] = environment
        worker['environment'] = environment

        master['replicas'] = pmeta['replicas']['master']
        worker['replicas'] = pmeta['replicas']['worker']

        run['master'] = master
        run['worker'] = worker

    polymap['run'] = run

    return polymap

def getExperimentsMap(meta):
    expmap = {}

    expmap['name'] = meta['name']
    expmap['description'] = meta['description']
    if len(meta['tags']) > 0:
        expmap['tags'] = meta['tags']
        
    return expmap