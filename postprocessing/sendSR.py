from pynetdicom.sop_class import ComprehensiveSRStorage
from pynetdicom import AE
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import config

def sendSR(ds):
    ae = AE()
    # Add a requested presentation context
    ae.add_requested_context(ComprehensiveSRStorage)
    assoc = ae.associate(config.pacsIP, config.pacsPort)
    if assoc.is_established:
        # Use the C-STORE service to send the dataset
        # returns the response status as a pydicom Dataset
        status = assoc.send_c_store(ds)

        # Check the status of the storage request
        if status:
            # If the storage request succeeded this will be 0x0000
            print('C-STORE request status: 0x{0:04x}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')