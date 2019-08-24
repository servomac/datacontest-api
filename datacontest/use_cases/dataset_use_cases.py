from datetime import datetime

from datacontest.shared import response_object as res
from datacontest.shared import use_case as uc


class UploadDatathonDataset(uc.UseCase):
    """ Attach a dataset to an existent datathon """

    def __init__(self, datathon_repo, dataset_repo):
        self.datathon_repo = datathon_repo
        self.dataset_repo = dataset_repo

    def process_request(self, request_object):
        # validate datathon exists
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
        # validate target colum exists

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


class DatasetDetailUseCase(uc.UseCase):
    """ Obtain the dataset of a datathon """

    def __init__(self, datathon_repo, dataset_repo):
        self.datathon_repo = datathon_repo
        self.dataset_repo = dataset_repo

    def _hide_test_set(self, dataset):
        dataset.test = 'Hidden'
        return dataset

    def process_request(self, request_object):
        # validate datathon exists
        domain_datathon = self.datathon_repo.find_by_id(request_object.datathon_id)
        if domain_datathon is None:
            return res.ResponseFailure.build_resource_error(
                'Datathon not found.'
            )

        # TODO only a valid dataset, with the current implementation
        #  of upload dataset i can upload N datasets
        datasets = self.dataset_repo.find_by('datathon_id', request_object.datathon_id)

        is_organizer = (domain_datathon.organizer_id == request_object.user_id)
        if is_organizer:
            return res.ResponseSuccess(datasets)

        # datathon is running
        now = datetime.now()
        if domain_datathon.start_date <= now <= domain_datathon.end_date:
            return res.ResponseSuccess([self._hide_test_set(d) for d in datasets])

        # datathon has ended
        if domain_datathon.end_date <= now:
            return res.ResponseSuccess(datasets)

        return res.ResponseFailure.build_resource_error(
            'Datathon has not started yet!'
        )