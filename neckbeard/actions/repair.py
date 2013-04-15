
@task
@notifies_hipchat(start_msg=REPAIR_START_MSG, end_msg=REPAIR_END_MSG)
def repair(force='n'):
    """
    Ensure that all healthy active-generation nodes are operational.
    """
    require('_deployment_name')
    require('_deployment_confs')
    require('_active_gen')

    force = force == 'y'

    assert env._active_gen
    deployment = Deployment(
        env._deployment_name,
        env._deployment_confs['ec2'],
        env._deployment_confs['rds'],
        env._deployment_confs['elb'],
    )
    deployment.verify_deployment_state()

    activated_nodes = deployment.repair_active_generation(
        force_operational=force)

    if len(activated_nodes):
        logger.info("Succesfully made %s node(s) operational",
                    len(activated_nodes))
    else:
        logger.info("No nodes modified")
