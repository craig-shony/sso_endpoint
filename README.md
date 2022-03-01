# sso_endpoint

Assignment for Security Engineer position at Parsley Health

## Problem Statement

For requests from one web application in particular, named senior-parsley, we need to be
able to apply certain rules. When the following conditions are met:
claim auth-provider == SSO
AND
claim email contains @parsleyhealth.com as an email suffix.
The GraphQL endpoint will return a valid JSON response (you can use any sample schema you
choose). If the conditions are NOT met, return a 401 and take any appropriate action.

## Included

1. A flask app to handle one endpoint "/sso"
2. JWT generator to handle test cases
3. Simulated client for testing

## Security Controls
1. Signed JWTs
2. Rate limiting
3. Expiry
4. **Not Included:** Vault protection for signing keys

## Testing Document
Matches parameters for tokenGen() function for test cases
1. valid sso request
2. user-pass request
3. non-parsleyhealth request
4. email fuzzing
5. expired JWT
