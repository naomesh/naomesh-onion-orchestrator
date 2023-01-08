import logging
import enoslib as en

def reserve(site: str):
    en.init_logging(level=logging.INFO)
    en.check()
    
    en.g5k
    
    CLUSTER = "paravance"
    SITE = en.g5k_api_utils.get_cluster_site(CLUSTER)
    
    prod_network = en.G5kNetworkConf(
        roles=["mynetwork"],
        type="prod",
        site=SITE
    )
    
    conf = (
        en.G5kConf()
            .add_network_conf(prod_network)
            .add_machine(cluster=CLUSTER, nodes=1, roles=["compute"], primary_network=prod_network)
            .finalize()
    )

    print(conf)
    provider = en.G5k(conf)
    roles, networks = provider.init()
    
    print(roles)
    print(networks)
    
    provider.destroy()