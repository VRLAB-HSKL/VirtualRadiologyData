from pydicom.dataset import Dataset
from pynetdicom import AE, evt, build_role, debug_logger
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelGet,
    CTImageStorage, ComputedRadiographyImageStorage
)
import config
#debug_logger()


# Implement the handler for evt.EVT_C_STORE
def handle_store(event):
    """Handle a C-STORE request event."""
    ds = event.dataset
    ds.file_meta = event.file_meta

    instanceList.append(ds)

    # Return a 'Success' status
    return 0x0000


def c_get(seriesid):
    handlers = [(evt.EVT_C_STORE, handle_store)]

    # Initialise the Application Entity
    ae = AE()

    # Add the requested presentation contexts (QR SCU)
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelGet)
    # Add the requested presentation context (Storage SCP)
    ae.add_requested_context(CTImageStorage)
    role = build_role(CTImageStorage, scp_role=True)

    # Create our Identifier (query) dataset
    # We need to supply a Unique Key Attribute for each level above the
    #   Query/Retrieve level
    ds = Dataset()
    ds.QueryRetrieveLevel = 'SERIES'
    # Unique key for PATIENT level
    #ds.PatientID = ''  # NOID
    # Unique key for STUDY level
    #ds.StudyInstanceUID = ''
    # Unique key for SERIES level
    ds.SeriesInstanceUID = seriesid
    # Associate with peer AE at IP 127.0.0.1 and port 4242
    print(f"{config.pacsIP = }, {config.pacsPort = }")
    assoc = ae.associate(config.pacsIP, config.pacsPort, ext_neg=[role], evt_handlers=handlers)

    if assoc.is_established:
        # Use the C-GET service to send the identifier
        responses = assoc.send_c_get(ds, PatientRootQueryRetrieveInformationModelGet)
        for (status, identifier) in responses:
            if not status:
                print('Connection timed out, was aborted or received invalid response')

                # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')


def imagelist(seriesid):
    global instanceList
    instanceList = []
    c_get(seriesid)
    instanceList.sort(key=lambda i: i.ImagePositionPatient[2], reverse=True)
    return instanceList
