from datacontest.shared import response_object as res
from datacontest.shared import use_case as uc


class DatathonListUseCase(uc.UseCase):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        domain_datathons = self.repo.list(filters=request_object.filters)
        return res.ResponseSuccess(domain_datathons)


class DatathonDetailUseCase(uc.UseCase):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        domain_datathon = self.repo.find_by_id(request_object.id)
        if domain_datathon is None:
            return res.ResponseFailure.build_resource_error('Id not found')

        return res.ResponseSuccess(domain_datathon)


class CreateDatathonUseCase(uc.UseCase):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        identifier = self.repo.build_primary_key()
        domain_datathon = self.repo.add(id=identifier,
                                        title=request_object.title,
                                        subtitle=request_object.subtitle,
                                        description=request_object.description,
                                        metric=request_object.metric,
                                        organizer_id=request_object.organizer_id,
                                        end_date=request_object.end_date)
        if domain_datathon is None:
            return res.ResponseFailure.build_resource_error(
                'Error adding the datathon to the repository'
            )

        return res.ResponseCreationSuccess(domain_datathon)


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
            return res.ResponseFailure.build_parameters_error(
                'Datathon not found while adding a dataset'
            )

        # user requesting is the organizer
        if domain_datathon.organizer_id != request_object.user_id:
            return res.ResponseFailure.build_authorization_error(
                'Only the organizer of a datathon can upload a dataset'
            )

        # 

        identifier = self.dataset_repo.build_primary_key()
        domain_dataset = self.dataset_repo.add(
            id=identifier,
            datathon_id=request_object.title,
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
