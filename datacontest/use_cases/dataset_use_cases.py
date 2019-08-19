from datetime import datetime

from datacontest.shared import response_object as res
from datacontest.shared import use_case as uc


class UploadDatathonDataset(uc.UseCase):
    """ Attach a dataset to an existent datathon """

    def __init__(self, datathon_repo, dataset_repo):
        self.datathon_repo = datathon_repo
        self.dataset_repo = dataset_repo

    def process_request(self, request_object):
        """
        Validate:
            datathon exists
            user requesting is the organizer
            datathon has not still started
            size and coherence of the dataset parts
            target_column exists
            datathon metric is compatible
        """

        # datathon exists
        domain_datathon = self.datathon_repo.find_by_id(request_object.datathon_id)
        if domain_datathon is None:
            return res.ResponseFailure.build_resource_error(
                'Datathon not found.'
            )

        # user requesting is the organizer
        if domain_datathon.organizer_id != request_object.user_id:
            return res.ResponseFailure.build_authentication_error(
                'Only the organizer of a datathon can upload a dataset.'
            )

        # datathon has not started yet
        if domain_datathon.start_date <= datetime.now():
            return res.ResponseFailure.build_parameters_error(
                'You can only upload a dataset before the start date.'
            )

        # TODO validate valid b64 files? or in the use case, as other validations?

        identifier = self.dataset_repo.build_primary_key()
        domain_dataset = self.dataset_repo.add(
            id=identifier,
            datathon_id=request_object.datathon_id,
            training=request_object.training,
            validation=request_object.validation,
            test=request_object.test,
            target_column=request_object.target_column,
        )
        if domain_dataset is None:
            return res.ResponseFailure.build_resource_error(
                'Error adding the dataset to the repository'
            )

        return res.ResponseCreationSuccess(domain_dataset)
