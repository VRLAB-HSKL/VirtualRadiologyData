from pydicom.dataset import Dataset

from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

#debug_logger()


def cfind(server, ds):
    ae = AE()
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

    # Create our Identifier (query) dataset

    # Associate with the peer AE at IP 127.0.0.1 and port 11112
    assoc = ae.associate(server, 4242)
    if assoc.is_established:
        # Send the C-FIND request
        responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
        liste = []

        for (status, identifier) in responses:
            if status:
                if status.Status > 0:
                    liste.append(identifier)

        # Release the association
        assoc.release()
        return liste

    else:
        print('Association rejected, aborted or never connected')
