# import mdsisclienttools.datastore.ReadWriteHelper as ProvenaRW
from provenaclient.auth import DeviceFlow
from provenaclient import ProvenaClient, Config
from asyncio import run

import typer

# Provena Config
# Replace the domain with the domain of your Provena instance
PROVENA_DOMAIN = "mds.gbrrestoration.org"
REALM_NAME = "rrap"
KC_ENDPOINT = f"auth.{PROVENA_DOMAIN}/auth/realms/{REALM_NAME}"
PROVENA_CLIENT_ID = "automated-access"

app = typer.Typer()

@app.command(help="Download a dataset from the M&DS datastore")
def download(
    dest: str,
    dataset_id: str
) -> None:
    """Download a dataset from the M&DS IS data store.

       Parameters
       ----------
       destination_path: str, output location of downloaded dataset
       dataset_id: str, dataset id of the connectivity matrices
    """

    # setup auth and provena client
    auth = DeviceFlow(
        keycloak_endpoint=KC_ENDPOINT,
        client_id=PROVENA_CLIENT_ID
    )
    client = ProvenaClient(
        auth=auth,
        config=Config(
            domain=PROVENA_DOMAIN,
            realm_name=REALM_NAME
        )
    )
    
    run(client.datastore.io.download_all_files(
        destination_directory=dest,
        dataset_id=dataset_id
    ))