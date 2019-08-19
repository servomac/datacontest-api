
## Technical/Architectural Backlog

 * Response Object
   - Not a unique message, but the possibility to express more than a unique error (i.e. multiple fields not provided to a use case, as in `test_user_registration_without_parameters`)

 * JWT logic
   - Should be separated from our User domain model. Separation of concerns. Also separate configuration (secret, algorithm).
   - ~~In REST API, the authorization should come as headers in the petition, not passing the token as part of the request json body~~.

 * Schema validation. The actual schema validation seems to be ocurring at the use case request objects level. Rethink.

 * Repositories should be part of the Config object, instead of global vars in rest files?

## Feature Backlog

 * ~~(Bug) Validate datathon start and end date are in the future~~

 * An organizer can upload a dataset to a datathon
   - ~~Only before the start date~~
   - The dataset gets -synchronously- validated
   - An authenticated used can download the dataset, but not test file (only the organizer can)

 * An authenticated user can send submissions to a datathon
   - Only when is open -between start and end date-
   - An organized can not send submissions

 * The submissions get evaluated asynchronously and can be listed
