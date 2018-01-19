
 * Response Object
   - Not a unique message, but the possibility to express more than a unique error (i.e. multiple fields not provided to a use case, as in `test_user_registration_without_parameters`)

 * JWT logic
   - Should be separated from our User domain model. Separation of concerns. Also separate configuration (secret, algorithm).

 * Schema validation. The actual schema validation seems to be ocurring at the use case request objects level. Rethink.