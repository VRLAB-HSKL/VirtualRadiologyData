from pydicom.dataset import Dataset

from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

#debug_logger()


def cfind(patname="", patid="", query='PATIENT', studyid=""):
    ae = AE()
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

    # Create our Identifier (query) dataset
    ds = Dataset()
    ds.QueryRetrieveLevel = query
    ds.PatientName = patname
    ds.PatientID = patid
    ds.PatientSex = ''
    ds.PatientBirthDate = ''
    ds.StudyInstanceUID = studyid
    ds.StudyDescription = ''
    ds.StudyDate = ''
    ds.Modality = ''

    ds.SeriesInstanceUID = ''
    ds.SeriesDate = ''
    ds.SeriesTime = ''
    ds.SeriesDescription = ''
    ds.BodyPartExamined = ''

    # Associate with the peer AE at IP 127.0.0.1 and port 11112
    assoc = ae.associate("10.0.184.148", 4242)
    if assoc.is_established:
        # Send the C-FIND request
        responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
        return responses

        """
        for (status, identifier) in responses:
            if status:
                print('C-FIND query status: 0x{0:04X}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')
        """

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')
