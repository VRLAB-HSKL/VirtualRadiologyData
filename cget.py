# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 06:24:31 2021

@author: Rafael
"""

from pydicom.dataset import Dataset
from pydicom.uid import UID
from pynetdicom import AE, evt, build_role, debug_logger
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelGet,
    CTImageStorage, ComputedRadiographyImageStorage
)

#debug_logger()


# Implement the handler for evt.EVT_C_STORE
def handle_store(event):
    """Handle a C-STORE request event."""
    ds = event.dataset
    ds.file_meta = event.file_meta

    instanceList.append(ds)
    #print(len(instanceList))
    #print("______________________________________")

    # Return a 'Success' status
    return 0x0000


def c_get(seriesid, modality):
    handlers = [(evt.EVT_C_STORE, handle_store)]

    # Initialise the Application Entity
    ae = AE()

    # Add the requested presentation contexts (QR SCU)
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelGet)
    # Add the requested presentation context (Storage SCP)
    if modality == 'CT':
        ae.add_requested_context(CTImageStorage)
        role = build_role(CTImageStorage, scp_role=True)
    if modality == 'CR':
        ae.add_requested_context(ComputedRadiographyImageStorage)
        role = build_role(ComputedRadiographyImageStorage, scp_role=True)


    # Create our Identifier (query) dataset
    # We need to supply a Unique Key Attribute for each level above the
    #   Query/Retrieve level
    ds = Dataset()
    ds.QueryRetrieveLevel = 'SERIES'
    # Unique key for PATIENT level
    ds.PatientID = ''  # NOID
    # Unique key for STUDY level
    ds.StudyInstanceUID = ''
    # Unique key for SERIES level
    ds.SeriesInstanceUID = seriesid

    # Associate with peer AE at IP 127.0.0.1 and port 4242
    assoc = ae.associate('10.0.184.148', 4242, ext_neg=[role], evt_handlers=handlers)

    if assoc.is_established:
        # Use the C-GET service to send the identifier
        responses = assoc.send_c_get(ds, PatientRootQueryRetrieveInformationModelGet)
        for (status, identifier) in responses:
            if status:
                print('C-GET query status: 0x{0:04x}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')

                # Release the association
                assoc.release()
    else:
        print('Association rejected, aborted or never connected')


def imagelist(seriesid, modality):
    global instanceList
    instanceList = []
    c_get(seriesid, modality)
    return instanceList
